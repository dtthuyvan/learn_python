import random
from datetime import date, datetime, timedelta
from typing import List, Dict, Any
from services.embeddings import embed_text
from services.vector_search import vector_search
from google.adk.agents import LlmAgent


def search_timesheet(query: str) -> List[Dict[str, Any]]:
    embedding = embed_text(query)
    results = vector_search(
        collection_name="x_timesheet_train",
        query_embedding=embedding,
        top_k=100,
        embedding_field="embedding",
    )
    for r in results:
        r.pop("embedding", None)
    return results


def create_agent() -> LlmAgent:
    """Constructs the ADK agent for Employee."""
    return LlmAgent(
        model="gemini-2.5-flash",
        name="TimeSheet_Agent",
        instruction="""
            **Role:** You are TimeSheet's personal scheduling assistant. 
            Your sole responsibility is to manage her calendar and respond to inquiries 
            about her availability for time tracking and attendance.

            **Core Directives:**

            *   **Check Availability:** Use the `get_timesheet_availability` tool to determine 
                    if TimeSheet is free on a requested date or over a range of dates. 
                    The tool requires a `start_date` and `end_date`. If the user only provides 
                    a single date, use that date for both the start and end.
            *   **Polite and Concise:** Always be polite and to the point in your responses.
            *   **Stick to Your Role:** Do not engage in any conversation outside of scheduling. 
                    If asked other questions, politely state that you can only help with time tracking and attendance.
        """,
        tools=[search_timesheet],
    )