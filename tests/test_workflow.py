from __future__ import annotations

import asyncio
import copy
import os
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


if __name__ == "__main__":
    unittest.main()
