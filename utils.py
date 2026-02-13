from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import pandas as pd

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

def generate_fetch_tasks(fetchers_with_pages):
    """
    Expand fetchers into individual page tasks.
    Input: [(fetcher_func, pages), ...]
    Output: [(fetcher_func, page_num), ...]
    """
    tasks = []
    for fetcher, pages in fetchers_with_pages:
        for page in range(1, pages + 1):
            tasks.append((fetcher, page))
    return tasks


def fetch_jobs(tasks, threads: int = 4):
    """
    Execute fetch tasks in parallel.
    tasks = [(fetcher_func, page), ...]
    """
    with ThreadPoolExecutor(threads) as executor:
        futures = [executor.submit(f, page) for f, page in tasks]
        results = [f.result() for f in futures]

    jobs = [job for sublist in results for job in sublist]
    return jobs

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
    print(f"\nSaved {len(df)} unique entries at Results/{filename}")