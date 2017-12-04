#!/usr/bin/env python
# -*- coding: utf-8 -*-
import csv
import os
import arrow


# GLOBAL SETTINGS
cwd = os.path.dirname(__file__)
INPUT_PATH = os.path.join(cwd, '../data')
INPUT_FILE = '2016_responses'
OUTPUT_PATH = os.path.join(cwd, '../output')
HEADER = ['id', 'timestamp', 'day', 'album_artist', 'ranking']
CSV_INDEX_MAP = {
    1: 5,
    2: 4,
    3: 3,
    4: 2,
    5: 1,
}


def run():
    """
    Parse allsongsconsidered form results and normalize it to be deduped.
    """

    # Create output files folder if needed
    if not os.path.exists(OUTPUT_PATH):
        os.makedirs(OUTPUT_PATH)

    rows = []
    with open('%s/%s_normalized.csv' % (OUTPUT_PATH, INPUT_FILE), 'w') as fo:
        writer = csv.writer(fo)
        writer.writerow(HEADER)
        with open('%s/%s.csv' % (INPUT_PATH, INPUT_FILE)) as fi:
            reader = csv.reader(fi)
            reader.next()
            for idx, row in enumerate(reader):
                timestamp = arrow.get(row[0], 'M/D/YYYY H:m:s')
                for k, v in CSV_INDEX_MAP.iteritems():
                    print type(row[k])
                    if row[k].strip() != '':
                        rows.append([idx+1, timestamp, timestamp.day, row[k].decode('utf-8').encode('ascii', 'ignore'), v])
            writer.writerows(rows)


if __name__ == '__main__':
    run()
