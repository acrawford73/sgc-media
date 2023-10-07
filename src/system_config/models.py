import datetime,time
from django.db import models
from django.urls import reverse

### System Configuration

class SystemConfig(models.Model):
	version = models.PositiveSmallIntegerField(default=1, null=False, blank=False)
	
	# Media Sources
	url_cdn = models.URLField(max_length=2038, default="", null=True, blank=True)
	path_media = models.CharField(max_length=256, default="", null=True, blank=True)
	
	# External Services
	roku_support = models.BooleanField(default=True)
	
	# System Features
	live_feed_enable = models.BooleanField(default=True)
	tv_special_enable = models.BooleanField(default=True)
	language_enable = models.BooleanField(default=True)

	created = models.DateTime(auto_now_add=True)
	updated = models.DateTime(auto_now=True)
	class Meta:
		ordering = ['-version']
		def __unicode__(self):
			return self.id
	def __str__(self):
		return str(self.id)
