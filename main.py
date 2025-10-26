import time
from utils import *

from JobListSites.remotive import fetch_remotive
from JobListSites.themuse import fetch_themuse
from JobListSites.arbeitnow import fetch_arbeitnow
from JobListSites.remoteok import fetch_remoteok

if __name__ == "__main__":
    fetchers = [
        fetch_remotive,
        fetch_themuse,
        fetch_arbeitnow,
        fetch_remoteok,
    ]
    # Serial process benchmark
    t0 = time.time()
    serial_jobs = []
    for f in tqdm(fetchers, desc="Serial fetching"):
        serial_jobs.extend(f())
    serial_time = time.time() - t0
    print(f"Serial collected {len(serial_jobs)} jobs in {serial_time:.2f}s")

    # Parallel processes benchmark 4 processes (multiprocessing)
    t1 = time.time()
    parallel_jobs = collect_jobs_parallel(fetchers, processes=4)
    parallel_time = time.time() - t1
    print(f"Parallel (4 processes) collected {len(parallel_jobs)} jobs in {parallel_time:.2f}s")

    # Parallel processes benchmark 8 processes (multiprocessing)
    t2 = time.time()
    parallel_jobs = collect_jobs_parallel(fetchers, processes=8)
    parallel_time = time.time() - t2
    print(f"Parallel (8 processes) collected {len(parallel_jobs)} jobs in {parallel_time:.2f}s")

    save_jobs(parallel_jobs)
    print(f"\nSpeedup factor in Parallel: {serial_time / parallel_time:.2f}x")
