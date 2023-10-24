from datetime import datetime
from rest_framework import serializers
from rest_framework.renderers import JSONRenderer
from rest_framework.permissions import IsAdminUser

from .models import RokuContentFeed
from .models import Language, Category, Playlist
from .models import Movie, LiveFeed, Series, Season, Episode, ShortFormVideo, TVSpecial
from .models import Content, Video, Caption, TrickPlayFile, Genre, ExternalID, Rating, \
					RatingSource, ParentalRating, Credit, Tag

### Roku Feeds

# This class provides the data used to populate the Roku channel menus and content
class RokuContentFeedSerializerList(serializers.ModelSerializer):
	providerName = serializers.CharField(source='provider_name')
	lastUpdated = serializers.DateTimeField(source='last_updated')
	shortFormVideos = serializers.StringRelatedField(source='short_form_videos')
	tvSpecials = serializers.StringRelatedField(source='tv_specials')
	language = serializers.StringRelatedField()
	rating = serializers.StringRelatedField()
	class Meta:
		model = RokuContentFeed
		fields = ['providerName', 'language', 'rating', 'lastUpdated', \
			'movies', 'series', 'shortFormVideos', 'tvSpecials', 'categories', 'playlists']
		depth = 2

### Content Categories

class CategorySerializerList(serializers.ModelSerializer):
	category = serializers.JSONField(source='category_name')
	playlist = serializers.JSONField(source='playlist_name')
	class Meta:
		model = Category
		fields = ['id', 'category', 'playlist', 'query_string', 'order']
		#fields = '__all__'  ## provide all fields

class PlaylistSerializerList(serializers.ModelSerializer):
	name = serializers.CharField(source='playlist_name')
	itemIds = serializers.JSONField(source='item_ids')
	class Meta:
		model = Playlist
		fields = ['name', 'itemIds']

class LanguageSerializerList(serializers.ModelSerializer):
	class Meta:
		model = Language
		fields = ['code_iso_639_2', 'code_iso_639_1', 'language_name_eng']


### Content Types

class MovieSerializerList(serializers.ModelSerializer):
	id = serializers.UUIDField(source='movie_id')
	rating = serializers.StringRelatedField()
	class Meta:
		model = Movie
		fields = ['id', 'title', 'short_description', 'long_description', 'content', \
			'genres', 'thumbnail', 'release_date', 'tags', 'rating', 'credits', 'external_ids']

class LiveFeedSerializerList(serializers.ModelSerializer):
	id = serializers.UUIDField(source='livefeed_id')
	genres = serializers.StringRelatedField()
	rating = serializers.StringRelatedField()
	class Meta:
		model = LiveFeed
		fields = ['id', 'title', 'short_description', 'long_description', 'content', \
			'thumbnail', 'branded_thumbnail', 'tags', 'genres', 'rating']

class SeriesSerializerList(serializers.ModelSerializer):
	id = serializers.UUIDField(source='series_id')
	genres = serializers.StringRelatedField()
	class Meta:
		model = Series
		fields = ['id', 'title', 'short_description', 'long_description', 'seasons', \
		'episodes', 'thumbnail', 'release_date', 'tags', 'genres', 'credits', 'external_ids']

class SeasonSerializerList(serializers.ModelSerializer):
	class Meta:
		model = Season
		fields = ['season_number', 'episodes']

class EpisodeSerializerList(serializers.ModelSerializer):
	id = serializers.UUIDField(source='episode_id')
	#content = serializers.StringRelatedField()
	#credits = serializers.StringRelatedField()
	rating = serializers.StringRelatedField()
	externalIds = serializers.StringRelatedField(source='external_ids')
	class Meta:
		model = Episode
		fields = ['id', 'episode_number', 'title', 'short_description', 'long_description', 'content', \
			'thumbnail', 'release_date', 'rating', 'credits', 'externalIds']

class ShortFormVideoSerializerList(serializers.ModelSerializer):
	id = serializers.UUIDField(source='short_form_video_id')
	genres = serializers.StringRelatedField()
	rating = serializers.StringRelatedField()
	class Meta:
		model = ShortFormVideo
		fields = ['id', 'title', 'short_description', 'long_description','content', \
			'thumbnail', 'release_date', 'tags', 'genres', 'rating', 'credits']

class TVSpecialSerializerList(serializers.ModelSerializer):
	id = serializers.UUIDField(source='tv_special_id')
	genres = serializers.StringRelatedField()
	rating = serializers.StringRelatedField()
	class Meta:
		model = TVSpecial
		fields = ['id', 'title', 'short_description', 'long_description', 'content', \
			'thumbnail', 'release_date', 'tags', 'genres', 'rating', 'credits', 'external_ids']


### Content Properties

class ContentSerializerList(serializers.ModelSerializer):
	dateAdded = serializers.DateField(source='date_added')
	trickPlayFiles = serializers.JSONField(source='trick_play_files')
	validityPeriodStart = serializers.DateField(source='validity_start_period')
	validityPeriodEnd = serializers.DateField(source='validity_end_period')
	#adBreaks = serializers.CharField(source='ad_breaks')  # Advertising not supported
	class Meta:
		model = Content
		fields = ['dateAdded', 'videos', 'duration', 'captions', 'trickPlayFiles', \
			'language', 'validityPeriodStart', 'validityPeriodEnd']

class VideoSerializerList(serializers.ModelSerializer):
	videoType = serializers.CharField(source='video_type')
	class Meta:
		model = Video
		fields = ['url', 'quality', 'videoType']

class CaptionSerializerList(serializers.ModelSerializer):
	captionType = serializers.CharField(source='caption_type')
	class Meta:
		model = Caption
		fields = ['url', 'language', 'caption_type']

class TrickPlayFileSerializerList(serializers.ModelSerializer):
	class Meta:
		model = TrickPlayFile
		fields = ['url', 'quality']

class GenreSerializerList(serializers.ModelSerializer):
	class Meta:
		model = Genre
		fields = ['genre']

class ExternalIDSerializerList(serializers.ModelSerializer):
	id = serializers.CharField(source='external_id')
	idType = serializers.CharField(source='id_type')
	class Meta:
		model = ExternalID
		fields = ['id', 'external_id', 'idType']

class RatingSerializerList(serializers.ModelSerializer):
	rating = serializers.StringRelatedField()
	ratingSource = serializers.CharField(source='rating_source')
	class Meta:
		model = Rating
		fields = ['rating', 'ratingSource']

class RatingSourceSerializerList(serializers.ModelSerializer):
	ratingSource = serializers.CharField(source='source_name')
	class Meta:
		model = RatingSource
		fields = ['ratingSource', 'source_long_name']

class ParentalRatingSerializerList(serializers.ModelSerializer):
	class Meta:
		model = ParentalRating
		fields = ['parental_rating']

class CreditSerializerList(serializers.ModelSerializer):
	name = serializers.CharField(source='credit_name')
	birthDate = serializers.CharField(source='birth_date')
	role = serializers.StringRelatedField()
	class Meta:
		model = Credit
		fields = ['name', 'role', 'birthDate']

class TagSerializerList(serializers.ModelSerializer):
	class Meta:
		model = Tag
		fields = ['tag_name']
