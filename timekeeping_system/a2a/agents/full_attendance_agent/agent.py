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
        Below is a list of employee attendance records in JSON format. Each entry includes:
        - Employee Name
        - Work Date (format: YYYY-MM-DD)
        - Check-in Time (format: HH:mm)
        - Check-out Time (format: HH:mm)

        Your task:
        1. Analyze the data and find the employees who worked full hours on the date "target_date". That means their check-out time minus check-in time must be greater than or equal to 8 hours.
        2. If no employee meets the condition, respond with exactly this sentence: "No one worked full hours."
        3. If there are any, return a list of employee names who worked full hours on that date.

        JSON data:

        ```json
        {jsondata}
        """
    model = GenerativeModel("gemini-2.5-flash")
    response = model.generate_content(prompt)
    print(response.text)


full_attendance_agent = LlmAgent(
    model=MODEL_NAME,
    name="full_attendance_agent",
    description="Identifies employees with full attendance for the day.",
    instruction="""You are an agent that identifies employees who worked a full 8 hours on a given day.
The user will provide a JSON query like {"query": "employees with full attendance on 2025-07-26"}.
1. Extract the date from the query.
2. Use the `get_full_attendance` tool to get the list of employees.
3. Respond with JSON: {"employees": list[str]}.
""",
    tools=[get_full_attendance],
    input_schema=EmployeeQueryInput,
    output_key="full_attendance_result",
)

