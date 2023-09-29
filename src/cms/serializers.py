from rest_framework import serializers
from .models import Category, Playlist, Movie, LiveFeed, Series, Season, Episode, ShortFormVideo, TVSpecial
from .models import Content, Video, Genre, ExternalID, Rating, RatingSource, ParentalRating, Credit


### Content Categories

class CategorySerializerList(serializers.ModelSerializer):
	category = serializers.JSONField(source='category_name')
	playlist = serializers.JSONField(source='playlist_name')
	class Meta:
		model = Content
		fields = ['id', 'category_name', 'playlist_name', 'query_string', 'order']

class PlaylistSerializerList(serializers.ModelSerializer):
	categories = serializers.JSONField(source='category')
	class Meta:
		model = Playlist
		fields = ['id', 'title', 'short_description', 'created', 'category']


### Content Types

class MovieSerializerList(serializers.ModelSerializer):
	id = models.UUIDField(source='movie_id')
	class Meta:
		model = Movie
		fields = ['movie_id', 'title', 'content', 'genres', 'thumbnail', 'release_date', \
			'short_description', 'long_description', 'tags', 'credits', 'rating', 'external_ids']

class LiveFeedSerializerList(serializers.ModelSerializer):
	id = models.UUIDField(source='livefeed_id')
	class Meta:
		model = LiveFeed
		fields = ['livefeed_id', 'title', 'content', 'thumbnail', 'branded_thumbnail', \
			'short_description', 'long_description', 'tags', 'rating', 'genres']

class SeriesSerializerList(serializers.ModelSerializer):
	id = models.UUIDField(source='series_id')
	class Meta:
		model = Series
		fields = ['series_id', 'title', 'seasons', 'episodes', 'genres', 'thumbnail', \
			'release_date', 'short_description', 'long_description', 'tags', 'credits', 'external_ids']

class SeasonSerializerList(serializers.ModelSerializer):
	class Meta:
		model = Season
		fields = ['season_number', 'episodes']

class EpisodeSerializerList(serializers.ModelSerializer):
	id = models.UUIDField(source='episode_id')
	class Meta:
		model = Episode
		fields = ['episode_id', 'title', 'content', 'thumbnail', 'release_date', 'episode_number', \
		'short_description', 'long_description', 'credits', 'rating', 'external_ids']

class ShortFormVideoSerializerList(serializers.ModelSerializer):
	id = models.UUIDField(source='short_form_video_id')
	class Meta:
		model = ShortFormVideo
		fields = ['short_form_video_id', 'title', 'content', 'thumbnail', 'short_description', \
		'long_description', 'release_date', 'tags', 'genres', 'credits', 'rating']

class TVSpecialSerializerList(serializers.ModelSerializer):
	id = models.UUIDField(source='tv_special_id')
	class Meta:
		model = TVSpecial
		fields = ['tv_special_id', 'title', 'content', 'thumbnail', 'genres', 'release_date', \
		'short_description', 'long_description', 'credits', 'rating', 'tags', 'external_ids']


### Content Properties






# class MovieSerializerDetail(serializers.ModelSerializer):
# 	class Meta:
# 		model = Movie
# 		fields = '__all__'
