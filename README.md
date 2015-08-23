[![Build passed](https://api.travis-ci.org/rschroen/django-xfeed.svg?branch=master)](https://pypi.python.org/pypi/django-xfeed/)
[![Latest Version](https://pypip.in/version/django-xfeed/badge.svg)](https://pypi.python.org/pypi/django-xfeed/)
    
xFeed
-----------
*django-xfeed is a reusable application for Django, that aims to be a single aggregator for various media types (e.g. RSS, Twitter, Facebook).*

There are many apps for gathering data from RSS, Twitter, Facebook or any other social media platform, but they are all individual apps. This app provides an all-in-one aggregator.

Features
-----------
* Fetches RSS items and channel data of a RSS feed
* Fetches tweets from the user timeline
* Handy template tag for generating a list of items
* Some useful management commands for managing your feeds

Install with pip
-----------
Run `pip install django-xfeed`

Install with setup.py
-----------
Run `python setup.py install`

Quick start
-----------
1. Add "xfeed" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = (
        ...
        'xfeed',
    )

2. Run `python manage.py migrate` to create the xfeed models.

4. Start the development server and visit http://127.0.0.1:8000/admin/
   to create a feed (you'll need the Admin app enabled).

5. Run `python manage.py refresh_feeds` to fetch content.

6. Revisit admin to find your Tweets and/or RSS items.

Generate a list of items
-----------
To generate a list of items from your feed, use the `generate_feed_list` tag. It requires a feed object. It also accepts the following parameters:
* amount (int) Amount of items to show
* list_class (str) Class to use on the <ul> or <ol>
* li_class (str) Class to use on the <li>
* list_type (str) Type of list to use, defaults to 'ul'

Example: `{% generate_feed_list 5 'my-list' 'my-list-item' 'ol' %}`

Documentation
-----------
*coming soon*

Dependencies
-----------
xFeed has a small set of dependencies.
* feedparser
* python-twitter
* pytz

Todo's
-----------
* Allow different API points (e.g. Twitter's home timeline instead of user timeline)
* Facebook status updates
* LinkedIn status updates
