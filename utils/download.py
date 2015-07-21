import os
import tempfile

from urllib.request import urlopen
from urllib.error import HTTPError

from .constants import TMP_DIR

import logging
log = logging.getLogger(__name__)


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
        log.info('Downloading {} to {}'.format(url, local_file.name))
        data = urlopen(url).read()
        if data:
            local_file.write(data)
            return local_file.name
    except HTTPError as e:
        log.info(e)
    finally:
        local_file.close()

    os.remove(local_file.name)
    return None
