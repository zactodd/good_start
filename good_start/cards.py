import os.path as osp
from typing import List
import utils



_BIRD_NAMES = osp.join(utils.RESOURCES, 'bird_names')
with open(osp.join(_BIRD_NAMES, 'base.txt'), 'r') as f:
    _BASE_BIRDS = f.read().splitlines()

with open(osp.join(_BIRD_NAMES, 'ss.txt'), 'r') as f:
    _SS_BIRDS = f.read().splitlines()

with open(osp.join(_BIRD_NAMES, 'ee.txt'), 'r') as f:
    _EE_BIRDS = f.read().splitlines()


ALL_BIRDS_DECK = _BASE_BIRDS + _SS_BIRDS + _EE_BIRDS
BASE_DECK = _BASE_BIRDS
_DECKS = {
    'base': _BASE_BIRDS,
    'ss': _SS_BIRDS,
    'ee': _EE_BIRDS,
}


def build_deck(sub_decks: List[str]) -> List[str]:
    deck = []
    for d in sub_decks:
        deck.extend(_DECKS[d])
    return deck


