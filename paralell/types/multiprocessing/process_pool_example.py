from multiprocessing import Pool
import time

def task(number : int) -> str: 
    print(f"{number} start")
    time.sleep(1)
    return f"{number}-done"

with Pool(processes=3) as pool:
    results2 = pool.map(task, range(10,1,-1))
 
for r in results2:
    print(r)

