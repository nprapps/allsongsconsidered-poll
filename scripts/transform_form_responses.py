#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import sys
import csv
import os
import arrow


# GLOBAL SETTINGS
cwd = os.path.dirname(__file__)
HEADER = ['id', 'timestamp', 'album', 'artist', 'comment', 'points']


def run(args):
    """
    Parse allsongsconsidered form results and normalize it to be deduped.
    """
    # Format date arguments
    start_timestamp = arrow.get(args.poll_start_date, 'M/D/YYYY')
    end_timestamp = arrow.get(args.poll_end_date, 'M/D/YYYY')

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
            for i in range(args.max_submit):
                points = 1
                album = row[(3 * i) + 1]
                artist = row[(3 * i) + 2]
                comment = row[(3 * i) + 3]
                key = '-'.join([album.strip().lower(),
                                artist.strip().lower()])
                try:
                    cache[key]
                    continue
                except KeyError:
                    cache[key] = 1
                # Remove empty albums & adjust poll period
                if (album.strip() != '' and (
                        timestamp >= start_timestamp and
                        timestamp <= end_timestamp)):
                    form_rows.append([
                        idx,
                        timestamp,
                        album.decode('utf-8').encode('ascii',
                                                     'ignore'),
                        artist.decode('utf-8').encode('ascii',
                                                      'ignore'),
                        comment.decode('utf-8').encode('ascii',
                                                      'ignore'),
                        points
                    ])
            # Only include albums that have at least one entry
            if len(form_rows) >= 1:
                rows.extend(form_rows)

    writer.writerows(rows)


if __name__ == '__main__':
    # Parse command-line arguments.
    parser = argparse.ArgumentParser(
        description="Transform Form Responses for csvdedupe")
    parser.add_argument('--max_submit',
                        type=int,
                        help="Max number of items submitted in each response",
                        required=True)
    parser.add_argument('--poll_start_date',
                        type=str,
                        help="Date the poll started formatted as M/D/YYYY",
                        required=True)
    parser.add_argument('--poll_end_date',
                        type=str,
                        help="Date the poll ended formatted as M/D/YYYY",
                        required=True)
    args = parser.parse_args()
    run(args)
