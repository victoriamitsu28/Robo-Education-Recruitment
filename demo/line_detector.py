"""A small, inspectable image-based line-position demo. It never drives motors."""

import argparse
from dataclasses import asdict, dataclass
import json
from pathlib import Path
import cv2 as cv
import numpy as np


@dataclass(frozen=True)
class Detection:
    status: str
    error: float | None
    center_x: float | None
    roi_y: int
    candidates: int
    reason: str


def detect_line(frame, threshold=100, roi_start=0.6):
    if frame is None or not isinstance(frame, np.ndarray) or frame.dtype != np.uint8:
        raise ValueError('expected a uint8 image')
    if frame.ndim not in (2, 3) or (frame.ndim == 3 and frame.shape[2] != 3):
        raise ValueError('expected a grayscale or BGR image')
    height, width = frame.shape[:2]
    if min(height, width) < 8 or not 0 <= threshold <= 255 or not 0 <= roi_start < 1:
        raise ValueError('invalid image size, threshold, or ROI')
    roi_y = min(int(height * roi_start), height - 2)
    roi = frame[roi_y:, :]
    gray = cv.cvtColor(roi, cv.COLOR_BGR2GRAY) if roi.ndim == 3 else roi
    _, mask = cv.threshold(gray, threshold, 255, cv.THRESH_BINARY_INV)
    contours, _ = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    area = mask.size
    candidates = [c for c in contours if cv.contourArea(c) >= 0.003 * area]
    if not candidates:
        return Detection('no_line', None, None, roi_y, 0, 'no significant foreground'), mask
    if len(candidates) != 1:
        return Detection('ambiguous', None, None, roi_y, len(candidates), 'multiple significant regions'), mask
    contour = candidates[0]
    _, _, box_width, _ = cv.boundingRect(contour)
    moments = cv.moments(contour)
    if moments['m00'] <= 0 or moments['m00'] > 0.35 * area or box_width > 0.55 * width:
        return Detection('ambiguous', None, None, roi_y, 1, 'region fails area or width check'), mask
    center_x = moments['m10'] / moments['m00']
    error = (center_x - (width - 1) / 2) / (width / 2)
    return Detection('ok', error, center_x, roi_y, 1, 'single plausible region'), mask


def direction(result, deadband=0.08):
    if result.status != 'ok' or result.error is None:
        return 'STOP'
    if result.error < -deadband:
        return 'LEFT'
    if result.error > deadband:
        return 'RIGHT'
    return 'STRAIGHT'


def annotate(frame, result):
    if frame.ndim == 2:
        frame = cv.cvtColor(frame, cv.COLOR_GRAY2BGR)
    output = frame.copy()
    height, width = output.shape[:2]
    cv.rectangle(output, (0, result.roi_y), (width - 1, height - 1), (0, 150, 220), 2)
    cv.line(output, (round((width - 1) / 2), result.roi_y),
            (round((width - 1) / 2), height - 1), (220, 120, 0), 1)
    if result.center_x is not None:
        cv.circle(output, (round(result.center_x), (result.roi_y + height - 1) // 2), 5, (0, 0, 230), -1)
    label = f'{result.status} {direction(result)}'
    cv.putText(output, label, (8, 22), cv.FONT_HERSHEY_SIMPLEX, 0.55, (10, 80, 180), 1)
    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--image', required=True)
    parser.add_argument('--output', default='results/demo')
    parser.add_argument('--threshold', type=int, default=100)
    args = parser.parse_args()
    # imdecode handles non-ASCII paths on Windows as well as ordinary paths.
    frame = cv.imdecode(np.fromfile(args.image, dtype=np.uint8), cv.IMREAD_COLOR)
    if frame is None:
        parser.error('could not decode the input image')
    result, mask = detect_line(frame, args.threshold)
    output = Path(args.output)
    output.mkdir(parents=True, exist_ok=True)
    for name, image in [('mask.png', mask), ('annotated.png', annotate(frame, result))]:
        ok, encoded = cv.imencode('.png', image)
        if not ok:
            raise RuntimeError('could not encode output image')
        encoded.tofile(output / name)
    record = asdict(result) | {'direction': direction(result), 'threshold': args.threshold}
    (output / 'result.json').write_text(json.dumps(record, indent=2), encoding='utf-8')
    print(json.dumps(record))


if __name__ == '__main__':
    main()
