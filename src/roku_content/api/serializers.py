from datetime import datetime
from collections import OrderedDict

from rest_framework import serializers
from rest_framework.renderers import JSONRenderer
from rest_framework.permissions import IsAdminUser

from roku_content.models import RokuContentFeed
from roku_content.models import Language, Category, Playlist
from roku_content.models import Movie, LiveFeed, Series, Season
from roku_content.models import Episode, ShortFormVideo, TVSpecial
from roku_content.models import Content, Video, Caption, TrickPlayFile
from roku_content.models import Genre, ExternalID, Rating, RatingSource
from roku_content.models import RatingCountry, ParentalRating, CreditRole, Credit, Tag


# Single string - serializers.StringRelatedField()
# List of strings - serializers.StringRelatedField(many=true)
# List of objects - create a *SerializerList class, (many=true)

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
	def to_representation(self, instance):
		result = super(TrickPlayFileSerializerList, self).to_representation(instance)
		return OrderedDict([(key, result[key]) for key in result if result[key] ])
	class Meta:
		model = TrickPlayFile
		fields = ['id', 'url', 'quality']


class ContentSerializerList(serializers.ModelSerializer):
	dateAdded = serializers.DateField(source='date_added')
	videos = VideoSerializerList(many=True)
	captions = CaptionSerializerList(many=True)
	#trickPlayFiles = TrickPlayFileSerializerList(many=True, source='trick_play_files')
	language = serializers.StringRelatedField()
	validityPeriodStart = serializers.DateField(source='validity_start_period')
	validityPeriodEnd = serializers.DateField(source='validity_end_period')
	#adBreaks = serializers.CharField(source='ad_breaks')  # Advertising not supported
	class Meta:
		model = Content
		fields = ['id', 'dateAdded', 'videos', 'duration', 'captions', \
			'language',	'validityPeriodStart', 'validityPeriodEnd']
			# 'trickPlayFiles', validityPeriodStart', 'validityPeriodEnd', 'adBreaks']


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
	sourceLongName = serializers.CharField(source='source_long_name')
	sourceCountry = serializers.CharField(source='source_country')
	class Meta:
		model = RatingSource
		fields = ['ratingSource', 'sourceLongName', 'sourceCountry']


class RatingCountrySerializerList(serializers.ModelSerializer):
	countryName = serializers.CharField(source='country_name')
	countryCode = serializers.CharField(source='country_code')
	class Meta:
		model = RatingCountry
		fields = ['countryName', 'countryCode']


class ParentalRatingSerializerList(serializers.ModelSerializer):
	parentalRating = serializers.CharField(source='parental_rating')
	class Meta:
		model = ParentalRating
		fields = ['parentalRating']


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
	tag = serializers.CharField(source='tag_name')
	class Meta:
		model = Tag
		fields = ['tag']


### Content Types

class MovieSerializerList(serializers.ModelSerializer):
	id = serializers.UUIDField(source='uuid_id')
	shortDescription = serializers.CharField(source='short_description')
	longDescription = serializers.CharField(source='long_description')
	releaseDate = serializers.DateField(source='release_date')
	content = ContentSerializerList()
	genres = serializers.StringRelatedField(many=True)
	tags = serializers.StringRelatedField(many=True)
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
	id = serializers.UUIDField(source='uuid_id')
	shortDescription = serializers.CharField(source='short_description')
	longDescription = serializers.CharField(source='long_description')
	brandedThumbnail = serializers.URLField(source='branded_thumbnail')
	content = ContentSerializerList()
	tags = serializers.StringRelatedField(many=True)
	genres = serializers.StringRelatedField(many=True)
	rating = RatingSerializerList()
	# advisoryRatings (AdvisoryRatingObject)
	def to_representation(self, instance):
		result = super(LiveFeedSerializerList, self).to_representation(instance)
		return OrderedDict([(key, result[key]) for key in result if result[key] ])
	class Meta:
		model = LiveFeed
		fields = ['id', 'title', 'shortDescription', 'longDescription', 'content', \
			'thumbnail', 'brandedThumbnail', 'tags', 'genres', 'rating']


class EpisodeSerializerList(serializers.ModelSerializer):
	id = serializers.UUIDField(source='uuid_id')
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
		fields = ['id', 'titleSeason', 'seasonNumber', 'episodes']


class SeriesSerializerList(serializers.ModelSerializer):
	id = serializers.UUIDField(source='uuid_id')
	shortDescription = serializers.CharField(source='short_description')
	longDescription = serializers.CharField(source='long_description')
	releaseDate = serializers.DateField(source='release_date')
	seasons = SeasonSerializerList(many=True)
	episodes = EpisodeSerializerList(many=True)
	tags = serializers.StringRelatedField(many=True)
	genres = serializers.StringRelatedField(many=True)
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
	#id = serializers.UUIDField(source='uuid_id')
	id = serializers.CharField()
	shortDescription = serializers.CharField(source='short_description')
	longDescription = serializers.CharField(source='long_description')
	releaseDate = serializers.DateField(source='release_date')
	rating = RatingSerializerList()
	genres = serializers.StringRelatedField(many=True)
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
	id = serializers.UUIDField(source='uuid_id')
	shortDescription = serializers.CharField(source='short_description')
	longDescription = serializers.CharField(source='long_description')
	releaseDate = serializers.DateField(source='release_date')
	tags = serializers.StringRelatedField(many=True)
	genres = serializers.StringRelatedField(many=True)
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


### Content Categories

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
	# prefer 'content type' id and playist item_ids to be uuids
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
	categories = CategorySerializerList(many=True)
	playlists = PlaylistSerializerList(many=True)
	def to_representation(self, instance):
		result = super(RokuContentFeedSerializerDetail, self).to_representation(instance)
		return OrderedDict([(key, result[key]) for key in result if result[key] ])
	class Meta:
		model = RokuContentFeed
		fields = ['providerName', 'language', 'rating', 'lastUpdated', 'movies', \
			'liveFeeds', 'series', 'shortFormVideos', 'tvSpecials', 'categories', 'playlists']


### NOTES
# # None field will be removed from response
# class NonNullModelSerializer(serializers.ModelSerializer):
# 	def to_representation(self, instance):
# 		result = super(NonNullModelSerializer, self).to_representation(instance)
# 		return OrderedDict([(key, result[key]) for key in result if result[key] is not None])

# # None field AND Blank field will be removed from response
# class ValueBasedModelSerializer(serializers.ModelSerializer):
# 	def to_representation(self, instance):
# 		result = super(ValueBasedModelSerializer, self).to_representation(instance)
# 		return OrderedDict([(key, result[key]) for key in result if result[key] ])
