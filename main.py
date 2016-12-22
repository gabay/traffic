#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import struct
import argparse
import itertools
import traceback

import googlemaps


DIRECTIONS_GENERATION = {
    'mesh': lambda locations: [d for d in itertools.product(locations, locations) if d[0] != d[1]],
    'src_dst': lambda locations: [locations[i:i+2] for i in xrange(0, len(locations), 2)]
}

class Outputter:
    def __init__(self, output_directory):
        self.output_directory = output_directory
        if not os.path.isdir(self.output_directory):
            os.makedirs(self.output_directory)

    def write(self, filename, data):
        with open(os.path.join(self.output_directory, filename), 'ab') as out:
            out.write(data)

def is_location(line):
    return line != '' and line[0] != '#'


def main():
    parser = argparse.ArgumentParser()
    # generic parameters
    #parser.add_argument('-p', '--parallel', help='Run requests in parallel', action='store_true', default=False)
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
    parser.add_argument('-d', '--output-directory', default='durations')

    args = parser.parse_args()

    directions_generator = DIRECTIONS_GENERATION[args.dir_generation]
    out = Outputter(args.output_directory)

    # generate the locations
    locations = args.location
    if args.location_file:
        locations.extend(filter(is_location, open(args.location_file, 'rb').read().splitlines()))
    assert len(locations) > 1, 'Not enough locations - got %d' % len(locations)

    # generate the directions
    directions = [googlemaps.Direction(src, dst) for src, dst in directions_generator(locations)]

    for direction in directions:
        try:
            direction.request()
            filename = '%s_%s.txt' % (direction.source, direction.destination)
            data = struct.pack('>LH', direction.timestamp, direction.duration)
        except Exception, e:
            filename = 'errors.txt'
            data = traceback.format_exc() + '\n'
        out.write(filename, data)


if __name__ == '__main__':
    main()
