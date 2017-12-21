#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import numpy as np
import pandas as pd

# Global variables & constants
NOTFOUND_VALUE = 200


def run():
    data = pd.read_csv(sys.stdin)

    # Find maximum rank value and increase by one to use as a fill_value
    # on the pivot with cluster by day
    # notfound_value = grouped['rank'].max()+1

    # #create pivot table and fill non existing with high number i.e:200
    pivot = pd.pivot_table(data,
                           values='rank',
                           index='Cluster ID',
                           columns=['day'],
                           fill_value=NOTFOUND_VALUE,
                           aggfunc=np.sum)

    # Write output
    pivot.to_csv(sys.stdout)


if __name__ == '__main__':
    run()
