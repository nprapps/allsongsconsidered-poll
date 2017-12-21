#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import pandas as pd


def run():

    data = pd.read_csv(sys.stdin)

    # Sort by aggregated ranking
    data.sort_values('agg_ranking', inplace=True)
    # create final ranking
    data['rank'] = data["agg_ranking"].rank(
        method='dense').astype(int)

    data.to_csv(sys.stdout, index=False)


if __name__ == '__main__':
    run()
