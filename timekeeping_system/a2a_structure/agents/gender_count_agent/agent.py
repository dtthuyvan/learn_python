import os
from typing import List, Dict
from pydantic import BaseModel, Field
from google.adk.agents import LlmAgent
import csv

MODEL_NAME = "gemini-2.5-flash"

class EmployeeQueryInput(BaseModel):
    query: str = Field(description="User's query related to employee data.")

class GenderCountOutput(BaseModel):
    male_count: int = Field(description="Number of male employees.")
    female_count: int = Field(description="Number of female employees.")

def get_gender_count() -> Dict[str, int]:
    """Counts the number of male and female employees from CSV data."""
    print("\n-- Calling tool: get_gender_count --")
    employees = read_employee_data()
    male_count = sum(1 for emp in employees if emp.get('gender', '').lower() == 'male')
    female_count = sum(1 for emp in employees if emp.get('gender', '').lower() == 'female')
    result = {"male_count": male_count, "female_count": female_count}
    print(f"-- Tool result: {result} --")
    return result

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

gender_count_agent = LlmAgent(
    model=MODEL_NAME,
    name="gender_count_agent",
    description="Counts the number of male and female employees.",
    instruction="""You are an agent that counts the number of male and female employees.
The user will provide a JSON query like {"query": "count male and female employees"}.
1. Use the `get_gender_count` tool to get the count.
2. Respond with JSON: {"male_count": int, "female_count": int}.
""",
    tools=[get_gender_count],
    input_schema=EmployeeQueryInput,
    output_key="gender_count_result",
)