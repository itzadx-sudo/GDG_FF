import os
from typing import Any, Dict

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_groq import ChatGroq


def generate_boss_fight(cv_data: Dict[str, Any]) -> str:
    """Generate a Space42 Satellite Crisis interview scenario using a candidate weakness."""
    weakness = ""
    if isinstance(cv_data, dict):
        weakness = str(cv_data.get("weakness", "") or "").strip()
    if not weakness:
        weakness = "an unclear technical gap around core systems troubleshooting"

    system_prompt = (
        "You are a dramatic technical interviewer. Create a Space42 Satellite Crisis scenario "
        "based on the candidate weakness provided. The output must be vivid, urgent, and "
        "present ONE specific technical question the candidate must answer to fix the crisis. "
        "Keep it concise: 1-2 short paragraphs followed by the question."
    )
    human_prompt = f"Candidate weakness: {weakness}\nGenerate the crisis scenario now."

    llm = ChatGroq(
        groq_api_key=os.getenv("GROQ_API_KEY"),
        model_name="llama3-70b-8192",
    )

    response = llm.invoke(
        [SystemMessage(content=system_prompt), HumanMessage(content=human_prompt)]
    )
    return response.content if hasattr(response, "content") else str(response)
