#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse
import itertools
import threading

import googlemaps

DEBUG = False

class DaemonThread(threading.Thread):
    def __init__(self, *args, **kwargs):
        super(DaemonThread, self).__init__(*args, **kwargs)
        self.daemon=True
        self.target = self._Thread__target


DIRECTIONS_GENERATION = {
    'mesh': lambda locations: [d for d in itertools.product(locations, locations) if d[0] != d[1]],
    'src_dst': lambda locations: [locations[i:i+2] for i in xrange(0, len(locations), 2)]
}

FORMATTERS = {
    'csv': lambda *items: ','.join(['"%s"' % s for s in items]),
    'text': lambda *items: '\t'.join(map(str, items)),
}

def main():
    parser = argparse.ArgumentParser()
    # generic parameters
    parser.add_argument('-p', '--parallel', help='Run requests in parallel', action='store_true', default=False)

    # locations generation
    parser.add_argument('location', nargs='*')
    parser.add_argument('-f', '--location-file', help='Location file, newline seperated')

    # directions generation
    direction_group = parser.add_mutually_exclusive_group(required=True)
    direction_group.add_argument('--mesh', dest='dir_generation', action='store_const', const='mesh',
                                help='Request directions between every 2 locations')
    direction_group.add_argument('--src-dst', dest='dir_generation', action='store_const', const='src_dst',
                                help='Request directions for locations 1->2, 3->4 etc')

    # output format
    parser.add_argument('-o', '--output-format', choices=['csv', 'text'], default='csv')

    args = parser.parse_args()

    directions_generator = DIRECTIONS_GENERATION[args.dir_generation]
    formatter = FORMATTERS[args.output_format]

    # generate the locations
    locations = args.location
    if args.location_file:
        locations.extend(filter(None, open(args.location_file, 'rb').read().splitlines()))
    assert len(locations) > 1, 'Not enough locations - got only %d' % len(locations)

    if DEBUG:
        print 'Locations:'
        for location in locations:
            print '\t', location

    # generate the directions
    directions = directions_generator(locations)
    directions = [googlemaps.Direction(src, dst) for src, dst in directions]

    if DEBUG:
        print 'Directions:'
        for direction in directions:
            print '\t', direction

    if args.parallel:
        tasks = [(direction, DaemonThread(target=direction.request)) for direction in directions]
        for direction, thread in tasks:
            thread.start()
        for direction, thread in tasks:
            thread.join()
            if direction.duration:
                print formatter(direction.timestamp, direction.source, direction.destination, direction.duration)
    else:
        for direction in directions:
            try:
                direction.request()
            except Exception, e:
                print e
            if direction.duration:
                print formatter(direction.timestamp, direction.source, direction.destination, direction.duration)

if __name__ == '__main__':
    main()
#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse
import itertools
import threading

import googlemaps

DEBUG = False

class DaemonThread(threading.Thread):
    def __init__(self, *args, **kwargs):
        super(DaemonThread, self).__init__(*args, **kwargs)
        self.daemon=True
        self.target = self._Thread__target


DIRECTIONS_GENERATION = {
    'mesh': lambda locations: [d for d in itertools.product(locations, locations) if d[0] != d[1]],
    'src_dst': lambda locations: [locations[i:i+2] for i in xrange(0, len(locations), 2)]
}

FORMATTERS = {
    'csv': lambda *items: '"%s"\n' % '","'.join(map(str, items)),
    'text': lambda *items: '\t'.join(map(str, items)),
}

def main():
    parser = argparse.ArgumentParser()
    # generic parameters
    parser.add_argument('-p', '--parallel', help='Run requests in parallel', action='store_true', default=False)

    # locations generation
    parser.add_argument('location', nargs='*')
    parser.add_argument('-f', '--location-file', help='Location file, newline seperated')

    # directions generation
    direction_group = parser.add_mutually_exclusive_group(required=True)
    direction_group.add_argument('--mesh', dest='dir_generation', action='store_const', const='mesh',
                                help='Request directions between every 2 locations')
    direction_group.add_argument('--src-dst', dest='dir_generation', action='store_const', const='src_dst',
                                help='Request directions for locations 1->2, 3->4 etc')

    # output format
    parser.add_argument('-o', '--output-format', choices=['csv', 'text'], default='csv')

    args = parser.parse_args()

    directions_generator = DIRECTIONS_GENERATION[args.dir_generation]
    formatter = FORMATTERS[args.output_format]

    # generate the locations
    locations = args.location
    if args.location_file:
        locations.extend(filter(None, open(args.location_file, 'rb').read().splitlines()))
    assert len(locations) > 1, 'Not enough locations - got only %d' % len(locations)

    if DEBUG:
        print 'Locations:'
        for location in locations:
            print '\t', location

    # generate the directions
    directions = directions_generator(locations)
    directions = [googlemaps.Direction(src, dst) for src, dst in directions]

    if DEBUG:
        print 'Directions:'
        for direction in directions:
            print '\t', direction

    if args.parallel:
        tasks = [(direction, DaemonThread(target=direction.request)) for direction in directions]
        for direction, thread in tasks:
            thread.start()
        for direction, thread in tasks:
            thread.join()
            if direction.duration:
                print formatter(direction.timestamp, direction.source, direction.destination, direction.duration)
    else:
        for direction in directions:
            try:
                direction.request()
            except Exception, e:
                print e
            if direction.duration:
                print formatter(direction.timestamp, direction.source, direction.destination, direction.duration)

if __name__ == '__main__':
    main()
