import json
from src.ai_insights import generate_job_insights
from src.scraper import scrape_wwr_jobs
from src.scoring import calculate_relevance_score

def run_basic_pipeline(parsed_input, api_key=None):
    """
    Simulates the pipeline flow for Phase 4.
    Takes parsed user input (Excel data or Text/URL) and fetches live scraped jobs,
    scores them, and attaches AI generated insights if an API key is provided.
    """
    # Fetch real live jobs instead of mock data
    live_jobs = scrape_wwr_jobs()
    
    matched_jobs = live_jobs
    
    if parsed_input.get("success"):
        # Let's say user typed some skills directly
        if "data" in parsed_input and isinstance(parsed_input["data"], str):
            user_text = parsed_input["data"]
            
            # Phase 4: Relevance Scoring
            scored_jobs = []
            for job in live_jobs:
                score = calculate_relevance_score(job, user_text)
                job["relevance_score"] = score
                if score > 0: # Filter out completely irrelevant jobs
                    scored_jobs.append(job)
            
            # Sort jobs by relevance score descending
            scored_jobs.sort(key=lambda x: x.get("relevance_score", 0), reverse=True)
            
            if scored_jobs:
                matched_jobs = scored_jobs

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
