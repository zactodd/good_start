import utils
from typing import Set, Tuple, List
import random


def bird_selection(hand: List[str], tray: List[str]) -> Tuple[List[str], Set[str]]:
    for items in utils.BIRD_IMPORTANCE:
        birds, food_suggestion, tray_req = items.values()
        if all(b in hand or b == '*' for b in birds) and any(b in tray_req for b in tray):
            tray_wants = [b for b in tray if b in tray_req]
            if '*' in birds:
                return birds + [next(c for c in hand if c not in birds)], food_suggestion
            else:
                food_count = 5 - len(birds)
                food = {f for b in birds + tray_wants for f in utils.BIRD_FOOD[b][1].keys()}
                food -= {'Wild', 'Nectar'}
                if len(food) == food_count:
                    return birds, food
                elif len(food) < food_count:
                    return birds, food | set(random.sample(set(utils.FOOD) - food, food_count - len(food)))
                else:
                    return birds, food_suggestion



def bonus_selection(cards: List[str]) -> str:
    return min(cards, key=lambda c: utils.BONUS_IMPORTANCE.index(c))
