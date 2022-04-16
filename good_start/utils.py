import os
import json
from functools import cache
import psutil

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

_BIRD_GROUPS_FILE = os.path.join(RESOURCES, 'bird_groups.json')

with open(_BIRD_GROUPS_FILE, 'r') as f:
    BIRD_GROUPS = {b: g for g, birds in json.load(f).items() for b in birds}


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


def check_if_process_running(name):
    for proc in psutil.process_iter():
        try:
            if name.lower() in proc.name().lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False
