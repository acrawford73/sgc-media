#from __future__ import unicode_literals
from django.shortcuts import render
from django.views.generic import ListView, DetailView, UpdateView
from .models import MediaVideo, MediaAudio, MediaPhoto
from rest_framework import generics
from .serializers import MediaVideoSerializerList, MediaVideoSerializerDetail
from .serializers import MediaAudioSerializerList, MediaAudioSerializerDetail
from .serializers import MediaPhotoSerializerList, MediaPhotoSerializerDetail


### Video
class MediaVideoListView(ListView):
	model = MediaVideo
	template_name = 'media/video_list.html'  #<app>/<model>_<viewtype>.html
	context_object_name = 'assets'
	ordering = ['-created']
	paginate_by = 15

class MediaVideoDetailView(DetailView):
	model = MediaVideo
	context_object_name = 'asset'

class MediaVideoUpdateView(UpdateView):
	model = MediaVideo
	context_object_name = 'asset'
	fields = ['is_published', 'title', 'short_description', 'long_description', 'notes']

class MediaVideoListAPI(generics.ListAPIView):
	queryset = MediaVideo.objects.all()  #.filter(is_published=True)
	serializer_class = MediaVideoSerializerList

class MediaVideoDetailAPI(generics.RetrieveAPIView):
	queryset = MediaVideo.objects.all()
	serializer_class = MediaVideoSerializerDetail


### Audio
class MediaAudioListView(ListView):
	model = MediaAudio
	template_name = 'media/audio_list.html'  #<app>/<model>_<viewtype>.html
	context_object_name = 'assets'
	ordering = ['-created']
	paginate_by = 15

class MediaAudioDetailView(DetailView):
	model = MediaAudio
	context_object_name = 'asset'

class MediaAudioUpdateView(UpdateView):
	model = MediaAudio
	context_object_name = 'asset'
	fields = ['is_published', 'title', 'artist', 'album', 'genre', 'location', 'geo_latitude', 'geo_longitude', 'short_description', 'notes']

class MediaAudioListAPI(generics.ListAPIView):
	queryset = MediaAudio.objects.all()
	serializer_class = MediaAudioSerializerList

class MediaAudioDetailAPI(generics.RetrieveAPIView):
	queryset = MediaAudio.objects.all()
	serializer_class = MediaAudioSerializerDetail


### Photo
class MediaPhotoListView(ListView):
	model = MediaPhoto
	template_name = 'media/photo_list.html'
	context_object_name = 'assets'
	ordering = ['-created']
	paginate_by = 15

class MediaPhotoDetailView(DetailView):
	model = MediaPhoto
	context_object_name = 'asset'

class MediaPhotoUpdateView(UpdateView):
	model = MediaPhoto
	context_object_name = 'asset'
	fields = ['is_public', 'title', 'short_description', 'notes', 'orientation', 'service', 'location', 'geo_latitude', 'geo_longitude']

class MediaPhotoListAPI(generics.ListAPIView):
	queryset = MediaPhoto.objects.all()
	serializer_class = MediaPhotoSerializerList

class MediaPhotoDetailAPI(generics.RetrieveAPIView):
	queryset = MediaPhoto.objects.all()
	serializer_class = MediaPhotoSerializerDetail
