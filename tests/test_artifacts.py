from __future__ import annotations

import json
import asyncio
import unittest
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch

from pydantic import ValidationError
from azure.core.exceptions import ResourceExistsError

from demo.artifacts import (
    Artifact,
    ArtifactError,
    AssignmentLocator,
    OutputLocator,
    Producer,
    Requirements,
    ScopeBinding,
    canonical_bytes,
    decode_document,
    digest,
)
from demo.artifact_store import BlobArtifacts, validate_storage_configuration


class ArtifactContractTests(unittest.TestCase):
    def binding(self, **changes):
        values = dict(
            project="https://example.services.ai.azure.com/api/projects/example",
            tenant="11111111-1111-1111-1111-111111111111",
            principal="platform-user",
            parent_session="platform-parent",
        )
        values.update(changes)
        return ScopeBinding(**values)

    def test_scope_requires_platform_binding_not_request_selector(self):
        config = SimpleNamespace(is_hosted=True, session_id="platform-parent")
        context = SimpleNamespace(
            session_id="supplied-parent", user_id="platform-user", call_id="platform-call"
        )
        with self.assertRaises(ArtifactError) as caught:
            ScopeBinding.from_platform(
                config, context, project=self.binding().project, tenant=self.binding().tenant
            )
        self.assertEqual(caught.exception.code, "TRUSTED_PARENT_REQUIRED")

    def test_scope_rejects_missing_identity_or_local_host(self):
        for hosted, user, call in ((False, "user", "call"), (True, "", "call"), (True, "user", "")):
            with self.subTest(hosted=hosted, user=user, call=call):
                with self.assertRaises(ArtifactError):
                    ScopeBinding.from_platform(
                        SimpleNamespace(is_hosted=hosted, session_id="parent"),
                        SimpleNamespace(session_id="parent", user_id=user, call_id=call),
                        project=self.binding().project, tenant=self.binding().tenant,
                    )

    def test_parent_principal_tenant_and_project_are_isolated(self):
        original = self.binding()
        variants = (
            self.binding(parent_session="other-parent"),
            self.binding(principal="other-principal"),
            self.binding(tenant="22222222-2222-2222-2222-222222222222"),
            self.binding(project="https://other.services.ai.azure.com/api/projects/example"),
        )
        self.assertEqual(len({original.prefix, *(item.prefix for item in variants)}), 5)
        self.assertNotIn("platform-parent", original.prefix)
        self.assertNotIn("platform-user", original.prefix)

    def test_framed_scope_digests_do_not_alias_concatenated_ids(self):
        self.assertNotEqual(
            self.binding(principal="a", parent_session="bc").prefix,
            self.binding(principal="ab", parent_session="c").prefix,
        )

    def test_binding_is_immutable_and_rejects_unknown_fields(self):
        with self.assertRaises(ValidationError):
            self.binding().parent_session = "replacement"
        with self.assertRaises(ValidationError):
            ScopeBinding(**{**self.binding().model_dump(), "authorization": True})

    def test_locators_require_integer_schema_version_one(self):
        content = Requirements(chunks=["Synthetic requirement."])
        artifact = Artifact(
            artifact_type="requirements", scope_binding=self.binding(), operation_id="a" * 32,
            producer=Producer(
                role="coordinator", name="coordinator", version="2", session_id="platform-parent",
                response_id="response-one",
            ),
            input_refs=[], requirements_revision=1, content=content, content_sha256=digest(content),
        )
        for model, fields in (
            (AssignmentLocator, {"scope_binding": self.binding().model_dump(), "operation_id": "a" * 32}),
            (OutputLocator, {"artifact_ref": artifact.ref().model_dump()}),
        ):
            with self.subTest(model=model.__name__, version=1):
                locator = model.model_validate({"schema_version": 1, **fields})
                self.assertEqual(decode_document(canonical_bytes(locator)), {"schema_version": 1, **fields})
            for version in (0, 2, -1, "1", True, False, 1.0, None):
                with self.subTest(model=model.__name__, version=version), self.assertRaises(ValidationError):
                    model.model_validate({"schema_version": version, **fields})
            with self.subTest(model=model.__name__, version="missing"), self.assertRaises(ValidationError):
                model.model_validate(fields)

    def test_canonical_serialization_is_stable_and_rejects_nonfinite_values(self):
        self.assertEqual(canonical_bytes({"b": 1, "a": "test"}), b'{"a":"test","b":1}')
        for value in (float("nan"), float("inf"), float("-inf")):
            with self.subTest(value=value), self.assertRaises(ArtifactError):
                canonical_bytes({"number": value})

    def test_json_duplicate_keys_and_oversize_are_rejected(self):
        for raw in (b'{"parent":"a","parent":"b"}', b" " * 131073, b'{"value":NaN}'):
            with self.subTest(raw_size=len(raw)), self.assertRaises(ArtifactError):
                decode_document(raw)

    def test_depth_limit_is_measured_not_only_byte_count(self):
        value = "leaf"
        for _ in range(17):
            value = [value]
        with self.assertRaises(ArtifactError):
            decode_document(json.dumps(value).encode())


class BlobArtifactTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.scope = ArtifactContractTests().binding()
        self.blob = MagicMock()
        self.blob.upload_blob = AsyncMock()
        self.blob.download_blob = AsyncMock()
        self.service = MagicMock()
        self.service.get_blob_client.return_value = self.blob
        self.store = self.make_store("coordinator")
        self.content = Requirements(chunks=["Synthetic private ingress requirement."])
        self.artifact = Artifact(
            artifact_type="requirements", scope_binding=self.scope, operation_id="a" * 32,
            producer=Producer(
                role="coordinator", name="coordinator", version="2", session_id="platform-parent",
                response_id="response-one",
            ),
            input_refs=[], requirements_revision=1, content=self.content,
            content_sha256=digest(self.content),
        )

    def make_store(self, role):
        return BlobArtifacts(
            role=role, scope=self.scope, endpoint="https://examplestorage.blob.core.windows.net",
            containers={"control": "control", "candidates": "candidates", "reviews": "reviews"},
            credential=None, service=self.service,
        )

    def downloaded(self, raw):
        download = MagicMock()
        download.size = len(raw)
        download.readall = AsyncMock(return_value=raw)
        self.blob.download_blob.return_value = download

    async def test_create_only_artifact_write_uses_own_container(self):
        ref = await self.store.write_artifact(self.artifact)
        self.assertEqual(ref.container, "control")
        self.assertFalse(self.blob.upload_blob.call_args.kwargs["overwrite"])
        self.assertEqual(self.blob.upload_blob.call_args.args[0], canonical_bytes(self.artifact))

    async def test_immutable_identical_duplicate_is_idempotent(self):
        self.blob.upload_blob.side_effect = ResourceExistsError("exists")
        self.downloaded(canonical_bytes(self.artifact))
        self.assertEqual(await self.store.write_artifact(self.artifact), self.artifact.ref())
        self.assertEqual(self.blob.upload_blob.await_count, 1)

    async def test_immutable_collision_fails_without_overwrite(self):
        self.blob.upload_blob.side_effect = ResourceExistsError("exists")
        self.downloaded(b'{"different":"content"}')
        with self.assertRaises(ArtifactError) as caught:
            await self.store.write_artifact(self.artifact)
        self.assertEqual(caught.exception.code, "ARTIFACT_IMMUTABLE_COLLISION")
        self.assertEqual(self.blob.upload_blob.await_count, 1)

    async def test_exact_hash_is_verified_when_consuming_input(self):
        self.downloaded(canonical_bytes(self.artifact))
        wrong = self.artifact.ref().model_copy(update={"sha256": "b" * 64})
        with self.assertRaises(ArtifactError) as caught:
            await self.store.read_artifact(wrong)
        self.assertEqual(caught.exception.code, "ARTIFACT_INTEGRITY")

    async def test_cross_parent_read_is_rejected_before_network(self):
        other = ArtifactContractTests().binding(parent_session="other")
        artifact = self.artifact.model_copy(update={"scope_binding": other})
        with self.assertRaises(ArtifactError):
            await self.store.read_artifact(artifact.ref())
        self.blob.download_blob.assert_not_awaited()

    async def test_specialists_cannot_write_control_or_manifests(self):
        for role in ("architect", "reviewer"):
            with self.subTest(role=role), self.assertRaises(ArtifactError):
                await self.make_store(role).write_artifact(self.artifact)
            with self.subTest(role=role), self.assertRaises(ArtifactError):
                async with self.make_store(role).lock_manifest():
                    self.fail("Specialist acquired manifest write authority.")
        self.blob.upload_blob.assert_not_awaited()

    async def test_private_dns_requires_the_exact_configured_rfc1918_set(self):
        self.store.expected_private_ips = ["10.1.2.3"]
        loop = asyncio.get_running_loop()
        with patch.object(loop, "getaddrinfo", new=AsyncMock(return_value=[
            (2, 1, 6, "", ("10.1.2.3", 443)),
        ])):
            await self.store.verify_private_path()
        for resolved in (["203.0.113.1"], ["10.1.2.3", "203.0.113.1"], ["10.1.2.4"], []):
            with self.subTest(resolved=resolved), patch.object(
                loop, "getaddrinfo",
                new=AsyncMock(return_value=[(2, 1, 6, "", (value, 443)) for value in resolved]),
            ):
                with self.assertRaises(ArtifactError) as caught:
                    await self.store.verify_private_path()
                self.assertEqual(caught.exception.code, "ARTIFACT_PRIVATE_DNS_MISMATCH")
        for expected in (["203.0.113.1"], ["127.0.0.1"], ["::1"], ["10.1.2.3", "10.1.2.3"]):
            self.store.expected_private_ips = expected
            with self.subTest(expected=expected), self.assertRaises(ArtifactError):
                await self.store.verify_private_path()
        self.blob.download_blob.assert_not_awaited()

    def test_storage_rejects_credentials_public_paths_and_aliased_containers(self):
        containers = {"control": "control", "candidates": "candidates", "reviews": "reviews"}
        for endpoint in (
            "http://examplestorage.blob.core.windows.net",
            "https://examplestorage.blob.core.windows.net/?sig=not-a-real-secret",
            "https://user@example.blob.core.windows.net", "https://example.com",
        ):
            with self.subTest(endpoint=endpoint), self.assertRaises(ArtifactError):
                validate_storage_configuration(endpoint, containers)
        with self.assertRaises(ArtifactError):
            validate_storage_configuration(
                "https://examplestorage.blob.core.windows.net",
                {**containers, "reviews": "control"},
            )


if __name__ == "__main__":
    unittest.main()
