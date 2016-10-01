#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import re
import json
import time
import traceback
import requests
requests.packages.urllib3.disable_warnings()

class Direction:
    URL = 'https://www.google.co.il/maps/dir/{source}/{destination}'
    DIRECTION_PARAMETER_RE = re.compile(r'cacheResponse\((.*)\)')

    def __init__(self, source, destination):
        self.source = source
        self.destination = destination
        self.url = self.URL.format(source=source, destination=destination)
        self.response = None
        self.duration = None
        self.timestamp = None
        self.error = None

    def __str__(self):
        return 'Direction %s > %s' % (self.source, self.destination)

    def request(self):
        self.response = None
        self.timestamp = None

        try:
            response = requests.get(self.url)
            self.timestamp = int(time.time())

            assert response.status_code == 200, 'Status code %d' % response.status_code

            match = self.DIRECTION_PARAMETER_RE.search(response.content)
            assert match is not None, 'Regex not matched, data: %s' % response.content

            self.response = json.loads(match.group(1))
            self.duration = int(self.response[10][0][0][0][6][0][0])
            return self.response
        except Exception, e:
            self.error = traceback.format_exc()
            raise
