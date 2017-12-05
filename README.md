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

1. Download original form responses
2. Combine like entries using csvdedupe
