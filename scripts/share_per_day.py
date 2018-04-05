#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import numpy as np
import pandas as pd


def run():
    data = pd.read_csv(sys.stdin)

    # sum total votes per day
    data.loc['total'] = data.sum()

    # divide an album's votes for a given day by the sum for that day
    share_df = data.div(data.loc['total'], axis=1)
    share_df = share_df * 100000
    share_df = share_df.astype('int')

    # Write output
    share_df.to_csv(sys.stdout)


if __name__ == '__main__':
    run()
