#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import pandas as pd

# TODO: send ascending as a variable, add variable for weighted
# vs. unweighted rank and use ranked/total variable as it makes sense

def run():
    data = pd.read_csv(sys.stdin, index_col=['Cluster ID'])
    # Aggregate the points per day for all the poll period and sort
    agg = data.sum(axis=1).sort_values(ascending=True)

    # Series to Dataframe to assign column name
    ranked = pd.DataFrame(agg, columns=['agg_ranking'])
    total = pd.DataFrame(agg, columns=['total_points'])

    # Write output
    ranked.to_csv(sys.stdout, index_label='Cluster ID')


if __name__ == '__main__':
    run()
