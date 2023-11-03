from datetime import datetime
from rest_framework import serializers
from rest_framework.renderers import JSONRenderer
from rest_framework.permissions import IsAdminUser

from .models import RokuContentFeed
from .models import Language, Category, Playlist
from .models import Movie, LiveFeed, Series, Season, Episode, ShortFormVideo, TVSpecial
from .models import Content, Video, Caption, TrickPlayFile, Genre, ExternalID, Rating, \
					RatingSource, ParentalRating, CreditRole, Credit, Tag


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
	videos = VideoSerializerList(many=True)
	captions = CaptionSerializerList(many=True)
	#trickPlayFiles = TrickPlayFileSerializerList(many=True, source='trick_play_files')
	language = serializers.StringRelatedField()
	#validityPeriodStart = serializers.DateField(source='validity_start_period')
	#validityPeriodEnd = serializers.DateField(source='validity_end_period')
	#adBreaks = serializers.CharField(source='ad_breaks')  # Advertising not supported
	class Meta:
		model = Content
		fields = ['dateAdded', 'videos', 'duration', 'captions', 'language']
			# 'trickPlayFiles', validityPeriodStart', 'validityPeriodEnd']

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

class CreditRoleSerializerList(serializers.ModelSerializer):
	role = serializers.CharField(source='credit_role')
	class Meta:
		model = CreditRole
		fields = ['role']

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
	releaseDate = serializers.DateField(source='release_date')
	content = ContentSerializerList()
	genres = serializers.StringRelatedField()
	tags = TagSerializerList(many=True)
	rating = RatingSerializerList()
	credits = CreditSerializerList(many=True)
	externalIds = ExternalIDSerializerList(many=True, source='external_ids')
	class Meta:
		model = Movie
		fields = ['id', 'title', 'shortDescription', 'longDescription', 'content', \
			'thumbnail', 'releaseDate', 'genres', 'tags', 'rating', 'credits', 'externalIds']

class LiveFeedSerializerList(serializers.ModelSerializer):
	id = serializers.UUIDField(source='livefeed_id')
	shortDescription = serializers.CharField(source='short_description')
	longDescription = serializers.CharField(source='long_description')
	brandedThumbnail = serializers.URLField(source='branded_thumbnail')
	content = ContentSerializerList()
	tags = serializers.StringRelatedField()
	genres = serializers.StringRelatedField()
	rating = RatingSerializerList()
	class Meta:
		model = LiveFeed
		fields = ['id', 'title', 'shortDescription', 'longDescription', 'content', \
			'thumbnail', 'brandedThumbnail', 'tags', 'genres', 'rating']

class EpisodeSerializerList(serializers.ModelSerializer):
	id = serializers.UUIDField(source='episode_id')
	episodeNumber = serializers.IntegerField(source='episode_number')
	shortDescription = serializers.CharField(source='short_description')
	longDescription = serializers.CharField(source='long_description')
	releaseDate = serializers.DateField(source='release_date')
	content = ContentSerializerList()
	rating = RatingSerializerList()
	credits = CreditSerializerList(many=True)
	externalIds = ExternalIDSerializerList(many=True, source='external_ids')
	class Meta:
		model = Episode
		fields = ['id', 'episodeNumber', 'title', 'shortDescription', 'longDescription', 'content', \
			'thumbnail', 'releaseDate', 'rating', 'credits', 'externalIds']

class SeasonSerializerList(serializers.ModelSerializer):
	episodes = EpisodeSerializerList(many=True)
	class Meta:
		model = Season
		fields = ['season_number', 'episodes']

class SeriesSerializerList(serializers.ModelSerializer):
	id = serializers.UUIDField(source='series_id')
	shortDescription = serializers.CharField(source='short_description')
	longDescription = serializers.CharField(source='long_description')
	releaseDate = serializers.DateField(source='release_date')
	tags = serializers.StringRelatedField()
	seasons = SeasonSerializerList(many=True)
	episodes = EpisodeSerializerList(many=True)
	genres = serializers.StringRelatedField()
	credits = CreditSerializerList(many=True)
	externalIds = ExternalIDSerializerList(many=True, source='external_ids')
	class Meta:
		model = Series
		fields = ['id', 'title', 'shortDescription', 'longDescription', 'seasons', \
		'episodes', 'thumbnail', 'releaseDate', 'tags', 'genres', 'credits', 'externalIds']

class ShortFormVideoSerializerList(serializers.ModelSerializer):
	id = serializers.UUIDField(source='short_form_video_id')
	shortDescription = serializers.CharField(source='short_description')
	longDescription = serializers.CharField(source='long_description')
	releaseDate = serializers.DateField(source='release_date')
	rating = RatingSerializerList()
	genres = serializers.StringRelatedField()
	content = ContentSerializerList()
	credits = CreditSerializerList(many=True)
	class Meta:
		model = ShortFormVideo
		fields = ['id', 'title', 'shortDescription', 'longDescription','content', \
			'thumbnail', 'releaseDate', 'tags', 'genres', 'rating', 'credits']

class TVSpecialSerializerList(serializers.ModelSerializer):
	id = serializers.UUIDField(source='tv_special_id')
	shortDescription = serializers.CharField(source='short_description')
	longDescription = serializers.CharField(source='long_description')
	releaseDate = serializers.DateField(source='release_date')
	tags = serializers.StringRelatedField()
	genres = serializers.StringRelatedField()
	rating = RatingSerializerList()
	content = ContentSerializerList()
	credits = CreditSerializerList(many=True)
	externalIds = ExternalIDSerializerList(many=True, source='external_ids')
	class Meta:
		model = TVSpecial
		fields = ['id', 'title', 'shortDescription', 'longDescription', 'content', \
			'thumbnail', 'releaseDate', 'tags', 'genres', 'rating', 'credits', 'externalIds']


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
	"""
	Serializer List class for Roku Content Feed. The data is used to display Roku channel menus populate them with content.
	"""
	providerName = serializers.CharField(source='provider_name')
	language = serializers.StringRelatedField()
	rating = RatingSerializerList()
	lastUpdated = serializers.DateTimeField(source='last_updated')
	movies = MovieSerializerList(many=True)
	#liveFeeds = LiveFeedSerializerList(many=True, source='live_feeds')
	series = SeriesSerializerList(many=True)
	shortFormVideos = ShortFormVideoSerializerList(many=True, source='short_form_videos')
	tvSpecials = TVSpecialSerializerList(many=True, source='tv_specials')
	categories = CategorySerializerList(many=True)
	playlists = PlaylistSerializerList(many=True)
	class Meta:
		model = RokuContentFeed
		#read_only_fields = ['is_public']
		fields = ['providerName', 'language', 'rating', 'lastUpdated', 'movies', \
			'series', 'shortFormVideos', 'tvSpecials', 'categories', 'playlists']
			#'liveFeeds', 'series', 'shortFormVideos', 'tvSpecials', 'categories', 'playlists']



class RokuContentFeedSerializerDetail(serializers.ModelSerializer):
	"""
	Serializer Detail class for Roku Content Feed.
	"""
	providerName = serializers.CharField(source='provider_name')
	language = serializers.StringRelatedField()
	rating = RatingSerializerList()
	lastUpdated = serializers.DateTimeField(source='last_updated')
	movies = MovieSerializerList(many=True)
	liveFeeds = LiveFeedSerializerList(many=True, source='live_feeds')
	series = SeriesSerializerList(many=True)
	shortFormVideos = ShortFormVideoSerializerList(many=True, source='short_form_videos')
	tvSpecials = TVSpecialSerializerList(many=True, source='tv_specials')
	categories = CategorySerializerList(many=True)
	playlists = PlaylistSerializerList(many=True)
	class Meta:
		model = RokuContentFeed
		#fields = '__all__'
		fields = ('providerName', 'language', 'rating', 'lastUpdated', 'movies', \
			'liveFeeds', 'series', 'shortFormVideos', 'tvSpecials', 'categories', 'playlists')
