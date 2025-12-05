# Memory-Mapped File Operations

## What is mmap?

-   Treats files as if they were in memory without loading them fully
-   Kernel loads pages on demand
-   Perfect for large files
-   Low-memory environments
-   Random-access binary operations

## Basic Usage

``` python
import mmap

with open("data.txt", "r+b") as f:
    mm = mmap.mmap(f.fileno(), 0)
    print(mm[:100])  # read first 100 bytes
    mm.close()
```

## Modify File In-Place

``` python
with open("data.bin", "r+b") as f:
    mm = mmap.mmap(f.fileno(), 0)
    mm[5:10] = b"HELLO"
    mm.flush()
    mm.close()
```

## Remove First N Lines

``` python
def remove_first_n_lines(path, n):
    with open(path, "r+b") as f:
        mm = mmap.mmap(f.fileno(), 0)
        pos = 0
        for _ in range(n):
            p = mm.find(b"\n", pos)
            if p == -1:
                return
            pos = p + 1
        remaining = mm[pos:]
        f.seek(0)
        f.write(remaining)
        f.truncate(len(remaining))
        mm.close()
```
