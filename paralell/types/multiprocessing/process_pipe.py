from typing import Any
from multiprocessing import Process, Pipe

def child(conn : Any):
    conn.send("Hello from child")
    msg = conn.recv()
    print("Child got:", msg)
    conn.close()

parent_conn, child_conn = Pipe()

p = Process(target=child, args=(child_conn,))
p.start()

print("Parent got:", parent_conn.recv())
parent_conn.send("Hello from parent")

p.join()
