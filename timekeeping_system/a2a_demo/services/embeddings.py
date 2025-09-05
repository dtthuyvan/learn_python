from typing import List
import os
from dotenv import load_dotenv
import google.generativeai as genai


_configured = False


def _ensure_configured():
    global _configured
    if _configured:
        return
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY is not set")
    genai.configure(api_key=api_key)
    _configured = True


def embed_text(text: str, model: str | None = None) -> List[float]:
    _ensure_configured()
    embedding_model = model or os.getenv("EMBEDDING_MODEL", "text-embedding-004")
    resp = genai.embed_content(model=embedding_model, content=text)
    return resp["embedding"]


