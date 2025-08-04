import os
from google import genai
from google.genai import types
from dotenv import load_dotenv
import json

def analyze_full_time_report(data: list[dict], employees: str):
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY was null. Please setup.")

    config = types.GenerateContentConfig(
            temperature=0,
            # thinking_config=types.ThinkingConfig(thinking_budget=0), response imediately, no thinking
        )

    content_json = json.dumps(data, ensure_ascii=False, indent=2)
    prompt = f"""You are a data analysis expert.
Analyze the following JSon data to find employees who worked **less than** 9.50 hours.
Follow these steps exactly:
1. First, for EACH row in the provided data, calculate the working hours. List out the name, date, and the calculated working hours for all employees.
2. Second, from the complete list you just created in step 1, filter and create a final, clean list containing ONLY the employees whose working hours are less than 10.
3. From the list of employees provided, list out the employees name do not appear in the list from step 2.
4. Your final output should be clean list from step 3, do not inlude any other text, code and explainations, if that list is empty, just show No Employees worked full time all days 
Here is the JSon data:
{content_json}
Here is list of employees, separated by **,**: {employees}
""" 
    client = genai.Client()
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=config,
    )

    print(response)
    return response.text

def analyze_full_attendance_report(data: list[dict]):
    prompt = f"""Analyze the following JSon data and list out the employees who worked on ***all of the days** present in the dataset
Your final output should only include employee name. Do not inlude any other text, code and explainations. If no employee found just show No employess has full attendance
"""
    return make_request(data, prompt)

def analyze_gender_report(data: list[dict]):
    prompt = f"""Analyze the following JSon data and provide a breakdown of the total number of male and female employees.
The response only contains number of male and female, do not include any code, text or explainations.
"""
    return make_request(data, prompt)

def analyze_report_insufficient(data: list[dict]):
    prompt = f"""Analyze the following JSon data to find employees who worked **less than** 9.50 hours.
Follow these steps exactly:
1. First, for EACH row in the provided data, calculate the working hours. List out the name, date, and the calculated working hours for all employees.
2. Second, from the complete list you just created in step 1, filter and create a final, clean list containing ONLY the employees whose working hours are less than 10.
3. Your final output should only be the clean list from step 2, formatted as table, include: no., employee name, date, and working hour, do not include any other text, code, or explanations. Do not show your work from step 1.
""" 
    return make_request(data, prompt)

def make_request(data: list[dict], original_prompt):
    if not original_prompt:
        return "No prompt"
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY was null. Please setup.")

    config = types.GenerateContentConfig(
            temperature=0,
            # thinking_config=types.ThinkingConfig(thinking_budget=0), response imediately, no thinking
        )

    final_results_text = ""
    chunk_size = 100  
    for i in range(0, len(data), chunk_size):
        chunk_data = data[i:i + chunk_size]
        chunk_json = json.dumps(chunk_data, ensure_ascii=False, indent=2)
        prompt = f"""You are a data analysis expert.
{original_prompt}
Here is the JSon data:
{chunk_json}
""" 
        client = genai.Client()
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=config,
        )

        final_results_text += response.text + "\n"
        print(response)
    return final_results_text
