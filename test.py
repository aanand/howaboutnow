import sys

import logging
log = logging.getLogger(__name__)

from utils import make_video


def main():
    start_logging()

    query = sys.argv[1]
    make_video(query)


def start_logging():
    stderr = logging.StreamHandler()
    stderr.setLevel(logging.DEBUG)
    stderr.setFormatter(logging.Formatter(fmt='%(levelname)8s: %(message)s'))

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    root_logger.addHandler(stderr)


if __name__ == '__main__':
    main()
