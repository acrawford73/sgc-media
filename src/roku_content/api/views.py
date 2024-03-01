import logging
logger = logging.getLogger(__name__)

from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
### Models
## Roku Content Feeds, Categories, Types, Properties
from roku_content.models import RokuContentFeed
from roku_content.models import Language, Category, Playlist
from roku_content.models import Movie, LiveFeed, Series, Season, Episode, ShortFormVideo, TVSpecial
from roku_content.models import Content, Video, Caption, TrickPlayFile, Genre, ExternalID, Rating
from roku_content.models import RatingSource, Country, ParentalRating, CreditRole, Credit, Tag
### Rest Framework
from rest_framework.response import Response
from rest_framework.reverse import reverse, reverse_lazy
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import filters
from rest_framework.renderers import JSONRenderer
from django_filters.rest_framework import DjangoFilterBackend
### Serializers
# Feeds
from .serializers import RokuContentFeedSerializerList, RokuContentFeedSerializerDetail #, RokuSearchFeedSerializerList
# Categories
from .serializers import CategorySerializerList, PlaylistSerializerList
# Types
from .serializers import MovieSerializerList, LiveFeedSerializerList, SeriesSerializerList
from .serializers import SeasonSerializerList, EpisodeSerializerList, ShortFormVideoSerializerList
from .serializers import TVSpecialSerializerList
# Properties
from .serializers import ContentSerializerList, VideoSerializerList, CaptionSerializerList
from .serializers import TrickPlayFileSerializerList, GenreSerializerList, ExternalIDSerializerList
from .serializers import RatingSerializerList, RatingSourceSerializerList, CountrySerializerList, ParentalRatingSerializerList
from .serializers import CreditRoleSerializerList, CreditSerializerList, LanguageSerializerList, TagSerializerList


## Roku Feeds

# Roku Content Feed

class RokuContentFeedListAPI(APIView):
	"""
	Roku Content Feed fields for ListAPIView :model:`roku_content.RokuContentFeed`.
	"""
#	queryset = RokuContentFeed.objects.all().filter(is_public=True)
	#serializer_class = RokuContentFeedSerializerList
	#filter_backends = [DjangoFilterBackend]
	#filterset_fields = ['language']
#	pagination_class = None
	# lookup_field = ['id']
	# http_method_names = ['get']

	# def get(self, request, format=None, queryset):
	# 	#feed = RokuContentFeed.objects.all().filter(is_public=True)
	# 	#providerName = feed.provider_name
	# 	#serializer = RokuContentFeedSerializerList(feed, many=False)
	# 	providerName = [feed.providerName for feed in feed.objects.all()]
	# 	return Response(providerName)

	#####
	renderer_classes = [JSONRenderer]
	pagination_class = None
	def get(self, request, format=None):
		feeds = RokuContentFeed.objects.first() #.filter(is_public=True)
		serializer = RokuContentFeedSerializerList(feeds)
		if feed is not None:
			logger.debug("RokuContentFeed list objects returned.")
		return Response(serializer.data)
#####


	# def get(self, request, *args, **kwargs):
	# 	serializer = RokuContentFeedSerializerDetail(RokuContentFeed.objects.all().filter(is_public=True), many=False)
	# 	return Response(serializer.data)

	
	# def get_queryset(self):
	# 	return __str__(self.queryset)
	# def get_serializer_class(self):
	# 	return RokuContentFeedSerializerList


# class RokuContentFeedListAPI(generics.ListAPIView):
# 	"""
# 	Roku Content Feed fields for ListAPIView :model:`roku_content.RokuContentFeed`.
# 	"""
# 	queryset = RokuContentFeed.objects.all().filter(is_public=True)
# 	serializer_class = RokuContentFeedSerializerList
# 	filter_backends = [DjangoFilterBackend]
# 	filterset_fields = ['language']
# 	pagination_class = None
# 	renderer_classes = [JSONRenderer]

# class RokuContentFeedListSearchAPI(generics.ListAPIView):
# 	queryset = RokuContentFeed.objects.all().filter(is_public=True)
# 	serializer_class = RokuContentFeedSerializerDetail
# 	#filter_backends = [DjangoFilterBackend]
# 	filter_backends = [filters.SearchFilter]
# 	filterset_fields = ['roku_content_feed_id']
# 	search_fields = ['roku_content_feed_id']
# 	lookup_field = ['roku_content_feed_id']
# 	pagination_class = None

class RokuContentFeedDetailAPI(generics.RetrieveAPIView):
	# queryset = RokuContentFeed.objects.all().filter(is_public=True)
	# serializer_class = RokuContentFeedSerializerDetail
	renderer_classes = [JSONRenderer]
	pagination_class = None
	def get(self, request, pk, format=None):
		feed = RokuContentFeed.objects.get(pk=pk)
		serializer = RokuContentFeedSerializerDetail(feed)
		if feed is not None:
			logger.debug("RokuContentFeed detail object " + str(feed.pk) + " returned.")
		return Response(serializer.data)


## Roku Content Categories

# Language

class LanguageListAPI(generics.ListAPIView):
	queryset = Language.objects.all()
	serializer_class = LanguageSerializerList
	ordering_fields = ['id', 'code_iso_639_2', 'code_iso_639_1', 'language_name_eng']
	ordering = ['language_name_eng']

# Category

class CategoryListAPI(generics.ListAPIView):
	queryset = Category.objects.all()
	serializer_class = CategorySerializerList
	#filter_backends = [DjangoFilterBackend]
	#filterset_fields = ['category_name', 'playlist_name', 'order']
	ordering_fields = ['id', 'category_name', 'playlist_name', 'order']
	ordering = ['category_name']
	pagination_class = None

# class CategoryListAPISearch(generics.ListAPIView):
# 	queryset = Category.objects.all()
# 	serializer_class = CategorySerializerList
# 	filter_backends = [filters.SearchFilter]
# 	search_fields = ['title', 'short_description', 'long_description', 'service', 'orientation', 'username', '@tags', 'location_name', 'location_city', 'location_state', 'location_country']
# 	ordering_fields = ['id', 'category_name', 'playlist_name']
# 	ordering = ['-id']

# class CategoryDetailAPI(generics.RetrieveAPIView):
# 	queryset = Category.objects.all()
# 	serializer_class = CategorySerializerDetail

# Playlist

class PlaylistListAPI(generics.ListAPIView):
	queryset = Playlist.objects.all()
	serializer_class = PlaylistSerializerList
	#filter_backends = [DjangoFilterBackend]
	#filterset_fields = ['playlist_name']
	ordering_fields = ['id', 'playlist_name']
	ordering = ['playlist_name']
	pagination_class = None

# class PlaylistListAPISearch(generics.ListAPIView):
# 	queryset = Playlist.objects.all()
# 	serializer_class = PlaylistSerializerList
# 	filter_backends = [filters.SearchFilter]
# 	search_fields = ['playlist_name']
# 	ordering_fields = ['id', 'playlist_name']
# 	ordering = ['-id']

# class PlaylistDetailAPI(generics.RetrieveAPIView):
# 	queryset = Playlist.objects.all()
# 	serializer_class = PlaylistSerializerDetail


## Roku Content Types

# Movie

class MovieListAPI(generics.ListAPIView):
	queryset = Movie.objects.all()
	serializer_class = MovieSerializerList
	#filter_backends = [DjangoFilterBackend]
	#filterset_fields = ['title', 'genres', 'release_date', 'tags', 'credits', 'rating', 'external_ids']
	ordering_fields = ['title', 'release_date', 'tags', 'rating']
	ordering = ['-id']

# class MovieListAPISearch(generics.ListAPIView):
# 	queryset = Movie.objects.all()
# 	serializer_class = MovieSerializerList
# 	filter_backends = [filters.SearchFilter]
# 	search_fields = ['uuid_id', 'title', 'content', 'genres', 'thumbnail', 'release_date', \
# 		'short_description', 'long_description', 'tags', 'credits', 'rating', 'external_ids']
# 	ordering_fields = ['uuid_id', 'title', 'release_date', 'short_description', 'tags', 'rating']
# 	ordering = ['-id']

# class MovieDetailAPI(generics.RetrieveAPIView):
# 	queryset = Movie.objects.all()
# 	serializer_class = MovieSerializerDetail

# LiveFeed

class LiveFeedListAPI(generics.ListAPIView):
	queryset = LiveFeed.objects.all()
	serializer_class = LiveFeedSerializerList
	#filter_backends = [DjangoFilterBackend]
	#filterset_fields = ['title', 'content', 'tags', 'rating', 'genres']
	ordering_fields = ['id', 'title', 'tags', 'rating', 'genres']
	ordering = ['-id']

# class LiveFeedListAPISearch(generics.ListAPIView):
# 	queryset = LiveFeed.objects.all()
# 	serializer_class =LiveFeedSerializerList
# 	filter_backends = [filters.SearchFilter]
# 	search_fields = ['uuid_id', 'title', 'content', 'short_description', \
# 		'long_description', 'tags', 'rating', 'genres']
# 	ordering_fields = ['id', 'title', 'tags', 'rating', 'genres']
# 	ordering = ['-id']

# class LiveFeedDetailAPI(generics.RetrieveAPIView):
# 	queryset = LiveFeed.objects.all()
# 	serializer_class = LiveFeedSerializerDetail

# Series

class SeriesListAPI(generics.ListAPIView):
	queryset = Series.objects.all()
	serializer_class = SeriesSerializerList
	#filter_backends = [DjangoFilterBackend]
	#filterset_fields = ['title', 'seasons', 'episodes', 'genres', 'tags', 'credits', 'external_ids']
	ordering_fields = ['id', 'seasons', 'episodes', 'genres', 'release_date', 'tags', 'credits', 'external_ids']
	ordering = ['-id']

# class SeriesListAPISearch(generics.ListAPIView):
# 	queryset = Series.objects.all()
# 	serializer_class = SeriesSerializerList
# 	filter_backends = [filters.SearchFilter]
# 	search_fields = ['uuid_id', 'title', 'seasons', 'episodes', 'genres', 'release_date', \
# 		'short_description', 'long_description', 'tags', 'credits', 'external_ids']
# 	ordering_fields = ['id', 'seasons', 'episodes', 'genres', 'release_date', 'tags', 'credits', 'external_ids']
# 	ordering = ['-id']

# class SeriesDetailAPI(generics.RetrieveAPIView):
# 	queryset = Series.objects.all()
# 	serializer_class = SeriesSerializerDetail

# Season

class SeasonListAPI(generics.ListAPIView):
	queryset = Season.objects.all()
	serializer_class = SeasonSerializerList
	#filter_backends = [DjangoFilterBackend]
	#filterset_fields = ['season_number', 'episodes']
	ordering_fields = ['id', 'season_number', 'episodes']
	ordering = ['-id']

# class SeasonListAPISearch(generics.ListAPIView):
# 	queryset = Season.objects.all()
# 	serializer_class = SeasonSerializerList
# 	filter_backends = [filters.SearchFilter]
# 	search_fields = ['season_number', 'episodes']
# 	ordering_fields = ['id', 'season_number', 'episodes']
# 	ordering = ['-id']

# class SeriesDetailAPI(generics.RetrieveAPIView):
# 	queryset = Season.objects.all()
# 	serializer_class = SeasonSerializerDetail

# Episode

class EpisodeListAPI(generics.ListAPIView):
	queryset = Episode.objects.all()
	serializer_class = EpisodeSerializerList
	#filter_backends = [DjangoFilterBackend]
	#filterset_fields = ['release_date', 'episode_number', 'rating']
	ordering_fields = ['id', 'title', 'release_date', 'episode_number', 'credits', 'rating', 'external_ids']
	ordering = ['-id']

# class EpisodeListAPISearch(generics.ListAPIView):
# 	queryset = Episode.objects.all()
# 	serializer_class = EpisodeSerializerList
# 	filter_backends = [filters.SearchFilter]
# 	search_fields = ['uuid_id', 'title', 'content', 'release_date', 'episode_number', \
# 		'short_description', 'long_description', 'credits', 'rating', 'external_ids']
# 	ordering_fields = ['id', 'title', 'release_date', 'episode_number', 'credits', 'rating', 'external_ids']
# 	ordering = ['-id']

# class EpisodeDetailAPI(generics.RetrieveAPIView):
# 	queryset = Episode.objects.all()
# 	serializer_class = EpisodeSerializerDetail

# ShortFormVideo

class ShortFormVideoListAPI(generics.ListAPIView):
	queryset = ShortFormVideo.objects.all()
	serializer_class = ShortFormVideoSerializerList
	#filter_backends = [DjangoFilterBackend]
	#filterset_fields = ['release_date', 'tags', 'genres', 'rating']
	ordering_fields = ['id', 'title', 'release_date']
	ordering = ['-id']

# class ShortFormVideoListAPISearch(generics.ListAPIView):
# 	queryset = ShortFormVideo.objects.all()
# 	serializer_class = ShortFormVideoSerializerList
# 	filter_backends = [filters.SearchFilter]
# 	search_fields = ['uuid_id', 'title', 'short_description', 'long_description', \
# 		'release_date', 'tags', 'genres', 'credits', 'rating']
# 	ordering_fields = ['id', 'title', 'release_date', 'tags', 'genres', 'credits', 'rating']
# 	ordering = ['-id']

# class ShortFormVideoDetailAPI(generics.RetrieveAPIView):
# 	queryset = ShortFormVideo.objects.all()
# 	serializer_class = ShortFormVideoSerializerDetail

# TVSpecial

class TVSpecialListAPI(generics.ListAPIView):
	queryset = TVSpecial.objects.all()
	serializer_class = TVSpecialSerializerList
	#filter_backends = [DjangoFilterBackend]
	#filterset_fields = ['genres', 'release_date', 'credits', 'rating', 'tags', 'external_ids']
	ordering_fields = ['id', 'title', 'release_date', 'rating', 'tags', 'credits', 'external_ids']
	ordering = ['-id']

# class TVSpecialListAPISearch(generics.ListAPIView):
# 	queryset = TVSpecial.objects.all()
# 	serializer_class = TVSpecialSerializerList
# 	filter_backends = [filters.SearchFilter]
# 	search_fields = ['tvspecial_id', 'title', 'content', 'release_date', \
# 		'short_description', 'long_description', 'credits', 'rating', 'external_ids']
# 	ordering_fields = ['id', 'title', 'release_date', 'credits', 'rating', 'tags', 'external_ids']
# 	ordering = ['-id']

# class TVSpecialDetailAPI(generics.RetrieveAPIView):
# 	queryset = TVSpecial.objects.all()
# 	serializer_class = TVSpecialSerializerDetail


## Roku ContentPoperties

# Content

class ContentListAPI(generics.ListAPIView):
	queryset = Content.objects.all()
	serializer_class = ContentSerializerList
	#filter_backends = [DjangoFilterBackend]
	#filterset_fields = ['language', 'validity_start_period', 'validity_end_period']
	ordering_fields = ['id', 'date_added', 'language', 'validity_start_period', 'validity_end_period']
	ordering = ['id']

# class ContentListAPISearch(generics.ListAPIView):
# 	queryset = Content.objects.all()
# 	serializer_class = ContentSerializerList
# 	filter_backends = [filters.SearchFilter]
# 	search_fields = ['title', 'short_description', 'long_description', '@tags']
# 	ordering_fields = ['id', 'category_name', 'playlist_name']
# 	ordering = ['-id']

# class ContentDetailAPI(generics.RetrieveAPIView):
# 	queryset = Content.objects.all()
# 	serializer_class = ContentSerializerDetail

# Video

class VideoListAPI(generics.ListAPIView):
	queryset = Video.objects.all()
	serializer_class = VideoSerializerList
	#filter_backends = [DjangoFilterBackend]
	#filterset_fields = ['quality', 'video_type']
	ordering_fields = ['id', 'quality', 'video_type']
	ordering = ['-id']

# class VideoListAPISearch(generics.ListAPIView):
# 	queryset = Video.objects.all()
# 	serializer_class = VideoSerializerList
# 	filter_backends = [filters.SearchFilter]
# 	search_fields = ['url', 'quality', 'video_type']
# 	ordering_fields = ['id', 'quality', 'video_type']
# 	ordering = ['-id']

# class VideoDetailAPI(generics.RetrieveAPIView):
# 	queryset = Video.objects.all()
# 	serializer_class = VideoSerializerDetail

# Caption

class CaptionListAPI(generics.ListAPIView):
	queryset = Caption.objects.all()
	serializer_class = CaptionSerializerList
	#filter_backends = [DjangoFilterBackend]
	#filterset_fields = ['language', 'caption_type']
	ordering_fields = ['id', 'language', 'caption_type']
	ordering = ['-id']

# class CaptionListAPISearch(generics.ListAPIView):
# 	queryset = Caption.objects.all()
# 	serializer_class = CaptionSerializerList
# 	filter_backends = [filters.SearchFilter]
# 	search_fields = ['url', 'language', 'caption_type']
# 	ordering_fields = ['id', 'language', 'caption_type']
# 	ordering = ['-id']

# class CaptionDetailAPI(generics.RetrieveAPIView):
# 	queryset = Caption.objects.all()
# 	serializer_class = CaptionSerializerDetail

# TrickPlayFile

class TrickPlayFileListAPI(generics.ListAPIView):
	queryset = TrickPlayFile.objects.all()
	serializer_class = TrickPlayFileSerializerList
	ordering_fields = ['id', 'quality']
	ordering = ['-id']

# class TrickPlayFileListAPISearch(generics.ListAPIView):
# 	queryset = TrickPlayFile.objects.all()
# 	serializer_class = TrickPlayFileSerializerList
# 	filter_backends = [filters.SearchFilter]
# 	search_fields = ['url', 'quality']
# 	ordering_fields = ['id', 'quality']
# 	ordering = ['-id']

# class TrickPlayFileDetailAPI(generics.RetrieveAPIView):
# 	queryset = TrickPlayFile.objects.all()
# 	serializer_class = TrickPlayFileSerializerDetail

# Genre

class GenreListAPI(generics.ListAPIView):
	queryset = Genre.objects.all()
	serializer_class = GenreSerializerList
	#filter_backends = [DjangoFilterBackend]
	#filterset_fields = ['genre']
	ordering_fields = ['id', 'genre']
	ordering = ['genre']
	pagination_class = None

# class GenreListAPISearch(generics.ListAPIView):
# 	queryset = Genre.objects.all()
# 	serializer_class = GenreSerializerList
# 	filter_backends = [filters.SearchFilter]
# 	search_fields = ['genre']
# 	ordering_fields = ['id', 'genre']
# 	ordering = ['-id']

# class GenreDetailAPI(generics.RetrieveAPIView):
# 	queryset = Genre.objects.all()
# 	serializer_class = GenreSerializerDetail

# ExternalID

class ExternalIDListAPI(generics.ListAPIView):
	queryset = ExternalID.objects.all()
	serializer_class = ExternalIDSerializerList
	#filter_backends = [DjangoFilterBackend]
	#filterset_fields = ['external_id']
	ordering_fields = ['id', 'external_id', 'id_type']
	ordering = ['-id']
	pagination_class = None

# class ExternalIDListAPISearch(generics.ListAPIView):
# 	queryset = ExternalID.objects.all()
# 	serializer_class = ExternalIDSerializerList
# 	filter_backends = [filters.SearchFilter]
# 	search_fields = ['external_id']
# 	ordering_fields = ['id', 'external_id', 'id_type']
# 	ordering = ['-id']

# class ExternalIDDetailAPI(generics.RetrieveAPIView):
# 	queryset = ExternalID.objects.all()
# 	serializer_class = ExternalIDSerializerDetail

# Rating

class RatingListAPI(generics.ListAPIView):
	queryset = Rating.objects.all()
	serializer_class = RatingSerializerList
	#filter_backends = [DjangoFilterBackend]
	#filterset_fields = ['rating']
	ordering_fields = ['rating', 'rating_source']
	ordering = ['-id']
	pagination_class = None

# class RatingListAPISearch(generics.ListAPIView):
# 	queryset = Rating.objects.all()
# 	serializer_class = RatingSerializerList
# 	filter_backends = [filters.SearchFilter]
# 	search_fields = ['rating']
# 	ordering_fields = ['id', 'rating', 'rating_source']
# 	ordering = ['-id']

# class RatingDetailAPI(generics.RetrieveAPIView):
# 	queryset = ParentalRating.objects.all()
# 	serializer_class = ParentalRatingSerializerDetail

# RatingSource

class RatingSourceListAPI(generics.ListAPIView):
	queryset = RatingSource.objects.all()
	serializer_class = RatingSourceSerializerList
	#filter_backends = [DjangoFilterBackend]
	#filterset_fields = ['source_name']
	ordering_fields = ['id', 'source_name']
	ordering = ['source_name']
	pagination_class = None
# class RatingSourceListAPISearch(generics.ListAPIView):
# 	queryset = RatingSource.objects.all()
# 	serializer_class = RatingSourceSerializerList
# 	filter_backends = [filters.SearchFilter]
# 	search_fields = ['source_name']
# 	ordering_fields = ['id', 'source_name']
# 	ordering = ['-id']

# class RatingSourceDetailAPI(generics.RetrieveAPIView):
# 	queryset = RatingSource.objects.all()
# 	serializer_class = RatingSourceSerializerDetail

# Countries

class CountryListAPI(generics.ListAPIView):
	queryset = Country.objects.all()
	serializer_class = CountrySerializerList
	#filter_backends = [DjangoFilterBackend]
	#filterset_fields = ['country_code']
	ordering_fields = ['country_name', 'country_code']
	ordering = ['country_code']
	pagination_class = None

# ParentalRating

class ParentalRatingListAPI(generics.ListAPIView):
	queryset = ParentalRating.objects.all()
	serializer_class = ParentalRatingSerializerList
	#filter_backends = [DjangoFilterBackend]
	#filterset_fields = ['parental_rating']
	ordering_fields = ['id', 'parental_rating']
	ordering = ['parental_rating']
	pagination_class = None

# class ParentalRatingListAPISearch(generics.ListAPIView):
# 	queryset = ParentalRating.objects.all()
# 	serializer_class = ParentalRatingSerializerList
# 	filter_backends = [filters.SearchFilter]
# 	search_fields = ['rating']
# 	ordering_fields = ['id', 'rating']
# 	ordering = ['-id']

# class ParentalRatingDetailAPI(generics.RetrieveAPIView):
# 	queryset = ParentalRating.objects.all()
# 	serializer_class = ParentalRatingSerializerDetail

# Credit Role

class CreditRoleListAPI(generics.ListAPIView):
	queryset = CreditRole.objects.all()
	serializer_class = CreditRoleSerializerList
	#filter_backends = [DjangoFilterBackend]
	#filterset_fields = ['credit_role']
	ordering_fields = ['credit_role']
	ordering = ['credit_role']
	pagination_class = None

# class CreditListAPISearch(generics.ListAPIView):
# 	queryset = Credit.objects.all()
# 	serializer_class = CreditRoleSerializerList
# 	filter_backends = [filters.SearchFilter]
# 	search_fields = ['credit_name']
# 	ordering_fields = ['id', 'credit_role']
# 	ordering = ['credit_role']

# class CreditRoleDetailAPI(generics.RetrieveAPIView):
# 	queryset = CreditRole.objects.all()
# 	serializer_class = CreditRoleSerializerDetail

# Credit

class CreditListAPI(generics.ListAPIView):
	queryset = Credit.objects.all()
	serializer_class = CreditSerializerList
	#filter_backends = [DjangoFilterBackend]
	#filterset_fields = ['credit_name']
	ordering_fields = ['id', 'credit_name', 'role', 'birth_date']
	ordering = ['credit_name']
	pagination_class = None

# class CreditListAPISearch(generics.ListAPIView):
# 	queryset = Credit.objects.all()
# 	serializer_class = CreditSerializerList
# 	filter_backends = [filters.SearchFilter]
# 	search_fields = ['credit_name']
# 	ordering_fields = ['id', 'credit_name', 'role', 'birth_date']
# 	ordering = ['-id']

# class CreditDetailAPI(generics.RetrieveAPIView):
# 	queryset = Credit.objects.all()
# 	serializer_class = CreditSerializerDetail

# Tags

class TagListAPI(generics.ListAPIView):
	queryset = Tag.objects.all()
	serializer_class = TagSerializerList
	ordering_fields = ['id', 'tag_name']
	ordering = ['tag_name']
	pagination_class = None
