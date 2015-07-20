import os
import tempfile

from urllib.request import urlopen
from urllib.error import HTTPError

from .constants import TMP_DIR


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
