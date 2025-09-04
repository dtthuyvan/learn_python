import os
import click
import uvicorn

from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import AgentCapabilities, AgentCard, AgentSkill

from a2a_structure.host_agent.host_agent_executor import HostAgentExecutor


@click.command()
@click.option("--host", default="localhost")
@click.option("--port", default=10000)
def main(host, port):
    # --- 2. Define Host Agent Card ---
    capabilities = AgentCapabilities(streaming=True)
    skill = AgentSkill(
        id="agent_coordination",
        name="Host Agent",
        description="Delegates tasks to specialized agents.",
        capabilities=capabilities,
        executor=HostAgentExecutor(),
        tags=["host", "coordination"],
    )

    agent_card = AgentCard(
        name="Host Agent",
        description="Coordinates and delegates tasks to other agents.",
        url=f"http://{host}:{port}/",
        version="1.0.0",
        defaultInputModes=["text", "text/plain"],
        defaultOutputModes=["text", "text/plain"],
        capabilities=capabilities,
        skills=[skill],
    )

    # --- 3. Setup Request Handler ---
    request_handler = DefaultRequestHandler(
        agent_executor=HostAgentExecutor(),
        task_store=InMemoryTaskStore(),
    )

    # --- 4. Start server ---
    server = A2AStarletteApplication(
        agent_card=agent_card, http_handler=request_handler
    )
    uvicorn.run(server.build(), host=host, port=port)


if __name__ == "__main__":
    main()
