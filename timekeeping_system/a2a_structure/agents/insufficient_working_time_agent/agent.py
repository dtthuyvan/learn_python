import os
import sys
from typing import List, Dict
from pydantic import BaseModel, Field
from google.adk.agents import LlmAgent
from datetime import datetime, timedelta

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from agents.insufficient_working_time_agent.core.database import get_database, get_timekeeping_tracking_collection, get_employee_collection
from models.timekeeping import serialize_timekeeping

MODEL_NAME = "gemini-2.5-flash"

def load_data():
    db = get_database()
    timekeeping_collection = get_timekeeping_tracking_collection(db)
    data = [serialize_timekeeping(t) for t in timekeeping_collection.find()]
    for item in data:
        item.pop('id', None)
    return data

DATA_TIMEKEEPING = load_data()

class QueryInput(BaseModel):
    query: str = Field(description="User's query related to insufficient working hours.")

class ResultOutput(BaseModel):
    name: str = Field(description="Name of employees.")
    hour: float = Field(description="Actual working hour.")

def find_insufficient_employee() -> List[str]:
    print("\n-- Calling tool: find_insufficient_employee --")
    if(not DATA_TIMEKEEPING):
        return None
    
    incomplete_workdays : List[str] = []
    i = 0
    for record in DATA_TIMEKEEPING:
        i+=1
        try:
            check_in_str = f"{record['date']} {record['checkin']}"
            check_out_str = f"{record['date']} {record['checkout']}"
            
            check_in_time = datetime.strptime(check_in_str, "%d/%m/%Y %I:%M %p")
            check_out_time = datetime.strptime(check_out_str, "%d/%m/%Y %I:%M %p")
            duration = check_out_time - check_in_time
            
            if duration < timedelta(hours=9.5):
                time = duration.total_seconds()/3600 - 1.5
                result = f"{i}. Employee Name: {record['name']} | Date: {record['date']} | Working Time: {time}"
                incomplete_workdays.append(result)

        except (ValueError, KeyError) as e:
            print(f"Skip record: {record}. Exception: {e}")
            continue
    print(incomplete_workdays)
    return incomplete_workdays

insufficient_employee_report_agent = LlmAgent(
    model=MODEL_NAME,
    name="insufficient_employee_report_agent", 
    description="Identifying Employees with Insufficient Daily Working Hours.",
    instruction="""You are a helpful assistant for HR-related queries.
Your task is to analyze employee timekeeping data and generate a list of employees who have not met the minimum required working hours per day.
The minimum required working hours per day is 8, not include 1.5 hours for lunch time.
The user will provide a JSON query like {"query": "List of employees who have not met the required working hours per day"}.
1. Use the `find_insufficient_employee` tool to get result.
2. Respond in plaint text, new line for each item in list.
""",
    tools=[find_insufficient_employee],
    input_schema=QueryInput,
    output_key="insufficient_result",
)