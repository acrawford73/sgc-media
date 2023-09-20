from django.contrib import admin
from .models import MediaVideo, MediaVideoGenre, MediaVideoFormat, MediaVideoService, \
					MediaAudio, MediaAudioGenre, MediaAudioFormat, \
					MediaPhoto, MediaPhotoFormat, \
					MediaDoc, MediaDocFormat, MediaService


# Video
class MediaVideoAdmin(admin.ModelAdmin):
	list_display = ['file_name', 'size', 'media_video_format', 'service', 'created', 'updated']
	search_fields = ['file_name', 'media_video_format']
	list_filter = ['media_video_format', 'service', 'is_public']
	readonly_fields = ['size', 'sha256', 'file_uuid', 'created', 'updated', 'media_video_duration', \
	'media_video_width', 'media_video_height', 'media_video_format', 'media_video_frame_rate', \
	'media_video_codec', 'media_audio_codec', 'media_audio_channels', 'media_audio_sample_rate', 'doc_format']
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
	list_display = ['service_name']
	search_fields = ['service_name']
	class Meta:
		model = MediaVideoService


# Audio
class MediaAudioAdmin(admin.ModelAdmin):
	list_display = ['file_name', 'size', 'artist', 'album', 'created', 'updated']
	search_fields = ['file_name', 'artist', 'album', 'genre', 'year']
	list_filter = ['genre', 'year', 'service', 'is_public']
	readonly_fields = ['size', 'sha256', 'file_uuid', 'created', 'updated', 'doc_format']
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
	list_display = ['file_name', 'size', 'orientation', 'service', 'created', 'updated']
	search_fields = ['file_name']
	list_filter = ['orientation', 'service', 'is_public']
	readonly_fields = ['size', 'sha256', 'file_uuid', 'created', 'updated', 'doc_format']
	class Meta:
		model = MediaPhoto

class MediaPhotoFormatAdmin(admin.ModelAdmin):
	list_display = ['doc_format', 'doc_format_name']
	search_fields = ['doc_format', 'doc_format_name']
	class Meta:
		model = MediaPhotoFormat


# Documents
class MediaDocAdmin(admin.ModelAdmin):
	list_display = ['file_name', 'title', 'doc_format', 'size', 'created', 'updated']
	search_fields = ['file_name', 'title']
	list_filter = ['doc_format_id', 'is_public']
	readonly_fields = ['size', 'sha256', 'file_uuid', 'created', 'updated', 'doc_format']
	class Meta:
		model = MediaDoc

class MediaDocFormatAdmin(admin.ModelAdmin):
	list_display = ['doc_format', 'doc_format_name']
	search_fields = ['doc_format', 'doc_format_name']
	class Meta:
		model = MediaDocFormat


# Services
class MediaServiceAdmin(admin.ModelAdmin):
	list_display = ['service', 'media_type']
	class Meta:
		model = MediaService


# Register models
admin.site.register(MediaVideo, MediaVideoAdmin)
admin.site.register(MediaVideoFormat, MediaVideoFormatAdmin)
admin.site.register(MediaVideoService, MediaVideoServiceAdmin)
admin.site.register(MediaVideoGenre, MediaVideoGenreAdmin)

admin.site.register(MediaAudioFormat, MediaAudioFormatAdmin)
admin.site.register(MediaAudio, MediaAudioAdmin)
admin.site.register(MediaAudioGenre, MediaAudioGenreAdmin)

admin.site.register(MediaPhoto, MediaPhotoAdmin)
admin.site.register(MediaPhotoFormat, MediaPhotoFormatAdmin)

admin.site.register(MediaDoc, MediaDocAdmin)
admin.site.register(MediaDocFormat, MediaDocFormatAdmin)



admin.site.register(MediaService, MediaServiceAdmin)
