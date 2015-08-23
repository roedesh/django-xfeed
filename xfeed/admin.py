from django.contrib import admin
from models import Feed, Tweet, RSSItem, RSSChannelData

class RSSChannelDataInline(admin.StackedInline):
    model = RSSChannelData

class FeedAdmin(admin.ModelAdmin):
    inlines = [RSSChannelDataInline]

    def get_formsets_with_inlines(self, request, obj=None):
        for inline in self.get_inline_instances(request, obj):
            if obj is not None and inline.get_queryset(request).count() > 0:
                yield inline.get_formset(request, obj), inline

admin.site.register(Feed, FeedAdmin)
admin.site.register(Tweet)
admin.site.register(RSSItem)
