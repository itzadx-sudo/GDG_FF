import random

def get_missions():
    return [
        {"id": "sat-01", "title": "Satellite Systems Engineer", "dept": "Orbital Ops", "loc": "Mars-1"},
        {"id": "ai-04", "title": "AI Ethics Architect", "dept": "Cybernetics", "loc": "Earth-Delta"},
        {"id": "prop-11", "title": "Fusion Propulsion Lead", "dept": "Heavy Lift", "loc": "Luna Gate"},
    ]

def get_fleet():
    return [
        {"name": "VANGUARD-01", "type": "Weather Ops", "alt": "35,000km", "status": "ACTIVE"},
        {"name": "OBSIDIAN-IX", "type": "Deep Relay", "alt": "120,000km", "status": "NOMINAL"},
        {"name": "NEXUS-X", "type": "Global Net", "alt": "2,000km", "status": "CALIBRATING"}
    ]

def analyze_candidate(name, skills):
    # Member 2 + 3 simulation
    score = random.randint(82, 98)
    return {
        "name": name,
        "score": score,
        "weakness": "PID Controller Calibration for Sat-Drift",
        "matrix": [random.randint(50, 100) for _ in range(5)],
        "id": random.randint(1000, 9999)
    }