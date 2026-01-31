import sqlite3
import datetime
# Import your new vault
try:
    from vault import encrypt_email, decrypt_email, hash_password, verify_password
except ImportError:
    from vault import encrypt_email, decrypt_email, hash_password, verify_password

DB_NAME = "orbit.db"

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row 
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    # Note: 'email' now stores the Long AES String
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS candidates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL, 
            password_hash TEXT NOT NULL,
            filename TEXT,
            secure_path TEXT,
            role TEXT DEFAULT 'PILOT',
            match_score INTEGER DEFAULT 0,
            skills_detected TEXT,
            weakness_focus TEXT,
            mission_status TEXT DEFAULT 'ANALYZING',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

# ==========================================
#  USER REGISTRATION
# ==========================================
def add_candidate(email, password, filename, secure_path, role='PILOT'):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 🔒 ENCRYPT SENSITIVE DATA
    safe_email = encrypt_email(email)       # AES-256
    safe_pass = hash_password(password)     # SHA-256 Hash
    
    cursor.execute('''
        INSERT INTO candidates (email, password_hash, filename, secure_path, role, mission_status)
        VALUES (?, ?, ?, ?, ?, 'ANALYZING')
    ''', (safe_email, safe_pass, filename, secure_path, role))
    
    new_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return new_id

# ==========================================
#  USER LOGIN (The Loop Check)
# ==========================================
def login_user(input_email, input_password):
    """
    Since AES is randomized, we must decrypt DB emails to find a match.
    """
    conn = get_db_connection()
    rows = conn.execute('SELECT * FROM candidates').fetchall()
    conn.close()
    
    found_user = None
    
    # Loop through all users to find the email
    for row in rows:
        try:
            # 🔓 DECRYPT EMAIL TO CHECK
            db_email = decrypt_email(row['email'])
            
            if db_email == input_email:
                # Email matches! Now verify password
                if verify_password(row['password_hash'], input_password):
                    found_user = dict(row)
                    found_user['email'] = db_email # Return readable email
                    break
        except:
            continue
            
    return found_user

# ==========================================
#  FETCHING DATA
# ==========================================
def get_pilot_status(candidate_id):
    conn = get_db_connection()
    row = conn.execute('SELECT * FROM candidates WHERE id = ?', (candidate_id,)).fetchone()
    conn.close()
    
    if row:
        data = dict(row)
        # 🔓 DECRYPT BEFORE SHOWING TO UI
        data['email'] = decrypt_email(data['email'])
        return data
    return None

def fetch_all_pilots():
    conn = get_db_connection()
    rows = conn.execute("SELECT * FROM candidates WHERE role = 'PILOT'").fetchall()
    conn.close()
    
    results = []
    for row in rows:
        data = dict(row)
        data['email'] = decrypt_email(data['email']) # Decrypt for HR View
        results.append(data)
    return results

# Helper for AI updates
def update_ai_results(candidate_id, score, weakness, status):
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