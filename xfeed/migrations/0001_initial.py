# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Feed',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('modified_on', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('feed_type', models.CharField(max_length=255, verbose_name='feed type', choices=[(b'twitter', b'Twitter'), (b'rss', b'RSS')])),
                ('uuid', models.CharField(unique=True, max_length=100, blank=True)),
                ('target', models.CharField(help_text='Enter a valid URL or Twitter screen name', max_length=255, verbose_name='feed url')),
                ('api_point', models.CharField(help_text='Specify an API point (e.g. user timeline of Twitter. Check documentation for more information.', max_length=255, null=True, verbose_name='api point')),
                ('website', models.URLField(help_text='Website url (e.g. http://mywebsite.com)', max_length=255, null=True, verbose_name='website')),
                ('last_refreshed', models.DateTimeField(null=True, verbose_name='last refreshed', blank=True)),
                ('is_active', models.BooleanField(default=True, help_text='Must be checked if this feed should be updated', verbose_name='is active')),
            ],
            options={
                'ordering': ('feed_type', 'name'),
                'verbose_name': 'feed',
                'verbose_name_plural': 'feeds',
            },
        ),
        migrations.CreateModel(
            name='RSSItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('modified_on', models.DateTimeField(auto_now=True)),
                ('ogid', models.CharField(max_length=255, verbose_name='original ID')),
                ('ogid_is_link', models.BooleanField(default=False, verbose_name='original ID is link')),
                ('pub_date', models.DateTimeField(verbose_name='publishing date')),
                ('language', models.CharField(max_length=255, verbose_name='iso language code')),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('description', models.TextField(verbose_name='description')),
                ('link', models.URLField(max_length=255, verbose_name='link')),
                ('hide', models.BooleanField(default=False, verbose_name='hide this item')),
            ],
            options={
                'ordering': ('feed', 'title'),
                'get_latest_by': 'ogid',
                'verbose_name': 'RSS item',
                'verbose_name_plural': 'RSS items',
            },
        ),
        migrations.CreateModel(
            name='Tweet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('modified_on', models.DateTimeField(auto_now=True)),
                ('ogid', models.CharField(max_length=255, verbose_name='original ID')),
                ('create_date', models.DateTimeField(verbose_name='create date')),
                ('from_user_id', models.CharField(max_length=255, verbose_name='from user ID')),
                ('from_user_name', models.CharField(max_length=255, verbose_name='from user name')),
                ('language', models.CharField(max_length=255, verbose_name='iso language code')),
                ('profile_image_url', models.URLField(max_length=255, verbose_name='profile image URL')),
                ('source', models.CharField(max_length=255, verbose_name='source')),
                ('text', models.TextField(verbose_name='text')),
                ('to_user_id', models.CharField(max_length=255, null=True, verbose_name='reply to user id')),
                ('to_user_screen_name', models.CharField(max_length=255, null=True, verbose_name='reply to user screen name')),
                ('to_status_id', models.CharField(max_length=255, null=True, verbose_name='reply to status ID')),
                ('hide', models.BooleanField(default=False, verbose_name='hide this tweet')),
            ],
            options={
                'ordering': ('create_date',),
                'get_latest_by': 'ogid',
                'verbose_name': 'tweet',
                'verbose_name_plural': 'tweets',
            },
        ),
        migrations.CreateModel(
            name='RSSChannelData',
            fields=[
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('modified_on', models.DateTimeField(auto_now=True)),
                ('feed', models.OneToOneField(primary_key=True, serialize=False, to='xfeed.Feed')),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('subtitle', models.CharField(max_length=255, verbose_name='subtitle')),
                ('link', models.CharField(max_length=255, verbose_name='link')),
                ('language', models.CharField(max_length=255, verbose_name='language')),
                ('pub_date', models.DateTimeField(verbose_name='publishing date')),
                ('last_build_date', models.DateTimeField(verbose_name='last build date')),
                ('generator', models.CharField(max_length=255, verbose_name='generator')),
                ('copyright', models.CharField(max_length=255, verbose_name='copyright')),
            ],
            options={
                'ordering': ('feed',),
                'get_latest_by': 'ogid',
                'verbose_name': 'RSS channel data',
                'verbose_name_plural': 'RSS channel data',
            },
        ),
        migrations.AddField(
            model_name='tweet',
            name='feed',
            field=models.ForeignKey(related_name='tweets', verbose_name='feed', to='xfeed.Feed'),
        ),
        migrations.AddField(
            model_name='rssitem',
            name='feed',
            field=models.ForeignKey(related_name='rss_items', verbose_name='feed', to='xfeed.Feed'),
        ),
    ]
