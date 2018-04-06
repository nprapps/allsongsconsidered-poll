#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import numpy as np
import pandas as pd


def run():
    data = pd.read_csv(sys.stdin)

    # data_noid = data.drop('Cluster ID', axis=1)
    # clipped_data = data.clip(data.quantile(0), data.quantile(0.95), axis=0)
    # clipped_data = data.clip(0, 5, axis=0)

    # clipped_data = data.apply(lambda row: row.clip(row.quantile([0, 0.95]).values), axis=1)

    # clipped_data = data.clip(data.drop('Cluster ID', axis=1).quantile(0), data.drop('Cluster ID', axis=1).quantile(0.95), axis=0)
    data_index = data['Cluster ID']
    data_other = data.drop(data.columns[:2], axis=1)

    data_other = data_other.clip(0, data_other.quantile(0.95, axis=1), axis=0)
    data_other = data_other.astype('int')

    clipped_data = pd.DataFrame(data=data_index)
    clipped_data = clipped_data.merge(data_other, left_index=True, right_index=True)

    # clipped_data = data_other

    # Write output
    clipped_data.to_csv(sys.stdout)


if __name__ == '__main__':
    run()
