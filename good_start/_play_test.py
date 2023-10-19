import time
import traceback
import sys
import logging
import selection
import cards
import gui_interactions as gi
import key_positions as kp
import subprocess


WINGSPAN_PATH = 'steam://rungameid/2466010'

cards.Deck().set_deck(('base', 'oe'))

root_logger = logging.getLogger()
root_logger.setLevel(logging.DEBUG)


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
            time.sleep(10)
            gi.start_without_sync()
            time.sleep(10)
            gi.activate_window()
            gi.menu_from_start(True)
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

                # Select birds
                if selected_birds := selection.bird_selection(birds, tray):
                    logging.info(f'Selected birds: {selected_birds}')
                    logging.info(f'\tTray: {tray}')
                    successes += 1
                    gi.new_game_from_game()
                else:
                    gi.new_game_from_game_with_delete()
            else:
                average_time = (average_time * checks + (time.perf_counter() - run_time)) / (checks + 1)
                checks += 1
                gi.new_game_from_game()
        except (SystemError, ValueError) as e:
            traceback.print_exception(*sys.exc_info())
            root_logger.error(e)
            gi.kill_window()
            time.sleep(3)

