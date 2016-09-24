#!/usr/bin/python

import os
import sys
import csv
from datetime import datetime
import pygal

def parse_csv(path, filter_src=None, filter_dst=None):
    lines = {}
    for line in csv.reader(open(path, 'rb')):
        try:
            timestamp, src, dst, duration = line
        except:
            sys.stdout.write('Error parsing line %s\n\n' % line)
            continue
        if filter_src and filter_src not in src.lower():
            continue
        if filter_dst and filter_dst not in dst.lower():
            continue
        timestamp = datetime.fromtimestamp(int(timestamp))
        duration = int(duration)
        lines.setdefault((src, dst), []).append((timestamp, duration))
    return lines

def int_to_time(i):
    i = int(i)
    result = []
    hours, minutes = divmod(i / 60, 60)
    if hours > 0:
        result.append('%d Hours' % hours)
    if minutes > 0:
        result.append('%d Minutes' % minutes)
    return ' '.join(result)

def main(*args):
    csv_path = args[0] if len(args) > 0 else 'traffic.csv'
    filter_src = args[1].lower() if len(args) > 1 else None
    filter_dst = args[2].lower() if len(args) > 2 else None

    lines = parse_csv(csv_path, filter_src, filter_dst)

    plot = pygal.DateTimeLine(x_label_rotation=35, x_value_formatter=lambda dt: dt.strftime('%d.%m.%y %H:%M:%S'), value_formatter=int_to_time)
    for src_dst, values in lines.items():
        src, dst = src_dst
        plot.add('%s -> %s' % (src, dst), values)

    plot.render_in_browser()


if __name__ == '__main__':
    main(*sys.argv[1:])
