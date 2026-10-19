from __future__ import annotations

import argparse
import asyncio
from contextlib import redirect_stdout
import hashlib
import io
import json
import math
import re
from types import SimpleNamespace
from urllib.parse import quote

from demo.contracts import AGENTS, PROJECT, Candidate, Review, alias
from demo.foundry import ProjectClient, data_client
from demo.terminal import chat, private_state_path, rest, session_lease, verify_lab, write_state
from azure.identity.aio import AzureCliCredential

from agent_metadata import agent_metadata
from demo.artifacts import Artifact, ArtifactRef, Candidate as ArtifactCandidate, Decision, Review as ArtifactReview
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


async def observe_host_failure(http, credential, hosted_id, version, *, role="coordinator", response_id=None):
    token = await credential.get_token("https://ai.azure.com/.default")
    path = (
        f"/agents/{quote(AGENTS[role], safe='')}/versions/{quote(version, safe='')}"
        f"/sessions/{quote(hosted_id, safe='')}:logstream"
    )
    diagnostics = {"failures": [], "limit": None}
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
                if size > 131072:
                    diagnostics["limit"] = "bytes"
                    break
                pending += chunk
                while b"\n" in pending:
                    line, pending = pending.split(b"\n", 1)
                    if line.startswith(b"data:"):
                        text = line[5:].strip().decode("utf-8")
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
        }
        write_state(journal_path, journal, new=True)
        token = await credential.get_token("https://ai.azure.com/.default")
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
                    http, credential, hosted_id, state["version"], response_id=response.id,
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
                        response_id=child["response_id"],
                    )
                if child and child["status"] == "failed":
                    result["parent_host_diagnostics"] = await observe_host_failure(
                        http, credential, hosted_id, state["version"], response_id=response.id,
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
