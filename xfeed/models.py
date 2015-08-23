# -*- coding: utf-8 -*-
"""
Provides Feed, Tweet, RSSItem and RSSChannelData, classes for storing data about a feed and items fetched from the feed.

Feed holds the necessary information for fetching items from the feed.
Tweet holds information about tweets fetched from the feed.
RSSItems holds information about rss items fetched from the feed.
RSSChannelData holds information about a RSS feed (e.g. generator, feed title, copyright)
"""

from django.conf import settings
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext as _
from django.utils import timezone
from datetime import datetime
import feedparser
from time import mktime
import twitter
import urlparse

__author__ = 'Ruud Schroën'
__copyright__ = 'Copyright 2015, Ruud Schroën'
__license__ = 'BSD'
__version__ = '0.2'
__maintainer__ = 'Ruud Schroën'
__email__ = 'schroenruud@gmail.com'
__status__ = 'Development'

FEED_TYPES = [
    ('twitter', 'Twitter'),
    ('rss', 'RSS'),
]


class NoCredentials(Exception):
    """
    Exception for incomplete credentials
    """
    pass


class Base(models.Model):
    """
    Abstract model that has datetime fields 'created_on' and 'modified_on'. Used for admin purposes.
    """
    created_on = models.DateTimeField(auto_now_add=True, editable=False)
    modified_on = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('base')
        verbose_name_plural = _('base')
        abstract = True
        app_label = 'xfeed'


@python_2_unicode_compatible
class Feed(Base):
    """
    Stores a single Feed
    """
    name = models.CharField(max_length=255, verbose_name=_('name'))
    feed_type = models.CharField(max_length=255, choices=FEED_TYPES, verbose_name=_('feed type'))
    uuid = models.CharField(max_length=100, blank=True, unique=True)
    target = models.CharField(max_length=255, verbose_name=_('feed url'),
                              help_text=_('Enter a valid URL or Twitter screen name'))
    api_point = models.CharField(max_length=255, null=True, blank=True, verbose_name=_('api point'),
                                 help_text=_('Specify an API point (e.g. user timeline of Twitter. '
                                             'Check documentation for more information.'))
    website = models.URLField(max_length=255, verbose_name=_('website'),
                              help_text=_('Website url (e.g. http://mywebsite.com)'), null=True, blank=True)
    last_refreshed = models.DateTimeField(verbose_name=_('last refreshed'), null=True, blank=True)
    is_active = models.BooleanField(default=True, verbose_name=_('is active'),
                                    help_text=_('Must be checked if this feed should be updated'))

    class Meta:
        ordering = ('feed_type', 'name',)
        verbose_name = _('feed')
        verbose_name_plural = _('feeds')
        app_label = 'xfeed'

    def __str__(self):
        return self.name

    def set_active(self, which):
        """Sets the active state on/off for a Feed.

        :param which: True or False.
        :type which: bool
        :raises: ValueError

        """
        if not isinstance(which, (bool,)):
            raise ValueError(_('The "force" parameter must be True or False!'))
        self.is_active = which

    def clean_up(self, date, feed_type=None):
        """Cleans up a Feed by removing all Tweets and RSSItems that where published before a given date.

        :param date: Date to use in the "lower than" delete query.
        :type date: DateTime
        :param feed_type: If given, only items with a matching feed_type will be deleted.
        :type feed_type: str
        :returns:  Object -- holds counts for the amount of deleted tweets/rss-items

        """
        tweets_count = 0
        rss_items_count = 0
        if not feed_type:
            tweets = Tweet.objects.filter(feed=self, create_date__lt=date)
            tweets_count = tweets.count()
            tweets.delete()
            rss_items = RSSItem.objects.filter(feed=self, pub_date__lt=date)
            rss_items_count = rss_items.count()
            rss_items.delete()
        elif feed_type == 'twitter':
            tweets = Tweet.objects.filter(feed=self, create_date__lt=date)
            tweets_count = tweets.count()
            tweets.delete()
        elif feed_type == 'rss':
            rss_items = RSSItem.objects.filter(feed=self, pub_date__lt=date)
            rss_items_count = rss_items.count()
            rss_items.delete()
        return {'tweets_count': tweets_count, 'rss_items_count': rss_items_count}

    def flush(self, feed_type=None):
        """Removes all Tweets and RSSItems of a Feed.

        :param feed_type: If given, only items with a matching feed_type will be deleted.
        :type feed_type: str
        :returns:  Object -- holds counts for the amount of deleted tweets/rss-items

        """
        tweets_count = 0
        rss_items_count = 0
        if not feed_type:
            tweets = Tweet.objects.filter(feed=self)
            tweets_count = tweets.count()
            tweets.delete()
            rss_items = RSSItem.objects.filter(feed=self)
            rss_items_count = rss_items.count()
            rss_items.delete()
        elif feed_type == 'twitter':
            tweets = Tweet.objects.filter(feed=self)
            tweets_count = tweets.count()
            tweets.delete()
        elif feed_type == 'rss':

            rss_items = RSSItem.objects.filter(feed=self)
            rss_items_count = rss_items.count()
            rss_items.delete()
        return {'tweets_count': tweets_count, 'rss_items_count': rss_items_count}

    def refresh(self):
        """Refreshes a Feed. Gathers new content if available.
        Sets the last_refreshed field of the Feed to the date of refreshing.

        :raises: RuntimeError

        """
        if self.feed_type == 'twitter':
            consumer_key = getattr(settings, 'TWITTER_CONSUMER_KEY', None)
            consumer_secret = getattr(settings, 'TWITTER_CONSUMER_SECRET', None)
            access_token_key = getattr(settings, 'TWITTER_ACCESS_TOKEN_KEY', None)
            access_token_secret = getattr(settings, 'TWITTER_ACCESS_TOKEN_SECRET', None)

            if not consumer_key:
                raise NoCredentials(_('Twitter consumer key missing'))
            if not consumer_secret:
                raise NoCredentials(_('Twitter consumer secret missing'))
            if not access_token_key:
                raise NoCredentials(_('Twitter access token key missing'))
            if not access_token_secret:
                raise NoCredentials(_('Twitter access token secret missing'))

            try:
                api = twitter.Api(consumer_key=consumer_key,
                                  consumer_secret=consumer_secret,
                                  access_token_key=access_token_key,
                                  access_token_secret=access_token_secret)
                statuses = api.GetUserTimeline(screen_name=self.target)
                for s in statuses:
                    new = True
                    ogid = s.id
                    for t in self.tweets.all():
                        if t.ogid == str(ogid):
                            new = False
                            break
                    if new:
                        current_tz = timezone.get_current_timezone()
                        naive_date = datetime.strptime(s.created_at, '%a %b %d %H:%M:%S +0000 %Y')
                        create_date = current_tz.localize(naive_date)
                        t = Tweet(feed=self, ogid=ogid, create_date=create_date, from_user_id=s.user.id,
                                  from_user_name=s.user.screen_name, language=s.user.lang,
                                  profile_image_url=s.user.profile_image_url,
                                  source=s.source, text=s.text, to_user_id=s.in_reply_to_user_id,
                                  to_user_screen_name=s.in_reply_to_screen_name, to_status_id=s.in_reply_to_status_id)
                        t.save()
            except Exception, e:
                raise RuntimeError('Failed to fetch Tweets for feed %s, reason: %s' % (self.name, e))
        if self.feed_type == "rss":
            if not bool(urlparse.urlparse(self.target).scheme):
                raise ValueError('RSS target is not a valid URL')

            try:
                d = feedparser.parse(self.target)
                current_tz = timezone.get_current_timezone()
                feed_timestamp = d.feed.published_parsed
                feed_pub_date = current_tz.localize(datetime.fromtimestamp(mktime(feed_timestamp)))
                last_build_timestamp = d.feed.updated_parsed
                last_build_date = current_tz.localize(datetime.fromtimestamp(mktime(last_build_timestamp)))

                # Updating or inserting RSS channel data
                try:
                    # If channel data exists, update
                    RSSChannelData.objects.filter(feed=self).update(title=d.feed.title, subtitle=d.feed.subtitle,
                                                                    link=d.feed.link, language=d.feed.language,
                                                                    pub_date=feed_pub_date,
                                                                    last_build_date=last_build_date,
                                                                    generator=d.feed.generator, copyright=d.feed.rights)
                except RSSChannelData.DoesNotExist:
                    # Else create a new record
                    channel_data = RSSChannelData(feed=self, title=d.feed.title, subtitle=d.feed.subtitle,
                                                  link=d.feed.link, language=d.feed.language, pub_date=feed_pub_date,
                                                  last_build_date=last_build_date, generator=d.feed.generator,
                                                  copyright=d.feed.rights,
                                                  )
                    channel_data.save()

                # Inserting new posts into database
                for post in d.entries:
                    new = True
                    ogid = post.id
                    for e in self.rss_items.all():
                        if e.ogid == ogid:
                            new = False
                            break
                    post_timestamp = post.published_parsed
                    naive_date = datetime.fromtimestamp(mktime(post_timestamp))
                    pub_date = current_tz.localize(naive_date)
                    if new:
                        item = RSSItem(feed=self, ogid=ogid, ogid_is_link=post.guidislink, pub_date=pub_date,
                                       language=d.feed.language, title=post.title, description=post.summary,
                                       link=post.link)
                        item.save()
            except Exception, e:
                raise RuntimeError('Failed to fetch RSS for feed %s, reason: %s' % (self.name, e))

        self.last_refreshed = timezone.now()
        self.save()


@python_2_unicode_compatible
class Tweet(Base):
    """
    Stores a single Tweet, related to model:'xfeed.Feed'
    """
    feed = models.ForeignKey(Feed, related_name="tweets", verbose_name=_('feed'))
    ogid = models.CharField(max_length=255, verbose_name=_('original ID'))
    create_date = models.DateTimeField(verbose_name=_('create date'))
    from_user_id = models.CharField(max_length=255, verbose_name=_('from user ID'))
    from_user_name = models.CharField(max_length=255, verbose_name=_('from user name'))
    language = models.CharField(max_length=255, verbose_name=_('iso language code'))
    profile_image_url = models.URLField(max_length=255, verbose_name=_('profile image URL'))
    source = models.CharField(max_length=255, verbose_name=_('source'))
    text = models.TextField(verbose_name=_('text'))
    to_user_id = models.CharField(max_length=255, verbose_name=_('reply to user id'), null=True)
    to_user_screen_name = models.CharField(max_length=255, verbose_name=_('reply to user screen name'), null=True)
    to_status_id = models.CharField(max_length=255, verbose_name=_('reply to status ID'), null=True)
    hide = models.BooleanField(default=False, verbose_name=_('hide this tweet'))

    class Meta:
        ordering = ('create_date',)
        verbose_name = _('tweet')
        verbose_name_plural = _('tweets')
        get_latest_by = "ogid"
        app_label = 'xfeed'

    def __str__(self):
        return self.text

    def set_hide(self, which):
        """Sets the hide state on/off for a Tweet.

        :param which: True or False.
        :type which: bool
        :raises: ValueError

        """
        if not isinstance(which, (bool,)):
            raise ValueError(_('The "force" parameter must be True or False!'))
        self.hide = which


@python_2_unicode_compatible
class RSSItem(Base):
    """
    Stores a single RSS item, related to model:'xfeed.Feed'
    """
    feed = models.ForeignKey(Feed, related_name="rss_items", verbose_name=_('feed'))
    ogid = models.CharField(max_length=255, verbose_name=_('original ID'))
    ogid_is_link = models.BooleanField(default=False, verbose_name=_('original ID is link'))
    pub_date = models.DateTimeField(verbose_name=_('publishing date'))
    language = models.CharField(max_length=255, verbose_name=_('iso language code'))
    title = models.CharField(max_length=255, verbose_name=_('title'))
    description = models.TextField(verbose_name=_('description'))
    link = models.URLField(max_length=255, verbose_name=_('link'))
    hide = models.BooleanField(default=False, verbose_name=_('hide this item'))

    class Meta:
        ordering = ('feed', 'title',)
        verbose_name = _('RSS item')
        verbose_name_plural = _('RSS items')
        get_latest_by = 'ogid'
        app_label = 'xfeed'

    def __str__(self):
        return self.title

    def set_hide(self, which):
        """Sets the hide state on/off for a RSSItem.

        :param which: True or False.
        :type which: bool
        :raises: ValueError

        """
        if not isinstance(which, (bool,)):
            raise ValueError(_('The "force" parameter must be True or False!'))
        self.hide = which


@python_2_unicode_compatible
class RSSChannelData(Base):
    """
    Stores a single RSSChannelData object, related to model:'xfeed.Feed'.
    Holds additional information about the feed itself.
    """
    feed = models.OneToOneField(Feed, primary_key=True)
    title = models.CharField(max_length=255, verbose_name=_('title'))
    subtitle = models.CharField(max_length=255, verbose_name=_('subtitle'))
    link = models.CharField(max_length=255, verbose_name=_('link'))
    language = models.CharField(max_length=255, verbose_name=_('language'))
    pub_date = models.DateTimeField(verbose_name=_('publishing date'))
    last_build_date = models.DateTimeField(verbose_name=_('last build date'))
    generator = models.CharField(max_length=255, verbose_name=_('generator'))
    copyright = models.CharField(max_length=255, verbose_name=_('copyright'))

    class Meta:
        ordering = ('feed',)
        verbose_name = _('RSS channel data')
        verbose_name_plural = _('RSS channel data')
        get_latest_by = 'ogid'
        app_label = 'xfeed'

    def __str__(self):
        return self.feed.name
