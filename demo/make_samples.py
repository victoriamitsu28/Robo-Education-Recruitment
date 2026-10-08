"""Generate clearly labeled synthetic classroom inputs, not real camera data."""

from pathlib import Path
import cv2 as cv
import numpy as np

ROOT = Path(__file__).resolve().parents[1]


def sample(kind):
    image = np.full((240, 320, 3), 240, dtype=np.uint8)
    if kind in ('left', 'center', 'right'):
        center = {'left': 79.5, 'center': 159.5, 'right': 239.5}[kind]
        image[:, int(center - 11.5):int(center + 12.5)] = 20
    elif kind == 'two_lines':
        image[:, 68:92] = 20
        image[:, 228:252] = 20
    elif kind == 'shadow':
        image[:, :210] = 20
        image[:, 228:252] = 20
    elif kind == 'dark_background':
        image[:] = 120
        image[:, 148:172] = 20
    elif kind != 'no_line':
        raise ValueError(kind)
    return image


def main():
    folder = ROOT / 'assets' / 'samples'
    folder.mkdir(parents=True, exist_ok=True)
    for kind in ('left', 'center', 'right', 'no_line', 'two_lines', 'shadow', 'dark_background'):
        ok, encoded = cv.imencode('.png', sample(kind))
        if not ok:
            raise RuntimeError('image encoding failed')
        encoded.tofile(folder / (kind + '.png'))
    print('Generated 7 synthetic teaching images.')


if __name__ == '__main__':
    main()
