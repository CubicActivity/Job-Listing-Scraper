import os
import time
import threading

from dotenv import load_dotenv
import requests
from utils import extract_skills

load_dotenv()

API_URL = "https://findwork.dev/api/jobs/"
API_TOKEN = os.getenv("FINDWORK_API_TOKEN")

_rate_limit_lock = threading.Lock()
_last_call_time = 0


def fetch_findwork(page=1):
    global _last_call_time

    try:
        with _rate_limit_lock:
            elapsed = time.time() - _last_call_time
            if elapsed < 1.0:
                time.sleep(1.0 - elapsed)

        headers = {
            "Authorization": f"Token {API_TOKEN}",
            "User-Agent": "Mozilla/5.0"
        }

        resp = requests.get(
            API_URL,
            headers=headers,
            params={"page": page},
            timeout=15
        )
        resp.raise_for_status()

        data = resp.json()
        all_jobs = data.get("results", [])

        jobs = []
        for job in all_jobs:
            jobs.append({
                "id": str(job.get("id", "")),
                "source": "findwork",
                "title": job.get("role", ""),
                "company": job.get("company_name", ""),
                "category": ", ".join(job.get("keywords", [])),
                "job_type": "remote" if job.get("remote") else "onsite",
                "location": job.get("location", "Remote"),
                "url": job.get("url", ""),
                "publication_date": job.get("date_posted", ""),
                "skills": extract_skills(job.get("role", "") + " " + " ".join(job.get("keywords", []))),
            })
        return jobs
    except Exception as e:
        print(f"Findwork error: {e}")
        return []