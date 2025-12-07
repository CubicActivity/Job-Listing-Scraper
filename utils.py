from multiprocessing import Pool
from pathlib import Path

import pandas as pd
import requests
from requests.adapters import HTTPAdapter
from tqdm import tqdm
from urllib3 import Retry

COMMON_SKILLS = [
    "Python", "JavaScript", "Java", "C++", "C#", "Ruby", "Go",
    "React", "Angular", "Vue", "Django", "Flask", "Node.js",
    "AWS", "GCP", "Azure", "Docker", "Kubernetes", "SQL", "NoSQL",
    "HTML", "CSS", "TypeScript", "Machine Learning", "Data Science",
]

FIELDS = [
    "id", "source", "title", "company", "category", "job_type",
    "location", "url", "publication_date", "skills",
]

def get_session() -> requests.Session:
    retry_strategy = Retry(
        total=5,
        status_forcelist=[429, 500, 502, 503, 504],
        backoff_factor=1,
        allowed_methods=["HEAD", "GET", "OPTIONS"],
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session = requests.Session()
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session

def collect_jobs_parallel(fetchers, processes: int = 4):
    with Pool(processes=processes) as pool:
        results = list(tqdm(pool.imap(run_fetcher, fetchers), total=len(fetchers), desc="Parallel fetching"))
    all_jobs = [job for sublist in results for job in sublist]
    return all_jobs

def run_fetcher(fetcher):
    return fetcher()

# def extract_skills(text: str) -> str:
#     found = [skill for skill in COMMON_SKILLS if skill.lower() in text.lower()]
#     return ", ".join(found)

def save_jobs(jobs, filename="jobs.csv"):
    Path("CSV").mkdir(exist_ok=True)
    df = pd.DataFrame(jobs)
    for col in FIELDS:
        if col not in df.columns:
            df[col] = ""
    df = df[FIELDS]
    df.drop_duplicates(subset=["title", "company", "url"], inplace=True)
    df.to_csv(Path("CSV") / filename, index=False)
    print(f"\nSaved {len(df)} jobs to CSV/{filename}")
