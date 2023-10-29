from django.contrib import admin

from .models import SearchFeed

# Roku Content Feed

class SearchFeedAdmin(admin.ModelAdmin):
	list_display = ['search_feed_id', 'version', 'default_language']
	search_fields = ['search_feed_id']
	list_filter = ['default_language']
	readonly_fields = ['search_feed_id']
	class Meta:
		model = SearchFeed


# Register with Admin
admin.site.register(SearchFeed, SearchFeedAdmin)
