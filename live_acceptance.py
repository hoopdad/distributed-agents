from __future__ import annotations

import argparse
import asyncio
from contextlib import redirect_stdout
import hashlib
import io
import json
import math
import re
import uuid
from types import SimpleNamespace
from urllib.parse import quote

from demo.contracts import AGENTS, PROJECT, Candidate, Review, alias
from demo.foundry import ProjectClient, data_client
from demo import effect_observation as effects
from demo.terminal import chat, private_state_path, rest, session_lease, verify_lab, write_state
from azure.identity.aio import AzureCliCredential

from agent_metadata import agent_metadata
from demo.artifacts import (
    Artifact, ArtifactRef, Candidate as ArtifactCandidate, Decision, Effect, Manifest,
    Review as ArtifactReview,
)
from demo.workflow import PREPARATION_CHECKS


SCENARIOS = {
    "initial": "Create and review a synthetic architecture for Project Harbor. "
               "All application ingress must remain private: no public application ingress. "
               "Use the curated lab fact sheet and do not operate on Azure resources.",
    "followup": "For the same Project Harbor design, add an asynchronous queue between document "
                "submission and processing. Preserve every earlier requirement, especially private "
                "application ingress. Have both specialists revise and review their previous work.",
    "isolated": "Create and review a separate synthetic architecture for Project Cedar. "
                "All application ingress must remain private: no public application ingress. "
                "Use managed identities and private TLS endpoints, preserve the curated lab constraints, "
                "and do not operate on Azure resources. This conversation has no Project Harbor requirements.",
}
SCENARIOS["restart"] = (
    "Continue the same synthetic Project Harbor design after hosting compute resumes. "
    "Preserve all earlier requirements, including private ingress and the asynchronous queue. "
    "Have both specialists revise and review their existing work; do not operate on Azure resources."
)


def host_log_message(line):
    if line.startswith("{"):
        try:
            value = json.loads(line)
        except ValueError:
            return None
        if not isinstance(value, dict) or not isinstance(value.get("message"), str):
            return None
        line = value["message"]
    return line


def ingress_identity(line, response_id):
    """Return only SDK ingress-presence flags for the exact observed response."""
    line = host_log_message(line)
    if line is None or not response_id:
        return None
    match = re.search(
        r"Creating response " + re.escape(response_id)
        + r": [^\r\n]*has_user_id=(True|False) has_call_id=(True|False)$", line,
    )
    if match:
        return {"has_user_id": match[1] == "True", "has_call_id": match[2] == "True"}
    return None


def outbound_identity(line, response_id):
    """Expose only exact-response-bound HTTP-edge context flags."""
    line = host_log_message(line)
    if line is None or not response_id:
        return None
    binding = hashlib.sha256(response_id.encode()).hexdigest()
    match = re.search(
        r"Native outbound context response_binding=" + binding
        + r" role=(coordinator|architect|reviewer) has_call_id=(True|False)"
        r" call_matches_context=(True|False) has_delegated_user=(True|False)"
        r" has_container_user=(True|False)\.$", line,
    )
    if match:
        return {
            "role": match[1], "has_call_id": match[2] == "True",
            "call_matches_context": match[3] == "True",
            "has_delegated_user": match[4] == "True", "has_container_user": match[5] == "True",
        }
    return None


def workflow_failure(line):
    """Expose only the SDK's fixed phase/type diagnostic, never arbitrary host logs."""
    line = host_log_message(line)
    if line is None:
        return None
    check = re.search(r"Native workflow preparation rejected \(([A-Z][A-Z0-9_]{0,63})\)\.$", line)
    if check and check[1] in PREPARATION_CHECKS:
        return {"phase": "preparation", "exception_type": "ArtifactError", "check": check[1]}
    match = re.search(
        r"Native Responses workflow failed during "
        r"(preparation|scoped continuation|input parsing|input validation|execution|final output persistence) "
        r"\((ArtifactError|ValueError|TypeError|RuntimeError|ConfigurationError|ValidationError)\)\.$",
        line,
    )
    return {"phase": match[1], "exception_type": match[2]} if match else None


def project_profile_event(text: str, role: str) -> dict | None:
    """Closed private emitter schema, not raw logs or an authenticated join.

    The logstream URL binds a hosted session/version. Local observation UUIDs
    do not independently bind a response, operation or authenticated user.
    """
    from demo import diagnostics as d

    if type(text) is not str or len(text) > 8192:
        return None
    try:
        value = json.loads(text)
        if type(value) is dict and type(value.get("message")) is str:
            value = json.loads(value["message"])
        if type(value) is not dict or type(value.get("schema_version")) is not int:
            return None
        if value["schema_version"] != 1 or value.get("role") != role:
            return None
        fields = {name: cls(value[name]) for name, cls in (
            ("role", d.Role), ("stage", d.Stage), ("kind", d.Kind),
            ("method", d.Method), ("route", d.Route), ("category", d.Category),
            ("scope_request_match", d.Match),
        )}
        for name in ("status", "duration_ms"):
            if name in value:
                fields[name] = value[name]
        if "binding" in value:
            fields["binding"] = d.Binding(**{
                name: uuid.UUID(item) for name, item in value["binding"].items()
            })
        for name in ("delegation", "platform", "call", "scope_user", "request_user"):
            if name in value:
                slot = value[name]
                fields[name] = d.Observation(
                    d.Coverage(slot["coverage"]),
                    d.Presence(slot["presence"]) if "presence" in slot else None,
                )
        result = d.event_fields(d.Event(**fields))
        if result != value or len(json.dumps(result)) > 4096:
            return None
        return result
    except (ValueError, TypeError, KeyError, AttributeError, OverflowError):
        return None


async def observe_host_failure(http, credential, hosted_id, version, *, role="coordinator", response_id=None,
                               structured=False):
    token = await credential.get_token("https://ai.azure.com/.default")
    path = (
        f"/agents/{quote(AGENTS[role], safe='')}/versions/{quote(version, safe='')}"
        f"/sessions/{quote(hosted_id, safe='')}:logstream"
    )
    diagnostics = {"failures": [], "limit": None}
    if structured:
        diagnostics["structured_profiles"] = []
        diagnostics["structured_scope"] = "exact hosted session/version; local aliases not independently joined to response"
    # The pinned SDK's log API is a never-ending SSE stream. Bound both time and bytes.
    deadline = asyncio.timeout(30)
    try:
        async with deadline, http.stream(
            "GET", PROJECT + path, params={"api-version": "v1"},
            headers={"Authorization": "Bearer " + token.token, "Accept": "text/event-stream"},
        ) as response:
            if response.status_code != 200:
                raise RuntimeError(f"HOST_LOG_HTTP_{response.status_code}")
            if not response.headers.get("content-type", "").startswith("text/event-stream"):
                raise RuntimeError("HOST_LOG_SSE_REQUIRED")
            size = 0
            pending = b""
            async for chunk in response.aiter_bytes():
                size += len(chunk)
                if size > (2097152 if structured else 131072):
                    diagnostics["limit"] = "bytes"
                    break
                pending += chunk
                while b"\n" in pending:
                    line, pending = pending.split(b"\n", 1)
                    if line.startswith(b"data:"):
                        text = line[5:].strip().decode("utf-8")
                        if structured:
                            event = project_profile_event(text, role)
                            if event is not None:
                                if len(diagnostics["structured_profiles"]) >= 512:
                                    diagnostics["limit"] = "records"
                                    return diagnostics
                                # Preserve occurrences; repetition is not deduplicated.
                                diagnostics["structured_profiles"].append(event)
                        identity = ingress_identity(text, response_id)
                        if identity is not None:
                            observations = diagnostics.setdefault("ingress_identity", [])
                            if identity not in observations:
                                observations.append(identity)
                        outbound = outbound_identity(text, response_id)
                        if outbound is not None:
                            observations = diagnostics.setdefault("outbound_context", [])
                            if outbound not in observations:
                                observations.append(outbound)
                        failure = workflow_failure(text)
                        if failure is not None and failure not in diagnostics["failures"]:
                            diagnostics["failures"].append(failure)
                        for code in storage_codes(text):
                            codes = diagnostics.setdefault("storage_codes", [])
                            if code not in codes:
                                codes.append(code)
    except TimeoutError:
        if not deadline.expired():
            raise
        diagnostics["limit"] = "time"
    return diagnostics


def storage_codes(text):
    codes = [code for code in (
        "AuthorizationPermissionMismatch", "AuthorizationFailure", "AuthenticationFailed",
        "BlobNotFound", "ContainerNotFound", "ResourceNotFoundError", "HttpResponseError",
        "FoundryStorageError", "FoundryStorageConflictError", "FoundryStoragePreconditionError",
        "STORAGE_CONTEXT", "ManagedIdentityCredential", "CredentialUnavailableError",
    ) if re.search(r"\b" + code + r"\b", text)]
    for message, code in {
        "Foundry hosted requests require a trusted user ID and call ID.": "NATIVE_HOST_TRUSTED_USER_AND_CALL",
        "Foundry hosted requests require a platform FOUNDRY_AGENT_SESSION_ID.": "NATIVE_HOST_PLATFORM_SESSION",
        "The request agent_session_id does not match the platform session ID.": "NATIVE_HOST_SESSION_MISMATCH",
        "Native hosting requires a freshly built, unrun workflow.": "NATIVE_HOST_FRESH_WORKFLOW",
        "Native hosting owns checkpoint storage; build the workflow without a store.": "NATIVE_HOST_CHECKPOINT_OWNER",
    }.items():
        if message in text:
            codes.append(code)
    return codes


async def stop_hosting_for_acceptance(http, credential, state, path):
    if state.get("runtime") != "native" or state.get("bound") is not True or state.get("pending"):
        raise RuntimeError("COMPLETED_NATIVE_PARENT_REQUIRED")
    hosted_id = state["framework"]["state"]["foundry_hosted_agent_session_id"]
    locator = f"/agents/{AGENTS['coordinator']}/endpoint/sessions/{quote(hosted_id, safe='')}"
    before = await rest(http, credential, "GET", locator)
    if (before.get("agent_session_id") != hosted_id
            or before.get("version_indicator", {}).get("agent_version") != state["version"]):
        raise RuntimeError("RESTART_PARENT_BINDING")
    journal_path = private_state_path(str(path) + ".hosting-restart.json")
    if journal_path.exists():
        journal = json.loads(journal_path.read_text())
        if journal.get("parent") != hosted_id or journal.get("version") != state["version"]:
            raise RuntimeError("RESTART_JOURNAL_BINDING")
        if journal.get("phase") != "stop_pending":
            raise RuntimeError("RESTART_ALREADY_ATTEMPTED")
        # An uncertain stop is observed, never sent again.
    else:
        if before["status"] != "active":
            raise RuntimeError("ACTIVE_COMPUTE_REQUIRED_FOR_RESTART_TEST")
        journal = {
            "schema_version": 1, "parent": hosted_id, "version": state["version"],
            "phase": "stop_pending", "previous_stopped_at": before.get("stopped_at"),
            "operation_id": uuid.uuid4().hex,
        }
        write_state(journal_path, journal, new=True)
        token = await credential.get_token("https://ai.azure.com/.default")
        with effects.dispatch(effects.Binding(
            journal["operation_id"], "coordinator", hosted_id, state["version"], "stop",
        )):
            response = await http.request(
                "POST", PROJECT + locator + ":stop", params={"api-version": "v1"},
                headers={"Authorization": "Bearer " + token.token},
            )
        if response.status_code != 204:
            raise RuntimeError(f"HOST_STOP_HTTP_{response.status_code}")
        journal["stop_http_status"] = 204
        write_state(journal_path, journal)
    async with asyncio.timeout(120):
        while True:
            observed = await rest(http, credential, "GET", locator)
            if (observed.get("agent_session_id") != hosted_id
                    or observed.get("version_indicator", {}).get("agent_version") != state["version"]):
                raise RuntimeError("RESTART_PARENT_BINDING")
            stopped = observed.get("stopped_at")
            previous = journal["previous_stopped_at"]
            if (observed["status"] == "idle" and type(stopped) in (int, float)
                    and math.isfinite(stopped) and stopped > 0
                    and (previous is None or stopped > previous)):
                journal.update(phase="stop_confirmed", stopped_at=stopped)
                write_state(journal_path, journal)
                return journal
            if observed["status"] in ("failed", "expired", "deleted", "deleting"):
                raise RuntimeError("RESTART_SESSION_UNAVAILABLE")
            await asyncio.sleep(1)


def events(text):
    records = [json.loads(line) for line in text.splitlines() if line.startswith("{")]
    results = [record for record in records if record.get("event") == "result"]
    if len(results) != 1 or results[0].get("status") != "ACCEPTED_ADVISORY":
        raise RuntimeError(f"LIVE_TURN_NOT_ACCEPTED: {results}")
    calls = [record for record in records if record.get("event") == "delegation"]
    if {record["role"] for record in calls} != {"architect", "reviewer"}:
        raise RuntimeError("BOTH_SPECIALISTS_REQUIRED")
    if not 2 <= len(calls) <= 6:
        raise RuntimeError("LIVE_DELEGATION_BOUND")
    if any(call.get("status") != "completed" for call in calls):
        raise RuntimeError("LIVE_DELEGATION_INCOMPLETE")
    result = results[0]
    workflow_mode = result.get("native_workflow") == "distributed-agents-v1"
    turn, decisions = result.get("turn"), result.get("decisions")
    if (type(turn) is not int or turn < 1 or type(result.get("calls")) is not int or
            result.get("calls") != len(calls) or
            type(decisions) is not int or not len(calls) + (not workflow_mode) <= decisions <= 10):
        raise RuntimeError("LIVE_RESULT_COUNTERS")
    if workflow_mode:
        if result.get("pending_effect") is not None or result.get("specialists") != "hosted":
            raise RuntimeError("NATIVE_REMOTE_EFFECT_HOLD")
        if (result.get("artifact_authentication") != "managed_identity"
                or result.get("artifact_private_path_verified") is not True):
            raise RuntimeError("NATIVE_PRIVATE_MI_PATH_REQUIRED")
        refs = result.get("artifact_refs")
        if not isinstance(refs, dict) or set(refs) != {"requirements", "candidate", "review"}:
            raise RuntimeError("NATIVE_ARTIFACT_REFS_REQUIRED")
        for kind, value in refs.items():
            ref = ArtifactRef.model_validate(value)
            if ref.artifact_type != kind or ref.requirements_revision != turn:
                raise RuntimeError("NATIVE_ARTIFACT_REVISION")
        decision_refs = result.get("decision_refs")
        if not isinstance(decision_refs, list) or len(decision_refs) != decisions:
            raise RuntimeError("NATIVE_DECISION_RECORDS_REQUIRED")
        for value in decision_refs:
            ref = ArtifactRef.model_validate(value)
            if ref.artifact_type != "decision" or ref.requirements_revision != turn:
                raise RuntimeError("NATIVE_DECISION_RECORD_TYPE")
        evidence = result.get("decision_evidence")
        if not isinstance(evidence, list) or len(evidence) != decisions:
            raise RuntimeError("NATIVE_DECISION_EVIDENCE_REQUIRED")
        for value, call in zip(evidence, calls, strict=True):
            decision = Decision.model_validate(value)
            if decision.gated_action != call["action"] or decision.model != "Microsoft-Decision-1":
                raise RuntimeError("NATIVE_DECISION_DELEGATION_BINDING")
        validate_artifact_evidence(result)
        if any(call.get("specialist_mode") != "hosted" for call in calls):
            raise RuntimeError("REMOTE_SPECIALISTS_REQUIRED")
    try:
        candidate = (ArtifactCandidate if workflow_mode else Candidate).model_validate(result.get("candidate"))
        review = (ArtifactReview if workflow_mode else Review).model_validate(result.get("review"))
    except ValueError as exc:
        raise RuntimeError("LIVE_ARTIFACT_SCHEMA") from exc
    if (candidate.requirements_revision != turn or review.requirements_revision != turn or
            candidate.candidate_revision != review.candidate_revision):
        raise RuntimeError("LIVE_ARTIFACT_REVISION")
    if not review.approved:
        raise RuntimeError("LIVE_REVIEW_NOT_APPROVED")
    return {"result": result, "delegations": calls}


def validate_artifact_evidence(result):
    evidence = result.get("artifact_evidence")
    if not isinstance(evidence, dict) or set(evidence) != {"requirements", "candidate", "review"}:
        raise RuntimeError("NATIVE_ARTIFACT_EVIDENCE_REQUIRED")
    artifacts = {kind: Artifact.model_validate(value) for kind, value in evidence.items()}
    scope = artifacts["requirements"].scope_binding
    for kind, artifact in artifacts.items():
        ref = ArtifactRef.model_validate(result["artifact_refs"][kind])
        role = {"requirements": "coordinator", "candidate": "architect", "review": "reviewer"}[kind]
        if (artifact.ref() != ref or artifact.scope_binding != scope or artifact.artifact_type != kind
                or artifact.producer.role != role or artifact.producer.name != AGENTS[role]):
            raise RuntimeError("NATIVE_ARTIFACT_PROVENANCE")
        for prerequisite in artifact.input_refs:
            prerequisite.assert_scope(scope)
    if (artifacts["requirements"].input_refs
            or not artifacts["candidate"].input_refs
            or artifacts["candidate"].input_refs[0] != artifacts["requirements"].ref()
            or artifacts["review"].input_refs != [
                artifacts["requirements"].ref(), artifacts["candidate"].ref(),
            ]):
        raise RuntimeError("NATIVE_EXACT_PREREQUISITES")
    for kind in ("candidate", "review"):
        if artifacts[kind].content.model_dump(mode="json", exclude={"kind"}) != result[kind]:
            raise RuntimeError("NATIVE_ACCEPTED_CONTENT_CHANGED")
    decisions = result.get("decision_artifacts")
    if not isinstance(decisions, list) or len(decisions) != len(result["decision_refs"]):
        raise RuntimeError("NATIVE_DECISION_PROVENANCE")
    for value, ref, content in zip(
        decisions, result["decision_refs"], result["decision_evidence"], strict=True,
    ):
        artifact = Artifact.model_validate(value)
        if (artifact.ref() != ArtifactRef.model_validate(ref) or artifact.scope_binding != scope
                or artifact.producer.role != "coordinator"
                or artifact.producer.name != AGENTS["coordinator"]
                or artifact.content.model_dump(mode="json") != content):
            raise RuntimeError("NATIVE_DECISION_PROVENANCE")
        for prerequisite in artifact.input_refs:
            prerequisite.assert_scope(scope)
    return artifacts


def validate_exercised_versions(parent_version, metadata, delegations, children):
    if parent_version != metadata["coordinator"]["version"]:
        raise RuntimeError("EXERCISED_COORDINATOR_PACKAGE_VERSION")
    for role in ("architect", "reviewer"):
        child_version = children[role].get("version_indicator", {}).get("agent_version")
        expected = metadata[role]["version"]
        role_events = [event for event in delegations if event["role"] == role]
        if not role_events or child_version != expected or any(
            event.get("version") != expected for event in role_events
        ):
            raise RuntimeError("EXERCISED_SPECIALIST_PACKAGE_VERSION")


def _require(condition, code):
    if not condition:
        raise RuntimeError(code)


def _evidence_turn(snapshot):
    """Validate private observations, not aliases or a caller's PASS flags."""
    proof = snapshot["proof"]
    parsed = events("\n".join(json.dumps(item) for item in [
        *proof["delegations"], proof["result"],
    ]))
    result = parsed["result"]
    _require(result.get("native_workflow") == "distributed-agents-v1", "EVIDENCE_NATIVE_REQUIRED")
    artifacts = validate_artifact_evidence(result)
    manifest = Manifest.model_validate(snapshot["manifest"])
    scope = manifest.scope_binding
    framework = proof["framework"]
    parent = framework["state"]["foundry_hosted_agent_session_id"]
    _require(
        scope == artifacts["requirements"].scope_binding and scope.parent_session == parent
        and bool(framework["session_id"]) and manifest.turn == result["turn"]
        and manifest.status == "ACCEPTED_ADVISORY"
        and manifest.coordinator_version == proof["version"]
        and bool(manifest.active_response_id)
        and (manifest.effect is None or manifest.effect.status == "accepted")
        and set(manifest.children) == {"architect", "reviewer"},
        "EVIDENCE_MANIFEST_BINDING",
    )
    validate_exercised_versions(
        proof["version"], proof["metadata"], parsed["delegations"], proof["child_sessions"],
    )
    bindings = {}
    for kind in ("requirements", "candidate", "review"):
        _require(getattr(manifest, kind) == artifacts[kind].ref(), "EVIDENCE_CURRENT_ACCEPTANCE")
    producer = artifacts["requirements"].producer
    _require(producer.session_id == parent and producer.version == proof["version"],
             "EVIDENCE_PARENT_PRODUCER")
    for role, kind in (("architect", "candidate"), ("reviewer", "review")):
        child = manifest.children[role]
        identity = child.framework
        producer = artifacts[kind].producer
        _require(
            child.bound and child.role == role and child.name == AGENTS[role]
            and bool(identity["session_id"])
            and identity["state"]["foundry_hosted_agent_session_id"] == child.hosted_id
            and proof["child_sessions"][role]["agent_session_id"] == child.hosted_id
            and producer.session_id == child.hosted_id and producer.version == child.version,
            "EVIDENCE_CHILD_BINDING",
        )
        bindings[role] = (child.hosted_id, identity["session_id"], child.version)
    _require(len({value[0] for value in bindings.values()}) == 2
             and len({value[1] for value in bindings.values()}) == 2, "EVIDENCE_DISTINCT_CHILDREN")

    # Immutable operation transition documents are cumulative within this parent.
    # Separate request captures count actual boundary sends, not journal intentions.
    operations = {}
    for record in snapshot["operations"]:
        _require(record["scope_binding"] == scope.model_dump(mode="json"), "EVIDENCE_OPERATION_SCOPE")
        effect = Effect.model_validate(record["effect"])
        transitions = operations.setdefault(effect.operation_id, {})
        _require(effect.status not in transitions, "EVIDENCE_DUPLICATE_TRANSITION")
        transitions[effect.status] = effect
    _require(bool(operations), "EVIDENCE_OPERATIONS_REQUIRED")
    calls, creates = {}, {}
    for operation, transitions in operations.items():
        accepted = transitions.get("accepted")
        _require(accepted is not None and not ({"unknown", "failed"} & transitions.keys()),
                 "EVIDENCE_UNRECONCILED_EFFECT")
        _require("prepared" in transitions, "EVIDENCE_INTENT_REQUIRED")
        for value in transitions.values():
            _require(
                (value.kind, value.role, value.input_refs) ==
                (accepted.kind, accepted.role, accepted.input_refs),
                "EVIDENCE_EFFECT_CHANGED",
            )
            _require(value.response_id in (None, accepted.response_id), "EVIDENCE_RESPONSE_CHANGED")
        if accepted.kind in ("create", "call"):
            _require("dispatched" in transitions, "EVIDENCE_DISPATCH_REQUIRED")
            _require(accepted.role in bindings, "EVIDENCE_EFFECT_ROLE")
        if accepted.kind == "create":
            creates[operation] = accepted
        elif accepted.kind == "call":
            _require(bool(accepted.response_id) and accepted.output_ref in manifest.accepted
                     and accepted.input_refs, "EVIDENCE_CALL_ACCEPTANCE")
            accepted.output_ref.assert_scope(scope)
            for ref in accepted.input_refs:
                ref.assert_scope(scope)
                _require(ref in manifest.accepted
                         and ref.requirements_revision == accepted.output_ref.requirements_revision,
                         "EVIDENCE_CALL_PREREQUISITES")
            _require(accepted.output_ref.artifact_type == {
                "architect": "candidate", "reviewer": "review",
            }[accepted.role], "EVIDENCE_CALL_ROLE")
            calls[operation] = accepted
    for field, expected in (("creations", creates), ("sends", calls)):
        observed = snapshot[field]
        _require(isinstance(observed, list) and all(isinstance(item, str) for item in observed)
                 and len(observed) == len(set(observed)) and set(observed) == set(expected),
                 "EVIDENCE_REQUEST_ACCOUNTING")
    _require(len(creates) == 2 and {item.role for item in creates.values()} == set(bindings),
             "EVIDENCE_EXACTLY_TWO_CREATIONS")
    _require(len({item.response_id for item in calls.values()}) == len(calls),
             "EVIDENCE_FRESH_RESPONSES")
    current = {
        operation: effect for operation, effect in calls.items()
        if effect.output_ref.requirements_revision == manifest.turn
    }
    _require(len(current) == len(parsed["delegations"]), "EVIDENCE_INVOCATION_COUNT")
    _require(len({json.dumps(event["artifact_ref"], sort_keys=True)
                  for event in parsed["delegations"]}) == len(current),
             "EVIDENCE_DUPLICATE_DELEGATION")
    for effect in current.values():
        _require(effect.input_refs[0] == manifest.requirements, "EVIDENCE_CALL_PREREQUISITES")
    for event in parsed["delegations"]:
        ref = ArtifactRef.model_validate(event["artifact_ref"])
        matches = [effect for effect in current.values() if effect.output_ref == ref]
        _require(len(matches) == 1, "EVIDENCE_DELEGATION_OPERATION")
        effect = matches[0]
        child = manifest.children[effect.role]
        _require(
            event["role"] == effect.role and event["hosted_session"] == alias(child.hosted_id)
            and event["framework_session"] == alias(child.framework["session_id"])
            and event["version"] == child.version and event["response"] == alias(effect.response_id),
            "EVIDENCE_DELEGATION_BINDING",
        )
    for role, kind in (("architect", "candidate"), ("reviewer", "review")):
        artifact = artifacts[kind]
        matches = [
            effect for effect in current.values()
            if effect.role == role and effect.output_ref == artifact.ref()
            and effect.response_id == artifact.producer.response_id
        ]
        _require(len(matches) == 1, "EVIDENCE_OUTPUT_RESPONSE")
        _require(matches[0].input_refs == artifact.input_refs, "EVIDENCE_OUTPUT_PREREQUISITES")
    return manifest, artifacts, bindings, operations, current


def _evidence_continuation(before, after):
    old = _evidence_turn(before)
    new = _evidence_turn(after)
    prior, current = old[0], new[0]
    _require(
        prior.scope_binding == current.scope_binding and old[2] == new[2]
        and before["proof"]["framework"]["session_id"] == after["proof"]["framework"]["session_id"]
        and prior.coordinator_version == current.coordinator_version
        and prior.active_response_id != current.active_response_id
        and current.turn == prior.turn + 1 and current.generation > prior.generation,
        "EVIDENCE_CONTINUITY",
    )
    for operation, transitions in old[3].items():
        _require(operation in new[3] and transitions == new[3][operation], "EVIDENCE_JOURNAL_CHANGED")
    _require(set(before["creations"]) == set(after["creations"]), "EVIDENCE_EXTRA_CREATION")
    _require(
        set(after["sends"]) - set(before["sends"]) == set(new[4])
        and len(after["sends"]) == len(before["sends"]) + len(new[4]),
        "EVIDENCE_DUPLICATE_OR_MISSING_SEND",
    )
    previous_chunks = old[1]["requirements"].content.chunks
    chunks = new[1]["requirements"].content.chunks
    _require(chunks[:len(previous_chunks)] == previous_chunks and len(chunks) > len(previous_chunks),
             "EVIDENCE_UPDATED_REQUIREMENTS")
    _require(
        prior.candidate != current.candidate and prior.review != current.review
        and all(ref.requirements_revision == current.turn for ref in (
            current.requirements, current.candidate, current.review,
        )),
        "EVIDENCE_STALE_APPROVAL",
    )
    return old, new


def validate_scenario_evidence(*, initial, followup, restart, isolated, stopped_session):
    """Offline assertions over existing private scenario/manifest/journal captures.

    See docs/design.md for the input contract and executable local invocation.
    No network, new output fields, persistent comparison ledger or retry occurs.
    Success validates supplied observations; it does not authenticate their source.
    """
    try:
        _require(
            [item["proof"]["scenario"] for item in (initial, followup, restart, isolated)]
            == ["initial", "followup", "restart", "isolated"], "EVIDENCE_SCENARIOS",
        )
        first, second = _evidence_continuation(initial, followup)
        _, resumed = _evidence_continuation(followup, restart)
        separate = _evidence_turn(isolated)
        _require(len({item[0].active_response_id for item in (first, second, resumed)}) == 3,
                 "EVIDENCE_PARENT_RESPONSE_REUSE")
        _require(first[0].turn == separate[0].turn == 1, "EVIDENCE_INITIAL_TURN")
        chunks = second[1]["requirements"].content.chunks
        _require(SCENARIOS["initial"] in chunks and SCENARIOS["followup"] in chunks,
                 "EVIDENCE_SYNTHETIC_REQUIREMENTS")
        _require(SCENARIOS["restart"] in resumed[1]["requirements"].content.chunks,
                 "EVIDENCE_RESTART_REQUIREMENTS")

        stop = restart["proof"]["hosting_restart"]
        parent = second[0].scope_binding.parent_session
        _require(
            stop["schema_version"] == 1 and stop["phase"] == "stop_confirmed"
            and stop["parent"] == parent and stop["version"] == second[0].coordinator_version
            and stop["stop_http_status"] == 204
            and stopped_session["agent_session_id"] == parent
            and stopped_session["version_indicator"]["agent_version"] == stop["version"]
            and stopped_session["status"] == "idle"
            and type(stop["stopped_at"]) in (int, float) and math.isfinite(stop["stopped_at"])
            and stop["stopped_at"] > 0 and stopped_session["stopped_at"] == stop["stopped_at"]
            and (stop["previous_stopped_at"] is None or (
                type(stop["previous_stopped_at"]) in (int, float)
                and math.isfinite(stop["previous_stopped_at"])
                and stop["stopped_at"] > stop["previous_stopped_at"]
            )), "EVIDENCE_CONFIRMED_STOP",
        )
        # Each entry is one actual stop POST observed at the boundary. A recovered
        # stop_pending journal is not itself evidence of another POST.
        _require(restart["stops"] == [parent], "EVIDENCE_ONCE_ONLY_STOP")
        before_checkpoints, after_checkpoints = {}, {}
        for snapshot, target in ((followup, before_checkpoints), (restart, after_checkpoints)):
            capture = snapshot["checkpoints"]
            _require(capture["scope_binding"] == second[0].scope_binding.model_dump(mode="json"),
                     "EVIDENCE_CHECKPOINT_SCOPE")
            for checkpoint in capture["records"]:
                key = checkpoint["checkpoint_id"]
                _require(
                    isinstance(key, str) and bool(key) and key not in target
                    and checkpoint["workflow_name"] == "distributed-agents-v1"
                    and bool(checkpoint["graph_signature_hash"])
                    and type(checkpoint["iteration_count"]) is int
                    and checkpoint["iteration_count"] >= 0
                    and isinstance(checkpoint["state"], dict),
                    "EVIDENCE_CHECKPOINT",
                )
                target[key] = checkpoint
        _require(
            bool(before_checkpoints) and len(after_checkpoints) > len(before_checkpoints)
            and all(after_checkpoints.get(key) == value for key, value in before_checkpoints.items())
            and len({item["graph_signature_hash"] for item in after_checkpoints.values()}) == 1,
            "EVIDENCE_CHECKPOINT_RECONCILIATION",
        )
        original_scope, isolated_scope = first[0].scope_binding, separate[0].scope_binding
        _require(
            (original_scope.project, original_scope.tenant, original_scope.principal) ==
            (isolated_scope.project, isolated_scope.tenant, isolated_scope.principal)
            and original_scope.parent_session != isolated_scope.parent_session
            and initial["proof"]["framework"]["session_id"] != isolated["proof"]["framework"]["session_id"]
            and original_scope.prefix != isolated_scope.prefix
            and not ({value[0] for value in first[2].values()} & {value[0] for value in separate[2].values()})
            and not ({value[1] for value in first[2].values()} & {value[1] for value in separate[2].values()}),
            "EVIDENCE_PARENT_ISOLATION",
        )
        _require(separate[1]["requirements"].content.chunks == [SCENARIOS["isolated"]],
                 "EVIDENCE_ISOLATED_REQUIREMENTS")
        _require(
            not (set(restart["sends"]) & set(isolated["sends"]))
            and not (set(restart["creations"]) & set(isolated["creations"]))
            and not ({value["accepted"].response_id for value in resumed[3].values()
                      if value["accepted"].kind == "call"} &
                     {value["accepted"].response_id for value in separate[3].values()
                      if value["accepted"].kind == "call"}),
            "EVIDENCE_ISOLATED_EFFECTS",
        )
        # Check all supplied isolated artifacts, not just model prose in the final
        # candidate. The isolated brief itself contains a negative Harbor reference.
        for kind in ("candidate", "review"):
            content = json.dumps(separate[1][kind].content.model_dump(mode="json")).casefold()
            _require("harbor" not in content and "asynchronous queue" not in content,
                     "EVIDENCE_CONTENT_LEAK")
        for item in (followup, restart, isolated):
            _require(item["proof"]["metadata"] == initial["proof"]["metadata"],
                     "EVIDENCE_RELEASE_DRIFT")
    except RuntimeError as exc:
        if re.fullmatch(r"EVIDENCE_[A-Z_]+", str(exc)):
            raise
        raise RuntimeError("EVIDENCE_TURN_REJECTED") from None
    except (KeyError, TypeError, ValueError, AttributeError, IndexError):
        # Do not echo private inputs or Pydantic validation details to terminals.
        raise RuntimeError("EVIDENCE_MISSING_OR_INVALID") from None


async def observe_pending_child(project, response):
    records = [json.loads(line) for line in response.output_text.splitlines() if line.startswith("{")]
    results = [record for record in records if record.get("event") == "result"]
    if len(results) != 1 or results[0].get("native_workflow") != "distributed-agents-v1":
        return None
    effect = results[0].get("pending_effect")
    if not effect or effect.get("role") not in ("architect", "reviewer") or not effect.get("response_id"):
        return None
    child = await project.get_openai_client(agent_name=AGENTS[effect["role"]]).responses.retrieve(
        effect["response_id"],
    )
    if child.id != effect["response_id"]:
        raise RuntimeError("CHILD_RESPONSE_CHANGED")
    return {
        "role": effect["role"], "response_id": child.id, "status": child.status,
        "error_code": child.error.code if child.error else None,
        "storage_codes": storage_codes(child.error.message) if child.error else [],
        "agent_session_id": getattr(child, "agent_session_id", None),
        "parent_hold": results[0]["status"],
    }


async def run(args):
    tenant, subscription, user = verify_lab()
    if args.scenario == "observe":
        state = json.loads(private_state_path(args.session_file).read_text())
        if state.get("schema_version") != 1 or state.get("user") != user or state.get("tenant") != tenant:
            raise RuntimeError("SESSION_OWNER")
        if state.get("runtime") != "native" or state.get("bound") is not True:
            raise RuntimeError("BOUND_NATIVE_SESSION_REQUIRED")
        if not state.get("pending") or not state.get("pending_response"):
            raise RuntimeError("KNOWN_PENDING_RESPONSE_REQUIRED")
        hosted_id = state["framework"]["state"]["foundry_hosted_agent_session_id"]
        async with AzureCliCredential(subscription=subscription, process_timeout=30) as credential, \
                data_client(socks=args.socks) as http, ProjectClient(credential, http, {}) as project:
            response = await project.get_openai_client(agent_name=AGENTS["coordinator"]).responses.retrieve(
                state["pending_response"], extra_query={"agent_session_id": hosted_id},
            )
            result = response.model_dump(mode="json", include={
                "id", "status", "error", "incomplete_details", "usage", "created_at",
            })
            if response.id != state["pending_response"]:
                raise RuntimeError("PARENT_RESPONSE_CHANGED")
            if response.status == "failed":
                result["host_diagnostics"] = await observe_host_failure(
                    http, credential, hosted_id, state["version"], response_id=response.id, structured=True,
                )
            elif response.status == "completed":
                result["pending_child"] = await observe_pending_child(project, response)
                child = result["pending_child"]
                if child and child["status"] == "failed" and child["agent_session_id"]:
                    session = await rest(
                        http, credential, "GET",
                        f"/agents/{AGENTS[child['role']]}/endpoint/sessions/"
                        + quote(child["agent_session_id"], safe=""),
                    )
                    version = session["version_indicator"]["agent_version"]
                    child["host_diagnostics"] = await observe_host_failure(
                        http, credential, child["agent_session_id"], version, role=child["role"],
                        response_id=child["response_id"], structured=True,
                    )
                if child and child["status"] == "failed":
                    result["parent_host_diagnostics"] = await observe_host_failure(
                        http, credential, hosted_id, state["version"], response_id=response.id, structured=True,
                    )
            print(json.dumps(result))
        return
    async with AzureCliCredential(subscription=subscription, process_timeout=30) as credential, \
            data_client(socks=args.socks) as http:
        observed = {}
        for role, name in AGENTS.items():
            body = await rest(http, credential, "GET", "/agents/" + name)
            metadata = agent_metadata(name, body)
            code = metadata["code_configuration"]
            if (metadata["status"] != "active" or code["content_hash"] != args.sha256 or
                code["dependency_resolution"] != "bundled"):
                raise RuntimeError(f"DEPLOYED_BUNDLE_REQUIRED: {name}")
            observed[role] = metadata
    path = private_state_path(args.session_file)
    continuation = args.scenario in ("followup", "recover", "restart")
    if not continuation and path.exists():
        raise RuntimeError("NEW_ACCEPTANCE_PARENT_REQUIRED")
    if continuation and not path.exists():
        raise RuntimeError("EXISTING_ACCEPTANCE_PARENT_REQUIRED")
    before = json.loads(path.read_text()) if path.exists() else None
    if before and (before.get("user") != user or before.get("tenant") != tenant
                   or before.get("runtime") != "native" or before.get("version") != observed["coordinator"]["version"]):
        raise RuntimeError("OWNED_NATIVE_CONTINUATION_REQUIRED")
    output = io.StringIO()
    restart_proof = None
    try:
        with session_lease(path), redirect_stdout(output):
            if args.scenario == "restart":
                async with AzureCliCredential(subscription=subscription, process_timeout=30) as credential, \
                        data_client(socks=args.socks) as http:
                    restart_proof = await stop_hosting_for_acceptance(http, credential, before, path)
            await chat(SimpleNamespace(
                socks=args.socks, session_file=str(path), message=SCENARIOS.get(args.scenario),
                show_ids=True, native=True, recover_only=args.scenario == "recover",
            ))
    finally:
        private_state_path(args.evidence).write_text(output.getvalue(), encoding="utf-8")
    text = output.getvalue()
    proof = events(text)
    if proof["result"].get("native_workflow") != "distributed-agents-v1":
        raise RuntimeError("NATIVE_ACCEPTANCE_REQUIRED")
    after = json.loads(path.read_text())
    artifacts = validate_artifact_evidence(proof["result"])
    binding = artifacts["requirements"].scope_binding
    if (binding.project != PROJECT or binding.tenant != tenant
            or binding.parent_session != after["framework"]["state"]["foundry_hosted_agent_session_id"]
            or artifacts["requirements"].producer.session_id != binding.parent_session
            or artifacts["requirements"].producer.version != after["version"]):
        raise RuntimeError("NATIVE_PARENT_ARTIFACT_BINDING")
    if after["pending"]:
        raise RuntimeError("PARENT_TURN_UNCERTAIN")
    if before and before["framework"]["session_id"] != after["framework"]["session_id"]:
        raise RuntimeError("PARENT_CONTINUITY_FAILED")
    children = {}
    async with AzureCliCredential(subscription=subscription, process_timeout=30) as credential, \
            data_client(socks=args.socks) as http:
        for role in ("architect", "reviewer"):
            role_events = [event for event in proof["delegations"] if event["role"] == role]
            workflow_mode = proof["result"].get("native_workflow") == "distributed-agents-v1"
            if not workflow_mode and len(role_events) != 1:
                raise RuntimeError("MULTIPLE_CHILD_SESSIONS_PER_ROLE")
            if workflow_mode and len({
                (event["hosted_session"], event["framework_session"], event["version"]) for event in role_events
            }) != 1:
                raise RuntimeError("CHILD_BINDING_CHANGED_WITHIN_TURN")
            role_event = role_events[0]
            if role_event.get("specialist_mode") == "in_process":
                children[role] = {
                    "agent_session_id": role_event["framework_session"],
                    "mode": "in_process",
                }
                continue
            identities = {role_event["hosted_session"]}
            body = await rest(http, credential, "GET", f"/agents/{AGENTS[role]}/endpoint/sessions")
            matches = [session for session in body["data"]
                       if alias(session["agent_session_id"]) in identities]
            if len(matches) != 1:
                raise RuntimeError("EXACT_CHILD_SESSION_UNPROVEN")
            children[role] = matches[0]
    validate_exercised_versions(after["version"], observed, proof["delegations"], children)
    for role, kind in (("architect", "candidate"), ("reviewer", "review")):
        producer = artifacts[kind].producer
        if (producer.version != observed[role]["version"]
                or producer.session_id != children[role]["agent_session_id"] or not producer.response_id):
            raise RuntimeError("NATIVE_CHILD_ARTIFACT_BINDING")
    proof.update(scenario=args.scenario, metadata=observed,
                 framework=after["framework"], version=after["version"],
                 child_sessions=children,
                 terminal_process_restarted=continuation,
                 hosting_restart=restart_proof)
    print(json.dumps(proof))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--socks", required=True)
    parser.add_argument("--sha256", required=True)
    parser.add_argument("--session-file", required=True)
    parser.add_argument("--evidence", required=True)
    parser.add_argument("--scenario", choices=(*SCENARIOS, "observe", "recover"), required=True)
    asyncio.run(run(parser.parse_args()))


if __name__ == "__main__":
    main()
