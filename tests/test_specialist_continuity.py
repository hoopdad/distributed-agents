"""Offline proof at both real specialists' persisted history/model boundaries.

No hosted execution or model memory is claimed: only external storage, connection
setup and the model transport are controlled. Role stages, Agent.run, AgentSession
serialization and the framework's continuation updates execute normally.
"""

from __future__ import annotations

import copy
import os
import time
import unittest
from contextlib import ExitStack
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

from agent_framework import AgentSession, ChatResponse, ChatResponseUpdate, Content, ResponseStream
from agent_framework.foundry import FoundryChatClient

from demo.architect_agent import ArchitectAgent
from demo.reviewer_agent import ReviewerAgent
from demo.artifacts import (
    Artifact, ArtifactError, Assignment, Candidate, OutputLocator, Producer, Requirements,
    Review, ScopeBinding, canonical_bytes, decode_document, digest,
)
from demo.contracts import AGENTS


class SerializedHistory:
    """Round-trip by value, never return the object handed to set()."""

    def __init__(self):
        self.snapshot = None
        self.writes = []
        self.fail_after_output = False

    async def get(self, key):
        assert key == "history"
        return AgentSession.from_dict(copy.deepcopy(self.snapshot)) if self.snapshot else None

    async def set(self, key, session):
        assert key == "history"
        if self.fail_after_output and "pending_operation" not in session.state:
            self.fail_after_output = False
            raise RuntimeError("synthetic history persistence interruption")
        self.snapshot = decode_document(canonical_bytes(session.to_dict()))
        self.writes.append(copy.deepcopy(self.snapshot))


class ArtifactBoundary:
    """Synthetic immutable storage; the actual role builds/validates the artifacts."""

    def __init__(self):
        self.values = {}
        self.reads = []
        self.writes = []

    async def read_artifact(self, ref):
        self.reads.append(ref.model_copy(deep=True))
        return Artifact.model_validate(copy.deepcopy(self.values[ref.name]))

    async def write_artifact(self, artifact):
        ref = artifact.ref()
        value = artifact.model_dump(mode="json")
        if ref.name in self.values and self.values[ref.name] != value:
            raise AssertionError("Fixture attempted to replace an immutable output")
        self.values[ref.name] = copy.deepcopy(value)
        self.writes.append(copy.deepcopy(value))
        return ref


class SpecialistHarness:
    def __init__(self, case, role):
        self.case, self.role = case, role
        self.cls = ArchitectAgent if role == "architect" else ReviewerAgent
        self.module = f"demo.{role}_agent"
        self.scope = ScopeBinding(
            project="https://example.services.ai.azure.com/api/projects/example-project",
            tenant="11111111-1111-1111-1111-111111111111",
            principal="synthetic-user", parent_session="synthetic-parent",
        )
        self.config = SimpleNamespace(
            is_hosted=True, session_id=f"{role}-hosted-child",
            agent_name=AGENTS[role], agent_version="7", project_endpoint=self.scope.project,
        )
        self.context = SimpleNamespace(
            session_id=self.config.session_id, user_id=self.scope.principal,
            call_id="synthetic-call",
        )
        self.history, self.artifacts = SerializedHistory(), ArtifactBoundary()
        self.runs, self.model_calls, self.provider_calls = [], [], []
        self.headers = {"x-agent-foundry-call-id": "synthetic-call"}
        self.retrieve = AsyncMock()
        self.project = SimpleNamespace(
            get_openai_client=lambda **_kwargs: SimpleNamespace(responses=SimpleNamespace(retrieve=self.retrieve)),
        )
        self.assignment = None
        self.existing = None
        self.model_response = None
        self.model_text = None

    def operation(self, number):
        revision = number
        requirements = Requirements(
            chunks=["Synthetic private-ingress application."] + (
                ["Add an asynchronous queue; retain private ingress."] if number > 1 else []
            ),
        )
        producer = Producer(
            role="coordinator", name=AGENTS["coordinator"], version="7",
            session_id=self.scope.parent_session, response_id=f"parent-response-{number}",
        )
        inputs = [Artifact(
            artifact_type="requirements", scope_binding=self.scope,
            operation_id=f"{number:032x}", producer=producer, input_refs=[],
            requirements_revision=revision, content=requirements, content_sha256=digest(requirements),
        )]
        if self.role == "reviewer":
            candidate = Candidate(
                requirements_revision=revision, candidate_revision=revision,
                design=f"Private design revision {revision}; queue={number > 1}.",
            )
            inputs.append(Artifact(
                artifact_type="candidate", scope_binding=self.scope,
                operation_id=f"{number + 10:032x}",
                producer=Producer(
                    role="architect", name=AGENTS["architect"], version="7",
                    session_id="architect-hosted-child", response_id=f"architect-response-{number}",
                ),
                input_refs=[inputs[0].ref()], requirements_revision=revision,
                candidate_revision=revision, content=candidate, content_sha256=digest(candidate),
            ))
        for value in inputs:
            self.artifacts.values[value.ref().name] = value.model_dump(mode="json")
        self.assignment = Assignment(
            scope_binding=self.scope, operation_id=f"{number + 100:032x}",
            producer=Producer(
                role=self.role, name=AGENTS[self.role], version="7",
                session_id=self.config.session_id,
            ),
            input_refs=[value.ref() for value in inputs],
            requirements_revision=revision, candidate_revision=revision,
            output_type="candidate" if self.role == "architect" else "review",
            deadline_epoch=int(time.time()) + 600,
        )
        content = Candidate(
            requirements_revision=revision, candidate_revision=revision,
            design=f"Synthetic design {number}.",
        ) if self.role == "architect" else Review(
            requirements_revision=revision, candidate_revision=revision,
            approved=True, blocking_findings=[], unresolved_requirements=[],
            recommendation=f"Synthetic review {number}.",
        )
        self.model_text = canonical_bytes(content).decode()
        self.model_response = f"{self.role}-model-response-{number}"
        return self.assignment

    async def brief(self):
        read = (
            self.cls.read_requirements_and_prior_work if self.role == "architect"
            else self.cls.read_requirements_and_design
        )
        return await read(self.artifacts, self.assignment)

    def pending(self, brief, response_id):
        return {
            "id": self.assignment.operation_id, "input_sha256": digest(brief),
            "model_deployment": "synthetic-worker", "response_id": response_id,
        }

    def patches(self):
        stack = ExitStack()
        stack.enter_context(patch.dict(os.environ, {
            "SPECIALIST_MODEL_DEPLOYMENT": "synthetic-worker",
            "FOUNDRY_PROJECT_ENDPOINT": self.scope.project,
        }))

        async def connect(*_args, **_kwargs):
            return self.artifacts, self.project, self.headers, self.assignment, self.existing

        # Do not mock the role class or Agent.run: record the real call then delegate.
        original_run = self.cls.run

        def record_run(agent, text, *, session, **kwargs):
            self.runs.append({
                "brief": decode_document(text.encode()),
                "session": copy.deepcopy(session.to_dict()),
            })
            return original_run(agent, text, session=session, **kwargs)

        def model(_client, *, messages, options, stream=False, **_kwargs):
            self.case.assertTrue(stream)
            self.case.assertEqual(
                self.history.snapshot["state"]["pending_operation"],
                self.pending(self.runs[-1]["brief"], None),
            )
            self.model_calls.append(copy.deepcopy(dict(options)))
            response_id, text = self.model_response, self.model_text

            async def updates():
                yield ChatResponseUpdate(
                    role="assistant", response_id=response_id, conversation_id=response_id,
                    contents=[Content.from_text(text)], finish_reason="stop",
                )

            return ResponseStream(updates(), finalizer=ChatResponse.from_updates)

        stack.enter_context(patch.object(self.cls, "connect_and_load_assignment", side_effect=connect))
        stack.enter_context(patch.object(self.cls, "run", record_run))
        # Retain real FoundryChatClient / framework plumbing, replace only external model transport.
        stack.enter_context(patch.object(FoundryChatClient, "_inner_get_response", model))
        provider = stack.enter_context(patch(f"{self.module}.AgentSessionStoreProvider"))

        def get_store(*, config, platform_context):
            provider.assert_called_with(store_name="specialist_history_v2")
            self.case.assertIs(config, self.config)
            self.case.assertIs(platform_context, self.context)
            self.provider_calls.append((config.session_id, config.agent_version, platform_context.session_id))
            return self.history

        provider.return_value.get_store.side_effect = get_store
        return stack, provider

    async def run(self, outer_response):
        value = await self.cls.run_assignment(
            "synthetic-locator", config=self.config, context=self.context,
            scope=self.scope, response_id=outer_response,
        )
        return OutputLocator.model_validate(decode_document(value.encode())).artifact_ref


class SpecialistContinuityTests(unittest.IsolatedAsyncioTestCase):
    async def check_continuation(self, role):
        h = SpecialistHarness(self, role)
        with h.patches()[0]:
            first_assignment = h.operation(1)
            first_ref = await h.run("outer-first")
            first = copy.deepcopy(h.history.snapshot)
            self.assertEqual(first["service_session_id"], f"{role}-model-response-1")
            self.assertNotIn("pending_operation", first["state"])
            self.assertEqual(
                h.history.writes[-2]["state"]["pending_operation"]["response_id"],
                f"{role}-model-response-1",
            )
            # A marker makes loss of non-continuation framework state observable too.
            h.history.snapshot["state"]["synthetic_history_marker"] = {"turn": 1}
            second_assignment = h.operation(2)
            second_ref = await h.run("outer-second")
            second = copy.deepcopy(h.history.snapshot)
            self.assertEqual(len(h.runs), 2)
            self.assertEqual(len(h.model_calls), 2)
            restored = h.runs[1]["session"]
            self.assertEqual(restored["session_id"], first["session_id"])
            self.assertEqual(restored["service_session_id"], first["service_session_id"])
            self.assertEqual(restored["state"]["synthetic_history_marker"], {"turn": 1})
            self.assertEqual(restored["state"]["pending_operation"], h.pending(h.runs[1]["brief"], None))
            self.assertEqual(h.model_calls[1]["conversation_id"], first["service_session_id"])
            self.assertEqual(second["session_id"], first["session_id"])
            self.assertEqual(second["service_session_id"], f"{role}-model-response-2")
            self.assertNotEqual(second["service_session_id"], first["service_session_id"])
            self.assertNotIn("pending_operation", second["state"])
            self.assertEqual(first["service_session_id"], f"{role}-model-response-1")
            self.assertEqual(h.provider_calls, [(h.config.session_id, "7", h.config.session_id)] * 2)
            h.retrieve.assert_not_awaited()
            self.assertEqual(h.artifacts.reads, first_assignment.input_refs + second_assignment.input_refs)
            for ref, assignment, outer in (
                (first_ref, first_assignment, "outer-first"), (second_ref, second_assignment, "outer-second"),
            ):
                artifact = Artifact.model_validate(h.artifacts.values[ref.name])
                self.assertEqual(artifact.ref(), ref)
                self.assertEqual(artifact.input_refs, assignment.input_refs)
                self.assertEqual(artifact.producer, assignment.producer.model_copy(update={"response_id": outer}))
                self.assertEqual(artifact.requirements_revision, assignment.requirements_revision)
                self.assertEqual(artifact.candidate_revision, assignment.candidate_revision)
            second_brief = copy.deepcopy(h.runs[1]["brief"])
            second_pending = copy.deepcopy(restored["state"]["pending_operation"])
            # Same operation and brief, deliberately absent history: no first continuation.
            h.history = SerializedHistory()
            h.artifacts.values.pop(second_ref.name)
            await h.run("outer-negative-control")
            fresh = h.runs[2]["session"]
            self.assertEqual(h.runs[2]["brief"], second_brief)
            self.assertEqual(fresh["state"]["pending_operation"], second_pending)
            self.assertNotEqual(fresh["session_id"], first["session_id"])
            self.assertIsNone(fresh["service_session_id"])
            self.assertNotIn("synthetic_history_marker", fresh["state"])
            self.assertIsNone(h.model_calls[2].get("conversation_id"))
            self.assertEqual(h.history.snapshot["service_session_id"], f"{role}-model-response-2")
            self.assertNotIn("pending_operation", h.history.snapshot["state"])

    async def test_architect_persists_and_restores_model_continuation_with_fresh_history_control(self):
        await self.check_continuation("architect")

    async def test_reviewer_persists_and_restores_model_continuation_with_fresh_history_control(self):
        await self.check_continuation("reviewer")

    async def check_recovery(self, role):
        h = SpecialistHarness(self, role)
        with h.patches()[0]:
            h.operation(1)
            await h.run("outer-first")
            first = copy.deepcopy(h.history.snapshot)
            assignment = h.operation(2)
            brief = await h.brief()
            h.history.snapshot["state"]["pending_operation"] = h.pending(brief, h.model_response)
            h.retrieve.return_value = SimpleNamespace(
                id=h.model_response, status="completed", output_text=h.model_text,
            )
            h.runs.clear()
            h.model_calls.clear()
            ref = await h.run("outer-recovered")
            h.retrieve.assert_awaited_once_with(f"{role}-model-response-2")
            self.assertEqual(h.runs, [])
            self.assertEqual(h.model_calls, [])
            self.assertEqual(h.history.snapshot["session_id"], first["session_id"])
            self.assertEqual(h.history.snapshot["service_session_id"], f"{role}-model-response-2")
            self.assertNotIn("pending_operation", h.history.snapshot["state"])
            artifact = Artifact.model_validate(h.artifacts.values[ref.name])
            self.assertEqual(artifact.input_refs, assignment.input_refs)
            self.assertEqual(artifact.producer.response_id, "outer-recovered")
            self.assertEqual(artifact.producer.session_id, h.config.session_id)
            self.assertEqual(artifact.producer.version, "7")

    async def test_architect_known_response_recovery_persists_continuation_without_send(self):
        await self.check_recovery("architect")

    async def test_reviewer_known_response_recovery_persists_continuation_without_send(self):
        await self.check_recovery("reviewer")

    async def check_holds(self, role):
        h = SpecialistHarness(self, role)
        with h.patches()[0]:
            h.operation(2)
            brief = await h.brief()
            baseline = AgentSession().to_dict()
            for field, invalid in (
                ("response_id", None), ("id", "f" * 32),
                ("input_sha256", "f" * 64), ("model_deployment", "different-deployment"),
            ):
                with self.subTest(role=role, field=field):
                    h.history.snapshot = copy.deepcopy(baseline)
                    pending = h.pending(brief, "known-model-response")
                    pending[field] = invalid
                    h.history.snapshot["state"]["pending_operation"] = pending
                    before = copy.deepcopy(h.history.snapshot)
                    with self.assertRaisesRegex(ArtifactError, "SPECIALIST_MODEL_EFFECT_UNCERTAIN"):
                        await h.run("outer-held")
                    self.assertEqual(h.history.snapshot, before)
            self.assertEqual(h.runs, [])
            self.assertEqual(h.model_calls, [])
            self.assertEqual(h.artifacts.writes, [])
            h.retrieve.assert_not_awaited()

    async def test_architect_unknown_and_mismatched_pending_effects_remain_held(self):
        await self.check_holds("architect")

    async def test_reviewer_unknown_and_mismatched_pending_effects_remain_held(self):
        await self.check_holds("reviewer")

    async def check_incomplete_recovery(self, role):
        h = SpecialistHarness(self, role)
        with h.patches()[0]:
            h.operation(2)
            brief = await h.brief()
            session = AgentSession(service_session_id="prior-completed-model-response")
            session.state["pending_operation"] = h.pending(brief, "known-model-response")
            h.history.snapshot = copy.deepcopy(session.to_dict())
            before = copy.deepcopy(h.history.snapshot)
            for response_id, status, text in (
                ("wrong-response", "completed", h.model_text),
                ("known-model-response", "in_progress", h.model_text),
                ("known-model-response", "completed", ""),
            ):
                with self.subTest(role=role, response_id=response_id, status=status, empty=not text):
                    h.retrieve.return_value = SimpleNamespace(id=response_id, status=status, output_text=text)
                    with self.assertRaisesRegex(ArtifactError, "SPECIALIST_MODEL_RECOVERY_INCOMPLETE"):
                        await h.run("outer-incomplete-recovery")
                    self.assertEqual(h.history.snapshot, before)
                    self.assertEqual(h.retrieve.await_args.args, ("known-model-response",))
            self.assertEqual(h.retrieve.await_count, 3)
            self.assertEqual(h.runs, [])
            self.assertEqual(h.model_calls, [])
            self.assertEqual(h.artifacts.writes, [])
            self.assertEqual(h.history.writes, [])

    async def test_architect_incomplete_or_wrong_retrieval_cannot_advance_history(self):
        await self.check_incomplete_recovery("architect")

    async def test_reviewer_incomplete_or_wrong_retrieval_cannot_advance_history(self):
        await self.check_incomplete_recovery("reviewer")

    async def check_output_reconciliation(self, role):
        h = SpecialistHarness(self, role)
        with h.patches()[0]:
            assignment = h.operation(1)
            h.history.fail_after_output = True
            with self.assertRaisesRegex(RuntimeError, "synthetic history persistence interruption"):
                await h.run("outer-before-interruption")
            interrupted = copy.deepcopy(h.history.snapshot)
            self.assertEqual(interrupted["state"]["pending_operation"]["response_id"], h.model_response)
            self.assertEqual(len(h.artifacts.writes), 1)
            h.existing = Artifact.model_validate(h.artifacts.writes[0])
            h.runs.clear()
            h.model_calls.clear()
            ref = await h.run("outer-after-interruption")
            self.assertEqual(ref, h.existing.ref())
            self.assertEqual(h.existing.input_refs, assignment.input_refs)
            self.assertEqual(h.history.snapshot["session_id"], interrupted["session_id"])
            self.assertEqual(h.history.snapshot["service_session_id"], h.model_response)
            self.assertNotIn("pending_operation", h.history.snapshot["state"])
            self.assertEqual(len(h.artifacts.writes), 1)
            self.assertEqual(h.runs, [])
            self.assertEqual(h.model_calls, [])
            h.retrieve.assert_not_awaited()
            # A different operation cannot adopt this output or clear held state.
            h.assignment = assignment.model_copy(update={"candidate_revision": 2})
            with self.assertRaisesRegex(ArtifactError, "SPECIALIST_ARTIFACT_PROVENANCE"):
                await h.run("outer-wrong-provenance")
            self.assertEqual(len(h.artifacts.writes), 1)

    async def test_architect_existing_output_reconciles_history_without_resend(self):
        await self.check_output_reconciliation("architect")

    async def test_reviewer_existing_output_reconciles_history_without_resend(self):
        await self.check_output_reconciliation("reviewer")
