from multiprocessing import Queue
from concurrent.futures import ProcessPoolExecutor, as_completed
import httpx
import time

URL = "https://google.com"
N = 100

results = Queue(maxsize=N)

def download():
    resp = httpx.get(URL)
    results.put(resp.text)


print(f"Start {N} request")
start = time.perf_counter()

with ProcessPoolExecutor(max_workers=4) as executor:
    futures = [executor.submit(download) for _ in range(N)]
    for f in as_completed(futures):
        _ = f.result()

end = time.perf_counter()
diff = end-start
print(f"Done with: {results.qsize()} in {diff:.6f} seconds")
results.close()
