import logging
import os

from agent_framework_foundry_hosting import ResponsesHostServer
from agent_framework_foundry_hosting import CheckpointStoreProvider
from azure.ai.agentserver.responses import ResponsesServerOptions
from azure.ai.agentserver.core import AgentConfig, get_request_context

from .foundry import create_hosted_agent


class NativePreparationDiagnostics(logging.Filter):
    def __init__(self, config):
        super().__init__()
        self.config = config

    def filter(self, record):
        if (record.msg == "Native Responses workflow failed during %s (%s)."
                and record.args == ("preparation", "RuntimeError")):
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
            raise RuntimeError("Native hosting requires the hosted resilient task backend.")
        from .workflow import create_native_workflow, parse_native_turn
        logger = logging.getLogger("agent_framework_foundry_hosting._workflow_responses")
        if not any(isinstance(item, NativePreparationDiagnostics) for item in logger.filters):
            logger.addFilter(NativePreparationDiagnostics(AgentConfig.from_env()))
        ResponsesHostServer(
            workflow=create_native_workflow, parse_response=parse_native_turn,
            checkpoint_store_provider=CheckpointStoreProvider(),
            options=ResponsesServerOptions(resilient_background=True),
            unsupported_options="error",
        ).run()
        return
    if runtime != "legacy":
        raise RuntimeError("Unsupported DEMO_RUNTIME.")
    ResponsesHostServer(
        create_hosted_agent,
        history_source="agent" if role == "coordinator" else "agent_server",
    ).run()


if __name__ == "__main__":
    main()
