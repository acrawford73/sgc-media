from django.contrib import admin
from .models import MediaVideo, MediaVideoGenre, MediaVideoFormat, MediaVideoService, MediaVideoThumbnail
from .models import MediaAudio, MediaAudioGenre, MediaAudioFormat, MediaAudioService
from .models import MediaPhoto, MediaPhotoFormat, MediaPhotoService
from .models import MediaDoc, MediaDocFormat, MediaDocType, MediaDocService
from .models import MediaCountry, MediaTag, MediaCategory
					

# Video
class MediaVideoAdmin(admin.ModelAdmin):
	list_display = ['file_name', 'size', 'media_video_format', 'service', 'created']
	search_fields = ['file_name', 'media_video_format']
	list_filter = ['media_video_format', 'service', 'is_public']
	readonly_fields = ['size', 'path_sha256', 'file_sha256', 'file_uuid', 'created', 'media_video_duration', \
	'media_video_width', 'media_video_height', 'media_video_format', 'media_video_frame_rate', \
	'media_video_codec', 'media_audio_codec', 'media_audio_channels', 'media_audio_sample_rate', \
	'doc_format', 'media_video_bitrate', 'media_audio_bitrate']
	class Meta:
		model = MediaVideo

class MediaVideoGenreAdmin(admin.ModelAdmin):
	list_display = ['genre']
	class Meta:
		model = MediaVideoGenre

class MediaVideoFormatAdmin(admin.ModelAdmin):
	list_display = ['doc_format', 'doc_format_name']
	search_fields = ['doc_format', 'doc_format_name']
	class Meta:
		model = MediaVideoFormat

class MediaVideoServiceAdmin(admin.ModelAdmin):
	list_display = ['service_source']
	search_fields = ['service_source']
	class Meta:
		model = MediaVideoService


# Audio
class MediaAudioAdmin(admin.ModelAdmin):
	list_display = ['file_name', 'size', 'artist', 'album', 'created']
	search_fields = ['file_name', 'artist', 'album', 'genre', 'year']
	list_filter = ['genre', 'year', 'service', 'is_public']
	readonly_fields = ['size', 'path_sha256', 'file_sha256', 'file_uuid', 'created', 'doc_format', 'image']
	class Meta:
		model = MediaAudio

class MediaAudioGenreAdmin(admin.ModelAdmin):
	list_display = ['genre']
	class Meta:
		model = MediaAudioGenre

class MediaAudioFormatAdmin(admin.ModelAdmin):
	list_display = ['doc_format', 'doc_format_name']
	search_fields = ['doc_format', 'doc_format_name']
	class Meta:
		model = MediaAudioFormat


# Photo
class MediaPhotoAdmin(admin.ModelAdmin):
	list_display = ['file_name', 'size', 'orientation', 'service', 'created']
	search_fields = ['file_name']
	list_filter = ['orientation', 'service', 'is_public']
	readonly_fields = ['size', 'path_sha256', 'file_sha256', 'file_uuid', 'created', 'doc_format', 'height', 'width', 'photo_format', 'orientation']
	class Meta:
		model = MediaPhoto

class MediaPhotoFormatAdmin(admin.ModelAdmin):
	list_display = ['doc_format', 'doc_format_name']
	search_fields = ['doc_format', 'doc_format_name']
	class Meta:
		model = MediaPhotoFormat


# Documents
class MediaDocAdmin(admin.ModelAdmin):
	list_display = ['file_name', 'title', 'doc_format', 'size', 'created']
	search_fields = ['file_name', 'title', 'authors', 'publication', 'service', 'keywords']
	list_filter = ['doc_format_id', 'is_public']
	readonly_fields = ['size', 'path_sha256', 'file_sha256', 'file_uuid', 'created', 'doc_format']
	class Meta:
		model = MediaDoc

class MediaDocFormatAdmin(admin.ModelAdmin):
	list_display = ['doc_format', 'doc_format_name']
	search_fields = ['doc_format', 'doc_format_name']
	class Meta:
		model = MediaDocFormat

class MediaDocTypeAdmin(admin.ModelAdmin):
	list_display = ['document_type']
	search_fields = ['document_type']
	class Meta:
		model = MediaDocType

class MediaCountryAdmin(admin.ModelAdmin):
	list_display = ['country_name', 'country_code']
	search_fields = ['country_name', 'country_code']
	class Meta:
		model = MediaCountry

class MediaTagAdmin(admin.ModelAdmin):
	list_display = ['tag_name']
	search_fields = ['tag_name']
	class Meta:
		model = MediaTag

class MediaCategoryAdmin(admin.ModelAdmin):
	list_display = ['category']
	search_fields = ['category']
	class Meta:
		model = MediaCategory

# Services
class MediaVideoServiceAdmin(admin.ModelAdmin):
	list_display = ['service_source']
	search_fields = ['service_source']
	class Meta:
		model = MediaVideoService

class MediaAudioServiceAdmin(admin.ModelAdmin):
	list_display = ['service_source']
	search_fields = ['service_source']
	class Meta:
		model = MediaAudioService

class MediaPhotoServiceAdmin(admin.ModelAdmin):
	list_display = ['service_source']
	search_fields = ['service_source']
	class Meta:
		model = MediaPhotoService

class MediaDocServiceAdmin(admin.ModelAdmin):
	list_display = ['service_source', 'service_description', 'service_url']
	search_fields = ['service_source']
	class Meta:
		model = MediaDocService


# Register models
admin.site.register(MediaVideo, MediaVideoAdmin)
admin.site.register(MediaVideoFormat, MediaVideoFormatAdmin)
admin.site.register(MediaVideoService, MediaVideoServiceAdmin)
admin.site.register(MediaVideoGenre, MediaVideoGenreAdmin)

admin.site.register(MediaAudio, MediaAudioAdmin)
admin.site.register(MediaAudioGenre, MediaAudioGenreAdmin)
admin.site.register(MediaAudioFormat, MediaAudioFormatAdmin)
admin.site.register(MediaAudioService, MediaAudioServiceAdmin)

admin.site.register(MediaPhoto, MediaPhotoAdmin)
admin.site.register(MediaPhotoFormat, MediaPhotoFormatAdmin)
admin.site.register(MediaPhotoService, MediaPhotoServiceAdmin)

admin.site.register(MediaDoc, MediaDocAdmin)
admin.site.register(MediaDocFormat, MediaDocFormatAdmin)
admin.site.register(MediaDocService, MediaDocServiceAdmin)
admin.site.register(MediaDocType, MediaDocTypeAdmin)

admin.site.register(MediaCountry, MediaCountryAdmin)
admin.site.register(MediaTag, MediaTagAdmin)
admin.site.register(MediaCategory, MediaCategoryAdmin)