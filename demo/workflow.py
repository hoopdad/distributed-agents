"""MAF workflow hosted in Microsoft Foundry:

The host parses each turn, builds a role-specific workflow, then runs the
coordinator graph: requirements -> routing -> effect -> publication -> routing.
Read WorkflowRuntime.begin(), route(), execute(), and publish() in that order;
shared storage, validation, and recovery helpers follow the four lifecycle methods.
Each event opens the shared Blob artifact plane through the role's managed
identity; workflow checkpoints and agent-session history are separate stores.
"""

from __future__ import annotations

import asyncio
import logging
import os
import time
import uuid
from contextlib import AsyncExitStack, asynccontextmanager
from pathlib import Path
from typing import Literal

from agent_framework import Executor, WorkflowBuilder, WorkflowContext, handler
from agent_framework.exceptions import ChatClientException
from agent_framework.foundry import FoundryAgent
from agent_framework_foundry_hosting import (
    HostedResponseRequest, WorkflowTurn,
)
from agent_framework_foundry import FOUNDRY_HOSTED_AGENT_SESSION_ID_KEY
from azure.ai.agentserver.core import AgentConfig, get_request_context
from azure.identity.aio import ManagedIdentityCredential
from pydantic import ValidationError
from .host import context_checkpoint, execution_checkpoint
from .diagnostics import Stage
from . import effect_observation as effects

from .artifact_store import BlobArtifacts, credential_diagnostics_options
from .architect_agent import ArchitectAgent
from .artifacts import (
    Artifact, ArtifactError, ArtifactRef, Assignment, AssignmentLocator, Candidate, ChildBinding, Decision,
    Effect, Manifest, OutputLocator, Producer, Requirements, Review, ScopeBinding,
    canonical_bytes, decode_document, digest,
)
from .config import required
from .contracts import AGENTS, ORIGIN, PROJECT, Child, DemoError, alias
from .foundry import ProjectClient, RemoteAgents, data_client, specialist_identity_headers
from .reviewer_agent import ReviewerAgent
from .routing import Choice, DecisionClient, gated_choice, load_calibration, reserve_decision, routing_state

ROOT = Path(__file__).resolve().parents[1]
LOGGER = logging.getLogger(__name__)
PREPARATION_CHECKS = frozenset({
    "NATIVE_HOST_ROLE", "NATIVE_HOST_PROJECT", "NATIVE_HOST_AGENT", "NATIVE_HOST_VERSION",
    "NATIVE_HOST_PLATFORM", "NATIVE_HOST_PRINCIPAL", "NATIVE_HOST_CALL", "NATIVE_HOST_SESSION",
    "TRUSTED_PARENT_REQUIRED", "REMOTE_SPECIALIST_REQUIRED",
    "DECISION_CALIBRATION_REQUIRED", "DECISION_CALIBRATION_DEPLOYMENT",
    "DECISION_CALIBRATION_PROVENANCE", "DECISION_CALIBRATION_POLICY",
    "DECISION_CALIBRATION_CORPUS", "DECISION_CALIBRATION_FAILED",
    "ARTIFACT_JSON", "ARTIFACT_DEPTH_LIMIT", "ARTIFACT_BYTE_LIMIT", "ARTIFACT_DUPLICATE_KEY",
})


def create_workflow(request: HostedResponseRequest):
    """Build the coordinator graph or a specialist's assigned-output workflow."""
    context_checkpoint(Stage.PREPARATION, request)
    try:
        runtime = WorkflowRuntime(request)
    except ArtifactError as exc:
        code = exc.code if exc.code in PREPARATION_CHECKS else "UNCLASSIFIED"
        LOGGER.error("Native workflow preparation rejected (%s).", code)
        raise
    if runtime.role != "coordinator":
        executor = SpecialistExecutor(runtime)
        return WorkflowBuilder(name=f"distributed-{runtime.role}-v1", start_executor=executor).build()
    begin = BeginExecutor(runtime)
    route = RouteExecutor(runtime)
    effect = EffectExecutor(runtime)
    publish = PublishExecutor(runtime)
    return (
        WorkflowBuilder(name="distributed-agents-v1", max_iterations=40, start_executor=begin)
        .add_edge(begin, route)
        .add_edge(route, effect)
        .add_edge(effect, publish)
        .add_edge(publish, route)
        .build()
    )


async def parse_turn(request: HostedResponseRequest) -> WorkflowTurn[str]:
    """Validate the stored, resilient request and expose its user text as workflow input."""
    context_checkpoint(
        Stage.BACKGROUND if request.request.get("background") is True else Stage.REQUEST, request,
    )
    if request.request.get("store") is False or request.request.get("background") is not True:
        raise ArtifactError("STORED_RESILIENT_BACKGROUND_REQUIRED")
    text = await request.get_input_text()
    if not isinstance(text, str) or not text.strip():
        raise ArtifactError("INPUT_SCHEMA")
    return WorkflowTurn(input=text)


class WorkflowRemoteAgents(RemoteAgents):
    def _client(self, child: Child):
        if child.role not in self.clients:
            self.clients[child.role] = FoundryAgent(
                project_client=self.project, agent_name=child.name, allow_preview=True,
                default_headers=self.headers, default_options={"store": True, "background": True},
                timeout=120,
            )
        return self.clients[child.role]

    async def invoke(self, child, brief, on_response):
        known_id = None

        async def remember(response_id):
            nonlocal known_id
            known_id = response_id
            await on_response(response_id)

        try:
            return await super().invoke(child, brief, remember)
        except DemoError as exc:
            if known_id is None or exc.code != "SPECIALIST_INCOMPLETE":
                raise
        except (ChatClientException, TimeoutError):
            if known_id is None:
                raise
            LOGGER.warning("Specialist stream interrupted; retrieving its persisted response without resend.")
        return await self.recover(child, known_id)

    async def recover(self, child, response_id):
        deadline = time.monotonic() + 120
        while True:
            try:
                return await super().recover(child, response_id)
            except DemoError as exc:
                if (
                    exc.code != "SPECIALIST_INCOMPLETE" or not exc.details
                    or exc.details.get("status") not in ("queued", "in_progress")
                    or time.monotonic() >= deadline
                ):
                    raise
            await asyncio.sleep(1)


def operation_id(scope: ScopeBinding, response_id: str, step: str) -> str:
    return uuid.uuid5(uuid.NAMESPACE_URL, scope.prefix + response_id + ":" + step).hex


def create_artifact_store(scope: ScopeBinding, role: str, credential) -> BlobArtifacts:
    return BlobArtifacts(
        role=role, scope=scope, endpoint=required("ARTIFACT_STORAGE_ENDPOINT"),
        containers={
            "control": required("ARTIFACT_CONTROL_CONTAINER"),
            "candidates": required("ARTIFACT_CANDIDATES_CONTAINER"),
            "reviews": required("ARTIFACT_REVIEWS_CONTAINER"),
        }, credential=credential,
        expected_private_ips=required("ARTIFACT_PRIVATE_IPS").split(","),
    )


class WorkflowRuntime:
    """Coordinator recipe: begin -> route -> execute -> publish -> route."""

    def __init__(self, request: HostedResponseRequest):
        self.request = request
        self.config = AgentConfig.from_env()
        self.context = get_request_context()
        self.role = os.environ["DEMO_ROLE"]
        if self.role not in AGENTS:
            raise ArtifactError("NATIVE_HOST_ROLE")
        for valid, code in (
            (self.config.project_endpoint == PROJECT, "NATIVE_HOST_PROJECT"),
            (self.config.agent_name == AGENTS[self.role], "NATIVE_HOST_AGENT"),
            (bool(self.config.agent_version), "NATIVE_HOST_VERSION"),
            (request.scope.is_hosted, "NATIVE_HOST_PLATFORM"),
            (bool(request.scope.user_id), "NATIVE_HOST_PRINCIPAL"),
            (bool(request.scope.call_id), "NATIVE_HOST_CALL"),
            (self.config.session_id == request.scope.session_id, "NATIVE_HOST_SESSION"),
        ):
            if not valid:
                raise ArtifactError(code)
        self.scope = ScopeBinding.from_platform(
            self.config, self.context, project=PROJECT, tenant=required("EXPECTED_AZURE_TENANT_ID")
        )
        self.response_id = request.response_id
        if self.role == "coordinator" and os.environ.get("DEMO_SPECIALIST_MODE") != "hosted":
            raise ArtifactError("REMOTE_SPECIALIST_REQUIRED")
        if self.role == "coordinator":
            self.calibration = load_calibration(
                ROOT / "config" / "routing-calibration.json", ROOT / "config" / "routing-corpus.json",
                required("DECISION_MODEL_DEPLOYMENT"),
            )

    async def begin(self, text: str) -> str:
        """Append this turn's requirements and invalidate the previous design/review."""
        if not text.strip() or len(text) > 4000:
            raise ArtifactError("INPUT_LIMIT")
        async with self.resources() as (store, *_):
            async with store.lock_manifest() as document:
                # STAGE 1: Bind this turn, or recognize an already recorded turn.
                manifest = document.value
                if manifest.status == "NEW" and not manifest.accepted:
                    manifest.coordinator_version = self.config.agent_version
                if manifest.coordinator_version != self.config.agent_version:
                    raise ArtifactError("PARENT_VERSION_CHANGED")
                if manifest.active_response_id == self.response_id:
                    return self.response_id
                if (
                    manifest.status == "RUNNING"
                    or manifest.effect is not None and manifest.effect.status not in ("accepted", "failed")
                ):
                    raise ArtifactError("PARENT_TURN_UNCERTAIN")

                # STAGE 2: Read earlier requirements and append the user's new text.
                requirement_chunks = []
                if manifest.requirements is not None:
                    previous_requirements = await store.read_artifact(manifest.requirements)
                    if not isinstance(previous_requirements.content, Requirements):
                        raise ArtifactError("REQUIREMENTS_SCHEMA")
                    requirement_chunks = list(previous_requirements.content.chunks)
                requirements = Requirements(chunks=[*requirement_chunks, text])

                # STAGE 3: Store the immutable requirements before publishing their reference.
                requirements_operation = operation_id(self.scope, self.response_id, "requirements")
                requirements_artifact = Artifact(
                    artifact_type="requirements", scope_binding=self.scope, operation_id=requirements_operation,
                    producer=self.producer(), input_refs=[], requirements_revision=len(requirements.chunks),
                    content=requirements, content_sha256=digest(requirements),
                )
                requirements_ref = await store.write_artifact(requirements_artifact)

                # STAGE 4: Start a fresh revision, keeping the existing specialist sessions.
                manifest.accepted.append(requirements_ref)
                manifest.requirements = requirements_ref
                manifest.candidate = None
                manifest.review = None
                manifest.turn = len(requirements.chunks)
                manifest.calls = 0
                manifest.rounds = 0
                manifest.decisions = 0
                manifest.active_response_id = self.response_id
                manifest.status = "RUNNING"
                manifest.effect = None
                manifest.next_action = None
                manifest.routing_operation_id = None
                manifest.deadline_epoch = int(time.time()) + 360
                await self.save(document, manifest)
        return self.response_id

    async def route(self, token: str) -> tuple[str | None, dict | None]:
        """Apply deterministic gates, then recover or request one semantic routing decision."""
        if token != self.response_id:
            raise ArtifactError("WORKFLOW_TURN_BINDING")
        async with self.resources() as (store, _, _, credential, http, headers):
            async with store.lock_manifest() as document:
                # STAGE 1: Resume the current turn or return its recorded action/result.
                manifest = document.value
                self.assert_turn(manifest)
                if manifest.status != "RUNNING":
                    return None, await self.result(store, manifest)
                if manifest.next_action is not None:
                    return manifest.next_action, None

                # STAGE 2: Validate accepted inputs, finish an approval, and enforce budgets.
                input_refs, routing_inputs = await self.inputs(store, manifest)
                if manifest.review is not None:
                    review = await store.read_artifact(manifest.review)
                    if not isinstance(review.content, Review):
                        raise ArtifactError("REVIEW_SCHEMA")
                    if review.content.approved:
                        manifest.status = "ACCEPTED_ADVISORY"
                        await self.save(document, manifest)
                        return None, await self.result(store, manifest)

                if manifest.candidate is None or manifest.review is not None:
                    action = "ask_architect"
                else:
                    action = "ask_reviewer"
                if (
                    manifest.decisions >= 10 or manifest.calls >= 6
                    or action == "ask_architect" and manifest.rounds >= 3
                    or time.time() >= manifest.deadline_epoch
                ):
                    manifest.status = "LIMIT_REACHED"
                    await self.save(document, manifest)
                    return None, await self.result(store, manifest)

                # STAGE 3: Recover an existing decision, or journal a new one before calling the model.
                calibration = load_calibration(
                    ROOT / "config" / "routing-calibration.json", ROOT / "config" / "routing-corpus.json",
                    required("DECISION_MODEL_DEPLOYMENT"),
                )
                effect = manifest.effect
                decision_artifact = None
                if effect and effect.kind == "decision" and effect.status != "accepted":
                    decision_operation = effect.operation_id
                    decision_artifact = await store.read_output(
                        artifact_type="decision", revision=manifest.turn, operation_id=decision_operation
                    )
                    if decision_artifact is None and effect.status != "prepared":
                        await self.hold(store, document, manifest, "DECISION_EFFECT_UNCERTAIN")
                        return None, await self.result(store, manifest)
                else:
                    manifest.decisions += 1
                    decision_operation = operation_id(self.scope, self.response_id, f"decision-{manifest.decisions}")
                    manifest.effect = Effect(
                        operation_id=decision_operation, kind="decision", status="prepared",
                        role="coordinator", input_refs=input_refs,
                        reserved_name=f"{self.scope.prefix}decisions/{manifest.turn}/{decision_operation}.json",
                    )
                    await self.transition(store, document, manifest, "prepared")

                # STAGE 4: Request and store a decision only when no completed decision exists.
                if decision_artifact is None:
                    limit_text = required("DECISION_REQUESTS_PER_MINUTE")
                    if not limit_text.isdecimal() or not 1 <= int(limit_text) <= 1000:
                        raise ArtifactError("DECISION_ADMISSION_CONFIGURATION")
                    await reserve_decision(
                        store, operation_id=decision_operation, deployment=required("DECISION_MODEL_DEPLOYMENT"),
                        limit=int(limit_text), deadline=min(time.time() + 65, manifest.deadline_epoch),
                    )
                    await self.transition(store, document, manifest, "dispatched")
                    router = DecisionClient(
                        http=http, credential=credential, origin=ORIGIN,
                        deployment=required("DECISION_MODEL_DEPLOYMENT"), headers=headers,
                    )
                    try:
                        async with asyncio.timeout(min(120, max(0, manifest.deadline_epoch - time.time()))):
                            choice = await router.choose(
                                state=routing_inputs, allowed=[action, "request_input"], calibration=calibration
                            )
                    except (ArtifactError, ValidationError, TimeoutError) as exc:
                        code = exc.code if isinstance(exc, ArtifactError) else type(exc).__name__
                        await self.hold(store, document, manifest, code)
                        return None, await self.result(store, manifest)
                    decision_artifact = Artifact(
                        artifact_type="decision", scope_binding=self.scope, operation_id=decision_operation,
                        producer=self.producer(), input_refs=input_refs, requirements_revision=manifest.turn,
                        candidate_revision=manifest.candidate_revision or None,
                        content=choice, content_sha256=digest(choice),
                    )
                    await store.write_artifact(decision_artifact)

                # STAGE 5: Validate the decision's provenance and publish its action or hold.
                await self.accept_decision(store, document, manifest, decision_artifact, input_refs, routing_inputs)
                if manifest.next_action is not None:
                    return manifest.next_action, None
                return None, await self.result(store, manifest)

    async def execute(self, action: str) -> str:
        """Bind a specialist, journal its assignment, and invoke or recover its response."""
        if action not in ("ask_architect", "ask_reviewer"):
            raise ArtifactError("SPECIALIST_ACTION")
        role: Literal["architect", "reviewer"]
        output_type: Literal["candidate", "review"]
        if action == "ask_architect":
            role = "architect"
            output_type = "candidate"
            output_collection = "candidates"
        else:
            role = "reviewer"
            output_type = "review"
            output_collection = "reviews"
        async with self.resources() as (store, remote, *_):
            async with store.lock_manifest() as document:
                # STAGE 1: Verify that the accepted routing decision authorizes this action.
                manifest = document.value
                self.assert_turn(manifest)
                if manifest.next_action != action or not manifest.routing_operation_id:
                    raise ArtifactError("ROUTING_OPERATION_BINDING")
                route_op = manifest.routing_operation_id

                # STAGE 2: Create or recover the pinned specialist's child session.
                child = manifest.children.get(role)
                if child is None:
                    prepared = await remote.prepare(role)
                    if prepared.name != AGENTS[role] or prepared.role != role or prepared.version.startswith("in-process"):
                        raise ArtifactError("REMOTE_SPECIALIST_REQUIRED")
                    child = ChildBinding.model_validate(prepared.model_dump(mode="json"))
                    manifest.children[role] = child
                    manifest.effect = Effect(
                        operation_id=operation_id(self.scope, route_op, "create"),
                        routing_operation_id=route_op, kind="create", status="prepared", role=role, input_refs=[],
                    )
                    await self.transition(store, document, manifest, "prepared")
                if (
                    child.role != role or child.name != AGENTS[role]
                    or child.framework.get("state", {}).get(FOUNDRY_HOSTED_AGENT_SESSION_ID_KEY) != child.hosted_id
                ):
                    raise ArtifactError("CHILD_BINDING")
                if not child.bound:
                    if manifest.effect is None or manifest.effect.kind != "create" or manifest.effect.role != role:
                        raise ArtifactError("CHILD_CREATE_BINDING")
                    target = Child.model_validate(child.model_dump(mode="json"))
                    try:
                        if manifest.effect.status == "prepared":
                            await self.transition(store, document, manifest, "dispatched")
                            with effects.dispatch(effects.Binding(
                                manifest.effect.operation_id, role, target.hosted_id,
                                target.version, "create",
                            )):
                                await remote.create(target)
                        else:
                            await remote.recover_creation(target)
                    except DemoError as exc:
                        await self.hold(store, document, manifest, exc.code)
                        return manifest.effect.operation_id
                    child.bound = True
                    await self.transition(store, document, manifest, "accepted")

                # STAGE 3: Store the exact input/output assignment before any specialist call.
                call_op = operation_id(self.scope, route_op, "call")
                effect = manifest.effect
                if effect is None or effect.operation_id != call_op:
                    refs = [ref for ref in (manifest.requirements, manifest.candidate, manifest.review) if ref is not None]
                    if role == "reviewer":
                        refs = refs[:2]
                    candidate_revision = manifest.candidate_revision
                    if role == "architect":
                        candidate_revision += 1
                    producer = Producer(
                        role=role, name=child.name, version=child.version, session_id=child.hosted_id
                    )
                    assignment = Assignment(
                        scope_binding=self.scope, operation_id=call_op, producer=producer, input_refs=refs,
                        requirements_revision=manifest.turn, candidate_revision=candidate_revision,
                        output_type=output_type,
                        deadline_epoch=manifest.deadline_epoch,
                    )
                    await store.write_assignment(assignment)
                    manifest.calls += 1
                    manifest.effect = Effect(
                        operation_id=call_op, routing_operation_id=route_op, kind="call", status="prepared",
                        role=role, input_refs=refs, assignment_sha256=digest(assignment),
                        reserved_name=f"{self.scope.prefix}{output_collection}/{manifest.turn}/{call_op}.json",
                    )
                    await self.transition(store, document, manifest, "prepared")
                effect = manifest.effect
                if effect.status in ("output_observed", "accepted"):
                    return call_op
                target = Child.model_validate(child.model_dump(mode="json"))

                # STAGE 4: Recover a known response, or dispatch once and record its ID immediately.
                async def remember(response_id: str):
                    if effect.response_id not in (None, response_id):
                        raise ArtifactError("REMOTE_RESPONSE_CHANGED")
                    if effect.response_id is None:
                        effect.response_id = response_id
                        await self.transition(store, document, manifest, "response_observed")

                try:
                    if effect.status != "prepared":
                        if effect.response_id is None:
                            proposal = await store.read_output(
                                artifact_type=output_type,
                                revision=manifest.turn, operation_id=call_op,
                            )
                            if proposal is None:
                                await self.hold(store, document, manifest, "DELEGATION_UNCERTAIN")
                                return call_op
                            assignment = await store.read_assignment(call_op)
                            self.verify_proposal(proposal, assignment, manifest)
                            await remember(proposal.producer.response_id)
                        output_text = await remote.recover(target, effect.response_id)
                    else:
                        await self.transition(store, document, manifest, "dispatched")
                        locator = AssignmentLocator(
                            schema_version=1, scope_binding=self.scope, operation_id=call_op
                        )
                        async with asyncio.timeout(min(120, max(0, manifest.deadline_epoch - time.time()))):
                            with effects.dispatch(effects.Binding(
                                call_op, role, target.hosted_id, target.version, "send",
                            )):
                                output_text = await remote.invoke(target, locator.model_dump(mode="json"), remember)

                    # STAGE 5: Record the output reference; publication validates the artifact itself.
                    output = OutputLocator.model_validate(decode_document(output_text.encode("utf-8")))
                    output.artifact_ref.assert_scope(self.scope)
                    if output.artifact_ref.name != effect.reserved_name:
                        raise ArtifactError("SPECIALIST_OUTPUT_BINDING")
                    child.framework = target.framework
                    effect.output_ref = output.artifact_ref
                    await self.transition(store, document, manifest, "output_observed")
                except (DemoError, ArtifactError, ValidationError, TimeoutError) as exc:
                    code = exc.code if isinstance(exc, (DemoError, ArtifactError)) else type(exc).__name__
                    await self.hold(store, document, manifest, code)
                return call_op

    async def publish(self, call_op: str) -> tuple[bool, dict | None]:
        """Validate the specialist's immutable output and accept it into the manifest."""
        async with self.resources() as (store, *_):
            async with store.lock_manifest() as document:
                # STAGE 1: Resume publication only for this turn's observed output.
                manifest = document.value
                self.assert_turn(manifest)
                effect = manifest.effect
                if manifest.status != "RUNNING":
                    return False, await self.result(store, manifest)
                if effect is None or effect.operation_id != call_op or effect.output_ref is None:
                    raise ArtifactError("PUBLICATION_OPERATION")
                if effect.status == "accepted":
                    return True, self.delegation_event(manifest)
                if effect.status != "output_observed":
                    raise ArtifactError("PUBLICATION_NOT_READY")

                # STAGE 2: Verify the assignment, producer, response, revisions, and exact inputs.
                assignment = await store.read_assignment(call_op)
                if digest(assignment) != effect.assignment_sha256:
                    raise ArtifactError("ASSIGNMENT_INTEGRITY")
                proposal = await store.read_artifact(effect.output_ref)
                self.verify_proposal(proposal, assignment, manifest)
                if proposal.producer.response_id != effect.response_id:
                    raise ArtifactError("SPECIALIST_RESPONSE_BINDING")
                for ref in assignment.input_refs:
                    await store.read_artifact(ref)

                # STAGE 3: Accept the design or review, invalidating findings for an older design.
                if effect.output_ref not in manifest.accepted:
                    manifest.accepted.append(effect.output_ref)
                if isinstance(proposal.content, Candidate):
                    manifest.candidate = effect.output_ref
                    manifest.candidate_revision = proposal.content.candidate_revision
                    manifest.review = None
                    manifest.rounds += 1
                elif isinstance(proposal.content, Review):
                    manifest.review = effect.output_ref
                else:
                    raise ArtifactError("SPECIALIST_ARTIFACT_TYPE")
                manifest.next_action = None

                # STAGE 4: Publish through the fenced manifest and return to routing.
                await self.transition(store, document, manifest, "accepted")
                return True, self.delegation_event(manifest)

    @asynccontextmanager
    async def resources(self):
        """Own the Azure clients and verify private storage before yielding to an event."""
        execution_checkpoint(self)
        async with AsyncExitStack() as stack:
            credential = await stack.enter_async_context(
                ManagedIdentityCredential(**credential_diagnostics_options(role=self.role))
            )
            http = await stack.enter_async_context(data_client(
                expected_call_id=self.context.call_id, response_id=self.response_id,
            ))
            headers = dict(self.context.platform_headers())
            project = await stack.enter_async_context(ProjectClient(credential, http, headers))
            # B candidate is confined to remote specialists. Routing/model/parent
            # resources retain the original opaque-only headers and cache.
            specialist_headers = specialist_identity_headers(
                config=self.config, context=self.context, scope=self.scope,
            )
            specialist_project = await stack.enter_async_context(
                ProjectClient(credential, http, specialist_headers)
            )
            artifact_store = await stack.enter_async_context(
                create_artifact_store(self.scope, self.role, credential)
            )
            await artifact_store.verify_private_path()
            yield (
                artifact_store, WorkflowRemoteAgents(specialist_project, specialist_headers),
                project, credential, http, headers,
            )

    def producer(self, *, response_id: str | None = None) -> Producer:
        return Producer(
            role=self.role, name=self.config.agent_name, version=self.config.agent_version,
            session_id=self.scope.parent_session, response_id=response_id or self.response_id,
        )

    async def save(self, document, manifest: Manifest):
        if manifest.coordinator_version != self.config.agent_version:
            raise ArtifactError("PARENT_VERSION_CHANGED")
        manifest.generation += 1
        validated = Manifest.model_validate(manifest.model_dump(mode="json"))
        await document.save(validated)

    def assert_turn(self, manifest: Manifest) -> None:
        if (
            manifest.scope_binding != self.scope or manifest.coordinator_version != self.config.agent_version
            or manifest.active_response_id != self.response_id
        ):
            raise ArtifactError("PARENT_TURN_BINDING")

    async def transition(self, store, document, manifest: Manifest, status: str):
        """Write the immutable operation transition before saving the fenced manifest."""
        if manifest.effect is None:
            raise ArtifactError("OPERATION_REQUIRED")
        manifest.effect.status = status
        await store.write_operation(
            manifest.effect.operation_id, status,
            {"scope_binding": self.scope.model_dump(mode="json"), "effect": manifest.effect.model_dump(mode="json")},
        )
        await self.save(document, manifest)

    async def inputs(self, store, manifest: Manifest) -> tuple[list[ArtifactRef], dict]:
        refs = [ref for ref in (manifest.requirements, manifest.candidate, manifest.review) if ref is not None]
        if not refs or refs[0] != manifest.requirements:
            raise ArtifactError("REQUIREMENTS_REQUIRED")
        if any(ref not in manifest.accepted for ref in refs):
            raise ArtifactError("ROUTING_PREREQUISITES_NOT_ACCEPTED")
        for kind, ref in (
            ("requirements", manifest.requirements), ("candidate", manifest.candidate), ("review", manifest.review),
        ):
            if ref is not None and (
                ref.artifact_type != kind or ref.requirements_revision != manifest.turn
                or kind != "requirements" and ref.candidate_revision != manifest.candidate_revision
            ):
                raise ArtifactError("ROUTING_PREREQUISITE_REVISION")
        input_artifacts = []
        for ref in refs:
            input_artifacts.append(await store.read_artifact(ref))
        state = routing_state(
            refs, [artifact.content for artifact in input_artifacts],
            candidate_revision=manifest.candidate_revision,
            remaining_calls=6 - manifest.calls, remaining_rounds=3 - manifest.rounds,
        )
        return refs, state

    async def accept_decision(self, store, document, manifest, proposal: Artifact, refs, state):
        effect = manifest.effect
        choice = proposal.content
        if (
            effect is None or proposal.operation_id != effect.operation_id or proposal.input_refs != refs
            or proposal.producer != self.producer() or not isinstance(choice, Decision)
            or choice.state_sha256 != digest(state)
            or choice.deployment != required("DECISION_MODEL_DEPLOYMENT")
            or proposal.requirements_revision != manifest.turn
            or choice.alternatives != [
                "ask_architect" if manifest.candidate is None or manifest.review is not None else "ask_reviewer",
                "request_input",
            ]
        ):
            raise ArtifactError("DECISION_PROVENANCE")
        answer = Choice(
            type="choice", choice=choice.action, confidence=choice.confidence, probabilities=choice.probabilities
        )
        answer.validate_choices(choice.alternatives)
        calibration = load_calibration(
            ROOT / "config" / "routing-calibration.json", ROOT / "config" / "routing-corpus.json",
            required("DECISION_MODEL_DEPLOYMENT"),
        )
        if (
            choice.calibration_sha256 != digest(calibration)
            or choice.gated_action != gated_choice(answer, calibration.threshold, calibration.margin)
        ):
            raise ArtifactError("DECISION_POLICY_PROVENANCE")
        ref = proposal.ref()
        if ref not in manifest.accepted:
            manifest.accepted.append(ref)
        effect.output_ref = ref
        manifest.routing_operation_id = effect.operation_id
        if choice.gated_action in ("hold", "request_input"):
            manifest.status = "ROUTING_HOLD" if choice.gated_action == "hold" else "REQUEST_INPUT"
            manifest.next_action = None
        elif choice.gated_action in ("ask_architect", "ask_reviewer"):
            manifest.next_action = choice.gated_action
        else:
            raise ArtifactError("DECISION_ACTION")
        await self.transition(store, document, manifest, "accepted")

    async def hold(self, store, document, manifest: Manifest, code: str):
        manifest.status = code
        manifest.next_action = None
        if manifest.effect:
            manifest.effect.failure = code
            await self.transition(store, document, manifest, "unknown")
        else:
            await self.save(document, manifest)

    def verify_proposal(self, proposal: Artifact, assignment: Assignment, manifest: Manifest):
        expected = assignment.producer.model_copy(update={"response_id": proposal.producer.response_id})
        expected_candidate_revision = manifest.candidate_revision
        if assignment.output_type == "candidate":
            expected_candidate_revision += 1
        if (
            proposal.scope_binding != self.scope or proposal.operation_id != assignment.operation_id
            or proposal.producer != expected or proposal.input_refs != assignment.input_refs
            or proposal.artifact_type != assignment.output_type
            or proposal.requirements_revision != assignment.requirements_revision
            or proposal.candidate_revision != assignment.candidate_revision
            or any(ref not in manifest.accepted for ref in proposal.input_refs)
            or assignment.requirements_revision != manifest.turn
            or assignment.candidate_revision != expected_candidate_revision
        ):
            raise ArtifactError("SPECIALIST_ARTIFACT_PROVENANCE")

    def delegation_event(self, manifest: Manifest) -> dict:
        effect = manifest.effect
        child = manifest.children[effect.role]
        return {
            "event": "delegation", "role": effect.role, "action": f"ask_{effect.role}",
            "specialist_mode": "hosted", "status": "completed", "round": manifest.rounds,
            "candidate_revision": manifest.candidate_revision,
            "hosted_session": alias(child.hosted_id), "framework_session": alias(child.framework["session_id"]),
            "response": alias(effect.response_id), "version": child.version,
            "artifact_ref": effect.output_ref.model_dump(mode="json"),
        }

    async def result(self, store, manifest: Manifest) -> dict:
        requirements = await store.read_artifact(manifest.requirements) if manifest.requirements else None
        candidate = await store.read_artifact(manifest.candidate) if manifest.candidate else None
        review = await store.read_artifact(manifest.review) if manifest.review else None
        decision_refs = [
            ref for ref in manifest.accepted if ref.artifact_type == "decision" and ref.requirements_revision == manifest.turn
        ]
        decision_evidence = []
        decision_artifacts = []
        for ref in decision_refs:
            record = await store.read_artifact(ref)
            if not isinstance(record.content, Decision):
                raise ArtifactError("DECISION_ARTIFACT_SCHEMA")
            decision_evidence.append(record.content.model_dump(mode="json"))
            decision_artifacts.append(record.model_dump(mode="json"))
        return {
            "event": "result", "status": manifest.status, "turn": manifest.turn,
            "calls": manifest.calls, "decisions": manifest.decisions,
            "candidate": candidate.content.model_dump(mode="json", exclude={"kind"}) if candidate else None,
            "review": review.content.model_dump(mode="json", exclude={"kind"}) if review else None,
            "artifact_refs": {
                kind: ref.model_dump(mode="json") if ref else None
                for kind, ref in (("requirements", manifest.requirements), ("candidate", manifest.candidate), ("review", manifest.review))
            },
            "decision_refs": [
                ref.model_dump(mode="json") for ref in decision_refs
            ],
            "decision_evidence": decision_evidence,
            "artifact_evidence": {
                kind: artifact.model_dump(mode="json") if artifact else None
                for kind, artifact in (
                    ("requirements", requirements), ("candidate", candidate), ("review", review),
                )
            },
            "decision_artifacts": decision_artifacts,
            "manifest_generation": manifest.generation, "native_workflow": "distributed-agents-v1",
            "specialists": "hosted", "pending_effect": (
                manifest.effect.model_dump(mode="json")
                if manifest.effect and manifest.effect.status not in ("accepted", "failed") else None
            ),
            "artifact_authentication": "managed_identity", "artifact_private_path_verified": True,
        }

    async def specialize(self, text: str) -> str:
        if self.role == "architect":
            return await ArchitectAgent.run_assignment(
                text, config=self.config, context=self.context, scope=self.scope, response_id=self.response_id,
            )
        if self.role == "reviewer":
            return await ReviewerAgent.run_assignment(
                text, config=self.config, context=self.context, scope=self.scope, response_id=self.response_id,
            )
        raise ArtifactError("NATIVE_HOST_ROLE")


class BeginExecutor(Executor):
    def __init__(self, runtime):
        super().__init__(id="requirements-v1")
        self.runtime = runtime

    @handler
    async def run_turn(self, text: str, context: WorkflowContext[str]):
        execution_checkpoint(self.runtime)
        await context.send_message(await self.runtime.begin(text))


class RouteExecutor(Executor):
    def __init__(self, runtime):
        super().__init__(id="routing-v1")
        self.runtime = runtime

    @handler
    async def route(self, token: str, context: WorkflowContext[str, str]):
        execution_checkpoint(self.runtime)
        action, result = await self.runtime.route(token)
        if action is not None:
            await context.send_message(action)
        else:
            await context.yield_output(canonical_bytes(result).decode() + "\n")


class EffectExecutor(Executor):
    def __init__(self, runtime):
        super().__init__(id="effects-v1")
        self.runtime = runtime

    @handler
    async def dispatch_effect(self, action: str, context: WorkflowContext[str]):
        execution_checkpoint(self.runtime)
        await context.send_message(await self.runtime.execute(action))


class PublishExecutor(Executor):
    def __init__(self, runtime):
        super().__init__(id="publication-v1")
        self.runtime = runtime

    @handler
    async def publish(self, call_op: str, context: WorkflowContext[str, str]):
        execution_checkpoint(self.runtime)
        continuing, result = await self.runtime.publish(call_op)
        if continuing:
            if result is not None:
                await context.yield_output(canonical_bytes(result).decode() + "\n")
            await context.send_message(self.runtime.response_id)
        else:
            await context.yield_output(canonical_bytes(result).decode() + "\n")


class SpecialistExecutor(Executor):
    def __init__(self, runtime):
        super().__init__(id="assigned-output-v1")
        self.runtime = runtime

    @handler
    async def specialize(self, text: str, context: WorkflowContext[str, str]):
        execution_checkpoint(self.runtime)
        await context.yield_output(await self.runtime.specialize(text))
