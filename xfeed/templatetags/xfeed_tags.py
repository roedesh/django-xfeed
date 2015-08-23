from django import template

register = template.Library()

@register.simple_tag
def generate_feed_list(feed, amount=None, ul_class=None, li_class=None):
    """Removes all values of arg from the given string

    :param feed: The feed to generate the list from.
    :type feed: Feed
    :param amount: The amount of items to show.
    :type amount: int
    :param ul_class: The <ul> class to use.
    :type ul_class: str
    :param li_class: The <li> class to use.
    :type li_class: str
    :raises:  ValueError
    """

    if feed.feed_type == 'twitter':
        ret = ['<ul class="%s">' % ul_class or 'tweet-list']
        tweets = feed.tweets.all()
        if amount:
            if not int(amount):
                raise ValueError('Amount must be a number')
            tweets = tweets[:amount]
        for t in tweets:
            ret.append(
                '<li class="%s">'
                '<div class="tweet-profile-picture">'
                '<img src="%s" alt="Twitter profile picture of %s" width="48" height="48" /></div>'
                '<div class="tweet-body">%s</div></li>' % (li_class or 'tweet', t.profile_image_url, t.from_user_name, t.text))
    if feed.feed_type == 'rss':
        ret = ['<ul class="%s">' % ul_class or 'rss-list']
        rss_items = feed.rss_items.all()
        if amount:
            if not int(amount):
                raise ValueError('Amount must be a number')
            rss_items = rss_items[:amount]
        for t in rss_items:
            ret.append(
                '<li class="%s">'
                '<div class="rss-item-body">%s</div></li>' % (li_class or 'rss-item', t.description))
    ret.append('</ul>')
    return ''.join(ret)
