import pandas as pd

RANKS = ["Rank 1", "Rank 2", "Rank 3", "Rank 4", "Rank 5"]
DUPLICATE_TIME_THRESHOLD = 60 * 60


def checkEqual(iterator):
    """
    Clever solution for seeing if all items in list identical from
    http://stackoverflow.com/questions/3844801/check-if-all-elements-in-a-list-are-identical
    """
    iterator = iter(iterator)
    try:
        first = next(iterator)
    except StopIteration:
        return True
    return all(first == rest for rest in iterator)


def find_dupe(row1, row2):
    """
    Check if pair of rows are identical
    """

    # Do row values match? If not, not a dupe
    for rank in RANKS:
        if row1[rank] != row2[rank]:
            return False

    return True


def find_oddities(row, idx, album_list):
    """
    Search backwards to see if current row if a dupe of something that came before
    """
    row['smelly'] = False

    # Check for identical rankings
    row_values = [str(row[rank]).lower() for rank in RANKS]
    if checkEqual(row_values):
        row['smelly'] = True

    # Check for dupes in previous time window
    previousrow = album_list[idx]
    delta = row["Timestamp"] - previousrow["Timestamp"]

    while row['smelly'] is False and delta.seconds < DUPLICATE_TIME_THRESHOLD and delta.seconds > 0:
        row['smelly'] = find_dupe(row, previousrow)
        idx = idx - 1
        previousrow = album_list[idx]
        delta = row["Timestamp"] - previousrow["Timestamp"]


def process():
    albums = pd.read_csv("Vote For 2016's Best Albums (Responses) - Form Responses 1.csv")

    # Convert timestamp column values to datetime objects
    albums["Timestamp"] = pd.to_datetime(albums["Timestamp"])

    # Drop empty rows
    albums.dropna(subset=RANKS)

    # Turn dataframe into list for easier handling of oddity detection
    album_list = albums.to_dict('records')
    for idx, row in enumerate(album_list):
        find_oddities(row, idx - 1, album_list)

    # Cast back to dataframe
    albums = pd.DataFrame(album_list)

    # Weed out rows with smells
    albums = albums[albums['smelly'] == False]

    albums.to_csv('finaltable.csv')


if __name__ == '__main__':
    process()
