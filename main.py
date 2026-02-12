import datetime
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

    # Sequential baseline
    t0 = time.time()
    serial_jobs = []
    for f in fetchers:  # Removed tqdm
        serial_jobs.extend(f())
    serial_time = time.time() - t0
    print(f"Sequential fetched {len(serial_jobs)} jobs in {serial_time:.2f}s")

    # 2 threads
    t1 = time.time()
    parallel_jobs = fetch_jobs(fetchers, max_workers=2)
    parallel_time = time.time() - t1
    print(f"2 threads fetched {len(parallel_jobs)} jobs in {parallel_time:.2f}s")

    # 4 threads
    t2 = time.time()
    parallel_jobs2 = fetch_jobs(fetchers, max_workers=4)
    parallel_time2 = time.time() - t2
    print(f"4 threads fetched {len(parallel_jobs2)} jobs in {parallel_time2:.2f}s")

    # 5 threads
    t3 = time.time()
    parallel_jobs3 = fetch_jobs(fetchers, max_workers=5)
    parallel_time3 = time.time() - t3
    print(f"5 threads fetched {len(parallel_jobs3)} jobs in {parallel_time3:.2f}s")


    # 6 threads
    t4 = time.time()
    parallel_jobs4 = fetch_jobs(fetchers, max_workers=8)
    parallel_time4 = time.time() - t4
    print(f"8 threads fetched {len(parallel_jobs4)} jobs in {parallel_time4:.2f}s")

    export_jobs(parallel_jobs4, str(datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S").replace(":", "-")))

    print(f"\nSpeedup (2 threads): {serial_time / parallel_time:.2f}x")
    print(f"Speedup (4 threads): {serial_time / parallel_time2:.2f}x")
    print(f"Speedup (5 threads): {serial_time / parallel_time3:.2f}x")
    print(f"Speedup (6 threads): {serial_time / parallel_time4:.2f}x")