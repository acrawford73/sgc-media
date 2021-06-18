from rest_framework import serializers
from .models import MediaVideo, MediaAudio, MediaPhoto


# Video
class MediaVideoSerializerList(serializers.ModelSerializer):
	class Meta:
		model = MediaVideo
		fields = ['id', 'title', 'file_name', 'file_path', 'sha256', 'file_uuid', 'size', 'created', 'service', 'orientation']

class MediaVideoSerializerDetail(serializers.ModelSerializer):
	class Meta:
		model = MediaVideo
		fields = '__all__'


# Audio
class MediaAudioSerializerList(serializers.ModelSerializer):
	class Meta:
		model = MediaAudio
		fields = ['id', 'title', 'file_name', 'file_path', 'sha256', 'file_uuid', 'size', 'created']

class MediaAudioSerializerDetail(serializers.ModelSerializer):
	class Meta:
		model = MediaAudio
		fields = '__all__'


# Photo
class MediaPhotoSerializerList(serializers.ModelSerializer):
	class Meta:
		model = MediaPhoto
		fields = ['id', 'title', 'media_path', 'sha256', 'size', 'created', 'service', 'orientation']

class MediaPhotoSerializerDetail(serializers.ModelSerializer):
	class Meta:
		model = MediaPhoto
		fields = '__all__'

