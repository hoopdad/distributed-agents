"""Private, read-only Blob evidence window; not an aggregate producer or CLI.

``await read_scoped_state(service=authorized_async_blob_service, containers=...,
scope=trusted_scope, head=owned_manifest, head_etag=owned_etag,
quiescence_receipt=private_attribution, refs=exact_owned_refs,
required_operations=previously_observed_names)`` uses only public list/download
APIs. The caller owns authorization, client lifecycle and quiescence attribution.
It must not derive these inputs from model text, guessed hashes or discovery.
No credential, store, output file, logging sink or network client is constructed.

All returned objects are PRIVATE: exact downloaded bytes, raw listing pages,
opaque cursors, names, ETags and allowlisted source headers are retained, never
printed. The repr deliberately excludes them. A failed window retains bounded
partial receipts and issue codes; it must not be attached as complete evidence.
No journal state (including accepted) is evidence of an HTTP send.

``complete`` means two exhausted enumerations agreed, all observed/required
records were readable and unchanged, and the attributed manifest/refs matched
on both reads. It is conditional on the caller's quiescence attribution and
service listing semantics, NOT an atomic snapshot, historical completeness,
authentication attestation or live pass. Explicit empty NextMarker is required;
an omitted marker fails closed even though the SDK treats it as terminal.
Deletion before both lists, a lying terminal marker, or transient ABA between
reads cannot be ruled out. Supply previously retained names as required anchors
and compare prior immutable receipts externally across windows; this reader
cannot reconstruct missing history.
"""
from __future__ import annotations

import asyncio
import hashlib
import re
from dataclasses import dataclass
from typing import Mapping, Sequence
from xml.etree import ElementTree

from azure.core import MatchConditions

from demo.artifacts import (
    MAX_DOCUMENT_BYTES, Artifact, ArtifactRef, Effect, Manifest, ScopeBinding,
    canonical_bytes, decode_document,
)

# Local evidence memory limits, not workflow execution/attempt budgets.
MAX_RECORDS = 4096
MAX_LIST_BYTES = 4 * 1024 * 1024
SOURCE_HEADERS = ("etag", "x-ms-request-id", "x-ms-version-id", "content-length")


@dataclass(frozen=True, repr=False)
class SourceReceipt:
    status: int
    headers: tuple[tuple[str, str], ...]


@dataclass(frozen=True, repr=False)
class BlobReceipt:
    container: str
    name: str
    raw: bytes
    etag: str
    sha256: str
    sources: tuple[SourceReceipt, ...]
    phase: str


@dataclass(frozen=True, repr=False)
class PageReceipt:
    phase: str
    cursor: str | None
    next_cursor: str | None
    raw: bytes
    source: SourceReceipt


@dataclass(frozen=True, repr=False)
class ReadReceipt:
    container: str
    name: str
    phase: str
    sources: tuple[SourceReceipt, ...]
    downloaded: bool


@dataclass(frozen=True, repr=False)
class ScopedStateCapture:
    complete: bool
    issues: tuple[str, ...]
    quiescence_receipt: str
    blobs: tuple[BlobReceipt, ...]
    pages: tuple[PageReceipt, ...]
    reads: tuple[ReadReceipt, ...]
    # All distinct named transitions, not just the latest status per operation.
    operations: tuple[BlobReceipt, ...]
    artifacts: tuple[BlobReceipt, ...]
    manifest: BlobReceipt | None
    manifest_recheck: BlobReceipt | None


def _source(response) -> SourceReceipt:
    return SourceReceipt(
        response.status_code,
        tuple((key, str(response.headers[key])) for key in SOURCE_HEADERS if key in response.headers),
    )


def _operation_name(scope, name):
    return isinstance(name, str) and re.fullmatch(
        re.escape(scope.prefix) + r"operations/[a-f0-9]{32}/[a-z_]{1,32}\.json", name,
    ) is not None


async def read_scoped_state(
    *, service, containers: Mapping[str, str], scope: ScopeBinding, head: Manifest,
    head_etag: str, quiescence_receipt: str, refs: Sequence[ArtifactRef],
    required_operations: Sequence[str] = (),
) -> ScopedStateCapture:
    """Observe one caller-attributed quiescent window, with no writes.

    ``service`` is an existing authorized azure.storage.blob.aio.BlobServiceClient
    (or public-interface equivalent). Only its get_container_client/list_blobs
    and get_blob_client/download_blob/readall surfaces are used. The service is
    neither entered nor closed. All three logical container bindings are required.
    ``refs`` must exactly cover head.accepted, including historical accepted refs.
    ``required_operations`` anchors previously retained journal names; the head
    effect's current transition is always required as well. Validation happens
    before the first client call. Bad caller bindings raise ValueError with a
    constant code; read/list/integrity failures return incomplete, not raw errors.
    Cancellation propagates unchanged. No result changes authorization or holds.
    No reader retry loop is added; per-call retry_total=0 disables pipeline
    retries. SDK-internal download recovery is not overridden; every source
    response reached by the public hook is retained.
    """
    # Freeze mutable caller-owned models/mappings before the first await.
    if not isinstance(scope, ScopeBinding) or not isinstance(head, Manifest):
        raise ValueError("READER_BINDING")
    try:
        scope = ScopeBinding.model_validate(scope.model_dump(mode="json"))
        head = Manifest.model_validate(head.model_dump(mode="json"))
        refs = tuple(ArtifactRef.model_validate(ref.model_dump(mode="json")) for ref in refs)
        containers = dict(containers)
        expected = canonical_bytes(head)
        required = tuple(required_operations)
    except Exception:
        # Pydantic errors can include private input values; do not propagate them.
        raise ValueError("READER_BINDING") from None
    if (
        head.scope_binding != scope or not isinstance(head_etag, str) or not head_etag
        or head.turn < 1 or not head.active_response_id or not head.coordinator_version
        or not isinstance(quiescence_receipt, str) or not quiescence_receipt
        or set(containers) != {"control", "candidates", "reviews"}
        or len(set(containers.values())) != 3
        or any(not isinstance(v, str) or not re.fullmatch(r"[a-z0-9-]{3,63}", v)
               for v in containers.values())
        or len(refs) != len(head.accepted) or set(refs) != set(head.accepted)
        or len(set(required)) != len(required)
        or any(not _operation_name(scope, name) for name in required)
    ):
        raise ValueError("READER_BINDING")
    for ref in refs:
        ref.assert_scope(scope)
    if head.effect is not None:
        for ref in (*head.effect.input_refs, *([head.effect.output_ref] if head.effect.output_ref else [])):
            ref.assert_scope(scope)
        required += (
            f"{scope.prefix}operations/{head.effect.operation_id}/{head.effect.status}.json",
        )
    issues, blobs, pages, reads = [], [], [], []

    def issue(code):
        if code not in issues:
            issues.append(code)

    async def download(container, name, phase, etag=None):
        sources = []
        downloaded = False

        def hook(response):
            sources.append(_source(response.http_response))

        options = {"raw_response_hook": hook, "retry_total": 0, "logging_enable": False}
        if etag is not None:
            options.update(etag=etag, match_condition=MatchConditions.IfNotModified)
        try:
            stream = await service.get_blob_client(containers[container], name).download_blob(
                offset=0, length=MAX_DOCUMENT_BYTES + 1, **options,
            )
            if not isinstance(stream.size, int) or not 0 <= stream.size <= MAX_DOCUMENT_BYTES:
                issue("BLOB_SIZE")
                return None
            raw = await stream.readall()
            receipt = BlobReceipt(
                container, name, raw, stream.properties.etag,
                hashlib.sha256(raw).hexdigest(), tuple(sources), phase,
            )
            blobs.append(receipt)
            downloaded = True
            if (
                not receipt.etag or len(raw) != stream.size or not sources
                or any(source.status not in (200, 206) for source in sources)
                or (etag is not None and receipt.etag != etag)
            ):
                issue("BLOB_RECEIPT")
            return receipt
        except asyncio.CancelledError:
            raise
        except Exception:
            issue("BLOB_READ")
            return None
        finally:
            reads.append(ReadReceipt(container, name, phase, tuple(sources), downloaded))

    async def manifest(phase):
        receipt = await download("control", scope.prefix + "manifest.json", phase, head_etag)
        if receipt:
            try:
                value = Manifest.model_validate(decode_document(receipt.raw))
                if value.scope_binding != scope or canonical_bytes(value) != expected:
                    issue("MANIFEST_MOVED")
            except Exception:
                issue("MANIFEST_INVALID")
        return receipt

    async def listing(phase):
        entries, seen_names, seen_tokens = [], set(), set()
        captured = []
        cursor = None
        terminal_seen = False

        def hook(response):
            # Public nonstreaming listing response, not artifact/model body.
            raw = response.http_response.body()
            if len(raw) > MAX_LIST_BYTES:
                issue("LIST_SIZE")
                raise ValueError("LIST_SIZE")
            captured.append((raw, _source(response.http_response)))

        try:
            iterator = service.get_container_client(containers["control"]).list_blobs(
                name_starts_with=scope.prefix + "operations/", results_per_page=100,
                raw_response_hook=hook, retry_total=0, logging_enable=False,
            ).by_page()
            async for page in iterator:
                batch = [item async for item in page]
                next_cursor = iterator.continuation_token
                invalid_page = False
                if len(captured) != 1:
                    issue("LIST_RECEIPT")
                    invalid_page = True
                for raw, source in captured:
                    pages.append(PageReceipt(phase, cursor, next_cursor, raw, source))
                    try:
                        root = ElementTree.fromstring(raw)
                        if (
                            root.tag != "EnumerationResults"
                            or root.findtext("Prefix") != scope.prefix + "operations/"
                        ):
                            issue("LIST_PREFIX")
                            invalid_page = True
                        markers = root.findall("NextMarker")
                        if len(markers) != 1:
                            issue("CURSOR_MISSING")
                            invalid_page = True
                        elif (markers[0].text or None) != (next_cursor or None):
                            issue("CURSOR_MISMATCH")
                            invalid_page = True
                        if source.status != 200:
                            issue("LIST_RECEIPT")
                            invalid_page = True
                    except ElementTree.ParseError:
                        issue("LIST_INVALID")
                        invalid_page = True
                captured.clear()
                for item in batch:
                    name = item.name
                    if not _operation_name(scope, name):
                        issue("OPERATION_SCOPE")
                        continue  # never download an out-of-scope listed name
                    if name in seen_names:
                        issue("DUPLICATE_NAME")
                    seen_names.add(name)
                    if not isinstance(item.etag, str) or not item.etag or not isinstance(item.size, int):
                        issue("LIST_ENTRY")
                        continue
                    entries.append((name, item.etag, item.size))
                if invalid_page:
                    break  # never let a response broaden the next SDK prefix
                if not next_cursor:
                    terminal_seen = True
                if len(entries) > MAX_RECORDS or len(pages) > MAX_RECORDS:
                    issue("LIST_LIMIT")
                    break
                if next_cursor:
                    if next_cursor in seen_tokens:
                        issue("CURSOR_REPEATED")
                        break
                    seen_tokens.add(next_cursor)
                cursor = next_cursor
        except asyncio.CancelledError:
            raise
        except Exception:
            issue("LIST_READ")
        finally:
            # Preserve a malformed/truncated page captured before SDK parsing.
            for raw, source in captured:
                pages.append(PageReceipt(phase, cursor, None, raw, source))
            if not terminal_seen:
                issue("LIST_INCOMPLETE")
        return entries

    async def artifact(ref, phase, etag=None):
        receipt = await download(ref.container, ref.name, phase, etag)
        if receipt:
            try:
                value = Artifact.model_validate(decode_document(receipt.raw))
                if value.scope_binding != scope or value.ref() != ref:
                    issue("ARTIFACT_INTEGRITY")
            except Exception:
                issue("ARTIFACT_INVALID")
        return receipt

    first = await manifest("before")
    artifacts = []
    for ref in refs:
        receipt = await artifact(ref, "before")
        if receipt:
            artifacts.append(receipt)
    entries = await listing("before")
    operations = []
    for name, etag, size in entries:
        receipt = await download("control", name, "before", etag)
        if receipt:
            operations.append(receipt)
            if len(receipt.raw) != size:
                issue("OPERATION_SIZE")
            try:
                value = decode_document(receipt.raw)
                if set(value) != {"scope_binding", "effect"}:
                    raise ValueError("OPERATION_DOCUMENT")
                binding = ScopeBinding.model_validate(value["scope_binding"])
                effect = Effect.model_validate(value["effect"])
                expected_name = (
                    f"{scope.prefix}operations/{effect.operation_id}/{effect.status}.json"
                )
                if binding != scope or name != expected_name:
                    issue("OPERATION_BINDING")
                for ref in (*effect.input_refs, *([effect.output_ref] if effect.output_ref else [])):
                    ref.assert_scope(scope)
                if head.effect and name == (
                    f"{scope.prefix}operations/{head.effect.operation_id}/{head.effect.status}.json"
                ) and effect != head.effect:
                    issue("HEAD_EFFECT_MISMATCH")
            except Exception:
                issue("OPERATION_INVALID")
    if not set(required).issubset({receipt.name for receipt in operations}):
        issue("OPERATION_GAP")
    second_entries = await listing("after")
    if sorted(entries) != sorted(second_entries):
        issue("LIST_MOVED")
    # Retain each second receipt too: rechecking never overwrites earlier bytes.
    for receipt in (*operations, *artifacts):
        second = await download(receipt.container, receipt.name, "after", receipt.etag)
        if second and (second.raw != receipt.raw or second.etag != receipt.etag):
            issue("IMMUTABLE_MOVED")
    last = await manifest("after")
    if first and last and (first.raw != last.raw or first.etag != last.etag):
        issue("MANIFEST_MOVED")
    return ScopedStateCapture(
        not issues, tuple(issues), quiescence_receipt, tuple(blobs), tuple(pages),
        tuple(reads), tuple(operations), tuple(artifacts), first, last,
    )
