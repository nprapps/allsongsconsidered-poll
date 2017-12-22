All Songs Considered - EOY Best Album Poll
==========================================

* [What is this?](#what-is-this)
* [Assumptions](#assumptions)
* [Installation](#installation)
* [Run project](#run-project)

What is this?
-------------

A repository for cleaning, processing and ranking the form responses of the All Songs Considered End of Year Best Album Poll. This code is inspired on the work from the [2016 poll blog post](http://blog.apps.npr.org/2016/12/16/all-songs-considered-poll.html).

In 2017 we decided we wanted to give `dedupe` a try for our data clustering task, specifically we wanted to use [csvdedude](https://github.com/dedupeio/csvdedupe). This library uses supervised machine learning techniques to detect similar entries and cluster them.

Also we wanted to use makefiles in order to make our data transformation pipeline more compact and reusable.

We have used two makefiles because we wanted to have a manual review checkpoint after `dedupe` has classified our album/artist key pairs into clusters, even though `dedupe` did a fantastic job of identifying the bulk of the similar entries some where misclassified and we used [OpenRefine](http://openrefine.org/) to make small adjustments that impacted our top 100 classification.

This codebase is licensed under the MIT open source license. See the [LICENSE](https://github.com/nprapps/allsongsconsidered-poll/blob/master/LICENSE) file for the complete license.


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

* Publish the form responses spreadsheet or a copy of it to leave the form and spreadsheet untouched as a csv. Follow instructions [here](https://support.google.com/docs/answer/37579?co=GENIE.Platform%3DDesktop&hl=en)

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


The Top100 should be available on `output/allsongs_responses_top100.csv`
