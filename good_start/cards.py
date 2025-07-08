import os.path as osp
import json
from typing import Tuple
import utils
from patterns import Singleton


_BIRD_NAMES = osp.join(utils.RESOURCES, 'bird_names')
with open(osp.join(_BIRD_NAMES, 'base.txt'), 'r') as f:
    _BASE_BIRDS = f.read().splitlines()
with open(osp.join(_BIRD_NAMES, 'ss.txt'), 'r') as f:
    _SS_BIRDS = f.read().splitlines()
with open(osp.join(_BIRD_NAMES, 'ee.txt'), 'r') as f:
    _EE_BIRDS = f.read().splitlines()
with open(osp.join(_BIRD_NAMES, 'oe.txt'), 'r', encoding='utf8') as f:
    _OE_BIRDS = f.read().splitlines()
with open(osp.join(_BIRD_NAMES, 'ae.txt'), 'r', encoding='utf8') as f:
    _AE_BIRDS = f.read().splitlines()


_BIRD_IMPORTANCE = osp.join(utils.RESOURCES, 'bird_importance')
with open(osp.join(_BIRD_IMPORTANCE, 'base.json'), 'r') as f:
    _BASE_BIRD_IMPORTANCE = json.load(f)
with open(osp.join(_BIRD_IMPORTANCE, 'base_with_ss.json'), 'r') as f:
    _BASE_WITH_SS_BIRD_IMPORTANCE = json.load(f)
with open(osp.join(_BIRD_IMPORTANCE, 'base_with_ee.json'), 'r') as f:
    _BASE_WITH_EE_BIRD_IMPORTANCE = json.load(f)
with open(osp.join(_BIRD_IMPORTANCE, 'base_with_oe.json'), 'r') as f:
    _BASE_WITH_OE_BIRD_IMPORTANCE = json.load(f)
with open(osp.join(_BIRD_IMPORTANCE, 'base_with_ss_ee.json'), 'r') as f:
    _BASE_WITH_SS_EE_BIRD_IMPORTANCE = json.load(f)
with open(osp.join(_BIRD_IMPORTANCE, 'base_with_ss_oe.json'), 'r') as f:
    _BASE_WITH_SS_OE_BIRD_IMPORTANCE = json.load(f)


BASE_DECK = _BASE_BIRDS
_BIRD_DECKS = {
    'base': _BASE_BIRDS,
    'ss': _SS_BIRDS,
    'ee': _EE_BIRDS,
    'oe': _OE_BIRDS,
    'ae': _AE_BIRDS
}

_BIRD_IMPORTANCE_DECKS = {
    frozenset({'base'}): _BASE_BIRD_IMPORTANCE,
    frozenset({'base', 'ss'}): _BASE_WITH_SS_BIRD_IMPORTANCE,
    frozenset({'base', 'ee'}): _BASE_WITH_EE_BIRD_IMPORTANCE,
    frozenset({'base', 'ss', 'ee'}): _BASE_WITH_SS_EE_BIRD_IMPORTANCE,
    frozenset({'base', 'oe'}): _BASE_WITH_OE_BIRD_IMPORTANCE,
    frozenset({'base', 'ss', 'oe'}): _BASE_WITH_SS_OE_BIRD_IMPORTANCE,

    # TODO Set deck importance for with AE
    frozenset({'base', 'ee', 'oe'}): _BASE_WITH_OE_BIRD_IMPORTANCE,
    frozenset({'base', 'ss', 'ee', 'oe'}): _BASE_WITH_SS_OE_BIRD_IMPORTANCE,
    frozenset({'base', 'ss', 'ee', 'oe', 'ae'}): _BASE_WITH_SS_OE_BIRD_IMPORTANCE,
    frozenset({'ee', 'oe'}): _BASE_WITH_SS_OE_BIRD_IMPORTANCE,


    frozenset({'ss', 'ee', 'oe'}): _BASE_WITH_SS_OE_BIRD_IMPORTANCE
}


class Deck(metaclass=Singleton):

    def __init__(self, *args, **kwargs) -> None:
        self.set_deck(*args, **kwargs)

    def set_deck(self, sub_decks : Tuple[str] = ('base', )) -> None:
        self.birds = []
        self.bonus_cards = []
        for d in sub_decks:
            self.birds.extend(_BIRD_DECKS[d])

        decks = frozenset(sub_decks)
        self.bird_importance = _BIRD_IMPORTANCE_DECKS[decks]
        self.possible_tray_birds = {b for items in self.bird_importance for b in items['tray']}

