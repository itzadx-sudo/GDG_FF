import json
import os
import re
from typing import Any, Dict

from PyPDF2 import PdfReader
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_groq import ChatGroq

DEFAULT_RESUME_JSON: Dict[str, Any] = {
    "name": "",
    "email": "",
    "years_experience": 0,
    "skills": [],
    "certifications": [],
    "projects": [],
    "weakness": "",
}


def _strip_json_fence(text: str) -> str:
    """Remove markdown JSON fences and surrounding whitespace."""
    if not text:
        return ""
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r"\s*```$", "", cleaned)
    return cleaned.strip()


def _normalize_resume_data(data: Any) -> Dict[str, Any]:
    """Ensure the parsed resume data matches the expected structure."""
    normalized: Dict[str, Any] = DEFAULT_RESUME_JSON.copy()
    if isinstance(data, dict):
        for key in normalized:
            if key in data:
                normalized[key] = data[key]
    try:
        normalized["years_experience"] = int(normalized.get("years_experience", 0) or 0)
    except (TypeError, ValueError):
        normalized["years_experience"] = 0
    for list_key in ["skills", "certifications", "projects"]:
        if not isinstance(normalized.get(list_key), list):
            normalized[list_key] = []
    if not isinstance(normalized.get("weakness"), str):
        normalized["weakness"] = ""
    if not isinstance(normalized.get("name"), str):
        normalized["name"] = ""
    if not isinstance(normalized.get("email"), str):
        normalized["email"] = ""
    return normalized


def parse_resume_to_json(pdf_path: str) -> Dict[str, Any]:
    """Parse a PDF resume into a structured JSON-compatible dictionary."""
    try:
        reader = PdfReader(pdf_path)
        text_parts = [page.extract_text() or "" for page in reader.pages]
        resume_text = "\n".join(text_parts).strip()
        if not resume_text:
            return DEFAULT_RESUME_JSON.copy()
    except Exception:
        return DEFAULT_RESUME_JSON.copy()

    system_prompt = (
        "You are a resume parsing engine. Extract structured data from the resume text "
        "and return ONLY valid JSON with the following schema: "
        "{\"name\": string, \"email\": string, \"years_experience\": int, "
        "\"skills\": list of strings, \"certifications\": list of strings, "
        "\"projects\": list of objects with fields {\"name\": string, \"description\": string, "
        "\"complexity\": one of [HIGH, MED, LOW]}, \"weakness\": string inferred technical gap}. "
        "Do not include markdown, explanations, or code fences. Return pure JSON only."
    )
    human_prompt = f"Resume text:\n{resume_text}\n\nReturn only JSON."

    llm = ChatGroq(
        groq_api_key=os.getenv("GROQ_API_KEY"),
        model_name="llama3-70b-8192",
    )

    try:
        response = llm.invoke(
            [SystemMessage(content=system_prompt), HumanMessage(content=human_prompt)]
        )
        raw_content = response.content if hasattr(response, "content") else str(response)
        cleaned = _strip_json_fence(raw_content)
        parsed = json.loads(cleaned)
        return _normalize_resume_data(parsed)
    except Exception:
        return DEFAULT_RESUME_JSON.copy()
