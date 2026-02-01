from typing import Any, Dict, List
# NOTE: User must run `pip install thefuzz`
from thefuzz import fuzz

def calculate_orbit_score(cv_data: Dict[str, Any], job_requirements: List[str]) -> Dict[str, Any]:
    """Calculate an orbit score using anti-gaming rules."""
    total_score = 0
    breakdown: List[str] = []

    # 1. Experience
    years_experience = cv_data.get("years_experience", 0) or 0
    try:
        years_experience = int(years_experience)
    except (TypeError, ValueError):
        years_experience = 0
    
    # Cap experience points at 10 years * 10 points
    experience_points = min(max(years_experience, 0), 10) * 10
    total_score += experience_points
    breakdown.append(f"Experience: {experience_points} pts")

    # 2. Projects Complexity
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
            
    # Cap project points to avoid runaway scores
    project_points = min(project_points, 100)
    total_score += project_points
    breakdown.append(f"Projects: {project_points} pts")

    # 3. Skills Fuzzy Matching
    skills = cv_data.get("skills", []) or []
    skill_points = 0
    if isinstance(skills, list) and isinstance(job_requirements, list):
        for requirement in job_requirements:
            for skill in skills:
                # Fuzzy match > 80%
                if fuzz.partial_ratio(str(skill).lower(), str(requirement).lower()) > 80:
                    skill_points += 20
                    break
    
    skill_points = min(skill_points, 100)
    total_score += skill_points
    breakdown.append(f"Skills: {skill_points} pts")

    # 4. Certifications
    certifications = cv_data.get("certifications", []) or []
    cert_points = 0
    if isinstance(certifications, list):
        # Diminishing returns for certs
        if len(certifications) >= 1: cert_points += 15
        if len(certifications) >= 2: cert_points += 10
        if len(certifications) >= 3: cert_points += 5
        
    total_score += cert_points
    breakdown.append(f"Certifications: {cert_points} pts")

    return {"total_score": int(total_score), "breakdown": breakdown}