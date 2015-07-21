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

    then_frames = get_frames(then, 'then.', MAX_FRAMES_THEN)
    now_frames = get_frames(now, 'now.', MAX_FRAMES_NOW)

    if len(then_frames) < MIN_FRAMES_THEN:
        raise Exception("Couldn't download enough old images - giving up")

    if len(now_frames) < MIN_FRAMES_NOW:
        raise Exception("Couldn't download enough new images - giving up")

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


def get_frames(items, prefix, max_items):
    frame_iterator = filter(None, (download_frame(item, prefix) for item in items))
    return take(frame_iterator, max_items)


def take(iterator, max_items):
    from itertools import islice
    return list(islice(iterator, 0, max_items))


def download_frame(item, prefix=None):
    image_type = image_mime_type(item).partition('/')[2]
    suffix = ('.' + image_type if image_type else None)
    downloaded = download(image_url(item), prefix=prefix, suffix=suffix)
    return make_thumbnail(downloaded, 500, 500) if downloaded else None


if __name__ == '__main__':
    main()
