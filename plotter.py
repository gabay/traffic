#!/usr/bin/python

import os
import sys
import glob
import struct
from datetime import datetime
import pygal

def parse_durations(path):
    deserializer = struct.Struct('>LH')
    data = []
    f = open(path, 'rb')
    while True:
        raw_data = f.read(deserializer.size)
        if len(raw_data) < deserializer.size:
            break
        timestamp, duration = deserializer.unpack(raw_data)
        dt = datetime.fromtimestamp(timestamp)
        data.append((dt, duration))
    f.close()
    return data

def datetime_to_str(dt):
    return dt.strftime('%d.%m.%y %H:%M:%S')

def int_to_time(i):
    result = []
    hours, minutes = divmod(i / 60, 60)
    if hours > 0:
        result.append('%d Hours' % hours)
    if minutes > 0:
        result.append('%d Minutes' % minutes)
    return ' '.join(result)

def main(*args):
    duration_directory = args[0] if len(args) > 0 else 'duration'
    filter_src = args[1].lower() if len(args) > 1 else None
    filter_dst = args[2].lower() if len(args) > 2 else None

    lines = []
    for path in sorted(glob.glob(os.path.join(duration_directory, '*_*.txt'))):
        src, dst = os.path.splitext(os.path.basename(path))[0].split('_')
        if (filter_src and filter_src not in src.lower()) or (filter_dst and filter_dst not in dst.lower()):
            continue
        lines.append((src, dst, parse_durations(path)))

    plot = pygal.DateTimeLine(x_label_rotation=35, x_value_formatter=datetime_to_str , value_formatter=int_to_time)
    for src, dst, values in lines:
        plot.add('%s -> %s' % (src, dst), values)

    plot.render_in_browser()


if __name__ == '__main__':
    main(*sys.argv[1:])
