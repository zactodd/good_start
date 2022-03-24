from card_selection import *
from gui_interactions import *
from read_cards import *
import matplotlib.pyplot as plt
from collections import Counter
import atexit


selected_games = []

@atexit.register
def on_kill():
    print("Post run statistics")
    bird_games = Counter()
    bonus_games = Counter()
    for i, (birds, selected_birds, food, bonuses, bonus, bird_image, bonus_image) \
            in enumerate(reversed(selected_games)):
        print(f'Game:\n'
              f'\tbirds:\t {list(birds)}\t -> \t{list(selected_birds)}\n'
              f'\tfood:\t {food}\n'
              f'\tbonuses:\t {bonuses}\t -> {bonus}')

        bird_games[tuple(selected_birds)] += 1
        bonus_games[bonus] += 1

        birds_image_name = "__".join(b.replace("'", "").replace(" ", "_") for b in selected_birds)
        plt.imsave(f'..\\.selected\\game_{i}_birds__{birds_image_name}.png', bird_image)
        plt.imsave(f'..\\.selected\\game_{i}_bonus_{bonus}.png', bonus_image)
    x, y = zip(*bird_games.items())
    x = '-'.join(b[:2] for b in x)
    plt.bar(x, y, align='center')
    plt.xticks(range(len(bird_games)), bird_games.keys())
    plt.xlabel('Birds')
    plt.ylabel('Games')
    plt.title('Birds')
    plt.show()

    x, y = zip(*bonus_games.items())
    x = '-'.join(b[:2] for b in x)
    plt.bar(x, y, align='center')
    plt.xticks(range(len(bonus_games)), bonus_games.keys())
    plt.xlabel('Bonuses')
    plt.ylabel('Games')
    plt.title('Bonuses')
    plt.show()



if __name__ == '__main__':
    time.sleep(3)
    print('Starting...')
    menu_from_start()
    while True:
        time.sleep(6)
        move_and_click(*key_positions.TURN_START_BUTTON)
        time.sleep(2)

        birds, centres, bird_image = extract_bird_cards()
        bird_centres = dict(zip(birds, centres))

        selection = bird_selection(birds)
        if selection:
            selected_birds, food = selection
            for b in selected_birds:
                move_and_click(*bird_centres[b])
                time.sleep(0.5)
            for f in food:
                move_and_click(*key_positions.RESOURCES_TO_BUTTONS[f])
                time.sleep(0.5)
            move_and_click(*key_positions.NEXT_BUTTON)
            time.sleep(1)

            bonuses, centres, bonus_image = extract_bonus_cards()
            bonus_centres = dict(zip(bonuses, centres))
            bonus = bonus_selection(bonuses)

            selected_games.append((birds, selected_birds, food, bonuses, bonus, bird_image, bonus_image))

            move_and_click(*bonus_centres[bonus])
            time.sleep(0.5)
            move_and_click(*key_positions.NEXT_BUTTON)
            time.sleep(30)
        new_game_from_game()
