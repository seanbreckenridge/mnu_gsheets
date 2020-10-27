from backoff import fibo
from typing import Iterator

def fibo_long() -> Iterator[int]:
    f = fibo()
    for _ in range(5):
        next(f)
    yield from f
