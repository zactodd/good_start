import os.path as osp
from typing import List, Tuple
import utils



_BIRD_NAMES = osp.join(utils.RESOURCES, 'bird_names')
with open(osp.join(_BIRD_NAMES, 'base.txt'), 'r') as f:
    _BASE_BIRDS = f.read().splitlines()
with open(osp.join(_BIRD_NAMES, 'ss.txt'), 'r') as f:
    _SS_BIRDS = f.read().splitlines()
with open(osp.join(_BIRD_NAMES, 'ee.txt'), 'r') as f:
    _EE_BIRDS = f.read().splitlines()

_BIRD_IMPORTANCE = osp.join(utils.RESOURCES, 'bird_importance')
with open(osp.join(_BIRD_IMPORTANCE, 'base.txt'), 'r') as f:
    _BASE_BIRD_IMPORTANCE = f.read().splitlines()
with open(osp.join(_BIRD_IMPORTANCE, 'base_with_ss.txt'), 'r') as f:
    _BASE_WITH_SS_BIRD_IMPORTANCE = f.read().splitlines()
with open(osp.join(_BIRD_IMPORTANCE, 'base_with_ss_ee.txt'), 'r') as f:
    _BASE_WITH_SS_EE_BIRD_IMPORTANCE = f.read().splitlines()


_BONUS_CARDS = osp.join(utils.RESOURCES, 'bonus_cards')
with open(osp.join(_BONUS_CARDS, 'base.txt'), 'r') as f:
    _BASE_BONUS_CARDS = f.read().splitlines()
with open(osp.join(_BONUS_CARDS, 'ee.txt'), 'r') as f:
    _EE_BONUS_CARDS = f.read().splitlines()

_BONUS_CARD_IMPORTANCE = osp.join(utils.RESOURCES, 'importance_bonus_cards')
with open(osp.join(_BONUS_CARD_IMPORTANCE, 'base.txt'), 'r') as f:
    _BASE_BONUS_CARD_IMPORTANCE = f.read().splitlines()
with open(osp.join(_BONUS_CARD_IMPORTANCE, 'base_with_ee.txt'), 'r') as f:
    _BASE_WITH_EE_BONUS_CARD_IMPORTANCE = f.read().splitlines()



ALL_BIRDS_DECK = _BASE_BIRDS + _SS_BIRDS + _EE_BIRDS
BASE_DECK = _BASE_BIRDS
_BIRD_DECKS = {
    'base': _BASE_BIRDS,
    'ss': _SS_BIRDS,
    'ee': _EE_BIRDS,
}

_BIRD_IMPORTANCE_DECKS = {
    frozenset({'base'}): _BASE_BIRD_IMPORTANCE,
    frozenset({'base', 'ss'}): _BASE_WITH_SS_BIRD_IMPORTANCE,
    frozenset({'base', 'ee'}): _BASE_WITH_SS_EE_BIRD_IMPORTANCE,
    frozenset({'base', 'ss', 'ee'}): _BASE_WITH_SS_EE_BIRD_IMPORTANCE,

}

_BONUS_CARD_DECKS = {
    'base': _BASE_BONUS_CARDS,
    'ss': [],
    'ee': _EE_BONUS_CARDS
}

_BONUS_CARD_IMPORTANCE_DECKS = {
    frozenset({'base'}): _BASE_BIRDS,
    frozenset({'base', 'ss'}): _BASE_BIRDS,
    frozenset({'base', 'ee'}): _BASE_WITH_EE_BONUS_CARD_IMPORTANCE,
    frozenset({'base', 'ss', 'ee'}): _BASE_WITH_EE_BONUS_CARD_IMPORTANCE,
}


def build_deck(sub_decks: List[str]) -> Tuple[List[str], List[str], List[str]]:
    birds = []
    bonus_cards = []
    for d in sub_decks:
        birds.extend(_BIRD_DECKS[d])
        bonus_cards.extend(_BONUS_CARD_DECKS[d])
    return birds, bonus_cards, _BONUS_CARD_IMPORTANCE_DECKS[frozenset(sub_decks)]


