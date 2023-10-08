from datetime import datetime
from rest_framework import serializers
from .models import RokuContentFeed
from .models import Language, Category, Playlist
from .models import ShortFormVideo
#from .models import Movie, LiveFeed, Series, Season, Episode, ShortFormVideo, TVSpecial
from .models import Content, Video, Caption, TrickPlayFile, Genre, ExternalID, Rating, \
					RatingSource, ParentalRating, Credit

### Roku Feeds

# This class provides the data used to populate the Roku channel menus and content
class RokuContentFeedSerializerList(serializers.ModelSerializer):
	providerName = models.CharField(source='provider_name')
	lastUpdated = models.DateTimeField(source='last_updated')
	shortFormVideos = serializers.JSONField(source='short_form_videos')
	#movies = serializers.JSONField(source='movies')
	#series = serializers.JSONField(source='series')
	playlists = serializers.JSONField(source='playlists')
	categories = serializers.JSONField(source='categories')
	class Meta:
		model = RokuContentFeed
		fields = ['provider_name', 'language', 'rating', 'last_updated', \
			'short_form_videos', 'movies', 'series', 'playlists', 'categories']


### Content Categories

class CategorySerializerList(serializers.ModelSerializer):
	category = serializers.JSONField(source='category_name')
	playlist = serializers.JSONField(source='playlist_name')
	class Meta:
		model = Category
		fields = ['id', 'category_name', 'playlist_name', 'query_string', 'order']
		#fields = '__all__'  ## provide all fields

class PlaylistSerializerList(serializers.ModelSerializer):
	name = models.CharField(source='playlist_name')
	itemIds = serializers.JSONField(source='item_ids')
	class Meta:
		model = Playlist
		fields = ['playlist_name', 'item_ids']


### Content Types

# class MovieSerializerList(serializers.ModelSerializer):
# 	id = models.UUIDField(source='movie_id')
# 	class Meta:
# 		model = Movie
# 		fields = ['movie_id', 'title', 'content', 'genres', 'thumbnail', 'release_date', \
# 			'short_description', 'long_description', 'tags', 'credits', 'rating', 'external_ids']

# class LiveFeedSerializerList(serializers.ModelSerializer):
# 	id = models.UUIDField(source='livefeed_id')
# 	class Meta:
# 		model = LiveFeed
# 		fields = ['livefeed_id', 'title', 'content', 'thumbnail', 'branded_thumbnail', \
# 			'short_description', 'long_description', 'tags', 'rating', 'genres']

# class SeriesSerializerList(serializers.ModelSerializer):
# 	id = models.UUIDField(source='series_id')
# 	class Meta:
# 		model = Series
# 		fields = ['series_id', 'title', 'seasons', 'episodes', 'genres', 'thumbnail', \
# 			'release_date', 'short_description', 'long_description', 'tags', 'credits', 'external_ids']

# class SeasonSerializerList(serializers.ModelSerializer):
# 	class Meta:
# 		model = Season
# 		fields = ['season_number', 'episodes']

# class EpisodeSerializerList(serializers.ModelSerializer):
# 	id = models.UUIDField(source='episode_id')
# 	class Meta:
# 		model = Episode
# 		fields = ['episode_id', 'title', 'content', 'thumbnail', 'release_date', 'episode_number', \
# 		'short_description', 'long_description', 'credits', 'rating', 'external_ids']

class ShortFormVideoSerializerList(serializers.ModelSerializer):
	id = models.UUIDField(source='short_form_video_id')
	class Meta:
		model = ShortFormVideo
		fields = ['short_form_video_id', 'title', 'content', 'thumbnail', 'short_description', \
		'long_description', 'release_date', 'tags', 'genres', 'credits', 'rating']

# class TVSpecialSerializerList(serializers.ModelSerializer):
# 	id = models.UUIDField(source='tv_special_id')
# 	class Meta:
# 		model = TVSpecial
# 		fields = ['tv_special_id', 'title', 'content', 'thumbnail', 'genres', 'release_date', \
# 		'short_description', 'long_description', 'credits', 'rating', 'tags', 'external_ids']


### Content Properties

class ContentSerializerList(serializers.ModelSerializer):
	dateAdded = models.DateField(source='date_added')
	trickPlayFiles = models.JSONField(source='trick_play_files')
	validityPeriodStart = models.DateField(source='validity_period_start')
	validityPeriodEnd = models.DateField(source='validity_period_end')
	#adBreaks = models.CharField(source='ad_breaks')  # Advertising not supported
	class Meta:
		model = Content
		fields = ['date_added', 'videos', 'duration', 'captions', 'trick_play_files', \
			'language', 'validity_period_start', 'validity_period_end']

class VideoSerializerList(serializers.ModelSerializer):
	videoType = models.CharField(source='video_type')
	class Meta:
		model = Video
		fields = ['url', 'quality', 'video_type']

class CaptionSerializerList(serializers.ModelSerializer):
	captionType = models.CharField(source='caption_type')
	class Meta:
		model = Caption
		fields = ['url', 'language', 'caption_type']

class TrickPlayFileSerializerList(serializers.ModelSerializer):
	class Meta:
		model = TrickPlayFile
		fields = ['url', 'quality']

class GenreFileSerializerList(serializers.ModelSerializer):
	class Meta:
		model = Genre
		fields = ['genre']

class ExternalIDSerializerList(serializers.ModelSerializer):
	id = models.CharField(source='external_id')
	idType = models.CharField(source='id_type')
	class Meta:
		model = ExternalID
		fields = ['external_id', 'id_type']

class RatingSerializerList(serializers.ModelSerializer):
	ratingSource = models.CharField(source='rating_source')
	class Meta:
		model = Rating
		fields = ['rating', 'rating_source']

class RatingSourceSerializerList(serializers.ModelSerializer):
	ratingSource = models.CharField(source='source_name')
	class Meta:
		model = RatingSource
		fields = ['source_name', 'source_long_name']

class ParentalRatingSourceSerializerList(serializers.ModelSerializer):
	class Meta:
		model = ParentRating
		fields = ['parental_rating']

class CreditSerializerList(serializers.ModelSerializer):
	name = models.CharField(source='credit_name')
	birthDate = models.CharField(source='birth_date')
	class Meta:
		model = Credit
		fields = ['credit_name', 'role', 'birth_date']
