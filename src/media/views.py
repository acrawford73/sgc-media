#from __future__ import unicode_literals
from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, ListView, DetailView, UpdateView, DeleteView
from .models import MediaVideo, MediaVideoFormat, MediaVideoGenre, MediaVideoService, \
					MediaAudio, MediaAudioFormat, \
					MediaPhoto, MediaPhotoFormat, \
					MediaDoc, MediaDocFormat
from rest_framework import generics
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
#from url_filter.filtersets import ModelFilterSet
from .serializers import MediaVideoSerializerList, MediaVideoSerializerDetail, MediaVideoGenreSerializerList
from .serializers import MediaAudioSerializerList, MediaAudioSerializerDetail, \
						 MediaAudioSerializerListArtists, MediaAudioSerializerListAlbums
from .serializers import MediaPhotoSerializerList, MediaPhotoSerializerDetail
from .serializers import MediaDocSerializerList, MediaDocSerializerDetail


### Upload
class MediaUploadView(TemplateView):
	template_name = 'media/upload.html'


### Video
class MediaVideoCreateView(CreateView):
	model = MediaVideo
	template_name = 'media/mediavideo_create.html'  #<app>/<model>_<viewtype>.html
	fields = ['title', 'short_description', 'long_description', 'orientation', 'service', 'file_path', 'notes']

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
	fields = ['is_public', 'title', 'short_description', 'long_description', 'notes', 'tags', 'genre', 'service', 'service_name', 'media_video_width', 'media_video_height', 'orientation', 'location_city', 'location_state', 'location_country']

class MediaVideoListAPI(generics.ListAPIView):
	queryset = MediaVideo.objects.all().filter(is_public=True)
	serializer_class = MediaVideoSerializerList
	filter_backends = [DjangoFilterBackend]
	filterset_fields = ['service', 'orientation', 'username', 'doc_format']
	ordering_fields = ['id', 'created']
	ordering = ['-id']

class MediaVideoListAPISearch(generics.ListAPIView):
	queryset = MediaVideo.objects.all().filter(is_public=True)
	serializer_class = MediaVideoSerializerList
	filter_backends = [filters.SearchFilter]
	search_fields = ['title', 'short_description', 'long_description', 'service', 'orientation', 'username', '@tags', 'location_name', 'location_city', 'location_state', 'location_country']
	ordering_fields = ['id', 'created']
	ordering = ['-id']

class MediaVideoGenreListAPI(generics.ListAPIView):
	queryset = MediaVideoGenre.objects.all()
	serializer_class = MediaVideoGenreSerializerList
	filter_backends = [DjangoFilterBackend]
	filterset_fields = ['genre']

class MediaVideoDetailAPI(generics.RetrieveAPIView):
	queryset = MediaVideo.objects.all()
	serializer_class = MediaVideoSerializerDetail

class MediaVideoGalleryListView(ListView):
	model = MediaVideo
	template_name = 'media/mediavideo_gallery.html'
	context_object_name = 'assets'
	ordering = ['-created']
	paginate_by = 24


class MediaVideoRSSFeed(Feed):
	title = "Video Feed"
	link = "/videos/rss/"
	description = "Latest videos"
	feed_copyright = "SGC-MEDIA-~2023"
	ttl = 600
	def items(self):
		return MediaVideo.objects.filter(is_public=True).order_by("-created")[:10]
	def item_title(self, item):
		return item.title
	def item_description(self, item):
		if (item.long_description is None) or (item.long_description == ""):
			item.long_description = "Long description is not available"
		return item.long_description
	def item_link(self, item):
		return "/videos/%s/" % (item.id)
	def item_author_name(self, item):
		if (item.username is None) or (item.username == ""):
			return "Unknown"
		else:
			return item.username
	def item_guid(self, item):
		guid = item.file_uuid
		return guid.upper()
	def item_pubdate(self, item):
		return item.created
	### should implement
	#def item_updateddate(self, item):
	#	return item.updated
	def get_feed(self, obj, request):
		feedgen = super().get_feed(obj, request)
		feedgen.content_type = "application/xml; charset=utf-8"
		return feedgen

class MediaVideoAtomFeed(MediaVideoRSSFeed):
    feed_type = Atom1Feed
    subtitle = MediaVideoRSSFeed.description

#class MediaVideoRokuRSSFeed(Feed):


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
	fields = ['is_public', 'rating', 'title', 'artist', 'album', 'genre', 'short_description', 'long_description', 'source', 'notes']

# class MediaAudioDeleteView(DeleteView):
# 	model = MediaAudio
# 	template_name = 'media/mediaaudio_confirm_delete.html'
# 	context_object_name = 'asset'
# 	success_url = reverse_lazy('media-audio-list')

class MediaAudioListAPI(generics.ListAPIView):
	queryset = MediaAudio.objects.all().filter(is_public=True)
	serializer_class = MediaAudioSerializerList
	filter_backends = [DjangoFilterBackend]
	filterset_fields = ['service', 'artist', 'album', 'album_artist', 'composer', 'genre', 'year']
	ordering_fields = ['id', 'created']
	ordering = ['-id']

class MediaAudioListAPIArtists(generics.ListAPIView):
	queryset = MediaAudio.objects.order_by("artist").distinct("artist").filter(is_public=True)
	serializer_class = MediaAudioSerializerListArtists
	filter_backends = [DjangoFilterBackend]
	filterset_fields = ['artist']

class MediaAudioListAPIAlbums(generics.ListAPIView):
	queryset = MediaAudio.objects.order_by("album").distinct("album").filter(is_public=True)
	serializer_class = MediaAudioSerializerListAlbums
	filter_backends = [DjangoFilterBackend]
	filterset_fields = ['album']

class MediaAudioListAPISearch(generics.ListAPIView):
	queryset = MediaAudio.objects.all().filter(is_public=True)
	serializer_class = MediaAudioSerializerList
	filter_backends = [filters.SearchFilter]
	search_fields = ['title', 'artist', 'album', 'genre', 'year', 'service', '@tags']
	ordering_fields = ['id', 'created']
	ordering = ['-id']

class MediaAudioDetailAPI(generics.RetrieveAPIView):
	queryset = MediaAudio.objects.all()
	serializer_class = MediaAudioSerializerDetail

class MediaAudioGalleryListView(ListView):
	model = MediaAudio
	template_name = 'media/mediaaudio_gallery.html'
	context_object_name = 'assets'
	ordering = ['-created']
	paginate_by = 24


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
	fields = ['is_public', 'title', 'short_description', 'long_description', 'notes', 'width', 'height', 'orientation', 'photo_format', 'service', 'tags', 'location_name', 'location_city', 'location_state', 'location_country']

class MediaPhotoListAPI(generics.ListAPIView):
	queryset = MediaPhoto.objects.all().filter(is_public=True)
	serializer_class = MediaPhotoSerializerList
	filter_backends = [DjangoFilterBackend]
	filterset_fields = ['service', 'orientation', 'username']
	ordering_fields = ['id', 'created']
	ordering = ['-id']

class MediaPhotoListAPISearch(generics.ListAPIView):
	queryset = MediaPhoto.objects.all().filter(is_public=True)
	serializer_class = MediaPhotoSerializerList
	filter_backends = [filters.SearchFilter]
	search_fields = ['title', 'short_description', 'long_description', 'service', 'orientation', 'photo_format', 'username', '@tags', 'location_name', 'location_city', 'location_state', 'location_country']
	ordering_fields = ['id', 'created']
	ordering = ['-id']

class MediaPhotoDetailAPI(generics.RetrieveAPIView):
	queryset = MediaPhoto.objects.all()
	serializer_class = MediaPhotoSerializerDetail

class MediaPhotoGalleryListView(ListView):
	model = MediaPhoto
	template_name = 'media/mediaphoto_gallery.html'
	context_object_name = 'assets'
	ordering = ['-created']
	paginate_by = 24


### Documents
class MediaDocListView(ListView):
	model = MediaDoc
	template_name = 'media/doc_list.html'
	context_object_name = 'assets'
	ordering = ['-created']
	paginate_by = 15

class MediaDocDetailView(DetailView):
	model = MediaDoc
	context_object_name = 'asset'

class MediaDocUpdateView(UpdateView):
	model = MediaDoc
	context_object_name = 'asset'
	fields = ['is_public', 'title', 'short_description', 'long_description', 'notes', 'source_url', 'doi_url', 'category', 'keywords', 'tags']

class MediaDocListAPI(generics.ListAPIView):
	queryset = MediaDoc.objects.all().filter(is_public=True)
	serializer_class = MediaDocSerializerList
	filter_backends = [DjangoFilterBackend]
	filterset_fields = ['keywords', 'doc_format']
	ordering_fields = ['id', 'created']
	ordering = ['-id']

class MediaDocListAPISearch(generics.ListAPIView):
	queryset = MediaDoc.objects.all().filter(is_public=True)
	serializer_class = MediaDocSerializerList
	filter_backends = [filters.SearchFilter]
	search_fields = ['title', 'short_description', 'long_description', 'notes', 'doc_format', 'keywords', '@tags'] 
	ordering_fields = ['id', 'created']
	ordering = ['-id']

class MediaDocDetailAPI(generics.RetrieveAPIView):
	queryset = MediaDoc.objects.all()
	serializer_class = MediaDocSerializerDetail
