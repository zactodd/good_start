import key_positions as kp


def score_on_game_board(game_image, score_image):
    x0, y0, rw, rh = kp.DUET_SCORE_BAR
    h, w, *_ = game_image.shape
    sx0, sy0, sw, sh = int(x0 * w), int(y0 * h), int(rw * w), int(rh * h)
    embossed_image = game_image.copy()
    embossed_image[0:sh, 0:sw, :] = score_image[sy0:sy0+sh, sx0:sx0+sw, :]
    return embossed_image