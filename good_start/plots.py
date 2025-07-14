import key_positions as kp
import imageio
from typing import List, Tuple, Dict, Any, Iterator
from tqdm import tqdm
import os


def score_on_game_board(game_image, score_image):
    x0, y0, rw, rh = kp.DUET_SCORE_BAR
    h, w, *_ = game_image.shape
    sx0, sy0, sw, sh = int(x0 * w), int(y0 * h), int(rw * w), int(rh * h)
    embossed_image = game_image.copy()
    embossed_image[0:sh, 0:sw, :] = score_image[sy0:sy0+sh, sx0:sx0+sw, :]
    return embossed_image


def create_video(frame_filenames: List[str],
                 output_video_filename: str = 'bird_play_frequency_animated.mp4',
                 fps: float = 0.75, verbose: bool=True):
    assert not frame_filenames, 'No frames generated, so no video was created.'

    writer = imageio.get_writer(output_video_filename, fps=fps, codec='libx264', quality=10) # quality 1-10

    if verbose:
        print(f"\nCreating video from {len(frame_filenames)} frames...")
        frame_filenames = tqdm(frame_filenames)

    for filename in frame_filenames:
        image = imageio.imread(filename)
        writer.append_data(image)
        os.remove(filename) # Clean up temporary frame file immediately after use

    writer.close()

    if verbose:
        print(f"Video '{output_video_filename}' created successfully!")
        print("Temporary frame files cleaned up.")
