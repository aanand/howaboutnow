import sys
import os
import tempfile
from urllib.request import urlopen
from urllib.error import HTTPError

from utils.images import search, debug, image_url, image_mime_type

TMP_DIR = './tmp'

MIN_FRAMES_THEN = 3
MAX_FRAMES_THEN = 6
MIN_FRAMES_NOW = 2
MAX_FRAMES_NOW = 4


def main():
    query = sys.argv[1]
    then = search(query, 2000, 2013)
    now = list(reversed(search(query, 2013, 2020)))

    print('Then:\n')
    debug(then)

    print('\n===============\n\n')

    print('Now:\n')
    debug(now)

    if len(then) < MIN_FRAMES_THEN:
        print("Couldn't find enough old images - giving up")
        return

    if len(now) < MIN_FRAMES_NOW:
        print("Couldn't find enough new images - giving up")
        return

    then_frames = list(filter(None, (download_frame(item, 'then.') for item in then)))
    now_frames = list(filter(None, (download_frame(item, 'now.') for item in now)))

    if len(then_frames) < MIN_FRAMES_THEN:
        print("Couldn't download enough old images - giving up")
        return

    if len(now_frames) < MIN_FRAMES_NOW:
        print("Couldn't download enough new images - giving up")
        return

    then_frames = then_frames[:MAX_FRAMES_THEN]
    now_frames = now_frames[:MAX_FRAMES_NOW]

    print(then_frames)
    print(now_frames)


def download_frame(item, prefix=None):
    mime_type = image_mime_type(item).partition('/')[2] or None
    suffix = ('.' + mime_type if mime_type else None)
    return download(image_url(item), prefix=prefix, suffix=suffix)


def download(url, prefix=None, suffix=None):
    if not os.path.exists(TMP_DIR):
        os.mkdir(TMP_DIR)

    local_file = tempfile.NamedTemporaryFile(
        dir=TMP_DIR,
        prefix=(prefix or ''),
        suffix=(suffix or ''),
        delete=False,
    )

    try:
        print('Downloading {} to {}'.format(url, local_file.name))
        local_file.write(urlopen(url).read())
        local_file.close()
        return local_file.name
    except HTTPError as e:
        print(e)
        local_file.close()
        os.remove(local_file.name)
        return None


if __name__ == '__main__':
    main()
