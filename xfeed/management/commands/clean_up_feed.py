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
        parser.add_argument('date_string', nargs='+', type=str)

    def handle(self, *args, **options):
        translation.activate(settings.LANGUAGE_CODE)
        try:
            feed = Feed.objects.get(uuid=options['feed_uuid'][0])
        except Feed.DoesNotExist:
            raise CommandError("Feed does not exist")
        try:
            date = datetime.strptime(options['date_string'][0], '%Y-%m-%d')
        except:
            raise CommandError("Invalid date format. Must be YYYY-MM-DD.")
        result = feed.clean_up(date)
        self.stdout.write('Successfully cleaned up %s-feed %s. %s tweets and %s RSS items were removed.' % (
            feed.get_feed_type_display(), feed.name, result['tweets_count'], result['rss_items_count']))
