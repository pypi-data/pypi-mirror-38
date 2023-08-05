from functools import reduce
from itertools import chain, combinations
from math import factorial
from typing import Collection, Iterator, List, Tuple, TypeVar

__all__ = ['C', 'P', 'powerset']

T = TypeVar('T')


def C(n: int, *k: int) -> int:
    if len(k) == 1:
        return factorial(n) // (factorial(n - k[0]) * factorial(k[0]))
    return factorial(n) // reduce(lambda x, y: x * y,
                                  map(lambda x: factorial(x), k))


def P(n: int, k: int) -> int:
    return factorial(n) // (factorial(n - k))


def powerset_generator(iterable: Collection[T]) -> Iterator[Tuple[T]]:
    """https://stackoverflow.com/questions/1482308/how-to-get-all-subsets-of-a-set-powerset"""
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(1, len(s) + 1))


def powerset(iterable: Collection[T]) -> List[Tuple[T]]:
    return list(powerset_generator(iterable))
