from __future__ import annotations

from contextlib import redirect_stdout
from io import StringIO
import json
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import AsyncMock, patch

import httpx2
from azure.ai.agentserver.core import FoundryAgentRequestContext
from azure.core.credentials import AccessToken
from agent_framework.exceptions import ChatClientException

from demo.artifacts import (
    Artifact, ArtifactError, Assignment, Candidate, ChildBinding, Effect,
    Manifest, Producer, Requirements, ScopeBinding, digest,
)
from demo.contracts import AGENTS, Child, DemoError
from demo.foundry import ProjectClient, RemoteAgents
from scripts import identity_handoff as handoff

PROJECT = "https://example.services.ai.azure.com/api/projects/example-project"


def parent():
    scope = ScopeBinding(
        project=PROJECT, tenant="11111111-1111-4111-8111-111111111111",
        principal="synthetic-user", parent_session="synthetic-parent",
    )
    config = SimpleNamespace(
        is_hosted=True, session_id=scope.parent_session, project_endpoint=PROJECT,
    )
    context = FoundryAgentRequestContext(
        session_id=scope.parent_session, user_id=scope.principal, call_id="synthetic-opaque-call",
    )
    return scope, config, context


class CandidateHeaderTests(unittest.TestCase):
    def test_omitted_invalid_or_call_identity_is_rejected(self):
        scope, config, context = parent()
        for user in (None, "", "bad user", "bad\nuser", "é", "x" * 257, context.call_id):
            with self.subTest(user=user):
                context.user_id = user
                binding = scope.model_copy(update={"principal": user}) if user else scope
                with self.assertRaises((ValueError, ArtifactError)):
                    handoff.candidate_headers("B", config=config, context=context, scope=binding)

    def test_forged_or_cross_parent_binding_is_rejected(self):
        scope, config, context = parent()
        for path in ("A", "B"):
            for updates in (
                {"principal": "forged-assignment-user"},
                {"parent_session": "other-parent"},
                {"project": PROJECT.replace("example-project", "other-project")},
            ):
                with self.subTest(path=path, updates=updates), self.assertRaises(ValueError):
                    handoff.candidate_headers(
                        path, config=config, context=context, scope=scope.model_copy(update=updates),
                    )
        context.session_id = "other-parent"
        with self.assertRaises(ArtifactError):
            handoff.candidate_headers("B", config=config, context=context, scope=scope)

    def test_candidate_does_not_change_shared_parent_headers(self):
        scope, config, context = parent()
        original = dict(context.platform_headers())
        delegated = handoff.candidate_headers("B", config=config, context=context, scope=scope)
        self.assertEqual(delegated, {**original, "x-ms-user-identity": scope.principal})
        self.assertEqual(context.platform_headers(), original)
        self.assertEqual(handoff.candidate_headers("A", config=config, context=context, scope=scope), original)
        self.assertNotIn("x-agent-user-id", delegated)
        delegated["x-agent-foundry-call-id"] = "changed"
        self.assertEqual(context.platform_headers(), original)

    def test_unexpected_platform_headers_are_rejected(self):
        scope, config, context = parent()
        for headers in (
            {}, {"x-agent-foundry-call-id": "other-call"},
            {**context.platform_headers(), "x-agent-user-id": scope.principal},
            {**context.platform_headers(), "x-ms-user-identity": scope.principal},
        ):
            with self.subTest(headers=headers), patch.object(
                FoundryAgentRequestContext, "platform_headers", return_value=headers,
            ), self.assertRaises(ValueError):
                handoff.candidate_headers("B", config=config, context=context, scope=scope)


class CandidateLifecycleTests(unittest.IsolatedAsyncioTestCase):
    async def test_failed_exact_retrieval_does_not_send_or_create(self):
        scope, config, context = parent()
        headers = handoff.candidate_headers("B", config=config, context=context, scope=scope)
        for role in ("architect", "reviewer"):
            with self.subTest(role=role):
                seen = []

                def handle(request):
                    seen.append((request.method, str(request.url)))
                    return httpx2.Response(200, json={
                        "id": "resp-synthetic-known", "object": "response", "created_at": 1,
                        "model": "synthetic", "status": "failed", "output": [],
                    })

                credential = SimpleNamespace(
                    get_token=AsyncMock(return_value=AccessToken("synthetic-token", 4102444800)),
                )
                async with httpx2.AsyncClient(transport=httpx2.MockTransport(handle)) as http:
                    async with ProjectClient(credential, http, headers) as project:
                        remote = RemoteAgents(project, headers)
                        child = Child(
                            role=role, name=AGENTS[role], version="7",
                            hosted_id="synthetic-child", framework={},
                        )
                        with patch.object(project.agents, "get_session", new_callable=AsyncMock) as check, \
                                patch.object(project.agents, "create_session", new_callable=AsyncMock) as create:
                            check.return_value = SimpleNamespace(
                                status="active", version_indicator=SimpleNamespace(agent_version="7"),
                            )
                            with self.assertRaises(DemoError) as caught:
                                await remote.recover(child, "resp-synthetic-known")
                            self.assertEqual(caught.exception.code, "SPECIALIST_INCOMPLETE")
                            create.assert_not_awaited()
                self.assertEqual([method for method, _ in seen], ["GET"])
                self.assertIn("resp-synthetic-known", seen[0][1])
                self.assertEqual(child.framework, {})

    async def test_both_paths_cover_raw_and_responses_lifecycle(self):
        # Real RemoteAgents, ProjectClient and FoundryAgent; raw SDK operation
        # methods and final HTTP transport are controlled external boundaries.
        # An intentional POST failure prevents a fake success from being called
        # specialist execution. Recovery uses one exact synthetic known response.
        scope, config, context = parent()
        for path in ("A", "B"):
            for role in ("architect", "reviewer"):
                with self.subTest(path=path, role=role):
                    headers = handoff.candidate_headers(path, config=config, context=context, scope=scope)
                    seen = []

                    def handle(request):
                        seen.append((request.method, dict(request.headers), str(request.url)))
                        if request.method == "POST":
                            return httpx2.Response(418, json={"error": {
                                "message": "Synthetic bounded stop.", "type": "probe", "code": "probe",
                            }})
                        return httpx2.Response(200, json={
                            "id": "resp-synthetic-known", "object": "response", "created_at": 1,
                            "model": "synthetic", "status": "completed",
                            "output": [{
                                "type": "message", "id": "msg-synthetic", "role": "assistant",
                                "status": "completed", "content": [{
                                    "type": "output_text", "text": "Synthetic recovered output.", "annotations": [],
                                }],
                            }],
                        })

                    credential = SimpleNamespace(
                        get_token=AsyncMock(return_value=AccessToken("synthetic-token", 4102444800)),
                    )
                    async with httpx2.AsyncClient(transport=httpx2.MockTransport(handle)) as http:
                        async with ProjectClient(credential, http, headers) as project:
                            remote = RemoteAgents(project, headers)
                            resource = SimpleNamespace(
                                status="active", version_indicator=SimpleNamespace(agent_version="7"),
                            )
                            with patch.object(project.agents, "get", new_callable=AsyncMock) as get, \
                                    patch.object(project.agents, "create_session", new_callable=AsyncMock) as create, \
                                    patch.object(project.agents, "get_session", new_callable=AsyncMock) as check:
                                get.return_value = SimpleNamespace(
                                    versions=SimpleNamespace(latest=SimpleNamespace(version="7")),
                                )
                                check.return_value = resource
                                child = await remote.prepare(role)
                                create.return_value = SimpleNamespace(agent_session_id=child.hosted_id)
                                await remote.create(child)
                                await remote._check(child)
                                await remote.recover_creation(child)
                                callback = AsyncMock()
                                with self.assertRaises(ChatClientException):
                                    await remote.invoke(child, {"synthetic": True}, callback)
                                result = await remote.recover(child, "resp-synthetic-known")
                                self.assertEqual(result, "Synthetic recovered output.")
                                self.assertEqual(check.await_count, 4)
                                self.assertEqual(create.await_count, 1)
                                get.assert_awaited_once_with(AGENTS[role], headers=headers)
                                for call in [*create.await_args_list, *check.await_args_list]:
                                    self.assertEqual(call.kwargs["headers"], headers)
                                callback.assert_not_awaited()
                    self.assertEqual([method for method, _, _ in seen], ["POST", "GET"])
                    for _, wire, url in seen:
                        for key, value in headers.items():
                            self.assertEqual(wire[key], value)
                        self.assertEqual("x-ms-user-identity" in wire, path == "B")
                        self.assertNotIn("x-agent-user-id", wire)
                        self.assertIn("/agents/" + AGENTS[role] + "/", url)
                    self.assertIn("resp-synthetic-known", seen[-1][2])
                    self.assertIn("agent_session_id=" + child.hosted_id, seen[-1][2])


class CandidateReceiverTests(unittest.TestCase):
    def test_actual_receiver_requires_same_principal_and_parent(self):
        scope, _, _ = parent()
        requirements = Requirements(chunks=["Synthetic private-ingress application."])
        req = Artifact(
            artifact_type="requirements", scope_binding=scope, operation_id="a" * 32,
            producer=Producer(
                role="coordinator", name=AGENTS["coordinator"], version="7",
                session_id=scope.parent_session, response_id="synthetic-parent-response",
            ),
            input_refs=[], requirements_revision=1, content=requirements, content_sha256=digest(requirements),
        ).ref()
        design = Candidate(requirements_revision=1, candidate_revision=1, design="Synthetic design.")
        candidate = Artifact(
            artifact_type="candidate", scope_binding=scope, operation_id="b" * 32,
            producer=Producer(
                role="architect", name=AGENTS["architect"], version="7",
                session_id="synthetic-architect", response_id="synthetic-architect-response",
            ),
            input_refs=[req], requirements_revision=1, candidate_revision=1,
            content=design, content_sha256=digest(design),
        ).ref()
        for role in ("architect", "reviewer"):
            with self.subTest(role=role):
                refs = [req] if role == "architect" else [req, candidate]
                producer = Producer(
                    role=role, name=AGENTS[role], version="7", session_id="synthetic-child",
                )
                assignment = Assignment(
                    scope_binding=scope, operation_id="c" * 32, producer=producer, input_refs=refs,
                    requirements_revision=1, candidate_revision=1,
                    output_type="candidate" if role == "architect" else "review", deadline_epoch=100,
                )
                manifest = Manifest(
                    scope_binding=scope, turn=1, candidate_revision=0 if role == "architect" else 1,
                    requirements=req, candidate=None if role == "architect" else candidate, accepted=refs,
                    children={role: ChildBinding(
                        role=role, name=producer.name, version="7", hosted_id=producer.session_id,
                        framework={}, bound=True,
                    )},
                    effect=Effect(
                        operation_id=assignment.operation_id, kind="call", status="dispatched", role=role,
                        input_refs=refs, assignment_sha256=digest(assignment),
                    ),
                )
                config = SimpleNamespace(
                    is_hosted=True, session_id=producer.session_id, project_endpoint=PROJECT,
                    agent_name=producer.name, agent_version="7",
                )
                context = SimpleNamespace(
                    session_id=producer.session_id, user_id=scope.principal, call_id="synthetic-child-call",
                )
                assignment.validate_receiver(config=config, context=context, manifest=manifest, now=100)
                for user in ("", "delegated-namespace:synthetic-user", "forged-user"):
                    context.user_id = user
                    with self.subTest(user=user), self.assertRaises(ArtifactError):
                        assignment.validate_receiver(config=config, context=context, manifest=manifest, now=100)
                context.user_id = scope.principal
                other = manifest.model_copy(update={
                    "scope_binding": scope.model_copy(update={"parent_session": "other-parent"}),
                })
                with self.assertRaises(ArtifactError):
                    assignment.validate_receiver(config=config, context=context, manifest=other, now=100)


class CandidateCommandTests(unittest.TestCase):
    def arguments(self, lab, version="1"):
        return [
            "--application-root", str(handoff.ROOT), "--lab-repository-root", str(lab),
            "--scenario", "offline-A-B",
            "--coordinator-version", "1", "--architect-version", version, "--reviewer-version", "1",
        ]

    def lab_fixture(self, directory):
        root = Path(directory)
        (root / ".git").mkdir()
        script = root / "foundry-tf/multi-agent/Test-PrivateConnectivity.ps1"
        script.parent.mkdir(parents=True)
        script.write_text("# Synthetic fixture, never executed.\n", encoding="utf-8")
        return root

    def test_invalid_roots_or_versions_fail_without_private_output(self):
        with tempfile.TemporaryDirectory() as directory:
            lab = self.lab_fixture(directory)
            cases = [self.arguments(handoff.ROOT), self.arguments(Path("relative-lab"))]
            cases += [self.arguments(lab, value) for value in ("invalid", "0", "-1", "1\n", "1.0")]
            for args in cases:
                with self.subTest(args=args), redirect_stdout(StringIO()) as output, \
                        patch.object(handoff, "offline_probes") as probes:
                    code = handoff.main(args)
                self.assertEqual(code, 1)
                probes.assert_not_called()
                self.assertNotIn(str(handoff.ROOT), output.getvalue())
                self.assertNotIn(directory, output.getvalue())
                self.assertEqual(json.loads(output.getvalue())["selection"], "unresolved")

    def test_verified_offline_report_stays_unresolved(self):
        with tempfile.TemporaryDirectory() as directory:
            lab = self.lab_fixture(directory)
            with redirect_stdout(StringIO()) as output, \
                    patch.object(handoff.diagnostic, "check_pins", return_value=[{"matches": True}]), \
                    patch.object(handoff, "offline_probes", return_value={"passed": True}):
                code = handoff.main(self.arguments(lab))
        report = json.loads(output.getvalue())
        self.assertEqual(code, 2)
        self.assertEqual(report["selection"], "unresolved")
        self.assertFalse(report["live_execution_available"])
        self.assertEqual(report["principal_namespace_compatibility"], "NOT_MEASURED")
        self.assertNotIn(directory, output.getvalue())


if __name__ == "__main__":
    unittest.main()
