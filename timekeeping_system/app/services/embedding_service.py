from typing import Dict, Any
from dotenv import load_dotenv
import os
from google import genai
from google.genai import types


def embed_text(text: str) -> list[float]:
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY was null. Please setup.")
    model_name = os.getenv("EMBEDDING_MODEL", "text-embedding-004")
    client = genai.Client()
    resp = client.models.embed_content(model=model_name, contents=text)
    return resp.embeddings[0].values


def build_employee_embedding_doc(employee: Dict[str, Any]) -> Dict[str, Any]:
    name = str(employee.get("name", "")).strip()
    dob = str(employee.get("dob", "")).strip()
    team = str(employee.get("team", "")).strip()
    gender = str(employee.get("gender", "")).strip().title()

    text = f"Name: {name} | Date of Birth: {dob} | Team: {team} | Gender: {gender}"

    return {
        "name": name,
        "dob": dob,
        "team": team,
        "gender": gender,
        "embedding": embed_text(text),
    }

def build_timesheet_embedding_doc(timesheet: Dict[str, Any]) -> Dict[str, Any]:
    name = str(timesheet.get("name", "")).strip()
    date = str(timesheet.get("date", "")).strip()
    checkin = str(timesheet.get("checkin", "")).strip()
    checkout = str(timesheet.get("checkout", "")).strip().title()

    text = f"Name: {name} | Date: {date} | Checkin: {checkin} | Checkout: {checkout}"

    return {
        "name": name,
        "date": date,
        "checkin": checkin,
        "checkout": checkout,
        "embedding": embed_text(text),
    }