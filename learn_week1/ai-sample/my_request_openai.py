from openai import OpenAI
import os

def make_request(message):
    openai_key = os.getenv("OPEN_AI_KEY")
    if not openai_key:
        raise ValueError("OPEN_AI_KEY was null. Please setup.")

    client = OpenAI(
        api_key=openai_key
    )

    #developer_msg = """You explain concepts in dept using simple term. and you give examples to help people learn.
    #At the end of each explanation, you ask a question to check understanding."""
    developer_msg = "just answer you don't know about it"
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.5,
        messages=[
            {"role": "system", "content": "You are smart assistant, you know everything."},
            {"role": "developer", "content": developer_msg},
            {"role": "user", "content": message}
        ],
        max_tokens=200
    )

    result = completion
    print(result)
    return result.choices[0].message.content
