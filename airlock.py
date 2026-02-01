import os
import re
from uuid import uuid4

# ==========================================
# CONFIGURATION
# ==========================================
UPLOAD_FOLDER = "secure_uploads"
ALLOWED_EXTENSIONS = {'.pdf'}

# Create the folder immediately
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ==========================================
# 2. ROLE VERIFICATION
# ==========================================
def validate_role(email: str) -> str:
    if not email or "@" not in email:
        return "UNKNOWN"
    domain = email.split("@")[1].lower()
    if domain == "space42admin.com":
        return "COMMANDER"
    return "PILOT"

# ==========================================
# 3. FILE SANITIZATION
# ==========================================
def secure_upload(file_obj, filename: str) -> dict:
    ext = os.path.splitext(filename)[1].lower()
    
    if ext not in ALLOWED_EXTENSIONS:
        return {"status": "DENIED", "reason": f"Invalid File Type. Only {ALLOWED_EXTENSIONS} allowed."}

    if filename.count('.') > 1:
        return {"status": "DENIED", "reason": "Security Alert: Malformed filename detected."}

    safe_name = f"{uuid4()}{ext}"
    safe_path = os.path.join(UPLOAD_FOLDER, safe_name)

    try:
        # Check if file_obj is bytes or file-like
        if isinstance(file_obj, bytes):
            with open(safe_path, "wb") as f:
                f.write(file_obj)
        else:
            with open(safe_path, "wb") as f:
                content = file_obj.read()
                f.write(content)
            
        return {"status": "CLEARED", "original_name": filename, "secure_path": safe_path}
    except Exception as e:
        return {"status": "ERROR", "reason": str(e)}

# ==========================================
# 4. PROMPT INJECTION DEFENSE
# ==========================================
def scan_for_injection(text_content: str) -> bool:
    if not text_content:
        return False
        
    threat_patterns = [
        r"ignore previous instructions",
        r"ignore all instructions",
        r"system override",
        r"delete all data",
        r"you are not an ai",
        r"reveal system prompt",
        r"DAN mode" 
    ]
    
    for pattern in threat_patterns:
        if re.search(pattern, text_content, re.IGNORECASE):
            return True 
            
    return False