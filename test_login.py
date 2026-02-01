import database
import vault

# Test login with a known user
print("Testing login functionality...")

# Try to login with test@space42.com
print("\n1. Testing test@space42.com login:")
result = database.login_user("test@space42.com", "12345")
if result:
    print(f"   ✓ SUCCESS: {result['email']}")
else:
    print("   ✗ FAILED")

# Check if there are any other users
print("\n2. Checking all candidates:")
conn = database.get_db_connection()
rows = conn.execute('SELECT id, email, password_hash FROM candidates').fetchall()
conn.close()

for row in rows:
    try:
        decrypted_email = vault.decrypt_email(row['email'])
        print(f"   ID {row['id']}: {decrypted_email}")
    except:
        print(f"   ID {row['id']}: [DECRYPT ERROR]")

# Try creating and logging in as a new user
print("\n3. Creating new test user:")
test_email = "testuser@example.com"
test_pass = "password123"

try:
    user_id = database.add_candidate(test_email, test_pass, "pending.pdf", "pending", "PILOT")
    print(f"   ✓ User created with ID: {user_id}")
    
    # Try to login immediately
    print("\n4. Testing login with new user:")
    result = database.login_user(test_email, test_pass)
    if result:
        print(f"   ✓ SUCCESS: Can login as {result['email']}")
    else:
        print("   ✗ FAILED: Cannot login with correct password")
        
except Exception as e:
    print(f"   ✗ Error: {e}")
