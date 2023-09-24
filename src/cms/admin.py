from django.contrib import admin
from .models import PlaylistVideo, PlaylistAudio, PlaylistPhoto
from .models import PlaylistVideoItems, PlaylistAudioItems, PlaylistPhotoItems

### Video

class PlaylistVideoAdmin(admin.ModelAdmin):
	list_display = ['file_name', 'size', 'media_video_format', 'service', 'created']
	search_fields = ['file_name', 'media_video_format']
	list_filter = ['media_video_format', 'service', 'is_public']
	readonly_fields = ['size', 'sha256', 'file_uuid', 'created']
	class Meta:
		model = PlaylistVideo

class PlaylistAudioAdmin(admin.ModelAdmin):
	list_display = ['file_name', 'size', 'service', 'created']
	search_fields = ['file_name']
	list_filter = ['service', 'is_public']
	readonly_fields = ['size', 'sha256', 'file_uuid', 'created']
	class Meta:
		model = PlaylistAudio

class PlaylistPhotoAdmin(admin.ModelAdmin):
	list_display = ['file_name', 'size', 'media_photo_format', 'service', 'created']
	search_fields = ['file_name', 'media_photo_format', 'service']
	list_filter = ['media_photo_format', 'service', 'is_public']
	readonly_fields = ['size', 'sha256', 'file_uuid', 'created']
	class Meta:
		model = PlaylistPhoto
