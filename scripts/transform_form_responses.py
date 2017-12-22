#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import sys
import csv
import os
import arrow


# GLOBAL SETTINGS
cwd = os.path.dirname(__file__)
HEADER = ['id', 'timestamp', 'day', 'album', 'artist', 'points']


def run(args):
    """
    Parse allsongsconsidered form results and normalize it to be deduped.
    """

    # Create output files folder if needed
    rows = []

    writer = csv.writer(sys.stdout)
    writer.writerow(HEADER)
    reader = csv.reader(sys.stdin)
    reader.next()
    for idx, row in enumerate(reader):
        # Use a small cache to remove duplicate
        # album-artist entries within a form response
        cache = {}
        form_rows = []
        if row[0] != '':
            timestamp = arrow.get(row[0], 'M/D/YYYY H:m:s')
            for i in range(5):
                points = args.max_points - i
                album = row[(2 * i) + 1]
                artist = row[(2 * i) + 2]
                key = '-'.join([album.strip().lower(),
                                artist.strip().lower()])
                try:
                    cache[key]
                    continue
                except KeyError:
                    cache[key] = 1
                # Remove empty albums & adjust poll period
                if (album.strip() != '' and (
                        timestamp.day >= args.poll_start_day and
                        timestamp.day <= args.poll_end_day)):
                    form_rows.append([
                        idx,
                        timestamp,
                        timestamp.day,
                        album.decode('utf-8').encode('ascii',
                                                     'ignore'),
                        artist.decode('utf-8').encode('ascii',
                                                      'ignore'),
                        points
                    ])
            # Only include albums that have more than one entry
            if len(form_rows) > 1:
                rows.extend(form_rows)

    writer.writerows(rows)


if __name__ == '__main__':
    # Parse command-line arguments.
    parser = argparse.ArgumentParser(
        description="Transform Form Responss for csvdedupe")
    parser.add_argument('--max_points',
                        type=int,
                        help="maximum points assigned to first album (>=5)",
                        required=True)
    parser.add_argument('--poll_start_day',
                        type=int,
                        help="Day where the poll has started",
                        required=True)
    parser.add_argument('--poll_end_day',
                        type=int,
                        help="Day where the poll has ended",
                        required=True)
    args = parser.parse_args()
    run(args)
