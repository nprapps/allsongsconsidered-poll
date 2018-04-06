#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import pandas as pd

# TODO: pass ascending as optional variable for weighting vs points

def run():

    data = pd.read_csv(sys.stdin)

    # # Sort by points
    # data.sort_values('total_points', inplace=True, ascending=False)
    #
    # # create first ranking
    # data['rank_points'] = data['total_points'].rank(
    #     method='first').astype(int)

    # Sort by aggregated ranking
    data.sort_values('agg_ranking', inplace=True)

    # create first ranking
    data['rank'] = data['agg_ranking'].rank(
        method='dense').astype(int)

    data.sort_values('agg_ranking_norm', inplace=True)

    data['rank_norm'] = data['agg_ranking_norm'].rank(
        method='dense').astype(int)

    output = data[['Cluster ID','album','artist','total_points','agg_ranking','rank','agg_ranking_norm','rank_norm']]

    output.to_csv(sys.stdout, index=False)


if __name__ == '__main__':
    run()
