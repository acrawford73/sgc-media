from datetime import datetime
from rest_framework import serializers
from rest_framework.renderers import JSONRenderer
from rest_framework.permissions import IsAdminUser

from .models import RokuContentFeed
from .models import Language, Category, Playlist
from .models import Movie, LiveFeed, Series, Season, Episode, ShortFormVideo, TVSpecial
from .models import Content, Video, Caption, TrickPlayFile, Genre, ExternalID, Rating, \
					RatingSource, ParentalRating, Credit, CreditRole, Tag


class LanguageSerializerList(serializers.ModelSerializer):
	class Meta:
		model = Language
		fields = ['code_iso_639_2', 'code_iso_639_1', 'language_name_eng']


### Content Properties

class VideoSerializerList(serializers.ModelSerializer):
	videoType = serializers.CharField(source='video_type')
	class Meta:
		model = Video
		fields = ['url', 'quality', 'videoType']

class CaptionSerializerList(serializers.ModelSerializer):
	captionType = serializers.CharField(source='caption_type')
	language = serializers.StringRelatedField()
	class Meta:
		model = Caption
		fields = ['url', 'language', 'captionType']

class TrickPlayFileSerializerList(serializers.ModelSerializer):
	class Meta:
		model = TrickPlayFile
		fields = ['url', 'quality']

class ContentSerializerList(serializers.ModelSerializer):
	dateAdded = serializers.DateField(source='date_added')
	trickPlayFiles = TrickPlayFileSerializerList(many=True, source='trick_play_files')
	videos = VideoSerializerList(many=True)
	captions = CaptionSerializerList(many=True)
	language = serializers.StringRelatedField()
	#validityPeriodStart = serializers.DateField(source='validity_start_period')
	#validityPeriodEnd = serializers.DateField(source='validity_end_period')
	#adBreaks = serializers.CharField(source='ad_breaks')  # Advertising not supported
	class Meta:
		model = Content
		fields = ['dateAdded', 'videos', 'duration', 'captions', 'trickPlayFiles', \
			'language'] #, 'validityPeriodStart', 'validityPeriodEnd']

class GenreSerializerList(serializers.ModelSerializer):
	class Meta:
		model = Genre
		fields = ['genre']

class ExternalIDSerializerList(serializers.ModelSerializer):
	id = serializers.CharField(source='external_id')
	idType = serializers.CharField(source='id_type')
	class Meta:
		model = ExternalID
		fields = ['id', 'idType']

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


### Content Types

class MovieSerializerList(serializers.ModelSerializer):
	id = serializers.UUIDField(source='movie_id')
	shortDescription = serializers.CharField(source='short_description')
	longDescription = serializers.CharField(source='long_description')
	content = ContentSerializerList(many=True)
	genres = serializers.StringRelatedField()
	tags = TagSerializerList(many=True)
	rating = RatingSerializerList()
	credits = CreditSerializerList(many=True)
	externalIds = ExternalIDSerializerList(many=True, source='external_ids')
	class Meta:
		model = Movie
		fields = ['id', 'title', 'shortDescription', 'longDescription', 'content', \
			'thumbnail', 'release_date', 'genres', 'tags', 'rating', 'credits', 'externalIds']

class LiveFeedSerializerList(serializers.ModelSerializer):
	id = serializers.UUIDField(source='livefeed_id')
	shortDescription = serializers.CharField(source='short_description')
	longDescription = serializers.CharField(source='long_description')
	content = ContentSerializerList(many=True)
	tags = serializers.StringRelatedField()
	genres = serializers.StringRelatedField()
	rating = RatingSerializerList()
	class Meta:
		model = LiveFeed
		fields = ['id', 'title', 'shortDescription', 'longDescription', 'content', \
			'thumbnail', 'branded_thumbnail', 'tags', 'genres', 'rating']

class EpisodeSerializerList(serializers.ModelSerializer):
	id = serializers.UUIDField(source='episode_id')
	shortDescription = serializers.CharField(source='short_description')
	longDescription = serializers.CharField(source='long_description')
	content = ContentSerializerList(many=True)
	rating = RatingSerializerList()
	credits = CreditSerializerList(many=True)
	externalIds = ExternalIDSerializerList(many=True, source='external_ids')
	class Meta:
		model = Episode
		fields = ['id', 'episode_number', 'title', 'shortDescription', 'longDescription', 'content', \
			'thumbnail', 'release_date', 'rating', 'credits', 'externalIds']

class SeasonSerializerList(serializers.ModelSerializer):
	episodes = EpisodeSerializerList(many=True)
	class Meta:
		model = Season
		fields = ['season_number', 'episodes']

class SeriesSerializerList(serializers.ModelSerializer):
	id = serializers.UUIDField(source='series_id')
	shortDescription = serializers.CharField(source='short_description')
	longDescription = serializers.CharField(source='long_description')
	tags = serializers.StringRelatedField()
	seasons = SeasonSerializerList(many=True)
	episodes = EpisodeSerializerList(many=True)
	genres = serializers.StringRelatedField()
	credits = CreditSerializerList(many=True)
	externalIds = ExternalIDSerializerList(many=True, source='external_ids')
	class Meta:
		model = Series
		fields = ['id', 'title', 'shortDescription', 'longDescription', 'seasons', \
		'episodes', 'thumbnail', 'release_date', 'tags', 'genres', 'credits', 'externalIds']

class ShortFormVideoSerializerList(serializers.ModelSerializer):
	id = serializers.UUIDField(source='short_form_video_id')
	shortDescription = serializers.CharField(source='short_description')
	longDescription = serializers.CharField(source='long_description')
	rating = RatingSerializerList()
	genres = serializers.StringRelatedField()
	content = ContentSerializerList(many=True)
	credits = CreditSerializerList(many=True)
	class Meta:
		model = ShortFormVideo
		fields = ['id', 'title', 'shortDescription', 'longDescription','content', \
			'thumbnail', 'release_date', 'tags', 'genres', 'rating', 'credits']

class TVSpecialSerializerList(serializers.ModelSerializer):
	id = serializers.UUIDField(source='tv_special_id')
	shortDescription = serializers.CharField(source='short_description')
	longDescription = serializers.CharField(source='long_description')
	tags = serializers.StringRelatedField()
	genres = serializers.StringRelatedField()
	rating = RatingSerializerList()
	content = ContentSerializerList(many=True)
	credits = CreditSerializerList(many=True)
	externalIds = ExternalIDSerializerList(many=True, source='external_ids')
	class Meta:
		model = TVSpecial
		fields = ['id', 'title', 'shortDescription', 'longDescription', 'content', \
			'thumbnail', 'release_date', 'tags', 'genres', 'rating', 'credits', 'externalIds']


### Content Categories

class CategorySerializerList(serializers.ModelSerializer):
	name = serializers.StringRelatedField(source='category_name')
	playlistName = serializers.StringRelatedField(source='playlist_name')
	query = serializers.StringRelatedField(source='query_string')
	class Meta:
		model = Category
		fields = ['name', 'playlistName', 'query', 'order']
		#fields = '__all__'  ## provide all fields

class PlaylistSerializerList(serializers.ModelSerializer):
	name = serializers.CharField(source='playlist_name')
	itemIds = serializers.StringRelatedField(source='item_ids')
	class Meta:
		model = Playlist
		fields = ['name', 'itemIds']


### Roku Feeds

# This class provides the data used to populate the Roku channel menus and content
class RokuContentFeedSerializerList(serializers.ModelSerializer):
	providerName = serializers.CharField(source='provider_name')
	language = serializers.StringRelatedField()
	rating = RatingSerializerList()
	lastUpdated = serializers.DateTimeField(source='last_updated')
	movies = MovieSerializerList(many=True)
	series = SeriesSerializerList(many=True)
	shortFormVideos = ShortFormVideoSerializerList(many=True, source='short_form_videos') # serializers.StringRelatedField(source='short_form_videos', read_only=True)
	tvSpecials = TVSpecialSerializerList(many=True, source='tv_specials')
	categories = CategorySerializerList(many=True)
	playlists = PlaylistSerializerList(many=True)
	class Meta:
		model = RokuContentFeed
		fields = ['providerName', 'language', 'rating', 'lastUpdated', \
			'movies', 'series', 'shortFormVideos', 'tvSpecials', 'categories', 'playlists']
		#depth = 2

class RokuContentFeedSerializerDetail(serializers.ModelSerializer):
	class Meta:
		model = RokuContentFeed
		fields = '__all__'
