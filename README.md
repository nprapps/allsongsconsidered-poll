All Songs Considered - EOY Best Album Poll
==========================================

* [What is this?](#what-is-this)
* [Assumptions](#assumptions)
* [Installation](#installation)
* [View analysis notebook](#view-analysis-notebook)

What is this?
-------------

A repository for cleaning, processing and ranking the form responses of the All Songs Considered End of Year Best Album Poll. This code is based off of the work from the [2016 poll blog post](http://blog.apps.npr.org/2016/12/16/all-songs-considered-poll.html).

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

Steps
-----

1. Download original form responses into `data/2017_responses.csv`
2. Check for duplicate entries (2017_responses.csv > clean_ballot_stuffing.py > 2017_responses_clean.csv)
3. Transform the csv into a vertical format and remove repeated albums and artists inside the same form response (2017_responses_clean.csv > transform_form_responses.py > 2017_responses_normalized.csv)
4. Combine like entries using csvdedupe (2017_responses_normalized.csv > dedupe.sh > 2017_responses_deduped.csv)
<!-- 4. Standardize responses (standardize_responses.py) -->
<!-- 5.  -->
