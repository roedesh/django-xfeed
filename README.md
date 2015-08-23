xFeed
-----------
*django-xfeed is a reusable application for Django, that aims to be a single aggregator for various media types (e.g. RSS, Twitter, Facebook).*

There are many apps for gathering data from RSS, Twitter, Facebook or any other social media platform, but they are all individual apps. This app provides an all-in-one aggregator.

Features
-----------
* Fetches RSS items and channel data of a RSS feed
* Fetches tweets from the user timeline

Quick start
-----------
1. Add "xfeed" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = (
        ...
        'xfeed',
    )

2. Run `python manage.py migrate` to create the polls models.

4. Start the development server and visit http://127.0.0.1:8000/admin/
   to create a poll (you'll need the Admin app enabled).

5. Visit http://127.0.0.1:8000/admin/ and create a new Feed.

6. Run `python manage.py refresh_feeds` to fetch content.

7. Revisit admin to find your Tweets or RSS items.

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
