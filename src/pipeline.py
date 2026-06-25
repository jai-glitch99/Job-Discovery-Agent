import json
import os

def load_mock_jobs():
    """Loads mock job data from the JSON file."""
    # Build path to the data folder relative to this file
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    mock_file_path = os.path.join(base_dir, 'data', 'mock_jobs.json')
    
    try:
        with open(mock_file_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading mock data: {e}")
        return []

def run_basic_pipeline(parsed_input):
    """
    Simulates the basic pipeline flow (Phase 1).
    Takes parsed user input (Excel data or Text/URL) and returns relevant mock jobs.
    """
    mock_jobs = load_mock_jobs()
    
    # In a real scenario (Phase 2 & 3), we would extract keywords from parsed_input using AI
    # and match them against real job listings. 
    # For Phase 1, we will just return the mock jobs to validate the flow.
    # Optionally, we can do a very basic filter if skills are provided in text.
    
    matched_jobs = mock_jobs
    
    if parsed_input.get("success"):
        # Let's say user typed some skills directly
        if "data" in parsed_input and isinstance(parsed_input["data"], str):
            user_text = parsed_input["data"].lower()
            # Simple keyword matching
            filtered_jobs = []
            for job in mock_jobs:
                job_skills = [s.lower() for s in job.get("skills_required", [])]
                # If any skill matches the text input
                if any(skill in user_text for skill in job_skills):
                    filtered_jobs.append(job)
            
            if filtered_jobs:
                matched_jobs = filtered_jobs

    return {
        "status": "success",
        "jobs": matched_jobs,
        "message": f"Found {len(matched_jobs)} potential job matches."
    }
