from __future__ import annotations

from datetime import datetime, timezone
import json
import re
import time
import uuid

from mcp.shared.exceptions import McpError

ROLES = ("architect", "reviewer")
REQUEST_IDS = (
    "apim-request-id", "x-ms-request-id", "x-ms-correlation-request-id",
    "request-id", "x-request-id", "x-ms-activity-id",
)
ERROR_CODES = {
    "PERMISSION_DENIED", "UNAUTHENTICATED", "NOT_FOUND", "INVALID_ARGUMENT",
    "INTERNAL", "UNAVAILABLE", "DEADLINE_EXCEEDED", "RESOURCE_EXHAUSTED",
}
RPC_METHODS = {"initialize", "notifications/initialized", "notifications/cancelled", "tools/list", "ping"}


def correlation_ids(headers) -> dict:
    result = {}
    for name in REQUEST_IDS:
        value = headers.get(name, "")
        if re.fullmatch(r"[0-9a-fA-F]{32}|[0-9a-fA-F]{8}(?:-[0-9a-fA-F]{4}){3}-[0-9a-fA-F]{12}", value):
            result[name] = value
    value = headers.get("traceparent", "")
    if re.fullmatch(r"00-[0-9a-f]{32}-[0-9a-f]{16}-0[01]", value):
        result["traceparent"] = value
    return result


def failure(error: BaseException, names: dict[str, str]) -> dict:
    """Retain error classes/codes, never exception text, identities or URLs."""
    pending, seen, classes, codes, sources = [error], set(), set(), set(), []
    rpc_code = None
    while pending and len(seen) < 32:
        current = pending.pop()
        if id(current) in seen:
            continue
        seen.add(id(current))
        classes.add(type(current).__name__)
        code = getattr(current, "code", None)
        if isinstance(code, str) and (
            re.fullmatch(r"DIAGNOSTIC_[A-Z_]{1,64}", code)
            or code in {"CLIENT_CONFIGURATION", "LAB_AUTH_REQUIRED", "LAB_SCOPE", "AZD_MISSING", "SOCKS_SCOPE"}
        ):
            codes.add(code)
        for nested in (current.__cause__, current.__context__, getattr(current, "inner_exception", None)):
            if isinstance(nested, BaseException):
                pending.append(nested)
        if isinstance(current, BaseExceptionGroup):
            pending.extend(current.exceptions)
        if not isinstance(current, McpError):
            continue
        rpc_code = current.error.code
        data = current.error.data
        if not isinstance(data, dict) or "errors" not in data:
            message = current.error.message
            start = message.find('{"errors":')
            if start < 0 or len(message) > 131072:
                continue
            try:
                data = json.loads(message[start:])
            except ValueError:
                continue
        rows = data.get("errors")
        if not isinstance(rows, list) or len(rows) > 16:
            continue
        for row in rows:
            if not isinstance(row, dict) or not isinstance(row.get("error"), dict):
                continue
            detail = row["error"]
            code = detail.get("code")
            message = detail.get("message")
            status = None
            if isinstance(message, str):
                match = re.search(
                    r"\b(400|401|403|404|408|429|500|502|503|504) "
                    r"\((?:Bad Request|Unauthorized|Forbidden|Not Found|Request Timeout|"
                    r"Too Many Requests|Internal Server Error|Bad Gateway|Service Unavailable|Gateway Timeout)\)",
                    message,
                )
                status = int(match[1]) if match else None
            role = names.get(row.get("name")) if isinstance(row.get("name"), str) else None
            sources.append({
                "role": role or "unrecognized-source",
                "code": code if isinstance(code, str) and code in ERROR_CODES else "UNRECOGNIZED",
                "reported_http_status": status,
            })
    result = {"classes": sorted(classes), "codes": sorted(codes), "mcp_code": rpc_code, "sources": sources}
    response = getattr(error, "response", None)
    if response is not None:
        result["http_status"] = response.status_code
        result["request_ids"] = correlation_ids(response.headers)
    return result


class WireCapture:
    def __init__(self, targets: dict[str, str], report: dict, persist):
        self.targets, self.report, self.persist = targets, report, persist
        self.sent = set()

    async def request(self, request):
        from .contracts import DemoError

        route = self.targets.get(str(request.url).split("?", 1)[0])
        if route is None:
            raise DemoError("DIAGNOSTIC_TARGET_CHANGED")
        rpc = None
        if route == "toolbox":
            if request.method == "POST":
                payload = json.loads(await request.aread())
                rpc = payload.get("method")
                if rpc not in RPC_METHODS:
                    raise DemoError("DIAGNOSTIC_RPC_NOT_READ_ONLY")
            elif request.method not in ("GET", "DELETE"):
                raise DemoError("DIAGNOSTIC_METHOD_NOT_READ_ONLY")
        elif request.method != "GET":
            raise DemoError("DIAGNOSTIC_METHOD_NOT_READ_ONLY")
        key = (route, request.method, rpc)
        if key in self.sent:
            raise DemoError("DIAGNOSTIC_REPEAT_REFUSED")
        self.sent.add(key)
        client_id = str(uuid.uuid4())
        request.headers["x-ms-client-request-id"] = client_id
        row = {
            "route": route, "method": request.method, "rpc": rpc,
            "client_request_id": client_id, "authorization_present": bool(request.headers.get("Authorization")),
            "sent_at": datetime.now(timezone.utc).isoformat(), "status": None,
        }
        request.extensions["delegation_diagnostic"] = (row, time.monotonic())
        self.report["http"].append(row)
        self.persist()

    async def response(self, response):
        row, started = response.request.extensions["delegation_diagnostic"]
        row.update(
            status=response.status_code, request_ids=correlation_ids(response.headers),
            duration_ms=round((time.monotonic() - started) * 1000, 1),
        )
        self.persist()
