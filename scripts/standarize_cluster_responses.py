#!/usr/bin/env python
# -*- coding: utf-8 -*-
import csv
import os
import arrow
import operator

# GLOBAL SETTINGS
cwd = os.path.dirname(__file__)
INPUT_PATH = os.path.join(cwd, '../output')
INPUT_FILE = '2017_responses_deduped_all_refine'
OUTPUT_PATH = os.path.join(cwd, '../output')

def run():
    """
    Parse allsongsconsidered form results and remove duplicate entries
    within a time window defined in DUPLICATE_TIME_THRESHOLD
    """

    # Create output files folder if needed
    if not os.path.exists(OUTPUT_PATH):
        os.makedirs(OUTPUT_PATH)

    cache = {}
    standard = {}
    with open('%s/%s.csv' % (INPUT_PATH, INPUT_FILE)) as fi:
        reader = csv.DictReader(fi)
        with open('%s/%s_standard.csv' % (OUTPUT_PATH, INPUT_FILE), 'w') as fo:
            writer = csv.DictWriter(fo, fieldnames=reader.fieldnames)
            writer.writeheader()
            rows = list(reader)
            for row in rows:
                key = "%s|%s" % (row['album'], row['artist'])
                try:
                    cluster = cache[row['Cluster ID']]
                    try:
                        cluster[key] += 1
                    except KeyError:
                        cluster[key] = 1
                except KeyError:
                    cache[row['Cluster ID']] = {key: 1}
            # Get key with maximum value via https://stackoverflow.com/questions/268272/getting-key-with-maximum-value-in-dictionary
            for cluster in cache:
                standard[cluster] = max(cache[cluster].iteritems(),
                                        key=operator.itemgetter(1))[0]
            # replace artist and album with most used one in cluster
            for row in rows:
                row['album'], row['artist'] = standard[
                    row['Cluster ID']].split('|')
                writer.writerow(row)




if __name__ == '__main__':
    run()
