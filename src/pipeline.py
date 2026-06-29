import json
from src.ai_insights import generate_job_insights
from src.scraper import scrape_wwr_jobs

def run_basic_pipeline(parsed_input, api_key=None):
    """
    Simulates the pipeline flow for Phase 3.
    Takes parsed user input (Excel data or Text/URL) and fetches live scraped jobs,
    along with AI generated insights if an API key is provided.
    """
    # Fetch real live jobs instead of mock data
    live_jobs = scrape_wwr_jobs()
    
    matched_jobs = live_jobs
    
    if parsed_input.get("success"):
        # Let's say user typed some skills directly
        if "data" in parsed_input and isinstance(parsed_input["data"], str):
            user_text = parsed_input["data"].lower()
            # Simple keyword matching
            filtered_jobs = []
            for job in live_jobs:
                job_skills = [s.lower() for s in job.get("skills_required", [])]
                # If any skill matches the text input
                if any(skill in user_text for skill in job_skills):
                    filtered_jobs.append(job)
            
            if filtered_jobs:
                matched_jobs = filtered_jobs

    # Phase 2: Add AI insights if API key is present
    if api_key:
        for job in matched_jobs:
            insights = generate_job_insights(job, parsed_input.get("data"), api_key)
            if insights:
                job["insights"] = insights

    return {
        "status": "success",
        "jobs": matched_jobs,
        "message": f"Found {len(matched_jobs)} potential job matches."
    }
