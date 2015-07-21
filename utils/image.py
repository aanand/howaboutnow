import os

from .subprocess import check_call


def make_thumbnail(filename, width, height):
    out_filename = os.path.join(
        os.path.dirname(filename),
        'thumb.' + os.path.basename(filename) + '.jpg',
    )

    check_call([
        'convert',
        '-define', 'jpeg:size=1000x1000',
        filename,
        '-thumbnail', '{}x{}^'.format(width, height),
        '-gravity', 'center',
        '-extent', '{}x{}'.format(width, height),
        out_filename,
    ])

    return out_filename