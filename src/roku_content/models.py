import uuid
import datetime,time
from datetime import date
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


### Roku content feed

class RokuContentFeed(models.Model):
	"""
	Model for Roku Content JSON Feed.

	Example:
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
	provider_name = models.CharField(max_length=32, null=False, blank=False)
	last_updated = models.DateTimeField(auto_now_add=True)
	language = models.ForeignKey("Language", on_delete=models.PROTECT, null=False, blank=False)
	rating = models.ForeignKey("Rating", on_delete=models.PROTECT, null=False, blank=False)
	categories = models.ForeignKey("Category", on_delete=models.PROTECT, null=True, blank=True)
	playlists = models.ForeignKey("Playlist", on_delete=models.PROTECT, limit_choices_to={"is_public": True}, null=True, blank=True)
	#movies = models.ForeignKey("Movie", on_delete=models.PROTECT, null=True, blank=True)
	#live_feeds = models.ForeignKey("LiveFeed", on_delete=models.PROTECT, null=True, blank=True)
	#series = models.ForeignKey("Series", on_delete=models.PROTECT, null=True, blank=True)
	short_form_videos = models.ForeignKey("ShortFormVideo", on_delete=models.PROTECT, null=True, blank=True)
	#tv_specials = models.ForeignKey("TVSpecial", on_delete=models.PROTECT, null=True, blank=True)
	# !Roku
	short_description = models.CharField(max_length=200, default="", null=True, blank=True)
	is_public = models.BooleanField(default=False)
	class Meta:
		ordering = ['id']
		def __unicode__(self):
			return self.id
	def __str__(self):
		return str(self.id)


### Content Categories

class Language(models.Model):
	""" Model for all models containing a language field. """
	code_iso_639_2 = models.CharField(max_length=8, null=False, blank=False)  # "eng"
	code_iso_639_1 = models.CharField(max_length=8, null=False, blank=False)  # "en"
	language_name_eng = models.CharField(max_length=64, null=False, blank=False)  # English"
	class Meta:
		ordering = ['id']
		def __unicode__(self):
			return self.id
	def __str__(self):
		return str(self.id)

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
	"""
	category_name = models.CharField(max_length=128, default="", null=False, blank=False)
	playlist_name = models.CharField(max_length=128, default="", null=True, blank=True)
	query_string = models.CharField(max_length=1024, default="", null=True, blank=True)
	order = models.CharField(max_length=16, choices=CONTENT_CATEGORY_ORDER, default='most_recent')
	class Meta:
		ordering = ['id']
		def __unicode__(self):
			return self.id
	def __str__(self):
		return str(self.id)

class Playlist(models.Model):
	"""
	A Playlist is an ordered list of videos that may contain a mix of Movies, Series, 
	Short-form videos, and TV Specials. It references a list of video IDs that are defined 
	elsewhere in the feed. The same video can be referenced in multiple playlists.
	Playlists are similar to tags: they help define the content that a channel's categories 
	will display. The main difference is that playlists enable the order of the content to be 
	manually specified; therefore, playlists are ideal for creating a "Featured" category in 
	a channel, for example.
	"""
	#playlist_id = models.PositiveBigIntegerField(primary_key=True)
	playlist_name = models.CharField(max_length=20, default="", null=False, blank=False)
	# List of mixed Movies, Series, Short Form Videos, TV Specials
	item_ids = models.JSONField(default=list, null=True, blank=True)
	# !Roku
	short_description = models.CharField(max_length=200, default="", null=True, blank=True)
	created = models.DateTimeField(auto_now_add=True)
	is_public = models.BooleanField(default=False)
	class Meta:
		ordering = ['-id']
		def __unicode__(self):
			return self.id
	def __str__(self):
		return str(self.id)


### Content Types

# class Movie(models.Model):
# 	""" Model which represents a movie object. """
# 	movie_id = models.UUIDField(default=uuid.uuid4, editable=False)
# 	title = models.CharField(max_length=64, default="", null=False, blank=False)
# 	content = models.URLField(max_length=2083, null=False, blank=False)
# 	genres = models.ForeignKey("Genre", on_delete=models.SET_NULL, blank=True, null=True)
# 	thumbnail = models.URLField(max_length=2083, null=False, blank=False)
# 	release_date = models.DateField(default=datetime.date.today(), null=True, blank=True)
# 	short_description = models.CharField(max_length=200, default="", null=False, blank=False)
# 	long_description = models.CharField(max_length=500, default="", null=False, blank=False)
# 	tags = models.CharField(max_length=200, default="", null=False, blank=False)
# 	credits = models.ForeignKey("Credit", on_delete=models.SET_NULL, blank=True, null=True) # Optional
# 	rating = models.ForeignKey("Rating", on_delete=models.SET_NULL, blank=True, null=True)
# 	# object, One or more third-party metadata provider IDs.
# 	external_ids = models.ForeignKey("ExternalID", on_delete=models.SET_NULL, blank=True, null=True) # Optional
# 	class Meta:
# 		ordering = ['movie_id']
# 		def __unicode__(self):
# 			return self.movie_id
# 	def __str__(self):
# 		return str(self.movie_id)

# class LiveFeed(models.Model):
# 	""" This Model represents a live linear stream. """
# 	livefeed_id = models.UUIDField(default=uuid.uuid4, editable=False)
# 	title = models.CharField(max_length=64, default="", null=False, blank=False)
# 	content = models.URLField(max_length=2083, null=False, blank=False)
# 	thumbnail = models.URLField(max_length=2083, null=False, blank=False)
# 	branded_thumbnail = models.URLField(max_length=2083, null=False, blank=False)
# 	short_description = models.CharField(max_length=200, default="", null=False, blank=False)
# 	long_description = models.CharField(max_length=500, default="", null=False, blank=False)
# 	tags = models.CharField(max_length=200, default="", null=True, blank=True) # Optional
# 	rating = models.ForeignKey("Rating", on_delete=models.SET_NULL, blank=True, null=True)
# 	genres = models.ForeignKey("Genre", on_delete=models.SET_NULL, blank=True, null=True) # Optional
# 	class Meta:
# 		ordering = ['livefeed_id']
# 		def __unicode__(self):
# 			return self.livefeed_id
# 	def __str__(self):
# 		return str(self.livefeed_id)

# class Series(models.Model):
# 	""" This Model represents a series, such as a season of a TV Show or a mini-series. """
# 	series_id = models.UUIDField(default=uuid.uuid4, editable=False)
# 	title = models.CharField(max_length=64, default="", null=False, blank=False)
# 	seasons = models.ForeignKey("Season", on_delete=models.SET_NULL, blank=False, null=False)
# 	episodes = models.ForeignKey("Episode", on_delete=models.SET_NULL, blank=False, null=False)
# 	genres = models.ForeignKey("Genre", on_delete=models.SET_NULL, blank=False, null=False)
# 	thumbnail = models.URLField(max_length=2083, null=False, blank=False)
# 	release_date = models.DateField(auto_now=True, null=False, blank=False)
# 	short_description = models.CharField(max_length=200, default="", null=False, blank=False)
# 	long_description = models.CharField(max_length=500, null=True, blank=True) # Optional
# 	tags = models.CharField(max_length=200, null=True, blank=True) # Optional
# 	credits = models.ForeignKey("Credit", on_delete=models.SET_NULL, blank=True, null=True) # Optional
# 	external_ids = models.ForeignKey("ExternalID", on_delete=models.SET_NULL, blank=True, null=True) # Optional
# 	class Meta:
# 		ordering = ['series_id']
# 		def __unicode__(self):
# 			return self.series_id
# 	def __str__(self):
# 		return str(self.series_id)

# class Season(models.Model):
# 	"""
# 	This Model represents a single season of a series.
# 	{
# 	  "seasonNumber": "1",
# 	  "episodes": [ ... ]
# 	}
# 	"""
# 	season_number = models.PositiveSmallIntegerField(default=1, null=False, blank=False)
# 	# One or more episodes of this particular season.
# 	episodes = models.CharField(max_length=10, null=False, blank=False)
# 	class Meta:
# 		ordering = ['id']
# 		def __unicode__(self):
# 			return self.id
# 	def __str__(self):
# 		return str(self.id)

# class Episode(models.Model):
# 	""" This Model represents a single episode in a series or a season. """
# 	episode_id = models.UUIDField(default=uuid.uuid4, editable=False)
# 	title = models.CharField(max_length=64, null=False, blank=False)
# 	content = models.URLField(max_length=2083, null=False, blank=False)
# 	thumbnail = models.URLField(max_length=2083, null=False, blank=False)
# 	release_date = models.DateField(auto_now=True, null=False, blank=False)
# 	episode_number = models.PositiveSmallIntegerField(default=1, null=False, blank=False)
# 	short_description = models.CharField(max_length=200, default="", null=False, blank=False)
# 	long_description = models.CharField(max_length=500, default="", null=False, blank=False)
# 	credits = models.ForeignKey("Credit", on_delete=models.SET_NULL, blank=True, null=True) # Optional
# 	rating = models.ForeignKey("Rating", on_delete=models.SET_NULL, blank=False, null=False)
# 	external_ids = models.ForeignKey("ExternalID", on_delete=models.SET_NULL, blank=True, null=True) # Optional
# 	class Meta:
# 		ordering = ['id']
# 		def __unicode__(self):
# 			return self.id
# 	def __str__(self):
# 		return str(self.id)

class ShortFormVideo(models.Model):
	""" Short-form videos are generally less than 15 minutes long, and are not TV Shows or Movies. """
	# An immutable string reference ID for the video that does not exceed 50 characters. 
	# This should serve as a unique identifier for the episode across different locales.
	short_form_video_id = models.UUIDField(default=uuid.uuid4, editable=False)
	# The title of the video in plain text. This field is used for matching in Roku Search. 
	# Do not include extra information such as year, version label, and so on.
	title = models.CharField(max_length=64, null=False, blank=False)
	# The video content, such as the URL of the video file, subtitles, and so on.
	content = models.URLField(max_length=2083, null=False, blank=False)
	# The URL of the thumbnail for the video. This is used within your channel and in search results.
	# Image dimensions must be at least 800x450 (width x height, 16x9 aspect ratio).
	thumbnail = models.URLField(max_length=2083, null=False, blank=False)
	# A description of the video that does not exceed 200 characters. 
	# The text will be clipped if longer.
	short_description = models.CharField(max_length=200, null=False, blank=False)
	# A description of the video that does not exceed 200 characters. 
	# The text will be clipped if longer.
	long_description = models.CharField(max_length=500, null=False, blank=False)
	# The date the video first became available.
	# This field is used to sort programs chronologically and group related content in Roku Search. 
	# Conforms to ISO 8601 format: {YYYY}-{MM}-{DD}. For example, 2020-11-11
	release_date = models.DateField(auto_now=False, default=date.today, null=True, blank=True)
	# One or more tags (e.g., “dramas”, “korean”, etc). 
	# Each tag is a string and is limited to 20 characters. 
	# Tags are used to define what content will be shown within a category.
	tags = models.CharField(max_length=200, null=True, blank=True) # Optional
	# A list of strings describing the genre(s) of the video.
	# Must be one of the values listed in genres.
	genres = models.ForeignKey("Genre", on_delete=models.PROTECT, blank=True, null=True)  # Optional
	# One or more credits. The cast and crew of the video.
	credits = models.ForeignKey("Credit", on_delete=models.PROTECT, blank=False, null=False)
	# A parental rating for the content.
	rating = models.ForeignKey("Rating", on_delete=models.PROTECT, blank=True, null=True)  # Optional
	class Meta:
		ordering = ['short_form_video_id']
		def __unicode__(self):
			return self.short_form_video_id
	def __str__(self):
		return str(self.short_form_video_id)

# class TVSpecial(models.Model):
# 	""" TV Specials are shorter or longer than 15 minutes. Special ad rules apply. """
# 	tv_special_id = models.UUIDField(default=uuid.uuid4, editable=False)
# 	title = models.CharField(max_length=64, null=False, blank=False)
# 	content = models.URLField(max_length=2083, null=False, blank=False)
# 	thumbnail = models.URLField(max_length=2083, null=False, blank=False)
# 	genres = models.ForeignKey("Genre", on_delete=models.SET_NULL, blank=True, null=True)
# 	release_date = models.DateField(auto_now=True, null=False, blank=False)
# 	short_description = models.CharField(max_length=200, default="", null=False, blank=False)
# 	long_description = models.CharField(max_length=500, default="", null=True, blank=True) # Optional
# 	credits = models.ForeignKey("Credit", on_delete=models.SET_NULL, blank=True, null=True) # Optional
# 	rating = models.ForeignKey("Rating", on_delete=models.SET_NULL, blank=False, null=False)
# 	tags = models.CharField(max_length=200, null=True, blank=True) # Optional
# 	external_ids = models.ForeignKey("ExternalID", on_delete=models.SET_NULL, blank=True, null=True) # Optional
# 	class Meta:
# 		ordering = ['tv_special_id']
# 		def __unicode__(self):
# 			return self.tv_special_id
# 	def __str__(self):
# 		return str(self.tv_special_id)


### Content Properties

LANGUAGES_ISO639 = (
	("en", "English"),
	("fr", "French"),
	("de", "German"),
	("it", "Italian"),
	("ja", "Japanese"),
	("ko", "Korean"),
	("pt", "Portuguese"),
	("ru", "Russian"),
	("es", "Spanish"),
	("zh", "Chinese"),
)

class Content(models.Model):
	""" 
	The Content object represents the details about a single video content item 
	such as a movie, episode, short-form video, or TV special.
	"""
	date_added = models.DateTimeField(auto_now_add=True)
	videos = models.ForeignKey("Video", on_delete=models.PROTECT, null=True, blank=True)
	duration = models.IntegerField(default=0, null=False, blank=True)
	captions = models.ForeignKey("Caption", on_delete=models.PROTECT, null=True, blank=True)
	trick_play_files = models.ForeignKey("TrickPlayFile", on_delete=models.PROTECT, null=True, blank=True) # Optional
	language = models.CharField(max_length=8, default="en", choices=LANGUAGES_ISO639, null=False, blank=False)
	validity_start_period = models.DateTimeField(null=True, blank=True) # Optional
	validity_end_period = models.DateTimeField(null=True, blank=True) # Optional
	ad_breaks = models.JSONField(default=list, null=True, blank=True) # Required only if monetizing
	class Meta:
		ordering = ['id']
		def __unicode__(self):
			return self.id
	def __str__(self):
		return str(self.id)

VIDEO_QUALITY = (
	("SD", "SD (Standard Definition, <720p)"),
	("HD", "HD (High Definition, 720p)"),
	("FHD", "FHD (Full HD, 1080p)"),
	("UHD", "UHD (4K)"),
)
VIDEO_TYPE = (
	("DASH", "DASH (Dynamic Adaptive Streaming over HTTP)"),
	("HLS", "HLS (HTTP Live Streaming"),
	("M4V", "M4V (MPEG-4 Apple"),
	("MOV", "MOV (Apple Quicktime"),
	("MP4", "MP4 (MPEG-4 h.264/h.265"),
	("SMOOTH", "SMOOTH"),
)

class Video(models.Model):
	"""
	This Model represents the details of a single video file. 
	The preferred videoType format is HLS (at minimum, DASH should be used).
	{
		"url": "https://example.org/cdn/videos/1509428502952", 
		"quality": "UHD", 
		"videoType": "HLS"
	}
	"""
	url = models.URLField(max_length=2083, null=False, blank=False)
	quality = models.CharField(max_length=16, choices=VIDEO_QUALITY, default='HD', null=False, blank=False)
	video_type = models.CharField(max_length=16, choices=VIDEO_TYPE, default='MP4', null=False, blank=False)
	class Meta:
		ordering = ['id']
		def __unicode__(self):
			return self.id
	def __str__(self):
		return str(self.id)

CAPTION_TYPE = (
	("CLOSED_CAPTION", "CLOSED_CAPTION"),
	("SUBTITLE", "SUBTITLE"),
)

class Caption(models.Model):
	"""
	This Model represents a single video caption file of a video content. The supported 
	formats are described in Closed Caption Support. The preferred closed caption formats 
	are: WebVTT, SRT.
	{
		"url": "https://example.org/cdn/subtitles/1509428502952/sub-fr.srt", 
		"language": "fr", 
		"captionType": "CLOSED_CAPTION"
	}
	"""
	url = models.URLField(max_length=2083, null=False, blank=False)
	language = models.CharField(max_length=16, default='en', null=False, blank=False)
	caption_type = models.CharField(max_length=16, choices=CAPTION_TYPE, default='SUBTITLE', null=False, blank=False)
	class Meta:
		ordering = ['id']
		def __unicode__(self):
			return self.id
	def __str__(self):
		return str(self.id)

TRICK_QUALITY = (
	("HD", "HD (720p)"),
	("FHD", "FHD (1080p)"),
)

class TrickPlayFile(models.Model):
	"""
	This Model represents a single trickplay file. Trickplay files are the images shown 
	when a user scrubs through a video, either fast-forwarding or rewinding. The file must 
	be in the Roku BIF format, as described in Trick Mode.
	{
		"url": "https://example.org/cdn/trickplayFiles/1509428502952/1", 
		"quality": "FHD"
	}
	"""
	url = models.URLField(max_length=2083, null=False, blank=False)
	quality = models.CharField(max_length=16, choices=TRICK_QUALITY, default="HD", null=False, blank=False)
	class Meta:
		ordering = ['id']
		def __unicode__(self):
			return self.id
	def __str__(self):
		return str(self.id)

ROKU_CONTENT_GENRES = (
	("Action", "Action"),
	("Adventure", "Adventure"),
	("Animals", "Animals"),
	("Animated", "Animated"),
	("Anime", "Anime"),
	("Children", "Children"),
	("Comedy", "Comedy"),
	("Crime", "Crime"),
	("Documentary", "Documentary"),
	("Drama", "Drama"),
	("Educational", "Educational"),
	("Fantasy", "Fantasy"),
	("Faith", "Faith"),
	("Food", "Food"),
	("Fashion", "Fashion"),
	("Gaming", "Gaming"),
	("Health", "Health"),
	("History", "History"),
	("Horror", "Horror"),
	("Miniseries", "Miniseries"),
	("Mystery", "Mystery"),
	("Nature", "Nature"),
	("News", "News"),
	("Reality", "Reality"),
	("Romance", "Romance"),
	("Science", "Science"),
	("Science Fiction", "Science Fiction"),
	("Sitcom", "Sitcom"),
	("Special", "Special"),
	("Sports", "Sports"),
	("Thriller", "Thriller"),
	("Technology", "Technology"),
)

class Genre(models.Model):
	"""	This Model provides a list of Roku platform specific genres. """
	genre = models.CharField(max_length=16, choices=ROKU_CONTENT_GENRES, default="educational", null=False, blank=False)
	class Meta:
		ordering = ['genre']
		def __str__(self):
			return str(self.genre)

EXTERNAL_ID_TYPE = (
	("TMS", "TMS (Tribune Metadata Service)"),
	("ROVI", "ROVI (Rovi ID)"),
	("IMDB", "IMDB (Internet Movie Database ID)"),
	("EIDR", "EIDR (Entertainment Identifier ID)"),
)

class ExternalID(models.Model):
	"""
	The third-party metadata provider ID for the video content.
	{
		"id": "tt0371724", 
		"idType": "IMDB"
	}
	"""
	external_id = models.CharField(max_length=16, default="0", null=False, blank=False)
	id_type = models.CharField(max_length=16, choices=EXTERNAL_ID_TYPE, default="IMDB", null=False, blank=False)
	class Meta:
		ordering = ['id']
		def __unicode__(self):
			return self.id
	def __str__(self):
		return str(self.id)

class Rating(models.Model):
	"""
	This Model represents the rating for the video content. The parental rating, as well as 
	the source must be defined (for example, USA Parental Rating, UK Content Provider, 
	and so on). See Parental Ratings and Rating Sources for acceptable values.
	{
		"rating": "PG", 
		"ratingSource": "USA_PR"
	}
	"""
	rating = models.ForeignKey("ParentalRating", on_delete=models.PROTECT, blank=True, null=True)
	rating_source = models.ForeignKey("RatingSource", on_delete=models.PROTECT, blank=True, null=True)
	class Meta:
		ordering = ['id']
		def __unicode__(self):
			return self.id
	def __str__(self):
		return str(self.id)

class RatingSource(models.Model):
	""" Model provides a list of rating sources, such as the Motion Picture Association (MPA). """
	source_name = models.CharField(max_length=16, default="", null=False, blank=False)
	source_long_name = models.CharField(max_length=128, null=True, blank=True)
	class Meta:
		ordering = ['id']
		def __unicode__(self):
			return self.id
	def __str__(self):
		return str(self.source_name)

class ParentalRating(models.Model):
	""" Model provides a list of parental ratings as determined by standards associations. """
	parental_rating = models.CharField(max_length=16, default="", null=False, blank=False, unique=True)
	class Meta:
		ordering = ['id']
		def __unicode__(self):
			return self.id
	def __str__(self):
		return str(self.parental_rating)

CREDIT_ROLES = (
	("actor", "Actor"),
	("anchor", "Anchor"),
	("director", "Director"),
	("host", "Host"),
	("narrator", "Narrator"),	
	("producer", "Producer"),
	("screenwriter", "Screenwriter"),
	("voice", "Voice"),
)

class Credit(models.Model):
	"""
	Model that represents a single person in the credits of a video content.
	{
		"name": "Douglas N. Adams", 
		"role": "screenwriter", 
		"birthDate": "1952-03-11"
	}
	"""
	credit_name = models.CharField(max_length=64, default="", null=False, blank=False)
	role = models.CharField(max_length=16, choices=CREDIT_ROLES, default="actor", null=True, blank=True)
	birth_date = models.CharField(max_length=10, default="0000-00-00", null=False, blank=False)
	class Meta:
		ordering = ['id']
		def __unicode__(self):
			return self.id
	def __str__(self):
		return str(self.id)


# Thumbnails

# class ThumbnailMovie(models.Model):
# 	""" Model for Movie thumbnail storage in database. May not be supported. """
# 	movie_id = models.ForeignKey("Movie", on_delete=CASCADE)
# 	url = models.URLField(max_length=2083, null=False, blank=False)
# 	file_path = models.CharField(max_length=4096, default="", null=False, blank=False)
# 	file_uuid = models.CharField(max_length=36, null=False, blank=False)
# 	sha256 = models.CharField(max_length=64, default="")
# 	image_data = models.TextField(default="", null=False, blank=False)
# 	class Meta:
# 		ordering = ['id']
# 		def __unicode__(self):
# 			return self.id
# 	def __str__(self):
# 		return str(self.id)

# class ThumbnailLiveFeed(models.Model):
# 	""" Model for Live Feed Thumbnail storage in database. May not be supported. """
# 	live_feed_id = models.ForeignKey("LiveFeed", on_delete=CASCADE)
# 	url = models.URLField(max_length=2083, null=False, blank=False)
# 	file_path = models.CharField(max_length=4096, default="", null=False, blank=False)
# 	file_uuid = models.CharField(max_length=36, null=False, blank=False)
# 	sha256 = models.CharField(max_length=64, default="")
# 	image_data = models.TextField(default="", null=False, blank=False)
# 	class Meta:
# 		ordering = ['id']
# 		def __unicode__(self):
# 			return self.id
# 	def __str__(self):
# 		return str(self.id)

# class ThumbnailSeries(models.Model):
# 	""" Model for Series thumbnail storage in database. May not be supported. """
# 	series_id = models.ForeignKey("Series", on_delete=CASCADE)
# 	url = models.URLField(max_length=2083, null=False, blank=False)
# 	file_path = models.CharField(max_length=4096, default="", null=False, blank=False)
# 	file_uuid = models.CharField(max_length=36, null=False, blank=False)
# 	sha256 = models.CharField(max_length=64, default="")
# 	image_data = models.TextField(default="", null=False, blank=False)
# 	class Meta:
# 		ordering = ['id']
# 		def __unicode__(self):
# 			return self.id
# 	def __str__(self):
# 		return str(self.id)

# class ThumbnailEpisode(models.Model):
# 	""" Model for Episode thumbnail storage in database. May not be supported. """
# 	episode_id = models.ForeignKey("Episode", on_delete=CASCADE)
# 	url = models.URLField(max_length=2083, null=False, blank=False)
# 	file_path = models.CharField(max_length=4096, default="", null=False, blank=False)
# 	file_uuid = models.CharField(max_length=36, null=False, blank=False)
# 	sha256 = models.CharField(max_length=64, default="")
# 	image_data = models.TextField(default="", null=False, blank=False)
# 	class Meta:
# 		ordering = ['id']
# 		def __unicode__(self):
# 			return self.id
# 	def __str__(self):
# 		return str(self.id)

class ThumbnailShortFormVideo(models.Model):
	""" Model for Short Form Video thumbnail storage in database. May not be supported. """
	short_form_video_id = models.ForeignKey("ShortFormVideo", on_delete=models.CASCADE)
	url = models.URLField(max_length=2083, null=False, blank=False)
	file_path = models.CharField(max_length=4096, default="", null=False, blank=False)
	file_uuid = models.CharField(max_length=36, null=False, blank=False)
	sha256 = models.CharField(max_length=64, default="")
	image_data = models.TextField(default="", null=False, blank=False)
	class Meta:
		ordering = ['id']
		def __unicode__(self):
			return self.id
	def __str__(self):
		return str(self.id)

# class ThumbnailTVSpecial(models.Model):
# 	""" Model for TV Special thumbnail storage in database. May not be supported. """
# 	tv_special_id = models.ForeignKey("TVSpecial", on_delete=CASCADE)
# 	url = models.URLField(max_length=2083, null=False, blank=False)
# 	file_path = models.CharField(max_length=4096, default="", null=False, blank=False)
# 	file_uuid = models.CharField(max_length=36, null=False, blank=False)
# 	sha256 = models.CharField(max_length=64, default="")
# 	image_data = models.TextField(default="", null=False, blank=False)
# 	class Meta:
# 		ordering = ['id']
# 		def __unicode__(self):
# 			return self.id
# 	def __str__(self):
# 		return str(self.id)
