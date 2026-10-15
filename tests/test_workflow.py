from __future__ import annotations

import asyncio
import copy
import json
import os
import tempfile
import unittest
import uuid
from pathlib import Path
from contextlib import asynccontextmanager
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
    BeginExecutor, EffectExecutor, NativeRuntime, OutputLocator, PublishExecutor, RouteExecutor,
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
        content = (
            Candidate(
                requirements_revision=assignment.requirements_revision,
                candidate_revision=assignment.candidate_revision, design="Synthetic private design.",
            ) if child.role == "architect" else Review(
                requirements_revision=assignment.requirements_revision, candidate_revision=assignment.candidate_revision,
                approved=True, blocking_findings=["blocker"] if self.contradict_review else [],
                unresolved_requirements=[], recommendation="Synthetic current approval.",
            )
        )
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

    async def recover(self, child, response_id):
        self.recoveries += 1
        return self.responses[response_id]


def make_store(backend, scope, role):
    return BlobArtifacts(
        role=role, scope=scope, endpoint="https://syntheticstorage.blob.core.windows.net",
        containers={"control": "control", "candidates": "candidates", "reviews": "reviews"},
        credential=None, service=backend,
    )


class TestRuntime(NativeRuntime):
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

    async def test_native_resources_forward_sdk_context_without_redelegating_platform_user(self):
        import httpx2
        from azure.ai.agentserver.core import FoundryAgentRequestContext
        from azure.core.credentials import AccessToken
        from agent_framework.exceptions import ChatClientException
        from demo.contracts import PROJECT
        from urllib.parse import urlsplit
        self.runtime.context = FoundryAgentRequestContext(
            session_id=self.runtime.scope.parent_session, user_id=self.runtime.scope.principal,
            call_id="synthetic-opaque-call",
        )
        seen = []
        def handle(request):
            seen.append({"headers": {
                key: request.headers[key] for key in (
                    "x-agent-foundry-call-id", "x-ms-user-identity", "x-agent-user-id",
                ) if key in request.headers
            }, "method": request.method, "path": request.url.path,
                "session": json.loads(request.content).get("agent_session_id")})
            return httpx2.Response(418, json={"error": {
                "message": "Synthetic context probe.", "type": "probe", "code": "probe",
            }})
        credential = MagicMock()
        credential.__aenter__ = AsyncMock(return_value=credential)
        credential.__aexit__ = AsyncMock(return_value=False)
        credential.get_token = AsyncMock(return_value=AccessToken("synthetic-token", 4102444800))
        store = MagicMock()
        store.__aenter__ = AsyncMock(return_value=store)
        store.__aexit__ = AsyncMock(return_value=False)
        store.verify_private_path = AsyncMock()
        http = httpx2.AsyncClient(transport=httpx2.MockTransport(handle))
        session = AgentSession()
        session.state[FOUNDRY_HOSTED_AGENT_SESSION_ID_KEY] = "a" * 32
        child = Child(role="architect", name=AGENTS["architect"], version="1",
                      hosted_id="a" * 32, framework=session.to_dict())
        with patch("demo.workflow.ManagedIdentityCredential", return_value=credential), \
                patch("demo.workflow.data_client", return_value=http), \
                patch("demo.workflow.storage", return_value=store):
            async with NativeRuntime.resources(self.runtime) as (_, remote, _, _, _, _):
                stream = remote._client(child).run("Synthetic probe.", session=session, stream=True)
                with self.assertRaises(ChatClientException):
                    async with stream:
                        async for _ in stream:
                            pass
        self.assertEqual(seen, [{
            "headers": {"x-agent-foundry-call-id": "synthetic-opaque-call"},
            "method": "POST",
            "path": urlsplit(PROJECT).path + "/agents/" + AGENTS["architect"]
                    + "/endpoint/protocols/openai/responses",
            "session": "a" * 32,
        }])
        store.verify_private_path.assert_awaited_once()

    async def step_to_call(self):
        await self.runtime.begin("Synthetic requirements.")
        action, result = await self.runtime.route(self.runtime.response_id)
        self.assertIsNone(result)
        return action

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

    async def test_native_graph_reaches_current_accepted_remote_outputs(self):
        result = await graph(self.runtime).run("Synthetic requirements.")
        outputs = [decode_document(item.strip().encode()) for item in result.get_outputs()]
        final = outputs[-1]
        self.assertEqual(final["status"], "ACCEPTED_ADVISORY")
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

    async def check_specialist_model_recovery(self, *, known, publication_crash=False):
        action = await self.step_to_call()
        self.remote.crash = "unknown_response"
        with self.assertRaises(ProcessCrash):
            await self.runtime.execute(action)
        store = make_store(self.backend, self.runtime.scope, "coordinator")
        manifest = await store.read_manifest()
        assignment = await store.read_assignment(manifest.effect.operation_id)
        child = manifest.children["architect"]
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
        )
        retrieve = AsyncMock(return_value=SimpleNamespace(
            id="inner-model-response", status="completed", output_text=canonical_bytes(content).decode(),
        ))
        project = SimpleNamespace(get_openai_client=lambda: SimpleNamespace(
            responses=SimpleNamespace(retrieve=retrieve),
        ))
        worker = TestRuntime(self.backend, self.remote)
        worker.role = "architect"
        worker.response_id = "trusted-worker-outer-response"
        worker.config = SimpleNamespace(
            is_hosted=True, session_id=child.hosted_id, project_endpoint=self.runtime.scope.project,
            agent_name=child.name, agent_version=child.version,
        )
        worker.context = SimpleNamespace(
            session_id=child.hosted_id, user_id=self.runtime.scope.principal, call_id="trusted-worker-call",
        )

        @asynccontextmanager
        async def resources(**_kwargs):
            yield make_store(self.backend, self.runtime.scope, "architect"), None, project, None, None, {}

        worker.resources = resources
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
                raise ProcessCrash()

        agent = MagicMock()
        agent.__aenter__ = AsyncMock(return_value=agent)
        agent.__aexit__ = AsyncMock(return_value=None)
        agent.run.return_value = InterruptedStream()
        with patch("demo.workflow.AgentSessionStoreProvider") as provider, \
                patch("demo.workflow.Agent", return_value=agent), \
                patch("demo.workflow.FoundryChatClient"):
            provider.return_value.get_store.return_value = session_store
            with self.assertRaises(ProcessCrash):
                await worker.specialize(locator)
            self.assertEqual(
                session_store.snapshot["state"]["pending_operation"]["response_id"],
                "inner-model-response" if known else None,
            )
            if known:
                if publication_crash:
                    with self.assertRaises(ProcessCrash):
                        await worker.specialize(locator)
                result = OutputLocator.model_validate(decode_document((await worker.specialize(locator)).encode()))
                self.assertEqual(result.artifact_ref.artifact_type, "candidate")
                retrieve.assert_awaited_once_with("inner-model-response")
                self.assertNotIn("pending_operation", session_store.snapshot["state"])
            else:
                with self.assertRaises(ArtifactError) as caught:
                    await worker.specialize(locator)
                self.assertEqual(caught.exception.code, "SPECIALIST_MODEL_EFFECT_UNCERTAIN")
                retrieve.assert_not_awaited()
            agent.run.assert_called_once()
            if publication_crash:
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
        await graph(self.runtime).run("First requirements.")
        store = make_store(self.backend, self.runtime.scope, "coordinator")
        first = await store.read_manifest()
        followup = TestRuntime(self.backend, self.remote, response="followup-response")
        await followup.begin("Add a queue while preserving all earlier requirements.")
        pending = await store.read_manifest()
        self.assertIsNone(pending.candidate)
        self.assertIsNone(pending.review)
        self.assertEqual(pending.turn, 2)
        self.assertEqual(pending.children, first.children)
        await graph(followup).run("Add a queue while preserving all earlier requirements.")
        final = await store.read_manifest()
        self.assertEqual(final.candidate_revision, 2)
        self.assertEqual(self.remote.creates, 2)
        self.assertEqual(final.children["architect"].hosted_id, first.children["architect"].hosted_id)

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
        with patch.dict(os.environ, {"DEMO_ROLE": "coordinator", "DEMO_RUNTIME": "native"}):
            with patch("demo.host.ResponsesHostServer") as server:
                main()
        kwargs = server.call_args.kwargs
        self.assertTrue(kwargs["options"].resilient_background)
        self.assertEqual(kwargs["unsupported_options"], "error")
        self.assertIn("workflow", kwargs)
        self.assertIn("checkpoint_store_provider", kwargs)
        self.assertNotIn("agent", kwargs)

    async def test_native_preparation_names_each_rejected_host_check_without_values(self):
        from demo.workflow import create_native_workflow, PROJECT
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
                    create_native_workflow(request)
                self.assertEqual(logs.records[0].getMessage(), f"Native workflow preparation rejected ({code}).")
                self.assertNotIn("synthetic-private-value", str(logs.output))

    async def test_native_preparation_unknown_error_never_logs_its_payload(self):
        from demo.workflow import create_native_workflow
        with patch("demo.workflow.NativeRuntime", side_effect=ArtifactError("synthetic-private-value")), \
                self.assertLogs("demo.workflow", level="ERROR") as logs:
            with self.assertRaises(ArtifactError):
                create_native_workflow(None)
        self.assertEqual(logs.records[0].getMessage(), "Native workflow preparation rejected (UNCLASSIFIED).")
        self.assertNotIn("synthetic-private-value", str(logs.output))


class LiveObservationTests(unittest.IsolatedAsyncioTestCase):
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
        from demo.host import NativePreparationDiagnostics
        config = SimpleNamespace(session_id="synthetic-session")
        diagnostic = NativePreparationDiagnostics(config)
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
        from demo.workflow import NativeRemoteAgents
        remote = NativeRemoteAgents(None, {})
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
