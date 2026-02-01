import dash
from dash import dcc, html, Input, Output, State, callback_context, no_update, ALL, MATCH
import dash_bootstrap_components as dbc
import base64
import threading
import json
import os
import time
import datetime
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_groq import ChatGroq

# =============================================================================
# BACKEND SETUP & AI AGENT
# =============================================================================
try:
    import database
    import airlock
    import parser_SIB
    import scoring
    import holodeck
    from flask import send_file
    # Ensure database is initialized
    if hasattr(database, 'init_db'):
        database.init_db()
except ImportError as e:
    print(f"⚠️ CRITICAL: Backend failed to load. {e}")
    database = None

# AI Chat Agent using Groq
class AIAgent:
    def __init__(self):
        self.api_key = "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" 
        try:
            self.llm = ChatGroq(groq_api_key=self.api_key, model_name="llama-3.3-70b-versatile")
            self.online = True
        except:
            self.online = False

    def ask(self, query, context=""):
        if not self.online:
            return "Neural Core Offline. I cannot process queries right now."
        
        # Enhanced system prompt with job database access
        system_prompt = (
            "You are 'Orbital', the AI Recruitment Agent for Space42's Satellite Operations Portal. "
            "You are helpful, professional, and knowledgeable about aerospace careers. "
            "You have access to the complete job database and can help candidates find suitable positions. "
            "When asked about jobs, provide specific details from the database including job titles, departments, "
            "requirements, and descriptions. Keep responses concise (under 150 words) and use space/aerospace terminology. "
            "If asked about a specific job, provide details. If asked about job categories or skills, recommend relevant positions."
        )
        
        # Prepare job database context for AI queries
        job_context = self._prepare_job_context(query)
        human_prompt = f"Available Jobs Context: {job_context}\n\nUser Context: {context}\n\nUser Question: {query}"
        
        try:
            res = self.llm.invoke([SystemMessage(content=system_prompt), HumanMessage(content=human_prompt)])
            return res.content
        except Exception as e:
            return f"Comms Error: {str(e)}"
    
    def _prepare_job_context(self, query):
        """Prepare relevant job database context based on the query"""
        # Access JOBS_DB from globals (available after module initialization)
        import sys
        jobs_db = sys.modules[__name__].JOBS_DB if 'JOBS_DB' in dir(sys.modules[__name__]) else {}
        
        if not jobs_db:
            return "Job database not yet loaded."
        
        query_lower = query.lower()
        
        # If asking about specific job categories/departments
        if any(keyword in query_lower for keyword in ['engineering', 'engineer', 'software', 'developer']):
            relevant_jobs = {k: v for k, v in jobs_db.items() if 'engineer' in v['title'].lower() or 'developer' in v['title'].lower()}
        elif any(keyword in query_lower for keyword in ['security', 'cyber', 'cryptography']):
            relevant_jobs = {k: v for k, v in jobs_db.items() if 'security' in v['dept'].lower() or 'security' in v['title'].lower()}
        elif any(keyword in query_lower for keyword in ['data', 'analytics', 'scientist']):
            relevant_jobs = {k: v for k, v in jobs_db.items() if 'data' in v['title'].lower() or 'analytics' in v['title'].lower()}
        elif any(keyword in query_lower for keyword in ['operations', 'mission', 'satellite']):
            relevant_jobs = {k: v for k, v in jobs_db.items() if 'operations' in v['dept'].lower() or 'mission' in v['title'].lower()}
        elif any(keyword in query_lower for keyword in ['research', 'scientist', 'physics']):
            relevant_jobs = {k: v for k, v in jobs_db.items() if 'research' in v['dept'].lower() or 'scientist' in v['title'].lower()}
        elif any(keyword in query_lower for keyword in ['remote', 'work from home']):
            relevant_jobs = {k: v for k, v in jobs_db.items() if v['location'] == 'Remote'}
        elif any(keyword in query_lower for keyword in ['abu dhabi', 'uae', 'onsite']):
            relevant_jobs = {k: v for k, v in jobs_db.items() if 'Abu Dhabi' in v['location']}
        else:
            # Return all jobs summary for general queries
            relevant_jobs = jobs_db
        
        # Format job data for AI context (limit to 10 jobs to avoid token overflow)
        job_list = []
        for job_id, job in list(relevant_jobs.items())[:10]:
            job_list.append(
                f"- {job['title']} ({job['dept']}) | {job['location']} | "
                f"Skills: {', '.join(job['reqs'][:3])} | {job['desc']}"
            )
        
        return f"Total positions: {len(jobs_db)}. Relevant jobs:\n" + "\n".join(job_list)

agent = AIAgent()

# =============================================================================
# APP CONFIGURATION
# =============================================================================
app = dash.Dash(
    __name__, 
    external_stylesheets=[dbc.themes.BOOTSTRAP, "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css"],
    suppress_callback_exceptions=True,
    title="Space42 | Orbital Intelligence"
)

# Job Database
JOBS_DB = {
    # Engineering - AI/ML
    "job_01": {
        "title": "Orbital AI Engineer",
        "dept": "Intelligence Systems",
        "location": "Abu Dhabi, UAE",
        "type": "Full-time",
        "reqs": ["Python", "C++", "TensorFlow", "Embedded Systems", "Computer Vision"],
        "desc": "Design and implement next-generation satellite AI systems for autonomous orbital operations.",
        "full_desc": "Join our Intelligence Systems team to architect cutting-edge AI solutions for satellite autonomy. You'll work on real-time computer vision, edge AI deployment, and mission-critical decision systems."
    },
    "job_02": {
        "title": "Machine Learning Research Scientist",
        "dept": "AI Research",
        "location": "Remote",
        "type": "Full-time",
        "reqs": ["Python", "PyTorch", "Research", "Deep Learning", "NLP"],
        "desc": "Conduct advanced ML research for space telemetry analysis and predictive maintenance.",
        "full_desc": "Lead research initiatives in machine learning algorithms for satellite health monitoring, anomaly detection, and predictive analytics. Publish papers and collaborate with academic institutions."
    },
    "job_03": {
        "title": "Computer Vision Engineer",
        "dept": "Imaging Systems",
        "location": "Abu Dhabi, UAE",
        "type": "Full-time",
        "reqs": ["Python", "OpenCV", "CUDA", "Deep Learning", "Real-time Processing"],
        "desc": "Develop real-time image processing systems for Earth observation satellites.",
        "full_desc": "Build high-performance computer vision pipelines for satellite imagery analysis. Work on object detection, semantic segmentation, and real-time video processing for Earth monitoring missions."
    },
    
    # Engineering - Software
    "job_04": {
        "title": "Spacecraft Software Architect",
        "dept": "Flight Software",
        "location": "Abu Dhabi, UAE",
        "type": "Full-time",
        "reqs": ["C++", "RTOS", "Flight Software", "Systems Design", "Safety-Critical"],
        "desc": "Design mission-critical flight software architectures for next-generation spacecraft.",
        "full_desc": "Lead the architecture of flight software systems for satellite constellations. Ensure fault tolerance, real-time performance, and compliance with space standards (ECSS, DO-178C)."
    },
    "job_05": {
        "title": "Embedded Systems Engineer",
        "dept": "Hardware Integration",
        "location": "Abu Dhabi, UAE",
        "type": "Full-time",
        "reqs": ["C", "ARM", "FPGA", "Device Drivers", "Linux Kernel"],
        "desc": "Develop low-level embedded software for satellite payload systems.",
        "full_desc": "Work on embedded Linux systems, device drivers, and FPGA programming for satellite payloads. Optimize for power consumption and radiation tolerance in extreme space environments."
    },
    "job_06": {
        "title": "Full Stack Space Systems Developer",
        "dept": "Ground Systems",
        "location": "Remote",
        "type": "Full-time",
        "reqs": ["React", "Node.js", "Python", "Docker", "Kubernetes"],
        "desc": "Build web applications for satellite command and control systems.",
        "full_desc": "Develop modern ground station software with real-time telemetry visualization, mission planning tools, and automated operations interfaces. Work with microservices and cloud-native technologies."
    },
    
    # Infrastructure & DevOps
    "job_07": {
        "title": "Deep Space Network Architect",
        "dept": "Infrastructure",
        "location": "Remote",
        "type": "Full-time",
        "reqs": ["Networking", "DTN Protocol", "RF Engineering", "Physics", "Python"],
        "desc": "Build the interplanetary internet backbone for deep space communications.",
        "full_desc": "Lead the development of delay-tolerant networking (DTN) protocols for Mars missions and beyond. Design resilient communication architectures that can handle extreme latencies and unreliable links."
    },
    "job_08": {
        "title": "Cloud Infrastructure Engineer",
        "dept": "DevOps",
        "location": "Remote",
        "type": "Full-time",
        "reqs": ["AWS", "Terraform", "Kubernetes", "CI/CD", "Python"],
        "desc": "Build and maintain cloud infrastructure for satellite data processing pipelines.",
        "full_desc": "Design scalable cloud architectures for petabyte-scale satellite data processing. Implement infrastructure-as-code, automated deployments, and monitoring systems for mission-critical services."
    },
    "job_09": {
        "title": "Site Reliability Engineer",
        "dept": "Operations",
        "location": "Abu Dhabi, UAE",
        "type": "Full-time",
        "reqs": ["Linux", "Python", "Monitoring", "Incident Response", "Automation"],
        "desc": "Ensure 99.99% uptime for satellite ground station networks.",
        "full_desc": "Build and maintain highly reliable systems for satellite operations. Implement monitoring, alerting, and automated recovery systems. Participate in on-call rotation for mission-critical infrastructure."
    },
    
    # Security & Cryptography
    "job_10": {
        "title": "Quantum Cryptography Specialist",
        "dept": "Security Operations",
        "location": "Abu Dhabi, UAE",
        "type": "Full-time",
        "reqs": ["Cryptography", "Rust", "Mathematics", "Lattice-based Crypto", "QKD"],
        "desc": "Implement post-quantum cryptography (PQC) for satellite security systems.",
        "full_desc": "Protect our orbital infrastructure with quantum-resistant cryptographic protocols. Research and implement cutting-edge security solutions using lattice-based cryptography and quantum key distribution."
    },
    "job_11": {
        "title": "Cybersecurity Engineer - Space Systems",
        "dept": "Security Operations",
        "location": "Abu Dhabi, UAE",
        "type": "Full-time",
        "reqs": ["Security", "Penetration Testing", "Threat Modeling", "Python", "Network Security"],
        "desc": "Secure satellite systems against cyber threats and adversarial attacks.",
        "full_desc": "Conduct security assessments, penetration testing, and threat modeling for satellite command and control systems. Develop security hardening guidelines and incident response procedures."
    },
    "job_12": {
        "title": "Security Architect",
        "dept": "Security Operations",
        "location": "Remote",
        "type": "Full-time",
        "reqs": ["Architecture", "Zero Trust", "IAM", "Compliance", "Risk Assessment"],
        "desc": "Design zero-trust security architectures for distributed space systems.",
        "full_desc": "Lead security architecture design for satellite constellations and ground infrastructure. Implement zero-trust principles, secure authentication systems, and ensure compliance with aerospace security standards."
    },
    
    # Space Operations
    "job_13": {
        "title": "Mission Control Engineer",
        "dept": "Flight Operations",
        "location": "Abu Dhabi, UAE",
        "type": "Full-time",
        "reqs": ["Orbital Mechanics", "Flight Dynamics", "Python", "Real-time Systems", "MATLAB"],
        "desc": "Operate and monitor satellite constellations from Mission Control Center.",
        "full_desc": "Execute satellite operations including orbit maneuvers, payload commanding, and anomaly resolution. Work in shifts to provide 24/7 coverage for active missions. Analyze telemetry and make real-time decisions."
    },
    "job_14": {
        "title": "Satellite Operations Specialist",
        "dept": "Flight Operations",
        "location": "Abu Dhabi, UAE",
        "type": "Full-time",
        "reqs": ["Spacecraft Systems", "Telemetry Analysis", "Ground Systems", "Communication Protocols"],
        "desc": "Monitor and command satellites during routine and emergency operations.",
        "full_desc": "Perform daily health checks, execute commanding sequences, and troubleshoot spacecraft anomalies. Interface with ground station networks and coordinate with engineering teams for mission success."
    },
    "job_15": {
        "title": "Flight Dynamics Engineer",
        "dept": "Orbital Analysis",
        "location": "Abu Dhabi, UAE",
        "type": "Full-time",
        "reqs": ["Orbital Mechanics", "MATLAB", "STK", "Trajectory Optimization", "Astrodynamics"],
        "desc": "Plan and execute orbital maneuvers for satellite constellation management.",
        "full_desc": "Design orbit maintenance strategies, collision avoidance maneuvers, and rendezvous trajectories. Develop tools for orbit determination and prediction using ground tracking data."
    },
    
    # Research & Development
    "job_16": {
        "title": "Astrophysicist - Mission Planning",
        "dept": "Science Operations",
        "location": "Remote",
        "type": "Full-time",
        "reqs": ["Physics", "Astronomy", "Data Analysis", "Python", "Research"],
        "desc": "Lead scientific mission planning for deep space observation satellites.",
        "full_desc": "Define observation targets, design scientific experiments, and analyze astronomical data from space telescopes. Collaborate with international scientific community and publish research findings."
    },
    "job_17": {
        "title": "Quantum Computing Researcher",
        "dept": "Advanced R&D",
        "location": "Remote",
        "type": "Full-time",
        "reqs": ["Quantum Computing", "Qiskit", "Physics", "Python", "Mathematics"],
        "desc": "Research quantum computing applications for satellite data processing.",
        "full_desc": "Explore quantum algorithms for optimization problems in satellite routing, data compression, and signal processing. Work with quantum hardware partners to develop proof-of-concept implementations."
    },
    "job_18": {
        "title": "Materials Science Engineer",
        "dept": "Spacecraft Engineering",
        "location": "Abu Dhabi, UAE",
        "type": "Full-time",
        "reqs": ["Materials Science", "Thermal Analysis", "CAD", "Testing", "Space Environment"],
        "desc": "Develop radiation-hardened materials for spacecraft construction.",
        "full_desc": "Research and test materials for space applications, focusing on radiation tolerance, thermal stability, and mechanical properties. Design experiments and analyze results for spacecraft component qualification."
    },
    
    # Data Science & Analytics
    "job_19": {
        "title": "Data Engineer - Satellite Analytics",
        "dept": "Data Platform",
        "location": "Remote",
        "type": "Full-time",
        "reqs": ["Python", "Spark", "SQL", "ETL", "Data Pipelines"],
        "desc": "Build scalable data pipelines for processing terabytes of satellite imagery.",
        "full_desc": "Design and implement big data pipelines for satellite telemetry and imagery processing. Work with distributed systems, stream processing, and data lake architectures to enable analytics at scale."
    },
    "job_20": {
        "title": "Geospatial Data Scientist",
        "dept": "Earth Observation",
        "location": "Remote",
        "type": "Full-time",
        "reqs": ["Python", "GIS", "Remote Sensing", "Machine Learning", "Geospatial Analytics"],
        "desc": "Extract insights from satellite imagery for Earth monitoring applications.",
        "full_desc": "Apply machine learning to satellite imagery for environmental monitoring, agriculture, urban planning, and disaster response. Work with multispectral and SAR data to develop analytical products."
    },
    "job_21": {
        "title": "Telemetry Analytics Lead",
        "dept": "Mission Analytics",
        "location": "Abu Dhabi, UAE",
        "type": "Full-time",
        "reqs": ["Python", "Time Series Analysis", "Statistics", "Anomaly Detection", "Visualization"],
        "desc": "Lead analytics initiatives for satellite health monitoring and predictive maintenance.",
        "full_desc": "Develop statistical models and machine learning systems for satellite anomaly detection. Create dashboards and reports for mission teams. Drive data-driven decision making in satellite operations."
    },
    
    # Product & Program Management
    "job_22": {
        "title": "Technical Program Manager - Satellite Constellation",
        "dept": "Program Management",
        "location": "Abu Dhabi, UAE",
        "type": "Full-time",
        "reqs": ["Program Management", "Aerospace", "Agile", "Stakeholder Management", "Technical Leadership"],
        "desc": "Lead technical program management for satellite constellation deployment.",
        "full_desc": "Coordinate cross-functional teams across engineering, operations, and business. Manage timelines, budgets, and stakeholder expectations for satellite development and launch programs."
    },
    "job_23": {
        "title": "Product Manager - Ground Systems",
        "dept": "Product",
        "location": "Remote",
        "type": "Full-time",
        "reqs": ["Product Management", "User Research", "Roadmapping", "Technical Background"],
        "desc": "Define product strategy for next-generation satellite ground control systems.",
        "full_desc": "Work with operators and engineers to design intuitive ground system interfaces. Define product roadmaps, prioritize features, and drive user-centered design for mission-critical software."
    },
    
    # Hardware Engineering
    "job_24": {
        "title": "RF Systems Engineer",
        "dept": "Communications",
        "location": "Abu Dhabi, UAE",
        "type": "Full-time",
        "reqs": ["RF Engineering", "Antenna Design", "Link Budget", "Signal Processing", "MATLAB"],
        "desc": "Design radio frequency systems for satellite communication payloads.",
        "full_desc": "Develop RF subsystems including transmitters, receivers, and antennas for satellite communications. Perform link budget analysis, interference mitigation, and regulatory compliance."
    },
    "job_25": {
        "title": "Power Systems Engineer",
        "dept": "Electrical Engineering",
        "location": "Abu Dhabi, UAE",
        "type": "Full-time",
        "reqs": ["Power Electronics", "Solar Arrays", "Battery Systems", "Electrical Engineering"],
        "desc": "Design electrical power systems for long-duration space missions.",
        "full_desc": "Develop power generation, storage, and distribution systems for satellites. Design solar array architectures, battery management systems, and power conditioning units for harsh space environments."
    },
    "job_26": {
        "title": "Optical Systems Engineer",
        "dept": "Payload Engineering",
        "location": "Abu Dhabi, UAE",
        "type": "Full-time",
        "reqs": ["Optics", "Imaging", "ZEMAX", "Calibration", "Physics"],
        "desc": "Design high-resolution optical payloads for Earth observation satellites.",
        "full_desc": "Develop optical systems for satellite cameras and sensors. Perform optical design, tolerance analysis, and calibration procedures. Work on next-generation hyperspectral imaging systems."
    },
    
    # Business & Strategy
    "job_27": {
        "title": "Business Development Manager - Space Services",
        "dept": "Commercial",
        "location": "Abu Dhabi, UAE",
        "type": "Full-time",
        "reqs": ["Business Development", "Aerospace Industry", "Sales", "Market Analysis"],
        "desc": "Drive commercial partnerships and revenue growth for satellite services.",
        "full_desc": "Identify and pursue new business opportunities in satellite communications, Earth observation, and data services. Build relationships with government and commercial customers across the Middle East."
    },
    "job_28": {
        "title": "Space Policy Analyst",
        "dept": "Strategy & Policy",
        "location": "Remote",
        "type": "Full-time",
        "reqs": ["Policy Analysis", "Space Law", "Regulatory Affairs", "Research", "Writing"],
        "desc": "Analyze space regulations and advise on policy compliance strategies.",
        "full_desc": "Monitor international space policy developments, ensure regulatory compliance, and support strategic planning. Work with government agencies and international bodies on space governance issues."
    },
}

# =============================================================================
# BACKGROUND PIPELINE
# =============================================================================
def run_pipeline_thread(user_id, file_path, job_id):
    if not database: 
        print("[DEBUG] Database not available in pipeline thread")
        return
    try:
        print(f"[*] Pipeline Processing: {file_path} for User: {user_id}")
        # 1. Parse
        print("[DEBUG] Step 1: Calling parser_SIB.parse_resume_to_json...")
        ai_data = parser_SIB.parse_resume_to_json(file_path)
        print(f"[DEBUG] Parser returned data with keys: {list(ai_data.keys())}")
        
        # 2. Security
        print("[DEBUG] Step 2: Running security scan...")
        if airlock.scan_for_injection(str(ai_data)):
            print("[DEBUG] Security threat detected!")
            database.update_ai_results(user_id, 0, "THREAT DETECTED", "THREAT_BLOCKED")
            return

        # 3. Score
        print("[DEBUG] Step 3: Calculating score...")
        job_reqs = JOBS_DB.get(job_id, {}).get("reqs", [])
        score_res = scoring.calculate_orbit_score(ai_data, job_reqs)
        final_score = score_res.get("total_score", 0)
        print(f"[DEBUG] Score calculated: {final_score}")
        
        # 4. Save
        print("[DEBUG] Step 4: Updating database...")
        conn = database.get_db_connection()
        skills = ", ".join(ai_data.get("skills", [])[:15])
        conn.execute('''
            UPDATE candidates SET match_score=?, weakness_focus=?, skills_detected=?, mission_status=? WHERE id=?
        ''', (final_score, ai_data.get("weakness", "General"), skills, "MISSION_READY", user_id))
        conn.commit()
        conn.close()
        print(f"[*] Analysis Complete: {final_score}% - Database updated to MISSION_READY")
    except Exception as e:
        print(f"[!] Pipeline Failed: {e}")
        if database:
            database.update_ai_results(user_id, 0, str(e), "SYSTEM_ERROR")

# =============================================================================
# LAYOUT
# =============================================================================
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    dcc.Store(id='session-store', storage_type='local'),
    dcc.Store(id='chat-history', data=[]),
    
    html.Div(className="space-bg"),
    html.Div(className="space-overlay"),
    
    html.Div(id="page-content"),
    
    # Chat Widget
    html.Button(html.I(className="fas fa-robot"), className="chat-toggle-btn", id="chat-toggle"),
    html.Div(id="chat-window", className="chat-widget closed", children=[
        html.Div(className="chat-header", children=[
            html.Span([html.I(className="fas fa-satellite-dish me-2"), "ORBITAL AGENT"], className="chat-header-title"),
            html.I(className="fas fa-times", id="chat-close", style={"cursor": "pointer", "color": "#94A3B8"})
        ]),
        html.Div(id="chat-messages", className="chat-body", children=[
            html.Div("Greetings, Pilot. I am Orbital. How may I assist you today?", className="chat-msg ai")
        ]),
        html.Div(className="chat-input-area", children=[
            dbc.InputGroup([
                dbc.Input(id="chat-input", placeholder="Ask Orbital...", className="input-glass", style={"border": "none"}),
                dbc.Button(html.I(className="fas fa-paper-plane"), id="chat-send", color="primary", className="btn-neon", style={"borderRadius": "0 10px 10px 0"})
            ], style={"gap": "8px"})
        ])
    ]),
    

])

# =============================================================================
# VIEWS & COMPONENTS
# =============================================================================

def Navbar(active="/", session=None):
    """Navigation bar component"""
    if not session:
        session = {}
    
    # Determine login link text
    if session.get('id'):
        login_text = [html.I(className="fas fa-user-circle"), f" {session.get('email', 'User').split('@')[0]}"]
    else:
        login_text = [html.I(className="fas fa-sign-in-alt"), " Login"]
    
    return html.Div(className="navbar-glass", children=[
        dcc.Link(
            html.Div(className="nav-brand", children=["SPACE42", html.Span("ORBITAL INTELLIGENCE")]),
            href="/",
            style={"textDecoration": "none"}
        ),
        html.Div(className="nav-menu", children=[
            dcc.Link([html.I(className="fas fa-home"), " Home"], href="/", className=f"nav-link {'active' if active=='/' else ''}"),
            dcc.Link([html.I(className="fas fa-briefcase"), " Missions"], href="/jobs", className=f"nav-link {'active' if active=='/jobs' else ''}"),
            dcc.Link(login_text, href="/login", className=f"nav-link {'active' if active=='/login' else ''}"),
        ])
    ])

def satellite_svg():
    """SVG satellite icon"""
    return html.Div(className="satellite", children=[
        html.I(className="fas fa-satellite", style={"fontSize": "40px", "color": "#00E5FF"})
    ])

def landing_page(session=None):
    """Enhanced landing page with satellites and active missions badge"""
    return html.Div(className="fade-in", children=[
        Navbar("/", session),
        
        # Active Missions Badge
        dcc.Link(
            html.Div(className="missions-badge", children=[
                html.Div("ACTIVE MISSIONS", className="missions-badge-title"),
                html.Div(str(len(JOBS_DB)), className="missions-badge-count")
            ]),
            href="/jobs"
        ),
        
        # Hero Section
        html.Div(className="hero-container", children=[
            html.H1("The Sky Is Not The Limit.", className="hero-title"),
            html.P("It Is Just The Lobby.", className="hero-subtitle"),
            dcc.Link(html.Button("ENTER MISSION CONTROL", className="btn-primary"), href="/jobs"),
        ]),
        
        # Animated Satellites at bottom
        html.Div(className="satellites-container", children=[
            satellite_svg(),
            satellite_svg(),
            satellite_svg(),
            satellite_svg(),
            satellite_svg(),
        ])
    ])

def jobs_page(session=None):
    """Jobs listing page with cards"""
    user_apps = []
    if session and session.get('id') and database:
        user_apps = database.get_user_applications(session['id'])
    
    applied_job_ids = [app['job_id'] for app in user_apps]
    
    job_cards = []
    for job_id, job in JOBS_DB.items():
        has_applied = job_id in applied_job_ids
        
        card = html.Div(className="job-card", children=[
            html.Div(className="job-title", children=job["title"]),
            html.Div(className="job-dept", children=job["dept"]),
            html.Div(className="job-desc", children=job["desc"]),
            html.Div(className="job-reqs", children=[
                html.Span(req, className="skill-tag") for req in job["reqs"][:4]
            ]),
            html.Div(style={"marginTop": "20px"}, children=[
                dcc.Link(
                    html.Button(
                        "VIEW DETAILS" if not has_applied else "✓ APPLIED",
                        className="btn-primary" if not has_applied else "btn-secondary",
                        style={"width": "100%", "opacity": "0.6" if has_applied else "1", "pointerEvents": "none" if has_applied else "auto"}
                    ),
                    href=f"/jobs/{job_id}" if not has_applied else "#",
                    style={"textDecoration": "none"}
                )
            ])
        ], id={"type": "job-card-div", "index": job_id})
        
        job_cards.append(card)
    
    return html.Div(className="fade-in", children=[
        Navbar("/jobs", session),
        html.Div(style={"marginTop": "100px", "padding": "0 40px", "maxWidth": "1400px", "margin": "100px auto"}, children=[
            html.H2("Active Missions", style={"marginBottom": "10px", "fontWeight": "700"}),
            html.P(f"{len(JOBS_DB)} positions available", style={"color": "#94A3B8", "marginBottom": "40px"}),
            html.Div(className="jobs-grid", children=job_cards)
        ])
    ])

def dashboard_view(session=None):
    """User dashboard with widgets"""
    if not session or not session.get('id'):
        return login_page(session)
    
    email = session.get("email", "Guest")
    user_id = session.get("id")
    
    # Fetch user data
    status, score, skills, weakness = "AWAITING UPLOAD", 0, [], "None detected"
    applications = []
    recommendations = []
    
    if user_id and database:
        data = database.get_pilot_status(user_id)
        if data:
            status = data.get('mission_status', "AWAITING UPLOAD")
            score = data.get('match_score', 0)
            skills = data.get('skills_detected', "").split(", ") if data.get('skills_detected') else []
            weakness = data.get('weakness_focus', "None detected")
        
        applications = database.get_user_applications(user_id)
        rec_ids = database.get_job_recommendations(user_id)
        recommendations = [{**JOBS_DB[jid], 'id': jid} for jid in rec_ids if jid in JOBS_DB]
    
    status_color = "#FFD600" if status == "ANALYZING" else ("#00FF9D" if status == "MISSION_READY" else ("#FF5252" if "THREAT" in status else "#00E5FF"))
    is_ready = status == "MISSION_READY"
    profile_completion = min(100, 25 + (25 if score > 0 else 0) + (25 if len(skills) > 0 else 0) + (25 if len(applications) > 0 else 0))
    
    return html.Div([
        Navbar("/dashboard", session),
        html.Div(className="fade-in dashboard-container", children=[
            
            # Header
            html.Div(className="dashboard-header", children=[
                html.Div([
                    html.H2(f"Welcome, Pilot {email.split('@')[0]}", style={"fontWeight": "700", "margin": "0"}),
                    html.Div(f"Mission Command Center", style={"color": "#94A3B8", "fontSize": "14px", "marginTop": "5px"})
                ]),
                html.Div(style={"textAlign": "right"}, children=[
                    html.Div("SYSTEM STATUS", style={"fontSize": "10px", "fontWeight": "700", "color": "#666"}),
                    html.Div("● ONLINE", style={"color": "#00FF9D", "fontWeight": "bold"})
                ])
            ]),
            
            # Top Row: Quick Stats
            html.Div(className="widget-grid", style={"marginTop": "30px"}, children=[
                # Match Score
                html.Div(className="widget widget-small", children=[
                    html.Div("MATCH SCORE", className="widget-title"),
                    html.Div(f"{score}%", className="widget-value", style={"color": status_color}),
                    html.Div("Orbital Sync", className="widget-label")
                ]),
                
                # Active Applications
                html.Div(className="widget widget-small", children=[
                    html.Div("APPLICATIONS", className="widget-title"),
                    html.Div(str(len(applications)), className="widget-value"),
                    html.Div("Submitted", className="widget-label")
                ]),
                
                # Profile Completion
                html.Div(className="widget widget-small", children=[
                    html.Div("PROFILE", className="widget-title"),
                    html.Div(f"{profile_completion}%", className="widget-value"),
                    html.Div("Complete", className="widget-label")
                ]),
                
                # Status
                html.Div(className="widget widget-small", children=[
                    html.Div("STATUS", className="widget-title"),
                    html.Div(status.replace("_", " "), style={"fontSize": "16px", "fontWeight": "700", "color": status_color, "marginTop": "10px"}),
                ])
            ]),
            
            # Main Row
            html.Div(className="widget-grid", children=[
                # CV Upload & Analysis
                html.Div(className="widget widget-large", children=[
                    html.H4("Telemetry Analysis", style={"marginBottom": "20px"}),
                    
                    # Timeline
                    html.Div(style={"margin": "20px 0 30px"}, children=[
                        html.Div("1. UPLOAD TELEMETRY", className="timeline-item", style={"color": "white" if status != "AWAITING_UPLOAD" else "#00E5FF"}),
                        html.Div("2. AI ANALYSIS", className="timeline-item", style={"color": "white" if status in ["ANALYZING", "MISSION_READY"] else "#555"}),
                        html.Div("3. FLIGHT READY", className="timeline-item", style={"color": status_color if status == "MISSION_READY" else "#555"}),
                    ]),
                    
                    # Upload zone - always visible
                    html.Div(id="upload-container-dash", children=[
                        dcc.Upload(id='upload-cv', className="upload-zone", multiple=False,
                            children=html.Div([
                                html.I(className="fas fa-file-pdf", style={"fontSize": "40px", "marginBottom": "15px", "color": "#00E5FF"}),
                                html.Div("Drag & Drop PDF Resume", style={"fontSize": "14px", "fontWeight": "600"}),
                                html.Div("or click to browse", style={"fontSize": "12px", "color": "#666", "marginTop": "5px"})
                            ])),
                        html.Div(id="upload-feedback", style={"marginTop": "15px", "textAlign": "center"})
                    ]),
                    
                    # ANALYZING: Show animated progress
                    html.Div(style={"display": "block" if status == "ANALYZING" else "none", "textAlign": "center", "padding": "30px"}, children=[
                        html.Div([
                            html.I(className="fas fa-sync fa-spin", style={"fontSize": "48px", "color": "#FFD600", "marginBottom": "20px"}),
                            html.Div("Analyzing Your Profile", style={"fontSize": "20px", "fontWeight": "700", "marginBottom": "10px"}),
                            html.Div("AI is parsing your resume, calculating orbit score, and identifying skills...", 
                                   style={"color": "#94A3B8", "fontSize": "13px"}),
                        ])
                    ]),
                    
                    # MISSION_READY: Show score and results
                    html.Div(style={"display": "block" if is_ready else "none"}, children=[
                        html.Div([
                            html.I(className="fas fa-check-circle", style={"fontSize": "48px", "color": "#00FF9D", "marginBottom": "15px"}),
                            html.Div("Analysis Complete", style={"fontSize": "18px", "fontWeight": "700"}),
                            html.Div(f"Match Score: {score}%", style={"color": "#00E5FF", "marginTop": "8px", "fontSize": "24px", "fontWeight": "700"})
                        ], style={"textAlign": "center"})
                    ]),
                    
                    # THREAT_BLOCKED or SYSTEM_ERROR: Show error
                    html.Div(style={"display": "block" if status in ["THREAT_BLOCKED", "SYSTEM_ERROR"] else "none", "textAlign": "center", "padding": "30px"}, children=[
                        html.Div([
                            html.I(className="fas fa-exclamation-triangle", style={"fontSize": "48px", "color": "#FF5252", "marginBottom": "15px"}),
                            html.Div("Analysis Error", style={"fontSize": "18px", "fontWeight": "700", "color": "#FF5252"}),
                            html.Div(weakness if status in ["THREAT_BLOCKED", "SYSTEM_ERROR"] else "", 
                                   style={"color": "#94A3B8", "fontSize": "13px", "marginTop": "10px"})
                        ])
                    ]),
                    
                    dcc.Interval(id="dashboard-poller", interval=3000, disabled=False)
                ]),
                
                # Detected Skills
                html.Div(className="widget widget-large", children=[
                    html.Div("DETECTED SKILLS", className="widget-title"),
                    html.Div(
                        [html.Span(s, className="skill-tag") for s in skills[:12]] if skills 
                        else html.Div("No skills detected yet. Upload your CV to begin analysis.", 
                                    style={"color": "#666", "fontSize": "13px", "marginTop": "20px"}),
                        style={"marginTop": "10px"}
                    ),
                    html.Div(style={"marginTop": "20px", "paddingTop": "20px", "borderTop": "1px solid rgba(255,255,255,0.1)"}, children=[
                        html.Div("WEAKNESS ANALYSIS", style={"fontSize": "11px", "color": "#FF5252", "marginBottom": "8px", "textTransform": "uppercase"}),
                        html.Div(weakness, style={"fontSize": "13px", "color": "#FFD600"})
                    ])
                ])
            ]),
            
            # Bottom Row
            html.Div(className="widget-grid", children=[
                # Application Status
                html.Div(className="widget widget-large", children=[
                    html.Div("APPLICATION STATUS", className="widget-title"),
                    html.Div(
                        [
                            html.Div(style={"display": "flex", "justifyContent": "space-between", "alignItems": "center", 
                                          "padding": "12px 0", "borderBottom": "1px solid rgba(255,255,255,0.05)"}, children=[
                                html.Div([
                                    html.Div(app['job_title'], style={"fontSize": "14px", "fontWeight": "600", "marginBottom": "4px"}),
                                    html.Div(app['applied_at'][:10], style={"fontSize": "11px", "color": "#666"})
                                ]),
                                html.Span(app['status'], className=f"status-badge status-{app['status'].lower()}")
                            ]) for app in applications[:5]
                        ] if applications else 
                        html.Div("No applications yet. Browse available missions to get started!", 
                               style={"color": "#666", "fontSize": "13px", "marginTop": "20px"}),
                        style={"marginTop": "15px"}
                    )
                ]),
                
                # Job Recommendations
                html.Div(className="widget widget-large", children=[
                    html.Div("RECOMMENDED MISSIONS", className="widget-title"),
                    html.Div(
                        [
                            html.Div(style={"marginBottom": "16px", "paddingBottom": "16px", 
                                          "borderBottom": "1px solid rgba(255,255,255,0.05)"}, children=[
                                html.Div(job['title'], style={"fontSize": "14px", "fontWeight": "600", "marginBottom": "6px", "color": "#00E5FF"}),
                                html.Div(job['dept'], style={"fontSize": "11px", "color": "#666", "marginBottom": "8px"}),
                                dcc.Link(html.Button("View Details →", className="btn-secondary", style={"fontSize": "11px", "padding": "6px 14px"}), 
                                       href=f"/jobs/{job['id']}")
                            ]) for job in recommendations[:3]
                        ] if recommendations else
                        html.Div("Complete your profile to get personalized recommendations.", 
                               style={"color": "#666", "fontSize": "13px", "marginTop": "20px"}),
                        style={"marginTop": "15px"}
                    )
                ])
            ])
        ])
    ])

def job_detail_page(job_id, session=None):
    """Job detail page (replaces modal approach)"""
    if job_id not in JOBS_DB:
        return html.Div([
            Navbar("/jobs", session),
            html.Div(style={"textAlign": "center", "marginTop": "150px"}, children=[
                html.H2("Mission Not Found", style={"color": "#FF5252"}),
                dcc.Link(html.Button("← Back to Missions", className="btn-secondary"), href="/jobs")
            ])
        ])
    
    job = JOBS_DB[job_id]
    is_logged_in = session and session.get('id')
    
    # Check if user already applied
    has_applied = False
    if is_logged_in and database:
        user_apps = database.get_user_applications(session['id'])
        has_applied = job_id in [app['job_id'] for app in user_apps]
    
    return html.Div(className="fade-in", children=[
        Navbar("/jobs", session),
        
        # Back button
        html.Div(style={"position": "fixed", "top": "90px", "left": "40px", "zIndex": "100"}, children=[
            dcc.Link(html.Button("← All Missions", className="btn-secondary", style={"fontSize": "12px"}), href="/jobs")
        ]),
        
        # Main content - centered card
        html.Div(style={"display": "flex", "justifyContent": "center", "alignItems": "center", "minHeight": "100vh", "padding": "120px 40px 40px"}, children=[
            html.Div(className="glass-card", style={"maxWidth": "700px", "width": "100%"}, children=[
                html.H2(job["title"], style={"marginBottom": "8px", "color": "#00E5FF", "fontSize": "28px"}),
                html.Div(job["dept"], style={"color": "#94A3B8", "fontSize": "14px", "marginBottom": "8px", "textTransform": "uppercase", "letterSpacing": "1px"}),
                html.Div([
                    html.I(className="fas fa-map-marker-alt", style={"marginRight": "8px", "color": "#00E5FF"}),
                    job["location"],
                    html.Span(" • ", style={"margin": "0 12px", "color": "#555"}),
                    html.I(className="fas fa-clock", style={"marginRight": "8px", "color": "#00E5FF"}),
                    job["type"]
                ], style={"fontSize": "13px", "color": "#888", "marginBottom": "30px"}),
                
                html.Hr(style={"border": "none", "borderTop": "1px solid rgba(255,255,255,0.1)", "margin": "24px 0"}),
                
                html.H4("Mission Overview", style={"fontSize": "14px", "marginBottom": "16px", "color": "#00E5FF", "textTransform": "uppercase", "letterSpacing": "1px"}),
                html.P(job["full_desc"], style={"color": "#CCC", "lineHeight": "1.8", "marginBottom": "30px", "fontSize": "15px"}),
                
                html.H4("Required Skills", style={"fontSize": "14px", "marginBottom": "16px", "color": "#00E5FF", "textTransform": "uppercase", "letterSpacing": "1px"}),
                html.Div([html.Span(req, className="skill-tag") for req in job["reqs"]], style={"marginBottom": "30px"}),
                
                html.Hr(style={"border": "none", "borderTop": "1px solid rgba(255,255,255,0.1)", "margin": "24px 0"}),
                
                # Apply section
                html.Div(children=[
                    html.Button(
                        "✓ APPLICATION SUBMITTED" if has_applied else ("APPLY NOW" if is_logged_in else "LOGIN TO APPLY"),
                        id="apply-job-btn",
                        className="btn-primary" if not has_applied else "btn-secondary",
                        style={"width": "100%", "padding": "18px", "fontSize": "14px", "opacity": "0.6" if has_applied else "1"},
                        disabled=has_applied
                    ),
                    # Store job_id for the callback
                    dcc.Store(id="current-job-id", data=job_id),
                    html.Div(id="job-apply-feedback", style={"marginTop": "15px", "textAlign": "center"})
                ])
            ])
        ])
    ])

def login_page(session=None):
    """Login/Signup page"""
    return html.Div(style={"height": "100vh", "display": "flex", "justifyContent": "center", "alignItems": "center"}, children=[
        Navbar("/login", session),
        html.Div(className="glass-card fade-in", style={"width": "420px", "textAlign": "center", "marginTop": "70px"}, children=[
            html.H2("Pilot Access", style={"marginBottom": "10px", "fontWeight": "700"}),
            html.P("Enter your credentials to access Mission Control", style={"color": "#94A3B8", "fontSize": "13px", "marginBottom": "30px"}),
            
            dcc.Input(id="login-email", className="input-glass", placeholder="Email Address", style={"marginBottom": "15px"}),
            dcc.Input(id="login-pwd", type="password", className="input-glass", placeholder="Password", style={"marginBottom": "25px"}),
            
            html.Button("LOGIN", id="login-btn", className="btn-primary", style={"width": "100%", "marginBottom": "12px"}),
            html.Button("SIGN UP", id="signup-btn", className="btn-secondary", style={"width": "100%", "marginBottom": "12px"}),
            
            html.Div(id="auth-message", style={"marginTop": "20px", "fontSize": "13px", "minHeight": "20px"})
        ])
    ])

# =============================================================================
# CALLBACKS
# =============================================================================

# Routing
@app.callback(
    Output("page-content", "children"),
    [Input("url", "pathname")],
    [State("session-store", "data")]
)
def router(path, session):
    if not session:
        session = {}
    
    path = path or "/"
    
    if path == "/":
        return landing_page(session)
    elif path == "/jobs":
        return jobs_page(session)
    elif path.startswith("/jobs/"):
        # Job Detail Modal View
        job_id = path.replace("/jobs/", "")
        return job_detail_page(job_id, session)
    elif path == "/dashboard":
        if session.get('role') == 'ADMIN':
            return admin_dashboard_view(session)
        return dashboard_view(session)
    elif path == "/login":
        return login_page(session)
    else:
        return landing_page(session)

# =============================================================================
# ADMIN DASHBOARD
# =============================================================================
def admin_dashboard_view(session):
    if not session or session.get('role') != 'ADMIN' or session.get('email') != 'test@space42.com':
        return html.Div("Unauthorized Access - Security Clearance Level 5 Required", style={"color": "red", "textAlign": "center", "marginTop": "50px"})
    
    email = session.get("email", "Admin")
    
    # Statistics
    stats = {"total": 0, "pending": 0, "approved": 0}
    if database:
        apps = database.get_all_applications()
        stats["total"] = len(apps)
        stats["pending"] = len([a for a in apps if a['status'] == 'PENDING'])
        stats["approved"] = len([a for a in apps if a['status'] == 'APPROVED'])

    return html.Div([
        Navbar("/dashboard", session),
        html.Div(className="fade-in dashboard-container", children=[
            # Header
            html.Div(className="dashboard-header", children=[
                html.Div([
                    html.H2(f"Command Deck", style={"fontWeight": "700", "margin": "0"}),
                    html.Div(f"Officer: {email}", style={"color": "#94A3B8", "fontSize": "14px", "marginTop": "5px"})
                ]),
                html.Div(style={"textAlign": "right"}, children=[
                    html.Div("SECURITY CLEARANCE", style={"fontSize": "10px", "fontWeight": "700", "color": "#666"}),
                    html.Div("● LEVEL 5 (ADMIN)", style={"color": "#FFD600", "fontWeight": "bold"})
                ])
            ]),
            
            # Stats Cards
            html.Div(className="widget-grid", style={"marginTop": "30px"}, children=[
                html.Div(className="widget widget-small", children=[
                    html.Div("TOTAL APPLICANTS", className="widget-title"),
                    html.Div(str(stats["total"]), className="widget-value"),
                ]),
                html.Div(className="widget widget-small", children=[
                    html.Div("PENDING REVIEW", className="widget-title"),
                    html.Div(str(stats["pending"]), className="widget-value", style={"color": "#FFD600"}),
                ]),
                html.Div(className="widget widget-small", children=[
                    html.Div("MISSION READY", className="widget-title"),
                    html.Div(str(stats["approved"]), className="widget-value", style={"color": "#00FF9D"}),
                ])
            ]),
            
            # Main Content: Applications Table
            html.Div(className="widget-grid", children=[
                html.Div(className="widget widget-full", style={"gridColumn": "span 12"}, children=[
                    html.Div(style={"display": "flex", "justifyContent": "space-between", "alignItems": "center", "marginBottom": "20px"}, children=[
                        html.H4("Recruitment Manifest", style={"margin": "0"}),
                        html.Div(style={"display": "flex", "gap": "10px", "alignItems": "center"}, children=[
                            html.Span("Filter by Score:", style={"fontSize": "12px", "color": "#94A3B8"}),
                            dcc.Dropdown(
                                id="score-filter",
                                options=[
                                    {"label": "All Candidates", "value": "all"},
                                    {"label": "🟢 Elite (80%+)", "value": "high"},
                                    {"label": "🔵 Qualified (50-79%)", "value": "medium"},
                                    {"label": "⚪ Developing (<50%)", "value": "low"},
                                ],
                                value="all",
                                clearable=False,
                                style={"width": "180px", "fontSize": "12px"},
                                className="filter-dropdown"
                            )
                        ])
                    ]),
                    html.Div(id="admin-table-container"),
                    dcc.Interval(id="admin-poller", interval=5000)
                ])
            ])
        ])
    ])

# Serve CV File
@app.server.route('/view_cv/<app_id>')
def view_cv(app_id):
    # Retrieve secure path from DB
    if not database: return "Database Error", 500
    conn = database.get_db_connection()
    row = conn.execute("SELECT c.secure_path, c.filename, c.mission_status FROM job_applications ja JOIN candidates c ON ja.candidate_id = c.id WHERE ja.id = ?", (app_id,)).fetchone()
    conn.close()
    
    if not row:
        return "Application not found", 404
        
    secure_path = row['secure_path']
    mission_status = row.get('mission_status', 'UNKNOWN')
    
    # Handle pending/unuploaded CVs
    if not secure_path or secure_path == 'pending' or secure_path == 'admin_init':
        return f"""<!DOCTYPE html>
        <html><head><title>CV Not Available</title>
        <style>body{{font-family:Arial;text-align:center;padding:50px;background:#0a0f1e;color:#94A3B8;}}
        h2{{color:#FFD600;}}</style></head>
        <body><h2>CV Not Available</h2>
        <p>This candidate has not uploaded a CV yet (Status: {mission_status}).</p>
        <p>Please ask them to upload their CV from the Dashboard.</p></body></html>""", 200
    
    try:
        # Construct absolute path
        import os
        base_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(base_dir, secure_path)
        
        if os.path.exists(file_path):
            return send_file(file_path, as_attachment=False, mimetype='application/pdf')
        else:
            return f"""<!DOCTYPE html>
            <html><head><title>File Not Found</title>
            <style>body{{font-family:Arial;text-align:center;padding:50px;background:#0a0f1e;color:#94A3B8;}}
            h2{{color:#FF5252;}}</style></head>
            <body><h2>File Not Found</h2>
            <p>CV file not found at: {secure_path}</p>
            <p>The file may have been moved or deleted.</p></body></html>""", 404
    except Exception as e:
        return f"File Error: {e}", 500


# Authentication
@app.callback(
    [Output("session-store", "data", allow_duplicate=True), 
     Output("url", "pathname", allow_duplicate=True), 
     Output("auth-message", "children")],
    [Input("login-btn", "n_clicks"), 
     Input("signup-btn", "n_clicks")],
    [State("login-email", "value"), 
     State("login-pwd", "value"), 
     State("session-store", "data")],
    prevent_initial_call=True
)
def authenticate(login_clicks, signup_clicks, email, pwd, session):
    if not callback_context.triggered:
        return no_update
    
    ctx = callback_context.triggered[0]['prop_id']
    print(f"[DEBUG] Auth Triggered by: {ctx}")
    
    # Remove Test Mode handling
    
    if not email or not pwd:
        return no_update, no_update, html.Div("Please enter email and password", style={"color": "#FF5252"})
    
    if not database:
        return no_update, no_update, html.Div("Database offline", style={"color": "#FF5252"})
    
    # Login
    if "login-btn" in ctx:
        user = database.login_user(email, pwd)
        if user:
            # STRICT ADMIN CHECK: Only test@space42.com is admin
            role = 'ADMIN' if user['email'] == 'test@space42.com' else 'PILOT'
            return {
                "email": user['email'], 
                "id": user['id'], 
                "role": role
            }, "/dashboard", ""
        else:
            return no_update, no_update, html.Div("Invalid credentials", style={"color": "#FF5252"})
    
    # Signup
    if "signup-btn" in ctx:
        # Restriction: Block @space42.com emails for signup
        if email.endswith('@space42.com'):
             return no_update, no_update, html.Div("Restricted Domain. Staff accounts must be provisioned internally.", style={"color": "#FF5252"})

        # Check if user exists
        existing = database.login_user(email, "dummy_check")
        if existing:
            return no_update, no_update, html.Div("Email already registered. Please login.", style={"color": "#FFD600"})
        
        # Create new user - Default to PILOT
        role = 'PILOT' 
        user_id = database.add_candidate(email, pwd, "pending.pdf", "pending", role)
        return {
            "email": email,
            "id": user_id,
            "role": role
        }, "/dashboard", ""
    
    return no_update, no_update, ""

# CV Upload
@app.callback(
    Output("upload-feedback", "children"),
    [Input("upload-cv", "contents")],
    [State("upload-cv", "filename"), State("session-store", "data")],
    prevent_initial_call=True
)
def handle_upload(contents, filename, session):
    print(f"[DEBUG] handle_upload ENTERED. Filename: {filename}")
    print(f"[DEBUG] Session keys: {list(session.keys()) if session else 'None'}")
    
    if not contents or not session or not session.get('id'):
        print("[DEBUG] Early exit: Missing contents or session ID")
        return no_update
    
    try:
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        print(f"[DEBUG] File decoded successfully. Size: {len(decoded)} bytes")
        
        path = filename
        if airlock:
            res = airlock.secure_upload(decoded, filename)
            if res["status"] != "CLEARED":
                error_msg = html.Div(f"⛔ {res['reason']}", style={"color": "#FF5252"})
                return error_msg
            path = res["secure_path"]
        
        # Immediately update database status to ANALYZING
        if database:
            database.update_ai_results(session.get("id"), 0, "Processing", "ANALYZING")
        
        # Start background processing
        threading.Thread(
            target=run_pipeline_thread, 
            args=(session.get("id"), path, "job_01")
        ).start()
        
        success_msg = html.Div([
            html.I(className="fas fa-check-circle", style={"marginRight": "8px"}),
            "Upload successful! Analyzing..."
        ], style={"color": "#00FF9D"})
        
        return success_msg
        
    except Exception as e:
        error_msg = html.Div(f"Error: {str(e)}", style={"color": "#FF5252"})
# Dashboard Polling (refresh data)
@app.callback(
    Output("page-content", "children", allow_duplicate=True),
    [Input("dashboard-poller", "n_intervals")],
    [State("session-store", "data"), State("url", "pathname")],
    prevent_initial_call=True
)
def poll_dashboard(n, session, path):
    if path == "/dashboard" and session and session.get('id'):
        return dashboard_view(session)
    return no_update



# Apply to Job from Job Detail Page
@app.callback(
    [Output("job-apply-feedback", "children"), 
     Output("url", "pathname", allow_duplicate=True)],
    [Input("apply-job-btn", "n_clicks")],
    [State("current-job-id", "data"), State("session-store", "data")],
    prevent_initial_call=True
)
def apply_to_job_detail(n_clicks, job_id, session):
    if not n_clicks:
        return no_update, no_update
    
    # Not logged in -> redirect to login
    if not session or not session.get('id'):
        return no_update, "/login"
    
    if not database:
        return html.Div("Database offline", style={"color": "#FF5252"}), no_update
    
    # Check if CV uploaded
    user_data = database.get_pilot_status(session['id'])
    if not user_data or user_data.get('mission_status') != 'MISSION_READY':
        return html.Div("Please upload your CV on the Dashboard first.", style={"color": "#FFD600"}), "/dashboard"
    
    # Apply
    job = JOBS_DB.get(job_id)
    if job:
        result = database.apply_to_job(session['id'], job_id, job['title'])
        if result['success']:
            return html.Div([
                html.I(className="fas fa-check-circle", style={"marginRight": "8px"}),
                "Application submitted successfully! Redirecting..."
            ], style={"color": "#00FF9D"}), "/dashboard"
        else:
            return html.Div(result['message'], style={"color": "#FFD600"}), no_update
    
    return no_update, no_update

# Chat Widget
@app.callback(
    [Output("chat-window", "className"), 
     Output("chat-messages", "children"), 
     Output("chat-input", "value")],
    [Input("chat-toggle", "n_clicks"), 
     Input("chat-close", "n_clicks"), 
     Input("chat-send", "n_clicks"),
     Input("chat-input", "n_submit")],
    [State("chat-window", "className"), 
     State("chat-input", "value"), 
     State("chat-messages", "children"), 
     State("session-store", "data")],
    prevent_initial_call=True
)
def chat_control(toggle_clicks, close_clicks, send_clicks, submit, current_class, msg_text, current_msgs, session):
    ctx = callback_context.triggered[0]['prop_id']
    
    # Toggle open/close
    if "chat-toggle" in ctx:
        new_class = "chat-widget" if "closed" in current_class else "chat-widget closed"
        return new_class, no_update, no_update
    
    if "chat-close" in ctx:
        return "chat-widget closed", no_update, no_update
    
    # Send message
    if ("chat-send" in ctx or "chat-input" in ctx) and msg_text and msg_text.strip():
        # Add user message
        user_msg = html.Div(msg_text, className="chat-msg user")
        current_msgs.append(user_msg)
        
        # Add typing indicator
        typing = html.Div(className="chat-typing", children=[
            html.Div(className="typing-dots", children=[
                html.Span(),
                html.Span(),
                html.Span()
            ])
        ])
        current_msgs.append(typing)
        
        # Generate AI response
        context = ""
        if session and session.get('id') and database:
            user_data = database.get_pilot_status(session['id'])
            if user_data:
                context = f"User Status: {user_data['mission_status']}, Score: {user_data['match_score']}%, Skills: {user_data.get('skills_detected', 'None')}"
        
        response = agent.ask(msg_text, context)
        
        # Remove typing indicator and add AI response
        current_msgs.pop()
        ai_msg = html.Div(response, className="chat-msg ai")
        current_msgs.append(ai_msg)
        
        return no_update, current_msgs, ""
    
    return no_update, no_update, no_update

# Admin: Update Table & Handle Actions
@app.callback(
    Output("admin-table-container", "children"),
    [Input("admin-poller", "n_intervals"), 
     Input({"type": "admin-action", "index": ALL, "action": ALL}, "n_clicks"),
     Input("score-filter", "value")],
    prevent_initial_call=False
)
def update_admin_table(n, action_clicks, score_filter):
    # Handle Actions
    ctx = callback_context.triggered[0] if callback_context.triggered else None
    if ctx and "admin-action" in ctx['prop_id']:
        try:
            prop = json.loads(ctx['prop_id'].replace('.n_clicks', ''))
            app_id = prop['index']
            action = prop['action']
            
            if action == 'approve':
                database.update_application_status(app_id, "APPROVED")
            elif action == 'reject':
                database.update_application_status(app_id, "REJECTED")
            elif action == 'waitlist':
                database.update_application_status(app_id, "WAITLISTED")
        except Exception as e:
            print(f"Admin Action Error: {e}")

    # Fetch Data
    if not database: return html.Div("DB Offline")
    apps = database.get_all_applications()
    
    if not apps:
        return html.Div("No active applications.", style={"color": "#666", "textAlign": "center", "marginTop": "20px"})
    
    # Apply score filter
    if score_filter and score_filter != "all":
        if score_filter == "high":
            apps = [a for a in apps if a.get('match_score', 0) >= 80]
        elif score_filter == "medium":
            apps = [a for a in apps if 50 <= a.get('match_score', 0) < 80]
        elif score_filter == "low":
            apps = [a for a in apps if a.get('match_score', 0) < 50]
    
    # Classification function
    def classify_candidate(score):
        if score >= 80:
            return ("ELITE", "#00FF9D")
        elif score >= 60:
            return ("QUALIFIED", "#00E5FF")
        elif score >= 40:
            return ("DEVELOPING", "#FFD600")
        else:
            return ("ENTRY", "#94A3B8")
    
    # Render Table
    rows = []
    for app in apps:
        status_color = "#FFD600"
        if app['status'] == 'APPROVED': status_color = "#00FF9D"
        elif app['status'] == 'REJECTED': status_color = "#FF5252"
        elif app['status'] == 'WAITLISTED': status_color = "#FFD600"
        else: status_color = "#00E5FF" # Pending
        
        score = app.get('match_score', 0)
        classification, class_color = classify_candidate(score)
        
        row = html.Tr([
            html.Td(app['job_title'], style={"color": "#00E5FF", "padding": "12px 8px", "maxWidth": "150px", "whiteSpace": "nowrap", "overflow": "hidden", "textOverflow": "ellipsis"}),
            html.Td(app.get('email', 'Unknown'), style={"padding": "12px 8px", "fontSize": "12px"}),
            html.Td(f"{score}%", style={"padding": "12px 8px", "color": "#00E5FF", "fontWeight": "bold", "textAlign": "center"}),
            html.Td(html.Span(classification, style={"color": class_color, "fontWeight": "600", "fontSize": "10px", "padding": "4px 8px", "background": f"rgba({int(class_color[1:3], 16)}, {int(class_color[3:5], 16)}, {int(class_color[5:7], 16)}, 0.15)", "borderRadius": "4px"}), style={"padding": "12px 8px", "textAlign": "center"}),
            html.Td(html.Span(app['status'], style={"color": status_color, "fontWeight": "bold", "fontSize": "11px"}), style={"padding": "12px 8px", "textAlign": "center"}),
            html.Td([
                html.A(
                    html.Button("CV", className="btn-secondary", style={"padding": "4px 10px", "fontSize": "10px", "marginRight": "6px"}),
                    href=f"/view_cv/{app['id']}",
                    target="_blank"
                ) if app.get('secure_path') and app.get('secure_path') != 'pending' else html.Span("—", style={"color": "#555"}),
                
                html.Button("✓", id={"type": "admin-action", "index": app['id'], "action": "approve"}, 
                           style={"color": "#00FF9D", "marginRight": "4px", "background": "none", "border": "none", "cursor": "pointer", "fontSize": "16px"}),
                html.Button("✗", id={"type": "admin-action", "index": app['id'], "action": "reject"}, 
                           style={"color": "#FF5252", "marginRight": "4px", "background": "none", "border": "none", "cursor": "pointer", "fontSize": "16px"}),
                html.Button("◷", id={"type": "admin-action", "index": app['id'], "action": "waitlist"}, 
                           style={"color": "#FFD600", "background": "none", "border": "none", "cursor": "pointer", "fontSize": "16px"}),
            ], style={"padding": "12px 8px", "whiteSpace": "nowrap"})
        ], style={"borderBottom": "1px solid rgba(255,255,255,0.05)"})
        rows.append(row)
        
    table = html.Table([
        html.Thead(html.Tr([
            html.Th("MISSION", style={"textAlign": "left", "padding": "12px 8px", "color": "#666", "fontSize": "10px", "width": "150px"}), 
            html.Th("PILOT", style={"textAlign": "left", "padding": "12px 8px", "color": "#666", "fontSize": "10px"}), 
            html.Th("SCORE", style={"textAlign": "center", "padding": "12px 8px", "color": "#666", "fontSize": "10px", "width": "70px"}), 
            html.Th("CLASS", style={"textAlign": "center", "padding": "12px 8px", "color": "#666", "fontSize": "10px", "width": "90px"}), 
            html.Th("STATUS", style={"textAlign": "center", "padding": "12px 8px", "color": "#666", "fontSize": "10px", "width": "90px"}), 
            html.Th("ACTIONS", style={"textAlign": "left", "padding": "12px 8px", "color": "#666", "fontSize": "10px", "width": "140px"})
        ], style={"borderBottom": "1px solid rgba(255,255,255,0.1)"})),
        html.Tbody(rows)
    ], style={"width": "100%", "borderCollapse": "collapse", "marginTop": "10px", "tableLayout": "fixed"})
    
    return table

# =============================================================================
# RUN
# =============================================================================
if __name__ == "__main__":
    app.run(debug=True, port=8050, host='127.0.0.1')