import logging
log = logging.getLogger(__name__)

from .constants import TMP_DIR, FRAME_FILENAME_FORMAT, FRAMERATE
from .subprocess import check_call

FFMPEG_BINARY = 'bin/ffmpeg'


def make_video(input, audio_file):
    check_call([
        FFMPEG_BINARY,
        '-y',
        '-framerate', str(FRAMERATE),
        '-i', FRAME_FILENAME_FORMAT,
        '-i', audio_file,
        '-c:v', 'libx264',
        '-c:a', 'libvo_aacenc',
        '-b:a', '320k',
        '-r', str(FRAMERATE),
        '-pix_fmt', 'yuv420p',
        '-shortest',
        'tmp/out.mp4',
    ])
