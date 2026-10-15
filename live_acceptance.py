from __future__ import annotations

import argparse
import asyncio
from contextlib import redirect_stdout
import io
import json
import re
from types import SimpleNamespace
from urllib.parse import quote

from demo.contracts import AGENTS, PROJECT, Candidate, Review, alias
from demo.foundry import ProjectClient, data_client
from demo.terminal import chat, private_state_path, rest, session_lease, verify_lab
from azure.identity.aio import AzureCliCredential

from agent_metadata import agent_metadata
from demo.artifacts import ArtifactRef, Candidate as NativeCandidate, Decision, Review as NativeReview


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


def workflow_failure(line):
    """Expose only the SDK's fixed phase/type diagnostic, never arbitrary host logs."""
    if line.startswith("{"):
        try:
            value = json.loads(line)
        except ValueError:
            return None
        if not isinstance(value, dict) or not isinstance(value.get("message"), str):
            return None
        line = value["message"]
    match = re.search(
        r"Native Responses workflow failed during "
        r"(preparation|scoped continuation|input parsing|input validation|execution|final output persistence) "
        r"\((ArtifactError|ValueError|TypeError|RuntimeError|ConfigurationError|ValidationError)\)\.$",
        line,
    )
    return {"phase": match[1], "exception_type": match[2]} if match else None


async def observe_host_failure(http, credential, hosted_id, version):
    token = await credential.get_token("https://ai.azure.com/.default")
    path = (
        f"/agents/{quote(AGENTS['coordinator'], safe='')}/versions/{quote(version, safe='')}"
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
                        failure = workflow_failure(line[5:].strip().decode("utf-8"))
                        if failure is not None and failure not in diagnostics["failures"]:
                            diagnostics["failures"].append(failure)
    except TimeoutError:
        if not deadline.expired():
            raise
        diagnostics["limit"] = "time"
    return diagnostics


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
    native = result.get("native_workflow") == "distributed-agents-v1"
    turn, decisions = result.get("turn"), result.get("decisions")
    if (type(turn) is not int or turn < 1 or type(result.get("calls")) is not int or
            result.get("calls") != len(calls) or
            type(decisions) is not int or not len(calls) + (not native) <= decisions <= 10):
        raise RuntimeError("LIVE_RESULT_COUNTERS")
    if native:
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
        if any(call.get("specialist_mode") != "hosted" for call in calls):
            raise RuntimeError("REMOTE_SPECIALISTS_REQUIRED")
    try:
        candidate = (NativeCandidate if native else Candidate).model_validate(result.get("candidate"))
        review = (NativeReview if native else Review).model_validate(result.get("review"))
    except ValueError as exc:
        raise RuntimeError("LIVE_ARTIFACT_SCHEMA") from exc
    if (candidate.requirements_revision != turn or review.requirements_revision != turn or
            candidate.candidate_revision != review.candidate_revision):
        raise RuntimeError("LIVE_ARTIFACT_REVISION")
    if not review.approved:
        raise RuntimeError("LIVE_REVIEW_NOT_APPROVED")
    return {"result": result, "delegations": calls}


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
                    http, credential, hosted_id, state["version"],
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
    if args.scenario != "followup" and path.exists():
        raise RuntimeError("NEW_ACCEPTANCE_PARENT_REQUIRED")
    if args.scenario == "followup" and not path.exists():
        raise RuntimeError("EXISTING_ACCEPTANCE_PARENT_REQUIRED")
    before = json.loads(path.read_text()) if path.exists() else None
    output = io.StringIO()
    try:
        with session_lease(path), redirect_stdout(output):
            await chat(SimpleNamespace(
                socks=args.socks, session_file=str(path), message=SCENARIOS[args.scenario], show_ids=True, native=True,
            ))
    finally:
        private_state_path(args.evidence).write_text(output.getvalue(), encoding="utf-8")
    text = output.getvalue()
    proof = events(text)
    if proof["result"].get("native_workflow") != "distributed-agents-v1":
        raise RuntimeError("NATIVE_ACCEPTANCE_REQUIRED")
    after = json.loads(path.read_text())
    if after["pending"]:
        raise RuntimeError("PARENT_TURN_UNCERTAIN")
    if before and before["framework"]["session_id"] != after["framework"]["session_id"]:
        raise RuntimeError("PARENT_CONTINUITY_FAILED")
    children = {}
    async with AzureCliCredential(subscription=subscription, process_timeout=30) as credential, \
            data_client(socks=args.socks) as http:
        for role in ("architect", "reviewer"):
            role_events = [event for event in proof["delegations"] if event["role"] == role]
            native = proof["result"].get("native_workflow") == "distributed-agents-v1"
            if not native and len(role_events) != 1:
                raise RuntimeError("MULTIPLE_CHILD_SESSIONS_PER_ROLE")
            if native and len({
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
    proof.update(scenario=args.scenario, metadata=observed,
                 framework=after["framework"], version=after["version"],
                 child_sessions=children,
                 terminal_process_restarted=args.scenario == "followup")
    print(json.dumps(proof))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--socks", required=True)
    parser.add_argument("--sha256", required=True)
    parser.add_argument("--session-file", required=True)
    parser.add_argument("--evidence", required=True)
    parser.add_argument("--scenario", choices=(*SCENARIOS, "observe"), required=True)
    asyncio.run(run(parser.parse_args()))


if __name__ == "__main__":
    main()
