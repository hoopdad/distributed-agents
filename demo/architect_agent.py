"""Architect: read assigned Blob requirements, generate a design, and save its candidate artifact."""

from __future__ import annotations

import asyncio
import time
from contextlib import AsyncExitStack

from agent_framework import AgentSession, SessionStore
from agent_framework.foundry import FoundryChatClient
from agent_framework_foundry_hosting import AgentSessionStoreProvider
from azure.ai.agentserver.core import AgentConfig, FoundryAgentRequestContext
from azure.core.pipeline.transport import AioHttpTransport
from azure.identity.aio import ManagedIdentityCredential
from azure.storage.blob.aio import BlobServiceClient

from .artifact_store import BlobArtifacts, validate_storage_configuration
from .artifacts import (
    Artifact, ArtifactError, ArtifactRef, Assignment, AssignmentLocator, Candidate, Container, OutputLocator, ScopeBinding,
    canonical_bytes, decode_document, digest,
)
from .config import required
from .contracts import Candidate as SessionCandidate
from .foundry import ProjectClient, data_client
from .specialist import SpecialistAgent


class ArchitectAgent(SpecialistAgent):
    def __init__(self, *, artifact_mode: bool = False, **kwargs):
        super().__init__(
            role="architect", artifact_mode=artifact_mode,
            schema=Candidate if artifact_mode else SessionCandidate,
            guidance=(
                "Produce a complete candidate, revising blocking findings. Keep design concise and "
                "implementation-ready; design must be at most 10000 characters. Do not add open "
                "questions or TODO placeholders when you can provide a concrete design decision."
            ),
            **kwargs,
        )

    @classmethod
    async def run_assignment(
        cls, text: str, *, config: AgentConfig, context: FoundryAgentRequestContext,
        scope: ScopeBinding, response_id: str,
    ) -> str:
        """Read requirements from Azure Blob Storage, generate a design, and save the candidate JSON."""
        async with AsyncExitStack() as stack:
            # STAGE 1: Connect to Azure and load the assignment.
            store, project, headers, assignment, existing_design = await cls.connect_and_load_assignment(
                stack, text, config=config, context=context, scope=scope, response_id=response_id,
            )

            # STAGE 2: Read requirements and any previous design or reviewer findings.
            brief = await cls.read_requirements_and_prior_work(store, assignment)

            # STAGE 3: Load or create the architect's LLM conversation session.
            session_store, session, model_deployment = await cls.load_or_create_llm_session(
                config=config, context=context, assignment=assignment, brief=brief, existing_design=existing_design,
            )
            if existing_design is not None:
                return canonical_bytes(OutputLocator(schema_version=1, artifact_ref=existing_design.ref())).decode()

            # STAGE 4: Design the solution, or recover the model's existing response.
            design_text = await cls.design_solution(
                project=project, headers=headers, assignment=assignment, brief=brief,
                session_store=session_store, session=session, model_deployment=model_deployment,
            )

            # STAGE 5: Validate and store the design, save the session, and return the artifact reference.
            ref = await cls.store_design(
                store=store, assignment=assignment, text=design_text, response_id=response_id,
                session_store=session_store, session=session,
            )
            return canonical_bytes(OutputLocator(schema_version=1, artifact_ref=ref)).decode()

    @staticmethod
    async def connect_and_load_assignment(
        stack: AsyncExitStack, text: str, *, config: AgentConfig, context: FoundryAgentRequestContext,
        scope: ScopeBinding, response_id: str,
    ) -> tuple[BlobArtifacts, ProjectClient, dict[str, str], Assignment, Artifact | None]:
        locator = AssignmentLocator.model_validate(decode_document(text.encode("utf-8")))
        parent = locator.scope_binding
        if parent.project != scope.project or parent.tenant != scope.tenant or parent.principal != scope.principal:
            raise ArtifactError("ASSIGNMENT_RECEIVER")
        credential = await stack.enter_async_context(ManagedIdentityCredential())
        headers = context.platform_headers()
        http = await stack.enter_async_context(data_client(
            expected_call_id=context.call_id, response_id=response_id,
        ))
        # ProjectClient extends the Azure AIProjectClient with exact-origin, no-retry model transport.
        project = await stack.enter_async_context(ProjectClient(credential, http, headers))

        storage_endpoint = required("ARTIFACT_STORAGE_ENDPOINT")
        containers: dict[Container, str] = {
            "control": required("ARTIFACT_CONTROL_CONTAINER"),
            "candidates": required("ARTIFACT_CANDIDATES_CONTAINER"),
            "reviews": required("ARTIFACT_REVIEWS_CONTAINER"),
        }
        private_ips = required("ARTIFACT_PRIVATE_IPS").split(",")
        validate_storage_configuration(storage_endpoint, containers)
        blob_service = await stack.enter_async_context(BlobServiceClient(
            storage_endpoint.rstrip("/"), credential=credential,
            retry_total=0, connection_timeout=10, read_timeout=30,
            logging_enable=False, max_single_get_size=131072,
            transport=AioHttpTransport(use_env_settings=False),
        ))
        # The typed adapter checks scope/hashes and makes output writes immutable; Azure stores the bytes.
        store = BlobArtifacts(
            role="architect", scope=parent, endpoint=storage_endpoint, containers=containers,
            credential=credential, service=blob_service, expected_private_ips=private_ips,
        )
        await store.verify_private_path()
        assignment = await store.read_assignment(locator.operation_id)
        manifest = await store.read_manifest()
        existing_design = await store.read_output(
            artifact_type="candidate", revision=assignment.requirements_revision,
            operation_id=assignment.operation_id,
        )
        assignment.validate_receiver(
            config=config, context=context, manifest=manifest, now=int(time.time()),
            completed_output=existing_design is not None,
        )
        return store, project, headers, assignment, existing_design

    @staticmethod
    async def read_requirements_and_prior_work(store: BlobArtifacts, assignment: Assignment) -> dict[str, object]:
        requirements = await store.read_artifact(assignment.input_refs[0])
        previous_design_and_review = [
            await store.read_artifact(ref) for ref in assignment.input_refs[1:]
        ]
        return {
            "requirements_revision": assignment.requirements_revision,
            "candidate_revision": assignment.candidate_revision,
            "inputs": [
                value.content.model_dump(mode="json")
                for value in [requirements, *previous_design_and_review]
            ],
        }

    @staticmethod
    async def load_or_create_llm_session(
        *, config: AgentConfig, context: FoundryAgentRequestContext, assignment: Assignment,
        brief: dict[str, object], existing_design: Artifact | None,
    ) -> tuple[SessionStore, AgentSession, str]:
        session_store = AgentSessionStoreProvider(store_name="specialist_history_v2").get_store(
            config=config, platform_context=context
        )
        session = await session_store.get("history")
        if session is None:
            session = AgentSession()
        pending = session.state.get("pending_operation")
        model_deployment = required("SPECIALIST_MODEL_DEPLOYMENT")
        if existing_design is not None:
            expected = assignment.producer.model_copy(update={"response_id": existing_design.producer.response_id})
            if (
                existing_design.input_refs != assignment.input_refs or existing_design.producer != expected
                or existing_design.candidate_revision != assignment.candidate_revision
            ):
                raise ArtifactError("SPECIALIST_ARTIFACT_PROVENANCE")
            if pending is not None:
                if (
                    not isinstance(pending, dict) or pending.get("id") != assignment.operation_id
                    or pending.get("input_sha256") != digest(brief)
                    or pending.get("model_deployment") != model_deployment
                ):
                    raise ArtifactError("SPECIALIST_MODEL_EFFECT_UNCERTAIN")
                if pending.get("response_id"):
                    session.service_session_id = pending["response_id"]
                session.state.pop("pending_operation")
                await session_store.set("history", session)
            return session_store, session, model_deployment
        if pending is not None:
            if (
                not isinstance(pending, dict) or pending.get("id") != assignment.operation_id
                or pending.get("input_sha256") != digest(brief) or not pending.get("response_id")
                or pending.get("model_deployment") != model_deployment
            ):
                raise ArtifactError("SPECIALIST_MODEL_EFFECT_UNCERTAIN")
        else:
            session.state["pending_operation"] = {
                "id": assignment.operation_id, "input_sha256": digest(brief),
                "model_deployment": model_deployment, "response_id": None,
            }
            await session_store.set("history", session)
        return session_store, session, model_deployment

    @classmethod
    async def design_solution(
        cls, *, project: ProjectClient, headers: dict[str, str], assignment: Assignment, brief: dict[str, object],
        session_store: SessionStore, session: AgentSession, model_deployment: str,
    ) -> str:
        pending = session.state["pending_operation"]
        agent = cls(
            artifact_mode=True,
            client=FoundryChatClient(
                project_client=project, model=model_deployment, default_headers=headers,
            ),
        )
        if pending["response_id"] is not None:
            recovered = await project.get_openai_client().responses.retrieve(pending["response_id"])
            if recovered.id != pending["response_id"] or recovered.status != "completed" or not recovered.output_text:
                raise ArtifactError("SPECIALIST_MODEL_RECOVERY_INCOMPLETE")
            session.service_session_id = recovered.id
            return recovered.output_text
        async with agent:
            async with asyncio.timeout(max(0, assignment.deadline_epoch - time.time())):
                stream = agent.run(canonical_bytes(brief).decode(), session=session, stream=True)
                async with stream:
                    async for update in stream:
                        if update.response_id:
                            if pending["response_id"] not in (None, update.response_id):
                                raise ArtifactError("SPECIALIST_MODEL_RESPONSE_CHANGED")
                            if pending["response_id"] is None:
                                pending["response_id"] = update.response_id
                                await session_store.set("history", session)
                    response = await stream.get_final_response()
        if response.finish_reason != "stop" or not response.text.strip():
            raise ArtifactError("SPECIALIST_MODEL_INCOMPLETE")
        return response.text

    @staticmethod
    async def store_design(
        *, store: BlobArtifacts, assignment: Assignment, text: str, response_id: str,
        session_store: SessionStore, session: AgentSession,
    ) -> ArtifactRef:
        design = Candidate.model_validate(decode_document(text.encode("utf-8")))
        if (
            design.requirements_revision != assignment.requirements_revision
            or design.candidate_revision != assignment.candidate_revision
            or time.time() > assignment.deadline_epoch
        ):
            raise ArtifactError("SPECIALIST_REVISION_OR_DEADLINE")
        design_artifact = Artifact(
            artifact_type="candidate", scope_binding=assignment.scope_binding, operation_id=assignment.operation_id,
            producer=assignment.producer.model_copy(update={"response_id": response_id}),
            input_refs=assignment.input_refs, requirements_revision=assignment.requirements_revision,
            candidate_revision=assignment.candidate_revision, content=design, content_sha256=digest(design),
        )
        ref = await store.write_artifact(design_artifact)
        session.state.pop("pending_operation")
        await session_store.set("history", session)
        return ref
