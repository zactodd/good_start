import os
import json
from functools import cache
import random

RESOURCES = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'resources')
SELECTED_IMAGES = os.path.join(RESOURCES, '.selected')

_BIRD_NAMES_FILE = os.path.join(RESOURCES, 'bird_names.txt')

with open(_BIRD_NAMES_FILE, 'r') as f:
    BIRD_NAMES = [line.strip() for line in f]


_BIRD_IMPORTANCE_FILE = os.path.join(RESOURCES, 'bird_card_importance.json')

with open(_BIRD_IMPORTANCE_FILE, 'r') as f:
    BIRD_IMPORTANCE = json.load(f)


_BONUS_IMPORTANCE_FILE = os.path.join(RESOURCES, 'bonus_card_importance.txt')

with open(_BONUS_IMPORTANCE_FILE, 'r') as f:
    BONUS_IMPORTANCE = [line.strip() for line in f]


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


def sample_prob(sample=1000):
    return sum(any(all(b in hand for b in bird['birds']) for bird in BIRD_IMPORTANCE)
                    for hand in map(lambda _: random.sample(BIRD_NAMES, 5), range(sample))) / sample
