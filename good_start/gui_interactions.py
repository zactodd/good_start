import autoit
import key_positions
import time
import ctypes


def _window_coords_from_name(name: str)-> tuple:
    hwnd = ctypes.windll.user32.FindWindowW(0, name)
    rect = ctypes.wintypes.RECT()
    ctypes.windll.user32.GetWindowRect(hwnd, ctypes.pointer(rect))
    x0, y0, x1, y1 = rect.left, rect.top, rect.right, rect.bottom
    return x0, y0, x1 - x0, y1 - y0


WINDOW_X0, WINDOW_Y0, WINDOW_W, WINDOW_H = _window_coords_from_name('Wingspan')


def move_and_click(x: float, y: float) -> None:
    """
    Click on a given a relative x, y coordinate
    :param x:
    :param y:
    """
    autoit.mouse_click("left", int(WINDOW_X0 + WINDOW_W * x), int(WINDOW_Y0 + WINDOW_H * y), 1)


def menu_transition(buttons, wait=2) -> None:
    for button in buttons:
        move_and_click(*button)
        time.sleep(wait)


def menu_from_start() -> None:
    menu_transition(key_positions.FIRST_MENU_TRAVERSAL)


def new_game_from_game() -> None:
    menu_transition(key_positions.NEW_GAME_FROM_GAME)

