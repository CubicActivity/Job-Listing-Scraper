import requests
from utils import extract_skills
API_URL = "https://www.themuse.com/api/public/jobs"

def fetch_themuse(pages=3):
    jobs = []
    for page in range(1, pages+1):
        resp = requests.get(API_URL, params={"page": page}, timeout=15)
        resp.raise_for_status()
        for job in resp.json().get("results", []):
            categories = job.get("categories", [])
            category_name = categories[0]["name"] if categories else ""
            locations = job.get("locations", [])
            location_name = locations[0]["name"] if locations else ""
            contents = job.get("contents", "")
            jobs.append({
                "id": job.get("id", ""),
                "source": "themuse",
                "title": job.get("name", ""),
                "company": job.get("company", {}).get("name", ""),
                "category": category_name,
                "job_type": job.get("type", ""),
                "location": location_name,
                "url": job.get("refs", {}).get("landing_page", ""),
                "publication_date": job.get("publication_date", ""),
                "skills": extract_skills(job.get("name", "") + " " + contents),
            })
    return jobs