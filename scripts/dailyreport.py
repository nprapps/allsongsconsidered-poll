#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import pandas as pd
import argparse


def run(top100, pivot):

    top100 = pd.read_csv(top100)
    pivot = pd.read_csv(pivot)

    # merge with original data to bring album and artist
    merged = top100.merge(pivot, on='Cluster ID', how='left')

    # keep pivot columns
    columns = list(pivot.columns.values)
    # Add desired columns from top100
    columns.extend(['album', 'artist', 'agg_ranking', 'rank'])
    clean = merged[columns]
    clean.to_csv(sys.stdout, index=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'paths', metavar='PATHS', nargs='+', help='')
    args = parser.parse_args()
    run(args.paths[0], args.paths[1])
