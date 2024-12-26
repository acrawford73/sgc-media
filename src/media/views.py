#from __future__ import unicode_literals
from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, CreateView, ListView, DetailView, UpdateView, DeleteView
from bootstrap_datepicker_plus.widgets import DatePickerInput
from .models import MediaVideo, MediaVideoFormat, MediaVideoGenre, MediaVideoService
from .models import MediaAudio, MediaAudioFormat, MediaAudioService
from .models import MediaPhoto, MediaPhotoFormat, MediaPhotoService
from .models import MediaDoc, MediaDocFormat, MediaDocService
from .models import MediaCountry, MediaTag
from rest_framework import generics
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
#from url_filter.filtersets import ModelFilterSet
from .serializers import MediaVideoSerializerList, MediaVideoSerializerDetail, MediaVideoGenreSerializerList, \
						 MediaVideoServiceSerializerList, MediaVideoServiceSerializerDetail
from .serializers import MediaAudioSerializerList, MediaAudioSerializerDetail, MediaAudioServiceSerializerList, \
						 MediaAudioServiceSerializerDetail, MediaAudioSerializerListArtists, MediaAudioSerializerListAlbums
from .serializers import MediaPhotoSerializerList, MediaPhotoSerializerDetail, \
						 MediaPhotoServiceSerializerList, MediaPhotoServiceSerializerDetail
from .serializers import MediaDocSerializerList, MediaDocSerializerDetail, MediaDocServiceSerializerList, MediaDocServiceSerializerDetail
from .serializers import MediaTagSerializerList

### Transcription
# class TranscriptionCreateView(CreateView):
# 	model = Transcription
# 	#template_name = 'media/transcription_create.html'  #<app>/<model>_<viewtype>.html
# 	fields = ['language']

# class TranscriptionListView(ListView):
# 	model = Transcription
# 	#template_name = 'media/transcription_list.html'  #<app>/<model>_<viewtype>.html
# 	context_object_name = 'transcription'
# 	ordering = ['-id']
# 	paginate_by = 15

# class TranscriptionDetailView(DetailView):
# 	model = Transcription
# 	context_object_name = 'transcription'

# class TranscriptionUpdateView(UpdateView):
# 	model = Transcription
# 	context_object_name = 'transcription'
# 	fields = ['language', 'transcription']



### Upload
class MediaUploadView(TemplateView):
	template_name = 'media/upload.html'


### Video
class MediaVideoCreateView(LoginRequiredMixin, CreateView):
	model = MediaVideo
	template_name = 'media/video/mediavideo_create.html'  #<app>/<model>_<viewtype>.html
	fields = ['title', 'short_description', 'long_description', 'orientation', 'service', 'file_path', 'notes']

class MediaVideoListView(LoginRequiredMixin, ListView):
	model = MediaVideo
	template_name = 'media/video/video_list.html'
	context_object_name = 'assets'
	ordering = ['-created']
	paginate_by = 15

class MediaVideoDetailView(LoginRequiredMixin, DetailView):
	model = MediaVideo
	template_name = 'media/video/mediavideo_detail.html'
	context_object_name = 'asset'

class MediaVideoUpdateView(LoginRequiredMixin, UpdateView):
	model = MediaVideo
	template_name = 'media/video/mediavideo_form.html'
	context_object_name = 'asset'
	fields = ['is_public', 'original_published_date', 'title', 'short_description', 'long_description', 'notes', 'transcription', 'tags', 'genre', 'service', 'service_source', 'location_city', 'location_state', 'location_country']
	def get_form(self):
		form = super().get_form()
		form.fields['original_published_date'].widget = DatePickerInput()
		return form

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
	queryset = MediaVideo.objects.all().filter(is_public=True)
	serializer_class = MediaVideoSerializerDetail

class MediaVideoGalleryListView(LoginRequiredMixin, ListView):
	model = MediaVideo
	template_name = 'media/video/mediavideo_gallery.html'
	context_object_name = 'assets'
	ordering = ['-created']
	paginate_by = 24


class MediaVideoRSSFeed(Feed):
	title = "Video Feed"
	link = "/videos/rss/"
	description = "Latest videos"
	feed_copyright = "SGC-MEDIA-2024"
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

class MediaVideoServiceCreateView(LoginRequiredMixin, CreateView):
	model = MediaVideoService
	template_name = 'media/video/mediavideoservice_create.html'
	fields = ['service_source']

class MediaVideoServiceListView(LoginRequiredMixin, ListView):
	model = MediaVideoService
	template_name = 'media/video/mediavideoservice_list.html'
	context_object_name = 'assets'
	ordering = ['service_source']
	paginate_by = 15

class MediaVideoServiceDetailView(LoginRequiredMixin, DetailView):
	model = MediaVideoService
	template_name = 'media/video/mediavideoservice_detail.html'
	context_object_name = 'asset'

class MediaVideoServiceUpdateView(LoginRequiredMixin, UpdateView):
	model = MediaVideoService
	template_name = 'media/video/mediavideoservice_form.html'
	context_object_name = 'asset'
	fields = ['service_source']

class MediaVideoServiceListAPI(generics.ListAPIView):
	queryset = MediaVideoService.objects.all()
	serializer_class = MediaVideoServiceSerializerList
	filter_backends = [DjangoFilterBackend]
	filterset_fields = ['service_source']
	ordering_fields = ['id', 'service_source']
	ordering = ['-id']

class MediaVideoServiceListAPISearch(generics.ListAPIView):
	queryset = MediaVideoService.objects.all()
	serializer_class = MediaVideoServiceSerializerList
	filter_backends = [filters.SearchFilter]
	search_fields = ['service_source'] 
	ordering_fields = ['id', 'service_source']
	ordering = ['service_source']

class MediaVideoServiceDetailAPI(generics.RetrieveAPIView):
	queryset = MediaVideoService.objects.all()
	serializer_class = MediaVideoServiceSerializerDetail


### Audio
class MediaAudioListView(LoginRequiredMixin, ListView):
	model = MediaAudio
	template_name = 'media/audio/audio_list.html'
	context_object_name = 'assets'
	ordering = ['-created']
	paginate_by = 15

class MediaAudioDetailView(LoginRequiredMixin, DetailView):
	model = MediaAudio
	template_name = 'media/audio/mediaaudio_detail.html'
	context_object_name = 'asset'

class MediaAudioUpdateView(LoginRequiredMixin, UpdateView):
	model = MediaAudio
	context_object_name = 'asset'
	template_name = 'media/audio/mediaaudio_form.html'
	fields = ['is_public', 'original_published_date', 'rating', 'title', 'artist', 'album', 'genre', 'short_description', 'long_description', 'source', 'notes', 'transcription']
	def get_form(self):
		form = super().get_form()
		form.fields['original_published_date'].widget = DatePickerInput()
		return form

# class MediaAudioDeleteView(LoginRequiredMixin, DeleteView):
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

class MediaAudioGalleryListView(LoginRequiredMixin, ListView):
	model = MediaAudio
	template_name = 'media/audio/mediaaudio_gallery.html'
	context_object_name = 'assets'
	ordering = ['-created']
	paginate_by = 24

class MediaAudioServiceCreateView(LoginRequiredMixin, CreateView):
	model = MediaAudioService
	template_name = 'media/audio/mediaaudioservice_create.html'
	fields = ['service_source']

class MediaAudioServiceListView(LoginRequiredMixin, ListView):
	model = MediaAudioService
	template_name = 'media/audio/mediaaudioservice_list.html'
	context_object_name = 'assets'
	ordering = ['service_source']
	paginate_by = 15

class MediaAudioServiceDetailView(LoginRequiredMixin, DetailView):
	model = MediaAudioService
	template_name = 'media/audio/mediaaudioservice_detail.html'
	context_object_name = 'asset'

class MediaAudioServiceUpdateView(LoginRequiredMixin, UpdateView):
	model = MediaAudioService
	template_name = 'media/audio/mediaaudioservice_form.html'
	context_object_name = 'asset'
	fields = ['service_source']

class MediaAudioServiceListAPI(generics.ListAPIView):
	queryset = MediaAudioService.objects.all()
	serializer_class = MediaAudioServiceSerializerList
	filter_backends = [DjangoFilterBackend]
	filterset_fields = ['service_source']
	ordering_fields = ['id', 'service_source']
	ordering = ['-id']

class MediaAudioServiceListAPISearch(generics.ListAPIView):
	queryset = MediaAudioService.objects.all()
	serializer_class = MediaAudioServiceSerializerList
	filter_backends = [filters.SearchFilter]
	search_fields = ['service_source'] 
	ordering_fields = ['id', 'service_source']
	ordering = ['service_source']

class MediaAudioServiceDetailAPI(generics.RetrieveAPIView):
	queryset = MediaAudioService.objects.all()
	serializer_class = MediaAudioServiceSerializerDetail


### Photo
class MediaPhotoListView(LoginRequiredMixin, ListView):
	model = MediaPhoto
	template_name = 'media/photo/photo_list.html'
	context_object_name = 'assets'
	ordering = ['-created']
	paginate_by = 15

class MediaPhotoDetailView(LoginRequiredMixin, DetailView):
	model = MediaPhoto
	template_name = 'media/photo/mediaphoto_detail.html'
	context_object_name = 'asset'

class MediaPhotoUpdateView(LoginRequiredMixin, UpdateView):
	model = MediaPhoto
	template_name = 'media/photo/mediaphoto_form.html'
	context_object_name = 'asset'
	fields = ['is_public', 'original_published_date', 'title', 'short_description', 'long_description', 'notes', 'service', 'tags', 'location_name', 'location_city', 'location_state', 'location_country']
	def get_form(self):
		form = super().get_form()
		form.fields['original_published_date'].widget = DatePickerInput()
		return form

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

class MediaPhotoGalleryListView(LoginRequiredMixin, ListView):
	model = MediaPhoto
	template_name = 'media/photo/mediaphoto_gallery.html'
	context_object_name = 'assets'
	ordering = ['-created']
	paginate_by = 24

class MediaPhotoServiceCreateView(LoginRequiredMixin, CreateView):
	model = MediaPhotoService
	template_name = 'media/photo/mediaphotoservice_create.html'
	fields = ['service_source']

class MediaPhotoServiceListView(LoginRequiredMixin, ListView):
	model = MediaPhotoService
	template_name = 'media/photo/mediaphotoservice_list.html'
	context_object_name = 'assets'
	ordering = ['service_source']
	paginate_by = 15

class MediaPhotoServiceDetailView(LoginRequiredMixin, DetailView):
	model = MediaPhotoService
	template_name = 'media/photo/mediaphotoservice_detail.html'
	context_object_name = 'asset'

class MediaPhotoServiceUpdateView(LoginRequiredMixin, UpdateView):
	model = MediaPhotoService
	template_name = 'media/photo/mediaphotoservice_form.html'
	context_object_name = 'asset'
	fields = ['service_source']

class MediaPhotoServiceListAPI(generics.ListAPIView):
	queryset = MediaPhotoService.objects.all()
	serializer_class = MediaPhotoServiceSerializerList
	filter_backends = [DjangoFilterBackend]
	filterset_fields = ['service_source']
	ordering_fields = ['id', 'service_source']
	ordering = ['-id']

class MediaPhotoServiceListAPISearch(generics.ListAPIView):
	queryset = MediaPhotoService.objects.all()
	serializer_class = MediaPhotoServiceSerializerList
	filter_backends = [filters.SearchFilter]
	search_fields = ['service_source'] 
	ordering_fields = ['id', 'service_source']
	ordering = ['service_source']

class MediaPhotoServiceDetailAPI(generics.RetrieveAPIView):
	queryset = MediaPhotoService.objects.all()
	serializer_class = MediaPhotoServiceSerializerDetail


### Documents
class MediaDocListView(LoginRequiredMixin, ListView):
	model = MediaDoc
	template_name = 'media/doc/doc_list.html'
	context_object_name = 'assets'
	ordering = ['-created']
	paginate_by = 15

class MediaDocDetailView(LoginRequiredMixin, DetailView):
	model = MediaDoc
	template_name = 'media/doc/mediadoc_detail.html'
	context_object_name = 'asset'

class MediaDocUpdateView(LoginRequiredMixin, UpdateView):
	model = MediaDoc
	template_name = 'media/doc/mediadoc_form.html'
	context_object_name = 'asset'
	fields = ['is_public', 'original_published_date', 'title', 'short_description', \
		'long_description', 'abstract', 'notes', 'affiliations', 'authors', 'publication', 'service', \
		'source_url', 'doi_url', 'category', 'keywords', 'tags']
	def get_form(self):
		form = super().get_form()
		form.fields['original_published_date'].widget = DatePickerInput()
		return form

class MediaDocListAPI(generics.ListAPIView):
	queryset = MediaDoc.objects.all().filter(is_public=True)
	serializer_class = MediaDocSerializerList
	filter_backends = [DjangoFilterBackend]
	filterset_fields = ['service', 'keywords', 'doc_format']
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

class MediaDocServiceCreateView(LoginRequiredMixin, CreateView):
	model = MediaDocService
	template_name = 'media/doc/mediadocservice_create.html'
	fields = ['service_source']

class MediaDocServiceListView(LoginRequiredMixin, ListView):
	model = MediaDocService
	template_name = 'media/doc/mediadocservice_list.html'
	context_object_name = 'assets'
	ordering = ['service_source']
	paginate_by = 15

class MediaDocServiceDetailView(LoginRequiredMixin, DetailView):
	model = MediaDocService
	template_name = 'media/doc/mediadocservice_detail.html'
	context_object_name = 'asset'

class MediaDocServiceUpdateView(LoginRequiredMixin, UpdateView):
	model = MediaDocService
	template_name = 'media/doc/mediadocservice_form.html'
	context_object_name = 'asset'
	fields = ['service_source']

class MediaDocServiceListAPI(generics.ListAPIView):
	queryset = MediaDocService.objects.all()
	serializer_class = MediaDocServiceSerializerList
	filter_backends = [DjangoFilterBackend]
	filterset_fields = ['service_source']
	ordering_fields = ['id', 'service_source']
	ordering = ['-id']

class MediaDocServiceListAPISearch(generics.ListAPIView):
	queryset = MediaDocService.objects.all()
	serializer_class = MediaDocServiceSerializerList
	filter_backends = [filters.SearchFilter]
	search_fields = ['service_source'] 
	ordering_fields = ['id', 'service_source']
	ordering = ['service_source']

class MediaDocServiceDetailAPI(generics.RetrieveAPIView):
	queryset = MediaDocService.objects.all()
	serializer_class = MediaDocServiceSerializerDetail


### Tags
class MediaTagListView(LoginRequiredMixin, ListView):
	model = MediaTag
	template_name = 'media/tag/tag_list.html'
	context_object_name = 'assets'
	ordering = ['tag_name']
	paginate_by = 20

class MediaTagDetailView(LoginRequiredMixin, DetailView):
	model = MediaTag
	template_name = 'media/tag/mediatag_detail.html'
	context_object_name = 'asset'

class MediaTagUpdateView(LoginRequiredMixin, UpdateView):
	model = MediaTag
	template_name = 'media/tag/mediatag_form.html'
	context_object_name = 'asset'
	fields = ['tag_name']

class MediaTagListAPI(generics.ListAPIView):
	queryset = MediaTag.objects.all()
	serializer_class = MediaTagSerializerList
	filter_backends = [DjangoFilterBackend]
	filterset_fields = ['tag_name']
	ordering_fields = ['id', 'tag_name']
	ordering = ['tag_name']

class MediaTagListAPISearch(generics.ListAPIView):
	queryset = MediaTag.objects.all()
	serializer_class = MediaTagSerializerList
	filter_backends = [filters.SearchFilter]
	search_fields = ['tag_name'] 
	ordering_fields = ['id', 'tag_name']
	ordering = ['tag_name']
