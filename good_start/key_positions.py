
# Menu buttons
PLAY_BUTTON = (0.292, 0.480)
CUSTOM_GAME_BUTTON = (0.269, 0.778)
ORDER_BUTTON = (0.840, 0.600)

# Expansion selection
EXPANSION_BUTTON = (0.840, 0.767)
SWIFT_STARTER_PACK = (0.350, 0.550)
SELECT_EXPANSIONS = (0.500, 0.885)


# In Game buttons
NEXT_BUTTON = (0.935, 0.906)
TURN_START_BUTTON = (0.497, 0.678)

# Resource Buttons
RESOURCES_TO_BUTTONS = {
    'fruit': (0.556, 0.883),
    'fish': (0.624, 0.883),
    'invertebrate': (0.692, 0.883),
    'rodent': (0.780, 0.883),
    'seed': (0.848, 0.883),
}


# In game Buttons
SETTING_BUTTONS = (0.038, 0.094)
RETURN_TO_MAIN_MENU_BUTTON = (0.495, 0.588)
OVERVIEW_BUTTON = (0.062, 0.798)
RECENT_GAME_DELETE_BUTTON = (0.175, 0.164)
DELETE_GAME_BUTTON = (0.438, 0.564)


# Menus order
FIRST_MENU_TRAVERSAL = (PLAY_BUTTON, CUSTOM_GAME_BUTTON, ORDER_BUTTON, NEXT_BUTTON)
MENU_TRAVERSAL = (PLAY_BUTTON, CUSTOM_GAME_BUTTON, NEXT_BUTTON)
EXIT_GAME = (SETTING_BUTTONS, RETURN_TO_MAIN_MENU_BUTTON)
DELETE_GAME_TRAVERSAL = (RECENT_GAME_DELETE_BUTTON, DELETE_GAME_BUTTON)


BIRD_CARD_POSITIONS = [
    (0.165, 0.266),
    (0.314, 0.266),
    (0.458, 0.266),
    (0.600, 0.266),
    (0.746, 0.266)
]

TRAY_CARD_POSITIONS = [
    (0.547, 0.743),
    (0.656, 0.743),
    (0.764, 0.743)
]


PLAYER_BOARDS_POSITIONS = [
    (0.390, 0.08),
    (0.428, 0.08),
    (0.500, 0.08),
    (0.572, 0.08),
    (0.610, 0.08),
]


BIRDS_IN_HABITAT_NAMES_BBOXS = [
    (0.120, 0.170, 0.880, 0.210),
    (0.120, 0.345, 0.880, 0.385),
    (0.120, 0.525, 0.880, 0.565),
]


HIGHLIGHTED_CARD_BBOX = (0, 0.305, 1, 0.375)