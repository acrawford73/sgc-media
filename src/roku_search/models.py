import uuid
import datetime,time
from django.db import models
from django.urls import reverse
from roku_content.models import Movie, Series, Season, Episode, ShortFormVideo, TVSpecial, Content, Language
from roku_content.models import ExternalID, Rating, ParentalRating, RatingSource, Genre, Credit

## For the Roku Direct Publisher Feed info check this website:
# https://developer.roku.com/en-ca/docs/specs/direct-publisher-feed-specs/json-dp-spec.md

## References:
# JSON Schema Draft 4:   http://json-schema.org/draft/2020-12/json-schema-core.html
# ISO 8601:              http://www.iso.org/iso/home/standards/iso8601.htm
# JSON Schema Validator: http://www.jsonschemavalidator.net/
# JSON Schema Lint:      https://jsonschemalint.com/#!/version/draft-07/markup/json
# ISO 639.2 Codes:       https://www.loc.gov/standards/iso639-2/php/code_list.php


### Roku Search Feed

class SearchFeed(models.Model):
	search_feed_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, \
		help_text="There must be only ONE Search Feed. DO NOT create a second Search Feed.")
	version = models.CharField(default="1", null=False, blank=False, editable=False, \
		help_text="Search JSON Feed version is always 1.")
	default_language = models.ForeignKey('roku_content.Language', on_delete=models.PROTECT, null=False, blank=False, \
		help_text="Set the default language for the Search Feed.")
	# List, required if avilable countries for each asset are not provided
	#default_countries = models.CharField(default="en", null=False, blank=False, help_text="") 

	# !Roku
	last_updated = models.DateTimeField(auto_now=True)
	created = models.DateTimeField(auto_now_add=True)
	def get_absolute_url(self):
		return reverse('searchfeed-list')
	class Meta:
		def __unicode__(self):
			return self.search_feed_id
	def __str__(self):
		return str(self.search_feed_id)
