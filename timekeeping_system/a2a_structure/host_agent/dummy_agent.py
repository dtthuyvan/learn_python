# dummy_agent.py
from a2a.types import AgentCard

async def get_agent_card():
    return AgentCard(name="SummaryAgent", description="Summarizes text")

async def send_message(request):
    return {"response": f"SummaryAgent got: {request}"}
