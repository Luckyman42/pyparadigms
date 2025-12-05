from multiprocessing import Process, Manager

def worker(d, l):
    d["count"] += 1
    l.append(d["count"])

with Manager() as manager:
    d = manager.dict({"count": 0})
    l = manager.list()

    ps = [Process(target=worker, args=(d, l)) for _ in range(5)]
    for p in ps: p.start()
    for p in ps: p.join()

    print("Dict:", d)
    print("List:", list(l))
