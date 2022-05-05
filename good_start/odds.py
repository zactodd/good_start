from matplotlib import pyplot as plt
from collections import Counter
from typing import List
from card_selection import *
from utils import BIRD_GROUPS



def good_game_selection_with_tray(bird_deck: List[str], bird_importance, sample:int = 1000) -> None:
    good_games = Counter()
    for cards in map(lambda _: random.sample(bird_deck, 8), range(sample)):
        hand, tray = cards[:5], cards[5:]
        if selection := bird_selection(bird_importance, hand, tray):
            birds, _ = selection
            name = '_'.join(''.join(w[0] for w in BIRD_GROUPS[b].split()) for b in birds if b in BIRD_GROUPS)
            good_games[name] += 1
    good_games = {k: v / sample for k, v in good_games.items()}
    print(sum(good_games.values()))
    plt.bar(good_games.keys(), good_games.values())
    plt.xticks(rotation=45)
    plt.show()


def good_game_selection_with_tray_and_hummingbird(bird_deck: List[str], bird_importance, sample:int = 1000) -> None:
    good_games = Counter()
    for cards in map(lambda _: random.sample(bird_deck, 28), range(sample)):
        hand, tray, other = cards[:5], cards[5:8], cards[8:]
        if (selection := bird_selection(bird_importance, hand, tray)) and \
                        any(b in utils.BIRD_GROUPS and 'Hummingbird' in utils.BIRD_GROUPS[b] for b in other):
            birds, _ = selection
            name = '_'.join(''.join(w[0] for w in BIRD_GROUPS[b].split()) for b in birds if b in BIRD_GROUPS)
            good_games[name] += 1
    good_games = {k: v / sample for k, v in good_games.items()}
    print(sum(good_games.values()))
    plt.bar(good_games.keys(), good_games.values())
    plt.xticks(rotation=45)
    plt.show()


# from cards import ALL_DECK, build_deck
# n = 100000
# birds, _, bird_importance, *_ = ALL_DECK
# good_game_selection_with_tray(birds, bird_importance, n)
# good_game_selection_with_tray_and_hummingbird(birds, bird_importance, n)
#
# birds, _, bird_importance, *_ = build_deck(['base'])
# good_game_selection_with_tray(birds, bird_importance, n)
# good_game_selection_with_tray_and_hummingbird(birds, bird_importance, n)
