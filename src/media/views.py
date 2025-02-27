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
from .models import MediaCountry, MediaTag, MediaCategory

from rest_framework import generics
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
#from url_filter.filtersets import ModelFilterSet


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
	fields = ['title', 'short_description', 'long_description', 'orientation', 'service', 'file_path', \
		'notes', 'category']

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
	fields = ['is_public', 'original_published_date', 'title', 'short_description', 'long_description', \
		'notes', 'transcription', 'tags', 'category', 'genre', 'service', 'service_source', 'location_city', \
		'location_state', 'location_country']
	def get_form(self):
		form = super().get_form()
		form.fields['original_published_date'].widget = DatePickerInput()
		return form

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

### Audio
class MediaAudioCreateView(LoginRequiredMixin, CreateView):
	model = MediaAudio
	context_object_name = 'asset'
	template_name = 'media/audio/mediaaudio_form.html'
	fields = ['is_public', 'original_published_date', 'rating', 'title', 'artist', 'album', 'genre', \
		'composer', 'short_description', 'long_description', 'source', 'notes', 'transcription', 'category']
	def get_form(self):
		form = super().get_form()
		form.fields['original_published_date'].widget = DatePickerInput()
		return form

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
	fields = ['is_public', 'original_published_date', 'rating', 'title', 'artist', 'album', 'genre', \
		'composer', 'short_description', 'long_description', 'source', 'notes', 'transcription', 'category']
	def get_form(self):
		form = super().get_form()
		form.fields['original_published_date'].widget = DatePickerInput()
		return form

# class MediaAudioDeleteView(LoginRequiredMixin, DeleteView):
# 	model = MediaAudio
# 	template_name = 'media/mediaaudio_confirm_delete.html'
# 	context_object_name = 'asset'
# 	success_url = reverse_lazy('media-audio-list')

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

class MediaAudioRSSFeed(Feed):
	title = "Audio Feed"
	link = "/audio/rss/"
	description = "Latest audio files"
	feed_copyright = "SGC-MEDIA-2024"
	ttl = 600
	def items(self):
		return MediaAudio.objects.filter(is_public=True).order_by("-created")[:50]
	def item_title(self, item):
		return item.title
	def item_description(self, item):
		if (item.long_description is None) or (item.long_description == ""):
			item.long_description = "Long description is not available"
		return item.long_description
	def item_link(self, item):
		return "/videos/%s/" % (item.id)
	def item_author_name(self, item):
		if (item.artist is None) or (item.artist == ""):
			return "Unknown"
		else:
			return item.artist
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

class MediaAudioAtomFeed(MediaAudioRSSFeed):
	feed_type = Atom1Feed
	subtitle = MediaAudioRSSFeed.description


### Photo
class MediaPhotoCreateView(LoginRequiredMixin, CreateView):
	model = MediaPhoto
	template_name = 'media/photo/mediaphoto_form.html'
	context_object_name = 'asset'
	fields = ['is_public', 'original_published_date', 'title', 'short_description', 'long_description', \
		'notes', 'service', 'service_source', 'category', 'tags', 'location_name', 'location_city', \
		'location_state', 'location_country']
	def get_form(self):
		form = super().get_form()
		form.fields['original_published_date'].widget = DatePickerInput()
		return form

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
	fields = ['is_public', 'original_published_date', 'title', 'short_description', 'long_description', \
		'notes', 'service', 'service_source', 'category', 'tags', 'location_name', 'location_city', \
		'location_state', 'location_country']
	def get_form(self):
		form = super().get_form()
		form.fields['original_published_date'].widget = DatePickerInput()
		return form

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

class MediaPhotoRSSFeed(Feed):
	title = "Photo Feed"
	link = "/photos/rss/"
	description = "Latest photos"
	feed_copyright = "SGC-MEDIA-2024"
	ttl = 600
	def items(self):
		return MediaPhoto.objects.filter(is_public=True).order_by("-created")[:50]
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

class MediaPhotoAtomFeed(MediaPhotoRSSFeed):
	feed_type = Atom1Feed
	subtitle = MediaPhotoRSSFeed.description


### Documents

class MediaDocCreateView(LoginRequiredMixin, CreateView):
	model = MediaDoc
	template_name = 'media/doc/mediadoc_form.html'
	context_object_name = 'asset'
	fields = ['is_public', 'original_published_date', 'title', 'short_description', \
		'long_description', 'abstract', 'notes', 'affiliations', 'authors', 'publication', 'service', \
		'source_url', 'doi_url', 'category', 'keywords', 'document_type', 'tags']
	def get_form(self):
		form = super().get_form()
		form.fields['original_published_date'].widget = DatePickerInput()
		return form

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
		'source_url', 'doi_url', 'category', 'keywords', 'document_type', 'tags']
	def get_form(self):
		form = super().get_form()
		form.fields['original_published_date'].widget = DatePickerInput()
		return form

class MediaDocServiceCreateView(LoginRequiredMixin, CreateView):
	model = MediaDocService
	template_name = 'media/doc/mediadocservice_create.html'
	fields = ['service_source', 'service_description', 'service_url']

class MediaDocServiceListView(LoginRequiredMixin, ListView):
	model = MediaDocService
	template_name = 'media/doc/mediadocservice_list.html'
	context_object_name = 'assets'
	ordering = ['service_source']
	#paginate_by = 15

class MediaDocServiceDetailView(LoginRequiredMixin, DetailView):
	model = MediaDocService
	template_name = 'media/doc/mediadocservice_detail.html'
	context_object_name = 'asset'

class MediaDocServiceUpdateView(LoginRequiredMixin, UpdateView):
	model = MediaDocService
	template_name = 'media/doc/mediadocservice_form.html'
	context_object_name = 'asset'
	fields = ['service_source', 'service_description', 'service_url']

class MediaDocRSSFeed(Feed):
	title = "Document Feed"
	link = "/docs/rss/"
	description = "Latest documents"
	feed_copyright = "SGC-MEDIA-2024"
	ttl = 600
	def items(self):
		return MediaDoc.objects.filter(is_public=True).order_by("-created")[:50]
	def item_title(self, item):
		return item.title
	def item_description(self, item):
		if (item.long_description is None) or (item.long_description == ""):
			item.long_description = "Long description is not available"
		return item.long_description
	def item_link(self, item):
		return "/docs/%s/" % (item.id)
	def item_author_name(self, item):
		if (item.authors is None) or (item.authors == ""):
			return "Unknown"
		else:
			return item.authors
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

class MediaDocAtomFeed(MediaDocRSSFeed):
	feed_type = Atom1Feed
	subtitle = MediaDocRSSFeed.description


### Tags
class MediaTagCreateView(LoginRequiredMixin, CreateView):
	model = MediaTag
	template_name = 'media/tag/tag_create.html'
	fields = ['tag_name']

class MediaTagListView(LoginRequiredMixin, ListView):
	model = MediaTag
	template_name = 'media/tag/tag_list.html'
	context_object_name = 'assets'
	ordering = ['tag_name']
	#paginate_by = 20

class MediaTagDetailView(LoginRequiredMixin, DetailView):
	model = MediaTag
	template_name = 'media/tag/mediatag_detail.html'
	context_object_name = 'asset'

class MediaTagUpdateView(LoginRequiredMixin, UpdateView):
	model = MediaTag
	template_name = 'media/tag/mediatag_form.html'
	context_object_name = 'asset'
	fields = ['tag_name']


### Categories

class MediaCategoryCreateView(LoginRequiredMixin, CreateView):
	model = MediaCategory
	template_name = 'media/category/category_create.html'
	fields = ['category']

class MediaCategoryListView(LoginRequiredMixin, ListView):
	model = MediaCategory
	template_name = 'media/category/category_list.html'
	context_object_name = 'assets'
	ordering = ['category']
	#paginate_by = 15

class MediaCategoryDetailView(LoginRequiredMixin, DetailView):
	model = MediaCategory
	template_name = 'media/category/category_detail.html'
	context_object_name = 'asset'

class MediaCategoryUpdateView(LoginRequiredMixin, UpdateView):
	model = MediaCategory
	template_name = 'media/category/category_form.html'
	context_object_name = 'asset'
	fields = ['category']
