import time
from pathlib import Path
from multiprocessing import Pool

import pandas as pd
import requests
from requests.adapters import HTTPAdapter, Retry
from tqdm import tqdm

from JobListSites.remotive import fetch_remotive_serial
from JobListSites.themuse import fetch_themuse_serial
from JobListSites.arbeitnow import fetch_arbeitnow_serial
from JobListSites.remoteok import fetch_remoteok_serial

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

def run_fetcher(fetcher):
    return fetcher()

def collect_jobs_parallel(fetchers, processes: int = 4):
    with Pool(processes=processes) as pool:
        results = list(tqdm(pool.imap(run_fetcher, fetchers), total=len(fetchers), desc="Parallel fetching"))
    all_jobs = [job for sublist in results for job in sublist]
    return all_jobs

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

if __name__ == "__main__":
    fetchers = [
        fetch_remotive_serial,
        fetch_themuse_serial,
        fetch_arbeitnow_serial,
        fetch_remoteok_serial,
    ]

    # Serial benchmark
    t0 = time.time()
    serial_jobs = []
    for f in tqdm(fetchers, desc="Serial fetching"):
        serial_jobs.extend(f())
    serial_time = time.time() - t0
    print(f"Serial collected {len(serial_jobs)} jobs in {serial_time:.2f}s")

    # Parallel benchmark 4 processes (multiprocessing)
    t1 = time.time()
    parallel_jobs = collect_jobs_parallel(fetchers, processes=4)
    parallel_time = time.time() - t1
    print(f"Parallel (4 processes) collected {len(parallel_jobs)} jobs in {parallel_time:.2f}s")

    # Parallel benchmark 8 processes (multiprocessing)
    t2 = time.time()
    parallel_jobs = collect_jobs_parallel(fetchers, processes=8)
    parallel_time = time.time() - t2
    print(f"Parallel (8 processes) collected {len(parallel_jobs)} jobs in {parallel_time:.2f}s")

    save_jobs(parallel_jobs)
    print(f"\nSpeedup factor in Parallel: {serial_time / parallel_time:.2f}x")
