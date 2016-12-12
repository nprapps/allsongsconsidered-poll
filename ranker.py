import pandas as pd

RANKS = ["Rank 1", "Rank 2", "Rank 3", "Rank 4", "Rank 5"]

point_value = {
    'Rank.1': 5,
    'Rank.2': 4,
    'Rank.3': 3,
    'Rank.4': 2,
    'Rank.5': 1
}

def assignValue(row):
    row['points'] = point_value[row['variable']]

def rankEm():
    albums = pd.read_csv("finaltable_long.csv")

    album_list = albums.to_dict('records')
    for idx, row in enumerate(album_list):
        assignValue(row)

    albums = pd.DataFrame(album_list)
    albums.to_csv('ranked.csv')
    print 'Done.'


if __name__ == '__main__':
    rankEm()
