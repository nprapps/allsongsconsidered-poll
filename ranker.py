import pandas as pd
import numpy as np

RANKS = ["Rank 1", "Rank 2", "Rank 3", "Rank 4", "Rank 5"]

point_value = {
    'Rank.1': 3,
    'Rank.2': 2,
    'Rank.3': 2,
    'Rank.4': 2,
    'Rank.5': 1
}

def assignValue(row):
    row['points'] = point_value[row['variable']]

def rankEm():
    albums = pd.read_csv("finaltable_long.csv")

    #change dataframe to dict and apply point values by row
    album_list = albums.to_dict('records')
    for idx, row in enumerate(album_list):
        assignValue(row)

    #return results to dataframe
    albums = pd.DataFrame(album_list)

    #create pivot table and order by points descending
    albums = pd.pivot_table(albums, values='points', index='value', aggfunc=np.sum)

    albums.to_csv('ranked.csv')
    print 'Done.'


if __name__ == '__main__':
    rankEm()
