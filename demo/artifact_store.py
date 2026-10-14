from __future__ import annotations

import asyncio
import ipaddress
import re
from contextlib import asynccontextmanager, suppress
from dataclasses import dataclass
from typing import Any
from urllib.parse import urlsplit

from azure.core import MatchConditions
from azure.core.exceptions import HttpResponseError, ResourceExistsError, ResourceNotFoundError
from azure.core.pipeline.transport import AioHttpTransport
from azure.storage.blob import ContentSettings
from azure.storage.blob.aio import BlobServiceClient

from .artifacts import (
    Artifact,
    ArtifactError,
    ArtifactRef,
    Assignment,
    Container,
    Manifest,
    Role,
    ScopeBinding,
    canonical_bytes,
    decode_document,
    digest,
)

READ_ACCESS = {
    "coordinator": frozenset(("control", "candidates", "reviews")),
    "architect": frozenset(("control", "candidates", "reviews")),
    "reviewer": frozenset(("control", "candidates", "reviews")),
}
WRITE_ACCESS = {"coordinator": "control", "architect": "candidates", "reviewer": "reviews"}


def validate_storage_configuration(endpoint: str, containers: dict[Container, str]) -> None:
    uri = urlsplit(endpoint)
    if (
        uri.scheme != "https" or uri.port not in (None, 443) or uri.username or uri.password
        or uri.query or uri.fragment or uri.path not in ("", "/") or not uri.hostname
        or not re.fullmatch(r"[a-z0-9]{3,24}\.blob\.core\.windows\.net", uri.hostname)
    ):
        raise ArtifactError("ARTIFACT_STORAGE_CONFIGURATION")
    if set(containers) != {"control", "candidates", "reviews"} or len(set(containers.values())) != 3:
        raise ArtifactError("ARTIFACT_CONTAINER_CONFIGURATION")
    if any(
        not re.fullmatch(r"[a-z0-9](?:[a-z0-9-]{1,61}[a-z0-9])", value) or "--" in value
        for value in containers.values()
    ):
        raise ArtifactError("ARTIFACT_CONTAINER_CONFIGURATION")


@dataclass
class LockedDocument:
    blob: Any
    lease: Any
    etag: str
    value: Any
    renewal: asyncio.Task

    async def assert_owner(self) -> None:
        if self.renewal.done():
            await self.renewal
            raise ArtifactError("ARTIFACT_LEASE_LOST")
        await self.lease.renew()

    async def save(self, value: Any) -> None:
        await self.assert_owner()
        try:
            result = await self.blob.upload_blob(
                canonical_bytes(value), overwrite=True,
                etag=self.etag, match_condition=MatchConditions.IfNotModified,
                lease=self.lease.id, content_settings=ContentSettings(content_type="application/json"),
            )
        except HttpResponseError as exc:
            if exc.status_code in (409, 412):
                raise ArtifactError("ARTIFACT_FENCE_CONFLICT") from exc
            raise
        self.etag, self.value = result["etag"], value


class BlobArtifacts:
    def __init__(
        self, *, role: Role, scope: ScopeBinding, endpoint: str,
        containers: dict[Container, str], credential, service=None, expected_private_ips: list[str] | None = None,
    ):
        validate_storage_configuration(endpoint, containers)
        if role not in WRITE_ACCESS:
            raise ArtifactError("ARTIFACT_ROLE")
        self.role, self.scope, self.containers = role, scope, containers
        self.endpoint, self.expected_private_ips = endpoint, expected_private_ips
        if service is None and not expected_private_ips:
            raise ArtifactError("ARTIFACT_PRIVATE_BINDING_REQUIRED")
        self.service = service or BlobServiceClient(
            endpoint.rstrip("/"), credential=credential,
            retry_total=0, connection_timeout=10, read_timeout=30,
            logging_enable=False, max_single_get_size=131072,
            transport=AioHttpTransport(use_env_settings=False),
        )

    async def __aenter__(self):
        await self.service.__aenter__()
        return self

    async def __aexit__(self, *args):
        await self.service.__aexit__(*args)

    async def verify_private_path(self) -> None:
        if not self.expected_private_ips:
            raise ArtifactError("ARTIFACT_PRIVATE_BINDING_REQUIRED")
        try:
            expected = {ipaddress.IPv4Address(value) for value in self.expected_private_ips}
        except ipaddress.AddressValueError as exc:
            raise ArtifactError("ARTIFACT_PRIVATE_BINDING") from exc
        networks = tuple(ipaddress.IPv4Network(value) for value in ("10.0.0.0/8", "172.16.0.0/12", "192.168.0.0/16"))
        if len(expected) != len(self.expected_private_ips) or any(
            not any(address in network for network in networks) for address in expected
        ):
            raise ArtifactError("ARTIFACT_PRIVATE_BINDING")
        async with asyncio.timeout(10):
            resolved = await asyncio.get_running_loop().getaddrinfo(urlsplit(self.endpoint).hostname, 443)
        addresses = {ipaddress.ip_address(item[4][0]) for item in resolved}
        if not addresses or addresses != expected:
            raise ArtifactError("ARTIFACT_PRIVATE_DNS_MISMATCH")

    def _blob(self, container: Container, name: str, *, writing: bool = False, global_control=False):
        if container not in READ_ACCESS[self.role]:
            raise ArtifactError("ARTIFACT_ROLE_ACCESS")
        if writing and container != WRITE_ACCESS[self.role]:
            raise ArtifactError("ARTIFACT_ROLE_ACCESS")
        if global_control:
            if self.role != "coordinator" or container != "control" or not re.fullmatch(
                r"admission/v1/[a-f0-9]{64}\.json", name
            ):
                raise ArtifactError("ARTIFACT_SCOPE")
        elif (
            not name.startswith(self.scope.prefix) or "\\" in name or ".." in name
            or not re.fullmatch(r"[A-Za-z0-9/_.-]+", name)
        ):
            raise ArtifactError("ARTIFACT_SCOPE")
        return self.service.get_blob_client(self.containers[container], name)

    async def _read(self, blob) -> bytes:
        download = await blob.download_blob()
        if download.size > 131072:
            raise ArtifactError("ARTIFACT_BYTE_LIMIT")
        raw = await download.readall()
        decode_document(raw)
        return raw

    async def read_artifact(self, ref: ArtifactRef) -> Artifact:
        ref.assert_scope(self.scope)
        raw = await self._read(self._blob(ref.container, ref.name))
        artifact = Artifact.model_validate(decode_document(raw))
        if artifact.scope_binding != self.scope or artifact.ref() != ref:
            raise ArtifactError("ARTIFACT_INTEGRITY")
        return artifact

    async def read_output(self, *, artifact_type: str, revision: int, operation_id: str) -> Artifact | None:
        directories = {"requirements": "requirements", "candidate": "candidates", "review": "reviews", "decision": "decisions"}
        containers = {"requirements": "control", "candidate": "candidates", "review": "reviews", "decision": "control"}
        if artifact_type not in directories or not re.fullmatch(r"[a-f0-9]{32}", operation_id) or not 1 <= revision <= 50:
            raise ArtifactError("ARTIFACT_OUTPUT_LOCATOR")
        name = f"{self.scope.prefix}{directories[artifact_type]}/{revision}/{operation_id}.json"
        try:
            raw = await self._read(self._blob(containers[artifact_type], name))
        except ResourceNotFoundError:
            return None
        artifact = Artifact.model_validate(decode_document(raw))
        if (
            artifact.scope_binding != self.scope or artifact.operation_id != operation_id
            or artifact.artifact_type != artifact_type or artifact.requirements_revision != revision
            or artifact.ref().name != name
        ):
            raise ArtifactError("ARTIFACT_INTEGRITY")
        return artifact

    async def write_artifact(self, artifact: Artifact) -> ArtifactRef:
        if artifact.scope_binding != self.scope or artifact.producer.role != self.role:
            raise ArtifactError("ARTIFACT_PRODUCER")
        ref = artifact.ref()
        await self._immutable(ref.container, ref.name, canonical_bytes(artifact))
        return ref

    async def _immutable(self, container: Container, name: str, raw: bytes) -> None:
        blob = self._blob(container, name, writing=True)
        try:
            await blob.upload_blob(
                raw, overwrite=False, content_settings=ContentSettings(content_type="application/json")
            )
        except ResourceExistsError:
            if await self._read(blob) != raw:
                raise ArtifactError("ARTIFACT_IMMUTABLE_COLLISION")

    async def write_assignment(self, assignment: Assignment) -> str:
        if self.role != "coordinator" or assignment.scope_binding != self.scope:
            raise ArtifactError("ASSIGNMENT_WRITER")
        name = f"{self.scope.prefix}assignments/{assignment.operation_id}.json"
        await self._immutable("control", name, canonical_bytes(assignment))
        return name

    async def read_assignment(self, operation_id: str) -> Assignment:
        if not re.fullmatch(r"[a-f0-9]{32}", operation_id):
            raise ArtifactError("ASSIGNMENT_ID")
        name = f"{self.scope.prefix}assignments/{operation_id}.json"
        raw = await self._read(self._blob("control", name))
        value = Assignment.model_validate(decode_document(raw))
        if value.scope_binding != self.scope or value.operation_id != operation_id:
            raise ArtifactError("ASSIGNMENT_INTEGRITY")
        return value

    async def read_manifest(self) -> Manifest:
        raw = await self._read(self._blob("control", f"{self.scope.prefix}manifest.json"))
        manifest = Manifest.model_validate(decode_document(raw))
        if manifest.scope_binding != self.scope:
            raise ArtifactError("MANIFEST_SCOPE")
        return manifest

    async def write_operation(self, operation_id: str, transition: str, value: Any) -> None:
        if self.role != "coordinator" or not re.fullmatch(r"[a-f0-9]{32}", operation_id):
            raise ArtifactError("OPERATION_WRITER")
        if not re.fullmatch(r"[a-z_]{1,32}", transition):
            raise ArtifactError("OPERATION_TRANSITION")
        await self._immutable(
            "control", f"{self.scope.prefix}operations/{operation_id}/{transition}.json",
            canonical_bytes(value),
        )

    @asynccontextmanager
    async def lock_manifest(self):
        initial = Manifest(scope_binding=self.scope)
        async with self.lock_document(f"{self.scope.prefix}manifest.json", initial) as document:
            manifest = Manifest.model_validate(document.value)
            if manifest.scope_binding != self.scope:
                raise ArtifactError("MANIFEST_SCOPE")
            document.value = manifest
            yield document

    @asynccontextmanager
    async def lock_document(self, name: str, initial: Any, *, global_control=False):
        blob = self._blob("control", name, writing=True, global_control=global_control)
        try:
            await blob.upload_blob(
                canonical_bytes(initial), overwrite=False,
                content_settings=ContentSettings(content_type="application/json"),
            )
        except ResourceExistsError:
            pass
        try:
            lease = await blob.acquire_lease(lease_duration=60)
        except HttpResponseError as exc:
            if exc.status_code in (409, 412):
                raise ArtifactError("PARENT_IN_USE" if not global_control else "DECISION_ADMISSION_BUSY") from exc
            raise

        async def renew():
            while True:
                await asyncio.sleep(20)
                await lease.renew()

        renewal = asyncio.create_task(renew())
        try:
            download = await blob.download_blob(lease=lease.id)
            if download.size > 131072:
                raise ArtifactError("ARTIFACT_BYTE_LIMIT")
            value = decode_document(await download.readall())
            document = LockedDocument(blob, lease, download.properties.etag, value, renewal)
            yield document
            if renewal.done():
                await renewal
        finally:
            renewal.cancel()
            with suppress(asyncio.CancelledError):
                await renewal
            await lease.release()

    @property
    def admission_name(self) -> str:
        return f"admission/v1/{digest(self.scope.project)}.json"
