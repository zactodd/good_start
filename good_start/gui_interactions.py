import autoit
import key_positions
import time
import ctypes


def _window_bbox_from_name(name: str)-> tuple:
    hwnd = ctypes.windll.user32.FindWindowW(0, name)
    rect = ctypes.wintypes.RECT()
    ctypes.windll.user32.GetWindowRect(hwnd, ctypes.pointer(rect))
    x0, y0, x1, y1 = rect.left, rect.top, rect.right, rect.bottom
    return x0, y0, x1, y1


def window_bbox() -> tuple:
    return _window_bbox_from_name('Wingspan')


def window_dimensions() -> tuple:
    x0, y0, x1, y1 = window_bbox()
    return x1 - x0, y1 - y0


def move_and_click(x: float, y: float) -> None:
    w, h = window_dimensions()
    x0, y0, *_ = window_bbox()
    if x > 1:
        x, y = x / w, y / h
    autoit.mouse_click("left", round(x0 + x * w), round(y0 + y * h), 1, 1)


def activate_window():
    autoit.win_activate('Wingspan')


def click_buttons(buttons, wait=0.5) -> None:
    for button in buttons:
        move_and_click(*button)
        time.sleep(wait)


def menu_from_start() -> None:
    click_buttons(key_positions.FIRST_MENU_TRAVERSAL)


def new_game_from_game() -> None:
    click_buttons(key_positions.MENU_TRAVERSAL)


def exit_game() -> None:
    click_buttons(key_positions.EXIT_GAME)
