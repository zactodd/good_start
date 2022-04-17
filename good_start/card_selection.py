import utils


def bird_selection(hand, tray):
    for items in utils.BIRD_IMPORTANCE:
        birds, food, tray_req = items.values()
        if all(b in hand for b in birds) and any(b in tray_req for b in tray):
            if len(birds) + len(food) == 5:
                return birds, food
            else:
                return birds + [next(c for c in hand if c not in birds)], food


def bonus_selection(cards):
    return min(cards, key=lambda c: utils.BONUS_IMPORTANCE.index(c))
