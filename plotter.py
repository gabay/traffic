#!/usr/bin/python

import os
import sys
import glob
import struct
import argparse
from datetime import datetime
import pygal

def parse_durations(path):
    deserializer = struct.Struct('>LH')
    data = []
    with open(path, 'rb') as f:
        while True:
            raw_data = f.read(deserializer.size)
            if len(raw_data) < deserializer.size:
                break
            timestamp, duration = deserializer.unpack(raw_data)
            data.append((timestamp, duration))
    return data

def summarize_durations(durations):
    SECONDS_PER_WEEK = 60*60*24*7
    SECONDS_PER_BUCKET = 120
    BUCKETS_PER_WEEK = SECONDS_PER_WEEK / SECONDS_PER_BUCKET

    # sort the data into buckets based on their time of the week
    buckets = [[] for i in xrange(BUCKETS_PER_WEEK)]
    for timestamp, duration in durations:
        # epoch was a thursday - add 3 days so first day will be sunday
        seconds = (timestamp + (0*86400)) % SECONDS_PER_WEEK
        buckets[seconds / SECONDS_PER_BUCKET].append(duration)

    bucket_time = lambda index: (index * SECONDS_PER_BUCKET) + SECONDS_PER_BUCKET
    average = lambda items: sum(items) / len(items)
    summarized = [(bucket_time(index), average(durations)) for index, durations in enumerate(buckets) if len(durations) > 0]
    return summarized

def datetime_to_str(dt):
    return dt.strftime('%A %H:%M:%S')

def int_to_time(i):
    result = []
    hours, minutes = divmod(i / 60, 60)
    if hours > 0:
        result.append('%d Hours' % hours)
    if minutes > 0:
        result.append('%d Minutes' % minutes)
    return ' '.join(result)

def main(*args):
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--src')
    parser.add_argument('-d', '--dst')
    parser.add_argument('--directory', default='durations')
    args = parser.parse_args()

    lines = []
    for path in sorted(glob.glob(os.path.join(args.directory, '*_*.txt'))):
        src, dst = os.path.splitext(os.path.basename(path))[0].split('_')
        if (args.src and args.src not in src.lower()) or (args.dst and args.dst not in dst.lower()):
            continue
        lines.append((src, dst, parse_durations(path)))

    plot = pygal.DateTimeLine(x_label_rotation=35, x_value_formatter=datetime_to_str , value_formatter=int_to_time)
    for src, dst, durations in lines:
        durations = summarize_durations(durations)
        plot.add('%s -> %s' % (src, dst), durations)

    plot.render_in_browser()


if __name__ == '__main__':
    main(*sys.argv[1:])
