import requests
from utils import extract_skills
API_URL = "https://www.arbeitnow.com/api/job-board-api"

def fetch_arbeitnow():
    resp = requests.get(API_URL, timeout=15)
    resp.raise_for_status()
    jobs = []
    for job in resp.json().get("data", []):
        desc = job.get("description", "")
        jobs.append({
            "id": job.get("slug", ""),
            "source": "arbeitnow",
            "title": job.get("title", ""),
            "company": job.get("company_name", ""),
            "category": job.get("tags", [""])[0] if job.get("tags") else "",
            "job_type": job.get("employment_type", ""),
            "location": job.get("location", ""),
            "url": job.get("url", ""),
            "publication_date": job.get("created_at", ""),
            "skills": extract_skills(desc),
        })
    return jobs