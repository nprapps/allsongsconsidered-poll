#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import pandas as pd
import argparse

# TODO: pass variable for which header to use depending on sum versus weighted rank

def run(raw, ranked, points, highlow):

    raw_data = pd.read_csv(raw)
    ranked = pd.read_csv(ranked)
    points = pd.read_csv(points)
    highlow = pd.read_csv(highlow)

    # merge ranked and highlow
    rank_merge = ranked.merge(highlow, on='Cluster ID', how='left')

    # merge points and rank
    points_ranked = points.merge(rank_merge, on='Cluster ID', how='left')

    # merge with original data to bring album and artist
    merged = points_ranked.merge(raw_data, on='Cluster ID', how='left')

    # Drop duplicates by Cluster ID
    clean = merged[['Cluster ID', 'album', 'artist', 'total_points', 'agg_ranking', 'agg_ranking_norm']]

    clean = clean.drop_duplicates(['Cluster ID'])
    clean.to_csv(sys.stdout, index=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'paths', metavar='PATHS', nargs='+', help='')
    args = parser.parse_args()
    run(args.paths[0], args.paths[1], args.paths[2], args.paths[3])
