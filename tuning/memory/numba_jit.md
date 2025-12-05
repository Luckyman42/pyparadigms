# Numba -- JIT Accelerator for Python

## Why Numba?

-   Compiles Python code to machine code
-   Removes Python overhead + GIL when using `parallel=True`
-   Works best on:
    -   numerical loops
    -   array operations
    -   physics simulations
    -   tight CPU-bound logic

## Install

``` bash
pip install numba
```

## Basic JIT Example

``` python
from numba import njit

@njit
def fast_sum(arr):
    total = 0.0
    for x in arr:
        total += x
    return total
```

## Parallel Version (GIL Released)

``` python
from numba import njit, prange

@njit(parallel=True)
def fast_parallel(arr):
    total = 0.0
    for i in prange(len(arr)):
        total += arr[i]
    return total
```

## What Numba Cannot JIT

-   Python objects
-   Complex nested classes
-   List/dict manipulations
-   IO operations
-   Asynchronous code
-   Most Python dynamic features

