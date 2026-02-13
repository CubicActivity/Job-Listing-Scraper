import requests
from utils import extract_skills

API_URL = "https://www.arbeitnow.com/api/job-board-api"

def fetch_arbeitnow(page=1):
    try:
        resp = requests.get(
            API_URL,
            params={"page": page},
            timeout=15
        )
        resp.raise_for_status()
        data = resp.json()
        page_jobs = data.get("data", [])
        jobs = []
        for job in page_jobs:
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

    except Exception as e:
        print(f"ArbeitNow error: {e}")
        return []