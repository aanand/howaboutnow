from __future__ import unicode_literals

from subprocess import check_call as _check_call, CalledProcessError

import logging
log = logging.getLogger(__name__)


def check_call(cmd, *args, **kwargs):
    log.info("$ %s" % " ".join(cmd))
    return _check_call(cmd, *args, **kwargs)
