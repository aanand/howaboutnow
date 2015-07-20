import re
import os

import logging
log = logging.getLogger(__name__)

from apiclient.discovery import build

GOOGLE_API_KEY = os.environ['GOOGLE_API_KEY']
GOOGLE_CSE_ID = os.environ['GOOGLE_CSE_ID']

service = build('customsearch', 'v1', developerKey=GOOGLE_API_KEY)


def search(query, from_year, to_year):
    results = get_results(
        query=query,
        from_date='{}0101'.format(from_year),
        to_date='{}1231'.format(to_year-1),
    )

    items = [
        item for item in results
        if guess_year(item) in range(from_year, to_year)
    ]

    return sorted(items, key=guess_year)


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


def get_results(query, from_date=None, to_date=None):
    sort = None
    if from_date and to_date:
        sort = 'date:r:{}:{}'.format(from_date, to_date)

    return service.cse().list(
        q=query,
        cx=GOOGLE_CSE_ID,
        searchType='image',
        sort=sort,
    ).execute()['items']


def debug_items(items):
    for item in items:
        log.info(guess_year(item))
        log.info(page_url(item))
        log.info(image_url(item))
        log.info('')
