from rest_framework import serializers
from .models import MediaVideo, MediaAudio, MediaPhoto


# Video
class MediaVideoSerializerList(serializers.ModelSerializer):
	categories = serializers.JSONField(source='tags')
	description = serializers.CharField(source='short_description')
	width = serializers.IntegerField(source='media_video_width')
	height = serializers.IntegerField(source='media_video_height')
	duration = serializers.DecimalField(source='media_video_duration',max_digits=8, decimal_places=3)
	class Meta:
		model = MediaVideo
		fields = ['id', 'username', 'title', 'description', 'service', 'orientation', 'width', 'height', 'media_path', 'sha256', 'created', 'duration', 'size', 'categories']

class MediaVideoSerializerDetail(serializers.ModelSerializer):
	class Meta:
		model = MediaVideo
		fields = '__all__'


# Audio
class MediaAudioSerializerList(serializers.ModelSerializer):
	categories = serializers.JSONField(source='tags')
	class Meta:
		model = MediaAudio
		fields = ['id', 'title', 'artist', 'album', 'genre', 'media_path', 'sha256', 'created', 'size', 'categories']

class MediaAudioSerializerDetail(serializers.ModelSerializer):
	class Meta:
		model = MediaAudio
		fields = '__all__'


# Photo
class MediaPhotoSerializerList(serializers.ModelSerializer):
	categories = serializers.JSONField(source='tags')
	description = serializers.CharField(source='short_description')
	format = serializers.CharField(source='photo_format')
	class Meta:
		model = MediaPhoto
		fields = ['id', 'username', 'title', 'description', 'service', 'orientation', 'format', 'width', 'height', 'media_path', 'sha256', 'created', 'size', 'categories']

class MediaPhotoSerializerDetail(serializers.ModelSerializer):
	class Meta:
		model = MediaPhoto
		fields = '__all__'

