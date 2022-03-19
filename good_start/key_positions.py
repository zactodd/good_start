
# Menu buttons
PLAY_BUTTON = (0.292, 0.480)
CUSTOM_GAME_BUTTON = (0.269, 0.778)
ORDER_BUTTON = (0.790, 0.767)

# In Game buttons
NEXT_BUTTON = (0.935, 0.906)
TURN_START_BUTTON = (0.497, 0.678)

# Resource Buttons
FRUIT_BUTTON = (0.625, 0.883)
FISH_BUTTON = (0.682, 0.883)
INVERTEBRATE_BUTTON = (0.760, 0.883)
RODENT_BUTTON = (0.818, 0.883)
SEED_BUTTON = (0.876, 0.883)


# In game Buttons
SETTING_BUTTONS = (0.038, 0.094)
RETURN_TO_MAIN_MENU_BUTTON = (0.495, 0.588)


# Menus order
FIRST_MENU_TRAVERSAL = (PLAY_BUTTON, CUSTOM_GAME_BUTTON, ORDER_BUTTON, NEXT_BUTTON)
MENU_TRAVERSAL = (PLAY_BUTTON, CUSTOM_GAME_BUTTON, NEXT_BUTTON)
NEW_GAME_FROM_GAME = (SETTING_BUTTONS, RETURN_TO_MAIN_MENU_BUTTON, *MENU_TRAVERSAL)
