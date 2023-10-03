# import csv
#
#
# CARD_LIST_FILE  = 'card_list.tsv'
# SIMPLE_CARD_LIST = 'simple_card_list.tsv'
# HEADERS = ['name', 'points', 'food', 'food_all', 'habitats', 'nest', 'eggs', 'tags', 'bonus cards', 'color']
#
# TAG_HEADERS = ['Predator', 'Flocking', 'Bonus card']
#
# BONUS_CARD_HEADERS = []
# FOOD_HEADERS = ['Invertebrate', 'Seed', 'Fish', 'Fruit', 'Rodent', 'Nectar', 'Wild (food)']
# FOOD_WRITE = ['Invertebrate', 'Seed', 'Fish', 'Fruit', 'Rodent', 'Nectar', 'Any']
#
# HABITATS = ['Forest', 'Grassland', 'Wetland']
#
#
# with open(CARD_LIST_FILE, encoding="utf8") as rf:
#     lines = csv.DictReader(rf, delimiter='\t')
#
#
#
# with open(SIMPLE_CARD_LIST, 'w') as wf:
#     writer = csv.DictWriter(wf, fieldnames=HEADERS, delimiter='\t')
#
#     for l in lines:
#         writer.writerow({
#             'name': l['Common name'],
#             'points': l['Victory points'],
#             'color': l['Color'],
#             'nest': l['Nest type'],
#             'eggs': l['Egg capacity'],
#
#             'food': ('/' if l['/ (food cost)'] == 'X' else '+').join(
#                 v for h, w in zip(FOOD_HEADERS, FOOD_WRITE) for v in [w] * int('0' + l[h])
#             )
#
#             ''
#         })
#
#

