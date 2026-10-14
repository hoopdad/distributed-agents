import os

from agent_framework_foundry_hosting import ResponsesHostServer
from agent_framework_foundry_hosting import CheckpointStoreProvider
from azure.ai.agentserver.responses import ResponsesServerOptions

from .foundry import create_hosted_agent


def main():
    role = os.environ["DEMO_ROLE"]
    runtime = os.environ.get("DEMO_RUNTIME", "legacy")
    if runtime == "native":
        if os.environ.get("AGENTSERVER_TASKS_BACKEND", "hosted") != "hosted":
            raise RuntimeError("Native hosting requires the hosted resilient task backend.")
        from .workflow import create_native_workflow, parse_native_turn
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
