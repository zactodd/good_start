import utils


def bird_selection(cards):
    for items in utils.BIRD_IMPORTANCE:
        birds, food, *tray = items.values()
        if all(b in cards for b in birds):
            if len(birds) + len(food) == 5:
                return birds, food, tray
            else:
                return birds + [next(c for c in cards if c not in birds)], food, tray


def bonus_selection(cards):
    return min(cards, key=lambda c: utils.BONUS_IMPORTANCE.index(c))


def valid_tray(tray, tray_subsets):
    return all(any(b in tray for b in s) for s in tray_subsets)


