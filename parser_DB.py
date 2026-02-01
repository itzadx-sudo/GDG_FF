import concurrent.futures
from database import update_ai_results
from airlock import scan_for_injection

# --- THE CONNECTION ---
# Member 2 imports Member 3's work here:
from parser_SIB import parse_resume_to_json 

def process_candidate(candidate_id, file_path):
    """
    The Manager Function:
    1. Checks Security
    2. Asks Brain for analysis
    3. Saves to DB
    """
    try:
        # Step A: Ask the Brain (Member 3)
        # This is the slow part (AI), so it runs in a thread
        ai_result = parse_resume_to_json(file_path)
        
        # Step B: Check Security (Member 2)
        # We scan the text the AI found for "Ignore previous instructions"
        raw_text = ai_result.get("raw_text", "") # Ensure Brain returns this!
        if scan_for_injection(raw_text):
            update_ai_results(candidate_id, 0, "THREAT DETECTED", "THREAT_BLOCKED")
            return "THREAT_BLOCKED"

        # Step C: Save to Database (Member 2)
        score = ai_result.get("years_experience", 0) * 10 # Simplified scoring
        weakness = ai_result.get("weakness", "General")
        
        update_ai_results(candidate_id, score, weakness, "MISSION_READY")
        return "SUCCESS"
        
    except Exception as e:
        print(f"Error: {e}")
        # [FIX] Update DB even on error, so the App doesn't hang forever
        update_ai_results(candidate_id, 0, f"SYSTEM FAILURE: {str(e)}", "THREAT_BLOCKED")
        return "FAILED"

def run_parallel_parsing(candidates_list):
    """
    Run the manager function for 4 candidates at once.
    candidates_list = [(1, "path/to/cv1.pdf"), (2, "path/to/cv2.pdf")]
    """
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        # Map the function to the data
        futures = [
            executor.submit(process_candidate, cid, path) 
            for cid, path in candidates_list
        ]
        concurrent.futures.wait(futures)