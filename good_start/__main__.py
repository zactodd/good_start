from card_selection import *
from gui_interactions import *
from read_cards import *
import matplotlib.pyplot as plt
import utils
from collections import Counter
import atexit
from datetime import datetime
import subprocess


WINGSPAN_PATH = 'C:\\Users\\thoma\\Desktop\\Wingspan.url'


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


successes = 0

if __name__ == '__main__':
    while True:
        if not utils.check_if_process_running('Wingspan.exe'):
            time.sleep(10)
            subprocess.call(['start', WINGSPAN_PATH], shell=True)
            time.sleep(20)
            menu_from_start()
        time.sleep(1)

        try:
            # Read tray before hand loads
            move_and_click(*key_positions.OVERVIEW_BUTTON)
            time.sleep(2)
            tray = extract_tray_cards()
            time.sleep(3)

            # Start Turn
            move_and_click(*key_positions.TURN_START_BUTTON)
            time.sleep(1)

            # Read bird cards
            birds, centres, bird_image = extract_bird_cards()
            bird_centres = dict(zip(birds, centres))
            selection = bird_selection(birds, tray)

            # Select birds, food and bonus cards if valid birds in hand
            if selection:
                selected_birds, food = selection

                # Select birds
                time.sleep(0.5)
                for b in selected_birds:
                    move_and_click(*bird_centres[b])
                    time.sleep(0.5)

                # Select food
                for f in food:
                    move_and_click(*key_positions.RESOURCES_TO_BUTTONS[f])
                    time.sleep(0.5)
                move_and_click(*key_positions.NEXT_BUTTON)
                time.sleep(1)

                # Select bonus cards
                bonuses, centres, bonus_image = extract_bonus_cards()
                bonus_centres = dict(zip(bonuses, centres))
                bonus = bonus_selection(bonuses)
                move_and_click(*bonus_centres[bonus])
                time.sleep(0.5)

                # Save game
                selected_games.append((birds, selected_birds, food, bonuses, bonus, bird_image, bonus_image))
                move_and_click(*key_positions.NEXT_BUTTON)
                time.sleep(3)
                successes += 1
                print(f'{successes} Successes {datetime.now():%H:%M:%S}')

            # New Game
            exit_game()
            time.sleep(3)
            new_game_from_game()
        except SystemError as e:
            pass
