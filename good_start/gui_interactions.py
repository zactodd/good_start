import autoit
import key_positions as kp
import time
import ctypes
from typing import List, Tuple, Dict
import cv2
import pytesseract
import numpy as np
from PIL import ImageGrab
import matplotlib.pyplot as plt
import card_selection as cs
import subprocess
import utils
import cards


def _window_bbox_from_name(name: str)-> Tuple[int, int, int, int]:
    hwnd = ctypes.windll.user32.FindWindowW(0, name)
    rect = ctypes.wintypes.RECT()
    ctypes.windll.user32.GetWindowRect(hwnd, ctypes.pointer(rect))
    x0, y0, x1, y1 = rect.left, rect.top, rect.right, rect.bottom
    return x0, y0, x1, y1


def window_bbox() -> Tuple[int, int, int, int]:
    """
    Gets the bounding box of the game.
    :return: The bounding box of the game, x0, y0, x1, y1.
    """
    return _window_bbox_from_name('Wingspan')


def window_dimensions() -> Tuple[int, int]:
    """
    Gets the dimensions of the game window.
    :return: The dimensions of the game window, width, height.
    """
    x0, y0, x1, y1 = window_bbox()
    return x1 - x0, y1 - y0


def move_and_click(x: float, y: float) -> None:
    """
    Moves the mouse to the given coordinates and clicks.
    The x and y coords are scaled to the size of thw game window.
    :param x: The x coordinate.
    :param y: The y coordinate.
    :return:
    """
    w, h = window_dimensions()
    x0, y0, *_ = window_bbox()
    if x > 1:
        x, y = x / w, y / h
    autoit.mouse_click("left", round(x0 + x * w), round(y0 + y * h), 1, 1)


def move(x: float, y: float) -> None:
    """
    Moves the mouse to the given coordinates.
    The x and y coords are scaled to the size of thw game window.
    :param x: The x coordinate.
    :param y: The y coordinate.
    :return:
    """
    w, h = window_dimensions()
    x0, y0, *_ = window_bbox()
    if x > 1:
        x, y = x / w, y / h
    autoit.mouse_move(round(x0 + x * w), round(y0 + y * h), 1)


def _is_responding(name: str) -> bool:
    cmd = f'tasklist /FI "IMAGENAME eq {name}" /FI "STATUS eq running"'
    status = subprocess.Popen(cmd, stdout=subprocess.PIPE).stdout.read()
    return name in str(status)


def is_responding() -> bool:
    """
    Checks if the game is responding.
    :return: True if the game is responding, False otherwise.
    """
    return _is_responding('Wingspan.exe')


def activate_window() -> None:
    """
    Activates the game window.
    :return:
    """
    autoit.win_activate('Wingspan')


def kill_window() -> None:
    """
    Kills the game window, if it exists.
    :return:
    """
    if window_exists():
        autoit.win_kill('Wingspan')


def window_exists() -> bool:
    """
    Checks if the game window exists.
    :return:
    """
    return autoit.win_exists('Wingspan')


def click_buttons(buttons, wait=0.5) -> None:
    """
    Moves and clicks the mouse on the given buttons.
    :param buttons: A list of buttons to click.
    :param wait: The amount of time to wait between clicks.
    :return:
    """
    for button in buttons:
        move_and_click(*button)
        time.sleep(wait)


def menu_from_start() -> None:
    """
    Moves the mouse to the menu from the start screen.
    :return:
    """
    click_buttons(kp.FIRST_MENU_TRAVERSAL)


def new_game_from_game() -> None:
    """
    Moves from the current thought the menus to a new game.
    :return:
    """
    exit_game()
    time.sleep(3)
    click_buttons(kp.MENU_TRAVERSAL)


def new_game_from_game_with_delete() -> None:
    """
    Moves from the current thought the menus to a new game, while deleting the current game.
    :return:
    """
    time.sleep(3)
    move_and_click(*kp.PLAY_BUTTON)
    time.sleep(0.2)
    move(*kp.RECENT_GAME_DELETE_BUTTON)
    time.sleep(0.2)
    click_buttons((kp.RECENT_GAME_DELETE_BUTTON, kp.DELETE_GAME_BUTTON, kp.CUSTOM_GAME_BUTTON, kp.NEXT_BUTTON))


def exit_game() -> None:
    """
    Moves from the current thought the menus to the exit game.
    :return:
    """
    click_buttons(kp.EXIT_GAME, wait=1)


def select_and_play_bird(bird: str, attempts: int = 10) -> None:
    """
    Selects the given bird and plays it.
    :param bird: The bird to select.
    :param attempts: The number of attempts to select the bird.
    :return:
    """
    autoit.send('{UP}')
    for _ in range(attempts):
        time.sleep(1)
        if bird == extract_highlighted_card():
            autoit.send('{SPACE}')

            # TODO logic
            if bird == 'Killdeer':
                food = ['invertebrate']
            elif bird == 'Dark-Eyed Junco':
                food = ['seed', 'invertebrate']
            elif bird == 'Franklin\'s Gull':
                food = ['fish', 'invertebrate']
            else:
                return

            habitats = utils.BIRD_HABITATS[bird]
            idx = habitats.index('Grassland')

            if len(habitats) == 2:
                move_and_click(*kp.TWO_HABITAT_BUTTON_POSITIONS[idx])

            elif len(habitats) == 3:
                move_and_click(*kp.THREE_HABITAT_BUTTON_POSITIONS[idx])
            time.sleep(0.2)
            move_and_click(*kp.NEXT_BUTTON)
            time.sleep(0.2)
            move_and_click(*kp.CHANGE_FOOD_BUTTON)
            time.sleep(0.2)

            for f in food:
                move_and_click(*kp.FOOD_PAY_BUTTONS[f.lower()])
                time.sleep(0.2)

            move_and_click(*kp.NEXT_BUTTON)
            time.sleep(0.2)
            move_and_click(*kp.NEXT_BUTTON)
            break

        time.sleep(1)
        autoit.send('{LEFT}')
    else:
        raise ValueError('Could not find bird')


def select_starting_cards(birds: List[str], bird_locations: Dict[str, Tuple[int, int]], food: List[str]) -> None:
    """
    Selects the given birds, food and bonus cards.
    :param birds:
    :param bird_locations:
    :param food:
    :return:
    """
    for b in birds:
        move_and_click(*bird_locations[b])
        time.sleep(0.5)
    for f in food:
        move_and_click(*kp.RESOURCES_TO_BUTTONS[f.lower()])
        time.sleep(0.5)
    move_and_click(*kp.NEXT_BUTTON)
    time.sleep(1)

    bonuses, centres, bonus_image = extract_bonus_cards()
    bonus_centres = dict(zip(bonuses, centres))
    bonus = cs.bonus_selection(bonuses)
    move_and_click(*bonus_centres[bonus])
    time.sleep(0.5)
    move_and_click(*kp.NEXT_BUTTON)


def post_starting_selection_validation(birds, tray) -> bool:
    success = True
    if any(b in utils.BIRD_GROUPS and 'hummingbird' in utils.BIRD_GROUPS[b].lower() for b in tray):
        time.sleep(3)
    else:
        if utils.BIRD_GROUPS[birds[0]] == 'Draw':
            time.sleep(30)
            move_and_click(*kp.TURN_START_BUTTON)
            time.sleep(1)
            move_and_click(*kp.OVERVIEW_BUTTON)
            time.sleep(1)
            select_and_play_bird(birds[0], len(birds))
            time.sleep(30)
            move_and_click(*kp.TURN_START_BUTTON)
            time.sleep(0.5)

            for pos in kp.PLAYER_BOARDS_POSITIONS[1:]:
                move_and_click(*pos)
                time.sleep(3)
                if any(b in utils.BIRD_GROUPS and 'Hummingbird' in utils.BIRD_GROUPS[b]
                       for h in extract_player_board() for b in h):
                    break
            else:
                success = False
        if success:
            new_game_from_game()
        else:
            new_game_from_game_with_delete()
        return success


def find_contours(grey_image: np.ndarray) -> List[List[int]]:
    """
    Finds all the contours from a grey scale image.
    :param grey_image: A grey scale image.
    :return: a list of contours
    """
    _, thresh = cv2.threshold(grey_image, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    return contours

def contour_centre(contour: List[int]) -> Tuple[float, float]:
    """
    Calculates the centre of the contour.
    :param contour: The contour in which to obtain the centre.
    :return: x axis centre, y axis centre.
    """
    m = cv2.moments(contour)
    return m["m10"] / m["m00"], m["m01"] / m["m00"]

def filter_contours_by_area(contours: List[List[int]], upper: int, lower: int) -> List[List[int]]:
    """
    Filters a list of contours by area.
    :param contours: A list of contours.
    :param upper: The upper area bound.
    :param lower: The lower area bound.
    :return: The filtered list of contours.
    """
    return [c for c in contours if upper >= cv2.contourArea(c) >= lower]


def filter_contour_by_y_point(contour, y, distance) -> List[List[int]]:
    """
    Filters a contour by the y point.
    :param contour: The contour to filter.
    :param y: The y point to filter by.
    :param distance: The distance to filter by.
    :return: The filtered contour.
    """
    return [c for c in contour if (cy := contour_centre(c)[1]) <= y + distance and cy >= y - distance]


def draw_contours(image: np.ndarray, contours: List[List[int]]) -> None:
    """
    Draws contours on the image.
    :param image: The image to draw on top of.
    :param contours: THe list of contours to draw.
    """
    plot_image = image.copy()
    xs, ys = [], []
    for i, c in enumerate(contours):
        x, y = contour_centre(c)
        xs.append(x)
        ys.append(y)
        plot_image = cv2.drawContours(plot_image, contours, i, (0, 255, 0), 3)

    plt.imshow(plot_image)

    # Contour centres.
    plt.scatter(xs, ys)
    h, w, *_ = image.shape

    # Centre contour.
    plt.scatter(np.mean(xs), np.mean(ys), c="r")
    plt.show()


def text_from_image(image: np.ndarray, words: List[str]) -> str:
    """
    Extracts text from an image.
    :param image: The image to extract from.
    :param words: A list of possible words that are contained within the image.
    :return: The matched word.
    """
    img = cv2.resize(image, (0, 0), fx=2.0, fy=1.0, interpolation=cv2.INTER_CUBIC)
    custom_config = r"--oem 3 --psm 7 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    text = pytesseract.image_to_string(img, config=custom_config).strip()
    return min(words,
               key=lambda s: utils.minimum_edit_distance(s.replace(' ', '').replace('-', '').replace('\'', '').upper(),
                                                         text.replace(' ', '')))


def extract_bird_card_text_image(image: np.ndarray) -> Tuple[List[np.ndarray], List[Tuple[float, float]]]:
    card_text_images = []
    centres = []
    w, h = window_dimensions()
    for x0, y0 in kp.BIRD_CARD_POSITIONS:
        sx0, sy0 = int(w * x0), int(h * y0)
        card_text_images.append(image[sy0:sy0 + 40, sx0:sx0 + 155])
        centres.append((x0, y0 + 0.1))
    return card_text_images, centres


def extract_bonus_card_text_image(image:np.ndarray, contours:List[List[int]]) -> \
        Tuple[List[np.ndarray], List[Tuple[float, float]]]:
    card_text_images = []
    centres = []
    for c in contours:
        x0, y0, w, h = cv2.boundingRect(c)
        card_text_images.append(image[y0 - 15:y0 + 20, x0:x0 + w])
        centres.append(contour_centre(c))
    return card_text_images, centres


def extract_tray_card_text_image(image:np.ndarray) -> List[np.ndarray]:
    card_text_images = []
    w, h = window_dimensions()
    for x0, y0 in kp.TRAY_CARD_POSITIONS:
        sx0, sy0 = int(w * x0), int(h * y0)
        card_text_images.append(image[sy0:sy0 + 18, sx0:sx0 + 160])
    return card_text_images


def extract_bird_cards(verbose: bool = False):
    # TODO fix these magic numbers
    image = np.asarray(ImageGrab.grab(bbox=window_bbox()))
    card_text_images, centres = extract_bird_card_text_image(image)
    names = [text_from_image(i, cards.Deck().birds) for i in card_text_images]
    if verbose:
        plt.imshow(image)
        plt.show()
        print(f'Birds:\n{names}')
    return names, centres, image


def extract_tray_cards(verbose: bool = False) -> List[str]:
    image = np.asarray(ImageGrab.grab(bbox=window_bbox()))
    card_text_images = extract_tray_card_text_image(image)
    names = [text_from_image(i, cards.Deck().birds) for i in card_text_images]
    if verbose:
        plt.imshow(image)
        plt.show()
        print(f'Tray:\n{names}')
    return names


def extract_bonus_cards(verbose: bool = False):
    # TODO fix these magic numbers
    image = np.asarray(ImageGrab.grab(bbox=window_bbox()))
    grey = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    _, thresh = cv2.threshold(grey, 200, 255, cv2.THRESH_BINARY)
    contours = find_contours(thresh)
    contours = filter_contours_by_area(contours, 100000, 20000)
    contours = filter_contour_by_y_point(contours, 350, 150)
    card_text_images, centres = extract_bonus_card_text_image(image, contours)
    names = [text_from_image(i, cards.Deck().bonus_cards) for i in card_text_images]
    if verbose:
        plt.imshow(image)
        plt.show()
        print(f'Bonus:\n{names}')
    return names, centres, image


def extract_player_board(verbose: bool = False) -> List[List[str]]:
    image = np.asarray(ImageGrab.grab(bbox=window_bbox()))
    w, h = window_dimensions()
    board = []
    for x0, y0, x1, y1 in kp.BIRDS_IN_HABITAT_NAMES_BBOXS:
        sx0, sy0, sx1, sy1 = int(w * x0), int(h * y0), int(w * x1), int(h * y1)
        habitat_image = image[sy0:sy1, sx0:sx1]
        grey = cv2.cvtColor(habitat_image, cv2.COLOR_RGB2GRAY)
        _, thresh = cv2.threshold(grey, 200, 255, cv2.THRESH_BINARY_INV)
        contours = find_contours(thresh)
        contours = filter_contours_by_area(contours, 100000, 3000)
        board.append([text_from_image(habitat_image[cy:cy + ch, cx:cx + cw], cards.Deck().birds)
                      for cx, cy, cw, ch in map(cv2.boundingRect, contours)])
    if verbose:
        plt.imshow(image)
        plt.show()
        print('Board:\n\t', '\n\t'.join(f'{h}: {b}' for h, b in zip(utils.HABITATS, board)))
    return board


def extract_highlighted_card(verbose: bool = False) -> str:
    w, h = window_dimensions()
    x0, y0, x1, y1 = kp.HIGHLIGHTED_CARD_BBOX
    sx0, sy0, sx1, sy1 = int(w * x0), int(h * y0), int(w * x1), int(h * y1)
    image = np.asarray(ImageGrab.grab(bbox=window_bbox()))
    image = image[sy0:sy1, sx0:sx1]

    grey = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    _, thresh = cv2.threshold(grey, 200, 255, cv2.THRESH_BINARY_INV)
    contours = find_contours(thresh)
    contours = filter_contours_by_area(contours, 80000, 6000)

    cx, cy, cw, ch = cv2.boundingRect(contours[0])
    name = text_from_image(image[cy:cy + ch, cx:cx + cw], cards.Deck().birds)

    if verbose:
        plt.imshow(image)
        plt.show()
        print(f'Highlighted card: {name}')
    return name
