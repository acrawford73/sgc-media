from rest_framework import serializers
from .models import MediaVideo, MediaAudio, MediaPhoto


# Video
class MediaVideoSerializerList(serializers.ModelSerializer):
	class Meta:
		model = MediaVideo
		fields = ['id', 'username', 'title', 'service', 'media_path', 'sha256', 'created', 'size']

class MediaVideoSerializerDetail(serializers.ModelSerializer):
	class Meta:
		model = MediaVideo
		fields = '__all__'


# Audio
class MediaAudioSerializerList(serializers.ModelSerializer):
	class Meta:
		model = MediaAudio
		fields = ['id', 'title', 'artist', 'album', 'genre', 'media_path', 'sha256', 'created', 'size']

class MediaAudioSerializerDetail(serializers.ModelSerializer):
	class Meta:
		model = MediaAudio
		fields = '__all__'


# Photo
class MediaPhotoSerializerList(serializers.ModelSerializer):
	class Meta:
		model = MediaPhoto
		fields = ['id', 'username', 'title', 'service', 'media_path', 'sha256', 'created', 'size']

class MediaPhotoSerializerDetail(serializers.ModelSerializer):
	class Meta:
		model = MediaPhoto
		fields = '__all__'

