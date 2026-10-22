"""Offline candidate integration: real SDK clients, controlled network/storage."""
from __future__ import annotations

import asyncio
from contextlib import asynccontextmanager, contextmanager
from types import SimpleNamespace
import unittest
from unittest.mock import AsyncMock, patch

import httpx2
from agent_framework.exceptions import ChatClientException
from azure.core.credentials import AccessToken

from demo.artifacts import ArtifactError
from demo.contracts import AGENTS, DemoError
from demo.foundry import ProjectClient, specialist_identity_headers
from demo.workflow import WorkflowRuntime
from test_identity_handoff import parent


class IsolatedHeaderTests(unittest.TestCase):
    def test_runtime_revalidates_full_binding_and_identity(self):
        scope, config, context = parent()
        with patch.dict("os.environ", EXPECTED_AZURE_TENANT_ID=scope.tenant):
            headers = specialist_identity_headers(config=config, context=context, scope=scope)
            self.assertEqual(headers, {
                "x-agent-foundry-call-id": context.call_id, "x-ms-user-identity": scope.principal,
            })
            for key, value in (
                ("principal", "forged"), ("parent_session", "other"),
                ("project", scope.project + "-other"), ("tenant", "other"),
            ):
                with self.subTest(key=key), self.assertRaises((DemoError, ArtifactError)):
                    specialist_identity_headers(
                        config=config, context=context, scope=scope.model_copy(update={key: value}),
                    )
            for user in (None, "", "bad user", "bad\nuser", "é", "x" * 257, context.call_id):
                context.user_id = user
                with self.subTest(user=user), self.assertRaises((DemoError, ArtifactError, ValueError)):
                    specialist_identity_headers(
                        config=config, context=context, scope=scope.model_copy(update={"principal": user}),
                    )

    def test_runtime_rejects_changed_context_and_unexpected_headers(self):
        scope, config, context = parent()
        with patch.dict("os.environ", EXPECTED_AZURE_TENANT_ID=scope.tenant):
            for headers in (
                {}, {"x-agent-foundry-call-id": "changed"},
                {**context.platform_headers(), "x-agent-user-id": scope.principal},
                {**context.platform_headers(), "x-ms-user-identity": scope.principal},
            ):
                with self.subTest(headers=headers), patch.object(
                    type(context), "platform_headers", return_value=headers,
                ), self.assertRaises(DemoError):
                    specialist_identity_headers(config=config, context=context, scope=scope)
            context.session_id = "other-parent"
            with self.assertRaises(ArtifactError):
                specialist_identity_headers(config=config, context=context, scope=scope)
            context.session_id = scope.parent_session
            config.project_endpoint = scope.project + "-other"
            with self.assertRaises(DemoError):
                specialist_identity_headers(config=config, context=context, scope=scope)


class IsolatedResourcesTests(unittest.IsolatedAsyncioTestCase):
    @contextmanager
    def fixture(self, *, fail_store=False, fail_retrieval=False):
        scope, config, context = parent()
        runtime = WorkflowRuntime.__new__(WorkflowRuntime)
        runtime.scope, runtime.config, runtime.context = scope, config, context
        runtime.role, runtime.response_id = "coordinator", "synthetic-parent-response"
        credential = SimpleNamespace(
            get_token=AsyncMock(return_value=AccessToken("synthetic-token", 4102444800)),
        )
        events, requests, projects = [], [], []

        @asynccontextmanager
        async def owned_credential(**kwargs):
            self.assertEqual(set(kwargs), {"raw_request_hook", "raw_response_hook"})
            self.assertTrue(all(callable(hook) for hook in kwargs.values()))
            try:
                yield credential
            finally:
                events.append("credential")

        def handle(request):
            requests.append(request)
            if request.method == "POST":
                return httpx2.Response(418, json={"error": {
                    "message": "Synthetic stop.", "type": "probe", "code": "probe",
                }})
            if fail_retrieval:
                return httpx2.Response(200, json={
                    "id": "resp-synthetic-known", "object": "response", "created_at": 1,
                    "model": "synthetic", "status": "failed", "output": [],
                })
            return httpx2.Response(200, json={
                "id": "resp-synthetic-known", "object": "response", "created_at": 1,
                "model": "synthetic", "status": "completed",
                "output": [{
                    "type": "message", "id": "msg-synthetic", "role": "assistant",
                    "status": "completed", "content": [{
                        "type": "output_text", "text": "Recovered.", "annotations": [],
                    }],
                }],
            })

        http = httpx2.AsyncClient(transport=httpx2.MockTransport(handle))

        @asynccontextmanager
        async def owned_http(**kwargs):
            self.assertEqual(kwargs, {
                "expected_call_id": context.call_id, "response_id": runtime.response_id,
            })
            try:
                yield http
            finally:
                events.append("http")
                await http.aclose()

        @asynccontextmanager
        async def owned_project(*args):
            async with ProjectClient(*args) as project:
                projects.append(project)
                try:
                    yield project
                finally:
                    # Project close must not close another user's shared HTTP.
                    self.assertFalse(http.is_closed)
                    events.append("project")

        store = SimpleNamespace(verify_private_path=AsyncMock())
        if fail_store:
            store.verify_private_path.side_effect = RuntimeError("Synthetic setup failure.")

        @asynccontextmanager
        async def owned_store(*args):
            try:
                yield store
            finally:
                events.append("store")

        with patch.dict("os.environ", EXPECTED_AZURE_TENANT_ID=scope.tenant), \
                patch("demo.workflow.ManagedIdentityCredential", owned_credential), \
                patch("demo.workflow.data_client", owned_http), \
                patch("demo.workflow.ProjectClient", owned_project), \
                patch("demo.workflow.create_artifact_store", owned_store):
            yield runtime, requests, projects, events, http

    async def test_both_roles_lifecycle_uses_only_specialist_authority(self):
        with self.fixture() as (runtime, requests, projects, events, http):
            original = dict(runtime.context.platform_headers())
            async with runtime.resources() as (store, remote, project, credential, shared, headers):
                self.assertIs(shared, http)
                self.assertIsNot(remote.project, project)
                self.assertIsNot(remote.headers, headers)
                self.assertIsNot(remote.project.openai_clients, project.openai_clients)
                self.assertEqual(headers, original)
                model = project.get_openai_client()
                for role in ("architect", "reviewer"):
                    with self.subTest(role=role):
                        with patch.object(remote.project.agents, "get", new_callable=AsyncMock) as get, \
                                patch.object(remote.project.agents, "create_session", new_callable=AsyncMock) as create, \
                                patch.object(remote.project.agents, "get_session", new_callable=AsyncMock) as check:
                            get.return_value = SimpleNamespace(
                                versions=SimpleNamespace(latest=SimpleNamespace(version="7")),
                            )
                            check.return_value = SimpleNamespace(
                                status="active", version_indicator=SimpleNamespace(agent_version="7"),
                            )
                            child = await remote.prepare(role)
                            framework_id = child.framework["session_id"]
                            hosted_id = child.hosted_id
                            create.return_value = SimpleNamespace(agent_session_id=hosted_id)
                            await remote.create(child)
                            await remote._check(child)
                            await remote.recover_creation(child)
                            callback = AsyncMock()
                            with self.assertRaises(ChatClientException):
                                await remote.invoke(child, {"synthetic": True}, callback)
                            self.assertEqual(await remote.recover(child, "resp-synthetic-known"), "Recovered.")
                            self.assertEqual(child.hosted_id, hosted_id)
                            self.assertEqual(child.framework["session_id"], framework_id)
                            self.assertEqual(child.framework["service_session_id"], "resp-synthetic-known")
                            self.assertEqual(child.version, "7")
                            create.assert_awaited_once()
                            self.assertEqual(check.await_count, 4)
                            for call in [get.await_args, *create.await_args_list, *check.await_args_list]:
                                self.assertEqual(call.kwargs["headers"], remote.headers)
                            callback.assert_not_awaited()
                        wire = requests[-2:]
                        self.assertEqual([r.method for r in wire], ["POST", "GET"])
                        for request in wire:
                            self.assertIn("/agents/" + AGENTS[role] + "/", str(request.url))
                            self.assertEqual(request.headers["x-ms-user-identity"], runtime.scope.principal)
                            self.assertEqual(request.headers["x-agent-foundry-call-id"], runtime.context.call_id)
                            self.assertNotIn("x-agent-user-id", request.headers)
                        self.assertEqual(wire[-1].url.params["agent_session_id"], hosted_id)
                self.assertNotIn("x-ms-user-identity", model.default_headers)
                self.assertEqual(project.call_headers, original)
                self.assertEqual(runtime.context.platform_headers(), original)
                self.assertEqual(set(project.openai_clients), {"model"})
                self.assertEqual(set(remote.project.openai_clients), {AGENTS["architect"], AGENTS["reviewer"]})
                # SDK project closure does not close the externally owned http.
                await remote.project.close()
                await model.responses.retrieve("resp-synthetic-known")
                self.assertNotIn("x-ms-user-identity", requests[-1].headers)
                self.assertFalse(http.is_closed)
                store.verify_private_path.assert_awaited_once()
            self.assertEqual(events, ["store", "project", "project", "http", "credential"])
            self.assertTrue(http.is_closed)

    async def test_cleanup_on_setup_failure_and_cancellation(self):
        for failure in ("setup", "cancel"):
            with self.subTest(failure=failure), self.fixture(fail_store=failure == "setup") as fixture:
                runtime, _, _, events, http = fixture
                with self.assertRaises(RuntimeError if failure == "setup" else asyncio.CancelledError):
                    async with runtime.resources():
                        raise asyncio.CancelledError()
                self.assertEqual(events, ["store", "project", "project", "http", "credential"])
                self.assertTrue(http.is_closed)

    async def test_binding_failure_closes_original_resources_before_delegation(self):
        with self.fixture() as (runtime, requests, projects, events, http):
            runtime.context.user_id = "changed-after-capture"
            with self.assertRaises(DemoError):
                async with runtime.resources():
                    self.fail("Invalid binding yielded resources.")
            self.assertEqual(len(projects), 1)
            self.assertEqual(requests, [])
            self.assertEqual(events, ["project", "http", "credential"])
            self.assertTrue(http.is_closed)

    async def test_failed_recovery_both_roles_never_creates_or_sends(self):
        with self.fixture(fail_retrieval=True) as (runtime, requests, _, _, _):
            async with runtime.resources() as (_, remote, *_):
                with patch.object(remote.project.agents, "get", new_callable=AsyncMock) as get, \
                        patch.object(remote.project.agents, "create_session", new_callable=AsyncMock) as create, \
                        patch.object(remote.project.agents, "get_session", new_callable=AsyncMock) as check:
                    get.return_value = SimpleNamespace(
                        versions=SimpleNamespace(latest=SimpleNamespace(version="7")),
                    )
                    check.return_value = SimpleNamespace(
                        status="active", version_indicator=SimpleNamespace(agent_version="7"),
                    )
                    for role in ("architect", "reviewer"):
                        child = await remote.prepare(role)
                        before = dict(child.framework)
                        with self.assertRaises(DemoError) as caught:
                            await remote.recover(child, "resp-synthetic-known")
                        self.assertEqual(caught.exception.code, "SPECIALIST_INCOMPLETE")
                        self.assertEqual(child.framework, before)
                    create.assert_not_awaited()
            self.assertEqual([request.method for request in requests], ["GET", "GET"])
