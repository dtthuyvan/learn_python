import os
from typing import List, Dict
from pydantic import BaseModel, Field
from google.adk.agents import LlmAgent
import csv
import json
from google.generativeai import GenerativeModel

MODEL_NAME = "gemini-1.5-flash"

class EmployeeQueryInput(BaseModel):
    query: str = Field(description="User's query related to employee data.")

class FullAttendanceOutput(BaseModel):
    employees: List[str] = Field(description="List of employees with full attendance for the day.")

def read_employee_data(file_path: str = "employees.csv") -> List[Dict]:
    """Reads employee data from a CSV file."""
    try:
        current_dir = os.path.dirname(__file__)
        file_path = os.path.join(current_dir, file_path)
        with open(file_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            return [row for row in reader]
    except FileNotFoundError:
        print(f"File not found: {file_path}.")
        return []
    except Exception as e:
        print(f"Error reading CSV file: {str(e)}")
        return []

def get_full_attendance(date: str) -> List[str]:
    """Gets the list of employees with full attendance on a specified day."""
    print(f"\n-- Calling tool: get_full_attendance(date='{date}') --")
    employees = read_employee_data("timesheet.csv")
    jsondata = json.dumps(employees, ensure_ascii=False, indent=2)
    prompt = f"""
You are given a list of employee attendance records in JSON format. Each record includes:
- Employee Name
- Work Date (format: DD/MM/YYYY)
- Check-in Time (format: H:MM AM/PM)
- Check-out Time (format: H:MM AM/PM)

Your task:
1. Use the target date: "07/07/2025"
2. For each record on that date, calculate the total hours worked (check-out minus check-in).
3. If the total is **greater than or equal to 8 hours**, include the employee's name.
4. If no employee meets the condition, respond with **exactly**: `No one worked full hours.`

Respond only with valid JSON in the format:
{{list_of_names}}
No explanation, no formatting, no extra text, without ``` and json text.

Here is input data:
{jsondata}
"""
    model = GenerativeModel("gemini-2.5-flash")
    response = model.generate_content(prompt)
    print(response.text)
    return response.text


full_attendance_agent = LlmAgent(
    model=MODEL_NAME,
    name="full_attendance_agent",
    description="Identifies employees with full attendance for the day.",
    instruction="""You are an agent that identifies employees who worked a full 8 hours on a given day.
The user will provide a JSON query like {"query": "employees with full attendance on 2025-07-26"}.
1. Extract the date from the query.
2. Use the `get_full_attendance` tool to get the list of employees.
""",
    tools=[get_full_attendance],
    input_schema=EmployeeQueryInput,
    output_key="full_attendance_result",
)