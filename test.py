import sys

from utils.images import search, debug, image_url, image_mime_type
from utils.download import download
from utils.constants import TMP_DIR

import subprocess
import os.path
import shutil

import logging
log = logging.getLogger(__name__)


MIN_FRAMES_THEN = 3
MAX_FRAMES_THEN = 6
MIN_FRAMES_NOW = 2
MAX_FRAMES_NOW = 4


def main():
    start_logging()

    query = sys.argv[1]
    then = search(query, 2000, 2013)
    now = list(reversed(search(query, 2013, 2020)))

    print('Then:\n')
    debug(then)

    print('\n===============\n\n')

    print('Now:\n')
    debug(now)

    # if len(then) < MIN_FRAMES_THEN:
    #     print("Couldn't find enough old images - giving up")
    #     return

    # if len(now) < MIN_FRAMES_NOW:
    #     print("Couldn't find enough new images - giving up")
    #     return

    then_frames = list(filter(None, (download_frame(item, 'then.') for item in then)))
    now_frames = list(filter(None, (download_frame(item, 'now.') for item in now)))

    # if len(then_frames) < MIN_FRAMES_THEN:
    #     print("Couldn't download enough old images - giving up")
    #     return

    # if len(now_frames) < MIN_FRAMES_NOW:
    #     print("Couldn't download enough new images - giving up")
    #     return

    then_frames = then_frames[:MAX_FRAMES_THEN]
    now_frames = now_frames[:MAX_FRAMES_NOW]

    print(then_frames)
    print(now_frames)

    all_frames = then_frames + now_frames
    frame_filename_format = 'frame-%03d.jpg'
    numbered_frames = [
        os.path.join(TMP_DIR, frame_filename_format % index)
        for index in range(0, len(all_frames))
    ]
    print(numbered_frames)

    for src, dst in zip(all_frames, numbered_frames):
        shutil.copy(src, dst)

    check_call([
        'bin/ffmpeg',
        '-y',
        '-framerate', '1',
        '-i', os.path.join(TMP_DIR, frame_filename_format),
        '-c:v', 'libx264',
        '-r', '30',
        '-pix_fmt', 'yuv420p',
        'tmp/out.mp4',
    ])


def start_logging():
    stderr = logging.StreamHandler()
    stderr.setLevel(logging.DEBUG)
    stderr.setFormatter(logging.Formatter(fmt='%(levelname)8s: %(message)s'))

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    root_logger.addHandler(stderr)


def check_call(cmd, *args, **kwargs):
    log.info("$ %s" % " ".join(cmd))
    output = ""

    try:
        output = subprocess.check_output(cmd, *args, **kwargs)
    except subprocess.CalledProcessError:
        log.error(output)
        raise


def download_frame(item, prefix=None):
    image_type = image_mime_type(item).partition('/')[2]
    suffix = ('.' + image_type if image_type else None)
    return download(image_url(item), prefix=prefix, suffix=suffix)


if __name__ == '__main__':
    main()
