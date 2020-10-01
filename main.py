import argparse
import os
import sys

import numpy as np
from PIL import Image
from decord import VideoReader
from decord import cpu

if __name__ == '__main__':
    threshold = 15

    parser = argparse.ArgumentParser(description='Create thumbnail from video.')
    parser.add_argument('-p', action="store", dest="path", help="Path to a video file.")

    args = parser.parse_args()

    if not os.path.isfile(args.path):
        sys.exit("File for given path not found")

    filename, file_extension = os.path.splitext(args.path)
    vr = VideoReader(args.path, ctx=cpu(0))

    try:
        p = len(vr) // 10
        batch = [x for x in range(len(vr))[-p:]]
    except ZeroDivisionError:
        sys.exit("Video is too short")

    last_mean = 0
    indexes = []
    means = {}
    for f_number in batch:
        frame = vr[f_number]
        im = frame.asnumpy()

        frame_mean = np.sum(im) / (float(im.shape[0] * im.shape[1] * im.shape[2]))
        diff = frame_mean - last_mean

        if diff < 0 and np.abs(diff) >= threshold:
            indexes.append(f_number-1)

        last_mean = frame_mean

    if indexes:
        export_frame = vr[indexes[0]]
    else:
        export_frame = vr[batch[-1]]

    out_path = f"{args.path}".replace(file_extension, "_output.jpg")

    img = Image.fromarray(export_frame.asnumpy(), 'RGB')
    img.save(out_path)

    print(f"Your thumbnail has been generated successfully. Output path: {out_path}")
