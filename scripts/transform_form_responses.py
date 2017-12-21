#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import csv
import os
import arrow


# GLOBAL SETTINGS
cwd = os.path.dirname(__file__)
HEADER = ['id', 'timestamp', 'day', 'album', 'artist', 'points']
MAX_POINTS = 15
POLL_START_DAY = 4
POLL_END_DAY = 11


def run():
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
                points = MAX_POINTS - i
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
                        timestamp.day >= POLL_START_DAY and
                        timestamp.day <= POLL_END_DAY)):
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
    run()
