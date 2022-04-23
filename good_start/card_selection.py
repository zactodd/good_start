import utils
from typing import List, Tuple


def bird_selection(hand: List[str], tray: List[str]) -> Tuple[List[str], List[str]]:
    for items in utils.BIRD_IMPORTANCE:
        birds, food, tray_req = items.values()
        if all(b in hand for b in birds) and any(b in tray_req for b in tray):
            if len(birds) + len(food) == 5:
                return birds, food
            else:
                return birds + [next(c for c in hand if c not in birds)], food


def bonus_selection(cards: List[str]) -> str:
    return min(cards, key=lambda c: utils.BONUS_IMPORTANCE.index(c))
