import logging
logger = logging.getLogger(__name__)
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
### Templates
from django.views.generic import TemplateView, CreateView, ListView, DetailView, UpdateView
### Models
## Roku Content Feeds, Categories, Types, Properties
from .models import RokuContentFeed
from .models import Language, Category, Playlist
from .models import Movie, LiveFeed, Series, Season, Episode, ShortFormVideo, TVSpecial
from .models import Content, Video, Caption, TrickPlayFile, Genre, ExternalID, Rating, \
					RatingSource, Country, ParentalRating, CreditRole, Credit, Tag
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
from .api.serializers import RokuContentFeedSerializerList, RokuContentFeedSerializerDetail #, RokuSearchFeedSerializerList
# Categories
from .api.serializers import CategorySerializerList, PlaylistSerializerList
# Types
from .api.serializers import MovieSerializerList, LiveFeedSerializerList, SeriesSerializerList
from .api.serializers import SeasonSerializerList, EpisodeSerializerList, ShortFormVideoSerializerList
from .api.serializers import TVSpecialSerializerList
# Properties
from .api.serializers import ContentSerializerList, VideoSerializerList, CaptionSerializerList
from .api.serializers import TrickPlayFileSerializerList, GenreSerializerList, ExternalIDSerializerList
from .api.serializers import RatingSerializerList, RatingSourceSerializerList, CountrySerializerList, ParentalRatingSerializerList
from .api.serializers import CreditRoleSerializerList, CreditSerializerList, LanguageSerializerList, TagSerializerList


## Roku Feeds

# Roku Content Feed
class RokuContentFeedCreateView(LoginRequiredMixin, CreateView):
	"""
	Roku Content Feed fields for CreateView :model:`roku_content.RokuContentFeed`.

	**Context**

	``rokucontentfeed``
		An instance of :model:`roku_content.RokuContentFeed``.

	**Template:**

	:template:`roku_content/rokucontentfeed_create.html`
	"""
	model = RokuContentFeed
	fields = ['is_public', 'short_description', 'provider_name', 'language', 'rating', \
		'categories', 'playlists', 'movies', 'live_feeds', 'series', 'short_form_videos', 'tv_specials']

class RokuContentFeedListView(LoginRequiredMixin, ListView):
	"""
	Roku Content Feed fields for ListView :model:`roku_content.RokuContentFeed`.

	**Context**

	``rokucontentfeed``
		An instance of :model:`roku_content.RokuContentFeed``.

	**Template:**

	:template:`roku_content/rokucontentfeed_list.html`
	"""
	model = RokuContentFeed
	template_name = 'roku_content/rokucontentfeed_list.html'  #<app>/<model>_<viewtype>.html
	context_object_name = 'rokucontentfeed'
	ordering = ['-id']
	#paginate_by = 15

class RokuContentFeedDetailView(LoginRequiredMixin, DetailView):
	"""
	Roku Content Feed fields for DetailView :model:`roku_content.RokuContentFeed`.

	**Context**

	``rokucontentfeed``
		An instance of :model:`roku_content.RokuContentFeed``.

	**Template:**

	:template:`roku_content/rokucontentfeed_detail.html`
	"""
	model = RokuContentFeed
	context_object_name = 'rokucontentfeed'

class RokuContentFeedUpdateView(LoginRequiredMixin, UpdateView):
	"""
	Roku Content Feed fields for UpdateView :model:`roku_content.RokuContentFeed`.

	**Context**

	``rokucontentfeed``
		An instance of :model:`roku_content.RokuContentFeed``.

	**Template:**

	:template:`roku_content/rokucontentfeed_form.html`
	"""
	model = RokuContentFeed
	context_object_name = 'rokucontentfeed'
	fields = ['is_public', 'short_description', 'provider_name', 'language', 'rating', \
		'categories', 'playlists', 'movies', 'live_feeds', 'series', 'short_form_videos', 'tv_specials']

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
			logger.debug("RokuContentFeed object " + str(feed.pk) + " returned.")
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
			logger.debug("RokuContentFeed object " + str(feed.pk) + " returned.")
		return Response(serializer.data)


## Roku Content Categories

# Language
class LanguageCreateView(LoginRequiredMixin, CreateView):
	model = Language
	fields = ['language_name_eng', 'code_iso_639_2', 'code_iso_639_1']

class LanguageListView(LoginRequiredMixin, ListView):
	model = Language
	template_name = 'roku_content/language_list.html'  #<app>/<model>_<viewtype>.html
	context_object_name = 'language'
	ordering = ['id']
	paginate_by = 15

class LanguageDetailView(LoginRequiredMixin, DetailView):
	model = Language
	context_object_name = 'language'

class LanguageUpdateView(LoginRequiredMixin, UpdateView):
	model = Language
	context_object_name = 'language'
	fields = ['language_name_eng', 'code_iso_639_2', 'code_iso_639_1']

class LanguageListAPI(generics.ListAPIView):
	queryset = Language.objects.all()
	serializer_class = LanguageSerializerList
	ordering_fields = ['id', 'code_iso_639_2', 'code_iso_639_1', 'language_name_eng']
	ordering = ['language_name_eng']

# Category
class CategoryCreateView(LoginRequiredMixin, CreateView):
	model = Category
	fields = ['category_name', 'playlist_name', 'query_string', 'order']

class CategoryListView(LoginRequiredMixin, ListView):
	model = Category
	template_name = 'roku_content/category_list.html'  #<app>/<model>_<viewtype>.html
	context_object_name = 'category'
	ordering = ['-id']
	paginate_by = 15

class CategoryDetailView(LoginRequiredMixin, DetailView):
	model = Category
	context_object_name = 'category'

class CategoryUpdateView(LoginRequiredMixin, UpdateView):
	model = Category
	context_object_name = 'category'
	fields = ['category_name', 'playlist_name', 'query_string', 'order']

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
class PlaylistCreateView(LoginRequiredMixin, CreateView):
	model = Playlist
	fields = ['playlist_name', 'short_description', 'item_ids']

class PlaylistListView(LoginRequiredMixin, ListView):
	model = Playlist
	template_name = 'roku_content/playlist_list.html'  #<app>/<model>_<viewtype>.html
	context_object_name = 'playlist'
	ordering = ['-id']
	paginate_by = 15

class PlaylistDetailView(LoginRequiredMixin, DetailView):
	model = Playlist
	context_object_name = 'playlist'

class PlaylistUpdateView(LoginRequiredMixin, UpdateView):
	model = Playlist
	context_object_name = 'playlist'
	fields = ['playlist_name', 'short_description', 'item_ids']

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
class MovieCreateView(LoginRequiredMixin, CreateView):
	model = Movie
	fields = ['title', 'short_description', 'long_description', 'content', \
		'thumbnail', 'release_date', 'genres', 'rating', 'tags', 'credits', 'external_ids']

class MovieListView(LoginRequiredMixin, ListView):
	model = Movie
	template_name = 'roku_content/movie_list.html'  #<app>/<model>_<viewtype>.html
	context_object_name = 'movie'
	ordering = ['-id']
	paginate_by = 15

class MovieDetailView(LoginRequiredMixin, DetailView):
	model = Movie
	context_object_name = 'movie'

class MovieUpdateView(LoginRequiredMixin, UpdateView):
	model = Movie
	context_object_name = 'movie'
	fields = ['title', 'short_description', 'long_description', 'content', \
		'thumbnail', 'release_date', 'genres', 'rating', 'tags', 'credits', 'external_ids']

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
class LiveFeedCreateView(LoginRequiredMixin, CreateView):
	model = LiveFeed
	fields = ['title', 'short_description', 'long_description', 'content', \
		'thumbnail', 'branded_thumbnail', 'tags', 'rating', 'genres']

class LiveFeedListView(LoginRequiredMixin, ListView):
	model = LiveFeed
	template_name = 'roku_content/livefeed_list.html'  #<app>/<model>_<viewtype>.html
	context_object_name = 'livefeed'
	ordering = ['-id']
	paginate_by = 15

class LiveFeedDetailView(LoginRequiredMixin, DetailView):
	model = LiveFeed
	context_object_name = 'livefeed'

class LiveFeedUpdateView(LoginRequiredMixin, UpdateView):
	model = LiveFeed
	context_object_name = 'livefeed'
	fields = ['title', 'short_description', 'long_description', 'content', \
		'thumbnail', 'branded_thumbnail', 'tags', 'rating', 'genres']

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
class SeriesCreateView(LoginRequiredMixin, CreateView):
	model = Series
	fields = ['title', 'short_description', 'long_description', 'seasons', 'episodes', \
		'thumbnail', 'release_date', 'genres', 'tags', 'credits', 'external_ids']

class SeriesListView(LoginRequiredMixin, ListView):
	model = Series
	template_name = 'roku_content/series_list.html'  #<app>/<model>_<viewtype>.html
	context_object_name = 'series'
	ordering = ['-id']
	paginate_by = 15

class SeriesDetailView(LoginRequiredMixin, DetailView):
	model = Series
	context_object_name = 'series'

class SeriesUpdateView(LoginRequiredMixin, UpdateView):
	model = Series
	context_object_name = 'series'
	fields = ['title', 'short_description', 'long_description', 'seasons', 'episodes', \
		'thumbnail', 'release_date', 'genres', 'tags', 'credits', 'external_ids']

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
class SeasonCreateView(LoginRequiredMixin, CreateView):
	model = Season
	fields = ['title_season', 'season_number', 'episodes']

class SeasonListView(LoginRequiredMixin, ListView):
	model = Season
	template_name = 'roku_content/season_list.html'  #<app>/<model>_<viewtype>.html
	context_object_name = 'season'
	ordering = ['-id']
	paginate_by = 15

class SeasonDetailView(LoginRequiredMixin, DetailView):
	model = Season
	context_object_name = 'season'

class SeasonUpdateView(LoginRequiredMixin, UpdateView):
	model = Season
	context_object_name = 'season'
	fields = ['title_season', 'season_number', 'episodes']

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
class EpisodeCreateView(LoginRequiredMixin, CreateView):
	model = Episode
	fields = ['episode_number', 'title', 'short_description', 'long_description', \
		'content', 'thumbnail', 'release_date', 'rating', 'credits', 'external_ids']

class EpisodeListView(LoginRequiredMixin, ListView):
	model = Episode
	template_name = 'roku_content/episode_list.html'  #<app>/<model>_<viewtype>.html
	context_object_name = 'episode'
	ordering = ['title']
	paginate_by = 15

class EpisodeDetailView(LoginRequiredMixin, DetailView):
	model = Episode
	context_object_name = 'episode'

class EpisodeUpdateView(LoginRequiredMixin, UpdateView):
	model = Episode
	context_object_name = 'episode'
	fields = ['episode_number', 'title', 'short_description', 'long_description', \
		'content', 'thumbnail', 'release_date', 'rating', 'credits', 'external_ids']

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
class ShortFormVideoCreateView(LoginRequiredMixin, CreateView):
	model = ShortFormVideo
	fields = ['title', 'short_description', 'long_description', 'content', 'thumbnail', \
		'release_date', 'tags', 'genres', 'rating', 'credits']

class ShortFormVideoListView(LoginRequiredMixin, ListView):
	model = ShortFormVideo
	template_name = 'roku_content/shortformvideo_list.html'  #<app>/<model>_<viewtype>.html
	context_object_name = 'shortformvideo'
	ordering = ['-id']
	paginate_by = 15

class ShortFormVideoDetailView(LoginRequiredMixin, DetailView):
	model = ShortFormVideo
	context_object_name = 'shortformvideo'

class ShortFormVideoUpdateView(LoginRequiredMixin, UpdateView):
	model = ShortFormVideo
	context_object_name = 'shortformvideo'
	fields = ['title', 'short_description', 'long_description', 'content', 'thumbnail', \
		'release_date', 'tags', 'genres', 'rating', 'credits']

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
class TVSpecialCreateView(LoginRequiredMixin, CreateView):
	model = TVSpecial
	fields = ['title', 'short_description', 'long_description', 'content', \
		'thumbnail', 'genres', 'rating', 'tags', 'release_date', 'credits', 'external_ids']

class TVSpecialListView(LoginRequiredMixin, ListView):
	model = TVSpecial
	template_name = 'roku_content/tvspecial_list.html'  #<app>/<model>_<viewtype>.html
	context_object_name = 'tvspecial'
	ordering = ['-id']
	paginate_by = 15

class TVSpecialDetailView(LoginRequiredMixin, DetailView):
	model = TVSpecial
	context_object_name = 'tvspecial'

class TVSpecialUpdateView(LoginRequiredMixin, UpdateView):
	model = TVSpecial
	context_object_name = 'tvspecial'
	fields = ['title', 'short_description', 'long_description', 'content', \
		'thumbnail', 'genres', 'rating', 'tags', 'release_date', 'credits', 'external_ids']

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
class ContentCreateView(LoginRequiredMixin, CreateView):
	model = Content
	fields = ['title', 'language', 'duration', 'videos', 'captions', 'trick_play_files', \
		 'validity_start_period', 'validity_end_period']

class ContentListView(LoginRequiredMixin, ListView):
	model = Content
	template_name = 'roku_content/content_list.html'  #<app>/<model>_<viewtype>.html
	context_object_name = 'content'
	ordering = ['-id']
	paginate_by = 15

class ContentDetailView(LoginRequiredMixin, DetailView):
	model = Content
	context_object_name = 'content'

class ContentUpdateView(LoginRequiredMixin, UpdateView):
	model = Content
	context_object_name = 'content'
	fields = ['title', 'language', 'duration', 'videos', 'captions', 'trick_play_files', \
		 'validity_start_period', 'validity_end_period']

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
class VideoCreateView(LoginRequiredMixin, CreateView):
	model = Video
	fields = ['url', 'quality', 'video_type']

class VideoListView(LoginRequiredMixin, ListView):
	model = Video
	template_name = 'roku_content/video_list.html'  #<app>/<model>_<viewtype>.html
	context_object_name = 'video'
	ordering = ['-id']
	paginate_by = 15

class VideoDetailView(LoginRequiredMixin, DetailView):
	model = Video
	context_object_name = 'video'

class VideoUpdateView(LoginRequiredMixin, UpdateView):
	model = Video
	context_object_name = 'video'
	fields = ['url', 'quality', 'video_type']

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
class CaptionCreateView(LoginRequiredMixin, CreateView):
	model = Caption
	fields = ['url', 'language', 'caption_type']

class CaptionListView(LoginRequiredMixin, ListView):
	model = Caption
	template_name = 'roku_content/caption_list.html'  #<app>/<model>_<viewtype>.html
	context_object_name = 'caption'
	ordering = ['-id']
	paginate_by = 15

class CaptionDetailView(LoginRequiredMixin, DetailView):
	model = Caption
	context_object_name = 'caption'

class CaptionUpdateView(LoginRequiredMixin, UpdateView):
	model = Caption
	context_object_name = 'caption'
	fields = ['url', 'language', 'caption_type']

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
class TrickPlayFileCreateView(LoginRequiredMixin, CreateView):
	model = TrickPlayFile
	fields = ['url', 'quality']

class TrickPlayFileListView(LoginRequiredMixin, ListView):
	model = TrickPlayFile
	template_name = 'roku_content/trickplayfile_list.html'  #<app>/<model>_<viewtype>.html
	context_object_name = 'trickplayfile'
	ordering = ['-id']
	paginate_by = 15

class TrickPlayFileDetailView(LoginRequiredMixin, DetailView):
	model = TrickPlayFile
	context_object_name = 'trickplayfile'

class TrickPlayFileUpdateView(LoginRequiredMixin, UpdateView):
	model = TrickPlayFile
	context_object_name = 'trickplayfile'
	fields = ['url', 'quality']

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
class GenreCreateView(LoginRequiredMixin, CreateView):
	model = Genre
	fields = ['genre']

class GenreListView(LoginRequiredMixin, ListView):
	model = Genre
	template_name = 'roku_content/genre_list.html'  #<app>/<model>_<viewtype>.html
	context_object_name = 'genre'
	ordering = ['genre']
	paginate_by = 15

class GenreDetailView(LoginRequiredMixin, DetailView):
	model = Genre
	context_object_name = 'genre'

class GenreUpdateView(LoginRequiredMixin, UpdateView):
	model = Genre
	context_object_name = 'genre'
	fields = ['genre']

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
class ExternalIDCreateView(LoginRequiredMixin, CreateView):
	model = ExternalID
	fields = ['external_id', 'id_type']

class ExternalIDListView(LoginRequiredMixin, ListView):
	model = ExternalID
	template_name = 'roku_content/externalid_list.html'  #<app>/<model>_<viewtype>.html
	context_object_name = 'externalid'
	ordering = ['external_id']
	paginate_by = 15

class ExternalIDDetailView(LoginRequiredMixin, DetailView):
	model = ExternalID
	context_object_name = 'externalid'

class ExternalIDUpdateView(LoginRequiredMixin, UpdateView):
	model = ExternalID
	context_object_name = 'externalid'
	fields = ['external_id', 'id_type']

class ExternalIDListAPI(generics.ListAPIView):
	queryset = ExternalID.objects.all()
	serializer_class = ExternalIDSerializerList
	#filter_backends = [DjangoFilterBackend]
	#filterset_fields = ['external_id']
	ordering_fields = ['id', 'external_id', 'id_type']
	ordering = ['-id']

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
class RatingCreateView(LoginRequiredMixin, CreateView):
	model = Rating
	fields = ['rating', 'rating_source']

class RatingListView(LoginRequiredMixin, ListView):
	model = Rating
	template_name = 'roku_content/rating_list.html'  #<app>/<model>_<viewtype>.html
	context_object_name = 'rating'
	ordering = ['rating']
	paginate_by = 15

class RatingDetailView(LoginRequiredMixin, DetailView):
	model = Rating
	context_object_name = 'rating'

class RatingUpdateView(LoginRequiredMixin, UpdateView):
	model = Rating
	context_object_name = 'rating'
	fields = ['rating', 'rating_source']

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
class RatingSourceCreateView(LoginRequiredMixin, CreateView):
	model = RatingSource
	fields = ['source_name', 'source_long_name', 'source_country', 'source_url']

class RatingSourceListView(LoginRequiredMixin, ListView):
	model = RatingSource
	template_name = 'roku_content/ratingsource_list.html'  #<app>/<model>_<viewtype>.html
	context_object_name = 'ratingsource'
	ordering = ['source_name']
	paginate_by = 15

class RatingSourceDetailView(LoginRequiredMixin, DetailView):
	model = RatingSource
	context_object_name = 'ratingsource'

class RatingSourceUpdateView(LoginRequiredMixin, UpdateView):
	model = RatingSource
	context_object_name = 'ratingsource'
	fields = ['source_name', 'source_long_name', 'source_country', 'source_url']

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
class ParentalRatingCreateView(LoginRequiredMixin, CreateView):
	model = ParentalRating
	fields = ['parental_rating']

class ParentalRatingListView(LoginRequiredMixin, ListView):
	model = ParentalRating
	template_name = 'roku_content/parentalrating_list.html'  #<app>/<model>_<viewtype>.html
	context_object_name = 'parentalrating'
	ordering = ['parental_rating']
	paginate_by = 15

class ParentalRatingDetailView(LoginRequiredMixin, DetailView):
	model = ParentalRating
	context_object_name = 'parentalrating'

class ParentalRatingUpdateView(LoginRequiredMixin, UpdateView):
	model = ParentalRating
	context_object_name = 'parentalrating'
	fields = ['parental_rating']

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
class CreditRoleCreateView(LoginRequiredMixin, CreateView):
	model = CreditRole
	fields = ['credit_role']

class CreditRoleListView(LoginRequiredMixin, ListView):
	model = CreditRole
	template_name = 'roku_content/creditrole_list.html'  #<app>/<model>_<viewtype>.html
	context_object_name = 'creditrole'
	ordering = ['credit_role']
	paginate_by = 15

class CreditRoleDetailView(LoginRequiredMixin, DetailView):
	model = CreditRole
	context_object_name = 'creditrole'

class CreditRoleUpdateView(LoginRequiredMixin, UpdateView):
	model = CreditRole
	context_object_name = 'creditrole'
	fields = ['credit_role']

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
class CreditCreateView(LoginRequiredMixin, CreateView):
	model = Credit
	fields = ['credit_name', 'role', 'birth_date']

class CreditListView(LoginRequiredMixin, ListView):
	model = Credit
	template_name = 'roku_content/credit_list.html'  #<app>/<model>_<viewtype>.html
	context_object_name = 'credit'
	ordering = ['credit_name']
	paginate_by = 15

class CreditDetailView(LoginRequiredMixin, DetailView):
	model = Credit
	context_object_name = 'credit'

class CreditUpdateView(LoginRequiredMixin, UpdateView):
	model = Credit
	context_object_name = 'credit'
	fields = ['credit_name', 'role', 'birth_date']

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

class TagCreateView(LoginRequiredMixin, CreateView):
	model = Tag
	fields = ['tag_name']

class TagListView(LoginRequiredMixin, ListView):
	model = Tag
	template_name = 'roku_content/tag_list.html'  #<app>/<model>_<viewtype>.html
	context_object_name = 'tag'
	ordering = ['tag_name']

class TagDetailView(LoginRequiredMixin, DetailView):
	model = Tag
	context_object_name = 'tag'

class TagUpdateView(LoginRequiredMixin, UpdateView):
	model = Tag
	context_object_name = 'tag'
	fields = ['tag_name']

class TagListAPI(generics.ListAPIView):
	queryset = Tag.objects.all()
	serializer_class = TagSerializerList
	ordering_fields = ['id', 'tag_name']
	ordering = ['tag_name']
	pagination_class = None
