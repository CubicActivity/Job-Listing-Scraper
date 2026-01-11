import time
from utils import *
from Fetchers.remotive import fetch_remotive
from Fetchers.themuse import fetch_themuse
from Fetchers.arbeitnow import fetch_arbeitnow
from Fetchers.remoteok import fetch_remoteok

if __name__ == "__main__":
    fetchers = [
        fetch_remotive,
        fetch_themuse,
        fetch_arbeitnow,
        fetch_remoteok,
    ]
    
    # single processes benchmark
    t0 = time.time()
    serial_jobs = []
    for f in tqdm(fetchers, desc="Single process fetching"):
        serial_jobs.extend(f())
    serial_time = time.time() - t0
    print(f"Single processe collected {len(serial_jobs)} jobs in {serial_time:.2f}s")

    # 4 processes benchmark 
    t1 = time.time()
    parallel_jobs = fetch_jobs(fetchers, processes=4)
    parallel_time = time.time() - t1
    print(f"Parallel (4 processes) collected {len(parallel_jobs)} jobs in {parallel_time:.2f}s")

    # 8 processes benchmark 
    t2 = time.time()
    parallel_jobs2 = fetch_jobs(fetchers, processes=8)
    parallel_time2 = time.time() - t2
    print(f"Parallel (8 processes) collected {len(parallel_jobs2)} jobs in {parallel_time2:.2f}s")

    export_jobs(parallel_jobs)
    print(f"Speedup factor in Parallel: {serial_time / min(parallel_time2,parallel_time):.2f}x")
