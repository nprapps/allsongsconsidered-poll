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
df_deduped = pd.read_csv('../output/2017_responses_deduped.csv',dtype = {'Cluster ID':str,'id':str,'day':str,'ranking':str})

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

# export merged dataframe to csv
temp = pd.merge(df_deduped, checked, how='outer', on='Cluster ID').sort_values('id')
temp['album'] = np.vectorize(checkAccuracy)(temp['album_x'],temp['album_y'])
temp['artist'] = np.vectorize(checkAccuracy)(temp['artist_x'],temp['artist_y'])

export = temp.drop(['album_x','artist_x','album_y','artist_y'],axis=1).to_csv('../output/2017_responses_clustered.csv',index=False)
