#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import json
import time
import requests
import urllib3
urllib3.disable_warnings()

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
        
        response = requests.get(self.url)
        self.timestamp = int(time.time())
        
        assert response.status_code == 200, '[***] status code %d on URL %s' % (response.status_code, self.url)

        match = self.DIRECTION_PARAMETER_RE.search(response.content)
        assert match is not None, '[***] no regex match on URL %s' % self.url
        
        try:
            self.response = json.loads(match.group(1))
        except ValueError:
            raise ValueError('[***] JSON loading failed on URL %s' % self.url)
            
        return self.response

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
