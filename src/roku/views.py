from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
# Templates
from django.views.generic import TemplateView, CreateView, ListView, DetailView, UpdateView, DeleteView
# Models
### Roku Content Categories, Types, Properties
from .models import Category, Playlist
from .models import Movie, LiveFeed, Series, Season, Episode, ShortFormVideo, TVSpecial
from .models import Content, Video, Caption, TrickPlayFile, Genre, ExternalID, Rating, RatingSource, ParentalRating, Credit

### Rest Framework
from rest_framework import generics
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

# Serializers

## Roku Content
# Categories
from .serializers import CategorySerializerList, PlaylistSerializerList
# Types
from .serializers import MovieSerializerList, LiveFeedSerializerList, SeriesSerializerList
from .serializers import SeasonSerializerList, EpisodeSerializerList, ShortFormVideoSerializerList
from .serializers import TVSpecialSerializerList
# Properties
from .serializers import ContentSerializerList, VideoSerializerList, CaptionSerializerList
from .serializers import TrickPlayFileSerializerList, GenreSerializerList, ExternalIDSerializerList
from .serializers import RatingSerializerList, RatingSourceSerializerList, ParentalRatingSerializerList
from .serializers import CreditSerializerList

#

## Roku Content Categories
# Category
class CategoryCreateView(CreateView):
	model = Category
	template_name = 'cms/category_create.html'  #<app>/<model>_<viewtype>.html
	fields = ['category_name', 'playlist_name', 'query_string', 'order']

class CategoryListView(ListView):
	model = Category
	template_name = 'cms/category_list.html'  #<app>/<model>_<viewtype>.html
	context_object_name = 'category'
	ordering = ['-id']
	paginate_by = 15

class CategoryDetailView(DetailView):
	model = Category
	context_object_name = 'category'

class CategoryUpdateView(UpdateView):
	model = Category
	context_object_name = 'category'
	fields = ['category_name', 'playlist_name', 'query_string', 'order']

class CategoryListAPI(generics.ListAPIView):
	queryset = Category.objects.all()
	serializer_class = CategorySerializerList
	filter_backends = [DjangoFilterBackend]
	filterset_fields = ['category_name', 'playlist_name', 'query_string', 'order']
	ordering_fields = ['id', 'category_name', 'playlist_name']
	ordering = ['-id']

class CategoryListAPISearch(generics.ListAPIView):
	queryset = Category.objects.all()
	serializer_class = CategorySerializerList
	filter_backends = [filters.SearchFilter]
	search_fields = ['title', 'short_description', 'long_description', 'service', 'orientation', 'username', '@tags', 'location_name', 'location_city', 'location_state', 'location_country']
	ordering_fields = ['id', 'category_name', 'playlist_name']
	ordering = ['-id']

class CategoryDetailAPI(generics.RetrieveAPIView):
	queryset = Category.objects.all()
	serializer_class = CategorySerializerDetail

# Playlist
class PlaylistCreateView(CreateView):
	model = Playlist
	template_name = 'cms/playlist_create.html'  #<app>/<model>_<viewtype>.html
	fields = ['playlist_name', 'item_ids', 'short_description', 'notes']

class PlaylistListView(ListView):
	model = Playlist
	template_name = 'cms/playlist_list.html'  #<app>/<model>_<viewtype>.html
	context_object_name = 'playlist'
	ordering = ['-id']
	paginate_by = 15

class PlaylistDetailView(DetailView):
	model = Playlist
	context_object_name = 'playlist'

class PlaylistUpdateView(UpdateView):
	model = Playlist
	context_object_name = 'playlist'
	fields = ['playlist_name', 'item_ids', 'short_description', 'notes', 'is_public']

class PlaylistListAPI(generics.ListAPIView):
	queryset = Playlist.objects.all()
	serializer_class = PlaylistSerializerList
	filter_backends = [DjangoFilterBackend]
	filterset_fields = ['playlist_name', 'short_description', 'notes', 'is_public']
	ordering_fields = ['id', 'playlist_name']
	ordering = ['-id']

class PlaylistListAPISearch(generics.ListAPIView):
	queryset = Playlist.objects.all()
	serializer_class = PlaylistSerializerList
	filter_backends = [filters.SearchFilter]
	search_fields = ['playlist_name', 'short_description', 'notes', 'created', 'is_public']
	ordering_fields = ['id', 'playlist_name', 'created']
	ordering = ['-id']

class PlaylistDetailAPI(generics.RetrieveAPIView):
	queryset = Playlist.objects.all()
	serializer_class = PlaylistSerializerDetail
	filter_backends = [DjangoFilterBackend]
	filterset_fields = ['playlist_name', 'short_description', 'notes', 'created']

# Video
class VideoCreateView(CreateView):
	model = Video
	template_name = 'cms/video_create.html'  #<app>/<model>_<viewtype>.html
	fields = ['category_name', 'playlist_name', 'query_string', 'order']

class VideoListView(ListView):
	model = Video
	template_name = 'cms/video_list.html'  #<app>/<model>_<viewtype>.html
	context_object_name = 'video'
	ordering = ['-id']
	paginate_by = 15

class VideoDetailView(DetailView):
	model = Video
	context_object_name = 'video'

class VideoUpdateView(UpdateView):
	model = Video
	context_object_name = 'video'
	fields = ['category_name', 'playlist_name', 'query_string', 'order']

class VideoListAPI(generics.ListAPIView):
	queryset = Video.objects.all()
	serializer_class = VideoSerializerList
	filter_backends = [DjangoFilterBackend]
	filterset_fields = ['category_name', 'playlist_name', 'query_string', 'order']
	ordering_fields = ['id', 'category_name', 'playlist_name']
	ordering = ['-id']

class VideoListAPISearch(generics.ListAPIView):
	queryset = Video.objects.all()
	serializer_class = VideoSerializerList
	filter_backends = [filters.SearchFilter]
	search_fields = ['title', 'short_description', 'long_description', 'service', 'orientation', 'username', '@tags', 'location_name', 'location_city', 'location_state', 'location_country']
	ordering_fields = ['id', 'category_name', 'playlist_name']
	ordering = ['-id']

class VideoDetailAPI(generics.RetrieveAPIView):
	queryset = Video.objects.all()
	serializer_class = VideoSerializerDetail
