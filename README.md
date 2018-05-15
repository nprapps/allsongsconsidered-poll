All Songs Considered - EOY Best Album Poll
==========================================

* [What is this?](#what-is-this)
* [Assumptions](#assumptions)
* [Installation](#installation)
* [Run project](#run-project)

What is this?
-------------

A repository for cleaning, processing, weighting and ranking the form responses of the NPR Music End of Year Music poll. This code is inspired by the work from the [2016 music poll blog post](http://blog.apps.npr.org/2016/12/16/all-songs-considered-poll.html), and there is an [updated blog post](http://blog.apps.npr.org/2018/01/03/all-songs-considered-poll.html) for changes to the 2017 music poll.

There are two versions of this codebase. The major difference is that the [`master`](https://github.com/nprapps/allsongsconsidered-poll) branch includes weighting of albums, while the [`turning-tables`](https://github.com/nprapps/allsongsconsidered-poll/tree/turning-tables) branch does not.

In order to cluster the data, we used `dedupe`. We chose the library [csvdedupe](https://github.com/dedupeio/csvdedupe) because it uses supervised machine learning techniques to detect similar entries and cluster them.

To make our data transformation pipeline more compact and reusable, we used `GNU Make`. We have one central [`Makefile`](Makefile) with two main actions: `dedupe` and `rank`. We separated the processes to allow for a manual review checkpoint after using `csvdedupe` to cluster album/artist key pairs. We found that it's best to check before ranking because of oddities in the user-submitted data like inputting an artist in the album spot and vice versa. These misclassifications impacted our top 150 classification, so we added an extra step to ensure accuracy using [OpenRefine](http://openrefine.org/) to make small adjustments.

This codebase is licensed under the MIT open source license. See the [LICENSE](LICENSE) file for the complete license.


Assumptions
-----------

* You are using Python 2.7. (Probably the version that came OSX.)
* You have [virtualenv](https://pypi.python.org/pypi/virtualenv) and [virtualenvwrapper](https://pypi.python.org/pypi/virtualenvwrapper) installed and working.
* GNU make


Installation
------------

```
cd allsongsconsidered-poll
mkvirtualenv allsongsconsidered-poll
pip install -r requirements.txt
```

Run Project
-----

* Publish the form responses spreadsheet or a copy of it to leave the form and spreadsheet as a csv. Follow instructions [here](https://support.google.com/docs/answer/37579?co=GENIE.Platform%3DDesktop&hl=en)

*NOTE:* The spreadsheet headers will have to match `DUPE_DICT_KEYS` in the [`clean_ballot_stuffing`](/scripts/clean_ballot_stuffing.py#L16-L19) script. 

* Copy the url of the spreadsheet published as a csv we'll need to provide that as a parameter.

Having done that we are going to use the first of two makefiles commandds to execute our data transformation process.

* `make dedupe CSV_URL='https://docs.google.com/spreadsheets/d/e/2PACX-1vTdnDO2daqBhCWFPPPwzqwHzZIyNDKS_N9af5QEx7HwgAT-bApIjireeZ_F6KAD30BSe49kWc4Dp7UE/pub?gid=43875107&single=true&output=csv'`

Review the results on OpenRefine.

![OpenRefine screenshot][screenshot]

[screenshot]: readme-assets/OpenRefine_validation.png

If you make changes inside OpenRefine then you'll need to
1. Export the modified dataset into a csv file from OpenRefine.
2. Override the following makefile variables on the command file the `RANK_DATA_DIR` & `RANK_INPUT_FILE`.

* `make rank RANK_DATA_DIR=output RANK_INPUT_FILE=allsongs_responses_deduped_refine.csv`

If you did not make any changes on OpenRefine you can proceed with
* `make rank`


The Top 100 should be available on `output/allsongs_responses_top100.csv`
