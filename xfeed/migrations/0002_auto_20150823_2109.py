# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('xfeed', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feed',
            name='api_point',
            field=models.CharField(help_text='Specify an API point (e.g. user timeline of Twitter. Check documentation for more information.', max_length=255, null=True, verbose_name='api point', blank=True),
        ),
        migrations.AlterField(
            model_name='feed',
            name='website',
            field=models.URLField(help_text='Website url (e.g. http://mywebsite.com)', max_length=255, null=True, verbose_name='website', blank=True),
        ),
    ]
