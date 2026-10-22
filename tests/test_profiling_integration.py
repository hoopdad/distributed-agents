"""Exact factory/closure join; all endpoints, credentials and storage are synthetic."""
from __future__ import annotations

from contextlib import AsyncExitStack, asynccontextmanager
import importlib.util
import json
import os
from pathlib import Path
import sys
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
from demo.architect_agent import ArchitectAgent
from demo.reviewer_agent import ReviewerAgent
from demo.artifacts import ArtifactError, canonical_bytes
from demo.workflow import WorkflowRuntime, create_artifact_store
from test_identity_handoff import parent
from test_sdk_diagnostics import Credential, Transport


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
            self.assertIn("config/routing-corpus.json", closure)
            self.assertIn("config/routing-calibration.json", closure)
            for path in closure:
                self.assertTrue(roots.source(path).is_relative_to(ROOT))


if __name__ == "__main__":
    unittest.main()
