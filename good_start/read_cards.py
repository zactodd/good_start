import cv2
import pytesseract
import numpy as np
from PIL import ImageGrab
import matplotlib.pyplot as plt
import gui_interactions as gi
import utils


BIRD_CARD_COLOUR_BOUNDS = (
    (229,221,191), (229,221,191)
)


def find_contours(grey_image):
    """
    Finds all the contours from a grey scale image.
    :param grey_image: A grey scale image.
    :return: a list of contours
    """
    _, thresh = cv2.threshold(grey_image, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    return contours

def contour_centre(contour):
    """
    Calculates the centre of the contour.
    :param contour: The contour in which to obtain the centre.
    :return: x axis centre, y axis centre.
    """
    m = cv2.moments(contour)
    return m["m10"] / m["m00"], m["m01"] / m["m00"]

def filter_contours_by_area(contours, upper, lower):
    """
    Filters a list of contours by area.
    :param contours: A list of contours.
    :param upper: The upper area bound.
    :param lower: The lower area bound.
    :return: The filtered list of contours.
    """
    return [c for c in contours if upper >= cv2.contourArea(c) >= lower]


def filter_contour_by_y_point(contour, y, distance):
    """
    Filters a contour by the y point.
    :param contour: The contour to filter.
    :param y: The y point to filter by.
    :param distance: The distance to filter by.
    :return: The filtered contour.
    """
    return [c for c in contour if (cy := contour_centre(c)[1]) <= y + distance and cy >= y - distance]


def draw_contours(image, contours):
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


def extract_bird_card_text_image(image, card_contours):
    card_text_images = []
    centres = []
    for c in card_contours:
        x0, y0, w, h = cv2.boundingRect(c)
        card_text_images.append(image[y0:y0 + 45, x0 + 40:x0 + w])
        centres.append(contour_centre(c))
    return card_text_images, centres


def extract_bonus_card_text_image(image, card_contours):
    card_text_images = []
    centres = []
    for c in card_contours:
        x0, y0, w, h = cv2.boundingRect(c)
        card_text_images.append(image[y0 - 15:y0 + 20, x0:x0 + w])
        centres.append(contour_centre(c))
    return card_text_images, centres


def extract_bird_cards():
    # TODO fix these magic numbers
    bbox = gi.WINDOW_X0, gi.WINDOW_Y0, gi.WINDOW_X1, gi.WINDOW_Y1
    image = np.asarray(ImageGrab.grab(bbox=bbox))

    grey = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    _, thresh = cv2.threshold(grey, 200, 255, cv2.THRESH_BINARY)
    contours = find_contours(thresh)
    contours = filter_contours_by_area(contours, 100000, 20000)
    contours = filter_contour_by_y_point(contours, 350, 100)

    card_text_images, centres = extract_bird_card_text_image(image, contours)
    names = []
    for img in card_text_images:
        custom_config = r"--oem 3 --psm 7 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        text = pytesseract.image_to_string(img, config=custom_config).strip()
        name = min(utils.BIRD_NAMES,
                   key=lambda s: utils.minimum_edit_distance(s.replace(' ', '').replace('-', '').replace('\'', '').upper(),
                                                             text.replace(' ', '')))
        names.append(name)
    return names, centres, image


def extract_bonus_cards():
    # TODO fix these magic numbers
    bbox = gi.WINDOW_X0, gi.WINDOW_Y0, gi.WINDOW_X1, gi.WINDOW_Y1
    image = np.asarray(ImageGrab.grab(bbox=bbox))
    grey = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    _, thresh = cv2.threshold(grey, 200, 255, cv2.THRESH_BINARY)
    contours = find_contours(thresh)
    contours = filter_contours_by_area(contours, 100000, 20000)
    contours = filter_contour_by_y_point(contours, 350, 150)
    card_text_images, centres = extract_bonus_card_text_image(image, contours)
    names = []
    for img in card_text_images:
        custom_config = r"--oem 3 --psm 7 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        text = pytesseract.image_to_string(img, config=custom_config).strip()
        name = min(utils.BONUS_IMPORTANCE,
                   key=lambda s: utils.minimum_edit_distance(s.replace(' ', '').replace('-', '').upper(), text.replace(' ', '')))
        names.append(name)
    return names, centres, image
