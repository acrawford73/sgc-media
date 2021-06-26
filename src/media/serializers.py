from rest_framework import serializers
from .models import MediaVideo, MediaAudio, MediaPhoto


# Video
class MediaVideoSerializerList(serializers.ModelSerializer):
	categories = serializers.JSONField(source='tags')
	description = serializers.CharField(source='short_description')
	class Meta:
		model = MediaVideo
		fields = ['id', 'username', 'title', 'description', 'service', 'orientation', 'media_path', 'sha256', 'created', 'size', 'categories']

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
	class Meta:
		model = MediaPhoto
		fields = ['id', 'username', 'title', 'description', 'service', 'orientation', 'media_path', 'sha256', 'created', 'size', 'categories']

class MediaPhotoSerializerDetail(serializers.ModelSerializer):
	class Meta:
		model = MediaPhoto
		fields = '__all__'

