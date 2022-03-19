import utils


def bird_selection(cards):
    for items in utils.BIRD_IMPORTANCE:
        birds, food = items.values()
        if all(b in cards for b in birds):
            if len(birds) + len(food) == 5:
                return birds, food
            else:
                return birds + [next(c for c in cards if c not in birds)], food


def bonus_selection(cards):
    return min(cards, key=lambda c: utils.BONUS_IMPORTANCE.index(c))


