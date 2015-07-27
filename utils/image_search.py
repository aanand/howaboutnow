from __future__ import unicode_literals

import re
import os

import logging
log = logging.getLogger(__name__)

from apiclient.discovery import build

from utils.constants import (
    MAX_FRAMES_THEN,
    MAX_FRAMES_NOW,
)

GOOGLE_API_KEY = os.environ['GOOGLE_API_KEY']
GOOGLE_CSE_ID = os.environ['GOOGLE_CSE_ID']

service = build('customsearch', 'v1', developerKey=GOOGLE_API_KEY)


def search(query):
    old_query = 'old {}'.format(query)
    young_query = 'young {}'.format(query)

    old = get_response(q='"{}"'.format(old_query))
    young = get_response(q='"{}"'.format(young_query))

    if query == 'drake':
        # Special-case Drake because 'old drake' is a meme
        then = young
    else:
        then = max([old, young], key=lambda r: r.total_results())

    log.info("old: {} results".format(old.total_results()))
    log.info("young: {} results".format(young.total_results()))
    log.info('using {}'.format(then.query()['searchTerms']))

    now = get_response(
        q="2014 OR 2015",
        exactTerms=query,
    )
    log.info("now: {} results".format(now.total_results()))

    return then.items(), now.items()

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


def get_response(**kwargs):
    return Request(
        service.cse(),
        'list',
        cx=GOOGLE_CSE_ID,
        searchType='image',
        **kwargs
    )


class Request(object):
    def __init__(self, resource, method, *args, **kwargs):
        self._resource = resource
        self._method = method
        self._args = args
        self._kwargs = kwargs

        self._responses_iterator = None

    def total_results(self):
        for r in self.responses():
            return int(r['searchInformation']['totalResults'])

    def query(self):
        for r in self.responses():
            return r['queries']['request'][0]

    def responses(self):
        from itertools import tee
        a, b = tee(self._responses_iterator or self._responses())
        self._responses_iterator = b
        return a

    def items(self):
        for response in self.responses():
            for item in response.get('items', []):
                yield item

    def _responses(self):
        request = self._request()
        while request is not None:
            response = request.execute()
            yield response

            if hasattr(self._resource, 'list_next'):
                request = self._resource.list_next(request, response)
            else:
                request = None

    def _request(self):
        return getattr(self._resource, self._method)(*self._args, **self._kwargs)

def debug_items(items):
    for item in items:
        log.info(guess_year(item))
        log.info(page_url(item))
        log.info(image_url(item))
        log.info('')
