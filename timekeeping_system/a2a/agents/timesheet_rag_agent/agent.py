from typing import List, Dict, Any
from pydantic import BaseModel, Field
from google.adk.agents import LlmAgent
from services.embeddings import embed_text
from services.vector_search import vector_search


MODEL_NAME = "gemini-2.5-flash"


class TimesheetRagInput(BaseModel):
    query: str = Field(description="Natural language query about timesheet/timekeeping records")


def search_timesheet(query: str) -> List[Dict[str, Any]]:
    embedding = embed_text(query)
    results = vector_search(
        collection_name="timesheet_train",
        query_embedding=embedding,
        top_k=100,
        embedding_field="embedding",
    )
    for r in results:
        r.pop("embedding", None)
    return results


timesheet_rag_agent = LlmAgent(
    model=MODEL_NAME,
    name="timesheet_rag_agent",
    description="RAG agent for timesheet queries using MongoDB vector search",
    instruction=(
        "You are an assistant specialized in analyzing timesheet and attendance data. "
        "Your primary tool is `search_timesheet`, which retrieves the most relevant records from MongoDB (already embedded). "
        "Use only the retrieved records for your calculations—do not invent or assume missing data. "
        "If the retrieved set is empty but the query relates to attendance definitions "
        "(e.g., 'on time', 'late', 'full hours', 'hardworking', 'OT'), you must immediately call "
        "`search_timesheet` again with a broader query such as 'all timesheet records for [date range]' "
        "so you can filter and apply the definitions yourself. "
        "Definitions: "
        "- An employee is considered 'on time' if they check in before 8:30 AM; otherwise, they are 'late'. "
        "- An employee has worked 'full hours' if the total time between check-in and check-out is at least 9 hours. "
        "- A 'hardworking' employee is one who works full hours or more. "
        "- An employee is OT if they check out **after** 5:00 PM"
        "You can compute aggregates, totals, averages, durations, or generate lists strictly from retrieved records. "
        "Typical tasks include analyzing check-in/check-out times, total hours worked, late arrivals, absences, overtime, "
        "on-time rates, and productivity trends. "
        "Respond concisely and focus on the requested statistics or insights."
    ),
    tools=[search_timesheet],
    input_schema=TimesheetRagInput,
    output_key="timesheet_rag_result",
)

