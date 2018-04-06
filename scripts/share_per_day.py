#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import numpy as np
import pandas as pd


def run():
    data = pd.read_csv(sys.stdin)

    # sum total votes per day
    data.loc['total'] = data.sum()

    data_index = data['Cluster ID']
    data_other = data.drop(data.columns[0], axis=1)

    # divide an album's votes for a given day by the sum for that day
    data_other = data_other.div(data_other.loc['total'], axis=1)
    data_other = data_other * 100000
    data_other = data_other.astype('int')

    share_data = pd.DataFrame(data=data_index)
    share_data = share_data.merge(data_other, left_index=True, right_index=True)

    # Write output
    share_data.to_csv(sys.stdout)


if __name__ == '__main__':
    run()
