from typing import List, Dict, Any
from services.embeddings import embed_text
from services.vector_search import vector_search
from google.adk.agents import LlmAgent


def search_employee(query: str) -> List[Dict[str, Any]]:
    embedding = embed_text(query)
    results = vector_search(
        collection_name="x_employee_train",
        query_embedding=embedding,
        top_k=200,
        embedding_field="embedding",
    )
    for r in results:
        r.pop("embedding", None)
    return results


def create_agent() -> LlmAgent:
    """Constructs the ADK agent for Employee."""
    return LlmAgent(
        model="gemini-2.5-flash",
        name="Employee_Agent",
        instruction="""
            **Role:** You are an expert HR assistant. 
            Your sole responsibility is to respond to inquiries about the employees.

            **Core Directives:**

            ***Check Availability:** Use the `search_employee` tool to determine 
                if Employee is free on a requested date or over a range of dates. 
                The tool requires a `query`. 
            ***Polite and Concise:** Always be polite and to the point in your responses.
            ***Stick to Your Role:** Do not engage in any conversation outside of HR. 
                    If asked other questions, politely state that you can only help with HR.
        """,
        tools=[search_employee],
    )