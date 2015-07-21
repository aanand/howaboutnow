import sys

from utils.image_search import search, debug_items, image_url, image_mime_type
from utils.download import download
from utils.image import make_thumbnail
from utils.slideshow import make_slideshow
from utils.video import make_video
from utils.constants import (
    AUDIO_FILE,
    SECTION_LENGTH_THEN,
    SECTION_LENGTH_NOW,
    FRAME_FILENAME_FORMAT,
    MIN_FRAMES_THEN,
    MAX_FRAMES_THEN,
    MIN_FRAMES_NOW,
    MAX_FRAMES_NOW,
)

import logging
log = logging.getLogger(__name__)


def main():
    start_logging()

    query = sys.argv[1]
    then, now = search(query)

    log.info('Then:')
    debug_items(then)

    log.info('Now:')
    debug_items(now)

    if len(then) < MIN_FRAMES_THEN:
        raise Exception("Couldn't find enough old images - giving up")

    if len(now) < MIN_FRAMES_NOW:
        raise Exception("Couldn't find enough new images - giving up")

    then_frames = list(filter(None, (download_frame(item, 'then.') for item in then)))
    now_frames = list(filter(None, (download_frame(item, 'now.') for item in now)))

    if len(then_frames) < MIN_FRAMES_THEN:
        raise Exception("Couldn't download enough old images - giving up")

    if len(now_frames) < MIN_FRAMES_NOW:
        raise Exception("Couldn't download enough new images - giving up")

    then_frames = then_frames[:MAX_FRAMES_THEN]
    now_frames = now_frames[:MAX_FRAMES_NOW]

    all_frames = make_slideshow(
        [
            (then_frames, SECTION_LENGTH_THEN),
            (now_frames, SECTION_LENGTH_NOW),
        ],
        FRAME_FILENAME_FORMAT,
    )

    make_video(all_frames, AUDIO_FILE)


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
    downloaded = download(image_url(item), prefix=prefix, suffix=suffix)
    return make_thumbnail(downloaded, 500, 500) if downloaded else None


if __name__ == '__main__':
    main()
