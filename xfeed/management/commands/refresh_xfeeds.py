from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from xfeed.models import Feed
from django.utils import translation
from django.utils.translation import ugettext as _


class Command(BaseCommand):
    """
    This command will refresh all active feeds
    """
    help = _('Refresh all active feeds')

    def handle(self, *args, **options):
        translation.activate(settings.LANGUAGE_CODE)
        for feed in Feed.objects.filter(is_active=True):
            feed.refresh()
