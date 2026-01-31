import os
import hashlib
import base64
from cryptography.fernet import Fernet

# ==========================================
# 1. KEY MANAGEMENT (AES-256)
# ==========================================
KEY_FILE = "orbit.key"

def load_key():
    """
    Loads the AES Master Key. 
    If it doesn't exist, it creates one.
    """
    if not os.path.exists(KEY_FILE):
        # Generate a new 32-byte key (AES-256 compliant)
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as kf:
            kf.write(key)
    return open(KEY_FILE, "rb").read()

# Initialize the Cipher Suite (The Encryption Engine)
# We load this once so we don't read the file 100 times
cipher = Fernet(load_key())

# ==========================================
# 2. EMAIL ENCRYPTION (AES-256)
# ==========================================
def encrypt_email(plain_email: str) -> str:
    """
    Encrypts the email using AES.
    Note: This produces DIFFERENT output every time for the same email.
    """
    if not plain_email: return ""
    # Fernet requires bytes, so encode -> encrypt -> decode to string
    encrypted_bytes = cipher.encrypt(plain_email.encode('utf-8'))
    return encrypted_bytes.decode('utf-8')

def decrypt_email(encrypted_email: str) -> str:
    """
    Unlocks the email.
    """
    if not encrypted_email: return ""
    try:
        decrypted_bytes = cipher.decrypt(encrypted_email.encode('utf-8'))
        return decrypted_bytes.decode('utf-8')
    except Exception:
        return "[ENCRYPTION ERROR]"

# ==========================================
# 3. PASSWORD HASHING (PBKDF2 SHA-256)
# ==========================================
def hash_password(password: str) -> str:
    """
    Hashes password with a random Salt.
    Result: "salt$hash"
    """
    salt = os.urandom(16).hex() # Generate random salt
    # PBKDF2 is slower and safer than standard SHA256
    hash_obj = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
    return f"{salt}${hash_obj.hex()}"

def verify_password(stored_entry: str, provided_password: str) -> bool:
    """
    Verifies the password matches the hash.
    """
    try:
        salt, stored_hash = stored_entry.split('$')
        new_hash = hashlib.pbkdf2_hmac('sha256', provided_password.encode(), salt.encode(), 100000)
        return new_hash.hex() == stored_hash
    except Exception:
        return False