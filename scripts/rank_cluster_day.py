#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import pandas as pd


def run():
    data = pd.read_csv(sys.stdin)

    # Calculate sum of points by day and dedupe cluster
    grouped = data.groupby(['day', 'Cluster ID'],
                           as_index=False)['points'].sum()

    # Add a rank column per day in descending order as an integer
    grouped['rank'] = grouped.groupby(["day"])["points"].rank(
        method='dense', ascending=False).astype(int)

    # Write output
    grouped.to_csv(sys.stdout, index=False)


if __name__ == '__main__':
    run()
