#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import re
import json
import time
import requests
requests.packages.urllib3.disable_warnings()

class Direction:
    URL = 'https://www.google.co.il/maps/dir/{source}/{destination}'
    DIRECTION_PARAMETER_RE = re.compile(r'cacheResponse\((.*)\)')

    def __init__(self, source, destination):
        self.source = source
        self.destination = destination
        self.response = None
        self.timestamp = None

    def __str__(self):
        return 'Direction %s > %s' % (self.source, self.destination)

    @property
    def timestamp(self):
        if self.response is None: self.request()
        return self.timestamp

    @property
    def duration(self):
        if self.response is None: self.request()
        return int(self.response[10][0][0][0][6][0][0])

    def request(self):
        url = self.URL.format(source=self.source, destination=self.destination)
        response = requests.get(url)
        self.timestamp = int(time.time())

        assert response.status_code == 200, 'Status code %d' % response.status_code

        match = self.DIRECTION_PARAMETER_RE.search(response.content)
        assert match is not None, 'Regex not matched, data: %s' % response.content

        self.response = json.loads(match.group(1))
        return self.response
