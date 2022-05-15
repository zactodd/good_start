import time
import traceback
import sys
import logging
import card_selection as cs
import cards
import gui_interactions as gi
import key_positions as kp
import matplotlib.pyplot as plt
import utils
from collections import Counter
import atexit
from datetime import datetime
import subprocess


WINGSPAN_PATH = 'C:\\Users\\thoma\\Desktop\\Wingspan.url'

cards.Deck(['base', 'ss', 'ee'])


selected_games = []
root_logger = logging.getLogger()
root_logger.setLevel(logging.DEBUG)

@atexit.register
def _on_kill() -> None:
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
    average_time = 0
    checks = 0
    successes = 0
    if gi.window_exists():
        gi.kill_window()
    start = time.perf_counter()
    while True:
        if time.perf_counter() - start > 7200:
            logging.info(f'Average run time: {average_time:.2f}s')
            logging.info(f'Success rate: {successes / checks:.8f}%')
            gi.kill_window()
            time.sleep(3)
            start = time.perf_counter()
        if not gi.is_responding():
            gi.kill_window()
            time.sleep(10)
            subprocess.call(['start', WINGSPAN_PATH], shell=True)
            time.sleep(20)
            gi.activate_window()
            gi.menu_from_start()
        run_time = time.perf_counter()
        time.sleep(1)
        try:
            # Read tray before hand loads
            gi.move_and_click(*kp.OVERVIEW_BUTTON)
            time.sleep(2)
            tray = gi.extract_tray_cards()
            if any(b in cards.Deck().possible_tray_birds for b in tray):
                time.sleep(3)
                # Start Turn
                gi.move_and_click(*kp.TURN_START_BUTTON)
                time.sleep(1)

                # Read bird cards
                birds, centres, bird_image = gi.extract_bird_cards()
                bird_centres = dict(zip(birds, centres))

                # Select birds, food and bonus cards if valid birds in hand
                if selection := cs.bird_selection(birds, tray):
                    selected_birds, food = selection
                    logging.info(f'Selected birds: {selected_birds}')

                    # Select birds
                    time.sleep(0.5)
                    gi.select_starting_cards(selected_birds, bird_centres, food)
                    if gi.post_starting_selection_validation(selected_birds, tray):
                        successes += 1
            else:
                average_time = (average_time * checks + (time.perf_counter() - run_time)) / (checks + 1)
                checks += 1
                gi.new_game_from_game()
        except (SystemError, ValueError) as e:
            traceback.print_exception(*sys.exc_info())
            root_logger.error(e)
            gi.kill_window()
            time.sleep(3)

