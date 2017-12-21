#!/usr/bin/env python
# -*- coding: utf-8 -*-
import csv
import sys
import operator


def run():
    """
    Parse allsongsconsidered form results and remove duplicate entries
    within a time window defined in DUPLICATE_TIME_THRESHOLD
    """

    cache = {}
    standard = {}
    reader = csv.DictReader(sys.stdin)
    writer = csv.DictWriter(sys.stdout, fieldnames=reader.fieldnames)
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
