
import sqlite3
import os
import sys

# Add project root to path
sys.path.append(os.path.abspath("/Users/adityajain/Documents/GDG/Project/GDG_FF"))

try:
    import database
    from vault import encrypt_email, hash_password, decrypt_email
except ImportError as e:
    print(f"Import Error: {e}")
    sys.exit(1)

database.init_db()

target_email = "test@space42.com"
raw_password = "12345"

print(f"[*] Setting password for {target_email}...")

conn = database.get_db_connection()
cursor = conn.cursor()

# Find existing user (need to decrypt to match, or just encrypt target and search)
# vault.encrypt_email is deterministic for this app? Let's assume yes or search all.
# Looking at login_user in database.py, it fetches all and decrypts. That's inefficient but accurate for this app's design.

cursor.execute("SELECT id, email FROM candidates")
rows = cursor.fetchall()
found_id = None

for row in rows:
    try:
        if decrypt_email(row['email']) == target_email:
            found_id = row['id']
            break
    except:
        continue

new_hash = hash_password(raw_password)
encrypted_email = encrypt_email(target_email)

if found_id:
    # Update
    print(f"[*] User found (ID: {found_id}). Updating password...")
    cursor.execute("UPDATE candidates SET password_hash = ?, role = 'ADMIN' WHERE id = ?", (new_hash, found_id))
else:
    # Insert
    print("[*] User not found. Creating new admin user...")
    # add_candidate(email, password, filename, secure_path, role='PILOT')
    # Use database.py function to handle encryption/hashing if we use it, but we can do direct insert to force ID/Role
    # Actually, database.add_candidate handles encryption. Let's use it or verify it.
    
    # Direct insert to be sure about fields
    cursor.execute('''
        INSERT INTO candidates (email, password_hash, filename, secure_path, role, mission_status)
        VALUES (?, ?, ?, ?, ?, 'MISSION_READY')
    ''', (encrypted_email, new_hash, "admin_init.pdf", "admin_init", "ADMIN"))

conn.commit()
conn.close()

print("[*] Password set successfully.")
print(f"[*] Credentials -> Email: {target_email} | Password: {raw_password}")
