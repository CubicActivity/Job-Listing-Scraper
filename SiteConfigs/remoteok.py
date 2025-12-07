import requests
# from utils import extract_skills
API_URL = "https://remoteok.com/api"

def fetch_remoteok():
    resp = requests.get(API_URL, headers={"User-Agent": "Mozilla/5.0"}, timeout=15)
    resp.raise_for_status()
    data = resp.json()
    if isinstance(data, list):
        data = data[1:]
    jobs = []
    for job in data:
        desc = job.get("description", "")
        jobs.append({
            "id": job.get("id", ""),
            "source": "remoteok",
            "title": job.get("position", ""),
            "company": job.get("company", ""),
            "category": ", ".join(job.get("tags", [])),
            "job_type": job.get("job_type", ""),
            "location": job.get("location", ""),
            "url": "https://remoteok.com" + job.get("url", ""),
            "publication_date": job.get("date", ""),
            # "skills": extract_skills(job.get("position", "") + " " + desc),
        })
    return jobs