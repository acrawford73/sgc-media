import uuid
import datetime,time
from django.db import models
from django.urls import reverse

## For the Roku Direct Publisher Feed info check this website:
# https://developer.roku.com/en-ca/docs/specs/direct-publisher-feed-specs/json-dp-spec.md

## References:
# JSON Schema Draft 4:   http://json-schema.org/draft/2020-12/json-schema-core.html
# ISO 8601:              http://www.iso.org/iso/home/standards/iso8601.htm
# JSON Schema Validator: http://www.jsonschemavalidator.net/
# JSON Schema Lint:      https://jsonschemalint.com/#!/version/draft-07/markup/json
# ISO 639.2 Codes:       https://www.loc.gov/standards/iso639-2/php/code_list.php


### Roku search feed

class RokuSearchFeed(models.Model):
	provider_name = models.CharField(max_length=32, null=False, blank=False)
	last_updated = models.DateTimeField(auto_now_add=True)
	language = models.ForeignKey("Language", on_delete=models.PROTECT, null=False, blank=False)
	rating = models.ForeignKey("Rating", on_delete=models.PROTECT, null=False, blank=False)
	categories = models.ForeignKey("Category", on_delete=models.PROTECT, null=True, blank=True)
	playlists = models.ForeignKey("Playlist", on_delete=models.PROTECT, limit_choices_to={"is_public": True}, null=True, blank=True)
	movies = models.ForeignKey("Movie", on_delete=models.PROTECT, null=True, blank=True)
	live_feeds = models.ForeignKey("LiveFeed", on_delete=models.PROTECT, null=True, blank=True)
	series = models.ForeignKey("Series", on_delete=models.PROTECT, null=True, blank=True)
	short_form_videos = models.ForeignKey("ShortFormVideo", on_delete=models.PROTECT, null=True, blank=True)
	tv_specials = models.ForeignKey("TVSpecial", on_delete=models.PROTECT, null=True, blank=True)
	# !Roku
	short_description = models.CharField(max_length=200, default="", null=True, blank=True)
	is_public = models.BooleanField(default=False)
	class Meta:
		ordering = ['id']
		def __unicode__(self):
			return self.id
	def __str__(self):
		return str(self.id)