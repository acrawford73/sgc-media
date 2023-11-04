import datetime,time
from django.db import models
from django.urls import reverse

### System Configuration

class SystemConfig(models.Model):
	"""
	The SystemConfig model must only have one record. Therefore, the CreateView is not supported.
	
	Defaults will be loaded as a fixture.
	"""
	title = models.CharField(max_length=50, default="", null=False, blank=False)

	# Media Sources
	server_url = models.URLField(max_length=2083, default="", null=True, blank=True)
	cdn_url = models.URLField(max_length=2083, default="", null=True, blank=True)
	path_media = models.CharField(max_length=256, default="", null=True, blank=True)

	# Content Types, disabling removes from navbar
	movie_enable = models.BooleanField(default=True, null=False, blank=True)
	live_feed_enable = models.BooleanField(default=True, null=False, blank=True)
	series_enable = models.BooleanField(default=True, null=False, blank=True)
	short_form_video_enable = models.BooleanField(default=True, null=False, blank=True)
	tv_special_enable = models.BooleanField(default=True, null=False, blank=True)
	language_enable = models.BooleanField(default=True, null=False, blank=True)

	updated = models.DateTime(auto_now=True)
	class Meta:
		ordering = ['-id']
		def __unicode__(self):
			return self.id
