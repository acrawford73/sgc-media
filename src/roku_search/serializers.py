from datetime import datetime
from rest_framework import serializers
from rest_framework.renderers import JSONRenderer
from rest_framework.permissions import IsAdminUser

from .models import SearchFeed

from roku_content.models import Language #, Movie, Series, Season, Episode, ShortFormVideo, TVSpecial, Content
# from roku_content.models import ExternalID, Rating, ParentalRating, RatingSource, Genre, Credit

# class ExternalIDListSerializer(serializers.ModelSerializer):
# 	class Meta:
# 		model = MovieExternalID
# 		fields = ['external_id']

# class MovieSerializerList(serializers.ModelSerializer):
# 	id = serializers.UUIDField(source='movie_id')
# 	type = serializers.CharField(default="movie")
# 	externalIDs = ExternalIDSerializerList()
# 	class Meta:
# 		model = Movie
# 		fields = ['id', 'title']

# class AssetSerializerList(serializers.ModelSerializer):
# 	movies = MovieSerializerList(many=True)
# 	series = SeriesSerializerList(many=True)
# 	seasons = SeasonSerializerList(many=True)
# 	episodes = EpisodesSerializerList(many=True)
# 	shortFormVideos = ShortFormVideoSerializerList(many=True, source='short_form_videos')
# 	tvSpecials = TVSpecialSerializerList(many=True, source='tv_specials')
#	externalIDs = ExternalIDSerializerList()
#	externalIdSource = ?
#	titles = TitleSerializerList(man=True)
#	shortDescription = ShortDescriptionSerializerList(man=True)
#	longDescription = LongDescriptionSerializerList(man=True)
# 	class Meta:
# 		fields = ['ShortFormVideos', 'tvSpecials']

class SearchFeedSerializerDetail(serializers.ModelSerializer):
	"""
	Serializer Detail class for Roku Content Feed.
	"""
	defaultLanguage = serializers.StringRelatedField(source='default_language')
	#defaultAvailabilityCountries = serializers.StringRelatedField(source='available_countries')
	#assets = serializers.AssetSerializerList()
	
	class Meta:
		model = SearchFeed
		#fields = '__all__'
		fields = ['search_feed_id', 'version', 'defaultLanguage']




