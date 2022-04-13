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


WINDOW = WINDOW_X0, WINDOW_Y0, WINDOW_W, WINDOW_H = _window_coords_from_name('Wingspan')
WINDOW_X1, WINDOW_Y1 = WINDOW_X0 + WINDOW_W, WINDOW_Y0 + WINDOW_H


def move_and_click(x: float, y: float) -> None:
    if x > 1:
        x, y = x / WINDOW_W, y / WINDOW_H
    autoit.mouse_click("left", round(WINDOW_X0 + x * WINDOW_W), round(WINDOW_Y0 + y * WINDOW_H), 1, 1)


def click_buttons(buttons, wait=1) -> None:
    for button in buttons:
        move_and_click(*button)
        time.sleep(wait)


def menu_from_start() -> None:
    click_buttons(key_positions.FIRST_MENU_TRAVERSAL)


def new_game_from_game() -> None:
    click_buttons(key_positions.MENU_TRAVERSAL)


def exit_game() -> None:
    click_buttons(key_positions.EXIT_GAME)

