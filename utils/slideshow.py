from __future__ import unicode_literals

import shutil

from .constants import FRAMERATE

import logging
log = logging.getLogger(__name__)


def make_slideshow(sections, filename_format):
    frames = []

    for (input_frames, duration) in sections:
        output_length = int(round(FRAMERATE * duration))
        frames += make_section(input_frames, output_length, len(frames), filename_format)

    return frames


def make_section(input_frames, output_length, start_index, filename_format):
    log.info('make_section({}, {}, {})'.format(input_frames, output_length, start_index))

    baked = [
        input_frames[int(i * len(input_frames) / output_length)]
        for i in range(output_length)
    ]

    numbered = [
        filename_format % index
        for index in range(start_index, start_index + output_length)
    ]

    for src, dst in zip(baked, numbered):
        log.info('copy {} -> {}'.format(src, dst))
        shutil.copy(src, dst)

    return numbered
