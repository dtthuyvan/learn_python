from typing import Tuple, Optional, Dict
from google.adk.agents import LlmAgent
from google.adk.runners import Runner
from intent import classify_subject
from agents.employee_rag_agent.agent import employee_rag_agent
from agents.timesheet_rag_agent.agent import timesheet_rag_agent


def route_dynamic(
    prompt: str,
    session_ids: Dict[str, str],
    app_name: str,
    session_service,
) -> Tuple[Optional[Runner], Optional[LlmAgent], str, Dict]:
    subject = classify_subject(prompt)
    if subject == "employee":
        runner = Runner(agent=employee_rag_agent, app_name=app_name, session_service=session_service)
        return runner, employee_rag_agent, session_ids.setdefault("employee_rag", f"employee_rag"), {"query": prompt}
    if subject == "timesheet":
        runner = Runner(agent=timesheet_rag_agent, app_name=app_name, session_service=session_service)
        return runner, timesheet_rag_agent, session_ids.setdefault("timesheet_rag", f"timesheet_rag"), {"query": prompt}
    return None, None, "", {"message": "No matching agent"}


