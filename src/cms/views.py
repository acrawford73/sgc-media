from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, ListView, DetailView, UpdateView, DeleteView
from.models import PlaylistVideo, PlatlistVideoItems, PlaylistAudio, PlaylistAudioItems, \
					PlaylistPhoto, PlaylistPhotoItems
from rest_framework import generics
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import PlaylistVideoSerializerList, PlaylistVideoSerializerDetail
from .serializers import PlaylistAudioSerializerList, PlaylistAudioSerializerDetail
from .serializers import PlaylistPhotoSerializerList, PlaylistPhotoSerializerDetail


### Video

class PlaylistVideoCreateView(CreateView):
	model = PlaylistVideo
	template_name = 'playlist/playlistvideo_create.html'  #<app>/<model>_<viewtype>.html
	fields = ['title', 'short_description', 'long_description', 'orientation', 'service', 'file_path', 'notes']

class PlaylistVideoListView(ListView):
	model = PlaylistVideo
	template_name = 'playlist/playlistvideo_list.html'  #<app>/<model>_<viewtype>.html
	context_object_name = 'assets'
	ordering = ['-created']
	paginate_by = 15

class PlaylistVideoDetailView(DetailView):
	model = PlaylistVideo
	context_object_name = 'asset'

class PlaylistVideoUpdateView(UpdateView):
	model = PlaylistVideo
	context_object_name = 'asset'
	fields = ['is_public', 'title', 'short_description', 'long_description', 'notes', 'tags', 'genre', 'service', 'service_name', 'Playlist_video_width', 'Playlist_video_height', 'orientation', 'location_city', 'location_state', 'location_country']

class PlaylistVideoListAPI(generics.ListAPIView):
	queryset = PlaylistVideo.objects.all().filter(is_public=True)
	serializer_class = PlaylistVideoSerializerList
	filter_backends = [DjangoFilterBackend]
	filterset_fields = ['service', 'orientation', 'username', 'doc_format']
	ordering_fields = ['id', 'created']
	ordering = ['-id']

class PlaylistVideoListAPISearch(generics.ListAPIView):
	queryset = PlaylistVideo.objects.all().filter(is_public=True)
	serializer_class = PlaylistVideoSerializerList
	filter_backends = [filters.SearchFilter]
	search_fields = ['title', 'short_description', 'long_description', 'service', 'orientation', 'username', '@tags', 'location_name', 'location_city', 'location_state', 'location_country']
	ordering_fields = ['id', 'created']
	ordering = ['-id']

class PlaylistVideoDetailAPI(generics.RetrieveAPIView):
	queryset = PlaylistVideo.objects.all()
	serializer_class = PlaylistVideoSerializerDetail
