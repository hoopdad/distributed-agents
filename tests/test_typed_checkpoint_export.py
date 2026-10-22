"""Bounded public typed-export qualification; no collector or private codec.

All persisted data is synthetic and owned by TemporaryDirectory. The real
pinned Responses host produces the native checkpoints; cloud business work
alone is replaced. No credential, remote store, or live request is used.
"""
from __future__ import annotations

import hashlib
import importlib.metadata
import json
import os
import tempfile
import unittest
import warnings
from contextvars import ContextVar
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import httpx2
from agent_framework import (
    AgentSession,
    FileCheckpointStorage,
    WorkflowCheckpoint,
    WorkflowInvocationKwargs,
)
from agent_framework_foundry_hosting import CheckpointStoreProvider, ResponsesHostServer
from azure.ai.agentserver.responses import FileResponseStore, ResponsesServerOptions

from demo.workflow import create_workflow, parse_turn
import test_host_diagnostics as host_fixtures


def encoding_hash(encoded):
    """Hash a fixture-owned file encoding, NOT a re-encoding of typed state."""
    return hashlib.sha256(json.dumps(
        encoded, sort_keys=True, allow_nan=False, separators=(",", ":"),
    ).encode("utf-8")).hexdigest()


def invocation_values(value):
    """Locate typed values without projecting or changing the comparison state."""
    if isinstance(value, WorkflowInvocationKwargs):
        yield value
    elif isinstance(value, dict):
        for child in value.values():
            yield from invocation_values(child)
    elif isinstance(value, (list, tuple)):
        for child in value:
            yield from invocation_values(child)


class PublicTypedExportTests(unittest.IsolatedAsyncioTestCase):
    def test_pinned_public_contract(self):
        for name, version in {
            "agent-framework-core": "1.21.0",
            "agent-framework-foundry-hosting": "1.0.0b261002",
            "azure-ai-agentserver-core": "2.2.0",
            "azure-ai-agentserver-responses": "2.3.0",
        }.items():
            with self.subTest(package=name):
                self.assertEqual(importlib.metadata.version(name), version)
        # The typed wrapper has no public recursive JSON serializer. Registering
        # a checkpoint type is an allowlist, not an exported encoding API.
        self.assertFalse(hasattr(WorkflowInvocationKwargs, "to_dict"))
        self.assertFalse(hasattr(WorkflowInvocationKwargs, "from_dict"))

    async def test_public_file_roundtrip_preserves_nonempty_typed_kwargs(self):
        kwargs = WorkflowInvocationKwargs(
            global_kwargs={"labels": ("alpha", "beta"), "bytes": b"\x00\x01"},
            executor_kwargs={"specialist": {"enabled": True, "nested": {"count": 2}}},
        )
        checkpoint = WorkflowCheckpoint(
            workflow_name="synthetic-typed-export", graph_signature_hash="synthetic-graph",
            checkpoint_id="synthetic-typed", previous_checkpoint_id="synthetic-previous",
            state={"invocation": kwargs}, metadata={"purpose": "local qualification"},
        )
        with tempfile.TemporaryDirectory() as root:
            storage = FileCheckpointStorage(root)
            self.assertEqual(await storage.save(checkpoint), checkpoint.checkpoint_id)
            loaded = await storage.load(checkpoint.checkpoint_id)
            self.assertEqual(loaded.to_dict(), checkpoint.to_dict())
            self.assertIsInstance(loaded.state["invocation"], WorkflowInvocationKwargs)
            self.assertIsInstance(loaded.state["invocation"].global_kwargs["labels"], tuple)
            self.assertEqual(loaded.state["invocation"].global_kwargs["bytes"], b"\x00\x01")
            files = list(Path(root).glob("*.json"))
            self.assertEqual(len(files), 1)
            encoded = json.loads(files[0].read_text(encoding="utf-8"))
            before_hash = encoding_hash(encoded)
            # Use the public loader on the SDK's own file, not a private decoder.
            self.assertEqual((await storage.load(checkpoint.checkpoint_id)).to_dict(), loaded.to_dict())
            self.assertEqual(encoding_hash(json.loads(files[0].read_text(encoding="utf-8"))), before_hash)
            # JSON-encoded persistence is not the raw comparison-state contract.
            encoded_as_checkpoint = WorkflowCheckpoint.from_dict(encoded)
            self.assertNotEqual(encoded_as_checkpoint.state, loaded.state)
            with self.assertRaisesRegex(TypeError, "WorkflowInvocationKwargs"):
                json.dumps(loaded.to_dict(), allow_nan=False)
        self.assertFalse(Path(root).exists())

    def test_session_public_serialization_does_not_supply_checkpoint_codec(self):
        kwargs = WorkflowInvocationKwargs(global_kwargs={"keep": ("typed",)})
        session = AgentSession(session_id="synthetic-session")
        session.state["checkpoint"] = WorkflowCheckpoint(
            workflow_name="synthetic", graph_signature_hash="synthetic-graph",
            state={"invocation": kwargs},
        )
        with warnings.catch_warnings(record=True) as emitted:
            warnings.simplefilter("always", RuntimeWarning)
            value = session.to_dict()
        self.assertTrue(any("WorkflowInvocationKwargs" in str(item.message) for item in emitted))
        self.assertIs(value["state"]["checkpoint"]["state"]["invocation"], kwargs)
        with self.assertRaisesRegex(TypeError, "WorkflowInvocationKwargs"):
            json.dumps(value, allow_nan=False)
        # No global register_state_type callback: that would be a new codec,
        # not qualification of the pinned existing public checkpoint export.

    async def test_actual_host_typed_file_roundtrip_and_exact_origin_hash_interval(self):
        import asyncio
        from demo import diagnostics

        harness = host_fixtures.PinnedHostTests()
        previous_emit = diagnostics.emit
        previous_backend = os.environ.get("AGENTSERVER_TASKS_BACKEND")
        self.addCleanup(lambda: self.assertIs(diagnostics.emit, previous_emit))
        self.addCleanup(lambda: self.assertEqual(
            os.environ.get("AGENTSERVER_TASKS_BACKEND"), previous_backend,
        ))
        self.addCleanup(lambda: self.assertFalse(Path(harness.root).exists()))
        self.addCleanup(lambda: harness.stack.close())
        self.addAsyncCleanup(harness.asyncTearDown)
        await harness.asyncSetUp()
        binding = ContextVar("synthetic_typed_export_binding", default=None)
        captures = []

        class Provider(CheckpointStoreProvider):
            def get_store_for_scope(self, *, scope, context_id, platform_context):
                store = super().get_store_for_scope(
                    scope=scope, context_id=context_id, platform_context=platform_context,
                )
                captures.append((binding.get(), scope, context_id, store))
                return store

        class Boundary:
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
            checkpoint_store_provider=Provider(),
            options=ResponsesServerOptions(resilient_background=True),
            response_store=FileResponseStore(), configure_observability=None,
        )
        server.add_middleware(Boundary)
        async with server.router.lifespan_context(server):
            async with httpx2.AsyncClient(
                transport=httpx2.ASGITransport(app=server), base_url="http://synthetic",
            ) as client:
                responses = await asyncio.gather(*(
                    client.post("/responses", json={
                        "input": "synthetic typed-export turn", "background": True, "store": True,
                    }, headers={
                        "x-agent-user-id": f"synthetic-user-{index}",
                        "x-agent-foundry-call-id": f"synthetic-call-{index}",
                    }) for index in range(2)
                ))
                self.assertTrue(all(response.status_code == 200 for response in responses))
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

        checked = typed_count = matching_file_hashes = 0
        for (response_id, request_scope), store_scope, context_id, store in captures:
            self.assertEqual(request_scope, store_scope)
            self.assertEqual(store.context_id, context_id)
            self.assertTrue(response_id)
            checkpoints = await store.list_checkpoints(workflow_name="distributed-architect-v1")
            self.assertTrue(checkpoints)
            self.assertTrue(any(list(invocation_values(item.to_dict())) for item in checkpoints))
            with tempfile.TemporaryDirectory() as export_root:
                storage = FileCheckpointStorage(export_root)
                for checkpoint in checkpoints:
                    origin, origin_hash = await store.load_with_hash(checkpoint.checkpoint_id)
                    self.assertEqual(origin.to_dict(), checkpoint.to_dict())
                    self.assertRegex(origin_hash, r"^[0-9a-f]{64}$")
                    Provider().validate_checkpoint_value(origin.to_dict())
                    await storage.save(origin)
                    restored = await storage.load(origin.checkpoint_id)
                    # Full comparison: no omitted fields, normalization or projection.
                    self.assertEqual(restored.to_dict(), origin.to_dict())
                    self.assertEqual(
                        list(invocation_values(restored.to_dict())),
                        list(invocation_values(origin.to_dict())),
                    )
                    again, again_hash = await store.load_with_hash(origin.checkpoint_id)
                    self.assertEqual(again.to_dict(), origin.to_dict())
                    self.assertEqual(again_hash, origin_hash)
                    # A checkpoint can also contain typed WorkflowMessage.
                    # Test the entire record, then the exact unresolved wrapper
                    # independently; do not rely on JSON's first failing field.
                    with self.assertRaises(TypeError):
                        json.dumps(restored.to_dict(), allow_nan=False)
                    for invocation in invocation_values(restored.to_dict()):
                        typed_count += 1
                        with self.assertRaisesRegex(TypeError, "WorkflowInvocationKwargs"):
                            json.dumps(invocation, allow_nan=False)
                    checked += 1
                # Files created only by this public storage in an owned empty root.
                files = list(Path(export_root).glob("*.json"))
                self.assertEqual(len(files), len(checkpoints))
                for path in files:
                    encoded = json.loads(path.read_text(encoding="utf-8"))
                    checkpoint = await storage.load(encoded["checkpoint_id"])
                    self.assertNotEqual(
                        WorkflowCheckpoint.from_dict(encoded).state, checkpoint.state,
                    )
                    # Retain the exact file hash independently. It is not promoted
                    # to the Foundry original encoding hash after re-serialization.
                    file_hash = encoding_hash(encoded)
                    self.assertRegex(file_hash, r"^[0-9a-f]{64}$")
                    _, original_hash = await store.load_with_hash(checkpoint.checkpoint_id)
                    matching_file_hashes += file_hash == original_hash
            self.assertFalse(Path(export_root).exists())
        self.assertGreater(checked, 0)
        self.assertGreater(typed_count, 0)
        print(
            f"Typed export qualification: {len(captures)} scoped responses, "
            f"{checked} complete checkpoint roundtrips, {typed_count} invocation wrappers; "
            f"{matching_file_hashes}/{checked} re-encoded file hashes match original. "
            "Hash equality is observed, not a canonical encoding contract."
        )


if __name__ == "__main__":
    unittest.main()
