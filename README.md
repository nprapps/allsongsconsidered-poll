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


Installation
------------

```
cd allsongsconsidered-poll
mkvirtualenv allsongsconsidered-poll
pip install -r requirements.txt
```

Run Project
-----

* Download the original form responses into `data/2017_responses.csv`

Having done that we are going to use the first of two makefiles to execute our data transformation process.

* `make -f clean_dedupe.mk`

Review the results on OpenRefine.

![OpenRefine screenshot][screenshot]

[screenshot]: readme-assets/OpenRefine_validation.png

If you make changes inside OpenRefine then you'll need to
1. Export the modified dataset into a csv file from OpenRefine.
2. Change the `INPUT_DATA_DIR` & `INPUT_FILE` on the `rank.mk` to point to the modified file.

* `make -f rank.mk`

The Top100 should be available on `output/2017_responses_top100.csv`
