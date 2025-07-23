import os.path as osp
import json
import csv
import utils

_FACTS = osp.join(utils.RESOURCES, 'facts')
HABITATS = ['Forest', 'Grassland', 'Wetland']
FOOD = ['Fruit', 'Fish', 'Invertebrate', 'Rodent', 'Seed']
COLOURS = {
    "brown": (155 / 255, 132 / 255, 89 / 255),
    "pink": (223 / 255, 49 / 255, 105 / 255),
    "gold": (247 / 255, 214 / 255, 57 / 255),
    "white": (180 / 255, 180 / 255, 180 / 255),
    "teal": (27 / 255, 187 / 255, 173 / 255)
}


with (open(osp.join(_FACTS, 'birds_info.json'), 'r') as f):
    BIRDS_DATA = json.load(f)

    BIRDS_HABITS = {
        bird['common_name']: bird['habitat'] for bird in BIRDS_DATA
    }

    BIRDS_NEST = {
        bird['common_name']: {'type': bird['nest_type'], 'count': bird['egg_limit']} for bird in BIRDS_DATA
    }

    BIRDS_COLOUR = {
        bird['common_name']: bird['color'] for bird in BIRDS_DATA
    }


_BIRDS_UNRESTRICTED = {'Common Myna', 'Superb Lyrebird', 'Tui'}
FOREST_POSSIBLE = _BIRDS_UNRESTRICTED | {b for b, h in BIRDS_HABITS.items() if 'Forest' in h}
GRASSLAND_POSSIBLE = _BIRDS_UNRESTRICTED | {b for b, h in BIRDS_HABITS.items() if 'Grassland' in h}
WETLANDS_POSSIBLE = _BIRDS_UNRESTRICTED | {b for b, h in BIRDS_HABITS.items() if 'Wetland' in h}
SIDEWAYS_BIRDS = {'European Roller', 'Grey Heron', 'Long-Tailed Tit', 'Common Blackbird'}


with (open(osp.join(_FACTS, 'bird_tags.tsv'), 'r') as f):
    BIRD_TAGS = {r[0]: r[1] for r in csv.reader(f, delimiter='\t')}
    TAG_COLOUR = {v: BIRDS_COLOUR[k] for k, v in BIRD_TAGS.items()}
