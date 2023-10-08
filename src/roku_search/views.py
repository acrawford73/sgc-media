from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
### Templates
from django.views.generic import TemplateView, CreateView, ListView, DetailView, UpdateView
### Models
from .models import RokuSearchFeed
### Rest Framework
from rest_framework import generics
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
# Feeds
from .serializers import RokuSearchFeedSerializerList


# Roku Search Feed
class RokuSearchFeedCreateView(CreateView):
	model = RokuSearchFeed
	template_name = 'roku_search/rokusearchfeed_create.html'  #<app>/<model>_<viewtype>.html
	fields = ['provider_name', 'language', 'rating', 'categories', 'playlists', 'movies', \
		'live_feeds', 'series', 'short_form_videos', 'tv_specials']

class RokuSearchFeedListView(ListView):
	model = RokuSearchFeed
	template_name = 'roku_search/rokusearchfeed_list.html'  #<app>/<model>_<viewtype>.html
	context_object_name = 'rokusearchfeed'
	ordering = ['-id']
	#paginate_by = 15

class RokuSearchFeedDetailView(DetailView):
	model = RokuSearchFeed
	context_object_name = 'rokusearchfeed'

class RokuSearchFeedUpdateView(UpdateView):
	model = RokuSearchFeed
	context_object_name = 'rokusearchfeed'
	fields = fields = ['provider_name', 'language', 'rating', 'categories', 'playlists', 'movies', \
		'live_feeds', 'series', 'short_form_videos', 'tv_specials']

class RokuSearchFeedListAPI(generics.ListAPIView):
	queryset = RokuSearchFeed.objects.all().filter('is_public'=True)
	serializer_class = RokuSearchFeedSerializerList
	#filter_backends = [DjangoFilterBackend]
	#filterset_fields = ['category_name', 'playlist_name', 'query_string', 'order']
	#ordering_fields = ['id', 'category_name', 'playlist_name']
	ordering = ['-id']
