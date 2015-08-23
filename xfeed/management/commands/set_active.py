from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from xfeed.models import Feed
from django.utils import translation
from django.utils.translation import ugettext as _


class Command(BaseCommand):
    """
    This command sets the is_active state of a feed
    """
    help = _('Refresh all active feeds')

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('feed_uuid', nargs='+', type=str)
        parser.add_argument('which', nargs='+', type=bool)

    def handle(self, *args, **options):
        translation.activate(settings.LANGUAGE_CODE)
        try:
            feed = Feed.objects.get(uuid=options['feed_uuid'][0])
            feed.is_active = options['which'][0]
            feed.save()
            self.stdout.write(
                'Successfully set %s-feed %s is_active to %s' % (feed.feed_type, feed.uuid, feed.is_active))
        except Feed.DoesNotExist:
            raise CommandError("Feed does not exist")
