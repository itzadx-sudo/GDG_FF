import os
import re
import shutil
from uuid import uuid4

# ==========================================
# 1. CONFIGURATION
# ==========================================
# We hide uploads in a folder users can't directly access via URL
UPLOAD_FOLDER = "secure_uploads"
ALLOWED_EXTENSIONS = {'.pdf'}

# Create the folder immediately if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# ==========================================
# 2. ROLE VERIFICATION (The Gatekeeper)
# ==========================================
def validate_role(email: str) -> str:
    """
    Determines if the user is a Candidate (PILOT) or HR Admin (COMMANDER).
    
    Args:
        email (str): The user's email address.
        
    Returns:
        str: 'COMMANDER' if email is @space42admin.com, else 'PILOT'.
    """
    if not email or "@" not in email:
        return "UNKNOWN"
    
    # Extract domain (everything after @)
    domain = email.split("@")[1].lower()
    
    # 🔴 SECURITY CHECK: HR Privilege
    if domain == "space42admin.com":
        return "COMMANDER"
        
    # 🟢 DEFAULT ACCESS: Candidate
    return "PILOT"


# ==========================================
# 3. FILE SANITIZATION (The Shield)
# ==========================================
def secure_upload(file_obj, filename: str) -> dict:
    """
    Ingests a file, validates its type, and saves it with a secure random name.
    
    Args:
        file_obj: The raw file object (bytes) from the frontend.
        filename (str): The original filename (e.g. 'my_cv.pdf').
        
    Returns:
        dict: {'status': 'CLEARED'|'DENIED', 'secure_path': str, 'reason': str}
    """
    # A. Check File Extension
    # Get extension (e.g., .pdf)
    ext = os.path.splitext(filename)[1].lower()
    
    if ext not in ALLOWED_EXTENSIONS:
        return {
            "status": "DENIED", 
            "reason": f"Invalid File Type. Only {ALLOWED_EXTENSIONS} allowed."
        }

    # B. Double Extension Attack Check (e.g., "resume.pdf.exe")
    if filename.count('.') > 1:
        return {
            "status": "DENIED", 
            "reason": "Security Alert: Malformed filename detected."
        }

    # C. Anonymize the File
    # We rename the file to a random UUID so hackers can't guess paths
    safe_name = f"{uuid4()}{ext}"
    safe_path = os.path.join(UPLOAD_FOLDER, safe_name)

    # D. Write to Disk
    try:
        with open(safe_path, "wb") as f:
            # If using Flet/Streamlit, you might need file_obj.read()
            # If file_obj is already bytes, just file_obj
            content = file_obj.read() if hasattr(file_obj, 'read') else file_obj
            f.write(content)
            
        return {
            "status": "CLEARED",
            "original_name": filename,
            "secure_path": safe_path
        }
    except Exception as e:
        return {"status": "ERROR", "reason": str(e)}


# ==========================================
# 4. PROMPT INJECTION DEFENSE (The Guardrail)
# ==========================================
def scan_for_injection(text_content: str) -> bool:
    """
    Scans extracted text for malicious prompts designed to trick the AI.
    
    Args:
        text_content (str): The raw text extracted from the PDF.
        
    Returns:
        bool: True if a threat is detected, False if safe.
    """
    if not text_content:
        return False
        
    # List of common "Jailbreak" triggers
    threat_patterns = [
        r"ignore previous instructions",
        r"ignore all instructions",
        r"system override",
        r"delete all data",
        r"you are not an ai",
        r"reveal system prompt",
        r"DAN mode" 
    ]
    
    # Check against all patterns
    for pattern in threat_patterns:
        if re.search(pattern, text_content, re.IGNORECASE):
            # Log this event if you had a logger
            print(f"⚠️ SECURITY ALERT: Injection attempt detected: '{pattern}'")
            return True # Threat Found
            
    return False # Safe    return False