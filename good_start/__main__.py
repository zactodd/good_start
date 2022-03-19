from card_selection import *
from gui_interactions import *
from read_cards import *



if __name__ == '__main__':
    time.sleep(3)
    print('Starting...')
    menu_from_start()
    while True:
        time.sleep(6)
        move_and_click(*key_positions.TURN_START_BUTTON)
        time.sleep(2)

        birds, centres = extract_bird_cards()
        bird_centres = dict(zip(birds, centres))

        selection = bird_selection(birds)
        if selection:
            birds, food = selection
            print('Selected birds:', birds)
            print('Selected food:', food)
            for b in birds:
                move_and_click(*bird_centres[b])
                time.sleep(0.5)
            for f in food:
                move_and_click(*key_positions.RESOURCES_TO_BUTTONS[f])
                time.sleep(0.5)
            move_and_click(*key_positions.NEXT_BUTTON)
            time.sleep(1)

            bonuses, centres = extract_bonus_cards()
            bonus_centres = dict(zip(bonuses, centres))
            bonus = bonus_selection(bonuses)
            print('Selected bonus:', bonus)
            print()

            move_and_click(*bonus_centres[bonus])
            time.sleep(0.5)
            move_and_click(*key_positions.NEXT_BUTTON)
            time.sleep(30)
        new_game_from_game()





