#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np

def checkAccuracy(x, y):
    try:
        float(y)
        return x
    except:
        return y

# Import csvs
df_nprmusic = pd.read_csv('../data/nprmusic_top200.csv')
df_deduped = pd.read_csv('../output/2017_responses_deduped.csv',dtype = {'Cluster ID':str,'id':np.int64,'day':str,'ranking':str})
print(df_deduped)

# group deduped csv by cluster id and drop excess rows
cluster_groups = df_deduped.groupby(['Cluster ID','album','artist']).count().reset_index()
cluster_groups = cluster_groups.drop(['id','timestamp','day','ranking'], axis=1)

# assign true variable to nprmusic data
musictop200 = df_nprmusic
musictop200['checked'] = True

# merge
merged = pd.merge(cluster_groups, df_nprmusic, how='outer', on=['album','artist'])
checked = merged[merged['checked'] == True].drop_duplicates(subset=['album','artist'], keep='first')

# drop checked column
checked = checked.drop(['checked'],axis=1)

# merge dedupe and checked dfs on cluster id
deduped_clusters = pd.merge(df_deduped, checked, how='outer', on='Cluster ID').sort_values('id')
deduped_clusters['album'] = np.vectorize(checkAccuracy)(deduped_clusters['album_x'],deduped_clusters['album_y'])
deduped_clusters['artist'] = np.vectorize(checkAccuracy)(deduped_clusters['artist_x'],deduped_clusters['artist_y'])

# drop extra album/artist columns and rows with more then 3 nan
export = deduped_clusters.drop(['album_x','artist_x','album_y','artist_y'],axis=1).dropna(thresh=3)
export.to_csv('../output/2017_responses_clustered.csv',index=False)
