import os
import uuid
import datetime
#from datetime import date,time
from django.db import models
from django.urls import reverse
from time import strftime

### Models for the Roku Content Feed based on the Roku Direct Publisher specification.
## Roku channels do not have to conform to the RDP spec but it is recommended.
## Roku Direct Publisher Feed specification:
## https://developer.roku.com/en-ca/docs/specs/direct-publisher-feed-specs/json-dp-spec.md

## References:
# JSON Schema Draft 4:   http://json-schema.org/draft/2020-12/json-schema-core.html
# ISO 8601:              http://www.iso.org/iso/home/standards/iso8601.htm
# JSON Schema Validator: http://www.jsonschemavalidator.net/
# JSON Schema Lint:      https://jsonschemalint.com/#!/version/draft-07/markup/json
# ISO 639.2 Codes:       https://www.loc.gov/standards/iso639-2/php/code_list.php


### Roku content feed

class RokuContentFeed(models.Model):
	"""
	Model for Roku Content JSON Feed. Top level JSON data structure for the entire content feed.

	{
	"providerName": "Roku Media Productions",
	"lastUpdated": "2015-08-08T11:16:00+00:00",
	"language": "en",
	"categories": [ ... ],
	"playlists": [ ... ],
	"movies": [	...	],
	"liveFeeds": [ ... ],
	"series": [	...	],
	"shortFormVideos": [ ... ],
	"tvSpecials": [ ...	]
	}

	"""
	provider_name = models.CharField(max_length=50, default="", null=False, blank=False)
	# The date that the feed was last modified in ISO 8601 format: {YYYY}-{MM}-{DD}T{hh}:{mm}:{ss}+{TZ}.
	# For example, 2020-11-11T22:21:37+00:00
	#              YYYY-MM-DDTHH:MM:SS+?:?
	last_updated = models.DateTimeField(auto_now=True)
	language = models.ForeignKey('Language', on_delete=models.PROTECT, null=False, blank=False)
	rating = models.ForeignKey('Rating', on_delete=models.PROTECT, null=False, blank=False)
	categories = models.ManyToManyField('Category', through='RokuContentFeedCategory', blank=True)
	playlists = models.ManyToManyField('Playlist', through='RokuContentFeedPlaylist', blank=True)
	movies = models.ManyToManyField('Movie', through='RokuContentFeedMovie', blank=True)
	live_feeds = models.ManyToManyField('LiveFeed', through='RokuContentFeedLiveFeed', blank=True)
	series = models.ManyToManyField('Series', through='RokuContentFeedSeries', blank=True)
	short_form_videos = models.ManyToManyField('ShortFormVideo', through='RokuContentFeedShortFormVideo', blank=True)
	tv_specials = models.ManyToManyField('TVSpecial', through='RokuContentFeedTVSpecial', blank=True)
	# !Roku
	roku_content_feed_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
	short_description = models.CharField(max_length=200, default="", null=False, blank=True)
	created = models.DateTimeField(auto_now_add=True)
	is_public = models.BooleanField(default=False)
	def get_absolute_url(self):
		return reverse('rokucontentfeed-list')
	class Meta:
		ordering = ['id']
		def __unicode__(self):
			return self.id
	def __str__(self):
		return str(self.provider_name)

class RokuContentFeedCategory(models.Model):
	""" ManyToMany table for Roku Content Feed model and Category model. """
	roku_content_feed = models.ForeignKey('RokuContentFeed', on_delete=models.CASCADE)
	category = models.ForeignKey('Category', on_delete=models.CASCADE)
	class Meta:
		def __unicode__(self):
			return self.roku_content_feed

class RokuContentFeedPlaylist(models.Model):
	""" ManyToMany table for Roku Content Feed model and Playlist model. """
	roku_content_feed = models.ForeignKey('RokuContentFeed', on_delete=models.CASCADE)
	playlist = models.ForeignKey('Playlist', on_delete=models.CASCADE)

class RokuContentFeedMovie(models.Model):
	""" ManyToMany table for Roku Content Feed model and Movie model. """
	roku_content_feed = models.ForeignKey('RokuContentFeed', on_delete=models.CASCADE)
	movie = models.ForeignKey('Movie', on_delete=models.CASCADE)

class RokuContentFeedLiveFeed(models.Model):
	""" ManyToMany table for Roku Content Feed model and Live Feed model. """
	roku_content_feed = models.ForeignKey('RokuContentFeed', on_delete=models.CASCADE)
	live_feed = models.ForeignKey('LiveFeed', on_delete=models.CASCADE)

class RokuContentFeedSeries(models.Model):
	""" ManyToMany table for Roku Content Feed model and Series model. """
	roku_content_feed = models.ForeignKey('RokuContentFeed', on_delete=models.CASCADE)
	series = models.ForeignKey('Series', on_delete=models.CASCADE)

class RokuContentFeedShortFormVideo(models.Model):
	""" ManyToMany table for Roku Content Feed model and Short-Form Video model. """
	roku_content_feed = models.ForeignKey('RokuContentFeed', on_delete=models.CASCADE)
	short_form_video = models.ForeignKey('ShortFormVideo', on_delete=models.CASCADE)

class RokuContentFeedTVSpecial(models.Model):
	""" ManyToMany table for Roku Content Feed model and TV Special model. """
	roku_content_feed = models.ForeignKey('RokuContentFeed', on_delete=models.CASCADE)
	tv_special = models.ForeignKey('TVSpecial', on_delete=models.CASCADE)


### Content Categories

CONTENT_CATEGORY_ORDER = (
	("manual", "Manual"),
	("most_recent", "Most Recent"),
	("chronological", "Chronological"),
	("most_popular", "Most Popular"),
)

class Category(models.Model):
	"""
	The Category object defines a new category your channel will display, and the content 
	included in it based either on a playlist, or a query containing one or multiple tags. 
	There are three default categories in every channel: "Continue Watching", "Most Popular", 
	and "Recently Added". Each category is displayed as a separate row to end-users.

	NOTE: A Category must contain either a playlistName or query field.

	Category object example (query):
	{
	"name": "Cooking Shows",
	"query": "cooking AND reality shows",
	"order": "most_popular"
	}

	Category object example (playlist):
	{
	"name": "Featured",
	"playlistName": "featured content",
	"order": "manual"
	}
	"""
	# The category name that will show up in the channel.
	category_name = models.CharField(max_length=128, default="", null=False, blank=False, \
		help_text="The name of the category that will show up in the channel.")
	# The name of the playlist in this feed that contains the content for this category.
	playlist_name = models.ForeignKey('Playlist', on_delete=models.PROTECT, null=True, blank=True, \
		help_text="The name of the playlist in this feed that contains the content for this category.")
	# The query that will specify the content for this category.
	# Tags: "movie AND dramas", "action OR dramas".
	query_string = models.CharField(max_length=1024, default="", null=True, blank=True, \
		help_text="The query that will specify the content for this category. Please see documentation for correct query syntax.")
	# The order of the category in the channel.
	order = models.CharField(max_length=16, choices=CONTENT_CATEGORY_ORDER, default='most_recent', \
		null=False, blank=False, help_text="The order of content displayed within the category.")
	def get_absolute_url(self):
		return reverse('category-list')
	class Meta:
		ordering = ['category_name']
		def __unicode__(self):
			return self.id
	def __str__(self):
		return str(self.category_name)


class Playlist(models.Model):
	"""
	A Playlist is an ordered list of videos that may contain a mix of Movies, Series, 
	Short-form videos, and TV Specials. It references a list of video IDs that are defined 
	elsewhere in the feed. The same video can be referenced in multiple playlists.
	Playlists are similar to tags: they help define the content that a channel's categories 
	will display. The main difference is that playlists enable the order of the content to be 
	manually specified; therefore, playlists are ideal for creating a "Featured" category in 
	a channel.
	"""
	playlist_name = models.CharField(max_length=50, default="", null=False, blank=False)
	# List of mixed Movies, Series, Short Form Videos, TV Specials.
#	item_ids = models.JSONField(default=list, null=True, blank=True, 
#		help_text='An ordered list of one or more UUIDs from a Movie, Series, Short-Form Video or TV Show.')
	item_ids = models.ManyToManyField('ShortFormVideo', through='PlaylistShortFormVideo', blank=True, \
		help_text='Currently only Short-Form Videos can be added to a playlist.')
	# !Roku
	short_description = models.CharField(max_length=200, default="", null=True, blank=True)
	updated = models.DateTimeField(auto_now=True)
	created = models.DateTimeField(auto_now_add=True)
	def get_absolute_url(self):
		return reverse('playlist-list')
	class Meta:
		ordering = ['playlist_name']
		def __unicode__(self):
			return self.id
	def __str__(self):
		return str(self.playlist_name)

class PlaylistShortFormVideo(models.Model):
	playlist = models.ForeignKey('Playlist', on_delete=models.CASCADE)
	short_form_video = models.ForeignKey('ShortFormVideo', on_delete=models.CASCADE)


### Content Types

def thumb_path(instance, filename):
	file_uuid = instance.uuid_id
	file_ext = os.path.splitext(filename)[1]
	file_path = str(file_uuid) + file_ext
	return 'thumbs/{0}/{1}/{2}/{3}'.format(datetime.datetime.now().strftime('%Y'), \
		datetime.datetime.now().strftime('%m'), \
		datetime.datetime.now().strftime('%d'), file_path)

def branded_thumb_path(instance, filename):
	file_uuid = instance.uuid_id
	file_ext = os.path.splitext(filename)[1]
	file_path = "branded_" + str(file_uuid) + file_ext
	return 'thumbs/{0}/{1}/{2}/{3}'.format(datetime.datetime.now().strftime('%Y'), \
		datetime.datetime.now().strftime('%m'), \
		datetime.datetime.now().strftime('%d'), file_path)


class Movie(models.Model):
	"""
	Represents a Movie object. Movies have content attached with one or more videos. 
	Movie objects are added to a Roku Content Feed.
	"""
	uuid_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
	title = models.CharField(max_length=50, default="", null=False, blank=False)
	short_description = models.CharField(max_length=200, default="", null=False, blank=False, \
		help_text="200 characters maximum.")
	long_description = models.CharField(max_length=500, default="", null=False, blank=True, \
		help_text="500 characters maximum.")
	content = models.ForeignKey('Content', on_delete=models.PROTECT, null=True, blank=True, related_name="movies")
	thumbnail = models.ImageField(max_length=4096, upload_to=thumb_path, \
		height_field='thumbnail_height', width_field='thumbnail_width', null=True, blank=True, \
		help_text="URL to the thumbnail image. Image dimensions must be at least 800x450 (16x9 aspect ratio).")
	#thumbnail_url = models.URLField(max_length=2083, null=False, blank=False, \
	#	help_text="URL to the thumbnail image. Image dimensions must be at least 800x450 (16x9 aspect ratio).")
	thumbnail_width = models.PositiveSmallIntegerField(default=0, null=True, blank=True)
	thumbnail_height = models.PositiveSmallIntegerField(default=0, null=True, blank=True)
	release_date = models.DateField(default="2023-01-01", null=True, blank=True, help_text="Date format: YYYY-MM-DD")
	genres = models.ManyToManyField('Genre', through='MovieGenre', blank=True, related_name="movies")
	rating = models.ForeignKey('Rating', on_delete=models.PROTECT, blank=True, null=True, related_name="movies")
	tags = models.ManyToManyField('Tag', through='MovieTag', blank=True, related_name="movies")
	credits = models.ManyToManyField('Credit', through='MovieCredit', blank=True, related_name="movies")
	external_ids = models.ManyToManyField('ExternalID', through='MovieExternalID', blank=True, related_name="movies")
	def get_absolute_url(self):
		return reverse('movie-list')
	class Meta:
		ordering = ['title']
		def __unicode__(self):
			return self.id
	def __str__(self):
		return str(self.title)

class MovieGenre(models.Model):
	""" ManyToMany table for Movie model and Genre model. """
	movie = models.ForeignKey('Movie', on_delete=models.CASCADE)
	genre = models.ForeignKey('Genre', on_delete=models.CASCADE)

class MovieTag(models.Model):
	""" ManyToMany table for Movie model and Tag model. """
	movie = models.ForeignKey('Movie', on_delete=models.CASCADE)
	tag = models.ForeignKey('Tag', on_delete=models.CASCADE)

class MovieCredit(models.Model):
	""" ManyToMany table for Movie model and Credit model. """
	movie = models.ForeignKey('Movie', on_delete=models.CASCADE)
	credit = models.ForeignKey('Credit', on_delete=models.CASCADE)

class MovieExternalID(models.Model):
	""" ManyToMany table for Movie model and ExternalID model. """
	movie = models.ForeignKey('Movie', on_delete=models.CASCADE)
	external_id = models.ForeignKey('ExternalID', on_delete=models.CASCADE)


class LiveFeed(models.Model):
	""" Represents a live linear stream. """
	uuid_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
	title = models.CharField(max_length=50, default="", null=False, blank=False)
	short_description = models.CharField(max_length=200, default="", null=False, blank=False, \
		help_text="200 characters maximum.")
	long_description = models.CharField(max_length=500, default="", null=False, blank=True, \
		help_text="500 characters maximum.")
	content = models.ForeignKey('Content', on_delete=models.PROTECT, null=True, blank=True)
	thumbnail = models.ImageField(max_length=4096, upload_to=thumb_path, \
		height_field='thumbnail_height', width_field='thumbnail_width', null=True, blank=True, \
		help_text="URL to the thumbnail image. Image dimensions must be at least 800x450 (16x9 aspect ratio).")
	thumbnail_width = models.PositiveSmallIntegerField(default=0, null=True, blank=True)
	thumbnail_height = models.PositiveSmallIntegerField(default=0, null=True, blank=True)
	# thumbnail_url = models.URLField(max_length=2083, null=False, blank=False, \
	# 	help_text="URL to the main thumbnail image. Image dimensions must be at least 800x450 (16x9 aspect ratio).")
	branded_thumbnail = models.ImageField(max_length=4096, upload_to=branded_thumb_path, \
		height_field='branded_thumbnail_height', width_field='branded_thumbnail_width', null=True, blank=True, \
		help_text="URL to the thumbnail image. Image dimensions must be at least 800x450 (16x9 aspect ratio).")
	branded_thumbnail_width = models.PositiveSmallIntegerField(default=0, null=True, blank=True)
	branded_thumbnail_height = models.PositiveSmallIntegerField(default=0, null=True, blank=True)
	# branded_thumbnail_url = models.URLField(max_length=2083, null=False, blank=False, \
	# 	help_text="URL to the branded thumbnail image. It is a secondary thumbnail. Image dimensions must be at least 800x450 (16x9 aspect ratio).")
	tags = models.CharField(max_length=200, default="", null=True, blank=True) # Optional
	rating = models.ForeignKey('Rating', on_delete=models.PROTECT, blank=True, null=True)
	genres = models.ManyToManyField('Genre', through='LiveFeedGenre', blank=True)
	def get_absolute_url(self):
		return reverse('livefeed-list')
	class Meta:
		ordering = ['uuid_id']
		def __unicode__(self):
			return self.id
	def __str__(self):
		return str(self.title)

class LiveFeedGenre(models.Model):
	""" ManyToMany table for Series model and Genre model. """
	livefeed = models.ForeignKey('LiveFeed', on_delete=models.CASCADE)
	genre = models.ForeignKey('Genre', on_delete=models.CASCADE)


class Series(models.Model):
	""" Represents a Series, such as a Season of a TV Show or a Mini-Series. """
	uuid_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
	title = models.CharField(max_length=50, default="", null=False, blank=False)
	short_description = models.CharField(max_length=200, default="", null=False, blank=False, \
		help_text="200 characters maximum.")
	long_description = models.CharField(max_length=500, default="", null=False, blank=True, \
		help_text="500 characters maximum.")
	seasons = models.ManyToManyField('Season', through='SeriesSeason', blank=True, \
		help_text="One or more seasons of the series. Seasons should be used if episodes are grouped by seasons.")
	episodes = models.ManyToManyField('Episode', through='SeriesEpisode', blank=True, \
		help_text="One or more episodes of the series. Episodes should be used if they are not grouped by seasons.")
	genres = models.ManyToManyField('Genre', through='SeriesGenre', blank=True)
	thumbnail = models.ImageField(max_length=4096, upload_to=thumb_path, \
		height_field='thumbnail_height', width_field='thumbnail_width', null=True, blank=True, \
		help_text="URL to the thumbnail image. Image dimensions must be at least 800x450 (16x9 aspect ratio).")
	thumbnail_width = models.PositiveSmallIntegerField(default=0, null=True, blank=True)
	thumbnail_height = models.PositiveSmallIntegerField(default=0, null=True, blank=True)
	# thumbnail_url = models.URLField(max_length=2083, null=False, blank=False, \
	# 	help_text="URL to the thumbnail image. Image dimensions must be at least 800x450 (16x9 aspect ratio).")
	release_date = models.DateField(default="2023-01-01", null=True, blank=True, help_text="Date format: YYYY-MM-DD")
	tags = models.CharField(max_length=200, null=True, blank=True) # Optional
	credits = models.ManyToManyField('Credit', through='SeriesCredit', blank=True) # Optional
	external_ids = models.ManyToManyField('ExternalID', through='SeriesExternalID', blank=True) # Optional
	def get_absolute_url(self):
		return reverse('series-list')
	class Meta:
		ordering = ['uuid_id']
		def __unicode__(self):
			return self.id
	def __str__(self):
		return str(self.title)

class SeriesGenre(models.Model):
	""" ManyToMany table for Series model and Genre model. """
	series = models.ForeignKey('Series', on_delete=models.CASCADE)
	genre = models.ForeignKey('Genre', on_delete=models.CASCADE)

class SeriesSeason(models.Model):
	""" ManyToMany table for Series model and Season model. """
	series = models.ForeignKey('Series', on_delete=models.CASCADE)
	season = models.ForeignKey('Season', on_delete=models.CASCADE)

class SeriesEpisode(models.Model):
	""" ManyToMany table for Series model and Episode model. """
	series = models.ForeignKey('Series', on_delete=models.CASCADE)
	episode = models.ForeignKey('Episode', on_delete=models.CASCADE)

class SeriesCredit(models.Model):
	""" ManyToMany table for Series model and Credit model. """
	series = models.ForeignKey('Series', on_delete=models.CASCADE)
	credit = models.ForeignKey('Credit', on_delete=models.CASCADE)

class SeriesExternalID(models.Model):
	""" ManyToMany table for Series model and ExternalID model. """
	series = models.ForeignKey('Series', on_delete=models.CASCADE)
	externalid = models.ForeignKey('ExternalID', on_delete=models.CASCADE)


class Season(models.Model):
	"""
	Represents a single Season of a Series.
	{
	"seasonNumber": "1",
	"episodes": [ ... ]
	}
	"""
	title_season = models.CharField(max_length=50, default="", null=False, blank=False)
	season_number = models.PositiveSmallIntegerField(default=1, null=False, blank=False)
	# One or more episodes of this particular season.
	episodes = models.ManyToManyField('Episode', through='SeasonEpisode', \
		help_text='Multiple episodes can be selected for each season.')
	def get_absolute_url(self):
		return reverse('season-list')
	class Meta:
		ordering = ['id']
		def __unicode__(self):
			return self.id
	def __str__(self):
		return str(self.season_number)

class SeasonEpisode(models.Model):
	""" ManyToMany table for Season model and Episode model. """
	season = models.ForeignKey('Season', on_delete=models.CASCADE)
	episode = models.ForeignKey('Episode', on_delete=models.CASCADE)


class Episode(models.Model):
	""" This Model represents a single Episode in a Series or a Season. """
	uuid_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
	title = models.CharField(max_length=50, default="", null=False, blank=False)
	short_description = models.CharField(max_length=200, default="", null=False, blank=False, \
		help_text="200 characters maximum.")
	long_description = models.CharField(max_length=500, default="", null=False, blank=True, \
		help_text="500 characters maximum.")
	content = models.ForeignKey('Content', on_delete=models.PROTECT, null=True, blank=True)
	thumbnail = models.ImageField(max_length=4096, upload_to=thumb_path, \
		height_field='thumbnail_height', width_field='thumbnail_width', null=True, blank=True, \
		help_text="URL to the thumbnail image. Image dimensions must be at least 800x450 (16x9 aspect ratio).")
	thumbnail_width = models.PositiveSmallIntegerField(default=0, null=True, blank=True)
	thumbnail_height = models.PositiveSmallIntegerField(default=0, null=True, blank=True)
	# thumbnail_url = models.URLField(max_length=2083, null=False, blank=False, \
	# 	help_text="URL to the thumbnail image. Image dimensions must be at least 800x450 (16x9 aspect ratio).")
	release_date = models.DateField(default="2023-01-01", null=True, blank=True, help_text="Date format: YYYY-MM-DD")
	episode_number = models.PositiveSmallIntegerField(default=1, null=False, blank=False)
	credits = models.ManyToManyField('Credit', through='EpisodeCredit', blank=True) # Optional
	rating = models.ForeignKey('Rating', on_delete=models.PROTECT, blank=False, null=False)
	external_ids = models.ManyToManyField('ExternalID', through='EpisodeExternalID', blank=True) # Optional
	def get_absolute_url(self):
		return reverse('episode-list')
	class Meta:
		ordering = ['id']
		def __unicode__(self):
			return self.id
	def __str__(self):
		return str(self.title)

class EpisodeCredit(models.Model):
	""" ManyToMany table for Episode model and Credit model. """
	episode = models.ForeignKey('Episode', on_delete=models.CASCADE)
	credit = models.ForeignKey('Credit', on_delete=models.CASCADE)

class EpisodeExternalID(models.Model):
	""" ManyToMany table for Episode model and ExternalID model. """
	episode = models.ForeignKey('Episode', on_delete=models.CASCADE)
	externalid = models.ForeignKey('ExternalID', on_delete=models.CASCADE)


class ShortFormVideo(models.Model):
	""" Short-Form Videos are generally less than 15 minutes long, and are not TV Shows or Movies. """
	# An immutable string reference ID for the video that does not exceed 50 characters. 
	# This should serve as a unique identifier for the episode across different locales.
	uuid_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
	# The title of the video in plain text. This field is used for matching in Roku Search. 
	# Do not include extra information such as year, version label, and so on.
	title = models.CharField(max_length=50, default="", null=False, blank=False)
	# A description of the video that does not exceed 200 characters. 
	# The text will be clipped if longer.
	short_description = models.CharField(max_length=200, null=False, blank=False, \
		help_text="200 characters maximum.")
	# A description of the video that does not exceed 200 characters. 
	# The text will be clipped if longer.
	long_description = models.CharField(max_length=500, default="", null=False, blank=True, \
		help_text="500 characters maximum.")
	# The video content, such as the URL of the video file, subtitles, and so on.
	content = models.ForeignKey('Content', on_delete=models.PROTECT, null=True, blank=True)
	# The URL of the thumbnail for the video. This is used within your channel and in search results.
	# Image dimensions must be at least 800x450 (width x height, 16x9 aspect ratio).
	thumbnail = models.ImageField(max_length=4096, upload_to=thumb_path, \
		height_field='thumbnail_height', width_field='thumbnail_width', null=True, blank=True, \
		help_text="URL to the thumbnail image. Image dimensions must be at least 800x450 (16x9 aspect ratio).")
	thumbnail_width = models.PositiveSmallIntegerField(default=0, null=True, blank=True)
	thumbnail_height = models.PositiveSmallIntegerField(default=0, null=True, blank=True)
	# thumbnail_url = models.URLField(max_length=2083, null=False, blank=False, \
	# 	help_text="URL to the thumbnail image. Image dimensions must be at least 800x450 (16x9 aspect ratio).")
	# The date the video first became available.
	# This field is used to sort programs chronologically and group related content in Roku Search. 
	# Conforms to ISO 8601 format: {YYYY}-{MM}-{DD}. For example, 2020-11-11
	release_date = models.DateField(default="2023-01-01", null=True, blank=True, help_text="Date format: YYYY-MM-DD")
	# One or more tags (e.g., “dramas”, “korean”, etc). 
	# Each tag is a string and is limited to 20 characters. 
	# Tags are used to define what content will be shown within a category.
	tags = models.CharField(max_length=200, null=True, blank=True) # Optional
	# A list of strings describing the genre(s) of the video.
	# Must be one of the values listed in genres.
	genres = models.ManyToManyField('Genre', through='ShortFormVideoGenre', blank=True)
	# One or more credits. The cast and crew of the video.
	credits = models.ManyToManyField('Credit', through='ShortFormVideoCredit', blank=True)
	# A parental rating for the content.
	rating = models.ForeignKey('Rating', on_delete=models.PROTECT, blank=True, null=True)  # Optional
	def get_absolute_url(self):
		return reverse('shortformvideo-list')
	# def get_uuid(self):
	# 	return str(self.uuid_id)
	class Meta:
		ordering = ['uuid_id']
		def __unicode__(self):
			return self.id
	def __str__(self):
		#return str(self.title) + ":" + str(self.uuid_id)
		return str(self.id)

class ShortFormVideoGenre(models.Model):
	""" ManyToMany table for ShortFormVideo model and Genre model. """
	shortformvideo = models.ForeignKey('ShortFormVideo', on_delete=models.CASCADE)
	genre = models.ForeignKey('Genre', on_delete=models.CASCADE)

class ShortFormVideoCredit(models.Model):
	""" ManyToMany table for ShortFormVideo model and Credit model. """
	shortformvideo = models.ForeignKey('ShortFormVideo', on_delete=models.CASCADE)
	credit = models.ForeignKey('Credit', on_delete=models.CASCADE)


class TVSpecial(models.Model):
	""" TV Specials (TV Shows) are usually 30 or 60 minutes. Special ad rules apply. """
	uuid_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
	title = models.CharField(max_length=50, default="", null=False, blank=False)
	short_description = models.CharField(max_length=200, default="", null=False, blank=False, \
		help_text="200 characters maximum.")
	long_description = models.CharField(max_length=500, default="", null=False, blank=True, \
		help_text="500 characters maximum.")
	content = models.ForeignKey('Content', on_delete=models.PROTECT, null=True, blank=True)
	thumbnail = models.ImageField(max_length=4096, upload_to=thumb_path, \
		height_field='thumbnail_height', width_field='thumbnail_width', null=True, blank=True, \
		help_text="URL to the thumbnail image. Image dimensions must be at least 800x450 (16x9 aspect ratio).")
	thumbnail_width = models.PositiveSmallIntegerField(default=0, null=True, blank=True)
	thumbnail_height = models.PositiveSmallIntegerField(default=0, null=True, blank=True)
	# thumbnail_url = models.URLField(max_length=2083, null=False, blank=False, \
	# 	help_text="URL to the thumbnail image. Image dimensions must be at least 800x450 (16x9 aspect ratio).")
	genres = models.ManyToManyField('Genre', through='TVSpecialGenre', blank=True)
	release_date = models.DateField(default="2023-01-01", null=True, blank=True, help_text="Date format: YYYY-MM-DD")
	rating = models.ForeignKey('Rating', on_delete=models.PROTECT, null=False, blank=False)
	tags = models.CharField(max_length=200, null=True, blank=True) # Optional
	credits = models.ManyToManyField('Credit', through='TVSpecialCredit', blank=True) # Optional
	external_ids = models.ManyToManyField('ExternalID', through='TVSpecialExternalID', blank=True) # Optional
	def get_absolute_url(self):
		return reverse('tvspecial-list')
	class Meta:
		ordering = ['uuid_id']
		def __unicode__(self):
			return self.id
	def __str__(self):
		return str(self.title)

class TVSpecialGenre(models.Model):
	""" ManyToMany table for TVSpecial model and Genre model. """
	tvspecial = models.ForeignKey('TVSpecial', on_delete=models.CASCADE)
	genre = models.ForeignKey('Genre', on_delete=models.CASCADE)

class TVSpecialCredit(models.Model):
	""" ManyToMany table for TVSpecial model and Credit model. """
	tvspecial = models.ForeignKey('TVSpecial', on_delete=models.CASCADE)
	credit = models.ForeignKey('Credit', on_delete=models.CASCADE)

class TVSpecialExternalID(models.Model):
	""" ManyToMany table for TVSpecial model and ExternalID model. """
	tvspecial = models.ForeignKey('TVSpecial', on_delete=models.CASCADE)
	externalid = models.ForeignKey('ExternalID', on_delete=models.CASCADE)


### Content Properties

class Content(models.Model):
	""" 
	The Content model represents the details about a single video content
	item such as a Movie, Episode, Short-Form Video, or TV Show.
	"""
	title = models.CharField(max_length=50, default="", null=False, blank=False, help_text="The title should be unique.")
	date_added = models.DateField(auto_now_add=True)
	videos = models.ManyToManyField('Video', through='ContentVideo', blank=True)
	duration = models.IntegerField(default=0, null=False, blank=True, help_text="The video duration must be in seconds.")
	captions = models.ManyToManyField('Caption', through='ContentCaption', blank=True)
	trick_play_files = models.ManyToManyField('TrickPlayFile', through='ContentTrickPlayFile', blank=True) # Optional
	language = models.ForeignKey('Language', on_delete=models.PROTECT, null=True, blank=True)
	validity_start_period = models.DateField(null=True, blank=True, help_text="Date format: YYYY-MM-DD", db_index=True) # Optional
	validity_end_period = models.DateField(null=True, blank=True, help_text="Date format: YYYY-MM-DD", db_index=True) # Optional
	ad_breaks = models.JSONField(default=list, null=True, blank=True) # NOT SUPPORTED. Required only if monetizing.
	updated = models.DateField(auto_now=True)
	def get_absolute_url(self):
		return reverse('content-list')
	class Meta:
		ordering = ['id']
		def __unicode__(self):
			return self.id
	def __str__(self):
		return str(self.title)

class ContentVideo(models.Model):
	content = models.ForeignKey('Content', on_delete=models.CASCADE)
	video = models.ForeignKey('Video', on_delete=models.CASCADE)

class ContentCaption(models.Model):
	content = models.ForeignKey('Content', on_delete=models.CASCADE)
	caption = models.ForeignKey('Caption', on_delete=models.CASCADE)

class ContentTrickPlayFile(models.Model):
	content = models.ForeignKey('Content', on_delete=models.CASCADE)
	trick_play_files = models.ForeignKey('TrickPlayFile', on_delete=models.CASCADE)

class Language(models.Model):
	""" Model for any models containing a language field. """
	code_iso_639_2 = models.CharField(max_length=8, null=False, blank=False, unique=True)  # "eng"
	code_iso_639_1 = models.CharField(max_length=8, null=False, blank=False)  # "en"
	language_name_eng = models.CharField(max_length=64, null=False, blank=False)  # English"
	def get_absolute_url(self):
		return reverse('language-list')
	class Meta:
		ordering = ['id']
		def __unicode__(self):
			return self.id
	def __str__(self):
		return str(self.code_iso_639_1)


VIDEO_QUALITY = (
	("SD", "SD (Standard Definition, <720p)"),
	("HD", "HD (High Definition, 720p)"),
	("FHD", "FHD (Full HD, 1080p)"),
	("UHD", "UHD (4K)"),
)

class Video(models.Model):
	"""
	Represents the details of a single video file. 
	The preferred videoType format is HLS (at minimum, DASH should be used).
	
	{
	"url": "https://example.org/cdn/videos/1509428502952", 
	"quality": "UHD", 
	"videoType": "HLS"
	}
	"""
	url = models.URLField(max_length=2083, null=False, blank=False, unique=True)
	quality = models.CharField(max_length=16, choices=VIDEO_QUALITY, default='HD', null=False, blank=False)
	video_type = models.ForeignKey('VideoType', on_delete=models.PROTECT, null=False, blank=False)
	#content_item = models.ForeignKey('Content', on_delete=models.PROTECT, null=True, blank=True, \
	#	help_text="Select the Content item where this video will be used.")
	def get_absolute_url(self):
		return reverse('video-list')
	class Meta:
		ordering = ['id']
		def __unicode__(self):
			return self.id
	def __str__(self):
		return str(self.url)

class VideoType(models.Model):
	video_type_short = models.CharField(max_length=16, default="", null=False, blank=False)
	video_type_long = models.CharField(max_length=50, null=True, blank=True)
	class Meta:
		ordering = ['video_type_short']
		def __unicode__(self):
			return self.id
	def __str__(self):
		return str(self.video_type_short) #+ " (" + str(self.video_type_long) + ")"

CAPTION_TYPE = (
	("CLOSED_CAPTION", "CLOSED_CAPTION"),
	("SUBTITLE", "SUBTITLE"),
)

class Caption(models.Model):
	"""
	Represents a single video caption file of a video content.
	The supported formats are described in Closed Caption Support.
	The preferred closed caption formats are: WebVTT, SRT.
	
	{
	"url": "https://example.org/cdn/subtitles/1509428502952/sub-fr.srt",
	"language": "fr", 
	"captionType": "CLOSED_CAPTION"
	}
	"""
	url = models.URLField(max_length=2083, null=False, blank=False, unique=True)
	language = models.ForeignKey('Language', on_delete=models.PROTECT, null=True, blank=True)
	caption_type = models.CharField(max_length=16, choices=CAPTION_TYPE, default='CLOSED_CAPTION', null=False, blank=False)
	def get_absolute_url(self):
		return reverse('caption-list')
	class Meta:
		ordering = ['id']
		def __unicode__(self):
			return self.id
	def __str__(self):
		return str(self.url)

TRICK_QUALITY = (
	("HD", "HD (720p)"),
	("FHD", "FHD (1080p)"),
)

# Trickplay files should be created during content ingest.
# https://developer.roku.com/en-gb/docs/developer-program/media-playback/trick-mode/bif-file-creation.md
class TrickPlayFile(models.Model):
	"""
	Represents a single trickplay file. Trickplay files are the images shown 
	when a user scrubs through a video, either fast-forwarding or rewinding. 
	The file must be in the Roku BIF format.

	{
	"url": "https://example.org/cdn/trickplayFiles/1509428502952/1", 
	"quality": "FHD"
	}

	Trick mode provides visual feedback during playback operations such as seek, forward, and rewind. 
	This function lets a user visualize the timestamp of the content they are seeking. The Roku platform 
	supports two types of trick mode. For channels generating and publishing image archives in the 
	Roku BIF (Base Index Frame), HLS, or DASH standard file formats, a scene-based trick mode using 
	index frames is supported. When the thumbnails necessary to support scene-based trick mode are 
	not available at playback time, a time-based method of supporting trick modes is used instead.

	Channels must display thumbnails during trick play for VOD content longer than 15 minutes to pass certification.
	"""
	url = models.URLField(max_length=2083, null=False, blank=False, unique=True)
	quality = models.CharField(max_length=16, choices=TRICK_QUALITY, default="HD", null=False, blank=False)
	def get_absolute_url(self):
		return reverse('trickplayfile-list')
	class Meta:
		ordering = ['id']
		def __unicode__(self):
			return self.id
	def __str__(self):
		return str(self.url)

class Genre(models.Model):
	"""	Provides a list of Roku content specific genres. Maximum length of 30 characters. """
	genre = models.CharField(max_length=30, default="", null=False, blank=False, unique=True)
	def get_absolute_url(self):
		return reverse('genre-list')
	class Meta:
		ordering = ['genre']
		def __unicode__(self):
			return self.id
	def __str__(self):
		return str(self.genre)

class ExternalID(models.Model):
	"""
	The third-party metadata provider ID for the video content.

	{
	"id": "tt0371724", 
	"idType": "IMDB"
	}
	"""
	external_id = models.CharField(max_length=16, default="", null=False, blank=False)
	id_type = models.ForeignKey('ExternalIDType', on_delete=models.PROTECT, blank=True, null=True)
	def get_absolute_url(self):
		return reverse('externalid-list')
	class Meta:
		ordering = ['id']
		def __unicode__(self):
			return self.id
	def __str__(self):
		return str(self.external_id) + " (" + str(self.id_type) + ")"

class ExternalIDType(models.Model):
	""" 
	List of third-party external ID types.
	Typically the name of a company providing metadata services. 
	"""
	external_id_type = models.CharField(max_length=16, default="", null=False, blank=False, unique=True)
	external_id_long_name = models.CharField(max_length=50, default="", null=True, blank=True)
	class Meta:
		ordering = ['external_id_type']
		def __unicode__(self):
			return self.id
	def __str__(self):
		return str(self.external_id_type)

class Rating(models.Model):
	"""
	Represents the rating for the video content. The parental rating, as well as 
	the source must be defined (for example, USA Parental Rating, UK Content Provider, 
	and so on). See Parental Ratings and Rating Sources for acceptable values.

	{
	"rating": "PG", 
	"ratingSource": "MPAA"
	}
	"""
	rating = models.ForeignKey('ParentalRating', on_delete=models.PROTECT, null=False, blank=False)
	rating_source = models.ForeignKey('RatingSource', on_delete=models.PROTECT, null=False, blank=False)
	def get_absolute_url(self):
		return reverse('rating-list')
	class Meta:
		ordering = ['rating']
		def __unicode__(self):
			return self.id
	def __str__(self):
		return str(self.rating) + " (" + str(self.rating_source) + ")"

class RatingSource(models.Model):
	""" Model provides a list of rating sources, such as the Motion Picture Association (MPA). """
	source_name = models.CharField(max_length=16, default="", null=False, blank=False, unique=True)
	source_long_name = models.CharField(max_length=128, null=True, blank=True)
	source_url = models.URLField(max_length=2083, null=True, blank=True)
	source_country = models.ForeignKey('Country', on_delete=models.PROTECT, null=False, blank=True)
	def get_absolute_url(self):
		return reverse('ratingsource-list')
	class Meta:
		ordering = ['source_name']
		def __unicode__(self):
			return self.id
	def __str__(self):
		return str(self.source_name)

class Country(models.Model):
	""" List of all global countries with country code."""
	country_name = models.CharField(max_length=64, default="", null=False, blank=False, unique=True)
	country_code = models.CharField(max_length=2, default="", null=False, blank=False, unique=True)	
	class Meta:
		ordering = ['country_name']
		def __unicode__(self):
			return self.id
	def __str__(self):
		return str(self.country_code)

class ParentalRating(models.Model):
	""" Model provides a list of parental ratings as determined by standards associations. """
	parental_rating = models.CharField(max_length=16, default="", null=False, blank=False, unique=True)
	def get_absolute_url(self):
		return reverse('parentalrating-list')
	class Meta:
		ordering = ['parental_rating']
		def __unicode__(self):
			return self.id
	def __str__(self):
		return str(self.parental_rating)

class CreditRole(models.Model):
	""" Represents a role of the person credited in video content. """
	credit_role = models.CharField(max_length=50, default="", null=False, blank=False)
	def get_absolute_url(self):
		return reverse('creditrole-list')
	class Meta:
		ordering = ['credit_role']
		def __unicode__(self):
			return self.id
	def __str__(self):
		return str(self.credit_role)

class Credit(models.Model):
	"""
	Represents a single person in the credits of a video content.

	{
	"name": "Douglas N. Adams", 
	"role": "screenwriter", 
	"birthDate": "1952-03-11"
	}
	"""
	credit_name = models.CharField(max_length=50, default="", null=False, blank=False)
	role = models.ForeignKey('CreditRole', on_delete=models.PROTECT, null=False, blank=False)
	birth_date = models.CharField(max_length=10, default="2023-01-01", null=False, blank=False, \
		help_text = "Please use the following birth date format: YYYY-MM-DD.")
	def get_absolute_url(self):
		return reverse('credit-list')
	class Meta:
		ordering = ['credit_name']
		def __unicode__(self):
			return self.id
	def __str__(self):
		return str(self.credit_name)

# Catch all for Tags
class Tag(models.Model):
	tag_name = models.CharField(max_length=20, default="", null=False, blank=False, unique=True, \
		help_text="Max length 20 characters. Enter a new tag that hasn't been added yet.")
	def get_absolute_url(self):
		return reverse('tag-list')
	class Meta:
		ordering = ['tag_name']
		def __unicode__(self):
			return self.id
	def __str__(self):
		return str(self.tag_name)
