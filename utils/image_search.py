import re
import os

import logging
log = logging.getLogger(__name__)

from apiclient.discovery import build

GOOGLE_API_KEY = os.environ['GOOGLE_API_KEY']
GOOGLE_CSE_ID = os.environ['GOOGLE_CSE_ID']

service = build('customsearch', 'v1', developerKey=GOOGLE_API_KEY)


def search(query):
    old = get_response('"old {}"'.format(query))
    young = get_response('"young {}"'.format(query))
    then = max([old, young], key=total_results)

    now = get_response('"{}"'.format(query))

    log.info("old: {} results".format(total_results(old)))
    log.info("young: {} results".format(total_results(young)))
    log.info("now: {} results".format(total_results(now)))

    return then['items'], now['items']

def total_results(response):
    return int(response['searchInformation']['totalResults'])


def page_url(item):
    return item['image']['contextLink']


def image_url(item):
    return item['link']


def image_mime_type(item):
    return item['mime']


def guess_year(item):
    # Grab all strings of 4 or more digits out of image + page URL
    number_strings = [
        num
        for field in [page_url(item), image_url(item)]
        for num in re.findall(r'\d{4,}', field)
    ]

    # Prioritise shorter, i.e. 4-digit, sequences
    number_strings = sorted(number_strings, key=len)

    # Find sequences where the first 4 digits look like a year
    numbers = [int(num[:4]) for num in number_strings]
    numbers = [num for num in numbers if num in range(2000, 2020)]

    return numbers[0] if numbers else None


def get_response(query):
    return service.cse().list(
        q=query,
        cx=GOOGLE_CSE_ID,
        searchType='image',
    ).execute()


def debug_items(items):
    for item in items:
        log.info(page_url(item))
        log.info(image_url(item))
        log.info('')
