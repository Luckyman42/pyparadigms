import threading
import time

event = threading.Event()

def worker():
    print("Worker waiting for event...")
    event.wait()  # blocking
    print("Done")

t = threading.Thread(target=worker)
t.start()

time.sleep(2)
print("Event set!")
event.set()
t.join()



def worker2():
    print("Worker2 waiting for event...")
    while not event.is_set():
        event.wait(timeout=2)  # blocking
        if event.is_set():
            break
        print("event is not set yet")
    print("2 - done")

event.clear()
t = threading.Thread(target=worker2)
t.start()

time.sleep(5)
print("Event set!")
event.set()
