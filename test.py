import sys
from utils import start_logging, make_video

start_logging()

query = sys.argv[1]
filename = make_video(query)
print("Wrote {}".format(filename))
