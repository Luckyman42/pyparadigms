from multiprocessing import Process, Queue
import requests
import time

URL = "https://google.com"
N = 100


def download(q : Queue):
    resp = requests.get(URL)
    q.put(resp.text)

procs : list[Process]= []
results = Queue(maxsize=N)

for _ in range(N):
    p = Process(target=download, args=(results,))
    procs.append(p)

print(f"Start {N} request")
start = time.perf_counter()
for p in procs:
    p.start()
for p in procs:
    p.join()
end = time.perf_counter()
diff = end-start
print(f"Done with: {results.qsize()} in {diff:.6f} seconds")
results.close()
