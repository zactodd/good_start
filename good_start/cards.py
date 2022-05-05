import os.path as osp
from typing import List
import utils



_BIRD_NAMES = osp.join(utils.RESOURCES, 'bird_names')
with open(osp.join(_BIRD_NAMES, 'base.txt'), 'r') as f:
    _BASE = f.read().splitlines()

with open(osp.join(_BIRD_NAMES, 'ss.txt'), 'r') as f:
    _SS = f.read().splitlines()

with open(osp.join(_BIRD_NAMES, 'ee.txt'), 'r') as f:
    _EE = f.read().splitlines()


ALL_BIRDS_DECK = _BASE + _SS + _EE
BASE_DECK = _BASE
_DECKS = {
    'base': _BASE,
    'ss': _SS,
    'ee': _EE,
}


def build_deck(sub_decks: List[str]) -> List[str]:
    deck = []
    for d in sub_decks:
        deck.extend(_DECKS[d])
    return deck


