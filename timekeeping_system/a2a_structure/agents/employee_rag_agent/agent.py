from typing import List, Dict, Any
from pydantic import BaseModel, Field
from google.adk.agents import LlmAgent
from services.embeddings import embed_text
from services.vector_search import vector_search


MODEL_NAME = "gemini-2.5-flash"


class EmployeeRagInput(BaseModel):
    query: str = Field(description="Natural language query about employee information")


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


employee_rag_agent = LlmAgent(
    model=MODEL_NAME,
    name="employee_rag_agent",
    description="RAG agent for employee subject using MongoDB vector search",
    instruction=(
        '''"You are an expert HR assistant. 
For any query about employees, always call the tool `search_employee` first to retrieve the most relevant documents from MongoDB (already embedded). 
Use only the retrieved documents as your single source of truth. 
When processing and matching, pay special attention to keywords and phrases related to: 
- name (employee name, full name, first name, last name)
- gender (male, female, other)
- date of birth (dob, birth date, birthday)
- team (team name, department, group)

From these documents, extract only the above fields and use them to answer the user's question. 
Summarize the findings and respond accurately and concisely, without adding any external or assumed information."
'''
    ),
    tools=[search_employee],
    input_schema=EmployeeRagInput,
    output_key="employee_rag_result",
)