import os
from typing import TypeVar, Any, Iterable, Callable, Iterator, Any, List
from functools import cache
from itertools import zip_longest, islice
from threading import Thread
from concurrent.futures import ThreadPoolExecutor, as_completed

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


def parallel_evaluate_iterable(iterable: Iterable[Any], func: F, num_threads: int) -> Iterator[List[Any]]:
    """
    Evaluates a task_function over an iterable in parallel using a ThreadPoolExecutor.
    It processes items in chunks (size = num_threads) and yields the results
    of each chunk as they are completed.

    :param iterable: The items to be evaluated.
    :param func: The function to apply to each item from the iterable.
                          It should take one item and return its result.
    :param num_threads: The number of worker threads to use in the pool.
                        This also defines the maximum size of each chunk yielded.
    :yields: Individual results (Any) from the processed items.
             The order of individual results is not guaranteed to match
             the input order, as they are yielded as their tasks complete
             within each chunk. If a task raises an exception, the exception
             object itself will be yielded for that task's result.
    """
    if num_threads <= 0:
        raise ValueError("num_threads (max_workers and chunk size) must be a positive integer.")

    # Use ThreadPoolExecutor for efficient parallel execution and result collection
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        # Iterate over the iterable in chunks of `num_threads` size
        for chunk in grouper(iterable, num_threads):
            # Submit each item in the current chunk to the executor
            # and store the Future objects
            futures = {executor.submit(func, item) for item in chunk}

            chunk_results = []
            # Wait for all futures in the current chunk to complete
            # `as_completed` yields futures as they finish, so order might not be preserved
            # relative to the input chunk order, but all results from *this chunk* will be yielded together.
            for future in as_completed(futures):
                try:
                    # Get the result from the completed future
                    chunk_results.append(future.result())
                except Exception as exc:
                    # If a task raised an exception, catch it and store the exception object
                    chunk_results.append(exc)

            # Yield the collected results for the current chunk
            for result in chunk_results:
                yield result

