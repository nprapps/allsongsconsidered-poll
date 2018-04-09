All Songs Considered - Turning the Tables Poll
==============================================

* [What is this?](#what-is-this)
* [Assumptions](#assumptions)
* [What's in here?](#whats-in-here)
* [Installation](#installation)
* [Running the project](#running-the-project)

What is this?
-------------

A repository for cleaning, processing and ranking the form responses of the NPR Music Turning the Tables poll. This code is inspired on the work from the [2016 poll blog post](http://blog.apps.npr.org/2016/12/16/all-songs-considered-poll.html).

In order to cluster the data, we used `dedupe`. We chose the library [csvdedupe](https://github.com/dedupeio/csvdedupe) because it uses supervised machine learning techniques to detect similar entries and cluster them.

To make our data transformation pipeline more compact and reusable, we used `GNU Make`. We have one central [`Makefile`](Makefile) with two main actions: `dedupe` and `rank`. We separated the processes to allow for a manual review checkpoint after using `csvdedupe` to cluster album/artist key pairs. We found that it's best to check before ranking because of oddities in the user-submitted data like inputting an artist in the album spot and vice versa. These misclassifications impacted our top 150 classification, so we added an extra step to ensure accuracy using [OpenRefine](http://openrefine.org/) to make small adjustments.

This codebase is licensed under the MIT open source license. See the [LICENSE](LICENSE) file for the complete license.


Assumptions
-----------

* You are using Python 2.7. (Probably the version that came OSX.)
* You have [virtualenv](https://pypi.python.org/pypi/virtualenv) and [virtualenvwrapper](https://pypi.python.org/pypi/virtualenvwrapper) installed and working.
* You have make 3.x installed and working (this comes installed with the XCode Command Line Tools)


What's in here?
---------------
The project contains the following folders and important files:

* `Makefile` -- `GNU Make` for organizing and compiling scripts.
* `requirements.txt` -- Python requirements.
* `training.json` -- `csvdedupe` output from running `dedupe.sh`.


Installation
------------

```
cd allsongsconsidered-poll
mkvirtualenv allsongsconsidered-poll
pip install -r requirements.txt
```

Running the project
-------------------

This project uses `make` to run all the scripts. The first make command takes a `CSV_URL` from a published Google form responses spreadsheet. To publish a spreadsheet, follow [these instructions](https://support.google.com/docs/answer/37579?co=GENIE.Platform%3DDesktop&hl=en).

To start the `dedupe` command, run:

```
make dedupe CSV_URL='https://docs.google.com/spreadsheets/d/e/2PACX-1vSMW2pbk3YWfNWU4C0wHVdMr90oHvyMHrRp_SJlUei6P1bnQDUWKOfBkR2zi3QFefk2GEfv5TTE-vJw/pub?gid=1988637773&single=true&output=csv'
```

The `dedupe` command will download the published Google form spreadsheet, clean ballot stuffing then transform the data to normalize the responses for easier clustering.

`/scripts/clean_ballot_stuffing` takes two arguments:

* `DUPLICATE_TIME_THRESHOLD` -- time window to check and remove duplicate entries (in seconds)
* `RANDOM_ORDER_TIME_THRESHOLD` -- random ordering detection within a different smaller time window (in seconds)

`/scripts/transform_form_responses` takes three arguments:

* `MAX_SUBMIT` -- maximum number of albums a user can submit
* `POLL_START_DATE` -- date poll opened formatted M/D/YYYY
* `POLL_END_DATE` -- date poll closed formatted M/D/YYYY

After running those two scripts, the `csvdedupe` process is enabled to start cluster training. The more you train, the better the clustering will be. We trained true and false matches over 200 times each.

We used OpenRefine to check our clusters.

![OpenRefine screenshot][screenshot]

[screenshot]: readme-assets/OpenRefine_validation.png

If you make changes inside OpenRefine you'll need to:
1. Export the modified dataset into a csv file.
2. Override the `Makefile` variables when running `make rank`. With a modified csv, you'll have to update `RANK_DATA_DIR` & `RANK_INPUT_FILE` like this:

```
make rank RANK_DATA_DIR=output RANK_INPUT_FILE=allsongs_responses_deduped_refine.csv
```

If you did not make any changes in OpenRefine, you can run:
```
make rank
```

The top 200 will output to `output/allsongs_responses_top100.csv`. To change the number of albums output, you can modify the `RANKED_OUTPUT_NUM` variable.
