from django.contrib import admin

from .models import RokuSearchFeed

# Roku Content Feed

class RokuSearchFeedAdmin(admin.ModelAdmin):
	list_display = ['provider_name']
	search_fields = ['provider_name']
	list_filter = ['language']
	readonly_fields = ['last_updated']
	class Meta:
		model = RokuSearchFeed


# Register with Admin
admin.site.register(RokuSearchFeed, RokuSearchFeedAdmin)
