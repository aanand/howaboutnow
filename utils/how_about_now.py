import os

from itertools import ifilter, islice

from .image_search import search, debug_items, image_url, image_mime_type
from .download import download
from .image import make_thumbnail
from .slideshow import make_slideshow
from .video import make_video_from_images
from .constants import (
    TMP_DIR,
    AUDIO_FILE,
    SECTION_LENGTH_THEN,
    SECTION_LENGTH_NOW,
    MIN_FRAMES_THEN,
    MAX_FRAMES_THEN,
    MIN_FRAMES_NOW,
    MAX_FRAMES_NOW,
)


def make_video(query):
    then, now = search(query)

    then_frames = get_frames(then, 'then.', MAX_FRAMES_THEN)
    now_frames = get_frames(now, 'now.', MAX_FRAMES_NOW)

    if len(then_frames) < MIN_FRAMES_THEN:
        raise Exception("Couldn't download enough old images - giving up")

    if len(now_frames) < MIN_FRAMES_NOW:
        raise Exception("Couldn't download enough new images - giving up")

    filename_format = os.path.join(TMP_DIR, 'frame-%03d.jpg')

    all_frames = make_slideshow(
        [
            (then_frames, SECTION_LENGTH_THEN),
            (now_frames, SECTION_LENGTH_NOW),
        ],
        filename_format,
    )

    return make_video_from_images(filename_format, AUDIO_FILE)


def get_frames(items, prefix, max_items):
    frame_iterator = ifilter(None, (download_frame(item, prefix) for item in items))
    return take(frame_iterator, max_items)


def take(iterator, max_items):
    return list(islice(iterator, 0, max_items))


def download_frame(item, prefix=None):
    image_type = image_mime_type(item).partition('/')[2]
    suffix = ('.' + image_type if image_type else None)
    downloaded = download(image_url(item), prefix=prefix, suffix=suffix)
    return make_thumbnail(downloaded, 500, 500) if downloaded else None
