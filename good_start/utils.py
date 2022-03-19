import os
from functools import cache

RESOURCES = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'resources')
_BIRD_NAMES_FILE = os.path.join(RESOURCES, 'bird_names.txt')

with open(_BIRD_NAMES_FILE, 'r') as f:
    BIRD_NAMES = [line.strip() for line in f]


@cache
def minimum_edit_distance(a, b, m=None, n=None):
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
