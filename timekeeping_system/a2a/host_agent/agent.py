import json
import asyncio
import os
import sys
from dotenv import load_dotenv
import google.generativeai as genai
from google.adk.agents import LlmAgent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from pydantic import BaseModel, Field
import uuid
from datetime import date
from fastapi import FastAPI, Request
import uvicorn
from fastapi.responses import JSONResponse
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from agents.gender_count_agent.agent import gender_count_agent
from agents.full_attendance_agent.agent import full_attendance_agent
from agents.insufficient_working_time_agent.agent import insufficient_employee_report_agent
from fastapi.middleware.cors import CORSMiddleware
from router import route_dynamic

# --- Configure Google API Key ---
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY is not set in environment variables or .env file.")
genai.configure(api_key=api_key)
print("Google API Key configured.")

# ---  Define Constants ---
APP_NAME = "employee_analysis_app"
USER_ID = "test_user_789"
MODEL_NAME = "gemini-1.5-flash"
SESSION_IDS = {
    "gender_count": f"gender_count_{uuid.uuid4()}",
    "full_attendance": f"full_attendance_{uuid.uuid4()}",
    "absent_without_leave": f"absent_without_leave_{uuid.uuid4()}",
    "insufficient_time" : f"insufficient_time{uuid.uuid4()}",
    "employee_rag": f"employee_rag_{uuid.uuid4()}",
    "timesheet_rag": f"timesheet_rag_{uuid.uuid4()}",
}

# --- Define Schemas ---
class EmployeeQueryInput(BaseModel):
    query: str = Field(description="User's query related to employee data.")

# --- Set up Session Management and Runner ---
session_service = InMemorySessionService()

async def create_session_with_check(session_id: str):
    try:
        await session_service.create_session(app_name=APP_NAME, user_id=USER_ID, session_id=session_id)
        session = await session_service.get_session(app_name=APP_NAME, user_id=USER_ID, session_id=session_id)
        if session:
            print(f"Session '{session_id}' created successfully.")
        else:
            raise ValueError(f"Could not create session '{session_id}'")
    except Exception as e:
        print(f"Error creating session '{session_id}': {str(e)}")
        raise

async def init_sessions():
    for session_id in SESSION_IDS.values():
        await create_session_with_check(session_id)

gender_count_runner = Runner(
    agent=gender_count_agent,
    app_name=APP_NAME,
    session_service=session_service
)

full_attendance_runner = Runner(
    agent=full_attendance_agent,
    app_name=APP_NAME,
    session_service=session_service
)

insufficient_working_hour_runner = Runner(
    agent=insufficient_employee_report_agent,
    app_name=APP_NAME,
    session_service=session_service
)

def classify_intent_with_gemini(prompt: str) -> str:
    model = genai.GenerativeModel(MODEL_NAME)
    response = model.generate_content(
    f"""You are an intelligent router that classifies the user prompt into one of these task types: 
        - 'gender_count' 
        - 'full_attendance' 
        - 'insufficient_working_hour'
        - 'absent_without_leave'.
        Based on the prompt: '{prompt}', return only the task type name (e.g., 'gender_count') if it clearly matches one of the supported tasks.
        If none of the supported tasks match, return a brief, context-aware explanation of why the task is unsupported and clearly state that no matching agent is available."""
    )
    return response.text.strip()

# --- Prompt Analysis and Routing Function ---
async def analyze_prompt_and_route(prompt: str) -> tuple[Runner, LlmAgent, str, dict]:
    try:
        task = classify_intent_with_gemini(prompt)
        today = date.today().isoformat()
        
        if task == "gender_count":
            query = {"query": "count male and female employees"}
            return gender_count_runner, gender_count_agent, SESSION_IDS["gender_count"], query
        elif task == "full_attendance":
            query = {"query": f"employees with full attendance on {today}"}
            return full_attendance_runner, full_attendance_agent, SESSION_IDS["full_attendance"], query
        elif task == "insufficient_working_hour":
            query = {"query": "List of employees who have not met the required working hours per day"}
            return insufficient_working_hour_runner, insufficient_employee_report_agent, SESSION_IDS["insufficient_time"], query
        else:
            return None, None, "", task
    except Exception as e:
        print(f"Error analyzing prompt: {str(e)}")
        raise

# --- Define Agent Interaction Logic ---
async def call_agent_and_print(runner_instance: Runner, agent_instance: LlmAgent, session_id: str, query_json: dict):
    """Sends a query to the agent/runner and prints the result."""
    query_str = json.dumps(query_json)
    print(f"\n>>> Calling Agent: '{agent_instance.name}' | Query: {query_str}")

    try:
        session = await session_service.get_session(app_name=APP_NAME, user_id=USER_ID, session_id=session_id)
        if not session:
            raise ValueError(f"Session '{session_id}' not found before running the agent.")
    except Exception as e:
        print(f"Error accessing session '{session_id}': {str(e)}")
        return

    user_content = types.Content(role='user', parts=[types.Part(text=query_str)])
    final_response_content = "No final response received."

    try:
        async for event in runner_instance.run_async(user_id=USER_ID, session_id=session_id, new_message=user_content):
            if event.is_final_response() and event.content and event.content.parts:
                final_response_content = event.content.parts[0].text
    except Exception as e:
        print(f"Error executing agent: {str(e)}")
        return

    print(f"<<< Agent Response '{agent_instance.name}': {final_response_content}")

    # Validate output based on agent
    # try:
    #     parsed_output = json.loads(final_response_content)
    #     if agent_instance.name == "gender_count_agent":
    #         GenderCountOutput(**parsed_output)
    #     elif agent_instance.name == "full_attendance_agent":
    #         FullAttendanceOutput(**parsed_output)
    #     print(f"--- Output validated against the schema of {agent_instance.name} ---")
    # except Exception as e:
    #     print(f"Error validating output: {str(e)}")

    try:
        current_session = await session_service.get_session(app_name=APP_NAME, user_id=USER_ID, session_id=session_id)
        stored_output = current_session.state.get(agent_instance.output_key)
        print(f"--- Session State ['{agent_instance.output_key}']: ", end="")
        try:
            parsed_output = json.loads(stored_output)
            print(json.dumps(parsed_output, indent=2))
        except (json.JSONDecodeError, TypeError):
            print(stored_output)
        return stored_output
    except Exception as e:
        print(f"Error accessing session state: {str(e)}")
    print("-" * 30)

# --- Main Function ---
async def main():
    await init_sessions()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:8000"],  # Allow your frontend origin
    allow_credentials=True,
    allow_methods=["POST", "OPTIONS"],  # Allow POST and OPTIONS (for preflight)
    allow_headers=["Content-Type"],  # Allow Content-Type header
)

@app.post("/prompt")
async def handle_promt(req: Request):
    data = await req.json()
    prompt = data["prompt"]
    print(f"\n=== Processing prompt: '{prompt}' ===")
    try:
        # First try dynamic RAG routing based on subject
        runner, agent, session_id, query = route_dynamic(prompt, SESSION_IDS, APP_NAME, session_service)
        if not runner:
            # fallback to legacy task-based router
            runner, agent, session_id, query = await analyze_prompt_and_route(prompt)
        result = query
        if (runner):
            result = await call_agent_and_print(runner, agent, session_id, query)
        return JSONResponse(content=result)
    except Exception as e:
        print(f"Error processing prompt '{prompt}': {str(e)}")
        return JSONResponse(content="Error!")

def start_server():
    uvicorn.run("__main__:app", host="127.0.0.1", port=10000)

if __name__ == "__main__":
    asyncio.run(main())
    start_server()