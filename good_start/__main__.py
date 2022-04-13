from card_selection import *
from gui_interactions import *
from read_cards import *
import matplotlib.pyplot as plt
import utils
from collections import Counter
import atexit
from datetime import datetime


selected_games = []

@atexit.register
def on_kill():
    print("Post run statistics")
    bird_games = Counter()
    bonus_games = Counter()
    save_time = datetime.now()
    for i, (birds, selected_birds, food, bonuses, bonus, bird_image, bonus_image) \
            in enumerate(reversed(selected_games)):
        print(f'Game:\n'
              f'\tbirds:\t {list(birds)}\n\t\t->\t{list(selected_birds)}\n'
              f'\tfood:\t {food}\n'
              f'\tbonuses:\t {bonuses}\n\t\t->\t{bonus}')

        bird_games[tuple(selected_birds)] += 1
        bonus_games[bonus] += 1

        birds_image_name = "__".join(b.replace("'", "").replace(" ", "_").lower() for b in selected_birds)
        time_prefix = f'{utils.SELECTED_IMAGES}/game__{save_time:%y_%M_%d}__{i}'
        plt.imsave(f'{time_prefix}__birds__{birds_image_name}.png', bird_image)
        plt.imsave(f'{time_prefix}__bonus__{bonus}.png', bonus_image)



if __name__ == '__main__':
    time.sleep(3)
    print('Starting...')
    menu_from_start()
    while True:
        # Read tray
        move_and_click(*key_positions.OVERVIEW_BUTTON)
        time.sleep(2)
        tray = extract_tray_cards()

        time.sleep(2)
        move_and_click(*key_positions.TURN_START_BUTTON)
        time.sleep(1)

        birds, centres, bird_image = extract_bird_cards()
        bird_centres = dict(zip(birds, centres))
        selection = bird_selection(birds)

        if selection:
            print(f'Selected birds: {selection}')
            selected_birds, food, tray_requirements = selection

            # Select cards and food if tray requirements are met
            if any(c in tray_requirements for c in tray):
                print('Tray requirements met')
                move_and_click(*key_positions.OVERVIEW_BUTTON)
                time.sleep(0.5)
                for b in selected_birds:
                    move_and_click(*bird_centres[b])
                    time.sleep(0.5)
                for f in food:
                    move_and_click(*key_positions.RESOURCES_TO_BUTTONS[f])
                    time.sleep(0.5)
                move_and_click(*key_positions.NEXT_BUTTON)
                time.sleep(1)

                # Select bonus cards
                bonuses, centres, bonus_image = extract_bonus_cards()
                bonus_centres = dict(zip(bonuses, centres))
                bonus = bonus_selection(bonuses)

                selected_games.append((birds, selected_birds, food, bonuses, bonus, bird_image, bonus_image))

                move_and_click(*bonus_centres[bonus])

                # Wait to save game
                time.sleep(0.5)
                move_and_click(*key_positions.NEXT_BUTTON)
                time.sleep(3)

        exit_game()
        time.sleep(3)
        new_game_from_game()
