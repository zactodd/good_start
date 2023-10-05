import os
import json
import csv
from typing import Iterable, TypeVar, Callable, Any
from functools import cache
from threading import Thread


F = TypeVar('F', bound=Callable[..., Any])


RESOURCES = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'resources')
SELECTED_IMAGES = os.path.join(RESOURCES, '.selected')
HABITATS = ['Forest', 'Grassland', 'Wetland']
FOOD = ['Fruit', 'Fish', 'Invertebrate', 'Rodent', 'Seed']


_BIRD_GROUPS_FILE = os.path.join(RESOURCES, 'bird_groups.json')

# with open(_BIRD_GROUPS_FILE, 'r') as f:
#     BIRD_GROUPS = {b: g for g, birds in json.load(f).items() for b in birds}

# _FULL_CARD_INFO_FILE = os.path.join(RESOURCES, 'card_list.tsv')
# with open(_FULL_CARD_INFO_FILE, 'r', encoding='cp437') as f:
#     _FULL_CARD_INFO = csv.DictReader(f, delimiter='\t')
#     _FOOD_COST = FOOD + ['Wild']
#
#     BIRD_HABITATS = {}
#     BIRD_FOOD = {}
#     for r in _FULL_CARD_INFO:
#         BIRD_HABITATS[r['Common name'].strip()] = tuple(h for h in HABITATS if r[h] == 'X')
#
#         food_cost = {f: int(c) for f in _FOOD_COST if (c := r[f])}
#         total = 1 if r['/ (food cost)'] == 'X' else sum(food_cost.values())
#         BIRD_FOOD[r['Common name'].strip()] = (total , food_cost)


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

