import requests
from utils import extract_skills

API_URL = "https://remoteok.com/api"


def fetch_remoteok(page=1):
    try:
        resp = requests.get(API_URL, headers={"User-Agent": "Mozilla/5.0"}, timeout=15)
        resp.raise_for_status()
        data = resp.json()

        # Skip metadata object (first item)
        if isinstance(data, list) and len(data) > 0:
            data = data[1:]

        # API returns ~97 jobs total, so use larger page size
        page_size = 100
        start = (page - 1) * page_size

        # Return empty list if page is beyond available data
        if start >= len(data):
            return []

        page_jobs = data[start:start + page_size]

        jobs = []
        for job in page_jobs:
            desc = job.get("description", "")
            jobs.append({
                "id": str(job.get("id", "")),
                "source": "remoteok",
                "title": job.get("position", ""),
                "company": job.get("company", ""),
                "category": ", ".join(job.get("tags", [])),
                "job_type": job.get("job_type", ""),
                "location": job.get("location", ""),
                "url": f"https://remoteok.com{job.get('url', '')}",
                "publication_date": job.get("date", ""),
                "skills": extract_skills(f"{job.get('position', '')} {desc}"),
            })
        return jobs

    except Exception as e:
        print(f"RemoteOK error: {e}")
        return []