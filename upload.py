import sys
import os

import tweepy

from utils import (
    start_logging,
    upload_media,
)

import logging
log = logging.getLogger(__name__)

start_logging()

auth = tweepy.OAuthHandler(os.environ['TWITTER_CONSUMER_KEY'], os.environ['TWITTER_CONSUMER_SECRET'])
auth.set_access_token(os.environ['TWITTER_ACCESS_TOKEN'], os.environ['TWITTER_ACCESS_TOKEN_SECRET'])
api = tweepy.API(auth)

media_id = upload_media(api, sys.argv[1])
log.info('media_id = %s', media_id)
