from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
import pandas as pd
from tqdm import tqdm

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

def fetch_jobs(fetchers, max_workers: int = 4):
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        results = list(executor.map(run_fetcher, fetchers))
    jobs = [job for sublist in results for job in sublist]
    return jobs

def run_fetcher(fetcher):
    return fetcher()

def extract_skills(text: str) -> str:
    found = [skill for skill in COMMON_SKILLS if skill.lower() in text.lower()]
    return ", ".join(found)

def export_jobs(jobs, filename="jobs.csv"):
    Path("Results").mkdir(exist_ok=True)
    df = pd.DataFrame(jobs)
    for col in FIELDS:
        if col not in df.columns:
            df[col] = ""
    df = df[FIELDS]
    df.drop_duplicates(subset=["title", "company", "url"], inplace=True)
    df.to_csv(Path("Results") / filename, index=False)
    print(f"\nSaved {len(df)} entries at Results/{filename}")

























