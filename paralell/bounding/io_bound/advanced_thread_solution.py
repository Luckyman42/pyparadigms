from concurrent.futures import ThreadPoolExecutor, as_completed
import httpx
import time

URL = "https://google.com"
N = 100

results :list[str] = []

def download():
    resp = httpx.get(URL)
    results.append(resp.text)

print(f"Start {N} request")
start = time.perf_counter()

with ThreadPoolExecutor(max_workers=20) as executor:
    futures = [executor.submit(download) for _ in range(N)]
    for f in as_completed(futures):
        _ = f.result()

end = time.perf_counter()
diff = end-start
print(f"Done with: {len(results)} in {diff:.6f} seconds")
