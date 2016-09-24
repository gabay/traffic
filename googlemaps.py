#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import re
import json
import time
import requests

class Direction:
    URL = 'https://www.google.co.il/maps/dir/{source}/{destination}'
    DIRECTION_PARAMETER_RE = re.compile(r'cacheResponse\((.*)\)')

    def __init__(self, source, destination):
        self.source = source
        self.destination = destination
        self.url = self.URL.format(source=source, destination=destination)
        self.response = None
        self.timestamp = None

    def __str__(self):
        return 'Direction %s > %s' % (self.source, self.destination)

    def request(self):
        self.response = None
        self.timestamp = None

        try:
            response = requests.get(self.url)
            self.timestamp = int(time.time())

            assert response.status_code == 200, '[***] status code %d' % response.status_code

            match = self.DIRECTION_PARAMETER_RE.search(response.content)
            assert match is not None, '[***] no regex match, data: %s' % response.content

            self.response = json.loads(match.group(1))
            return self.response
        except Exception, e:
            sys.stderr.write('Error on %s - %s\n\n' % (self, e))
            raise

    @property
    def duration(self):
        if self.response is not None:
            try:
                duration = self.response[10][0][0][0][6][0][0]
                return duration
            except TypeError, e:
                print '[***] Duration extraction failed for URL %s' % self.url
                open(__file__ + '.debug.log', 'ab').write(self.response + '\n\n')
        return None
