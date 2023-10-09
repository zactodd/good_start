from matplotlib import pyplot as plt
import random
from collections import Counter
import cards
import selection
# from utils import BIRD_GROUPS



def good_game_selection_with_tray(sample:int = 1000) -> None:
    good_games = Counter()
    for c in map(lambda _: random.sample(cards.Deck().birds, 8), range(sample)):
        hand, tray = c[:5], c[5:]
        if selected := selection.bird_selection(hand, tray):
            birds, _ = selected
            # name = '_'.join(''.join(w[0] for w in BIRD_GROUPS[b].split()) for b in birds if b in BIRD_GROUPS)
            good_games[True] += 1
    good_games = {k: v / sample for k, v in good_games.items()}
    print(sum(good_games.values()))
    plt.bar(good_games.keys(), good_games.values())
    plt.xticks(rotation=45)
    plt.show()


def good_game_selection_with_tray_and_hummingbird(sample:int = 1000) -> None:
    good_games = Counter()
    for c in map(lambda _: random.sample(cards.Deck().birds, 28), range(sample)):
        hand, tray, other = c[:5], c[5:8], c[8:]
        if (selected := selection.bird_selection(hand, tray)) and \
                        any(b in BIRD_GROUPS and 'Hummingbird' in BIRD_GROUPS[b] for b in other):
            birds, _ = selected
            name = '_'.join(''.join(w[0] for w in BIRD_GROUPS[b].split()) for b in birds if b in BIRD_GROUPS)
            good_games[name] += 1
    good_games = {k: v / sample for k, v in good_games.items()}
    print(sum(good_games.values()))
    plt.bar(good_games.keys(), good_games.values())
    plt.xticks(rotation=45)
    plt.show()


n = 10000
cards.Deck().set_deck(('base', ))
good_game_selection_with_tray(n)
n = 10000
cards.Deck().set_deck(('base', 'oe'))
good_game_selection_with_tray(n)
# good_game_selection_with_tray_and_hummingbird(n)
