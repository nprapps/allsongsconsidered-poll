#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import pandas as pd
import numpy as np

cwd = os.path.dirname(__file__)
INPUT_PATH = os.path.join(cwd, '../output')
INPUT_FILE = '2017_responses_deduped_standard'
TMP_PATH = os.path.join(cwd, '../output/intermediate')
OUTPUT_PATH = os.path.join(cwd, '../output')
OUTPUT_FILE = '2017_responses_top100'


def rank_entries():
    # Create output files folder if needed
    if not os.path.exists(TMP_PATH):
        os.makedirs(TMP_PATH)
    if not os.path.exists(OUTPUT_PATH):
        os.makedirs(OUTPUT_PATH)

    data = pd.read_csv("%s/%s.csv" % (INPUT_PATH, INPUT_FILE))
    # Calculate sum of points by day and dedupe cluster
    grouped = data.groupby(['day', 'Cluster ID'], as_index=False)['points'].sum()
    # Add a rank column per day in descending order as an integer
    grouped['rank'] = grouped.groupby(["day"])["points"].rank(
        method='dense', ascending=False).astype(int)

    # Find maximum rank value and increase by one to use as a fill_value
    # on the pivot with cluster by day
    notfound_value = grouped['rank'].max()+1
    grouped.to_csv("%s/%s_ranked_intermediate_grouped.csv" % (TMP_PATH, INPUT_FILE), index=False)
    #create pivot table and fill non existing with high number i.e:100
    pivot = pd.pivot_table(grouped,
                           values='rank',
                           index='Cluster ID',
                           columns=['day'],
                           fill_value=notfound_value,
                           aggfunc=np.sum)

    pivot.to_csv("%s/%s_ranked_intermediate_pivot.csv" % (TMP_PATH, INPUT_FILE))
    # Aggregate the ranking per day for all the poll period and sort
    agg = pivot.sum(axis=1).sort_values()
    # Series to Dataframe to assign column name
    ranked = pd.DataFrame(agg, columns=['agg_ranking'])
    ranked.to_csv("%s/%s_ranked_intermediate_agg.csv" % (TMP_PATH, INPUT_FILE))
    # join with original data to bring album and artist
    joined = data.join(ranked, on='Cluster ID')
    joined.to_csv("%s/%s_ranked_intermediate_joined.csv" % (TMP_PATH, INPUT_FILE), index=False)
    # Drop duplicates by Cluster ID
    clean = joined[['Cluster ID','album', 'artist', 'agg_ranking']]

    nodups = clean.drop_duplicates(['Cluster ID']).sort_values('agg_ranking')
    nodups['rank'] = nodups["agg_ranking"].rank(
        method='dense').astype(int)

    final = nodups[['album', 'artist', 'agg_ranking', 'rank']].head(100)
    # Ouput to csv
    final.to_csv("%s/%s.csv" % (OUTPUT_PATH, OUTPUT_FILE), index=False)
    print 'Done.'


if __name__ == '__main__':
    rank_entries()
