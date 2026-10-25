import asyncio
import logging
import os
from time import perf_counter

from agent_framework_foundry_hosting import ResponsesHostServer
from agent_framework_foundry_hosting import CheckpointStoreProvider
from azure.ai.agentserver.responses import ResponsesServerOptions
from azure.ai.agentserver.core import AgentConfig, get_request_context
from azure.ai.agentserver.invocations import InvocationAgentServerHost

from .foundry import create_hosted_agent
from . import diagnostics as diag


class ProbeResponsesHostServer(ResponsesHostServer, InvocationAgentServerHost):
    """Compose the pinned SDK's cooperative protocol routes in one host."""


def context_checkpoint(stage, request=None, *, kind=diag.Kind.CONTEXT):
    """Observe supported SDK context, never create/repair trusted identity.

    A missing request means its resolved scope is unavailable (e.g. rejection
    before the factory), not an absent scope user. No SDK objects reach emit.
    Resilient recovery may have no inherited observation alias; do not invent
    a join to a previous HTTP request in that case.
    """
    try:
        context = get_request_context()
        scope_user = request.scope.user_id if request is not None else None
        diag.emit(diag.Event(
            role=diag.Role(os.environ["DEMO_ROLE"]), stage=stage, kind=kind,
            route=diag.Route.RESPONSES,
            category=diag.Category.REJECTED if kind is diag.Kind.EXECUTION_REJECTED else diag.Category.NONE,
            scope_user=diag.observe_value(scope_user) if request is not None else diag.unobserved(),
            request_user=diag.observe_value(context.user_id),
            call=diag.observe_value(context.call_id),
            scope_request_match=diag.compare_values(
                scope_user, context.user_id, same_representation=True,
            ),
        ))
    except Exception:
        # Even diagnostics/context access failure must preserve SDK rejection.
        pass


def prepare_diagnostic_options(request, options):
    """Public options hook; identity and caller options remain untouched."""
    context_checkpoint(
        diag.Stage.BACKGROUND if request.request.get("background") is True else diag.Stage.REQUEST,
        request,
    )
    return options


def execution_checkpoint(runtime):
    """Recovery can skip the parser, so observe actual executor/resource entry.

    No requirement is added to application runtime adapters solely for logging.
    Missing request-aware scope remains explicitly unavailable.
    """
    try:
        context_checkpoint(diag.Stage.EXECUTION, getattr(runtime, "request", None))
    except Exception:
        pass


class IngressDiagnostics:
    """Pure ASGI observation: no body buffering, extra reads or lifetime tasks.

    Final body means only ASGI completion, never successful agent execution.
    Raw headers are observed before endpoint parsing, not used as authority.
    """

    def __init__(self, app, *, role):
        self.app = app
        self.role = diag.Role(role)

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return
        started = perf_counter()
        method = next((item for item in diag.Method if item.value == scope.get("method")), diag.Method.OTHER)
        # Only literal route categories; no concrete path, query or ID escapes.
        route = diag.Route.RESPONSES if scope.get("path") == "/responses" else diag.Route.OTHER
        status = None

        def observe(kind, category=diag.Category.NONE, *, headers=False):
            try:
                raw = scope.get("headers") if headers else None
                diag.emit(diag.Event(
                    role=self.role, stage=diag.Stage.INGRESS, kind=kind,
                    method=method, route=route, status=status, category=category,
                    duration_ms=(perf_counter() - started) * 1000,
                    delegation=diag.observe_header(raw, "delegation") if headers else None,
                    platform=diag.observe_header(raw, "platform") if headers else None,
                    call=diag.observe_header(raw, "call") if headers else None,
                ))
            except Exception:
                pass

        async def observed_receive():
            message = await receive()
            if message["type"] == "http.disconnect":
                observe(diag.Kind.DISCONNECT)
            return message

        async def observed_send(message):
            nonlocal status
            await send(message)
            if message["type"] == "http.response.start":
                status = message.get("status")
                observe(diag.Kind.RESPONSE_HEADERS)
            elif message["type"] == "http.response.body" and not message.get("more_body", False):
                observe(diag.Kind.ASGI_FINAL_BODY)

        with diag.bind(diag.new_binding()):
            observe(diag.Kind.SEND, headers=True)
            try:
                await self.app(scope, observed_receive, observed_send)
            except asyncio.CancelledError:
                observe(diag.Kind.CANCELLED, diag.Category.CANCELLED)
                raise
            except Exception:
                observe(diag.Kind.ERROR, diag.Category.APPLICATION)
                raise


class WorkflowPreparationDiagnostics(logging.Filter):
    def __init__(self, config):
        super().__init__()
        self.config = config

    def filter(self, record):
        # SDK log text and diagnostic codes are consumed by existing observation tools.
        if (record.msg == "Native Responses workflow failed during %s (%s)."
                and record.args == ("preparation", "RuntimeError")):
            context_checkpoint(diag.Stage.PREPARATION, kind=diag.Kind.EXECUTION_REJECTED)
            context = get_request_context()
            code = next((code for valid, code in (
                (bool(self.config.session_id), "NATIVE_HOST_SESSION"),
                (bool(context.user_id), "NATIVE_HOST_PRINCIPAL"),
                (bool(context.call_id), "NATIVE_HOST_CALL"),
                (not context.session_id or context.session_id == self.config.session_id, "TRUSTED_PARENT_REQUIRED"),
            ) if not valid), "UNCLASSIFIED")
            logging.getLogger(__name__).error("Native workflow preparation rejected (%s).", code)
        return True


def main():
    role = os.environ["DEMO_ROLE"]
    runtime = os.environ.get("DEMO_RUNTIME", "legacy")
    if runtime == "native":
        if os.environ.get("AGENTSERVER_TASKS_BACKEND", "hosted") != "hosted":
            raise RuntimeError("Foundry workflow hosting requires the hosted resilient task backend.")
        from .workflow import create_workflow, parse_turn
        logger = logging.getLogger("agent_framework_foundry_hosting._workflow_responses")
        if not any(isinstance(item, WorkflowPreparationDiagnostics) for item in logger.filters):
            logger.addFilter(WorkflowPreparationDiagnostics(AgentConfig.from_env()))
        server = ProbeResponsesHostServer(
            workflow=create_workflow, parse_response=parse_turn,
            checkpoint_store_provider=CheckpointStoreProvider(),
            options=ResponsesServerOptions(resilient_background=True),
            unsupported_options="error",
            prepare_options=prepare_diagnostic_options,
        )
        from .identity_probe import register_identity_probe
        register_identity_probe(server)
        server.add_middleware(IngressDiagnostics, role=role)
        server.run()
        return
    if runtime != "legacy":
        raise RuntimeError("Unsupported DEMO_RUNTIME.")
    server = ResponsesHostServer(
        create_hosted_agent,
        history_source="agent" if role == "coordinator" else "agent_server",
    )
    server.add_middleware(IngressDiagnostics, role=role)
    server.run()


if __name__ == "__main__":
    main()
