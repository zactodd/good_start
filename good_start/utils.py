import os
import json
import csv
from typing import Iterable, TypeVar, Callable, Any
from functools import cache
from itertools import zip_longest
from threading import Thread


F = TypeVar('F', bound=Callable[..., Any])

RESOURCES = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'resources')
SELECTED_IMAGES = os.path.join(RESOURCES, '.selected')


@cache
def minimum_edit_distance(a: str, b: str, m=None, n=None) -> int:
    if m is None:
        m, n = len(a),  len(b)
    if m == 0:
        return n
    elif n == 0:
        return m
    elif a[m - 1] == b[n - 1]:
        return minimum_edit_distance(a, b, m - 1, n - 1)
    else:
        return 1 + min(
            minimum_edit_distance(a, b, m, n - 1),
            minimum_edit_distance(a, b, m - 1, n),
            minimum_edit_distance(a, b, m - 1, n - 1)
        )


def start_join_threads(threads: Iterable['Thread']) -> None:
    """
    Starts all threads in threads and joins all the threads.
    :param threads: AN iterable of threads.
    """
    for t in threads:
        t.start()
    for t in threads:
        t.join()


def thread_wrapper(func: F) -> F:
    """
    Wraps a function into a thread call.
    :param func: The function to be wrapped.
    :return: A function wrapped to a thread call.
    """
    def wrapper(*args, **kwargs):
        return Thread(target=func, args=args, kwargs=kwargs)
    return wrapper


def grouper(iterable: Iterable, n: int) -> Iterable:
    """
    Groups the iterable into a iterable of iterable of len n,
    e.g.((x0, x1, ..., xn-1), ((xn, xn+1, ..., x2n-1)), ...)
    :param iterable: The iterable to be grouped.
    :param n: The length of the groups. (The last group may be less the n in length.)
    :return: An iterable which groups objects into batches.
    """
    return zip_discard_generator(*([iter(iterable)] * n))


def zip_discard_generator(*iterables, sentinel: Any = object()):
    return ((entry for entry in iterable if entry is not sentinel)
            for iterable in zip_longest(*iterables, fillvalue=sentinel))


def parallel_evaluate_iterable(iterable, generate_thread_func: Callable[..., Thread], num_threads: int) -> None:
    """
    Evaluates a function over an iterable in parallel over several threads.
    :param iterable: The items to be evaluated.
    :param generate_thread_func: The function evaluating the items.
    :param num_threads: The number of threads to use.
    """
    if len(iterable) <= num_threads:
        threads = map(generate_thread_func, iterable)
        start_join_threads(threads)
    else:
        for g in grouper(iterable, num_threads):
            threads = map(generate_thread_func, g)
            start_join_threads(threads)

