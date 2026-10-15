from __future__ import annotations

import argparse
import asyncio
import json
import os
import subprocess
import sys
import uuid
from contextlib import contextmanager
from pathlib import Path
from urllib.parse import quote

from agent_framework import AgentSession
from agent_framework.exceptions import ChatClientException
from agent_framework.foundry import FoundryAgent
from agent_framework_foundry import FOUNDRY_HOSTED_AGENT_SESSION_ID_KEY
from azure.identity.aio import AzureCliCredential

from .config import ConfigurationError, required
from .contracts import AGENTS, PROJECT, DemoError, alias
from .foundry import ProjectClient, data_client


def verify_lab() -> tuple[str, str, str]:
    try:
        tenant = str(uuid.UUID(required("EXPECTED_AZURE_TENANT_ID")))
        subscription = str(uuid.UUID(required("EXPECTED_AZURE_SUBSCRIPTION_ID")))
        profile = Path(required("AZURE_CONFIG_DIR")).expanduser()
        if not profile.is_absolute() or not profile.is_dir():
            raise ConfigurationError("EXPLICIT_AZURE_CLI_PROFILE_REQUIRED")
    except (ConfigurationError, ValueError) as exc:
        raise DemoError("CLIENT_CONFIGURATION", {"validation": str(exc)}) from exc
    os.environ["AZURE_CONFIG_DIR"] = str(profile.resolve())
    os.environ["AZURE_EXTENSION_USE_DYNAMIC_INSTALL"] = "no"
    import shutil
    az = shutil.which("az")
    if not az:
        raise DemoError("AZURE_CLI_MISSING")
    command = [az, "account", "show", "--subscription", subscription,
               "--query", "{subscription:id,tenant:tenantId,user:user.name}",
               "-o", "json", "--only-show-errors"]
    result = subprocess.run(command, capture_output=True, text=True, timeout=30)
    if result.returncode:
        raise DemoError("LAB_AUTH_REQUIRED")
    actual = json.loads(result.stdout)
    if actual["subscription"] != subscription or actual["tenant"] != tenant:
        raise DemoError("LAB_SCOPE")
    return tenant, subscription, actual["user"]


@contextmanager
def session_lease(path: Path):
    import msvcrt
    with path.with_name(path.name + ".lock").open("a+b") as lock:
        if lock.tell() == 0:
            lock.write(b"0")
            lock.flush()
        lock.seek(0)
        try:
            msvcrt.locking(lock.fileno(), msvcrt.LK_NBLCK, 1)
        except OSError as exc:
            raise DemoError("PARENT_IN_USE") from exc
        try:
            yield
        finally:
            lock.seek(0)
            msvcrt.locking(lock.fileno(), msvcrt.LK_UNLCK, 1)


def write_state(path: Path, state: dict, *, new=False):
    encoded = json.dumps(state, indent=2, allow_nan=False)
    if new:
        with path.open("x", encoding="utf-8") as file:
            file.write(encoded)
            file.flush()
            os.fsync(file.fileno())
    else:
        temporary = path.with_name(path.name + ".tmp")
        with temporary.open("x", encoding="utf-8") as file:
            file.write(encoded)
            file.flush()
            os.fsync(file.fileno())
        temporary.replace(path)


def private_state_path(value: str) -> Path:
    path = Path(value).resolve()
    if path.is_relative_to(Path(__file__).resolve().parents[1]):
        raise DemoError("SESSION_FILE_MUST_BE_PRIVATE")
    if not path.parent.is_dir():
        raise DemoError("SESSION_DIRECTORY_MISSING")
    return path


async def recover_parent(project, hosted_id: str, response_id: str):
    client = project.get_openai_client(agent_name=AGENTS["coordinator"])
    async with asyncio.timeout(400):
        while True:
            response = await client.responses.retrieve(
                response_id, extra_query={"agent_session_id": hosted_id},
            )
            if response.id != response_id:
                raise DemoError("PARENT_RESPONSE_CHANGED")
            if response.status == "completed" and response.output_text:
                return response
            if response.status not in ("queued", "in_progress"):
                raise DemoError("PARENT_INCOMPLETE")
            await asyncio.sleep(1)


def finish_native_turn(path: Path, state: dict, session: AgentSession, text: str):
    records = [json.loads(line) for line in text.splitlines() if line.startswith("{")]
    results = [record for record in records if record.get("event") == "result"]
    if len(results) != 1:
        raise DemoError("PARENT_RESULT_SCHEMA")
    if results[0].get("pending_effect") is not None:
        state["operation_hold"] = results[0]["status"]
        write_state(path, state)
        raise DemoError("PARENT_OPERATION_UNCERTAIN")
    state.update(framework=session.to_dict(), pending=False)
    state.pop("pending_response", None)
    state.pop("operation_hold", None)
    write_state(path, state)


async def rest(http, credential, method: str, path: str, *, body=None):
    token = await credential.get_token("https://ai.azure.com/.default")
    response = await http.request(
        method, PROJECT + path, params={"api-version": "v1"}, json=body,
        headers={"Authorization": f"Bearer {token.token}"},
    )
    if response.status_code not in (200, 201):
        raise DemoError(f"PROJECT_HTTP_{response.status_code}")
    return response.json()


async def chat(args):
    tenant, subscription, user = verify_lab()
    state_path = private_state_path(args.session_file)
    native = getattr(args, "native", False)
    recover_only = getattr(args, "recover_only", False)
    # CLI token acquisition forbids combining tenant and subscription selectors.
    # verify_lab checks the registered tenant before selecting its subscription.
    async with AzureCliCredential(
        subscription=subscription, process_timeout=30
    ) as credential, data_client(socks=args.socks) as http:
        async with ProjectClient(credential, http, {}) as project:
            if state_path.exists():
                state = json.loads(state_path.read_text(encoding="utf-8"))
                if state.get("schema_version") != 1 or state.get("user") != user or state.get("tenant") != tenant:
                    raise DemoError("SESSION_OWNER")
                if state.get("runtime", "legacy") != ("native" if native else "legacy"):
                    raise DemoError("SESSION_RUNTIME_CHANGED")
                if state.get("pending") and not (native and recover_only and state.get("pending_response")):
                    raise DemoError("PARENT_TURN_UNCERTAIN")
                session = AgentSession.from_dict(state["framework"])
            else:
                if recover_only:
                    raise DemoError("KNOWN_PENDING_RESPONSE_REQUIRED")
                hosted_id = uuid.uuid4().hex
                session = AgentSession()
                session.state[FOUNDRY_HOSTED_AGENT_SESSION_ID_KEY] = hosted_id
                state = {
                    "schema_version": 1, "tenant": tenant, "user": user,
                    "framework": session.to_dict(), "bound": False, "pending": False,
                    "runtime": "native" if native else "legacy",
                }
                details = await rest(http, credential, "GET", f"/agents/{AGENTS['coordinator']}")
                state["version"] = details["versions"]["latest"]["version"]
                write_state(state_path, state, new=True)
                await rest(
                    http, credential, "POST",
                    f"/agents/{AGENTS['coordinator']}/endpoint/sessions",
                    body={
                        "agent_session_id": hosted_id,
                        "version_indicator": {"type": "version_ref", "agent_version": state["version"]},
                    },
                )
                state["bound"] = True
                write_state(state_path, state)
            hosted_id = session.state[FOUNDRY_HOSTED_AGENT_SESSION_ID_KEY]
            resource = await rest(
                http, credential, "GET",
                f"/agents/{AGENTS['coordinator']}/endpoint/sessions/{quote(hosted_id, safe='')}",
            )
            if resource["status"] in ("expired", "deleted"):
                raise DemoError("SESSION_EXPIRED")
            if resource["version_indicator"].get("agent_version") != state["version"]:
                raise DemoError("PARENT_VERSION_CHANGED")
            if not state["bound"]:
                # Reconcile an uncertain create by inspecting its persisted ID.
                state["bound"] = True
                write_state(state_path, state)
            if recover_only:
                if not state.get("pending") or not state.get("pending_response"):
                    raise DemoError("KNOWN_PENDING_RESPONSE_REQUIRED")
                response = await recover_parent(project, hosted_id, state["pending_response"])
                print(response.output_text, end="", flush=True)
                session.service_session_id = response.id
                finish_native_turn(state_path, state, session, response.output_text)
                return
            agent = FoundryAgent(
                project_client=project, agent_name=AGENTS["coordinator"],
                allow_preview=True, default_options={
                    "store": True, **({"background": True} if native else {}),
                }, timeout=400,
            )
            print(f"Parent hosted={alias(hosted_id)} framework={alias(session.session_id)}")
            if args.show_ids:
                print(f"Parent hosted_id={hosted_id} framework_id={session.session_id}")
            while True:
                text = args.message or await asyncio.to_thread(input, "You (/quit): ")
                if text.strip() == "/quit":
                    return
                state["pending"] = True
                write_state(state_path, state)
                stream = agent.run(text, session=session, stream=True)
                printed = ""
                try:
                    async with stream:
                        async for update in stream:
                            if update.response_id:
                                state["pending_response"] = update.response_id
                                write_state(state_path, state)
                            if update.text:
                                print(update.text, end="", flush=True)
                                printed += update.text
                        result = await stream.get_final_response()
                except (ChatClientException, TimeoutError) as exc:
                    if not native or not state.get("pending_response"):
                        raise
                    print(f"Recovering known parent after {type(exc).__name__}; no resend.", file=sys.stderr)
                    result = None
                if result is None or result.finish_reason != "stop":
                    if not native or not state.get("pending_response"):
                        raise DemoError("PARENT_INCOMPLETE")
                    response = await recover_parent(project, hosted_id, state["pending_response"])
                    if not response.output_text.startswith(printed):
                        raise DemoError("PARENT_OUTPUT_CHANGED")
                    print(response.output_text[len(printed):], end="", flush=True)
                    printed = response.output_text
                    session.service_session_id = response.id
                if session.state.get(FOUNDRY_HOSTED_AGENT_SESSION_ID_KEY) != hosted_id:
                    raise DemoError("PARENT_SESSION_CHANGED")
                if native:
                    finish_native_turn(state_path, state, session, printed)
                else:
                    state.update(framework=session.to_dict(), pending=False)
                    state.pop("pending_response", None)
                    write_state(state_path, state)
                if args.message:
                    return


def main():
    parser = argparse.ArgumentParser(description="Private, stateful Hosted Agent terminal.")
    parser.add_argument("--socks", required=True, help="Owned socks5h://127.0.0.1:<port>")
    parser.add_argument("--session-file", required=True, help="Private file outside the repository")
    parser.add_argument("--message", help="One synthetic turn, then exit")
    parser.add_argument("--show-ids", action="store_true")
    parser.add_argument("--native", action="store_true", help="Use the new native runtime; never reinterpret a legacy session.")
    parser.add_argument("--recover-only", action="store_true", help="Retrieve the exact persisted native response; never create another.")
    args = parser.parse_args()
    try:
        with session_lease(private_state_path(args.session_file)):
            asyncio.run(chat(args))
    except DemoError as exc:
        print(f"BLOCKED: {exc.code}", file=sys.stderr)
        raise SystemExit(1) from exc


if __name__ == "__main__":
    main()
