from __future__ import unicode_literals

import os

from .check_call import check_call, CalledProcessError


def make_thumbnail(filename, width, height):
    out_filename = os.path.join(
        os.path.dirname(filename),
        'thumb.' + os.path.basename(filename) + '.jpg',
    )

    try:
        check_call([
            'convert',
            '-define', 'jpeg:size=1000x1000',
            filename,
            '-thumbnail', '{}x{}^'.format(width, height),
            '-gravity', 'center',
            '-extent', '{}x{}'.format(width, height),
            out_filename,
        ])

        if os.path.exists(out_filename):
            return out_filename
    except CalledProcessError:
        pass

    return None
