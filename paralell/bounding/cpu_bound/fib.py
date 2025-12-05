N = 10
FIB_N = 30

def fib(n: int) -> int:
    if n < 2:
        return n
    return fib(n-1) + fib(n-2)
