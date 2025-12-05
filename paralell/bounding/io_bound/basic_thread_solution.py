import threading
import requests
import time

URL = "https://google.com"
N = 100

results :list[str] = []

def download():
    resp = requests.get(URL)
    results.append(resp.text)

threads : list[threading.Thread] = []

for _ in range(N):
    t = threading.Thread(target=download)
    threads.append(t)


print(f"Start {N} request")
start = time.perf_counter()
for t in threads:
    t.start()
for t in threads:
    t.join()
end = time.perf_counter()
diff = end-start
print(f"Done with: {len(results)} in {diff:.6f} seconds")
