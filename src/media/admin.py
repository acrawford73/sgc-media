from django.contrib import admin
from .models import MediaVideo, MediaAudio, MediaPhoto, MediaDoc, AudioGenre, MediaService

class MediaVideoAdmin(admin.ModelAdmin):
	list_display = ['file_name', 'size', 'media_video_format', 'created']
	search_fields = ['file_name', 'media_video_format']
	list_filter = ['media_video_format', 'service', 'is_public']
	readonly_fields = ['size', 'sha256', 'file_uuid', 'created', 'media_video_duration', 'media_video_width', 'media_video_height', 'media_video_format', 'media_video_frame_rate', 'media_video_codec', 'media_audio_codec', 'media_audio_channels', 'media_audio_sample_rate']
	class Meta:
		model = MediaVideo

class MediaAudioAdmin(admin.ModelAdmin):
	list_display = ['file_name', 'size', 'artist', 'album', 'created']
	search_fields = ['file_name', 'artist', 'album', 'genre', 'year']
	list_filter = ['genre', 'year', 'service', 'is_public']
	readonly_fields = ['size', 'sha256', 'file_uuid', 'created']
	class Meta:
		model = MediaAudio

class MediaPhotoAdmin(admin.ModelAdmin):
	list_display = ['file_name', 'size', 'orientation', 'created']
	search_fields = ['file_name']
	list_filter = ['orientation', 'service', 'is_public']
	readonly_fields = ['size', 'sha256', 'file_uuid', 'created']
	class Meta:
		model = MediaPhoto

class MediaDocAdmin(admin.ModelAdmin):
	list_display = ['file_name', 'size', 'title', 'created']
	search_fields = ['file_name', 'title']
	list_filter = ['doc_format', 'is_public']
	readonly_fields = ['size', 'sha256', 'file_uuid', 'created']
	class Meta:
		model = MediaDoc

class AudioGenreAdmin(admin.ModelAdmin):
	list_display = ['genre']
	class Meta:
		model = AudioGenre

class MediaServiceAdmin(admin.ModelAdmin):
	list_display = ['service']
	class Meta:
		model = MediaService


admin.site.register(MediaVideo, MediaVideoAdmin)
admin.site.register(MediaAudio, MediaAudioAdmin)
admin.site.register(MediaPhoto, MediaPhotoAdmin)

admin.site.register(AudioGenre, AudioGenreAdmin)
admin.site.register(MediaService, MediaServiceAdmin)
