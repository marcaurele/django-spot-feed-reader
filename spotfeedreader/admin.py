from django.contrib import admin
from spotfeedreader.models import SpotFeed, SpotMessage

class SpotFeedAdmin(admin.ModelAdmin):
	list_display = ('id', 'active', 'feed_id', 'name', 'created_date',)
	list_filter = ('active','created_date',)
	search_fields = ('feed_id', 'name', 'description',)
	readonly_fields = ('name', 'description','created_date',)

admin.site.register(SpotFeed, SpotFeedAdmin)


class SpotMessageAdmin(admin.ModelAdmin):
	list_display = ('id', 'message_id', 'date_time', 'message_type', 'latitude', 'longitude', 'created_date',)

admin.site.register(SpotMessage, SpotMessageAdmin)
