#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import pandas as pd


def run():
    data = pd.read_csv(sys.stdin, index_col=['Cluster ID'])
    # Aggregate the ranking per day for all the poll period and sort
    agg = data.sum(axis=1).sort_values()

    # Series to Dataframe to assign column name
    ranked = pd.DataFrame(agg, columns=['agg_ranking'])

    # Write output
    ranked.to_csv(sys.stdout, index_label='Cluster ID')


if __name__ == '__main__':
    run()
