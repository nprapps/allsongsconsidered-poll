#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import pandas as pd
import numpy as np

cwd = os.path.dirname(__file__)
INPUT_PATH = os.path.join(cwd, '../output')
INPUT_FILE1 = '2017_responses_more1_top100'
INPUT_FILE2 = '2017_responses_deduped_more1_refine_standard_ranked_intermediate_pivot'
TMP_PATH = os.path.join(cwd, '../output/intermediate')
OUTPUT_PATH = os.path.join(cwd, '../output')
OUTPUT_FILE = 'test'


def rank_entries():
    # Create output files folder if needed
    if not os.path.exists(TMP_PATH):
        os.makedirs(TMP_PATH)
    if not os.path.exists(OUTPUT_PATH):
        os.makedirs(OUTPUT_PATH)

    top100 = pd.read_csv("%s/%s.csv" % (INPUT_PATH, INPUT_FILE1))
    daily_pivot = pd.read_csv("%s/%s.csv" % (TMP_PATH, INPUT_FILE2))
    merged = top100.merge(daily_pivot, on='Cluster ID', how='left')
    clean = merged[['Cluster ID','album', 'artist',
                    '4', '5', '6', '7', '8', '9', '10', '11',
                    'agg_ranking', 'rank']]
    clean.to_csv("%s/%s_dailyreport.csv" % (OUTPUT_PATH, INPUT_FILE1), index=False)

if __name__ == '__main__':
    rank_entries()
