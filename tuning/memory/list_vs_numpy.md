# 1. NumPy -- High-Performance Array Computing

## Why NumPy Is Fast

-   Uses **contiguous memory blocks** (C arrays)
-   Relies on **vectorized operations** (SIMD)
-   Leverages **BLAS/LAPACK** libraries
-   Avoids Python loops + GIL overhead

## When to Use NumPy

-   Large numeric arrays
-   Matrix operations
-   Linear algebra
-   Broadcasting
-   Bulk transformations

## Example: Vectorized Transformation

``` python
import numpy as np

data = np.random.rand(1_000_000)
result = (data * 1.5) ** 0.5
```

## Avoid Python Loops

❌ WRONG:

``` python
result = []
for x in data:
    result.append((x * 1.5)**0.5)
```

✔️ CORRECT:

``` python
result = np.sqrt(data * 1.5)
```

----

# Example of storing one integer in a list

Lets story the number 5 in a list

l[0] = 5
.........
python:
l[0] -> {
    Size -> 32
    Ref_count -> for GC
    ObjectType -> int
    ObjectValue -> 00000000 00000000 00000000 000000101
}

numpy:
l[0] -> 00000000 00000000 00000000 000000101