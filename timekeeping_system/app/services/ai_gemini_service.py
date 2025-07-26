import os
from google import genai
from google.genai import types
from dotenv import load_dotenv
from typing import IO

def make_request(file: IO):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY was null. Please setup.")

    csv_raw_content = file.decode("utf-8")
    config3 = types.GenerateContentConfig(
            temperature=0.2,
            thinking_config=types.ThinkingConfig(thinking_budget=0) 
        )
    message_promt = f"""As a HR of a company, you must do a report about which employees have working hour less than prescribed working hours.
    Rule of working hours: employee must have working time greater than or equal to 8 hours, not include 1.5 hours for lunch, 
    mean total time of a day must grater than or equeal to 9.5 hours.
    The conttent of timekeeping file: ```csv {csv_raw_content}```
    Let analyze and do report.
"""
    client = genai.Client()
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=message_promt,
        config=config3,
    )

    answer = response.text
    print(response)
    return answer
