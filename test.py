import sys

from utils.image_search import search, debug_items, image_url, image_mime_type
from utils.download import download
from utils.video import make_video
from utils.constants import AUDIO_FILE

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

    log.info('Then:')
    debug_items(then)

    log.info('Now:')
    debug_items(now)

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

    make_video(
        then_frames+now_frames,
        AUDIO_FILE,
    )


def start_logging():
    stderr = logging.StreamHandler()
    stderr.setLevel(logging.DEBUG)
    stderr.setFormatter(logging.Formatter(fmt='%(levelname)8s: %(message)s'))

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    root_logger.addHandler(stderr)


def download_frame(item, prefix=None):
    image_type = image_mime_type(item).partition('/')[2]
    suffix = ('.' + image_type if image_type else None)
    return download(image_url(item), prefix=prefix, suffix=suffix)


if __name__ == '__main__':
    main()
