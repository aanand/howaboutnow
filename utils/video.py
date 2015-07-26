import logging
log = logging.getLogger(__name__)

from .constants import TMP_DIR, FRAMERATE
from .subprocess import check_call

FFMPEG_BINARY = 'bin/ffmpeg'


def make_video_from_images(input_filename_format, audio_file):
    output_filename = 'tmp/out.mp4'

    check_call([
        FFMPEG_BINARY,
        '-y',
        '-framerate', str(FRAMERATE),
        '-i', input_filename_format,
        '-i', audio_file,
        '-c:v', 'libx264',
        '-c:a', 'libvo_aacenc',
        '-b:a', '320k',
        '-r', str(FRAMERATE),
        '-pix_fmt', 'yuv420p',
        '-shortest',
        output_filename,
    ])

    return output_filename
