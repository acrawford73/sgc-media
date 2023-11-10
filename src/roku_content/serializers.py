from collections import OrderedDict

from datetime import datetime
from rest_framework import serializers
from rest_framework.renderers import JSONRenderer
from rest_framework.permissions import IsAdminUser

from .models import RokuContentFeed
from .models import Language, Category, Playlist
from .models import Movie, LiveFeed, Series, Season, Episode, ShortFormVideo, TVSpecial
from .models import Content, Video, Caption, TrickPlayFile, Genre, ExternalID, Rating, \
					RatingSource, ParentalRating, CreditRole, Credit, Tag, PlaylistShortFormVideo


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
	def to_representation(self, instance):
		result = super(CaptionSerializerList, self).to_representation(instance)
		return OrderedDict([(key, result[key]) for key in result if result[key] ])	
	class Meta:
		model = Caption
		fields = ['url', 'language', 'captionType']

class TrickPlayFileSerializerList(serializers.ModelSerializer):
	def to_representation(self, instance):
		result = super(TrickPlayFileSerializerList, self).to_representation(instance)
		return OrderedDict([(key, result[key]) for key in result if result[key] ])
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
	def to_representation(self, instance):
		result = super(ExternalIDSerializerList, self).to_representation(instance)
		return OrderedDict([(key, result[key]) for key in result if result[key] ])
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
	def to_representation(self, instance):
		result = super(CreditSerializerList, self).to_representation(instance)
		return OrderedDict([(key, result[key]) for key in result if result[key] ])
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
	def to_representation(self, instance):
		result = super(MovieSerializerList, self).to_representation(instance)
		return OrderedDict([(key, result[key]) for key in result if result[key] ])
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
	def to_representation(self, instance):
		result = super(LiveFeedSerializerList, self).to_representation(instance)
		return OrderedDict([(key, result[key]) for key in result if result[key] ])
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
	def to_representation(self, instance):
		result = super(EpisodeSerializerList, self).to_representation(instance)
		return OrderedDict([(key, result[key]) for key in result if result[key] ])
	class Meta:
		model = Episode
		fields = ['id', 'episodeNumber', 'title', 'shortDescription', 'longDescription', 'content', \
			'thumbnail', 'releaseDate', 'rating', 'credits', 'externalIds']

class SeasonSerializerList(serializers.ModelSerializer):
	titleSeason = serializers.CharField(source='title_season')
	seasonNumber = serializers.IntegerField(source="season_number")
	episodes = EpisodeSerializerList(many=True)
	class Meta:
		model = Season
		fields = ['titleSeason', 'seasonNumber', 'episodes']

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
	def to_representation(self, instance):
		result = super(SeriesSerializerList, self).to_representation(instance)
		return OrderedDict([(key, result[key]) for key in result if result[key] ])
	class Meta:
		model = Series
		fields = ['id', 'title', 'shortDescription', 'longDescription', 'seasons', \
		'episodes', 'thumbnail', 'releaseDate', 'tags', 'genres', 'credits', 'externalIds']

class ShortFormVideoSerializerList(serializers.ModelSerializer):
	#id = serializers.UUIDField(source='short_form_video_id')
	shortDescription = serializers.CharField(source='short_description')
	longDescription = serializers.CharField(source='long_description')
	releaseDate = serializers.DateField(source='release_date')
	rating = RatingSerializerList()
	genres = serializers.StringRelatedField()
	content = ContentSerializerList()
	credits = CreditSerializerList(many=True)
	def to_representation(self, instance):
		result = super(ShortFormVideoSerializerList, self).to_representation(instance)
		return OrderedDict([(key, result[key]) for key in result if result[key] ])
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
	def to_representation(self, instance):
		result = super(TVSpecialSerializerList, self).to_representation(instance)
		return OrderedDict([(key, result[key]) for key in result if result[key] ])
	class Meta:
		model = TVSpecial
		fields = ['id', 'title', 'shortDescription', 'longDescription', 'content', \
			'thumbnail', 'releaseDate', 'tags', 'genres', 'rating', 'credits', 'externalIds']


### Content Categoriess

class CategorySerializerList(serializers.ModelSerializer):
	name = serializers.StringRelatedField(source='category_name')
	playlistName = serializers.StringRelatedField(source='playlist_name')
	query = serializers.StringRelatedField(source='query_string')
	def to_representation(self, instance):
		result = super(CategorySerializerList, self).to_representation(instance)
		return OrderedDict([(key, result[key]) for key in result if result[key] ])
	class Meta:
		model = Category
		fields = ['name', 'playlistName', 'query', 'order']

class PlaylistSerializerList(serializers.ModelSerializer):
	name = serializers.CharField(source='playlist_name')
	itemIds = serializers.StringRelatedField(many=True, source='item_ids') #PrimaryKeyRelatedField(many=True, read_only=True, source='item_ids')
	def to_representation(self, instance):
		result = super(PlaylistSerializerList, self).to_representation(instance)
		return OrderedDict([(key, result[key]) for key in result if result[key] ])
	class Meta:
		model = Playlist
		fields = ['name', 'itemIds']


### Roku Feeds

# This class provides the data used to populate the Roku channel menus and content
class RokuContentFeedSerializerList(serializers.ModelSerializer):
	"""
	Serializer List class for Roku Content Feed. 
	The data is used to display Roku channel menus and populate them with content.
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
	def to_representation(self, instance):
		result = super(RokuContentFeedSerializerList, self).to_representation(instance)
		return OrderedDict([(key, result[key]) for key in result if result[key] ])
	class Meta:
		model = RokuContentFeed
		fields = ['providerName', 'language', 'rating', 'lastUpdated', 'movies', \
			'liveFeeds', 'series', 'shortFormVideos', 'tvSpecials', 'categories', 'playlists']


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
	playlists = PlaylistSerializerList(many=True)
	categories = CategorySerializerList(many=True)
	class Meta:
		model = RokuContentFeed
		#fields = '__all__'
		fields = ('providerName', 'language', 'rating', 'lastUpdated', 'movies', \
			'liveFeeds', 'series', 'shortFormVideos', 'tvSpecials', 'playlists', 'categories')


# # None field will be removed
# class NonNullModelSerializer(serializers.ModelSerializer):
# 	def to_representation(self, instance):
# 		result = super(NonNullModelSerializer, self).to_representation(instance)
# 		return OrderedDict([(key, result[key]) for key in result if result[key] is not None])


# # None & Blank field will be removed
# class ValueBasedModelSerializer(serializers.ModelSerializer):
# 	def to_representation(self, instance):
# 		result = super(ValueBasedModelSerializer, self).to_representation(instance)
# 		return OrderedDict([(key, result[key]) for key in result if result[key] ])


### HTTP Status Codes
### https://www.django-rest-framework.org/api-guide/status-codes/

# Informational - 1xx
# This class of status code indicates a provisional response. 
# There are no 1xx status codes used in REST framework by default.
# HTTP_100_CONTINUE
# HTTP_101_SWITCHING_PROTOCOLS

# Successful - 2xx
# This class of status code indicates that the client's request was successfully received, understood, and accepted.
# HTTP_200_OK
# HTTP_201_CREATED
# HTTP_202_ACCEPTED
# HTTP_203_NON_AUTHORITATIVE_INFORMATION
# HTTP_204_NO_CONTENT
# HTTP_205_RESET_CONTENT
# HTTP_206_PARTIAL_CONTENT
# HTTP_207_MULTI_STATUS
# HTTP_208_ALREADY_REPORTED
# HTTP_226_IM_USED

# Redirection - 3xx
# This class of status code indicates that further action needs to be taken by the user agent
# in order to fulfill the request.
# HTTP_300_MULTIPLE_CHOICES
# HTTP_301_MOVED_PERMANENTLY
# HTTP_302_FOUND
# HTTP_303_SEE_OTHER
# HTTP_304_NOT_MODIFIED
# HTTP_305_USE_PROXY
# HTTP_306_RESERVED
# HTTP_307_TEMPORARY_REDIRECT
# HTTP_308_PERMANENT_REDIRECT

# Client Error - 4xx
# The 4xx class of status code is intended for cases in which the client seems to have erred. 
# Except when responding to a HEAD request, the server SHOULD include an entity containing an 
# explanation of the error situation, and whether it is a temporary or permanent condition.
# HTTP_400_BAD_REQUEST
# HTTP_401_UNAUTHORIZED
# HTTP_402_PAYMENT_REQUIRED
# HTTP_403_FORBIDDEN
# HTTP_404_NOT_FOUND
# HTTP_405_METHOD_NOT_ALLOWED
# HTTP_406_NOT_ACCEPTABLE
# HTTP_407_PROXY_AUTHENTICATION_REQUIRED
# HTTP_408_REQUEST_TIMEOUT
# HTTP_409_CONFLICT
# HTTP_410_GONE
# HTTP_411_LENGTH_REQUIRED
# HTTP_412_PRECONDITION_FAILED
# HTTP_413_REQUEST_ENTITY_TOO_LARGE
# HTTP_414_REQUEST_URI_TOO_LONG
# HTTP_415_UNSUPPORTED_MEDIA_TYPE
# HTTP_416_REQUESTED_RANGE_NOT_SATISFIABLE
# HTTP_417_EXPECTATION_FAILED
# HTTP_422_UNPROCESSABLE_ENTITY
# HTTP_423_LOCKED
# HTTP_424_FAILED_DEPENDENCY
# HTTP_426_UPGRADE_REQUIRED
# HTTP_428_PRECONDITION_REQUIRED
# HTTP_429_TOO_MANY_REQUESTS
# HTTP_431_REQUEST_HEADER_FIELDS_TOO_LARGE
# HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS

# Server Error - 5xx
# Response status codes beginning with the digit "5" indicate cases in which the server is aware 
# that it has erred or is incapable of performing the request. Except when responding to a HEAD request, 
# the server SHOULD include an entity containing an explanation of the error situation, 
# and whether it is a temporary or permanent condition.
# HTTP_500_INTERNAL_SERVER_ERROR
# HTTP_501_NOT_IMPLEMENTED
# HTTP_502_BAD_GATEWAY
# HTTP_503_SERVICE_UNAVAILABLE
# HTTP_504_GATEWAY_TIMEOUT
# HTTP_505_HTTP_VERSION_NOT_SUPPORTED
# HTTP_506_VARIANT_ALSO_NEGOTIATES
# HTTP_507_INSUFFICIENT_STORAGE
# HTTP_508_LOOP_DETECTED
# HTTP_509_BANDWIDTH_LIMIT_EXCEEDED
# HTTP_510_NOT_EXTENDED
# HTTP_511_NETWORK_AUTHENTICATION_REQUIRED

# Helper functions
# The following helper functions are available for identifying the category of the response code.
#  is_informational()  # 1xx
#  is_success()        # 2xx
#  is_redirect()       # 3xx
#  is_client_error()   # 4xx
#  is_server_error()   # 5xx
