import json
import os
import re
from typing import Any, Dict

from PyPDF2 import PdfReader
from google import genai
from google.genai import types

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
    """Parse a PDF or text resume into a structured JSON-compatible dictionary."""
    resume_text = ""
    
    try:
        # Try PDF first
        if pdf_path.lower().endswith('.pdf'):
            reader = PdfReader(pdf_path)
            text_parts = [page.extract_text() or "" for page in reader.pages]
            resume_text = "\n".join(text_parts).strip()
        else:
            # Handle text files (for testing)
            print(f"[Parser] Reading text file: {pdf_path}")
            with open(pdf_path, 'r', encoding='utf-8') as f:
                resume_text = f.read().strip()
        
        if not resume_text:
            print("[Parser] ERROR: No text extracted from file")
            return DEFAULT_RESUME_JSON.copy()
            
        print(f"[Parser] Extracted {len(resume_text)} characters from resume")
        
    except Exception as e:
        print(f"[Parser] ERROR reading file: {e}")
        return DEFAULT_RESUME_JSON.copy()

    # Configure and use the new Gemini API
    client = genai.Client(api_key="AIzaSyC_YeBD5sbi9Urf1OeNqIovVYw97EEF3nQ")
    
    prompt = f"""You are a resume parsing engine. Extract structured data from the resume text and return ONLY valid JSON with the following schema:
{{
  "name": "string",
  "email": "string", 
  "years_experience": integer,
  "skills": ["list", "of", "strings"],
  "certifications": ["list", "of", "strings"],
  "projects": [
    {{"name": "string", "description": "string", "complexity": "HIGH|MED|LOW"}}
  ],
  "weakness": "inferred technical gap as a string"
}}

Resume text:
{resume_text}

Return only the JSON, no markdown, no explanations, no code fences."""

    try:
        print("[Parser] Calling Gemini API for resume analysis...")
        response = client.models.generate_content(
            model='gemini-flash-latest',
            contents=prompt
        )
        raw_content = response.text
        
        print(f"[Parser] Gemini response received ({len(raw_content)} chars)")
        
        cleaned = _strip_json_fence(raw_content)
        parsed = json.loads(cleaned)
        normalized = _normalize_resume_data(parsed)
        
        print(f"[Parser] SUCCESS: Parsed {len(normalized.get('skills', []))} skills, " 
              f"{normalized.get('years_experience', 0)} years exp")
        return normalized
    except json.JSONDecodeError as e:
        print(f"[Parser] ERROR: Invalid JSON from Gemini: {e}")
        print(f"[Parser] Response snippet: {raw_content[:200] if 'raw_content' in locals() else 'N/A'}")
        return DEFAULT_RESUME_JSON.copy()
    except Exception as e:
        print(f"[Parser] ERROR in Gemini call: {e}")
        return DEFAULT_RESUME_JSON.copy()