import os
import json
import uuid
import logging
import httpx

from dotenv import load_dotenv
from a2a.client import A2ACardResolver
from a2a.types import (
    AgentCard, Message, TextPart,
    MessageSendConfiguration, MessageSendParams,
    SendMessageRequest, SendMessageResponse,
    Task, TaskState
)
from google.adk import Agent
from google.adk.agents.readonly_context import ReadonlyContext
from google.adk.agents.callback_context import CallbackContext
from google.adk.tools.tool_context import ToolContext
from google.genai import types
from google import genai

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

load_dotenv()

class HostAgent:
    def __init__(self):
        self._setup_api_key()
        self.httpx_client = httpx.AsyncClient(timeout=30)
        self.remote_agent_connections = {}
        self.cards = {}
        self.agents = ''
        self.client = genai.Client()

    def _setup_api_key(self):
        """Set up the Google API key for the agent."""
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY is not set in environment variables or .env file.")
            
    async def init_remote_agent_addresses(self, remote_agent_addresses: list[str]):
        for address in remote_agent_addresses:
            await self.retrieve_card(address)

    async def retrieve_card(self, address: str):
        resolver = A2ACardResolver(self.httpx_client, address)
        card = await resolver.get_agent_card()
        self.cards[card.name] = card
        self.remote_agent_connections[card.name] = address  # dummy store
        self.agents = '\n'.join(
            json.dumps({"name": c.name, "desc": c.description}) for c in self.cards.values()
        )

    def create_agent(self) -> Agent:
        
        return Agent(
            model="gemini-2.5-flash",
            name="host_agent",
            instruction=self.root_instruction,
            before_model_callback=self.before_model_callback,
            description="Simple Host Agent orchestrator",
            tools=[self.send_message],
            client=self.client
        )

    def root_instruction(self, context: ReadonlyContext) -> str:
        return f"""
**Delegation Rule (POC)**
- 'download' → DownloadAgent
- 'summarize' → SummaryAgent

Available Agents:
{self.agents}
"""

    def before_model_callback(self, callback_context: CallbackContext, llm_request):
        state = callback_context.state
        if "session_active" not in state:
            state["session_active"] = True

    async def send_message(self, agent_name: str, message: str, tool_context: ToolContext):
        if agent_name not in self.remote_agent_connections:
            raise ValueError(f"Agent {agent_name} not registered")

        logger.info(f"[HOST_AGENT] Sending '{message}' to {agent_name}")
        # fake response
        return {"echo": message, "target_agent": agent_name, "status": "sent"}
