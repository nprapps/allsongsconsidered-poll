#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import pandas as pd

# TODO: pass ascending as optional variable for weighting vs points

def run():

    data = pd.read_csv(sys.stdin)

    # Sort by aggregated ranking
    data.sort_values('agg_ranking', inplace=True)
    # data.sort_values('total_points', inplace=True, ascending=False)

    # create final ranking
    data['rank'] = data["agg_ranking"].rank(
        method='dense').astype(int)
    # data['rank'] = data["total_points"].rank(
        # method='dense').astype(int)

    data.to_csv(sys.stdout, index=False)


if __name__ == '__main__':
    run()
