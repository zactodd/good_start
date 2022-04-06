import random
from matplotlib import pyplot as plt
from collections import Counter
from utils import BIRD_IMPORTANCE, BIRD_NAMES, BIRD_GROUPS


def good_game_selection(sample=1000):
    good_games = Counter()
    for hand in map(lambda _: random.sample(BIRD_NAMES, 5), range(sample)):
        for bird in BIRD_IMPORTANCE:
            required_birds = bird['birds']
            if all(b in hand for b in required_birds):
                name = '_'.join(''.join(w[0] for w in BIRD_GROUPS[b].split()) for b in required_birds)
                good_games[name] += 1
    good_games = {k: v / sample for k, v in good_games.items()}
    plt.bar(good_games.keys(), good_games.values())
    plt.xticks(rotation = 45)
    plt.show()


def good_game_selection_with_tray(sample=1000):
    good_games = Counter()
    for cards in map(lambda _: random.sample(BIRD_NAMES, 8), range(sample)):
        hand = cards[:5]
        tray = cards[5:]
        for bird in BIRD_IMPORTANCE:
            required_birds = bird['birds']
            if all(b in hand for b in required_birds) and any(b in tray for b in bird['tray']):
                name = '_'.join(''.join(w[0] for w in BIRD_GROUPS[b].split()) for b in required_birds)
                good_games[name] += 1
    good_games = {k: v / sample for k, v in good_games.items()}
    plt.bar(good_games.keys(), good_games.values())
    plt.xticks(rotation=45)
    plt.show()


def good_game_selection_with_double_tray(sample=1000):
    good_games = Counter()
    for cards in map(lambda _: random.sample(BIRD_NAMES, 8), range(sample)):
        hand = cards[:5]
        tray = cards[5:]
        for bird in BIRD_IMPORTANCE:
            required_birds = bird['birds']
            if all(b in hand for b in required_birds) and len({BIRD_GROUPS[b ]for b in bird['tray'] if b in tray}) > 1:
                name = '_'.join(''.join(w[0] for w in BIRD_GROUPS[b].split()) for b in required_birds)
                good_games[name] += 1
    good_games = {k: v / sample for k, v in good_games.items()}
    plt.bar(good_games.keys(), good_games.values())
    plt.xticks(rotation=45)
    plt.show()


n = 1000000
good_game_selection(n)
good_game_selection_with_tray(n)
good_game_selection_with_double_tray(n)

