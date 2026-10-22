"""Exact factory/closure join; all endpoints, credentials and storage are synthetic."""
from __future__ import annotations

from contextlib import AsyncExitStack, asynccontextmanager
from dataclasses import replace
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import AsyncMock, patch

# As with the retained test_demo bootstrap, never inherit operator endpoint
# settings into these synthetic client fixtures, even in standalone discovery.
os.environ.update({
    "FOUNDRY_PROJECT_ENDPOINT": "https://example.services.ai.azure.com/api/projects/example-project",
    "SPECIALIST_MODEL_DEPLOYMENT": "example-specialist",
    "DECISION_MODEL_DEPLOYMENT": "decision-1",
})

from demo import diagnostics as d
from demo import effect_observation as effects
from demo.private_effect_capture import OperationAnchor, PrivateEffectCapture, StopAnchor
from demo.architect_agent import ArchitectAgent
from demo.reviewer_agent import ReviewerAgent
from demo.artifacts import ArtifactError, canonical_bytes
from demo.contracts import AGENTS, PROJECT
from demo.foundry import OriginTransport, ProjectClient, RemoteAgents
from demo.workflow import WorkflowRuntime, create_artifact_store, operation_id
from test_effect_observation import ProjectWire, RawBytes, credential
from test_identity_handoff import parent
from test_scenario_state_reader import CONTAINERS, Transport as ReaderWire
from test_sdk_diagnostics import Credential, Transport
from test_workflow import FakeRemote, FakeRouter, MemoryBackend, TestRuntime, make_store, synthetic_calibration
from scenario_state_reader import read_scoped_state

import httpx2
from azure.storage.blob.aio import BlobServiceClient


ROOT = Path(__file__).resolve().parents[1]
STORAGE = {
    "ARTIFACT_STORAGE_ENDPOINT": "https://examplestorage.blob.core.windows.net",
    "ARTIFACT_CONTROL_CONTAINER": "control",
    "ARTIFACT_CANDIDATES_CONTAINER": "candidates",
    "ARTIFACT_REVIEWS_CONTAINER": "reviews",
    "ARTIFACT_PRIVATE_IPS": "10.0.0.1",
}


class FactoryJoinTests(unittest.IsolatedAsyncioTestCase):
    async def test_specialist_injected_blob_factories_emit_real_pipeline_events(self):
        for role, agent in (("architect", ArchitectAgent), ("reviewer", ReviewerAgent)):
            for failure in (None, ArtifactError("ASSIGNMENT_RECEIVER")):
                with self.subTest(role=role, rejection=failure is not None):
                    events, captured, closed = [], {}, []
                    inner = Transport()
                    scope, config, context = parent()
                    terminal = failure or RuntimeError("synthetic-stop-after-storage-observation")

                    @asynccontextmanager
                    async def credential_factory(**kwargs):
                        self.assertEqual(set(kwargs), {"raw_request_hook", "raw_response_hook"})
                        self.assertTrue(all(callable(hook) for hook in kwargs.values()))
                        # Neither supplied transport nor guessed timeout may bypass Identity defaults.
                        self.assertNotIn("transport", kwargs)
                        try:
                            yield Credential()
                        finally:
                            closed.append("credential")

                    def artifact_factory(**kwargs):
                        captured.update(kwargs)

                        async def verify_private_path():
                            # Exercise the real pinned Blob client injected by this exact factory.
                            blob = kwargs["service"].get_blob_client("control", "private-blob-sentinel")
                            await blob.get_blob_properties()

                        return SimpleNamespace(
                            verify_private_path=verify_private_path,
                            read_assignment=AsyncMock(side_effect=terminal),
                        )

                    module = f"demo.{role}_agent"
                    locator = canonical_bytes({
                        "schema_version": 1, "scope_binding": scope.model_dump(mode="json"),
                        "operation_id": "a" * 32,
                    }).decode()
                    with patch.dict(os.environ, STORAGE), \
                            patch(f"{module}.ManagedIdentityCredential", credential_factory), \
                            patch("demo.artifact_store.AioHttpTransport", return_value=inner) as transport, \
                            patch(f"{module}.BlobArtifacts", side_effect=artifact_factory), \
                            patch.object(d, "emit", side_effect=lambda e: events.append(d.event_fields(e))):
                        async with AsyncExitStack() as stack:
                            with self.assertRaises(type(terminal)) as caught:
                                await agent.connect_and_load_assignment(
                                    stack, locator, config=config, context=context,
                                    scope=scope, response_id="synthetic-response",
                                )
                            self.assertIs(caught.exception, terminal)
                    transport.assert_called_once_with(use_env_settings=False)
                    self.assertEqual(closed, ["credential"])
                    self.assertIn("close", inner.lifecycle)
                    self.assertEqual(captured["role"], role)
                    self.assertEqual([e["kind"] for e in events], ["send", "response_headers"])
                    self.assertTrue(all(e["role"] == role and e["stage"] == "storage" for e in events))
                    self.assertEqual(len(inner.requests), 1)
                    self.assertNotIn("private-blob-sentinel", json.dumps(events))

    async def test_workflow_owned_credential_hooks_and_default_blob_factory(self):
        events = []
        scope, config, context = parent()
        runtime = WorkflowRuntime.__new__(WorkflowRuntime)
        runtime.role, runtime.scope, runtime.config, runtime.context = "coordinator", scope, config, context
        runtime.response_id = "synthetic-response"
        inner = Transport()
        closed = []

        @asynccontextmanager
        async def credential_factory(**kwargs):
            self.assertEqual(set(kwargs), {"raw_request_hook", "raw_response_hook"})
            self.assertTrue(all(callable(hook) for hook in kwargs.values()))
            try:
                yield Credential()
            finally:
                closed.append("credential")

        def artifact_factory(*args):
            store = create_artifact_store(*args)
            store.verify_private_path = AsyncMock()
            return store

        with patch.dict(os.environ, {**STORAGE, "EXPECTED_AZURE_TENANT_ID": scope.tenant}), \
                patch("demo.workflow.ManagedIdentityCredential", credential_factory), \
                patch("demo.workflow.create_artifact_store", side_effect=artifact_factory), \
                patch("demo.artifact_store.AioHttpTransport", return_value=inner), \
                patch.object(d, "emit", side_effect=lambda e: events.append(d.event_fields(e))):
            async with runtime.resources() as (store, *_):
                await store.service.get_blob_client("control", "private-blob-sentinel").get_blob_properties()
        self.assertEqual(closed, ["credential"])
        self.assertIn("close", inner.lifecycle)
        storage_events = [e for e in events if e["stage"] == "storage"]
        self.assertEqual([e["kind"] for e in storage_events], ["send", "response_headers"])
        self.assertTrue(all(e["role"] == "coordinator" for e in storage_events))


class PackageClosureTests(unittest.TestCase):
    def test_existing_application_allowlists_include_shared_module(self):
        for name in (".agentignore", ".dockerignore"):
            self.assertIn("!demo/*.py", (ROOT / name).read_text().splitlines())
        self.assertIn("COPY demo demo", (ROOT / "Dockerfile").read_text().splitlines())
        self.assertTrue((ROOT / "demo/diagnostics.py").is_file())
        self.assertTrue((ROOT / "demo/effect_observation.py").is_file())
        self.assertTrue((ROOT / "demo/private_effect_capture.py").is_file())

    def test_actual_selected_lab_runtime_closure_includes_all_application_modules(self):
        tools = os.environ.get("AZURE_LAB_SOURCE_ROOT")
        if not tools:
            self.skipTest("Explicit linked lab root required; Test-Demo supplies it.")
        tools = Path(tools).resolve()
        # Read only the named public path contract, not profiles/settings/package evidence.
        name = "_profiling_release_roots_fixture"
        spec = importlib.util.spec_from_file_location(name, tools / "release_roots.py")
        module = importlib.util.module_from_spec(spec)
        with patch.dict(sys.modules, {name: module}):
            spec.loader.exec_module(module)
            roots = module.ReleaseRoots.select(ROOT, tools.parents[1])
            closure = roots.runtime_files()
            expected = {"demo/" + path.name for path in (ROOT / "demo").glob("*.py")}
            self.assertTrue(expected <= closure)
            self.assertIn("demo/diagnostics.py", closure)
            self.assertIn("demo/effect_observation.py", closure)
            self.assertIn("demo/private_effect_capture.py", closure)
            self.assertNotIn("scenario_state_reader.py", closure)
            self.assertNotIn("live_acceptance.py", closure)
            self.assertFalse(any(path.startswith("tests/") for path in closure))
            self.assertIn("config/routing-corpus.json", closure)
            self.assertIn("config/routing-calibration.json", closure)
            for path in closure:
                self.assertTrue(roots.source(path).is_relative_to(ROOT))


class ObservationJoinTests(unittest.IsolatedAsyncioTestCase):
    async def test_trusted_workflow_dispatch_public_wires_and_injected_reader_join(self):
        """Real execute/create/send paths; an HTTP 200 still leaves a held turn."""
        for sink_mode in ("retained", "broken", "absent", "durable"):
            with self.subTest(sink=sink_mode):
                receipts, seen, backend = [], [], MemoryBackend()
                wire = ProjectWire()
                durable = None

                def handle(request):
                    seen.append(request)
                    # No specialist artifact/output: the SDK-completed envelope
                    # must not manufacture successful collaboration.
                    response = {
                        "id": "resp_join", "object": "response", "created_at": 1,
                        "model": "", "status": "completed", "output": [],
                    }
                    return httpx2.Response(200, headers={"content-type": "text/event-stream"},
                                           stream=RawBytes(
                                               ("data: " + json.dumps({
                                                   "type": "response.completed", "response": response,
                                               }) + "\n\n").encode()))

                def sink(receipt):
                    receipts.append(receipt)
                    if durable is not None:
                        durable(receipt)
                    if sink_mode == "broken":
                        raise OSError("synthetic-private-sink-error")

                async with httpx2.AsyncClient(
                    transport=OriginTransport(httpx2.MockTransport(handle)),
                ) as http:
                    async with ProjectClient(credential(), http, {}, transport=wire) as project:
                        remote = RemoteAgents(project, {})
                        # Only version preparation/lookup are synthetic; actual
                        # public Project create and OpenAI streamed send execute.
                        remote.prepare = FakeRemote(backend).prepare
                        project.agents.get_session = AsyncMock(return_value=SimpleNamespace(
                            status="active",
                            version_indicator=SimpleNamespace(agent_version="2"),
                        ))
                        runtime = TestRuntime(backend, remote)
                        with patch.dict(os.environ, {"DECISION_REQUESTS_PER_MINUTE": "17"}), \
                                patch("demo.workflow.DecisionClient", return_value=FakeRouter()), \
                                patch("demo.workflow.load_calibration", return_value=synthetic_calibration()):
                            await runtime.begin("Synthetic join requirements.")
                            action, result = await runtime.route(runtime.response_id)
                            self.assertEqual((action, result), ("ask_architect", None))
                            if sink_mode == "durable":
                                # Expected bindings come from trusted routed source,
                                # not learned from the callback being measured.
                                selected = await remote.prepare("architect")
                                remote.prepare = AsyncMock(return_value=selected)
                                routed = await make_store(backend, runtime.scope, runtime.role).read_manifest()
                                bindings = tuple(effects.Binding(
                                    operation_id(runtime.scope, routed.routing_operation_id, suffix),
                                    "architect", selected.hosted_id, selected.version, verb,
                                ) for suffix, verb in (("create", "create"), ("call", "send")))
                                private_file = self.enterContext(tempfile.TemporaryFile("w+b"))
                                durable = PrivateEffectCapture(
                                    private_file, expected=bindings, new_exclusive=True,
                                )
                            with effects.private_sink(sink if sink_mode != "absent" else None):
                                call_op = await runtime.execute(action)
                        store = make_store(backend, runtime.scope, runtime.role)
                        head = await store.read_manifest()
                        self.assertEqual(head.status, "SPECIALIST_EMPTY")
                        self.assertEqual(head.effect.operation_id, call_op)
                        self.assertNotEqual(head.effect.status, "accepted")
                        self.assertEqual(head.effect.response_id, "resp_join")
                        self.assertEqual(len(wire.requests), 1)
                        self.assertEqual([request.method for request in seen], ["POST"])
                        # An installed observer neither authorizes a mismatched
                        # action nor suppresses the existing deterministic gate.
                        before = len(receipts)
                        with effects.private_sink(sink):
                            with self.assertRaises(ArtifactError):
                                await runtime.execute("ask_reviewer")
                        self.assertEqual(len(receipts), before)
                        self.assertEqual((len(wire.requests), len(seen)), (1, 1))

                attempts = [receipt for receipt in receipts if receipt.phase == "request"]
                if sink_mode == "absent":
                    self.assertEqual(receipts, [])
                else:
                    self.assertEqual([r.binding.action for r in attempts], ["create", "send"])
                    target = head.children["architect"]
                    self.assertTrue(all(
                        r.binding.target == target.hosted_id and r.binding.version == target.version
                        and r.binding.role == "architect" for r in attempts
                    ))
                    self.assertEqual(attempts[1].binding.operation, call_op)
                    self.assertNotEqual(attempts[0].binding.operation, call_op)
                    self.assertEqual(len({r.occurrence for r in attempts}), 2)
                    closed = [r for r in receipts if r.phase == "window_closed"]
                    self.assertEqual(len(closed), 2)
                    self.assertTrue(all(r.category == "incomplete" for r in closed)
                                    if sink_mode == "broken" else all(r.category is None for r in closed))

                # Export ONLY synthetic owned backend bytes to a real public
                # Blob SDK reader. No credential factory, writes or live store.
                reader_wire = ReaderWire()
                for (container, name), raw in backend.blobs.items():
                    reader_wire.put(container, name, raw, str(backend.etags[container, name]))
                names = sorted(name for container, name in backend.blobs
                               if container == "control" and "/operations/" in name)
                self.assertGreater(len(names), 2)
                reader_wire.pages[runtime.scope.prefix + "operations/"] = {
                    "": (names[:2], "rest"), "rest": (names[2:], ""),
                }
                options = dict(
                    containers=CONTAINERS, scope=runtime.scope, head=head,
                    head_etag=str(backend.etags["control", runtime.scope.prefix + "manifest.json"]),
                    quiescence_receipt="synthetic-owned-window", refs=head.accepted,
                    required_operations=names,
                )
                async with BlobServiceClient(
                    "https://synthetic.blob.core.windows.net", credential=None,
                    transport=reader_wire, retry_total=0,
                ) as service:
                    capture = await read_scoped_state(service=service, **options)
                    self.assertTrue(capture.complete, capture.issues)
                    self.assertEqual({r.name for r in capture.operations}, set(names))
                    self.assertEqual(capture.manifest.raw, canonical_bytes(head))
                    self.assertTrue(all(r.raw == backend.blobs[r.container, r.name]
                                        for r in capture.blobs))
                    # Complete read coverage cannot upgrade a held turn or
                    # turn journal transition counts into observed send counts.
                    self.assertEqual(head.status, "SPECIALIST_EMPTY")
                    self.assertFalse(hasattr(capture, "sends"))
                    self.assertGreater(len(capture.operations), len(attempts))
                    if durable is not None:
                        anchor = durable.checkpoint(quiescence_receipt=options["quiescence_receipt"])
                        readback = durable.readback(anchor)
                        self.assertTrue(readback.complete, readback.issues)
                        self.assertEqual(readback.receipts, tuple(receipts))
                        operation_anchors = []
                        for b in bindings:
                            # Raw journal name/digest originates in the separately
                            # read scoped window; request counts never come from it.
                            record = next(r for r in capture.operations
                                          if f"/{b.operation}/dispatched.json" in r.name)
                            operation_anchors.append(OperationAnchor(b, record.name, record.sha256))
                        join_options = dict(
                            state=capture, manifest_sha256=capture.manifest.sha256,
                            manifest_etag=capture.manifest.etag, operations=operation_anchors,
                        )
                        accounting = durable.reconcile(anchor, **join_options)
                        self.assertTrue(accounting.complete, accounting.issues)
                        self.assertEqual(accounting.creations, (bindings[0].operation,))
                        self.assertEqual(accounting.sends, (call_op,))
                        self.assertEqual(accounting.stops, ())
                        self.assertEqual(head.status, "SPECIALIST_EMPTY")  # not execution success
                        for changed in (
                            {"state": replace(capture, complete=False)},
                            {"state": replace(capture, quiescence_receipt="foreign-window")},
                            {"manifest_sha256": "0" * 64},
                            {"manifest_etag": "foreign-etag"},
                            {"operations": operation_anchors[:1]},
                            {"operations": [replace(operation_anchors[0], sha256="0" * 64),
                                            operation_anchors[1]]},
                            {"operations": [replace(operation_anchors[0], binding=replace(
                                bindings[0], target="foreign-child")), operation_anchors[1]]},
                        ):
                            failed = durable.reconcile(anchor, **(join_options | changed))
                            self.assertFalse(failed.complete)
                            self.assertEqual((failed.creations, failed.sends, failed.stops), ((), (), ()))
                            self.assertEqual(failed.capture.raw, readback.raw)
                        self.assertEqual(hashlib.sha256(readback.raw).hexdigest(), anchor.sha256)
                        # Independent stop binding/intent and actual public POST;
                        # idle alone or HTTP 200 cannot manufacture confirmation.
                        stop_binding = effects.Binding(
                            "f" * 32, "coordinator", runtime.scope.parent_session,
                            head.coordinator_version, "stop",
                        )
                        with tempfile.TemporaryFile("w+b") as stop_file:
                            stop_capture = PrivateEffectCapture(
                                stop_file, expected=[stop_binding], new_exclusive=True,
                            )
                            async with httpx2.AsyncClient(transport=OriginTransport(httpx2.MockTransport(
                                lambda request: httpx2.Response(204, stream=RawBytes(b"")),
                            ))) as stop_http:
                                with effects.private_sink(stop_capture), effects.dispatch(stop_binding):
                                    await stop_http.post(
                                        PROJECT + f"/agents/{AGENTS['coordinator']}/endpoint/sessions/"
                                        + runtime.scope.parent_session + ":stop",
                                    )
                            stop_anchor = stop_capture.checkpoint(
                                quiescence_receipt=options["quiescence_receipt"])
                            stop_options = dict(
                                state=capture, manifest_sha256=capture.manifest.sha256,
                                manifest_etag=capture.manifest.etag,
                                stops=[StopAnchor(stop_binding, "idle")],
                            )
                            stopped = stop_capture.reconcile(stop_anchor, **stop_options)
                            self.assertTrue(stopped.complete, stopped.issues)
                            self.assertEqual(stopped.stops, (runtime.scope.parent_session,))
                            unknown = stop_capture.reconcile(stop_anchor, **(stop_options | {
                                "stops": [StopAnchor(stop_binding, "unknown")],
                            }))
                            self.assertFalse(unknown.complete)
                    request_count = len(reader_wire.requests)
                    with self.assertRaisesRegex(ValueError, "READER_BINDING"):
                        await read_scoped_state(service=service, **(options | {"refs": []}))
                    self.assertEqual(len(reader_wire.requests), request_count)
                    # A changed attributed head fails closed; it cannot repair
                    # the held execution or alter the original backend.
                    reader_wire.put("control", runtime.scope.prefix + "manifest.json",
                                    canonical_bytes(head), "changed-etag")
                    moved = await read_scoped_state(service=service, **options)
                    self.assertFalse(moved.complete)
                    self.assertEqual(head, await store.read_manifest())
                    self.assertFalse(reader_wire.closed)  # injected lifecycle stays caller-owned
                self.assertTrue(reader_wire.closed)


if __name__ == "__main__":
    unittest.main()
