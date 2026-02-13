import datetime
import time
from utils import *
from Fetchers.jobicy import fetch_jobicy
from Fetchers.arbeitnow import fetch_arbeitnow
from Fetchers.remoteok import fetch_remoteok
from Fetchers.findwork import fetch_findwork

if __name__ == "__main__":
    fetchers= [
        (fetch_arbeitnow, 2),
        (fetch_jobicy, 3),
        (fetch_findwork, 2),
        (fetch_remoteok, 1)
    ]
    tasks = generate_fetch_tasks(fetchers)
    print(f"Fetching from {len(fetchers)} portals, total of: {len(tasks)} pages\n")

    sequential_jobs = []
    startTime = time.time()
    for fetcher, page in tasks:
        sequential_jobs.extend(fetcher(page))
    sequential_time = time.time() - startTime
    print(f"1 thread: {len(sequential_jobs)} jobs in {sequential_time:.2f}s")

    t2 = time.time()
    parallel_jobs = fetch_jobs(tasks, threads=2)
    parallel_time = time.time() - t2
    print(f"2 threads:  {len(parallel_jobs)} jobs in {parallel_time:.2f}s ({sequential_time / parallel_time:.2f}x)")

    t3 = time.time()
    parallel_jobs2 = fetch_jobs(tasks, threads=4)
    parallel_time2 = time.time() - t3
    print(f"4 threads:  {len(parallel_jobs2)} jobs in {parallel_time2:.2f}s ({sequential_time / parallel_time2:.2f}x)")

    t4 = time.time()
    parallel_jobs3 = fetch_jobs(tasks, threads=8)
    parallel_time3 = time.time() - t4
    print(f"8 threads:  {len(parallel_jobs3)} jobs in {parallel_time3:.2f}s ({sequential_time / parallel_time3:.2f}x)")

    export_jobs(parallel_jobs, str(datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S").replace(":", "-")))