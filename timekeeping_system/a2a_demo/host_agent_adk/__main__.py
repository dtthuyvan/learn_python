import os
import click
import uvicorn
import asyncio
from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import AgentCapabilities, AgentCard, AgentSkill
from host.agent import HostAgent


class MissingAPIKeyError(Exception):
    """Exception for missing API key."""
    pass


class HostAgentExecutor:
    """Executor for the Host Agent."""
    
    def __init__(self, host_agent: HostAgent):
        self.host_agent = host_agent
    
    async def execute(self, task, context=None):
        """Execute a task using the host agent."""
        session_id = context.get("session_id", "default") if context else "default"
        
        # Stream the response from the host agent
        response_parts = []
        async for chunk in self.host_agent.stream(task, session_id):
            if chunk.get("is_task_complete"):
                response_parts.append(chunk.get("content", ""))
            else:
                # Handle streaming updates if needed
                pass
        
        return "\n".join(response_parts)


@click.command()
@click.option("--host", default="localhost", help="Host to run the server on")
@click.option("--port", default=10000, help="Port to run the server on")
def main(host, port):
    """Starts the Host agent server."""
    try:
        # Check for API key
        if not os.getenv("GOOGLE_API_KEY"):
            raise MissingAPIKeyError("GOOGLE_API_KEY environment variable not set.")
        
        # Initialize the host agent
        print("Initializing Host Agent...")
        host_agent = asyncio.run(HostAgent.create([
            "http://localhost:10002",  # Employee's Agent
            "http://localhost:10003",  # Time tracking Agent
        ]))
        print("Host Agent initialized successfully")
        
        # Create agent card
        capabilities = AgentCapabilities(streaming=True)
        skill = AgentSkill(
            id="host_agent",
            name="Host Agent",
            description="Orchestrates time tracking and attendance operations",
            tags=["host", "orchestration", "time_tracking", "attendance"],
            examples=[
                "How many employees are there?",
                "Who checked in on time today?",
                "Show me overtime hours for this week"
            ],
        )
        
        agent_card = AgentCard(
            name="Host Agent",
            description="This Host agent orchestrates time tracking and attendance",
            url=f"http://{host}:{port}/",
            version="1.0.0",
            defaultInputModes=["text/plain"],
            defaultOutputModes=["text/plain"],
            capabilities=capabilities,
            skills=[skill],
        )
        
        # Create executor and request handler
        executor = HostAgentExecutor(host_agent)
        request_handler = DefaultRequestHandler(
            agent_executor=executor,
            task_store=InMemoryTaskStore(),
        )
        
        # Create and start server
        server = A2AStarletteApplication(
            agent_card=agent_card, 
            http_handler=request_handler
        )
        
        print(f"Starting Host Agent server on {host}:{port}")
        uvicorn.run(server.build(), host=host, port=port)
        
    except MissingAPIKeyError as e:
        print(f"Error: {e}")
        exit(1)
    except Exception as e:
        print(f"An error occurred during server startup: {e}")
        exit(1)


if __name__ == "__main__":
    main()
