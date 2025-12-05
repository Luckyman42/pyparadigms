from concurrent.futures import ThreadPoolExecutor, Future
import time

def task(number : int) -> str: 
    print(f"{number} start")
    time.sleep(1)
    return f"{number}-done"

with ThreadPoolExecutor(max_workers=3) as pool:
    results : list[Future[str]] = []
    for i in range(10,1,-1):
        result = pool.submit(task,i)
        results.append(result)

for r in results:
    print(r.result())

print("\nThe same but with map\n")

with ThreadPoolExecutor(max_workers=3) as pool:
    results2 = pool.map(task, range(10,1,-1))
 
for r in results2:
    print(r)
