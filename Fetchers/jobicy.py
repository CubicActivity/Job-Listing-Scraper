# Fetchers/jobicy.py
import time
import requests
from utils import extract_skills

API_URL = "https://jobicy.com/api/v2/remote-jobs"

INDUSTRIES = [
    "engineering",
    "marketing",
    "supporting",
]

_last_call_time = 0
def fetch_jobicy(page=1):
    global _last_call_time

    try:
        elapsed = time.time() - _last_call_time
        if elapsed < 1.0:
            time.sleep(1.0 - elapsed)
        _last_call_time = time.time()

        headers = {"User-Agent": "Mozilla/5.0"}
        industry = INDUSTRIES[(page - 1) % len(INDUSTRIES)]
        params = {"count": 100, "industry": industry}

        resp = requests.get(API_URL, params=params, headers=headers, timeout=15)

        if resp.status_code == 429:
            print(f"Jobicy {industry}: Rate limited (429)")
            return []

        resp.raise_for_status()
        data = resp.json()
        all_jobs = data.get("jobs", [])

        jobs = []
        for job in all_jobs:
            jobs.append({
                "id": str(job.get("id", "")),
                "source": "jobicy",
                "title": job.get("jobTitle", ""),
                "company": job.get("companyName", ""),
                "category": ", ".join(job.get("jobIndustry", [])),
                "job_type": ", ".join(job.get("jobType", [])),
                "location": job.get("jobGeo", ""),
                "url": job.get("url", ""),
                "publication_date": job.get("pubDate", ""),
                "skills": extract_skills(job.get("jobDescription", "")),
            })
        return jobs
    except Exception as e:
        print(f"Jobicy error: {e}")
        return []