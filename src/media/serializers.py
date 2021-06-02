from rest_framework import serializers
from .models import MediaVideo, MediaAudio, MediaPhoto


# Video
class MediaVideoSerializerList(serializers.ModelSerializer):
	class Meta:
		model = MediaVideo
		fields = ['id', 'title', 'file_name', 'file_path', 'file_sha256', 'file_uuid', 'file_size', 'created']

class MediaVideoSerializerDetail(serializers.ModelSerializer):
	class Meta:
		model = MediaVideo
		fields = '__all__'


# Audio
class MediaAudioSerializerList(serializers.ModelSerializer):
	class Meta:
		model = MediaAudio
		fields = ['id', 'title', 'file_name', 'file_path', 'file_sha256', 'file_uuid', 'file_size', 'created']

class MediaAudioSerializerDetail(serializers.ModelSerializer):
	class Meta:
		model = MediaAudio
		fields = '__all__'


# Photo
class MediaPhotoSerializerList(serializers.ModelSerializer):
	class Meta:
		model = MediaPhoto
		fields = ['id', 'title', 'file_name', 'file_path', 'media_path', 'file_sha256', 'file_uuid', 'file_size', 'created']

class MediaPhotoSerializerDetail(serializers.ModelSerializer):
	class Meta:
		model = MediaPhoto
		fields = '__all__'

