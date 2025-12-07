from typing import ParamSpec, TypeVar
from collections.abc import Callable
from functools import wraps

P = ParamSpec('P')
R = TypeVar('R')

def decorator(fun : Callable[P,R]) -> Callable[P,R]:
    def wrapper_fun(*args : P.args, **kwargs : P.kwargs):
        return fun(*args,**kwargs)
    return wrapper_fun

print("Use a decorator which not use wraps")

@decorator
def fun1(word : str):
    """Function 1 documentation"""
    return word.upper()

print("fun1.__name__: ",fun1.__name__)
print("fun1.__annotations__: ",fun1.__annotations__)
print("fun1.__doc__: ",fun1.__doc__)

def decorator_w_wraps(fun : Callable[P,R]) -> Callable[P,R]:
    @wraps(fun)
    def wrapper_fun(*args : P.args, **kwargs : P.kwargs):
        return fun(*args,**kwargs)
    return wrapper_fun

print("Use a decorator which use wraps")

@decorator_w_wraps
def fun2(word : str):
    """Function 2 documentation"""
    return word.upper()

print("fun2.__name__: ",fun2.__name__)
print("fun2.__annotations__: ",fun2.__annotations__)
print("fun2.__doc__: ",fun2.__doc__)