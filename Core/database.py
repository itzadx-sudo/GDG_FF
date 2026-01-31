import sqlite3
import datetime

DB_NAME = "orbit.db"

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row 
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Stores both HR admins and Candidates
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS candidates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL,
            filename TEXT,
            secure_path TEXT,
            
            -- AI DATA
            match_score INTEGER DEFAULT 0,
            skills_detected TEXT,
            weakness_focus TEXT, 
            
            -- STATUS & ROLE
            role TEXT DEFAULT 'PILOT',       -- 'PILOT' (User) or 'COMMANDER' (HR)
            mission_status TEXT DEFAULT 'ANALYZING', 
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

#String formatting for the frontend to use
def row_to_dict(row):
    return dict(row) if row else None

# ==========================================
#  USER FUNCTIONS (The Candidate Experience)
# ==========================================

def add_candidate(email, filename, secure_path, role='PILOT'):
    """
    Registers a new user (or HR admin) into the system.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO candidates (email, filename, secure_path, role, mission_status)
        VALUES (?, ?, ?, ?, 'ANALYZING')
    ''', (email, filename, secure_path, role))
    
    new_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return new_id

def get_pilot_status(candidate_id):
    """
    USER VIEW: Fetch only MY specific data.
    """
    conn = get_db_connection()
    row = conn.execute('SELECT * FROM candidates WHERE id = ?', (candidate_id,)).fetchone()
    conn.close()
    return row_to_dict(row)

# ==========================================
#  HR FUNCTIONS (The Commander Dashboard)
# ==========================================

def fetch_all_pilots():
    """
    HR VIEW: Fetch ALL candidates who are Pilots.
    Used to populate the HR table/list.
    """
    conn = get_db_connection()
    # Get everyone who is NOT a commander (HR shouldn't interview other HR)
    rows = conn.execute("SELECT * FROM candidates WHERE role = 'PILOT' ORDER BY match_score DESC").fetchall()
    conn.close()
    return [row_to_dict(row) for row in rows]

def update_ai_results(candidate_id, score, weakness, status):
    """
    Called by AI (Brain) to update the score.
    """
    conn = get_db_connection()
    conn.execute('''
        UPDATE candidates 
        SET match_score = ?, weakness_focus = ?, mission_status = ?
        WHERE id = ?
    ''', (score, weakness, status, candidate_id))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()