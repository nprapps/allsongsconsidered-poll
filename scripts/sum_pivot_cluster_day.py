#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import sys
import numpy as np
import pandas as pd


def run(args):
    data = pd.read_csv(sys.stdin)

    # Find maximum rank value and increase by one to use as a fill_value
    # on the pivot with cluster by day
    notfound_value = 200
    # grouped['rank'].max()+1

    # #create pivot table and fill non existing with high number i.e:200
    pivot_rank = pd.pivot_table(data,
                           values='rank',
                           index='Cluster ID',
                           columns=['day'],
                           fill_value=notfound_value,
                           aggfunc=np.sum)

    pivot_points = pd.pivot_table(data,
                                  values='points',
                                  index='Cluster ID',
                                  columns=['day'],
                                  fill_value=0,
                                  aggfunc=np.sum)


    # TODO: add argument that says which pivot table to do,
    # either sum by points or value and use the appropriate fill_value to pass

    # Write output
    pivot_points.to_csv(sys.stdout)


if __name__ == '__main__':
    # Parse command-line arguments.
    parser = argparse.ArgumentParser(
        description="Pivot table by cluster and day of the poll")
    parser.add_argument('--notfound_value',
                        type=int,
                        help="value to assign to N/A values on pivot table",
                        required=False)
    parser.add_argument('--novotes_value',
                        type=int,
                        help="value to assign to no votes on pivot table",
                        required=False)
    args = parser.parse_args()
    run(args)
