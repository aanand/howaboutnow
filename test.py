import sys
from utils import start_logging, make_video

start_logging()

query = sys.argv[1]
make_video(query)
