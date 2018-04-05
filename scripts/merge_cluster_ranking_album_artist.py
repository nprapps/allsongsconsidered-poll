#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import pandas as pd
import argparse

# TODO: pass variable for which header to use depending on sum versus weighted rank

def run(raw, ranked):

    raw_data = pd.read_csv(raw)
    ranked = pd.read_csv(ranked)

    # merge with original data to bring album and artist
    merged = raw_data.merge(ranked, on='Cluster ID', how='left')
    # Drop duplicates by Cluster ID
    # clean = merged[['Cluster ID', 'album', 'artist', 'agg_ranking']]
    clean = merged[['Cluster ID', 'album', 'artist', 'total_points']]
    clean = clean.drop_duplicates(['Cluster ID'])
    clean.to_csv(sys.stdout, index=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'paths', metavar='PATHS', nargs='+', help='')
    args = parser.parse_args()
    run(args.paths[0], args.paths[1])
