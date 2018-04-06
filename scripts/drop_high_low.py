#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import pandas as pd

# TODO: send ascending as a variable, add variable for weighted
# vs. unweighted rank and use ranked/total variable as it makes sense

def run():
    data = pd.read_csv(sys.stdin, index_col=['Cluster ID'])

    # Sum only day columns
    data['sum'] = data[['1','2','21','22','23','24','25','26','27','28','29','30','31']].sum(axis=1)

    # Find max and min only out of day columns
    data['max'] = data[['1','2','21','22','23','24','25','26','27','28','29','30','31']].max(axis=1)
    data['min'] = data[['1','2','21','22','23','24','25','26','27','28','29','30','31']].min(axis=1)

    # Do calcuations
    data['agg_ranking_norm'] = data['sum'] - data['max'] - data['min']

    output = data[['agg_ranking_norm']]

    # Write output
    output.to_csv(sys.stdout, index_label='Cluster ID')


if __name__ == '__main__':
    run()
