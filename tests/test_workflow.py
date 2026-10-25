from __future__ import annotations

import asyncio
import copy
import hashlib
import io
import json
import os
import tempfile
import unittest
import uuid
from pathlib import Path
from contextlib import ExitStack, asynccontextmanager, redirect_stdout
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch
from pydantic import ValidationError

os.environ.setdefault("FOUNDRY_PROJECT_ENDPOINT", "https://example.services.ai.azure.com/api/projects/example-project")
os.environ.setdefault("SPECIALIST_MODEL_DEPLOYMENT", "synthetic-worker")
os.environ.setdefault("DECISION_MODEL_DEPLOYMENT", "synthetic-decision")

from azure.core.exceptions import HttpResponseError, ResourceExistsError, ResourceNotFoundError
from agent_framework import AgentResponseUpdate, AgentSession, InMemoryCheckpointStorage, WorkflowBuilder
from agent_framework_foundry import FOUNDRY_HOSTED_AGENT_SESSION_ID_KEY
from demo.artifact_store import BlobArtifacts
from demo.artifacts import (
    Artifact, ArtifactError, Candidate, Decision, Manifest, Review, ScopeBinding,
    canonical_bytes, decode_document, digest,
)
from demo.contracts import AGENTS, Child
from demo.workflow import (
    BeginExecutor, EffectExecutor, WorkflowRuntime, OutputLocator, PublishExecutor, RouteExecutor,
)
from demo.routing import Calibration, CalibrationObservation, calibration_state, decision_request


def synthetic_calibration():
    corpus = decode_document((Path(__file__).resolve().parents[1] / "config" / "routing-corpus.json").read_bytes())
    return Calibration(
        corpus_sha256=digest(corpus), deployment=os.environ["DECISION_MODEL_DEPLOYMENT"],
        threshold=0.5, margin=0.0,
        observations=[
            CalibrationObservation(
                case_id=case["id"], expected=case["expected"], allowed=case["allowed"],
                state_sha256=digest(calibration_state(case["state"])),
                request_sha256=digest(decision_request(
                    calibration_state(case["state"]), case["allowed"], os.environ["DECISION_MODEL_DEPLOYMENT"],
                )),
                outcome={
                    "model": "Microsoft-Decision-1", "answers": {"next_action": {
                        "type": "choice", "choice": case["expected"], "confidence": 0.99,
                        "probabilities": {
                            action: 0.99 if action == case["expected"] else 0.01 for action in case["allowed"]
                        },
                    }},
                },
            ) for case in corpus["cases"]
        ],
    )


class ProcessCrash(BaseException):
    pass


def http_error(status):
    error = HttpResponseError("synthetic conditional failure")
    error.status_code = status
    return error


class MemoryBackend:
    def __init__(self):
        self.blobs = {}
        self.leases = {}
        self.etags = {}
        self.crash_publication = False

    def get_blob_client(self, container, name):
        return MemoryBlob(self, (container, name))

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        return None


class MemoryBlob:
    def __init__(self, backend, key):
        self.backend, self.key = backend, key

    async def upload_blob(self, raw, *, overwrite, lease=None, etag=None, **kwargs):
        data = self.backend
        if not overwrite and self.key in data.blobs:
            raise ResourceExistsError("synthetic existing object")
        if overwrite and (
            data.leases.get(self.key) != lease or str(data.etags.get(self.key)) != etag
        ):
            raise http_error(412)
        value = decode_document(raw)
        if (
            data.crash_publication and self.key[1].endswith("manifest.json")
            and value.get("candidate") and value.get("effect", {}).get("status") == "accepted"
        ):
            data.crash_publication = False
            raise ProcessCrash()
        data.blobs[self.key] = raw
        data.etags[self.key] = data.etags.get(self.key, 0) + 1
        return {"etag": str(data.etags[self.key])}

    async def download_blob(self, **kwargs):
        if self.key not in self.backend.blobs:
            raise ResourceNotFoundError("synthetic missing object")
        raw = self.backend.blobs[self.key]

        async def readall():
            return raw
        return SimpleNamespace(
            size=len(raw), readall=readall, properties=SimpleNamespace(etag=str(self.backend.etags[self.key]))
        )

    async def acquire_lease(self, *, lease_duration):
        if self.key in self.backend.leases:
            raise http_error(409)
        lease = MemoryLease(self.backend, self.key)
        self.backend.leases[self.key] = lease.id
        return lease


class MemoryLease:
    def __init__(self, backend, key):
        self.backend, self.key, self.id = backend, key, uuid.uuid4().hex

    async def renew(self):
        if self.backend.leases.get(self.key) != self.id:
            raise http_error(412)

    async def release(self):
        if self.backend.leases.get(self.key) == self.id:
            del self.backend.leases[self.key]


class FakeRouter:
    async def choose(self, *, state, allowed, calibration):
        return Decision(
            state_sha256=digest(state), deployment=os.environ["DECISION_MODEL_DEPLOYMENT"],
            alternatives=allowed, action=allowed[0],
            probabilities={allowed[0]: 0.99, allowed[1]: 0.01}, confidence=0.99,
            gated_action=allowed[0], reason="synthetic_test_selection", calibration_sha256=digest(calibration),
        )


class FakeRemote:
    def __init__(self, backend):
        self.backend = backend
        self.calls, self.creates, self.recoveries = 0, 0, 0
        self.responses = {}
        self.crash = None
        self.corrupt_producer = False
        self.contradict_review = False

    async def prepare(self, role):
        session = AgentSession()
        hosted_id = uuid.uuid4().hex
        session.state[FOUNDRY_HOSTED_AGENT_SESSION_ID_KEY] = hosted_id
        return Child(
            role=role, name=AGENTS[role], version="2", hosted_id=hosted_id,
            framework=session.to_dict(),
        )

    async def create(self, child):
        self.creates += 1

    async def recover_creation(self, child):
        return None

    async def invoke(self, child, locator, callback):
        self.calls += 1
        if self.crash == "unknown_response":
            self.crash = None
            raise ProcessCrash()
        scope = ScopeBinding.model_validate(locator["scope_binding"])
        store = make_store(self.backend, scope, "coordinator")
        assignment = await store.read_assignment(locator["operation_id"])
        manifest = await store.read_manifest()
        assignment.validate_receiver(
            config=SimpleNamespace(
                is_hosted=True, session_id=child.hosted_id, project_endpoint=scope.project,
                agent_name=child.name, agent_version=child.version,
            ),
            context=SimpleNamespace(session_id=child.hosted_id, user_id=scope.principal, call_id="trusted-call"),
            manifest=manifest, now=assignment.deadline_epoch,
        )
        response_id = "synthetic-" + uuid.uuid4().hex
        await callback(response_id)
        content = self.output_content(child, assignment)
        producer = assignment.producer.model_copy(update={"response_id": response_id})
        if self.corrupt_producer:
            producer = producer.model_copy(update={"version": "unassigned-version"})
        output = Artifact(
            artifact_type=assignment.output_type, scope_binding=scope, operation_id=assignment.operation_id,
            producer=producer, input_refs=assignment.input_refs,
            requirements_revision=assignment.requirements_revision, candidate_revision=assignment.candidate_revision,
            content=content, content_sha256=digest(content),
        )
        ref = await make_store(self.backend, scope, child.role).write_artifact(output)
        text = canonical_bytes(OutputLocator(schema_version=1, artifact_ref=ref)).decode()
        self.responses[response_id] = text
        if self.crash == "known_response":
            self.crash = None
            raise ProcessCrash()
        return text

    def output_content(self, child, assignment):
        return (
            Candidate(
                requirements_revision=assignment.requirements_revision,
                candidate_revision=assignment.candidate_revision, design="Synthetic private design.",
            ) if child.role == "architect" else Review(
                requirements_revision=assignment.requirements_revision, candidate_revision=assignment.candidate_revision,
                approved=True, blocking_findings=["blocker"] if self.contradict_review else [],
                unresolved_requirements=[], recommendation="Synthetic current approval.",
            )
        )

    async def recover(self, child, response_id):
        self.recoveries += 1
        return self.responses[response_id]


class RecordingRemote(FakeRemote):
    """Offline remote boundary, not live hosting or specialist model-memory proof.

    Snapshot by value at each send/return. Advance the simulated service response
    independently of stable hosted/framework identities, like the remote adapter.
    """

    def __init__(self, backend, *, reject_first_review=False):
        super().__init__(backend)
        self.reject_first_review = reject_first_review
        self.prepared, self.created, self.invocations = [], [], []

    async def prepare(self, role):
        child = await super().prepare(role)
        self.prepared.append(copy.deepcopy(child.model_dump(mode="json")))
        return child

    async def create(self, child):
        self.created.append(copy.deepcopy(child.model_dump(mode="json")))
        await super().create(child)

    def output_content(self, child, assignment):
        content = super().output_content(child, assignment)
        if child.role == "reviewer" and self.reject_first_review:
            self.reject_first_review = False
            return content.model_copy(update={
                "approved": False, "blocking_findings": ["Add the missing private ingress boundary."],
                "recommendation": "Revise the exact current candidate before approval.",
            })
        return content

    async def invoke(self, child, locator, callback):
        scope = ScopeBinding.model_validate(locator["scope_binding"])
        store = make_store(self.backend, scope, "coordinator")
        manifest = await store.read_manifest()
        assignment = await store.read_assignment(locator["operation_id"])
        requirements = await store.read_artifact(manifest.requirements)
        observation = copy.deepcopy({
            "scope": scope.model_dump(mode="json"),
            "before": child.model_dump(mode="json"),
            "assignment": assignment.model_dump(mode="json"),
            "manifest": manifest.model_dump(mode="json"),
            "requirements": requirements.content.model_dump(mode="json"),
        })
        text = await super().invoke(child, locator, callback)
        ref = OutputLocator.model_validate(decode_document(text.encode())).artifact_ref
        output = await store.read_artifact(ref)
        session = AgentSession.from_dict(child.framework)
        session.service_session_id = output.producer.response_id
        child.framework = session.to_dict()
        observation.update(copy.deepcopy({
            "after": child.model_dump(mode="json"), "response_id": output.producer.response_id,
            "output": output.model_dump(mode="json"), "output_ref": ref.model_dump(mode="json"),
        }))
        self.invocations.append(observation)
        return text


def make_store(backend, scope, role):
    return BlobArtifacts(
        role=role, scope=scope, endpoint="https://syntheticstorage.blob.core.windows.net",
        containers={"control": "control", "candidates": "candidates", "reviews": "reviews"},
        credential=None, service=backend,
    )


class TestRuntime(WorkflowRuntime):
    def __init__(self, backend, remote, *, parent="parent-one", response="response-one"):
        self.backend, self.remote = backend, remote
        self.scope = ScopeBinding(
            project="https://example.services.ai.azure.com/api/projects/example-project",
            tenant="11111111-1111-1111-1111-111111111111", principal="trusted-user", parent_session=parent,
        )
        self.response_id, self.role = response, "coordinator"
        self.config = SimpleNamespace(agent_name=AGENTS["coordinator"], agent_version="2")

    @asynccontextmanager
    async def resources(self, **kwargs):
        yield make_store(self.backend, self.scope, self.role), self.remote, None, None, None, {}


def graph(runtime, checkpoints=None):
    begin, route, effect, publish = (
        BeginExecutor(runtime), RouteExecutor(runtime), EffectExecutor(runtime), PublishExecutor(runtime)
    )
    return (
        WorkflowBuilder(
            name="distributed-agents-v1", start_executor=begin, max_iterations=40,
            checkpoint_storage=checkpoints,
        )
        .add_edge(begin, route).add_edge(route, effect).add_edge(effect, publish).add_edge(publish, route).build()
    )


class NativeOutboundTransportTests(unittest.IsolatedAsyncioTestCase):
    async def test_outbound_context_reports_wire_presence_and_matches_without_values(self):
        import httpx2
        from demo.contracts import PROJECT
        from demo.foundry import OriginTransport
        from live_acceptance import outbound_identity
        private_call, private_response = "synthetic-private-call", "synthetic-private-response"
        for headers, present, matches, delegated, container in (
            ({}, False, False, False, False),
            ({"x-agent-foundry-call-id": "different-private-call"}, True, False, False, False),
            ({"x-agent-foundry-call-id": private_call}, True, True, False, False),
            ({"x-agent-foundry-call-id": private_call,
              "x-ms-user-identity": "synthetic-private-delegated-user",
              "x-agent-user-id": "synthetic-private-container-user"}, True, True, True, True),
        ):
            seen = []
            def handle(request):
                seen.append(request)
                return httpx2.Response(200, json={})
            transport = OriginTransport(
                httpx2.MockTransport(handle), expected_call_id=private_call, response_id=private_response,
            )
            with self.subTest(present=present, matches=matches, delegated=delegated), \
                    self.assertLogs("demo.foundry.outbound_context", level="INFO") as logs:
                async with httpx2.AsyncClient(transport=transport) as http:
                    response = await http.post(
                        PROJECT + "/agents/" + AGENTS["architect"] + "/endpoint/protocols/openai/responses",
                        headers=headers | {"Authorization": "Bearer synthetic-private-token"},
                        json={"input": "synthetic-private-input"},
                    )
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(seen), 1)
            self.assertEqual(len(logs.output), 1)
            self.assertEqual(outbound_identity(logs.output[0], private_response), {
                "role": "architect", "has_call_id": present, "call_matches_context": matches,
                "has_delegated_user": delegated, "has_container_user": container,
            })
            self.assertNotIn("synthetic-private", logs.output[0])
            self.assertNotIn("different-private", logs.output[0])

    async def test_outbound_diagnostics_exclude_unrelated_requests_and_reject_other_origins(self):
        import httpx2
        from demo.contracts import PROJECT
        from demo.foundry import OriginTransport
        from demo.contracts import DemoError
        seen = []
        def handle(request):
            seen.append(request)
            return httpx2.Response(200, json={})
        transport = OriginTransport(
            httpx2.MockTransport(handle), expected_call_id="synthetic-call", response_id="synthetic-response",
        )
        with self.assertNoLogs("demo.foundry.outbound_context", level="INFO"):
            async with httpx2.AsyncClient(transport=transport) as http:
                await http.get(PROJECT + "/agents/" + AGENTS["architect"] + "/endpoint/protocols/openai/responses")
                await http.post(PROJECT + "/responses")
                await http.post(PROJECT + "/agents/unrelated/endpoint/protocols/openai/responses")
                with self.assertRaisesRegex(DemoError, "UNAUTHORIZED_ORIGIN"):
                    await http.post("https://example.invalid/responses")
        self.assertEqual(len(seen), 3)

    async def test_legacy_transport_does_not_emit_native_context_diagnostics(self):
        import httpx2
        from demo.contracts import PROJECT
        from demo.foundry import OriginTransport
        with self.assertNoLogs("demo.foundry.outbound_context", level="INFO"):
            async with httpx2.AsyncClient(
                transport=OriginTransport(httpx2.MockTransport(lambda request: httpx2.Response(200)))
            ) as http:
                await http.post(PROJECT + "/agents/" + AGENTS["architect"] + "/endpoint/protocols/openai/responses")

    async def test_outbound_diagnostics_require_both_nonempty_context_bindings(self):
        import httpx2
        from demo.foundry import OriginTransport
        from demo.contracts import DemoError
        for call, response in ((None, "response"), ("call", None), ("", ""), ("", "response")):
            with self.subTest(call=call, response=response), \
                    self.assertRaisesRegex(DemoError, "OUTBOUND_CONTEXT_CONFIGURATION"):
                OriginTransport(httpx2.MockTransport(lambda request: httpx2.Response(200)),
                                expected_call_id=call, response_id=response)


class NativeWorkflowTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.backend = MemoryBackend()
        self.remote = FakeRemote(self.backend)
        self.runtime = TestRuntime(self.backend, self.remote)
        self.env = patch.dict(os.environ, {"DECISION_REQUESTS_PER_MINUTE": "17"})
        self.env.start()
        self.router = patch("demo.workflow.DecisionClient", return_value=FakeRouter())
        self.router.start()
        self.calibration = patch("demo.workflow.load_calibration", return_value=synthetic_calibration())
        self.calibration.start()
        self.addCleanup(self.env.stop)
        self.addCleanup(self.router.stop)
        self.addCleanup(self.calibration.stop)

    async def test_architect_runs_five_stages_with_explicit_handoffs_and_owned_cleanup(self):
        await self.check_specialist_stage_handoffs("architect")

    async def test_reviewer_runs_five_stages_with_explicit_handoffs_and_owned_cleanup(self):
        await self.check_specialist_stage_handoffs("reviewer")

    async def check_specialist_stage_handoffs(self, role):
        from demo.architect_agent import ArchitectAgent
        from demo.reviewer_agent import ReviewerAgent

        agent_class = ArchitectAgent if role == "architect" else ReviewerAgent
        scope = self.runtime.scope
        content = Candidate(
            requirements_revision=1, candidate_revision=1, design="Synthetic staged design.",
        ) if role == "architect" else Review(
            requirements_revision=1, candidate_revision=1, approved=True,
            blocking_findings=[], unresolved_requirements=[], recommendation="Synthetic staged review.",
        )
        artifact = Artifact(
            artifact_type="candidate" if role == "architect" else "review", scope_binding=scope, operation_id="a" * 32,
            producer={
                "role": role, "name": AGENTS[role], "version": "2",
                "session_id": "child", "response_id": "outer-response",
            },
            input_refs=[], requirements_revision=1, candidate_revision=1,
            content=content, content_sha256=digest(content),
        )
        stage_names = (
            "connect_and_load_assignment", "read_requirements_and_prior_work",
            "load_or_create_llm_session", "design_solution", "store_design",
        ) if role == "architect" else (
            "connect_and_load_assignment", "read_requirements_and_design",
            "load_or_create_llm_session", "review_solution", "store_review",
        )
        existing_key = "existing_design" if role == "architect" else "existing_review"
        for completed in (False, True):
            with self.subTest(completed=completed), ExitStack() as patches:
                calls = MagicMock()
                stages = [
                    patches.enter_context(patch.object(agent_class, name, new_callable=AsyncMock))
                    for name in stage_names
                ]
                for name, stage in zip(stage_names, stages):
                    calls.attach_mock(stage, name)
                store, project, assignment, session_store, session = (object() for _ in range(5))
                headers = {"x-agent-foundry-call-id": "synthetic-call"}
                brief = {"inputs": ["Synthetic requirements."]}
                resource = MagicMock()

                async def connect(stack, *_args, **_kwargs):
                    await stack.enter_async_context(resource)
                    return store, project, headers, assignment, artifact if completed else None

                stages[0].side_effect = connect
                stages[1].return_value = brief
                stages[2].return_value = session_store, session, "synthetic-model"
                stages[3].return_value = "synthetic-model-output"
                stages[4].return_value = artifact.ref()
                result = await agent_class.run_assignment(
                    "synthetic-locator", config=self.runtime.config, context=SimpleNamespace(),
                    scope=scope, response_id="outer-response",
                )
                self.assertEqual([call[0] for call in calls.mock_calls], list(stage_names[:3 if completed else 5]))
                stages[1].assert_awaited_once_with(store, assignment)
                self.assertIs(stages[2].await_args.kwargs["brief"], brief)
                self.assertIs(stages[2].await_args.kwargs["assignment"], assignment)
                self.assertIs(stages[2].await_args.kwargs[existing_key], artifact if completed else None)
                if completed:
                    stages[3].assert_not_awaited()
                    stages[4].assert_not_awaited()
                else:
                    self.assertIs(stages[3].await_args.kwargs["session"], session)
                    self.assertIs(stages[3].await_args.kwargs["session_store"], session_store)
                    self.assertIs(stages[3].await_args.kwargs["project"], project)
                    self.assertEqual(stages[4].await_args.kwargs["text"], "synthetic-model-output")
                    self.assertIs(stages[4].await_args.kwargs["store"], store)
                self.assertEqual(OutputLocator.model_validate(decode_document(result.encode())).artifact_ref, artifact.ref())
                resource.__aenter__.assert_awaited_once()
                resource.__aexit__.assert_awaited_once()

    async def test_architect_closes_connections_when_any_stage_fails(self):
        await self.check_specialist_stage_cleanup("architect")

    async def test_reviewer_closes_connections_when_any_stage_fails(self):
        await self.check_specialist_stage_cleanup("reviewer")

    async def check_specialist_stage_cleanup(self, role):
        from demo.architect_agent import ArchitectAgent
        from demo.reviewer_agent import ReviewerAgent

        agent_class = ArchitectAgent if role == "architect" else ReviewerAgent
        stage_names = (
            "connect_and_load_assignment", "read_requirements_and_prior_work",
            "load_or_create_llm_session", "design_solution", "store_design",
        ) if role == "architect" else (
            "connect_and_load_assignment", "read_requirements_and_design",
            "load_or_create_llm_session", "review_solution", "store_review",
        )
        for failing_stage in range(5):
            with self.subTest(stage=stage_names[failing_stage]), ExitStack() as patches:
                stages = [
                    patches.enter_context(patch.object(agent_class, name, new_callable=AsyncMock))
                    for name in stage_names
                ]
                resource = MagicMock()

                async def connect(stack, *_args, **_kwargs):
                    await stack.enter_async_context(resource)
                    if failing_stage == 0:
                        raise RuntimeError("Synthetic stage failure")
                    return object(), object(), {}, object(), None

                stages[0].side_effect = connect
                stages[1].return_value = {}
                stages[2].return_value = object(), object(), "synthetic-model"
                stages[3].return_value = "synthetic-output"
                if failing_stage:
                    stages[failing_stage].side_effect = RuntimeError("Synthetic stage failure")
                with self.assertRaisesRegex(RuntimeError, "Synthetic stage failure"):
                    await agent_class.run_assignment(
                        "synthetic-locator", config=self.runtime.config, context=SimpleNamespace(),
                        scope=self.runtime.scope, response_id="outer-response",
                    )
                resource.__aenter__.assert_awaited_once()
                resource.__aexit__.assert_awaited_once()
                for stage in stages[failing_stage + 1:]:
                    stage.assert_not_awaited()

    async def test_native_resources_forward_sdk_context_without_redelegating_platform_user(self):
        import httpx2
        from azure.ai.agentserver.core import FoundryAgentRequestContext
        from azure.core.credentials import AccessTokenInfo
        from agent_framework.exceptions import ChatClientException
        from demo.contracts import PROJECT
        from demo.foundry import data_client
        from live_acceptance import outbound_identity
        from urllib.parse import urlsplit
        self.runtime.context = FoundryAgentRequestContext(
            session_id=self.runtime.scope.parent_session, user_id=self.runtime.scope.principal,
            call_id="synthetic-opaque-call",
        )
        self.runtime.config.is_hosted = True
        self.runtime.config.session_id = self.runtime.scope.parent_session
        self.runtime.config.project_endpoint = PROJECT
        seen = []
        def handle(request):
            seen.append({"headers": {
                key: request.headers[key] for key in (
                    "x-agent-foundry-call-id", "x-ms-user-identity", "x-agent-user-id",
                ) if key in request.headers
            }, "method": request.method, "path": request.url.path,
                "synthetic_bearer_matches": request.headers.get("authorization") == "Bearer synthetic-token",
                "session": json.loads(request.content).get("agent_session_id")})
            return httpx2.Response(418, json={"error": {
                "message": "Synthetic context probe.", "type": "probe", "code": "probe",
            }})
        credential = MagicMock()
        credential.__aenter__ = AsyncMock(return_value=credential)
        credential.__aexit__ = AsyncMock(return_value=False)
        credential.get_token = AsyncMock(side_effect=AssertionError("Unexpected legacy credential route"))
        credential.get_token_info = AsyncMock(return_value=AccessTokenInfo("synthetic-token", 4102444800))
        store = MagicMock()
        store.__aenter__ = AsyncMock(return_value=store)
        store.__aexit__ = AsyncMock(return_value=False)
        store.verify_private_path = AsyncMock()
        session = AgentSession()
        session.state[FOUNDRY_HOSTED_AGENT_SESSION_ID_KEY] = "a" * 32
        child = Child(role="architect", name=AGENTS["architect"], version="1",
                      hosted_id="a" * 32, framework=session.to_dict())
        with patch.dict(os.environ, EXPECTED_AZURE_TENANT_ID=self.runtime.scope.tenant,
                        OPENAI_API_KEY="synthetic-unrelated-key"), \
                patch("demo.workflow.ManagedIdentityCredential", return_value=credential), \
                patch("demo.workflow.data_client", wraps=data_client) as data_factory, \
                patch("demo.foundry.httpx2.AsyncHTTPTransport", return_value=httpx2.MockTransport(handle)), \
                patch("demo.workflow.create_artifact_store", return_value=store), \
                self.assertLogs("demo.foundry.outbound_context", level="INFO") as logs:
            async with WorkflowRuntime.resources(self.runtime) as (_, remote, project, actual_credential, _, headers):
                self.assertIs(actual_credential, credential)
                # Original resources still never redelegate the platform user;
                # only the B candidate's distinct specialist client does.
                self.assertEqual(headers, {"x-agent-foundry-call-id": "synthetic-opaque-call"})
                self.assertEqual(project.call_headers, headers)
                self.assertIsNot(project, remote.project)
                stream = remote._client(child).run("Synthetic probe.", session=session, stream=True)
                with self.assertRaises(ChatClientException):
                    async with stream:
                        async for _ in stream:
                            pass
        self.assertEqual(seen, [{
            "headers": {
                "x-agent-foundry-call-id": "synthetic-opaque-call",
                "x-ms-user-identity": self.runtime.scope.principal,
            },
            "method": "POST",
            "synthetic_bearer_matches": True,
            "path": urlsplit(PROJECT).path + "/agents/" + AGENTS["architect"]
                    + "/endpoint/protocols/openai/responses",
            "session": "a" * 32,
        }])
        store.verify_private_path.assert_awaited_once()
        # The public pinned Project/OpenAI path, not a mocked OpenAI client,
        # obtains its bearer from the resource-owned credential for this scope.
        # This is a synthetic credential-route check, not a live principal ID.
        credential.get_token.assert_not_awaited()
        self.assertEqual(credential.get_token_info.await_count, 1)
        self.assertEqual(credential.get_token_info.await_args.args, ("https://ai.azure.com/.default",))
        data_factory.assert_called_once_with(
            expected_call_id=self.runtime.context.call_id, response_id=self.runtime.response_id,
        )
        self.assertEqual(len(logs.output), 1)
        self.assertEqual(outbound_identity(logs.output[0], self.runtime.response_id), {
            "role": "architect", "has_call_id": True, "call_matches_context": True,
            "has_delegated_user": True, "has_container_user": False,
        })
        self.assertNotIn("synthetic-opaque-call", logs.output[0])

    async def test_specialist_credential_failure_never_falls_back_to_environment_key(self):
        import httpx2
        from azure.identity import CredentialUnavailableError
        from demo.foundry import ProjectClient, OriginTransport

        credential = SimpleNamespace(
            get_token=AsyncMock(side_effect=AssertionError("Unexpected legacy credential route")),
            get_token_info=AsyncMock(
                side_effect=CredentialUnavailableError("Synthetic credential unavailable."),
            ),
        )
        sends = []

        def handle(request):
            sends.append(request.method)
            return httpx2.Response(500)

        with patch.dict(os.environ, OPENAI_API_KEY="synthetic-unrelated-key"):
            async with httpx2.AsyncClient(transport=OriginTransport(httpx2.MockTransport(handle))) as http:
                async with ProjectClient(credential, http, {}) as project:
                    client = project.get_openai_client(agent_name=AGENTS["architect"])
                    with self.assertRaises(CredentialUnavailableError):
                        await client.responses.create(input="Synthetic credential-route probe.")
        self.assertEqual(sends, [])
        credential.get_token.assert_not_awaited()
        self.assertEqual(credential.get_token_info.await_count, 1)
        self.assertEqual(credential.get_token_info.await_args.args, ("https://ai.azure.com/.default",))

    async def step_to_call(self):
        await self.runtime.begin("Synthetic requirements.")
        action, result = await self.runtime.route(self.runtime.response_id)
        self.assertIsNone(result)
        return action

    async def test_recorded_begin_does_not_append_requirements_or_reset_the_turn(self):
        await self.step_to_call()
        store = make_store(self.backend, self.runtime.scope, "coordinator")
        before = await store.read_manifest()
        stored_blobs = dict(self.backend.blobs)

        response_id = await self.runtime.begin("Do not append this replayed text.")

        self.assertEqual(response_id, self.runtime.response_id)
        self.assertEqual(await store.read_manifest(), before)
        self.assertEqual(self.backend.blobs, stored_blobs)

    async def test_assignment_and_response_journals_are_saved_before_specialist_handoffs(self):
        action = await self.step_to_call()
        store = make_store(self.backend, self.runtime.scope, "coordinator")
        invoke = self.remote.invoke
        observed_roles = []

        async def inspect_handoff(child, locator, on_response):
            manifest = await store.read_manifest()
            effect = manifest.effect
            assignment = await store.read_assignment(locator["operation_id"])
            expected_refs = [manifest.requirements]
            if child.role == "reviewer":
                expected_refs.append(manifest.candidate)
                expected_output_type = "review"
                expected_collection = "reviews"
            else:
                expected_output_type = "candidate"
                expected_collection = "candidates"
            self.assertEqual(effect.status, "dispatched")
            self.assertEqual(effect.assignment_sha256, digest(assignment))
            self.assertEqual(assignment.input_refs, expected_refs)
            self.assertEqual(assignment.output_type, expected_output_type)
            self.assertEqual(assignment.candidate_revision, 1)
            self.assertEqual(assignment.deadline_epoch, manifest.deadline_epoch)
            self.assertEqual(assignment.producer.session_id, child.hosted_id)
            self.assertEqual(assignment.producer.version, child.version)
            self.assertEqual(
                effect.reserved_name,
                f"{self.runtime.scope.prefix}{expected_collection}/{manifest.turn}/{effect.operation_id}.json",
            )
            journal_prefix = f"{self.runtime.scope.prefix}operations/{effect.operation_id}/"
            dispatched = decode_document(self.backend.blobs[("control", journal_prefix + "dispatched.json")])
            self.assertEqual(dispatched["effect"], effect.model_dump(mode="json"))

            async def inspect_response(response_id):
                await on_response(response_id)
                observed = await store.read_manifest()
                self.assertEqual(observed.effect.status, "response_observed")
                self.assertEqual(observed.effect.response_id, response_id)
                response_record = decode_document(
                    self.backend.blobs[("control", journal_prefix + "response_observed.json")]
                )
                self.assertEqual(response_record["effect"], observed.effect.model_dump(mode="json"))

            observed_roles.append(child.role)
            return await invoke(child, locator, inspect_response)

        with patch.object(self.remote, "invoke", side_effect=inspect_handoff):
            for role in ("architect", "reviewer"):
                self.assertEqual(action, f"ask_{role}")
                operation = await self.runtime.execute(action)
                continuing, event = await self.runtime.publish(operation)
                self.assertTrue(continuing)
                self.assertEqual(event["role"], role)
                action, result = await self.runtime.route(self.runtime.response_id)

        self.assertIsNone(action)
        self.assertEqual(result["status"], "ACCEPTED_ADVISORY")
        self.assertEqual(observed_roles, ["architect", "reviewer"])
        self.assertEqual(self.remote.calls, 2)

    async def test_observed_output_resumes_execution_without_another_remote_effect(self):
        action = await self.step_to_call()
        operation = await self.runtime.execute(action)
        store = make_store(self.backend, self.runtime.scope, "coordinator")
        before = await store.read_manifest()

        with patch.object(self.remote, "invoke") as invoke, \
                patch.object(self.remote, "recover") as recover:
            self.assertEqual(await self.runtime.execute(action), operation)
            invoke.assert_not_awaited()
            recover.assert_not_awaited()

        self.assertEqual(await store.read_manifest(), before)
        continuing, event = await self.runtime.publish(operation)
        self.assertTrue(continuing)
        self.assertEqual(event["role"], "architect")
        self.assertEqual(self.remote.calls, 1)

    async def test_unaccepted_or_mistyped_prerequisite_never_reaches_router(self):
        await self.runtime.begin("Synthetic requirements.")
        key = ("control", self.runtime.scope.prefix + "manifest.json")
        baseline = decode_document(self.backend.blobs[key])
        for corruption in ("unaccepted", "mistyped", "stale_requirements"):
            manifest = copy.deepcopy(baseline)
            if corruption == "unaccepted":
                manifest["accepted"] = []
            elif corruption == "mistyped":
                manifest["candidate"] = manifest["requirements"]
                manifest["candidate_revision"] = 1
            else:
                manifest["turn"] = 2
            self.backend.blobs[key] = canonical_bytes(manifest)
            with self.subTest(corruption=corruption), patch("demo.workflow.DecisionClient") as client:
                with self.assertRaises((ArtifactError, ValidationError)):
                    await self.runtime.route(self.runtime.response_id)
                client.assert_not_called()
                self.assertEqual(self.remote.calls, 0)

    async def test_recorded_routing_action_resumes_without_another_decision(self):
        action = await self.step_to_call()
        store = make_store(self.backend, self.runtime.scope, "coordinator")
        before = await store.read_manifest()
        with patch("demo.workflow.DecisionClient") as client:
            self.assertEqual(await self.runtime.route(self.runtime.response_id), (action, None))
            client.assert_not_called()
        self.assertEqual(await store.read_manifest(), before)

    async def test_routing_limits_stop_before_requesting_a_decision(self):
        for limit in ("decisions", "calls", "rounds", "deadline"):
            with self.subTest(limit=limit):
                runtime = TestRuntime(self.backend, self.remote, parent=f"limit-{limit}")
                await runtime.begin("Synthetic requirements.")
                store = make_store(self.backend, runtime.scope, "coordinator")
                async with store.lock_manifest() as document:
                    manifest = document.value
                    if limit == "decisions":
                        manifest.decisions = 10
                    elif limit == "calls":
                        manifest.calls = 6
                    elif limit == "rounds":
                        manifest.rounds = 3
                    else:
                        manifest.deadline_epoch = 1
                    await runtime.save(document, manifest)
                with patch("demo.workflow.DecisionClient") as client:
                    action, result = await runtime.route(runtime.response_id)
                    client.assert_not_called()
                self.assertIsNone(action)
                self.assertEqual(result["status"], "LIMIT_REACHED")
                self.assertIsNone(result["pending_effect"])
                self.assertEqual(result["decision_refs"], [])
        self.assertEqual(self.remote.calls, 0)

    async def test_current_approval_finishes_before_checking_exhausted_budgets(self):
        await graph(self.runtime).run("Synthetic requirements.")
        store = make_store(self.backend, self.runtime.scope, "coordinator")
        async with store.lock_manifest() as document:
            manifest = document.value
            manifest.status = "RUNNING"
            manifest.decisions, manifest.calls, manifest.rounds = 10, 6, 3
            manifest.deadline_epoch = 1
            await self.runtime.save(document, manifest)
        with patch("demo.workflow.DecisionClient") as client:
            action, result = await self.runtime.route(self.runtime.response_id)
            client.assert_not_called()
        self.assertIsNone(action)
        self.assertEqual(result["status"], "ACCEPTED_ADVISORY")
        self.assertTrue(result["review"]["approved"])
        self.assertEqual(self.remote.calls, 2)

    async def test_prepared_decision_resumes_without_counting_a_second_decision(self):
        await self.runtime.begin("Synthetic requirements.")
        with patch("demo.workflow.reserve_decision", side_effect=ProcessCrash):
            with self.assertRaises(ProcessCrash):
                await self.runtime.route(self.runtime.response_id)
        store = make_store(self.backend, self.runtime.scope, "coordinator")
        before = await store.read_manifest()
        self.assertEqual(before.effect.status, "prepared")
        resumed = TestRuntime(self.backend, self.remote)
        router = FakeRouter()
        with patch.object(router, "choose", wraps=router.choose) as choose, \
                patch("demo.workflow.DecisionClient", return_value=router):
            self.assertEqual(await resumed.route(resumed.response_id), ("ask_architect", None))
            choose.assert_awaited_once()
        after = await store.read_manifest()
        self.assertEqual(after.decisions, 1)
        self.assertEqual(after.effect.operation_id, before.effect.operation_id)
        self.assertEqual(after.effect.status, "accepted")

    async def test_dispatched_decision_without_output_is_held_without_resend(self):
        await self.runtime.begin("Synthetic requirements.")
        with patch.object(FakeRouter, "choose", side_effect=ProcessCrash):
            with self.assertRaises(ProcessCrash):
                await self.runtime.route(self.runtime.response_id)
        store = make_store(self.backend, self.runtime.scope, "coordinator")
        self.assertEqual((await store.read_manifest()).effect.status, "dispatched")
        resumed = TestRuntime(self.backend, self.remote)
        with patch("demo.workflow.DecisionClient") as client:
            action, result = await resumed.route(resumed.response_id)
            self.assertEqual(await resumed.route(resumed.response_id), (action, result))
            client.assert_not_called()
        self.assertIsNone(action)
        self.assertEqual(result["status"], "DECISION_EFFECT_UNCERTAIN")
        self.assertEqual(result["pending_effect"]["kind"], "decision")
        self.assertEqual(result["pending_effect"]["status"], "unknown")
        self.assertEqual(result["decisions"], 1)
        self.assertEqual(self.remote.calls, 0)

    async def test_completed_decision_recovers_after_crash_without_another_model_call(self):
        await self.runtime.begin("Synthetic requirements.")
        with patch.object(self.runtime, "accept_decision", side_effect=ProcessCrash):
            with self.assertRaises(ProcessCrash):
                await self.runtime.route(self.runtime.response_id)
        store = make_store(self.backend, self.runtime.scope, "coordinator")
        before = await store.read_manifest()
        proposal = await store.read_output(
            artifact_type="decision", revision=before.turn, operation_id=before.effect.operation_id,
        )
        self.assertIsNotNone(proposal)
        resumed = TestRuntime(self.backend, self.remote)
        with patch("demo.workflow.DecisionClient") as client, \
                patch("demo.workflow.reserve_decision") as reserve:
            self.assertEqual(await resumed.route(resumed.response_id), ("ask_architect", None))
            client.assert_not_called()
            reserve.assert_not_awaited()
        after = await store.read_manifest()
        self.assertEqual(after.decisions, 1)
        self.assertEqual(after.effect.status, "accepted")
        self.assertEqual(after.effect.output_ref, proposal.ref())
        self.assertIn(proposal.ref(), after.accepted)

    async def test_routing_provider_error_remains_an_explicit_unknown_effect(self):
        await self.runtime.begin("Synthetic requirements.")
        with patch.object(FakeRouter, "choose", side_effect=ArtifactError("DECISION_HTTP_429")) as choose:
            action, result = await self.runtime.route(self.runtime.response_id)
            choose.assert_awaited_once()
        self.assertIsNone(action)
        self.assertEqual(result["status"], "DECISION_HTTP_429")
        self.assertEqual(result["pending_effect"]["status"], "unknown")
        self.assertEqual(result["pending_effect"]["failure"], "DECISION_HTTP_429")
        self.assertEqual(result["decision_refs"], [])
        self.assertEqual(self.remote.calls, 0)

    async def test_native_graph_reaches_current_accepted_remote_outputs(self):
        result = await graph(self.runtime).run("Synthetic requirements.")
        outputs = [decode_document(item.strip().encode()) for item in result.get_outputs()]
        final = outputs[-1]
        self.assertEqual(final["status"], "ACCEPTED_ADVISORY")
        self.assertEqual(final["native_workflow"], "distributed-agents-v1")
        self.assertIsNone(final["pending_effect"])
        self.assertEqual({item["role"] for item in outputs[:-1]}, {"architect", "reviewer"})
        self.assertEqual((self.remote.calls, self.remote.creates), (2, 2))
        self.assertEqual(final["candidate"]["candidate_revision"], final["review"]["candidate_revision"])
        self.assertEqual(len(final["decision_refs"]), 2)
        from live_acceptance import events, validate_artifact_evidence
        self.assertEqual(events("\n".join(json.dumps(item) for item in outputs))["result"], final)
        for corruption in ("content", "prerequisite", "decision"):
            changed = copy.deepcopy(final)
            if corruption == "content":
                changed["candidate"]["design"] = "Unrelated substituted synthetic design."
            elif corruption == "prerequisite":
                artifact = Artifact.model_validate(changed["artifact_evidence"]["review"])
                artifact = artifact.model_copy(update={"input_refs": []})
                changed["artifact_evidence"]["review"] = artifact.model_dump(mode="json")
                changed["artifact_refs"]["review"] = artifact.ref().model_dump(mode="json")
            else:
                changed["decision_artifacts"] = []
            with self.subTest(corruption=corruption), self.assertRaises(RuntimeError):
                validate_artifact_evidence(changed)

    async def test_result_preserves_complete_shape_read_order_and_read_only_behavior(self):
        for scenario in ("new", "requirements-only", "accepted", "held"):
            with self.subTest(scenario=scenario):
                backend = MemoryBackend()
                remote = FakeRemote(backend)
                runtime = TestRuntime(backend, remote)
                store = make_store(backend, runtime.scope, "coordinator")
                if scenario == "requirements-only":
                    await runtime.begin("Synthetic requirements.")
                elif scenario == "accepted":
                    await graph(runtime).run("Synthetic requirements.")
                elif scenario == "held":
                    await runtime.begin("Synthetic requirements.")
                    action, _ = await runtime.route(runtime.response_id)
                    remote.crash = "unknown_response"
                    with self.assertRaises(ProcessCrash):
                        await runtime.execute(action)
                    await runtime.execute(action)

                if scenario == "new":
                    manifest = Manifest(scope_binding=runtime.scope)
                else:
                    manifest = await store.read_manifest()
                artifact_refs = {
                    "requirements": manifest.requirements,
                    "candidate": manifest.candidate,
                    "review": manifest.review,
                }
                artifacts = {}
                for kind, ref in artifact_refs.items():
                    artifacts[kind] = await store.read_artifact(ref) if ref else None
                decision_refs = [
                    ref for ref in manifest.accepted
                    if ref.artifact_type == "decision" and ref.requirements_revision == manifest.turn
                ]
                decisions = [await store.read_artifact(ref) for ref in decision_refs]
                blobs_before = dict(backend.blobs)
                remote_counts = (remote.creates, remote.calls, remote.recoveries)
                with patch.object(store, "read_artifact", wraps=store.read_artifact) as read_artifact:
                    result = await runtime.result(store, manifest)

                expected_pending_effect = None
                if scenario == "held":
                    expected_pending_effect = manifest.effect.model_dump(mode="json")
                self.assertEqual(result, {
                    "event": "result", "status": manifest.status, "turn": manifest.turn,
                    "calls": manifest.calls, "decisions": manifest.decisions,
                    "candidate": (
                        artifacts["candidate"].content.model_dump(mode="json", exclude={"kind"})
                        if artifacts["candidate"] else None
                    ),
                    "review": (
                        artifacts["review"].content.model_dump(mode="json", exclude={"kind"})
                        if artifacts["review"] else None
                    ),
                    "artifact_refs": {
                        kind: ref.model_dump(mode="json") if ref else None
                        for kind, ref in artifact_refs.items()
                    },
                    "decision_refs": [ref.model_dump(mode="json") for ref in decision_refs],
                    "decision_evidence": [artifact.content.model_dump(mode="json") for artifact in decisions],
                    "artifact_evidence": {
                        kind: artifact.model_dump(mode="json") if artifact else None
                        for kind, artifact in artifacts.items()
                    },
                    "decision_artifacts": [artifact.model_dump(mode="json") for artifact in decisions],
                    "manifest_generation": manifest.generation, "native_workflow": "distributed-agents-v1",
                    "specialists": "hosted", "pending_effect": expected_pending_effect,
                    "artifact_authentication": "managed_identity", "artifact_private_path_verified": True,
                })
                self.assertEqual(
                    [call.args[0] for call in read_artifact.await_args_list],
                    [ref for ref in artifact_refs.values() if ref] + decision_refs,
                )
                self.assertEqual(backend.blobs, blobs_before)
                self.assertEqual((remote.creates, remote.calls, remote.recoveries), remote_counts)

    async def test_known_response_reconciles_after_crash_without_new_remote_call(self):
        action = await self.step_to_call()
        self.remote.crash = "known_response"
        with self.assertRaises(ProcessCrash):
            await self.runtime.execute(action)
        resumed = TestRuntime(self.backend, self.remote)
        operation = await resumed.execute(action)
        continuing, event = await resumed.publish(operation)
        self.assertTrue(continuing)
        self.assertEqual(event["role"], "architect")
        self.assertEqual((self.remote.calls, self.remote.creates, self.remote.recoveries), (1, 1, 1))

    async def test_native_checkpoint_resumes_fresh_graph_without_duplicate_effects(self):
        checkpoints = InMemoryCheckpointStorage()
        self.remote.crash = "known_response"
        with self.assertRaises(ProcessCrash):
            await graph(self.runtime, checkpoints).run("Synthetic checkpoint requirements.")
        saved = await checkpoints.list_checkpoints(workflow_name="distributed-agents-v1")
        self.assertTrue(saved)
        resumed = TestRuntime(self.backend, self.remote)
        result = await graph(resumed, checkpoints).run(checkpoint_id=saved[-1].checkpoint_id)
        final = decode_document(result.get_outputs()[-1].strip().encode())
        self.assertEqual(final["status"], "ACCEPTED_ADVISORY")
        self.assertEqual((self.remote.calls, self.remote.creates, self.remote.recoveries), (2, 2, 1))

    async def test_specialist_recovers_observed_model_response_without_replay(self):
        await self.check_specialist_model_recovery(known=True)

    async def test_specialist_holds_unobserved_model_response_without_replay(self):
        await self.check_specialist_model_recovery(known=False)

    async def test_specialist_publication_crash_reconciles_history_before_followup(self):
        await self.check_specialist_model_recovery(known=True, publication_crash=True)

    async def test_architect_reads_requirements_and_writes_design_artifact(self):
        await self.check_specialist_model_recovery(known=True, fresh=True)

    async def test_specialists_reject_unsupported_locator_version_before_opening_azure_clients(self):
        from demo.architect_agent import ArchitectAgent
        from demo.reviewer_agent import ReviewerAgent

        for agent in (ArchitectAgent, ReviewerAgent):
            module = agent.__module__
            locator = canonical_bytes({
                "schema_version": 2, "scope_binding": self.runtime.scope.model_dump(mode="json"),
                "operation_id": "a" * 32,
            }).decode()
            with self.subTest(agent=agent.__name__), patch(f"{module}.ManagedIdentityCredential") as credential:
                with self.assertRaises(ValidationError):
                    await agent.run_assignment(
                        locator, config=self.runtime.config, context=SimpleNamespace(),
                        scope=self.runtime.scope, response_id="synthetic-response",
                    )
                credential.assert_not_called()

    async def test_unsupported_specialist_output_version_is_held_without_acceptance(self):
        action = await self.step_to_call()
        invoke = self.remote.invoke

        async def unsupported_output(*args):
            output = decode_document((await invoke(*args)).encode())
            output["schema_version"] = 2
            return canonical_bytes(output).decode()

        with patch.object(self.remote, "invoke", side_effect=unsupported_output):
            operation = await self.runtime.execute(action)
        store = make_store(self.backend, self.runtime.scope, "coordinator")
        manifest = await store.read_manifest()
        self.assertEqual(manifest.effect.status, "unknown")
        self.assertEqual(manifest.status, "ValidationError")
        self.assertIsNone(manifest.effect.output_ref)
        self.assertIsNone(manifest.candidate)
        continuing, result = await self.runtime.publish(operation)
        self.assertFalse(continuing)
        self.assertEqual(result["status"], "ValidationError")

    async def test_reviewer_reads_requirements_and_design_and_writes_review_artifact(self):
        await self.check_specialist_model_recovery(role="reviewer", known=True, fresh=True)

    async def test_reviewer_recovers_observed_model_response_without_replay(self):
        await self.check_specialist_model_recovery(role="reviewer", known=True)

    async def test_reviewer_holds_unobserved_model_response_without_replay(self):
        await self.check_specialist_model_recovery(role="reviewer", known=False)

    async def test_reviewer_publication_crash_reconciles_history(self):
        await self.check_specialist_model_recovery(role="reviewer", known=True, publication_crash=True)

    async def test_specialists_close_azure_clients_when_private_storage_verification_fails(self):
        for role in ("architect", "reviewer"):
            with self.subTest(role=role):
                self.backend = MemoryBackend()
                self.remote = FakeRemote(self.backend)
                self.runtime = TestRuntime(self.backend, self.remote)
                await self.check_specialist_model_recovery(role=role, known=True, private_path_failure=True)

    async def check_specialist_model_recovery(
        self, *, known, role="architect", publication_crash=False, fresh=False, private_path_failure=False,
    ):
        action = await self.step_to_call()
        if role == "reviewer":
            operation = await self.runtime.execute(action)
            await self.runtime.publish(operation)
            action, _ = await self.runtime.route(self.runtime.response_id)
        self.remote.crash = "unknown_response"
        with self.assertRaises(ProcessCrash):
            await self.runtime.execute(action)
        store = make_store(self.backend, self.runtime.scope, "coordinator")
        manifest = await store.read_manifest()
        assignment = await store.read_assignment(manifest.effect.operation_id)
        child = manifest.children[role]
        session_store = SimpleNamespace(snapshot=None, crash=publication_crash)

        async def get(_key):
            return AgentSession.from_dict(copy.deepcopy(session_store.snapshot)) if session_store.snapshot else None

        async def set_value(_key, value):
            if session_store.crash and "pending_operation" not in value.state:
                session_store.crash = False
                raise ProcessCrash()
            session_store.snapshot = copy.deepcopy(value.to_dict())

        session_store.get, session_store.set = get, set_value
        content = Candidate(
            requirements_revision=assignment.requirements_revision,
            candidate_revision=assignment.candidate_revision, design="Synthetic recovered model design.",
        ) if role == "architect" else Review(
            requirements_revision=assignment.requirements_revision,
            candidate_revision=assignment.candidate_revision, approved=True,
            blocking_findings=[], unresolved_requirements=[], recommendation="Synthetic review.",
        )
        retrieve = AsyncMock(return_value=SimpleNamespace(
            id="inner-model-response", status="completed", output_text=canonical_bytes(content).decode(),
        ))
        project = SimpleNamespace(get_openai_client=lambda: SimpleNamespace(
            responses=SimpleNamespace(retrieve=retrieve),
        ))
        worker = TestRuntime(self.backend, self.remote)
        worker.role = role
        worker.response_id = "trusted-worker-outer-response"
        worker.config = SimpleNamespace(
            is_hosted=True, session_id=child.hosted_id, project_endpoint=self.runtime.scope.project,
            agent_name=child.name, agent_version=child.version,
        )
        worker.context = SimpleNamespace(
            session_id=child.hosted_id, user_id=self.runtime.scope.principal, call_id="trusted-worker-call",
            platform_headers=lambda: {"x-agent-foundry-call-id": "trusted-worker-call"},
        )

        specialist_store = make_store(self.backend, self.runtime.scope, role)
        specialist_store.verify_private_path = AsyncMock(
            side_effect=ArtifactError("ARTIFACT_PRIVATE_DNS_MISMATCH") if private_path_failure else None,
        )
        specialist_store.read_assignment = AsyncMock(wraps=specialist_store.read_assignment)
        specialist_store.read_artifact = AsyncMock(wraps=specialist_store.read_artifact)
        specialist_store.write_artifact = AsyncMock(wraps=specialist_store.write_artifact)
        worker.resources = MagicMock(side_effect=AssertionError("Specialists must open Azure clients inline."))
        locator = canonical_bytes({
            "schema_version": 1, "scope_binding": self.runtime.scope.model_dump(mode="json"),
            "operation_id": assignment.operation_id,
        }).decode()

        class InterruptedStream:
            async def __aenter__(self):
                return self

            async def __aexit__(self, *_args):
                return None

            async def __aiter__(self):
                if known:
                    yield AgentResponseUpdate(response_id="inner-model-response")
                if not fresh:
                    raise ProcessCrash()

            async def get_final_response(self):
                return SimpleNamespace(finish_reason="stop", text=canonical_bytes(content).decode())

        agent = MagicMock()
        agent.__aenter__ = AsyncMock(return_value=agent)
        agent.__aexit__ = AsyncMock(return_value=None)
        agent.run.return_value = InterruptedStream()
        module = f"demo.{role}_agent"
        from demo.architect_agent import ArchitectAgent
        from demo.reviewer_agent import ReviewerAgent
        agent_class = ArchitectAgent if role == "architect" else ReviewerAgent
        credential, http = MagicMock(), MagicMock()
        credential.__aenter__.return_value = credential
        http.__aenter__.return_value = http
        project_context, blob_context = MagicMock(), MagicMock()
        project_context.__aenter__.return_value = project
        blob_context.__aenter__.return_value = self.backend
        with patch(f"{module}.AgentSessionStoreProvider") as provider, \
                patch.object(agent_class, "__new__", return_value=agent), \
                patch(f"{module}.FoundryChatClient"), \
                patch(f"{module}.ManagedIdentityCredential", return_value=credential), \
                patch(f"{module}.data_client", return_value=http) as http_factory, \
                patch(f"{module}.ProjectClient", return_value=project_context) as project_factory, \
                patch(f"{module}.BlobServiceClient", return_value=blob_context) as blob_factory, \
                patch(f"{module}.blob_diagnostics_transport") as blob_transport, \
                patch(f"{module}.BlobArtifacts", return_value=specialist_store) as store_factory, \
                patch.dict(os.environ, {
                    "ARTIFACT_STORAGE_ENDPOINT": "https://syntheticstorage.blob.core.windows.net",
                    "ARTIFACT_CONTROL_CONTAINER": "control",
                    "ARTIFACT_CANDIDATES_CONTAINER": "candidates",
                    "ARTIFACT_REVIEWS_CONTAINER": "reviews",
                    "ARTIFACT_PRIVATE_IPS": "10.0.0.4",
                }):
            provider.return_value.get_store.return_value = session_store
            if private_path_failure:
                with self.assertRaisesRegex(ArtifactError, "ARTIFACT_PRIVATE_DNS_MISMATCH"):
                    await worker.specialize(locator)
                specialist_store.read_assignment.assert_not_awaited()
                specialist_store.read_artifact.assert_not_awaited()
                specialist_store.write_artifact.assert_not_awaited()
                provider.assert_not_called()
                agent.run.assert_not_called()
                for resource in (credential, http, project_context, blob_context):
                    resource.__aenter__.assert_awaited_once()
                    resource.__aexit__.assert_awaited_once()
                return
            if fresh:
                result = OutputLocator.model_validate(decode_document((await worker.specialize(locator)).encode()))
                retrieve.assert_not_awaited()
            else:
                with self.assertRaises(ProcessCrash):
                    await worker.specialize(locator)
                self.assertEqual(
                    session_store.snapshot["state"]["pending_operation"]["response_id"],
                    "inner-model-response" if known else None,
                )
            if known and not fresh:
                if publication_crash:
                    with self.assertRaises(ProcessCrash):
                        await worker.specialize(locator)
                result = OutputLocator.model_validate(decode_document((await worker.specialize(locator)).encode()))
                retrieve.assert_awaited_once_with("inner-model-response")
            elif not known:
                with self.assertRaises(ArtifactError) as caught:
                    await worker.specialize(locator)
                self.assertEqual(caught.exception.code, "SPECIALIST_MODEL_EFFECT_UNCERTAIN")
                retrieve.assert_not_awaited()
            agent.run.assert_called_once()
            expected_inputs = [await store.read_artifact(ref) for ref in assignment.input_refs]
            self.assertEqual(
                decode_document(agent.run.call_args.args[0].encode())["inputs"],
                [value.content.model_dump(mode="json") for value in expected_inputs],
            )
            self.assertEqual(
                [call.args[0] for call in specialist_store.read_artifact.await_args_list[:len(assignment.input_refs)]],
                assignment.input_refs,
            )
            if known:
                self.assertEqual(result.artifact_ref.artifact_type, assignment.output_type)
                self.assertEqual(result.artifact_ref.container, "candidates" if role == "architect" else "reviews")
                specialist_store.write_artifact.assert_awaited_once()
                artifact = await store.read_artifact(result.artifact_ref)
                self.assertEqual(artifact.content, content)
                self.assertEqual(artifact.input_refs, assignment.input_refs)
                self.assertEqual(artifact.producer.role, role)
                self.assertEqual(artifact.producer.response_id, worker.response_id)
                self.assertNotIn("pending_operation", session_store.snapshot["state"])
            else:
                specialist_store.write_artifact.assert_not_awaited()
            worker.resources.assert_not_called()
            http_factory.assert_called_with(
                expected_call_id=worker.context.call_id, response_id=worker.response_id,
            )
            project_factory.assert_called_with(credential, http, worker.context.platform_headers())
            blob_transport.assert_called_with(role=role)
            blob_factory.assert_called_with(
                "https://syntheticstorage.blob.core.windows.net", credential=credential,
                retry_total=0, connection_timeout=10, read_timeout=30,
                logging_enable=False, max_single_get_size=131072,
                transport=blob_transport.return_value,
            )
            store_factory.assert_called_with(
                role=role, scope=self.runtime.scope, endpoint="https://syntheticstorage.blob.core.windows.net",
                containers={"control": "control", "candidates": "candidates", "reviews": "reviews"},
                credential=credential, service=self.backend, expected_private_ips=["10.0.0.4"],
            )
            self.assertEqual(specialist_store.verify_private_path.await_count, blob_factory.call_count)
            for resource in (credential, http, project_context, blob_context):
                self.assertEqual(resource.__aenter__.await_count, blob_factory.call_count)
                self.assertEqual(resource.__aexit__.await_count, blob_factory.call_count)
            if publication_crash and role == "architect":
                async with store.lock_manifest() as document:
                    saved = document.value
                    saved.effect.response_id = worker.response_id
                    saved.effect.output_ref = result.artifact_ref
                    await self.runtime.transition(store, document, saved, "output_observed")
                await self.runtime.publish(assignment.operation_id)
                await graph(self.runtime).run("Synthetic requirements.")
                followup = TestRuntime(self.backend, self.remote, response="followup-response")
                await followup.begin("Add a synthetic queue.")
                next_action, _ = await followup.route(followup.response_id)
                self.remote.crash = "unknown_response"
                with self.assertRaises(ProcessCrash):
                    await followup.execute(next_action)
                latest = await store.read_manifest()
                self.assertEqual(latest.children["architect"].hosted_id, child.hosted_id)
                next_locator = decode_document(locator.encode())
                next_locator["operation_id"] = latest.effect.operation_id
                with self.assertRaises(ProcessCrash):
                    await worker.specialize(canonical_bytes(next_locator).decode())
                self.assertEqual(agent.run.call_count, 2)
                self.assertEqual(agent.run.call_args.kwargs["session"].service_session_id, "inner-model-response")

    async def test_unknown_effect_is_held_and_never_redispatched(self):
        action = await self.step_to_call()
        self.remote.crash = "unknown_response"
        with self.assertRaises(ProcessCrash):
            await self.runtime.execute(action)
        resumed = TestRuntime(self.backend, self.remote)
        operation = await resumed.execute(action)
        continuing, result = await resumed.publish(operation)
        self.assertFalse(continuing)
        self.assertEqual(result["status"], "DELEGATION_UNCERTAIN")
        self.assertEqual(result["pending_effect"]["status"], "unknown")
        self.assertEqual(self.remote.calls, 1)
        with self.assertRaises(ArtifactError):
            await TestRuntime(self.backend, self.remote, response="new-response").begin("Do not replay.")
        self.assertEqual(self.remote.calls, 1)

    async def test_publication_crash_accepts_existing_output_without_second_dispatch(self):
        action = await self.step_to_call()
        operation = await self.runtime.execute(action)
        self.backend.crash_publication = True
        with self.assertRaises(ProcessCrash):
            await self.runtime.publish(operation)
        manifest = await make_store(self.backend, self.runtime.scope, "coordinator").read_manifest()
        self.assertIsNone(manifest.candidate)
        self.assertEqual(manifest.effect.status, "output_observed")
        resumed = TestRuntime(self.backend, self.remote)
        await resumed.publish(operation)
        manifest = await make_store(self.backend, self.runtime.scope, "coordinator").read_manifest()
        self.assertEqual(manifest.candidate_revision, 1)
        self.assertEqual(self.remote.calls, 1)
        await resumed.publish(operation)
        self.assertEqual(self.remote.calls, 1)

    async def test_fencing_failure_prevents_stale_manifest_publication(self):
        store = make_store(self.backend, self.runtime.scope, "coordinator")
        async with store.lock_manifest() as document:
            key = ("control", self.runtime.scope.prefix + "manifest.json")
            self.backend.leases[key] = "different-fenced-owner"
            with self.assertRaises(HttpResponseError):
                await document.save(Manifest(scope_binding=self.runtime.scope, generation=1))
        manifest = await store.read_manifest()
        self.assertEqual(manifest.generation, 0)

    async def test_two_parent_writers_cannot_acquire_the_same_lease(self):
        store = make_store(self.backend, self.runtime.scope, "coordinator")
        async with store.lock_manifest():
            with self.assertRaises(ArtifactError) as caught:
                await self.runtime.begin("Competing turn.")
            self.assertEqual(caught.exception.code, "PARENT_IN_USE")
        self.assertEqual(self.remote.calls, 0)

    async def test_two_parents_remain_isolated_on_the_same_backend(self):
        await graph(self.runtime).run("First parent only.")
        other = TestRuntime(self.backend, self.remote, parent="parent-two", response="response-two")
        await graph(other).run("Second parent only.")
        store = make_store(self.backend, self.runtime.scope, "coordinator")
        first = await store.read_manifest()
        second = await make_store(self.backend, other.scope, "coordinator").read_manifest()
        self.assertNotEqual(first.requirements.name, second.requirements.name)
        self.assertNotEqual(first.children["architect"].hosted_id, second.children["architect"].hosted_id)
        with self.assertRaises(ArtifactError):
            await store.read_artifact(second.candidate)

    async def test_followup_invalidates_old_approval_and_preserves_children(self):
        self.remote = RecordingRemote(self.backend)
        self.runtime = TestRuntime(self.backend, self.remote)
        initial = "Design a synthetic application with private ingress."
        update = "Add an asynchronous queue while preserving all earlier requirements."
        first_result = await graph(self.runtime).run(initial)
        store = make_store(self.backend, self.runtime.scope, "coordinator")
        first = await store.read_manifest()
        first_snapshot = copy.deepcopy(first.model_dump(mode="json"))
        first_calls = copy.deepcopy(self.remote.invocations)
        self.assertEqual(decode_document(first_result.get_outputs()[-1].strip().encode())["status"],
                         "ACCEPTED_ADVISORY")
        self.assertEqual([call["before"]["role"] for call in first_calls], ["architect", "reviewer"])
        self.assertEqual(first.calls, 2)
        self.assertEqual(first.turn, 1)
        self.assertEqual(first.review, Artifact.model_validate(first_calls[-1]["output"]).ref())
        followup = TestRuntime(self.backend, self.remote, response="followup-response")
        self.assertEqual(followup.scope, self.runtime.scope)
        self.assertNotEqual(followup.response_id, self.runtime.response_id)
        await followup.begin(update)
        pending = await store.read_manifest()
        self.assertIsNone(pending.candidate)
        self.assertIsNone(pending.review)
        self.assertEqual(pending.turn, 2)
        self.assertEqual(pending.children, first.children)
        self.assertNotEqual(pending.requirements, first.requirements)
        self.assertEqual(pending.calls, 0)
        self.assertEqual(pending.active_response_id, followup.response_id)
        requirements = await store.read_artifact(pending.requirements)
        self.assertEqual(requirements.content.chunks, [initial, update])
        second_result = await graph(followup).run(update)
        final = await store.read_manifest()
        self.assertEqual(final.candidate_revision, 2)
        self.assertEqual(final.turn, 2)
        self.assertEqual(final.calls, 2)
        self.assertEqual(first.model_dump(mode="json"), first_snapshot)
        self.assertEqual(self.remote.invocations[:2], first_calls)
        self.assert_recorded_bindings(final, ["architect", "reviewer", "architect", "reviewer"])

        for index, call in enumerate(self.remote.invocations):
            turn = 1 if index < 2 else 2
            self.assertEqual(call["assignment"]["requirements_revision"], turn)
            self.assertEqual(call["assignment"]["candidate_revision"], turn)
            self.assertEqual(call["requirements"]["chunks"], [initial] if turn == 1 else [initial, update])
            expected = [call["manifest"]["requirements"]]
            if call["before"]["role"] == "reviewer":
                expected.append(self.remote.invocations[index - 1]["output_ref"])
            self.assertEqual(call["assignment"]["input_refs"], expected)
        # These are the actual persisted refs at the follow-up send, not just a
        # reset observed before route/execute could accidentally restore approval.
        second_architect = self.remote.invocations[2]
        self.assertIsNone(second_architect["manifest"]["candidate"])
        self.assertIsNone(second_architect["manifest"]["review"])
        self.assertEqual(second_architect["assignment"]["input_refs"],
                         [pending.requirements.model_dump(mode="json")])
        self.assertNotEqual(final.candidate, first.candidate)
        self.assertNotEqual(final.review, first.review)
        self.assert_current_acceptance(second_result, final)

    def assert_recorded_bindings(self, final, roles):
        remote = self.remote
        self.assertEqual((remote.calls, remote.creates, remote.recoveries), (len(roles), 2, 0))
        self.assertEqual([call["before"]["role"] for call in remote.invocations], roles)
        self.assertEqual([child["role"] for child in remote.created], ["architect", "reviewer"])
        self.assertEqual(len(remote.prepared), 2)
        self.assertEqual(len({call["response_id"] for call in remote.invocations}), len(roles))
        self.assertEqual(set(final.children), {"architect", "reviewer"})

        def stable(child):
            # Service response state must advance; never compare all framework
            # state as if it were an immutable binding.
            return {
                "role": child["role"], "name": child["name"], "version": child["version"],
                "hosted_id": child["hosted_id"], "framework_id": child["framework"]["session_id"],
                "stored_hosted_id": child["framework"]["state"][FOUNDRY_HOSTED_AGENT_SESSION_ID_KEY],
            }

        baselines = {child["role"]: stable(child) for child in remote.prepared}
        self.assertEqual(len({child["hosted_id"] for child in baselines.values()}), 2)
        self.assertEqual(len({child["framework_id"] for child in baselines.values()}), 2)
        continuations = dict.fromkeys(baselines)
        for child in remote.created:
            self.assertEqual(stable(child), baselines[child["role"]])
        for call in remote.invocations:
            role = call["before"]["role"]
            self.assertEqual(call["scope"], self.runtime.scope.model_dump(mode="json"))
            self.assertEqual(call["manifest"]["scope_binding"], call["scope"])
            self.assertEqual(stable(call["before"]), baselines[role])
            self.assertEqual(stable(call["after"]), baselines[role])
            self.assertEqual(stable(call["manifest"]["children"][role]), baselines[role])
            self.assertEqual(call["manifest"]["children"][role]["framework"], call["before"]["framework"])
            self.assertEqual(call["before"]["framework"].get("service_session_id"), continuations[role])
            self.assertEqual(call["after"]["framework"]["service_session_id"], call["response_id"])
            self.assertNotEqual(call["response_id"], continuations[role])
            self.assertEqual(call["assignment"]["producer"]["session_id"], baselines[role]["hosted_id"])
            self.assertEqual(call["assignment"]["producer"]["name"], AGENTS[role])
            self.assertEqual(call["assignment"]["producer"]["version"], baselines[role]["version"])
            self.assertEqual(call["output"]["producer"]["response_id"], call["response_id"])
            self.assertEqual(call["output"]["input_refs"], call["assignment"]["input_refs"])
            continuations[role] = call["response_id"]
        for role, child in final.children.items():
            self.assertEqual(stable(child.model_dump(mode="json")), baselines[role])
            self.assertEqual(child.framework["service_session_id"], continuations[role])
            self.assertTrue(child.bound)
            self.assertEqual(baselines[role]["hosted_id"], baselines[role]["stored_hosted_id"])
            self.assertEqual(baselines[role]["name"], AGENTS[role])
            self.assertEqual(baselines[role]["version"], "2")

    def assert_current_acceptance(self, result, manifest):
        outputs = [decode_document(item.strip().encode()) for item in result.get_outputs()]
        final = outputs[-1]
        self.assertEqual(final["event"], "result")
        self.assertEqual(final["status"], "ACCEPTED_ADVISORY")
        self.assertEqual(manifest.status, "ACCEPTED_ADVISORY")
        self.assertIsNone(final["pending_effect"])
        for kind in ("requirements", "candidate", "review"):
            ref = getattr(manifest, kind)
            self.assertEqual(final["artifact_refs"][kind], ref.model_dump(mode="json"))
            artifact = Artifact.model_validate(final["artifact_evidence"][kind])
            self.assertEqual(artifact.ref(), ref)
            self.assertIn(ref, manifest.accepted)
            self.assertEqual(artifact.requirements_revision, manifest.turn)
        self.assertTrue(final["review"]["approved"])
        self.assertEqual(final["candidate"]["candidate_revision"], manifest.candidate_revision)
        self.assertEqual(final["review"]["candidate_revision"], manifest.candidate_revision)

    async def test_reject_revise_review_reuses_both_children_with_fresh_responses(self):
        self.remote = RecordingRemote(self.backend, reject_first_review=True)
        self.runtime = TestRuntime(self.backend, self.remote)
        initial = "Design a synthetic application with private ingress."
        result = await graph(self.runtime).run(initial)
        store = make_store(self.backend, self.runtime.scope, "coordinator")
        final = await store.read_manifest()
        self.assert_recorded_bindings(final, ["architect", "reviewer", "architect", "reviewer"])
        self.assertEqual((final.turn, final.candidate_revision, final.rounds, final.calls), (1, 2, 2, 4))
        a1, r1, a2, r2 = self.remote.invocations
        requirements_ref = final.requirements.model_dump(mode="json")
        for call, revision in zip(self.remote.invocations, (1, 1, 2, 2)):
            self.assertEqual(call["requirements"]["chunks"], [initial])
            self.assertEqual(call["assignment"]["requirements_revision"], 1)
            self.assertEqual(call["assignment"]["candidate_revision"], revision)
            self.assertEqual(call["output"]["candidate_revision"], revision)
        self.assertEqual(a1["assignment"]["input_refs"], [requirements_ref])
        self.assertEqual(r1["assignment"]["input_refs"], [requirements_ref, a1["output_ref"]])
        self.assertFalse(r1["output"]["content"]["approved"])
        self.assertTrue(r1["output"]["content"]["blocking_findings"])
        self.assertEqual(a2["manifest"]["candidate"], a1["output_ref"])
        self.assertEqual(a2["manifest"]["review"], r1["output_ref"])
        self.assertEqual(a2["assignment"]["input_refs"],
                         [requirements_ref, a1["output_ref"], r1["output_ref"]])
        self.assertIsNone(r2["manifest"]["review"])
        self.assertEqual(r2["assignment"]["input_refs"], [requirements_ref, a2["output_ref"]])
        self.assertTrue(r2["output"]["content"]["approved"])
        self.assertEqual(final.candidate.model_dump(mode="json"), a2["output_ref"])
        self.assertEqual(final.review.model_dump(mode="json"), r2["output_ref"])
        outputs = [decode_document(item.strip().encode()) for item in result.get_outputs()]
        self.assertEqual([item["role"] for item in outputs[:-1]],
                         ["architect", "reviewer", "architect", "reviewer"])
        self.assert_current_acceptance(result, final)

    async def test_wrong_producer_version_cannot_publish(self):
        action = await self.step_to_call()
        self.remote.corrupt_producer = True
        operation = await self.runtime.execute(action)
        with self.assertRaises(ArtifactError) as caught:
            await self.runtime.publish(operation)
        self.assertEqual(caught.exception.code, "SPECIALIST_ARTIFACT_PROVENANCE")
        manifest = await make_store(self.backend, self.runtime.scope, "coordinator").read_manifest()
        self.assertIsNone(manifest.candidate)

    async def test_native_host_enables_checkpoint_and_resilient_background_apis(self):
        from demo.host import main
        from demo.identity_probe import create_host_workflow, parse_host_turn
        with patch.dict(os.environ, {"DEMO_ROLE": "coordinator", "DEMO_RUNTIME": "native"}):
            with patch("demo.host.ProbeResponsesHostServer") as server:
                main()
        kwargs = server.call_args.kwargs
        self.assertTrue(kwargs["options"].resilient_background)
        self.assertEqual(kwargs["unsupported_options"], "error")
        self.assertIn("workflow", kwargs)
        self.assertIs(kwargs["workflow"], create_host_workflow)
        self.assertIs(kwargs["parse_response"], parse_host_turn)
        self.assertIn("checkpoint_store_provider", kwargs)
        self.assertNotIn("agent", kwargs)

    async def test_native_preparation_names_each_rejected_host_check_without_values(self):
        from demo.workflow import create_workflow, PROJECT
        config = {
            "is_hosted": True, "session_id": "synthetic-parent", "project_endpoint": PROJECT,
            "agent_name": AGENTS["coordinator"], "agent_version": "18",
        }
        scope = {
            "is_hosted": True, "session_id": "synthetic-parent",
            "user_id": "synthetic-user", "call_id": "synthetic-call",
        }
        context = SimpleNamespace(**scope)
        cases = (
            ({"project_endpoint": "synthetic-private-value"}, {}, "NATIVE_HOST_PROJECT"),
            ({"agent_name": "synthetic-private-value"}, {}, "NATIVE_HOST_AGENT"),
            ({"agent_version": ""}, {}, "NATIVE_HOST_VERSION"),
            ({}, {"is_hosted": False}, "NATIVE_HOST_PLATFORM"),
            ({}, {"user_id": None}, "NATIVE_HOST_PRINCIPAL"),
            ({}, {"call_id": None}, "NATIVE_HOST_CALL"),
            ({"session_id": "synthetic-private-value"}, {}, "NATIVE_HOST_SESSION"),
        )
        for changes, scope_changes, code in cases:
            request = SimpleNamespace(scope=SimpleNamespace(**(scope | scope_changes)), response_id="response")
            with self.subTest(code=code), \
                    patch.dict(os.environ, {"DEMO_ROLE": "coordinator", "DEMO_SPECIALIST_MODE": "hosted"}), \
                    patch("demo.workflow.AgentConfig.from_env", return_value=SimpleNamespace(**(config | changes))), \
                    patch("demo.workflow.get_request_context", return_value=context), \
                    self.assertLogs("demo.workflow", level="ERROR") as logs:
                with self.assertRaisesRegex(ArtifactError, code):
                    create_workflow(request)
                self.assertEqual(logs.records[0].getMessage(), f"Native workflow preparation rejected ({code}).")
                self.assertNotIn("synthetic-private-value", str(logs.output))

    async def test_native_preparation_unknown_error_never_logs_its_payload(self):
        from demo.workflow import create_workflow
        with patch("demo.workflow.WorkflowRuntime", side_effect=ArtifactError("synthetic-private-value")), \
                self.assertLogs("demo.workflow", level="ERROR") as logs:
            with self.assertRaises(ArtifactError):
                create_workflow(None)
        self.assertEqual(logs.records[0].getMessage(), "Native workflow preparation rejected (UNCLASSIFIED).")
        self.assertNotIn("synthetic-private-value", str(logs.output))


class LiveObservationTests(unittest.IsolatedAsyncioTestCase):
    def test_terminal_help_describes_maf_foundry_and_preserves_existing_switch(self):
        from demo.terminal import main
        output = io.StringIO()
        with patch("sys.argv", ["demo.terminal", "--help"]), redirect_stdout(output), \
                self.assertRaises(SystemExit) as exit_status:
            main()
        self.assertEqual(exit_status.exception.code, 0)
        help_text = output.getvalue()
        self.assertIn("--native", help_text)
        self.assertIn("MAF/Foundry workflow", help_text)
        self.assertNotIn("new native runtime", help_text)
        self.assertNotIn("legacy", help_text)

    async def test_pinned_sdk_resilient_identity_survives_serialization_and_handler_entry(self):
        from azure.ai.agentserver.core import get_request_context
        from azure.ai.agentserver.responses.hosting._orchestrator import _iter_handler_with_request_context
        from azure.ai.agentserver.responses.hosting._resilient_input import ResilientResponseInput
        from azure.ai.agentserver.responses.models._generated import CreateResponse
        from agent_framework_foundry_hosting._scope import FoundryRequestScope
        original = ResilientResponseInput(
            request=CreateResponse(input="Synthetic probe.", stream=True, background=True, store=True),
            response_id="synthetic-response", disposition="re-invoke",
            agent_session_id="synthetic-session", user_id_key="synthetic-user", call_id="synthetic-call",
        )
        restored = ResilientResponseInput.from_task_input(json.loads(json.dumps(original.to_task_input())))
        ambient = get_request_context()
        captured = []
        async def handler(parsed, context, cancellation):
            captured.append(FoundryRequestScope.from_context(
                SimpleNamespace(is_hosted=True, session_id="synthetic-session"), get_request_context(),
            ))
            yield {"type": "response.completed"}
        context = SimpleNamespace(platform_context=restored.platform_context())
        events = [event async for event in _iter_handler_with_request_context(
            handler, restored.request, context, asyncio.Event(), restored.agent_session_id,
        )]
        self.assertEqual(events, [{"type": "response.completed"}])
        self.assertEqual(len(captured), 1)
        self.assertEqual((captured[0].user_id, captured[0].call_id, captured[0].session_id),
                         ("synthetic-user", "synthetic-call", "synthetic-session"))
        self.assertIs(get_request_context(), ambient)
        for missing in ("user_id_key", "call_id"):
            with self.subTest(missing=missing):
                params = json.loads(json.dumps(original.to_task_input()))
                params[missing] = None
                incomplete = ResilientResponseInput.from_task_input(params)
                context = SimpleNamespace(platform_context=incomplete.platform_context())
                with self.assertRaisesRegex(RuntimeError, "trusted user ID and call ID"):
                    async for _ in _iter_handler_with_request_context(
                        handler, incomplete.request, context, asyncio.Event(), incomplete.agent_session_id,
                    ):
                        self.fail("Incomplete platform identity must not produce an event.")
                self.assertIs(get_request_context(), ambient)

    async def test_sdk_preparation_filter_reports_only_missing_trusted_scope(self):
        import logging
        from demo.host import WorkflowPreparationDiagnostics
        config = SimpleNamespace(session_id="synthetic-session")
        diagnostic = WorkflowPreparationDiagnostics(config)
        context = SimpleNamespace(session_id="synthetic-session", user_id=None, call_id="synthetic-private-call")
        record = logging.LogRecord(
            "agent_framework_foundry_hosting._workflow_responses", logging.ERROR, "", 1,
            "Native Responses workflow failed during %s (%s).", ("preparation", "RuntimeError"), None,
        )
        with patch("demo.host.get_request_context", return_value=context), \
                self.assertLogs("demo.host", level="ERROR") as logs:
            self.assertTrue(diagnostic.filter(record))
        self.assertIn("NATIVE_HOST_PRINCIPAL", logs.output[0])
        self.assertNotIn("synthetic-private-call", logs.output[0])

    async def test_native_specialist_stream_failure_recovers_only_a_known_response(self):
        from agent_framework.exceptions import ChatClientException
        from demo.workflow import WorkflowRemoteAgents
        remote = WorkflowRemoteAgents(None, {})
        async def interrupted(child, brief, remember):
            await remember("known-response")
            raise ChatClientException("Synthetic parser failure.")
        remote.recover = AsyncMock(return_value="existing output")
        observed = AsyncMock()
        with patch("demo.foundry.RemoteAgents.invoke", side_effect=interrupted) as invoke:
            self.assertEqual(await remote.invoke(None, {}, observed), "existing output")
        self.assertEqual(invoke.await_count, 1)
        remote.recover.assert_awaited_once_with(None, "known-response")
        with patch("demo.foundry.RemoteAgents.invoke", side_effect=ChatClientException("No known ID.")):
            with self.assertRaises(ChatClientException):
                await remote.invoke(None, {}, observed)
        self.assertEqual(remote.recover.await_count, 1)

    async def test_terminal_parser_failure_recovers_known_parent_without_resend(self):
        from agent_framework.exceptions import ChatClientException
        from demo.terminal import chat, write_state
        class Interrupted:
            def __init__(self):
                self.first = True
            async def __aenter__(self):
                return self
            async def __aexit__(self, *args):
                return False
            def __aiter__(self):
                return self
            async def __anext__(self):
                if self.first:
                    self.first = False
                    return AgentResponseUpdate(response_id="known-parent-response")
                raise ChatClientException("Synthetic timestamp parser failure.")
        session = AgentSession()
        session.state[FOUNDRY_HOSTED_AGENT_SESSION_ID_KEY] = "synthetic-parent"
        state = dict(schema_version=1, user="user", tenant="tenant", version="20", runtime="native",
                     framework=session.to_dict(), bound=True, pending=False)
        agent = MagicMock()
        agent.run.return_value = Interrupted()
        recovered = SimpleNamespace(id="known-parent-response", output_text=json.dumps({
            "event": "result", "status": "ACCEPTED_ADVISORY", "pending_effect": None,
        }))
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "parent.json"
            write_state(path, state, new=True)
            with patch("demo.terminal.verify_lab", return_value=("tenant", "subscription", "user")), \
                    patch("demo.terminal.AzureCliCredential"), patch("demo.terminal.data_client"), \
                    patch("demo.terminal.ProjectClient"), patch("demo.terminal.FoundryAgent", return_value=agent), \
                    patch("demo.terminal.rest", AsyncMock(return_value={
                        "status": "active", "version_indicator": {"agent_version": "20"},
                    })), patch("demo.terminal.recover_parent", AsyncMock(return_value=recovered)) as recover:
                await chat(SimpleNamespace(session_file=str(path), socks=None, native=True,
                                           recover_only=False, message="Synthetic turn.", show_ids=False))
            persisted = json.loads(path.read_text())
        self.assertFalse(persisted["pending"])
        self.assertEqual(persisted["framework"]["service_session_id"], "known-parent-response")
        self.assertEqual(agent.run.call_count, 1)
        self.assertEqual(recover.await_count, 1)

    async def test_storage_and_scope_observation_exposes_only_fixed_codes(self):
        from live_acceptance import storage_codes
        self.assertEqual(storage_codes("private-synthetic-value"), [])
        self.assertEqual(storage_codes(
            "private-synthetic-value RuntimeError: Foundry hosted requests require a trusted user ID and call ID."
        ), ["NATIVE_HOST_TRUSTED_USER_AND_CALL"])

    async def test_observation_retrieves_only_the_known_child_response(self):
        from live_acceptance import observe_pending_child
        child = SimpleNamespace(
            id="known-child", status="completed", error=None,
            model_dump=lambda **kwargs: {"id": "known-child", "status": "completed"},
        )
        client = SimpleNamespace(responses=SimpleNamespace(retrieve=AsyncMock(return_value=child)))
        project = SimpleNamespace(get_openai_client=MagicMock(return_value=client))
        response = SimpleNamespace(output_text=json.dumps({
            "event": "result", "native_workflow": "distributed-agents-v1", "status": "TimeoutError",
            "pending_effect": {"role": "architect", "response_id": "known-child"},
        }))
        proof = await observe_pending_child(project, response)
        self.assertEqual(proof["status"], "completed")
        client.responses.retrieve.assert_awaited_once_with("known-child")
        child.id = "different"
        with self.assertRaisesRegex(RuntimeError, "CHILD_RESPONSE_CHANGED"):
            await observe_pending_child(project, response)

    async def test_hosting_restart_stops_exact_active_parent_and_proves_idle_compute(self):
        from live_acceptance import stop_hosting_for_acceptance
        state = {
            "runtime": "native", "bound": True, "pending": False, "version": "20",
            "framework": {"state": {FOUNDRY_HOSTED_AGENT_SESSION_ID_KEY: "synthetic-parent"}},
        }
        active = {
            "agent_session_id": "synthetic-parent", "version_indicator": {"agent_version": "20"},
            "status": "active", "stopped_at": 100,
        }
        idle = dict(active, status="idle", stopped_at=200)
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "parent.json"
            journal = Path(str(path) + ".hosting-restart.json")

            async def stop(*args, **kwargs):
                self.assertEqual(json.loads(journal.read_text())["phase"], "stop_pending")
                self.assertEqual(args[0], "POST")
                self.assertTrue(args[1].endswith("/endpoint/sessions/synthetic-parent:stop"))
                return SimpleNamespace(status_code=204)

            http = SimpleNamespace(request=AsyncMock(side_effect=stop))
            credential = SimpleNamespace(get_token=AsyncMock(return_value=SimpleNamespace(token="synthetic")))
            with patch("live_acceptance.rest", side_effect=[active, idle]):
                proof = await stop_hosting_for_acceptance(http, credential, state, path)
            self.assertEqual(proof["phase"], "stop_confirmed")
            self.assertEqual(proof["stop_http_status"], 204)
            self.assertEqual(proof["stopped_at"], 200)
            with patch("live_acceptance.rest", return_value=idle):
                with self.assertRaisesRegex(RuntimeError, "RESTART_ALREADY_ATTEMPTED"):
                    await stop_hosting_for_acceptance(http, credential, state, path)
            http.request.assert_awaited_once()

    async def test_unknown_host_stop_is_observed_not_sent_again(self):
        from live_acceptance import stop_hosting_for_acceptance
        state = {
            "runtime": "native", "bound": True, "pending": False, "version": "20",
            "framework": {"state": {FOUNDRY_HOSTED_AGENT_SESSION_ID_KEY: "synthetic-parent"}},
        }
        active = {
            "agent_session_id": "synthetic-parent", "version_indicator": {"agent_version": "20"},
            "status": "active",
        }
        idle = dict(active, status="idle", stopped_at=200)
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "parent.json"
            http = SimpleNamespace(request=AsyncMock(side_effect=TimeoutError))
            credential = SimpleNamespace(get_token=AsyncMock(return_value=SimpleNamespace(token="synthetic")))
            with patch("live_acceptance.rest", return_value=active):
                with self.assertRaises(TimeoutError):
                    await stop_hosting_for_acceptance(http, credential, state, path)
            with patch("live_acceptance.rest", return_value=idle):
                proof = await stop_hosting_for_acceptance(http, credential, state, path)
            self.assertEqual(proof["phase"], "stop_confirmed")
            self.assertNotIn("stop_http_status", proof)
            http.request.assert_awaited_once()

    async def test_host_stop_requires_completed_native_parent_and_exact_version(self):
        from live_acceptance import stop_hosting_for_acceptance
        state = {
            "runtime": "native", "bound": True, "pending": False, "version": "20",
            "framework": {"state": {FOUNDRY_HOSTED_AGENT_SESSION_ID_KEY: "synthetic-parent"}},
        }
        http = SimpleNamespace(request=AsyncMock())
        with self.assertRaisesRegex(RuntimeError, "COMPLETED_NATIVE_PARENT_REQUIRED"):
            await stop_hosting_for_acceptance(http, None, dict(state, pending=True), Path("unused"))
        with patch("live_acceptance.rest", return_value={
            "agent_session_id": "synthetic-parent", "version_indicator": {"agent_version": "21"},
        }):
            with self.assertRaisesRegex(RuntimeError, "RESTART_PARENT_BINDING"):
                await stop_hosting_for_acceptance(http, None, state, Path("unused"))
        http.request.assert_not_called()

    async def test_observation_requires_owned_bound_pending_native_session(self):
        from live_acceptance import run
        state = {
            "schema_version": 1, "tenant": "synthetic-tenant", "user": "synthetic-user",
            "runtime": "native", "bound": True, "pending": True, "pending_response": "known-response",
        }
        for changes, error in (
            ({"tenant": "other-tenant"}, "SESSION_OWNER"),
            ({"user": "other-user"}, "SESSION_OWNER"),
            ({"schema_version": 2}, "SESSION_OWNER"),
            ({"runtime": "legacy"}, "BOUND_NATIVE_SESSION_REQUIRED"),
            ({"bound": False}, "BOUND_NATIVE_SESSION_REQUIRED"),
            ({"pending": False}, "KNOWN_PENDING_RESPONSE_REQUIRED"),
            ({"pending_response": None}, "KNOWN_PENDING_RESPONSE_REQUIRED"),
        ):
            path = SimpleNamespace(read_text=lambda: json.dumps(state | changes))
            with self.subTest(changes=changes), \
                    patch("live_acceptance.verify_lab", return_value=(
                        "synthetic-tenant", "synthetic-subscription", "synthetic-user",
                    )), patch("live_acceptance.private_state_path", return_value=path), \
                    patch("live_acceptance.AzureCliCredential") as credential:
                with self.assertRaisesRegex(RuntimeError, error):
                    await run(SimpleNamespace(scenario="observe", session_file="private-state"))
                credential.assert_not_called()

    async def observe(self, chunks, *, status=200, content_type="text/event-stream", response_id=None):
        from live_acceptance import observe_host_failure

        async def stream():
            for chunk in chunks:
                yield chunk

        response = SimpleNamespace(
            status_code=status, headers={"content-type": content_type}, aiter_bytes=stream,
        )
        manager = MagicMock()
        manager.__aenter__ = AsyncMock(return_value=response)
        manager.__aexit__ = AsyncMock(return_value=False)
        http = SimpleNamespace(stream=MagicMock(return_value=manager))
        credential = SimpleNamespace(get_token=AsyncMock(return_value=SimpleNamespace(token="synthetic-token")))
        result = await observe_host_failure(
            http, credential, "parent/with space", "18", response_id=response_id,
        )
        self.assertEqual(http.stream.call_args.args[0], "GET")
        self.assertTrue(http.stream.call_args.args[1].endswith(
            "/versions/18/sessions/parent%2Fwith%20space:logstream"
        ))
        self.assertEqual(http.stream.call_args.kwargs["params"], {"api-version": "v1"})
        self.assertEqual(http.stream.call_args.kwargs["headers"]["Accept"], "text/event-stream")
        manager.__aexit__.assert_awaited_once()
        return result

    async def test_ingress_observation_reports_only_exact_response_presence_flags(self):
        from live_acceptance import ingress_identity
        line = (
            "Creating response known-response: streaming=True background=True store=True "
            "model=synthetic-private-model conversation_id=synthetic-private-conversation "
            "previous_response_id=None has_user_id=False has_call_id=True"
        )
        self.assertIsNone(ingress_identity(line, "other-response"))
        self.assertIsNone(ingress_identity(line, None))
        self.assertIsNone(ingress_identity('{"message":42}', "known-response"))
        self.assertIsNone(ingress_identity(line + " synthetic-private-tail", "known-response"))
        chunk = ("data: " + json.dumps({"message": line}) + "\n\n").encode()
        proof = await self.observe([chunk[:30], chunk[30:], chunk], response_id="known-response")
        self.assertEqual(proof, {
            "failures": [], "limit": None,
            "ingress_identity": [{"has_user_id": False, "has_call_id": True}],
        })
        self.assertNotIn("synthetic-private", json.dumps(proof))

    async def test_outbound_observation_is_exact_response_bound_and_allowlisted(self):
        from live_acceptance import outbound_identity
        binding = hashlib.sha256(b"known-response").hexdigest()
        line = (
            f"Native outbound context response_binding={binding} role=architect "
            "has_call_id=True call_matches_context=True "
            "has_delegated_user=False has_container_user=False."
        )
        for invalid in (
            line + " private tail", line.replace("role=architect", "role=private-role"),
            line.replace("has_call_id=True", "has_call_id=private-value"), '{"message":42}',
        ):
            self.assertIsNone(outbound_identity(invalid, "known-response"))
        self.assertIsNone(outbound_identity(line, "other-response"))
        self.assertIsNone(outbound_identity(line, None))
        chunk = ("data: " + json.dumps({"message": line}) + "\n\n").encode()
        proof = await self.observe([chunk[:30], chunk[30:], chunk], response_id="known-response")
        self.assertEqual(proof, {
            "failures": [], "limit": None, "outbound_context": [{
                "role": "architect", "has_call_id": True, "call_matches_context": True,
                "has_delegated_user": False, "has_container_user": False,
            }],
        })
        self.assertNotIn(binding, json.dumps(proof))

    async def test_failed_child_observation_also_reads_exact_parent_context_without_resend(self):
        from live_acceptance import run
        state = {
            "schema_version": 1, "tenant": "tenant", "user": "user", "runtime": "native",
            "bound": True, "pending": True, "pending_response": "known-parent-response", "version": "22",
            "framework": {"state": {FOUNDRY_HOSTED_AGENT_SESSION_ID_KEY: "known-parent-session"}},
        }
        response = SimpleNamespace(
            id="known-parent-response", status="completed",
            model_dump=lambda **kwargs: {"id": "known-parent-response", "status": "completed"},
        )
        client = SimpleNamespace(responses=SimpleNamespace(
            retrieve=AsyncMock(return_value=response), create=AsyncMock(),
        ))
        project = MagicMock()
        project.__aenter__ = AsyncMock(return_value=project)
        project.__aexit__ = AsyncMock(return_value=False)
        project.get_openai_client.return_value = client
        child = {
            "role": "architect", "response_id": "known-child-response", "status": "failed",
            "agent_session_id": "known-child-session",
        }
        output = io.StringIO()
        with patch("live_acceptance.verify_lab", return_value=("tenant", "subscription", "user")), \
                patch("live_acceptance.private_state_path",
                      return_value=SimpleNamespace(read_text=lambda: json.dumps(state))), \
                patch("live_acceptance.AzureCliCredential"), patch("live_acceptance.data_client"), \
                patch("live_acceptance.ProjectClient", return_value=project), \
                patch("live_acceptance.observe_pending_child", AsyncMock(return_value=child)), \
                patch("live_acceptance.rest", AsyncMock(return_value={
                    "version_indicator": {"agent_version": "17"},
                })) as rest, \
                patch("live_acceptance.observe_host_failure", AsyncMock(side_effect=[
                    {"failures": []}, {"failures": [], "outbound_context": []},
                ])) as observe, redirect_stdout(output):
            await run(SimpleNamespace(scenario="observe", session_file="private-state", socks=None))
        self.assertEqual(observe.await_count, 2)
        self.assertEqual(observe.await_args_list[0].args[2:], ("known-child-session", "17"))
        self.assertEqual(observe.await_args_list[0].kwargs,
                         {"role": "architect", "response_id": "known-child-response", "structured": True})
        self.assertEqual(observe.await_args_list[1].args[2:], ("known-parent-session", "22"))
        self.assertEqual(observe.await_args_list[1].kwargs,
                         {"response_id": "known-parent-response", "structured": True})
        self.assertIn("parent_host_diagnostics", json.loads(output.getvalue()))
        client.responses.retrieve.assert_awaited_once_with(
            "known-parent-response", extra_query={"agent_session_id": "known-parent-session"},
        )
        client.responses.create.assert_not_awaited()
        self.assertEqual(rest.await_args.args[2], "GET")

    async def test_host_failure_observation_suppresses_arbitrary_log_content(self):
        line = (
            b'event: log\r\ndata: {"message":"ERROR: Native Responses workflow failed '
            b'during preparation (ArtifactError)."}\r\n\r\n'
        )
        result = await self.observe([
            b'data: {"message":"synthetic private token, endpoint and user"}\n\n',
            line[:40], line[40:], line, b'data: malformed JSON\n\n',
        ])
        self.assertEqual(result, {
            "failures": [{"phase": "preparation", "exception_type": "ArtifactError"}], "limit": None,
        })

    async def test_host_failure_log_stream_is_byte_bounded(self):
        result = await self.observe([b"data: " + b"x" * 131073])
        self.assertEqual(result, {"failures": [], "limit": "bytes"})

    async def test_host_failure_rejects_http_failure_and_non_sse_response(self):
        with self.assertRaisesRegex(RuntimeError, "HOST_LOG_HTTP_403"):
            await self.observe([], status=403)
        with self.assertRaisesRegex(RuntimeError, "HOST_LOG_SSE_REQUIRED"):
            await self.observe([], content_type="application/json")

    async def test_host_failure_classification_is_allowlisted(self):
        from live_acceptance import workflow_failure
        for line in (
            '{"message":42}', '{"message":"unfinished"', '["invalid shape"]',
            "Native Responses workflow failed during private-phase (ArtifactError).",
            "Native Responses workflow failed during preparation (PrivateToken).",
            "Native Responses workflow failed during preparation (ArtifactError). private tail",
        ):
            self.assertIsNone(workflow_failure(line))
        self.assertEqual(workflow_failure(
            'Native workflow preparation rejected (NATIVE_HOST_PROJECT).'
        ), {"phase": "preparation", "exception_type": "ArtifactError", "check": "NATIVE_HOST_PROJECT"})
        self.assertIsNone(workflow_failure(
            'Native workflow preparation rejected (SYNTHETIC_PRIVATE_TOKEN).'
        ))


if __name__ == "__main__":
    unittest.main()
