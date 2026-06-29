import requests
from bs4 import BeautifulSoup

def scrape_wwr_jobs():
    """
    Scrapes the 'We Work Remotely' programming category for live remote jobs.
    Returns a list of dictionaries matching the pipeline format.
    """
    url = "https://weworkremotely.com/categories/remote-programming-jobs"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    jobs_data = []
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find all job list items
        job_listings = soup.find_all('li', class_='feature')
        
        for idx, job in enumerate(job_listings):
            # We Work Remotely specific HTML structure parsing
            company_elem = job.find('span', class_='company')
            title_elem = job.find('span', class_='title')
            region_elem = job.find('span', class_='region')
            
            # The main link is usually the first <a> tag inside the li
            link_elem = job.find('a', href=True)
            
            if company_elem and title_elem:
                title = title_elem.text.strip()
                company = company_elem.text.strip()
                location = region_elem.text.strip() if region_elem else "Remote"
                link = "https://weworkremotely.com" + link_elem['href'] if link_elem else url
                
                # We Work Remotely doesn't explicitly list skills on the preview page,
                # so we can parse them from the title or just leave them open for AI to deduce.
                # For this agent, we'll extract some generic keywords from the title as required skills.
                keywords = title.replace(",", "").replace("-", " ").split()
                skills = [word for word in keywords if len(word) > 2]
                
                jobs_data.append({
                    "id": idx + 1,
                    "title": title,
                    "company": company,
                    "location": location,
                    "description": f"Live remote programming job at {company}.",
                    "skills_required": skills,
                    "link": link
                })
                
            # Limit to 10 jobs to keep API costs down for Phase 2 insights
            if len(jobs_data) >= 10:
                break
                
        return jobs_data
        
    except Exception as e:
        print(f"Failed to scrape jobs: {e}")
        return []
