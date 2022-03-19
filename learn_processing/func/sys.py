#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from functools import reduce
import functools
from operator import truediv
from re import X


def f(n):
    return n * n


r = map(f, [1, 2, 3])
print(list(r))
print(list(map(str, [2, 34, 4])))

# list(reduce(f, [1, 2, 3, 4]))


def o(n):
    return n % 2


filter(o, [
    1,
    23,
    4,
])


def _odd_iter():
    n = 1
    while True:
        n = n + 2
        yield n


print(sorted([36, 5, -12, 9, -21]))


def lazy_sum(*args):

    def sum():
        ax = 0
        for n in args:
            ax = ax + n
        return ax

    return sum


f = lambda x: x * x
print(f(5))
print(lazy_sum.__name__)


def log(func):

    def wrapper(*args, **kw):
        print('call %s():' % func.__name__)
        return func(*args, **kw)

    return wrapper


@log
def now():
    print('2015-3-25')


int2 = functools.partial(int, base=2)
int2(213)