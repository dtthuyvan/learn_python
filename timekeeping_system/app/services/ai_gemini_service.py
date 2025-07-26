import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

def make_request(message):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY was null. Please setup.")

    config1 = types.GenerateContentConfig(
            temperature= 2,
            thinking_config=types.ThinkingConfig(thinking_budget=0), # Disables thinking
            max_output_tokens=200,
            #top_k=40,
            top_p=1
        )
    config3 = types.GenerateContentConfig(
            temperature=0.2,
            thinking_config=types.ThinkingConfig(thinking_budget=0) 
        )
    message_promt = f"""answer message from user, if you don't know, just say I don't know, the message of user is `{message}`"""
    client = genai.Client()
    response = client.models.generate_content(
        model="gemini-2.5-pro",
        contents=message_promt,
        config=config3,
    )

    answer = response.text
    print(response)
    return answer
