"""Offline qualification, not a live collector or evidence-origin attestation.

Use public SDK stores with their documented temporary local backend, existing
application service injection and the retained aggregate validator. No SDK
internals are patched and no real credential or network is used.
"""
from __future__ import annotations

import copy
import importlib.metadata
import json
import os
import tempfile
import unittest
from unittest.mock import patch

from agent_framework import AgentSession, WorkflowCheckpoint, WorkflowCheckpointException
from agent_framework_foundry_hosting import AgentSessionStoreProvider, CheckpointStoreProvider
from azure.ai.agentserver.core import AgentConfig, FoundryAgentRequestContext
from azure.ai.agentserver.core.storage import FoundryStateStore

from demo.artifacts import ArtifactError, Effect, ScopeBinding, decode_document
from live_acceptance import validate_scenario_evidence
import test_scenario_evidence as retained
from test_workflow import MemoryBackend, make_store


def config(parent="synthetic-parent"):
    return AgentConfig(
        agent_name="synthetic-coordinator", agent_version="2", agent_id="synthetic-coordinator:2",
        is_hosted=True, project_endpoint="https://example.services.ai.azure.com/api/projects/example",
        project_id="synthetic-project", session_id=parent, port=8088,
        appinsights_connection_string="", otlp_endpoint="", sse_keepalive_interval=0,
    )


def context(parent="synthetic-parent", *, user="synthetic-user", call="synthetic-call"):
    return FoundryAgentRequestContext(session_id=parent, user_id=user, call_id=call)


def scope(parent="synthetic-parent"):
    return ScopeBinding(
        project="https://example.services.ai.azure.com/api/projects/example",
        tenant="11111111-1111-1111-1111-111111111111",
        principal="synthetic-user", parent_session=parent,
    )


def frozen(value):
    """Fixture-owned JSON boundary, not a proposed runtime encoder."""
    return json.loads(json.dumps(value, allow_nan=False))


class PublicStoreSeamsTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        root = self.enterContext(tempfile.TemporaryDirectory())
        # The SDK documents this operator knob. Never touch ~/.agentserver or
        # instantiate its hosted DefaultAzureCredential/network branch.
        self.enterContext(patch.dict(os.environ, {
            "AGENTSERVER_STATE_ROOT": root, "FOUNDRY_HOSTING_ENVIRONMENT": "",
            "OTEL_SDK_DISABLED": "true",
        }))
        self.provider = CheckpointStoreProvider()
        self.store = self.provider.get_store(
            config=config(), context_id="synthetic-lineage", platform_context=context(),
        )

    def test_matching_installed_pins(self):
        for name, version in {
            "agent-framework-core": "1.21.0",
            "agent-framework-foundry-hosting": "1.0.0b261002",
            "azure-ai-agentserver-core": "2.2.0",
            "azure-ai-agentserver-responses": "2.3.0",
            "azure-ai-projects": "2.7.0",
            "azure-storage-blob": "12.31.0",
        }.items():
            with self.subTest(package=name):
                self.assertEqual(importlib.metadata.version(name), version)

    async def test_public_checkpoint_roundtrip_hash_and_cumulative_retention(self):
        checkpoint = WorkflowCheckpoint(
            workflow_name="distributed-agents-v1", graph_signature_hash="synthetic-graph",
            checkpoint_id="first", state={"payload": {"items": [1]}}, iteration_count=1,
        )
        self.provider.validate_checkpoint_value(checkpoint.to_dict())
        await self.store.save(checkpoint)
        first, first_hash = await self.store.load_with_hash("first")
        snapshot = frozen(first.to_dict())
        checkpoint.state["payload"]["items"].append(2)
        first.state["payload"]["items"].append(3)
        await self.store.save(WorkflowCheckpoint(
            workflow_name="distributed-agents-v1", graph_signature_hash="synthetic-graph",
            checkpoint_id="second", previous_checkpoint_id="first", iteration_count=1,
        ))
        unchanged, unchanged_hash = await self.store.load_with_hash("first")
        self.assertEqual(frozen(unchanged.to_dict()), snapshot)
        self.assertEqual(first_hash, unchanged_hash)
        records = await self.store.list_checkpoints(workflow_name="distributed-agents-v1")
        self.assertEqual({item.checkpoint_id for item in records}, {"first", "second"})
        self.assertEqual(await self.store.list_checkpoints(workflow_name="other"), [])
        # Equal iteration counts are legal; neither iteration nor workflow name
        # provides the outer response/lineage provenance.
        self.assertEqual({item.iteration_count for item in records}, {1})

    async def test_public_checkpoint_store_is_not_an_immutable_archive(self):
        checkpoint = WorkflowCheckpoint(
            workflow_name="distributed-agents-v1", graph_signature_hash="synthetic-graph",
            checkpoint_id="reused", state={"value": 1},
        )
        await self.store.save(checkpoint)
        _, before = await self.store.load_with_hash("reused")
        checkpoint.state["value"] = 2
        await self.store.save(checkpoint)
        after, after_hash = await self.store.load_with_hash("reused")
        self.assertEqual(after.state, {"value": 2})
        self.assertNotEqual(before, after_hash)
        # Qualified negative finding: the collector must retain frozen receipts
        # and reject changed/duplicate IDs, not assume save() enforces it.

    async def test_checkpoint_scope_rejection_and_collection_partition(self):
        for ctx in (context(user=None), context(call=None), context(parent="wrong-parent")):
            with self.subTest(case=(ctx.user_id, ctx.call_id, ctx.session_id)):
                with self.assertRaises(RuntimeError):
                    self.provider.get_store(
                        config=config(), context_id="synthetic-lineage", platform_context=ctx,
                    )
        await self.store.save(WorkflowCheckpoint(
            workflow_name="distributed-agents-v1", graph_signature_hash="graph", checkpoint_id="one",
        ))
        for parent, user, lineage in (
            ("other-parent", "synthetic-user", "synthetic-lineage"),
            ("synthetic-parent", "other-user", "synthetic-lineage"),
            ("synthetic-parent", "synthetic-user", "other-lineage"),
        ):
            other = self.provider.get_store(
                config=config(parent), context_id=lineage, platform_context=context(parent, user=user),
            )
            self.assertEqual(await other.list_checkpoints(workflow_name="distributed-agents-v1"), [])
            with self.assertRaises(WorkflowCheckpointException):
                await other.load("one")
        same_scope = self.provider.get_store(
            config=config(), context_id="synthetic-lineage",
            platform_context=context(call="next-call"),
        )
        self.assertEqual((await same_scope.load("one")).checkpoint_id, "one")

    def test_checkpoint_to_dict_requires_explicit_frozen_capture(self):
        checkpoint = WorkflowCheckpoint(workflow_name="w", graph_signature_hash="g", state={"x": []})
        shallow, receipt = checkpoint.to_dict(), frozen(checkpoint.to_dict())
        checkpoint.state["x"].append(1)
        self.assertEqual(shallow["state"]["x"], [1])
        self.assertEqual(receipt["state"]["x"], [])

    async def test_public_lower_store_pagination_and_missing_item(self):
        # Explicit caller-known name, not reverse-engineering a private SDK name.
        async with await FoundryStateStore.get_or_create("synthetic-qualified-list") as store:
            for key in ("a", "b", "c"):
                await store.create_item(key, {"key": key})
            self.assertIsNone(await store.get_item("missing"))
            seen, after = [], None
            while True:
                page = await store.list_keys(limit=1, after=after, order="asc")
                seen.extend(item.key for item in page.keys)
                if not page.has_more:
                    break
                self.assertIsNotNone(page.last_id)
                self.assertNotEqual(page.last_id, after)
                after = page.last_id
            self.assertEqual(seen, ["a", "b", "c"])
        # Local pagination qualifies serialization, not remote consistency,
        # retention, user isolation or a hosted snapshot transaction.

    async def test_public_session_snapshot_preserves_state_not_model_execution(self):
        provider = AgentSessionStoreProvider(store_name="specialist_history_v2")
        store = provider.get_store(config=config(), platform_context=context())
        self.assertIsNone(await store.get("history"))
        session = AgentSession(session_id="framework-child", service_session_id="prior-model-response")
        session.state["pending_operation"] = {
            "id": "a" * 32, "input_sha256": "b" * 64,
            "model_deployment": "synthetic-model", "response_id": None,
        }
        await store.set("history", session)
        receipt = frozen((await store.get("history")).to_dict())
        session.service_session_id = "next-model-response"
        await store.set("history", session)
        self.assertEqual(receipt["service_session_id"], "prior-model-response")
        self.assertEqual((await store.get("history")).service_session_id, "next-model-response")
        other = provider.get_store(config=config("other"), platform_context=context("other"))
        self.assertIsNone(await other.get("history"))
        # Arbitrary synthetic IDs round-trip; persistence alone cannot attest
        # which previous response/history the actual model request consumed.


class BlobAttachmentSeamsTests(unittest.IsolatedAsyncioTestCase):
    async def test_public_operation_write_retention_and_collision_rejection(self):
        backend, binding = MemoryBackend(), scope()
        store = make_store(backend, binding, "coordinator")
        operation = "a" * 32
        effect = Effect(operation_id=operation, kind="create", status="prepared",
                        role="architect", input_refs=[])
        prepared = {"scope_binding": binding.model_dump(mode="json"),
                    "effect": effect.model_dump(mode="json")}
        await store.write_operation(operation, "prepared", prepared)
        retained_bytes = dict(backend.blobs)
        effect.status = "dispatched"
        dispatched = {"scope_binding": binding.model_dump(mode="json"),
                      "effect": effect.model_dump(mode="json")}
        await store.write_operation(operation, "dispatched", dispatched)
        self.assertTrue(all(backend.blobs[key] == value for key, value in retained_bytes.items()))
        await store.write_operation(operation, "prepared", prepared)  # identical idempotent bytes
        with self.assertRaisesRegex(ArtifactError, "ARTIFACT_IMMUTABLE_COLLISION"):
            await store.write_operation(operation, "prepared", dispatched)
        with self.assertRaisesRegex(ArtifactError, "OPERATION_WRITER"):
            await make_store(backend, binding, "architect").write_operation(operation, "prepared", prepared)
        self.assertEqual(len(backend.blobs), 2)

    async def test_public_manifest_read_rejects_cross_scope_and_missing(self):
        backend, binding = MemoryBackend(), scope()
        store = make_store(backend, binding, "coordinator")
        async with store.lock_manifest() as document:
            await document.save(document.value)
        manifest = await store.read_manifest()
        self.assertEqual(manifest.scope_binding, binding)
        key = ("control", binding.prefix + "manifest.json")
        wrong = manifest.model_copy(update={"scope_binding": scope("other")})
        backend.blobs[key] = wrong.model_dump_json().encode()
        with self.assertRaisesRegex(ArtifactError, "MANIFEST_SCOPE"):
            await store.read_manifest()
        del backend.blobs[key]
        from azure.core.exceptions import ResourceNotFoundError
        with self.assertRaises(ResourceNotFoundError):
            await store.read_manifest()

    def test_public_document_decoder_rejects_duplicate_keys(self):
        with self.assertRaises(ArtifactError):
            decode_document(b'{"effect": {}, "effect": {}}')


class AggregateAttachmentSeamsTests(unittest.IsolatedAsyncioTestCase):
    """Join actual public serialized checkpoints to existing synthetic evidence.

    Inherit no fixture implementation from the aggregate validator. Reuse its
    existing offline graph captures; never reconstruct independent live sends
    from operation intentions.
    """

    asyncSetUp = PublicStoreSeamsTests.asyncSetUp

    async def test_public_checkpoint_exports_attach_without_weakening_validator(self):
        harness = retained.ScenarioEvidenceTests()
        before_clocks = retained.clock_bindings()
        self.addCleanup(lambda: self.assertEqual(retained.clock_bindings(), before_clocks))
        # The helper TestCase is not run by a second unittest runner. Register
        # its resource owner directly on this running case; doCleanups() on an
        # unstarted IsolatedAsyncioTestCase can swallow missing-runner failures.
        self.addCleanup(lambda: harness.fixture_resources.close())
        await harness.asyncSetUp()
        data = copy.deepcopy(harness.data)
        # This context ID is explicitly fixture-owned. There is no claim that a
        # real host's opaque lineage ID was discovered from a response.
        for scenario in ("followup", "restart"):
            for record in data[scenario]["checkpoints"]["records"]:
                await self.store.save(WorkflowCheckpoint.from_dict(record))
            data[scenario]["checkpoints"]["records"] = frozen([
                item.to_dict() for item in await self.store.list_checkpoints(
                    workflow_name="distributed-agents-v1",
                )
            ])
        validate_scenario_evidence(**data)
        mutations = (
            ("EVIDENCE_CHECKPOINT_RECONCILIATION",
             lambda d: d["followup"]["checkpoints"].update(records=[])),
            ("EVIDENCE_CHECKPOINT",
             lambda d: d["restart"]["checkpoints"]["records"].append(
                 copy.deepcopy(d["restart"]["checkpoints"]["records"][0]))),
            ("EVIDENCE_CHECKPOINT_SCOPE",
             lambda d: d["restart"]["checkpoints"].update(
                 scope_binding=scope("wrong-parent").model_dump(mode="json"))),
            ("EVIDENCE_REQUEST_ACCOUNTING",
             lambda d: d["initial"]["sends"].append(d["initial"]["sends"][0])),
            ("EVIDENCE_REQUEST_ACCOUNTING",
             lambda d: d["initial"]["creations"].clear()),
            ("EVIDENCE_OPERATION_SCOPE",
             lambda d: d["initial"]["operations"][0].update(
                 scope_binding=scope("wrong-parent").model_dump(mode="json"))),
        )
        for error, mutate in mutations:
            with self.subTest(rejection=error):
                invalid = copy.deepcopy(data)
                mutate(invalid)
                with self.assertRaisesRegex(RuntimeError, error):
                    validate_scenario_evidence(**invalid)


class ProjectBoundarySeamsTests(unittest.IsolatedAsyncioTestCase):
    async def test_create_boundary_exposes_target_not_journal_operation(self):
        import httpx2
        from azure.ai.projects.models import VersionRefIndicator
        from demo.foundry import ProjectClient
        from test_sdk_diagnostics import Credential, Transport

        transport = Transport(status=201, payload={
            "agent_session_id": "synthetic-child",
            "version_indicator": {"agent_version": "2"},
            "status": "active",
        })
        async with httpx2.AsyncClient(transport=httpx2.MockTransport(
            lambda request: httpx2.Response(500)
        )) as http:
            async with ProjectClient(Credential(), http, {}, transport=transport) as project:
                result = await project.agents.create_session(
                    "synthetic-agent", agent_session_id="synthetic-child",
                    version_indicator=VersionRefIndicator(agent_version="2"),
                )
        self.assertEqual(result.agent_session_id, "synthetic-child")
        self.assertEqual(len(transport.requests), 1)
        body = json.loads(transport.requests[0].body)
        self.assertEqual(body["agent_session_id"], "synthetic-child")
        self.assertEqual(body["version_indicator"]["agent_version"], "2")
        self.assertNotIn("operation_id", body)
        # A future adapter must bind trusted operation/role/target to this actual
        # boundary, keep duplicates, and define its complete observation window.
        # Counting journal intentions or inferring from timing cannot fill it.


class PinnedHostCollectionSeamsTests(unittest.IsolatedAsyncioTestCase):
    async def test_public_options_and_provider_bind_real_local_background_checkpoints(self):
        import asyncio
        from contextvars import ContextVar
        from types import SimpleNamespace
        import httpx2
        from agent_framework_foundry_hosting import ResponsesHostServer
        from azure.ai.agentserver.responses import ResponsesServerOptions, FileResponseStore
        from demo.workflow import create_workflow, parse_turn
        from demo import diagnostics
        import test_host_diagnostics as host_fixtures

        harness = host_fixtures.PinnedHostTests()
        previous_emit = diagnostics.emit
        previous_backend = os.environ.get("AGENTSERVER_TASKS_BACKEND")
        self.addCleanup(lambda: self.assertIs(diagnostics.emit, previous_emit))
        self.addCleanup(lambda: self.assertEqual(
            os.environ.get("AGENTSERVER_TASKS_BACKEND"), previous_backend,
        ))
        self.addCleanup(lambda: harness.stack.close())
        self.addAsyncCleanup(harness.asyncTearDown)
        await harness.asyncSetUp()
        binding = ContextVar("synthetic_collection_binding", default=None)
        captures = []

        class RecordingProvider(CheckpointStoreProvider):
            def get_store_for_scope(self, *, scope, context_id, platform_context):
                store = super().get_store_for_scope(
                    scope=scope, context_id=context_id, platform_context=platform_context,
                )
                captures.append((binding.get(), scope, context_id, store))
                return store

        class RequestBoundary:
            def __init__(self, app):
                self.app = app

            async def __call__(self, scope, receive, send):
                token = binding.set(None)
                try:
                    await self.app(scope, receive, send)
                finally:
                    binding.reset(token)

        def options(request, values):
            binding.set((request.response_id, request.scope))
            return values

        def factory(request):
            harness.owned_response_ids.append(request.response_id)

            async def specialize(text):
                return "synthetic result"

            runtime = SimpleNamespace(role="architect", request=request, specialize=specialize)
            with patch("demo.workflow.WorkflowRuntime", return_value=runtime):
                return create_workflow(request)

        server = ResponsesHostServer(
            workflow=factory, parse_response=parse_turn, prepare_options=options,
            checkpoint_store_provider=RecordingProvider(),
            options=ResponsesServerOptions(resilient_background=True),
            response_store=FileResponseStore(), configure_observability=None,
        )
        server.add_middleware(RequestBoundary)
        async with server.router.lifespan_context(server):
            async with httpx2.AsyncClient(
                transport=httpx2.ASGITransport(app=server), base_url="http://synthetic",
            ) as client:
                responses = await asyncio.gather(*(
                    client.post("/responses", json={
                        "input": "synthetic turn", "background": True, "store": True,
                    }, headers={
                        "x-agent-user-id": f"synthetic-user-{index}",
                        "x-agent-foundry-call-id": f"synthetic-call-{index}",
                    }) for index in range(2)
                ))
                self.assertTrue(all(item.status_code == 200 for item in responses))
                for index, response in enumerate(responses):
                    terminal = await harness.terminal_snapshot(client, response.json()["id"], {
                        "x-agent-user-id": f"synthetic-user-{index}",
                        "x-agent-foundry-call-id": f"synthetic-call-{index}",
                    })
                    self.assertEqual(terminal.json()["status"], "completed")
        self.assertIsNone(binding.get())
        self.assertEqual(len(captures), 2)
        self.assertEqual({item[0][0] for item in captures}, {item.json()["id"] for item in responses})
        self.assertEqual(len({item[2] for item in captures}), 2)
        for (response_id, request_scope), store_scope, context_id, store in captures:
            self.assertEqual(request_scope, store_scope)
            checkpoints = await store.list_checkpoints(workflow_name="distributed-architect-v1")
            self.assertTrue(checkpoints)
            for checkpoint in checkpoints:
                loaded, persisted_hash = await store.load_with_hash(checkpoint.checkpoint_id)
                self.assertEqual(loaded.checkpoint_id, checkpoint.checkpoint_id)
                self.assertTrue(persisted_hash)
            # Actual native checkpoints contain typed WorkflowInvocationKwargs.
            # to_dict() is deliberately shallow. Do not hide this uncovered
            # aggregate-JSON boundary behind default=str or a private encoder.
            with self.assertRaises(TypeError):
                frozen([item.to_dict() for item in checkpoints])
        # Qualified only for the local pinned public hooks and this process.
        # An offline caller cannot derive the real context_id from a parent or
        # graph name; cold recovery still needs an observed trusted association.
