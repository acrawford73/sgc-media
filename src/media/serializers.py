from rest_framework import serializers
from .models import MediaVideo, MediaAudio, MediaPhoto, MediaDoc, MediaVideoGenre


# Video
class MediaVideoSerializerList(serializers.ModelSerializer):
	id = serializers.CharField(source="file_uuid")
	categories = serializers.JSONField(source='tags')
	description = serializers.CharField(source='short_description')
	width = serializers.IntegerField(source='media_video_width')
	height = serializers.IntegerField(source='media_video_height')
	duration = serializers.DecimalField(source='media_video_duration',max_digits=8, decimal_places=3)
	class Meta:
		model = MediaVideo
		fields = ['id', 'username', 'title', 'description', 'service', 'orientation', 'width', 'height', 'media_path', 'sha256', 'created', 'duration', 'size', 'categories']

class MediaVideoGenreSerializerList(serializers.ModelSerializer):
	class Meta:
		model = MediaVideoGenre
		fields = ['id', 'genre']

class MediaVideoSerializerDetail(serializers.ModelSerializer):
	class Meta:
		model = MediaVideo
		fields = '__all__'


# Audio
class MediaAudioSerializerListArtists(serializers.ModelSerializer):
	class Meta:
		model = MediaAudio
		fields = ['id', 'artist']

class MediaAudioSerializerListAlbums(serializers.ModelSerializer):
	class Meta:
		model = MediaAudio
		fields = ['id', 'album', 'artist']

class MediaAudioSerializerList(serializers.ModelSerializer):
	id = serializers.CharField(source="file_uuid")
	description = serializers.CharField(source='short_description')
	bitrate = serializers.CharField(source='audio_bitrate')
	class Meta:
		model = MediaAudio
		fields = ['id', 'title', 'artist', 'album', 'album_artist', 'composer', 'genre', 'description', 'duration', 'bitrate', 'media_path', 'sha256', 'created', 'size']

class MediaAudioSerializerDetail(serializers.ModelSerializer):
	class Meta:
		model = MediaAudio
		fields = '__all__'


# Photo
class MediaPhotoSerializerList(serializers.ModelSerializer):
	id = serializers.CharField(source="file_uuid")
	categories = serializers.JSONField(source='tags')
	description = serializers.CharField(source='short_description')
	class Meta:
		model = MediaPhoto
		fields = ['id', 'username', 'title', 'description', 'service', 'orientation', 'photo_format', 'width', 'height', 'media_path', 'sha256', 'created', 'size', 'categories']

class MediaPhotoSerializerDetail(serializers.ModelSerializer):
	class Meta:
		model = MediaPhoto
		fields = '__all__'


# Documents
class MediaDocSerializerList(serializers.ModelSerializer):
	id = serializers.CharField(source="file_uuid")
	description = serializers.CharField(source='short_description')
	class Meta:
		model = MediaDoc
		fields = ['id', 'title', 'description', 'media_path', 'sha256', 'created', 'size', 'keywords']

class MediaDocSerializerDetail(serializers.ModelSerializer):
	class Meta:
		model = MediaDoc
		fields = '__all__'