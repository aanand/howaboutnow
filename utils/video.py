import os.path
import shutil

import logging
log = logging.getLogger(__name__)

from .constants import TMP_DIR
from .subprocess import check_call

FFMPEG_BINARY = 'bin/ffmpeg'
FRAME_FILENAME_FORMAT = 'frame-%03d.jpg'


def make_video(frame_files, audio_file):
    numbered_files = [
        os.path.join(TMP_DIR, FRAME_FILENAME_FORMAT % index)
        for index in range(0, len(frame_files))
    ]

    for src, dst in zip(frame_files, numbered_files):
        shutil.copy(src, dst)

    check_call([
        FFMPEG_BINARY,
        '-y',
        '-framerate', '1',
        '-i', os.path.join(TMP_DIR, FRAME_FILENAME_FORMAT),
        '-i', audio_file,
        '-c:v', 'libx264',
        '-c:a', 'copy',
        '-r', '30',
        '-pix_fmt', 'yuv420p',
        '-shortest',
        'tmp/out.mp4',
    ])
