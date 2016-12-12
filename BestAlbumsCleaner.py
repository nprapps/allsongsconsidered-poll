import pandas as pd

RANKS = ["Rank 1", "Rank 2", "Rank 3", "Rank 4", "Rank 5"]


def process():
    albums = pd.read_csv("Vote For 2016's Best Albums (Responses) - Form Responses 1.csv")

    # convert to datetime format (from object to dattime64)
    albums["Timestamp"] = pd.to_datetime(albums["Timestamp"])
    albums.dropna(subset=RANKS)
    albums = albums.drop_duplicates(subset=RANKS)
    albums.to_csv('finaltable.csv')


if __name__ == '__main__':
    process()
