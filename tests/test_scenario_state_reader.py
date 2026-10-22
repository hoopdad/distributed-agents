"""Pinned public Blob SDK + synthetic HTTP transport. No network or tokens.

These tests exercise real list_blobs().by_page() and download_blob().readall(),
not a stand-in pager. Fixtures retain private-style data only in process.
"""
from __future__ import annotations

import asyncio
from contextlib import redirect_stderr, redirect_stdout
import hashlib
import io
import json
import unittest
from urllib.parse import parse_qs, unquote, urlsplit
from xml.etree.ElementTree import Element, SubElement, tostring

from azure.core.pipeline.transport import AsyncHttpResponse, AsyncHttpTransport
from azure.core.utils import CaseInsensitiveDict
from azure.storage.blob.aio import BlobServiceClient

from demo.artifacts import (
    MAX_DOCUMENT_BYTES, Artifact, Candidate, Effect, Manifest, Producer, Requirements,
    Review, ScopeBinding, canonical_bytes, digest,
)
from scenario_state_reader import read_scoped_state

CONTAINERS = {"control": "control", "candidates": "candidates", "reviews": "reviews"}
DATE = "Wed, 21 Oct 2026 00:00:00 GMT"


def binding(parent="private-parent"):
    return ScopeBinding(
        project="https://example.services.ai.azure.com/api/projects/example",
        tenant="11111111-1111-1111-1111-111111111111",
        principal="private-principal", parent_session=parent,
    )


class Response(AsyncHttpResponse):
    def __init__(self, request, raw, status=200, *, etag='"etag"', request_id="source-request"):
        super().__init__(request, None)
        self.status_code, self.reason = status, "Synthetic"
        self.headers = CaseInsensitiveDict({
            "content-type": "application/xml", "content-length": str(len(raw)),
            "last-modified": DATE, "etag": etag, "x-ms-request-id": request_id,
            "x-ms-blob-type": "BlockBlob", "x-ms-version-id": "source-version",
            # Must not escape the allowlisted source-receipt boundary.
            "authorization": "synthetic-secret-header",
        })
        if status == 206:
            self.headers["content-range"] = f"bytes 0-{len(raw)-1}/{len(raw)}"
        self.content_type = self.headers["content-type"]
        self.raw = raw

    def body(self):
        return self.raw

    async def load_body(self):
        return None

    async def read(self):
        return self.raw

    def stream_download(self, pipeline, **kwargs):
        return Stream(self)

    async def close(self):
        pass


class Stream:
    """SDK deserializer attaches public response properties to its stream."""

    def __init__(self, response):
        self.response = response
        self.raw = response.raw
        self.content_length = len(self.raw)
        self.done = False

    def __aiter__(self):
        return self

    async def __anext__(self):
        if self.done:
            raise StopAsyncIteration
        self.done = True
        return self.raw


class Transport(AsyncHttpTransport):
    def __init__(self):
        self.data = {}
        self.pages = {}
        self.requests = []
        self.before_send = None
        self.page_calls = {}
        self.read_counts = {}
        self.closed = False

    async def open(self):
        pass

    async def close(self):
        self.closed = True

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        await self.close()

    def put(self, container, name, raw, etag='"immutable"'):
        self.data[container, name] = (raw, etag)

    def list_xml(self, names, marker, prefix):
        root = Element("EnumerationResults", ServiceEndpoint="https://synthetic.blob.core.windows.net/",
                       ContainerName="control")
        SubElement(root, "Prefix").text = prefix
        SubElement(root, "MaxResults").text = "100"
        blobs = SubElement(root, "Blobs")
        for name in names:
            raw, etag = self.data.get(("control", name), (b"missing", '"missing"'))
            blob = SubElement(blobs, "Blob")
            SubElement(blob, "Name").text = name
            properties = SubElement(blob, "Properties")
            for key, value in {
                "Last-Modified": DATE, "Etag": etag, "Content-Length": str(len(raw)),
                "Content-Type": "application/json", "BlobType": "BlockBlob",
            }.items():
                SubElement(properties, key).text = value
        if marker is not None:
            SubElement(root, "NextMarker").text = marker
        return tostring(root)

    async def send(self, request, **kwargs):
        self.requests.append(request)
        # Yield to exercise reader-local, concurrent state separation.
        await asyncio.sleep(0)
        uri = urlsplit(request.url)
        query = parse_qs(uri.query, keep_blank_values=True)
        container, _, name = unquote(uri.path).lstrip("/").partition("/")
        if self.before_send:
            self.before_send(request, container, name, query)
        if query.get("comp") == ["list"]:
            prefix, marker = query["prefix"][0], query.get("marker", [""])[0]
            key = prefix, marker
            self.page_calls[key] = self.page_calls.get(key, 0) + 1
            if marker not in self.pages[prefix]:
                return Response(request, b"<Error><Code>InvalidMarker</Code></Error>", 400)
            names, next_marker = self.pages[prefix][marker]
            raw = self.list_xml(names, next_marker, prefix)
            if getattr(self, "wrong_prefix", False):
                raw = raw.replace(prefix.encode(), b"unowned-prefix/")
            if getattr(self, "truncate", False):
                raw = raw[:-8]
            return Response(request, raw, request_id=f"list-{len(self.requests)}")
        key = container, name
        self.read_counts[key] = self.read_counts.get(key, 0) + 1
        if key not in self.data:
            return Response(request, b"<Error><Code>BlobNotFound</Code></Error>", 404)
        raw, etag = self.data[key]
        headers = {key.lower(): value for key, value in request.headers.items()}
        if headers.get("if-match", etag) != etag:
            return Response(request, b"<Error><Code>ConditionNotMet</Code></Error>", 412, etag=etag)
        return Response(request, raw, 206, etag=etag, request_id=f"read-{len(self.requests)}")


def fixture(transport, scope=None):
    scope = scope or binding()
    content = Requirements(chunks=["private source bytes"])
    artifact = Artifact(
        artifact_type="requirements", scope_binding=scope, operation_id="a" * 32,
        producer=Producer(role="coordinator", name="coordinator", version="2",
                          session_id=scope.parent_session, response_id="owned-response"),
        input_refs=[], requirements_revision=1, content=content, content_sha256=digest(content),
    )
    ref = artifact.ref()
    # Preserve noncanonical private bytes, not a reserialized substitute.
    artifact_raw = b" \n" + artifact.model_dump_json(indent=2).encode() + b"\n"
    transport.put("control", ref.name, artifact_raw)
    operations = []
    effect = None
    for status in ("prepared", "dispatched", "unknown", "failed"):
        effect = Effect(operation_id="b" * 32, kind="call", role="architect",
                        status=status, input_refs=[ref], failure="private-failure" if status == "failed" else None)
        name = scope.prefix + f"operations/{effect.operation_id}/{status}.json"
        raw = canonical_bytes({
            "scope_binding": scope.model_dump(mode="json"),
            "effect": effect.model_dump(mode="json"),
        })
        transport.put("control", name, raw)
        operations.append(name)
    head = Manifest(
        scope_binding=scope, generation=7, turn=1, requirements=ref, accepted=[ref],
        active_response_id="owned-response", coordinator_version="2", effect=effect,
        status="SPECIALIST_INCOMPLETE",
    )
    transport.put("control", scope.prefix + "manifest.json", canonical_bytes(head), '"head"')
    transport.pages[scope.prefix + "operations/"] = {
        "": (operations[:2], "page-two"),
        "page-two": (operations[2:], "empty-page"),
        "empty-page": ([], ""),
    }
    return dict(scope=scope, head=head, head_etag='"head"', refs=[ref],
                quiescence_receipt="private-owned-quiescence-receipt",
                required_operations=operations)


class ScopedReaderTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.transport = Transport()
        self.options = fixture(self.transport)
        self.service = BlobServiceClient(
            "https://synthetic.blob.core.windows.net", credential=None,
            transport=self.transport, retry_total=0,
        )
        self.addAsyncCleanup(self.service.close)

    async def capture(self, **overrides):
        return await read_scoped_state(service=self.service, containers=CONTAINERS,
                                       **(self.options | overrides))

    def pages(self):
        return self.transport.pages[self.options["scope"].prefix + "operations/"]

    def head_name(self):
        return self.options["scope"].prefix + "manifest.json"

    async def test_complete_public_pagination_empty_terminal_and_exact_bytes(self):
        result = await self.capture()
        self.assertTrue(result.complete, result.issues)
        self.assertEqual(result.issues, ())
        self.assertEqual(len(result.pages), 6)
        self.assertEqual([p.next_cursor for p in result.pages[:3]], ["page-two", "empty-page", None])
        self.assertEqual({r.name for r in result.operations}, set(self.options["required_operations"]))
        self.assertEqual(len(result.operations), 4)  # never reduce to failed/latest
        self.assertEqual({json.loads(r.raw)["effect"]["status"] for r in result.operations},
                         {"prepared", "dispatched", "unknown", "failed"})
        self.assertFalse(hasattr(result, "sends"))  # journals never become boundary receipts
        for receipt in result.blobs:
            self.assertEqual(receipt.raw, self.transport.data[receipt.container, receipt.name][0])
            self.assertEqual(receipt.sha256, hashlib.sha256(receipt.raw).hexdigest())
            self.assertTrue(receipt.sources)
            self.assertIn("x-ms-request-id", dict(receipt.sources[0].headers))
        self.assertTrue(result.artifacts[0].raw.startswith(b" \n"))
        self.assertEqual(result.manifest.etag, '"head"')
        self.assertEqual(result.manifest.raw, result.manifest_recheck.raw)
        self.assertTrue(all(r.method == "GET" for r in self.transport.requests))
        self.assertFalse(self.transport.closed)  # caller retains lifecycle ownership

    async def test_exact_refs_in_all_three_containers(self):
        scope, head = self.options["scope"], self.options["head"]
        for role, content, operation in (
            ("architect", Candidate(requirements_revision=1, candidate_revision=1,
                                    design="private candidate"), "c" * 32),
            ("reviewer", Review(requirements_revision=1, candidate_revision=1, approved=True,
                               blocking_findings=[], unresolved_requirements=[],
                               recommendation="private review"), "d" * 32),
        ):
            value = Artifact(
                artifact_type=content.kind, scope_binding=scope, operation_id=operation,
                producer=Producer(role=role, name=role, version="2", session_id=role + "-child",
                                  response_id=role + "-response"),
                input_refs=list(head.accepted), requirements_revision=1, candidate_revision=1,
                content=content, content_sha256=digest(content),
            )
            ref = value.ref()
            self.transport.put(ref.container, ref.name, canonical_bytes(value))
            head.accepted.append(ref)
            setattr(head, ref.artifact_type, ref)
            head.candidate_revision = 1
        self.options["refs"] = list(head.accepted)
        self.transport.put("control", self.head_name(), canonical_bytes(head), '"head"')
        result = await self.capture()
        self.assertTrue(result.complete, result.issues)
        self.assertEqual({r.container for r in result.artifacts}, set(CONTAINERS))

    async def test_empty_operation_listing_is_valid_only_with_no_known_journal_head(self):
        head = self.options["head"].model_copy(update={"effect": None})
        self.transport.pages[self.options["scope"].prefix + "operations/"] = {"": ([], "")}
        self.transport.put("control", self.head_name(), canonical_bytes(head), '"head"')
        result = await self.capture(head=head, required_operations=())
        self.assertTrue(result.complete, result.issues)
        self.assertEqual(result.operations, ())
        self.assertEqual(len(result.pages), 2)

    async def test_changed_scope_prefix_in_response_cannot_broaden_next_request(self):
        self.transport.wrong_prefix = True
        result = await self.capture()
        self.assertFalse(result.complete)
        self.assertIn("LIST_PREFIX", result.issues)
        list_queries = [parse_qs(urlsplit(r.url).query) for r in self.transport.requests
                        if "comp=list" in r.url]
        self.assertEqual(len(list_queries), 2)
        self.assertTrue(all(q["prefix"] == [self.options["scope"].prefix + "operations/"]
                            for q in list_queries))

    async def test_omitted_cursor_is_not_sdk_terminal_success(self):
        names, _ = self.pages()[""]
        self.pages()[""] = names, None
        result = await self.capture()
        self.assertFalse(result.complete)
        self.assertIn("CURSOR_MISSING", result.issues)
        self.assertIn("OPERATION_GAP", result.issues)

    async def test_truncated_xml_retains_source_page_and_incomplete_window(self):
        self.transport.truncate = True
        with self.assertLogs("azure.core.pipeline.policies", level="WARNING"):
            result = await self.capture()
        self.assertFalse(result.complete)
        self.assertIn("LIST_READ", result.issues)
        self.assertTrue(result.pages)
        self.assertFalse(result.pages[0].raw.endswith(b"</EnumerationResults>"))

    async def test_truncated_cursor_keeps_page_and_service_failure_receipts(self):
        names, _ = self.pages()[""]
        self.pages()[""] = names, "page-tw"
        result = await self.capture()
        self.assertFalse(result.complete)
        self.assertIn("LIST_READ", result.issues)
        self.assertIn("OPERATION_GAP", result.issues)
        self.assertEqual(result.pages[0].next_cursor, "page-tw")
        self.assertTrue(any(p.source.status == 400 for p in result.pages))
        self.assertTrue(all(p.cursor == "page-tw" for p in result.pages if p.source.status == 400))

    async def test_repeated_cursor_terminates_without_deduplication_success(self):
        self.pages()["empty-page"] = [], "page-two"
        result = await self.capture()
        self.assertFalse(result.complete)
        self.assertIn("CURSOR_REPEATED", result.issues)
        self.assertEqual(len(result.pages), 6)

    async def test_duplicate_name_on_different_pages_is_incomplete(self):
        names, marker = self.pages()["page-two"]
        self.pages()["page-two"] = [self.pages()[""][0][0], *names], marker
        result = await self.capture()
        self.assertFalse(result.complete)
        self.assertIn("DUPLICATE_NAME", result.issues)
        self.assertEqual(len(result.operations), 5)  # retained, not silently collapsed

    async def test_explicit_terminal_with_known_missing_transition_is_incomplete(self):
        self.pages()["page-two"] = [], ""
        result = await self.capture()
        self.assertIn("OPERATION_GAP", result.issues)
        self.assertFalse(result.complete)

    async def test_head_transition_is_required_without_extra_name_anchors(self):
        self.pages()["page-two"] = [], ""
        result = await self.capture(required_operations=[])
        self.assertIn("OPERATION_GAP", result.issues)

    async def test_disappeared_blob_retains_404_read_receipt(self):
        name = self.options["required_operations"][0]

        def disappear(request, container, path, query):
            if path == name:
                self.transport.data.pop(("control", name), None)
        self.transport.before_send = disappear
        result = await self.capture()
        self.assertFalse(result.complete)
        self.assertIn("BLOB_READ", result.issues)
        self.assertTrue(any(s.status == 404 for r in result.reads for s in r.sources))

    async def test_changed_blob_rejected_by_listed_etag_condition(self):
        name = self.options["required_operations"][0]

        def change(request, container, path, query):
            if path == name:
                raw, _ = self.transport.data["control", name]
                self.transport.put("control", name, raw, '"changed"')
        self.transport.before_send = change
        result = await self.capture()
        self.assertFalse(result.complete)
        self.assertIn("BLOB_READ", result.issues)
        self.assertTrue(any(s.status == 412 for r in result.reads for s in r.sources))

    async def test_operation_disappearing_only_on_recheck_is_incomplete(self):
        name = self.options["required_operations"][0]

        def disappear(request, container, path, query):
            if path == name and self.transport.read_counts.get(("control", name)) == 1:
                self.transport.data.pop(("control", name), None)
        self.transport.before_send = disappear
        result = await self.capture()
        self.assertFalse(result.complete)
        self.assertIn("BLOB_READ", result.issues)
        self.assertTrue(any(r.name == name for r in result.operations))
        self.assertTrue(any(s.status == 404 for r in result.reads if r.phase == "after"
                            for s in r.sources))

    async def test_same_etag_changed_bytes_rejected_on_immutable_recheck(self):
        name = self.options["refs"][0].name

        def change(request, container, path, query):
            if path == name and self.transport.read_counts.get(("control", name)) == 1:
                raw, etag = self.transport.data["control", name]
                self.transport.put("control", name, raw + b"\n", etag)
        self.transport.before_send = change
        result = await self.capture()
        self.assertFalse(result.complete)
        self.assertIn("IMMUTABLE_MOVED", result.issues)
        observations = [r for r in result.blobs if r.name == name]
        self.assertNotEqual(observations[0].raw, observations[1].raw)

    async def test_cross_scope_listed_name_is_never_downloaded(self):
        name = binding("other-parent").prefix + "operations/" + "c" * 32 + "/prepared.json"
        self.pages()["empty-page"] = [name], ""
        result = await self.capture()
        self.assertFalse(result.complete)
        self.assertIn("OPERATION_SCOPE", result.issues)
        self.assertNotIn(("control", name), self.transport.read_counts)

    async def test_cross_scope_operation_body_rejected_without_losing_bytes(self):
        name = self.options["required_operations"][0]
        raw, etag = self.transport.data["control", name]
        value = json.loads(raw)
        value["scope_binding"] = binding("other-parent").model_dump(mode="json")
        self.transport.put("control", name, canonical_bytes(value), etag)
        result = await self.capture()
        self.assertIn("OPERATION_BINDING", result.issues)
        self.assertFalse(result.complete)
        self.assertIn(canonical_bytes(value), [r.raw for r in result.operations])

    async def test_filename_status_mismatch_is_not_a_valid_transition(self):
        name = self.options["required_operations"][0]
        raw, etag = self.transport.data["control", name]
        value = json.loads(raw)
        value["effect"]["status"] = "accepted"
        self.transport.put("control", name, canonical_bytes(value), etag)
        result = await self.capture()
        self.assertIn("OPERATION_BINDING", result.issues)
        self.assertFalse(result.complete)

    async def test_attributed_head_generation_and_response_are_rechecked(self):
        for field, value in (("generation", 8), ("active_response_id", "unowned-response")):
            with self.subTest(field=field):
                raw, etag = self.transport.data["control", self.head_name()]
                changed = json.loads(raw)
                changed[field] = value
                self.transport.put("control", self.head_name(), canonical_bytes(changed), etag)
                result = await self.capture()
                self.assertIn("MANIFEST_MOVED", result.issues)
                self.assertFalse(result.complete)
                self.transport.put("control", self.head_name(), raw, etag)

    async def test_head_movement_during_window_invalidates_capture(self):
        name = self.head_name()

        def change(request, container, path, query):
            if path == name and self.transport.read_counts.get(("control", name)) == 1:
                raw, _ = self.transport.data["control", name]
                self.transport.put("control", name, raw, '"new-head"')
        self.transport.before_send = change
        result = await self.capture()
        self.assertFalse(result.complete)
        self.assertIn("BLOB_READ", result.issues)
        self.assertIsNone(result.manifest_recheck)

    async def test_list_changes_between_enumerations_are_incomplete(self):
        prefix = self.options["scope"].prefix + "operations/"

        def change(request, container, path, query):
            if (
                query.get("prefix") == [prefix] and not query.get("marker", [""])[0]
                and self.transport.page_calls.get((prefix, "")) == 1
            ):
                self.pages()["page-two"] = [], ""
        self.transport.before_send = change
        result = await self.capture()
        self.assertFalse(result.complete)
        self.assertIn("LIST_MOVED", result.issues)

    async def test_invalid_caller_binding_performs_no_requests(self):
        for overrides in (
            {"scope": binding("other-parent")}, {"refs": []},
            {"head_etag": ""}, {"quiescence_receipt": ""},
            {"required_operations": [binding("other-parent").prefix + "operations/x/failed.json"]},
        ):
            with self.subTest(keys=list(overrides)):
                with self.assertRaises(ValueError):
                    await self.capture(**overrides)
        self.assertEqual(self.transport.requests, [])

    async def test_corrupt_artifact_and_duplicate_json_are_incomplete(self):
        name = self.options["refs"][0].name
        self.transport.put("control", name, b'{"scope_binding":{},"scope_binding":{}}')
        result = await self.capture()
        self.assertFalse(result.complete)
        self.assertIn("ARTIFACT_INVALID", result.issues)
        self.assertEqual(result.artifacts[0].raw, b'{"scope_binding":{},"scope_binding":{}}')

    async def test_valid_but_wrong_artifact_hash_is_incomplete(self):
        name = self.options["refs"][0].name
        raw, etag = self.transport.data["control", name]
        value = json.loads(raw)
        value["content"]["chunks"][0] = "altered private source"
        value["content_sha256"] = digest(value["content"])
        self.transport.put("control", name, canonical_bytes(value), etag)
        result = await self.capture()
        self.assertFalse(result.complete)
        self.assertIn("ARTIFACT_INTEGRITY", result.issues)

    async def test_oversized_blob_fails_bounded_capture(self):
        name = self.options["refs"][0].name
        self.transport.put("control", name, b"x" * (MAX_DOCUMENT_BYTES + 1))
        result = await self.capture()
        self.assertFalse(result.complete)
        self.assertIn("BLOB_SIZE", result.issues)
        self.assertFalse(any(r.name == name for r in result.blobs))

    async def test_source_exceptions_do_not_leak_private_messages_or_look_complete(self):
        def failure(*args):
            raise RuntimeError("private-token-and-scope-secret")
        self.transport.before_send = failure
        output, errors = io.StringIO(), io.StringIO()
        with redirect_stdout(output), redirect_stderr(errors):
            result = await self.capture()
        self.assertFalse(result.complete)
        self.assertIn("LIST_READ", result.issues)
        self.assertIn("BLOB_READ", result.issues)
        self.assertEqual(output.getvalue() + errors.getvalue(), "")
        self.assertNotIn("private-token", repr(result.issues))

    async def test_head_effect_body_must_match_the_attributed_head(self):
        name = self.options["required_operations"][-1]
        raw, etag = self.transport.data["control", name]
        value = json.loads(raw)
        value["effect"]["failure"] = "different-private-failure"
        self.transport.put("control", name, canonical_bytes(value), etag)
        result = await self.capture()
        self.assertFalse(result.complete)
        self.assertIn("HEAD_EFFECT_MISMATCH", result.issues)

    async def test_cancellation_propagates_not_a_complete_partial_result(self):
        def cancel(*args):
            raise asyncio.CancelledError()
        self.transport.before_send = cancel
        with self.assertRaises(asyncio.CancelledError):
            await self.capture()

    async def test_concurrent_scope_and_client_lifecycle_isolation(self):
        other = fixture(self.transport, binding("other-parent"))
        first, second = await asyncio.gather(self.capture(), self.capture(**other))
        self.assertTrue(first.complete, first.issues)
        self.assertTrue(second.complete, second.issues)
        self.assertTrue(set(r.name for r in first.blobs).isdisjoint(r.name for r in second.blobs))
        for result, options in ((first, self.options), (second, other)):
            self.assertTrue(all(r.name.startswith(options["scope"].prefix) for r in result.blobs))
        self.assertFalse(self.transport.closed)

    async def test_private_capture_never_changes_stdout_or_leaks_through_repr(self):
        output, errors = io.StringIO(), io.StringIO()
        with redirect_stdout(output), redirect_stderr(errors):
            result = await self.capture()
        self.assertEqual(output.getvalue(), "")
        self.assertEqual(errors.getvalue(), "")
        rendered = repr(result) + repr(result.blobs) + repr(result.pages) + repr(result.reads)
        for private in ("private-principal", "private-parent", "private source", "scope_binding",
                        "synthetic-secret-header", self.options["scope"].prefix):
            self.assertNotIn(private, rendered)
        for receipt in result.blobs:
            for source in receipt.sources:
                self.assertNotIn("authorization", dict(source.headers))


if __name__ == "__main__":
    unittest.main()
