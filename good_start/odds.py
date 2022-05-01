from matplotlib import pyplot as plt
from collections import Counter
from card_selection import *
from utils import BIRD_NAMES, BIRD_GROUPS


def good_game_selection_with_tray(sample:int = 1000):
    good_games = Counter()
    for cards in map(lambda _: random.sample(BIRD_NAMES, 8), range(sample)):
        hand, tray = cards[:5], cards[5:]
        if selection := bird_selection(hand, tray):
            birds, _ = selection
            name = '_'.join(''.join(w[0] for w in BIRD_GROUPS[b].split()) for b in birds if b in BIRD_GROUPS)
            good_games[name] += 1
    good_games = {k: v / sample for k, v in good_games.items()}
    plt.bar(good_games.keys(), good_games.values())
    plt.xticks(rotation=45)
    plt.show()


def good_game_selection_with_tray_and_hummingbird(sample:int =1000):
    good_games = Counter()
    for cards in map(lambda _: random.sample(BIRD_NAMES, 28), range(sample)):
        hand, tray, other = cards[:5], cards[5:8], cards[8:]
        if (selection := bird_selection(hand, tray)) and \
                        any(b in utils.BIRD_GROUPS and 'Hummingbird' in utils.BIRD_GROUPS[b] for b in other):
            birds, _ = selection
            name = '_'.join(''.join(w[0] for w in BIRD_GROUPS[b].split()) for b in birds if b in BIRD_GROUPS)
            good_games[name] += 1
    good_games = {k: v / sample for k, v in good_games.items()}
    plt.bar(good_games.keys(), good_games.values())
    plt.xticks(rotation=45)
    plt.show()
