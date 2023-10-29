from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
### Templates
from django.views.generic import TemplateView, CreateView, ListView, DetailView, UpdateView
### Models
from .models import SearchFeed
### Rest Framework
from rest_framework import generics
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
# Feeds
from .serializers import SearchFeedSerializerDetail


# Roku Search Feed
class SearchFeedCreateView(CreateView):
	model = SearchFeed
	fields = ['default_language']

class SearchFeedListView(ListView):
	model = SearchFeed
	#template_name = 'roku_search/searchfeed_list.html'  #<app>/<model>_<viewtype>.html
	context_object_name = 'searchfeed'
	ordering = ['-id']

class SearchFeedDetailView(DetailView):
	model = SearchFeed
	context_object_name = 'searchfeed'

class SearchFeedUpdateView(UpdateView):
	model = SearchFeed
	context_object_name = 'searchfeed'
	fields = ['default_language']

class SearchFeedDetailAPI(generics.RetrieveAPIView):
	queryset = SearchFeed.objects.all()
	serializer_class = SearchFeedSerializerDetail
	lookup_field = ['search_feed_id']
