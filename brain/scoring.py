from typing import Any, Dict, List

from thefuzz import fuzz


def calculate_orbit_score(cv_data: Dict[str, Any], job_requirements: List[str]) -> Dict[str, Any]:
    """Calculate an orbit score using anti-gaming rules."""
    total_score = 0
    breakdown: List[str] = []

    years_experience = cv_data.get("years_experience", 0) or 0
    try:
        years_experience = int(years_experience)
    except (TypeError, ValueError):
        years_experience = 0
    experience_points = min(max(years_experience, 0), 10) * 10
    total_score += experience_points
    breakdown.append(f"Experience: {experience_points} pts")

    projects = cv_data.get("projects", []) or []
    project_points = 0
    for project in projects:
        complexity = ""
        if isinstance(project, dict):
            complexity = str(project.get("complexity", "")).upper()
        if complexity == "HIGH":
            project_points += 25
        elif complexity == "MED":
            project_points += 15
        elif complexity == "LOW":
            project_points += 5
    total_score += project_points
    breakdown.append(f"Projects: {project_points} pts")

    skills = cv_data.get("skills", []) or []
    skill_points = 0
    if isinstance(skills, list) and isinstance(job_requirements, list):
        for requirement in job_requirements:
            for skill in skills:
                if fuzz.partial_ratio(str(skill).lower(), str(requirement).lower()) > 80:
                    skill_points += 20
                    break
    total_score += skill_points
    breakdown.append(f"Skills: {skill_points} pts")

    certifications = cv_data.get("certifications", []) or []
    cert_points = 0
    if isinstance(certifications, list):
        for index, _ in enumerate(certifications):
            if index == 0:
                cert_points += 15
            elif index == 1:
                cert_points += 10
            elif index == 2:
                cert_points += 5
            else:
                cert_points += 0
    total_score += cert_points
    breakdown.append(f"Certifications: {cert_points} pts")

    return {"total_score": int(total_score), "breakdown": breakdown}
