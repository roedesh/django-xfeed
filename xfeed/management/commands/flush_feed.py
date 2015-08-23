from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from xfeed.models import Feed
from django.utils import translation
from django.utils.translation import ugettext as _
from datetime import datetime


class Command(BaseCommand):
    """
    This command will refresh all active feeds
    """
    help = _('Refresh all active feeds')

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('feed_uuid', nargs='+', type=str)

    def handle(self, *args, **options):
        translation.activate(settings.LANGUAGE_CODE)
        try:
            feed = Feed.objects.get(uuid=options['feed_uuid'][0])
        except Feed.DoesNotExist:
            raise CommandError("Feed does not exist")
        result = feed.flush()
        self.stdout.write('Successfully flushed %s-feed %s. %s tweets and %s RSS items were removed.' % (
            feed.get_feed_type_display(), feed.name, result['tweets_count'], result['rss_items_count']))
