import os.path as osp
import json
from typing import List, Tuple, Dict
import utils
from patterns import Singleton



_BIRD_NAMES = osp.join(utils.RESOURCES, 'bird_names')
with open(osp.join(_BIRD_NAMES, 'base.txt'), 'r') as f:
    _BASE_BIRDS = f.read().splitlines()
with open(osp.join(_BIRD_NAMES, 'ss.txt'), 'r') as f:
    _SS_BIRDS = f.read().splitlines()
with open(osp.join(_BIRD_NAMES, 'ee.txt'), 'r') as f:
    _EE_BIRDS = f.read().splitlines()

_BIRD_IMPORTANCE = osp.join(utils.RESOURCES, 'bird_importance')
with open(osp.join(_BIRD_IMPORTANCE, 'base.json'), 'r') as f:
    _BASE_BIRD_IMPORTANCE = json.load(f)
with open(osp.join(_BIRD_IMPORTANCE, 'base_with_ss.json'), 'r') as f:
    _BASE_WITH_SS_BIRD_IMPORTANCE = json.load(f)
with open(osp.join(_BIRD_IMPORTANCE, 'base_with_ss_ee.json'), 'r') as f:
    _BASE_WITH_SS_EE_BIRD_IMPORTANCE = json.load(f)


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


class Deck(metaclass=Singleton):

    def __init__(self, sub_decks : List[str] = ['base'] ) -> None:
        self.birds = []
        self.bonus_cards = []
        for d in sub_decks:
            self.birds.extend(_BIRD_DECKS[d])
            self.bonus_cards.extend(_BONUS_CARD_DECKS[d])

        decks = frozenset(sub_decks)
        self.bird_importance = _BIRD_IMPORTANCE_DECKS[decks]
        self.bonus_importance = _BONUS_CARD_IMPORTANCE_DECKS[decks]
