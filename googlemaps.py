#!/usr/bin/python
# -*- coding: utf-8 -*-

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
        
        response = requests.get(self.url)
        self.timestamp = int(time.time())
        
        if response.status_code != 200:
            print '[***] status code %d on URL %s' % (response.status_code, self.url)
            return
        match = self.DIRECTION_PARAMETER_RE.search(response.content)
        if not match:
            print '[***] no regex match on URL %s' % self.url
            return
        try:
            self.response = json.loads(match.group(1))
        except ValueError:
            print '[***] JSON loading failed on URL %s' % self.url
        return self.response

    @property
    def duration(self):
        if self.response is not None:
            try:
                duration = self.response[10][0][0][0][6][0][0]
                return duration
            except TypeError, e:
                print '[***] Duration extraction failed for URL %s' % self.url
        return None
