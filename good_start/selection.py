import utils
from typing import Set, Tuple, List
import cards


def bird_selection(hand: List[str], tray: List[str]) -> List[str]:
    for items in cards.Deck().bird_importance:
        birds, tray_req = items.values()
        if all(b in hand for b in birds) and any(b in tray_req for b in tray):
            return birds


def bonus_selection(bonus_cards: List[str]) -> str:
    return min(bonus_cards, key=lambda c: cards.Deck().bonus_importance.index(c))
