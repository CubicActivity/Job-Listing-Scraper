import requests
from utils import extract_skills
API_URL = "https://remotive.com/api/remote-jobs"

def fetch_remotive():
    resp = requests.get(API_URL, timeout=15)
    resp.raise_for_status()
    jobs = []
    for job in resp.json().get("jobs", []):
        desc = job.get("description", "")
        jobs.append({
            "id": job.get("id", ""),
            "source": "remotive",
            "title": job.get("title", ""),
            "company": job.get("company_name", ""),
            "category": job.get("category", ""),
            "job_type": job.get("job_type", ""),
            "location": job.get("candidate_required_location", ""),
            "url": job.get("url", ""),
            "publication_date": job.get("publication_date", ""),
            "skills": extract_skills(job.get("title", "") + " " + desc),
        })
    return jobs