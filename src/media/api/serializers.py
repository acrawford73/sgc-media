from datetime import datetime
from rest_framework import serializers
from media.models import MediaVideo, MediaAudio, MediaPhoto, MediaDoc, MediaVideoGenre
from media.models import MediaVideoService, MediaAudioService, MediaPhotoService, MediaDocService
from media.models import MediaTag, MediaCategory


# Video
class MediaVideoSerializerList(serializers.ModelSerializer):
	#id = serializers.CharField(source='file_uuid')
	#categories = serializers.JSONField(source='tags')
	major_category = serializers.CharField(source='category')
	description = serializers.CharField(source='short_description')
	width = serializers.IntegerField(source='media_video_width')
	height = serializers.IntegerField(source='media_video_height')
	duration = serializers.DecimalField(source='media_video_duration',max_digits=8, decimal_places=3)
	source = serializers.CharField(source='service_source')
	format = serializers.CharField(source='doc_format')
	class Meta:
		model = MediaVideo
		fields = ['id', 'username', 'title', 'description', 'service', 'orientation', 'width', 'height', \
		'media_path', 'file_sha256', 'path_sha256', 'file_uuid', 'created', 'updated', 'duration', 'size', \
		'major_category', 'source', 'format']

class MediaVideoGenreSerializerList(serializers.ModelSerializer):
	class Meta:
		model = MediaVideoGenre
		fields = ['id', 'genre']

class MediaVideoSerializerDetail(serializers.ModelSerializer):
	class Meta:
		model = MediaVideo
		fields = '__all__'

class MediaVideoServiceSerializerList(serializers.ModelSerializer):
	class Meta:
		model = MediaVideoService
		fields = '__all__'

class MediaVideoServiceSerializerDetail(serializers.ModelSerializer):
	class Meta:
		model = MediaVideoService
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
	#id = serializers.CharField(source="file_uuid")
	description = serializers.CharField(source='short_description')
	bitrate = serializers.CharField(source='audio_bitrate')
	major_category = serializers.CharField(source='category')
	class Meta:
		model = MediaAudio
		fields = ['id', 'title', 'artist', 'album', 'album_artist', 'composer', 'genre', \
			'description', 'duration', 'bitrate', 'media_path', 'file_sha256', 'path_sha256', \
			'file_uuid', 'created', 'updated', 'size', 'major_category']

class MediaAudioSerializerDetail(serializers.ModelSerializer):
	class Meta:
		model = MediaAudio
		fields = '__all__'

class MediaAudioServiceSerializerList(serializers.ModelSerializer):
	class Meta:
		model = MediaAudioService
		fields = '__all__'

class MediaAudioServiceSerializerDetail(serializers.ModelSerializer):
	class Meta:
		model = MediaAudioService
		fields = '__all__'

# Photo
class MediaPhotoSerializerList(serializers.ModelSerializer):
	#id = serializers.CharField(source="file_uuid")
	#categories = serializers.JSONField(source='tags')
	description = serializers.CharField(source='short_description')
	source = serializers.CharField(source='service_source')
	major_category = serializers.CharField(source='category')
	class Meta:
		model = MediaPhoto
		fields = ['id', 'username', 'title', 'description', 'service', 'source', 'orientation', \
			'photo_format', 'width', 'height', 'media_path', 'file_sha256', 'path_sha256', \
			'file_uuid', 'created', 'updated', 'size', 'major_category']

class MediaPhotoSerializerDetail(serializers.ModelSerializer):
	class Meta:
		model = MediaPhoto
		fields = '__all__'

class MediaPhotoServiceSerializerList(serializers.ModelSerializer):
	class Meta:
		model = MediaPhotoService
		fields = '__all__'

class MediaPhotoServiceSerializerDetail(serializers.ModelSerializer):
	class Meta:
		model = MediaPhotoService
		fields = '__all__'

# Documents
class MediaDocSerializerList(serializers.ModelSerializer):
	#id = serializers.CharField(source="file_uuid")
	description = serializers.CharField(source='short_description')
	source = serializers.CharField(source="service")
	doc_type = serializers.CharField(source="document_type")
	class Meta:
		model = MediaDoc
		fields = ['id', 'title', 'description', 'authors', 'publication', 'source', 'keywords', \
			'doc_type', 'media_path', 'file_uuid', 'file_sha256', 'path_sha256', 'created', \
			'updated', 'size']

class MediaDocSerializerDetail(serializers.ModelSerializer):
	class Meta:
		model = MediaDoc
		fields = '__all__'

class MediaDocServiceSerializerList(serializers.ModelSerializer):
	class Meta:
		model = MediaDocService
		fields = '__all__'

class MediaDocServiceSerializerDetail(serializers.ModelSerializer):
	class Meta:
		model = MediaDocService
		fields = '__all__'

# Tags
class MediaTagSerializerList(serializers.ModelSerializer):
	class Meta:
		model = MediaTag
		fields = '__all__'

# Category
class MediaCategorySerializerList(serializers.ModelSerializer):
	class Meta:
		model = MediaCategory
		fields = '__all__'
