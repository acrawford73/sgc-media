from django.db import models
from django.urls import reverse
from datetime import datetime

#

class MediaCountry(models.Model):
	country_name = models.CharField(max_length=64, null=False, blank=False, unique=True)
	country_code = models.CharField(max_length=2, null=False, blank=False, unique=True)
	class Meta:
		ordering = ['country_name']
	def __str__(self):
		return self.country_name


### VIDEO

# SD: Anything under 720p
# HD: 720p
# FHD: 1080p
# UHD: 4K

MEDIA_FORMATS = (
	("SD", "SD"),
	("HD", "HD"),
	("FHD", "FHD"),
	("UHD", "UHD"),
)

MEDIA_ORIENTATION = (
	("Landscape", "Landscape"),
	("Portrait", "Portrait"),
	("Square", "Square"),
)

VIDEO_SERVICES = (
	("NA", "NA"),
	("Personal", "Personal"),
	("Instagram", "Instagram"),
	("Tumblr", "Tumblr"),
	("DLive", "DLive"),
	("Bitchute", "Bitchute"),
	("Rumble", "Rumble"),
	("Odysee", "Odysee"),
	("Gab", "Gab"),
	("Vimeo", "Vimeo"),
	("Odysee", "Odysee"),
)

class MediaVideoService(models.Model):
	service_name = models.CharField(max_length=32, null=False, blank=False, unique=True)
	class Meta:
		ordering = ['service_name']
	def __str__(self):
		return self.service_name

class MediaVideoFormat(models.Model):
	doc_format = models.CharField(max_length=32, null=False, blank=False, unique=True)
	doc_format_name = models.CharField(max_length=64, null=False, blank=False)
	class Meta:
		ordering = ['doc_format']
	def __str__(self):
		return str(self.doc_format) + " (" + str(self.doc_format_name) + ")"

class MediaVideoGenre(models.Model):
	genre = models.CharField(max_length=64, null=False, blank=False)
	class Meta:
		ordering = ['genre']
	def __str__(self):
		return self.genre

class MediaVideoThumbnail(models.Model):
	mediavideo = models.ForeignKey("MediaVideo", on_delete=models.CASCADE)
	image = models.TextField(max_length=1048576, null=False, blank=False)
	# class Meta:
	# 	ordering = ['mediavideo_id']
	def __str__(self):
		return self.mediavideo

class MediaVideo(models.Model):
	title = models.CharField(max_length=512, default="", null=True, blank=True)
	short_description = models.CharField(max_length=512, default="", null=True, blank=True)
	long_description = models.TextField(max_length=2048, default="", null=True, blank=True)
	notes = models.TextField(max_length=2048, default="", null=True, blank=True)
	file_name = models.CharField(max_length=255, default="")
	file_path = models.CharField(max_length=4096, default="")
	media_path = models.CharField(max_length=4096, default="")
	size = models.PositiveIntegerField(default=0)
	sha256 = models.CharField(max_length=64, default="")
	file_uuid = models.CharField(max_length=36, null=False, blank=False)
	orientation = models.CharField(max_length=16, default="Landscape", null=False, choices=MEDIA_ORIENTATION)
	media_video_width = models.PositiveSmallIntegerField(default=0)
	media_video_height= models.PositiveSmallIntegerField(default=0)
	media_video_format = models.CharField(max_length=16, choices=MEDIA_FORMATS, default='HD')
	media_video_frame_rate = models.CharField(max_length=32, default="", null=True, blank=True)
	media_video_frame_rate_calc = models.DecimalField(default=0.0, max_digits=4, decimal_places=2)
	media_video_bitrate = models.IntegerField(default=0, null=False, blank=False)
	media_video_codec = models.CharField(max_length=32, null=True, blank=True)
	media_video_codec_long_name = models.CharField(max_length=128, null=True, blank=True)
	media_video_codec_tag_string = models.CharField(max_length=128, null=True, blank=True)
	media_video_duration = models.DecimalField(max_digits=12, decimal_places=3, default=0.0, null=True, blank=True)
	media_video_aspect_ratio = models.CharField(max_length=16, null=True, blank=True)
	media_video_pixel_format = models.CharField(max_length=16, null=True, blank=True)
	media_video_color_space = models.CharField(max_length=16, null=True, blank=True)
	media_video_is_avc = models.BooleanField(default=False)
	media_audio_bitrate = models.IntegerField(default=0, null=False, blank=False)
	media_audio_codec = models.CharField(max_length=32, null=True, blank=True)
	media_audio_codec_long_name = models.CharField(max_length=128, null=True, blank=True)
	media_audio_codec_tag_string = models.CharField(max_length=128, null=True, blank=True)
	media_audio_channels = models.PositiveSmallIntegerField(default=0)
	media_audio_sample_rate = models.CharField(max_length=16, null=True, blank=True)
	location_name = models.CharField(max_length=64, default="", null=True, blank=True)
	location_city = models.CharField(max_length=64, default="", null=True, blank=True)
	location_state = models.CharField(max_length=64, default="", null=True, blank=True)
	location_country = models.CharField(max_length=64, default="", null=True, blank=True)
	location_latitude = models.DecimalField(max_digits=12, decimal_places=9, default=0.0, null=True, blank=True)
	location_longitude = models.DecimalField(max_digits=12, decimal_places=9, default=0.0, null=True, blank=True)
	created = models.DateTimeField(auto_now_add=True)
	is_public = models.BooleanField(default=True)
	tags = models.JSONField(default=list, null=True, blank=True)
	service = models.CharField(max_length=32, default="NA", null=True, blank=True, choices=VIDEO_SERVICES)
	service_name = models.ForeignKey("MediaVideoService", on_delete=models.SET_NULL, blank=True, null=True)
	username = models.CharField(max_length=64, default="", null=True, blank=True)
	genre = models.ForeignKey("MediaVideoGenre", on_delete=models.SET_NULL, blank=True, null=True)
	doc_format = models.ForeignKey("MediaVideoFormat", on_delete=models.SET_NULL, blank=True, null=True)

	def get_absolute_url(self):
		return reverse('media-video-detail', kwargs={'pk': self.pk})

	class Meta:
		ordering = ['-created']
		def __unicode__(self):
			return self.file_name



MEDIA_SERVICES = (
	("NA", "NA"),
	("Audio", "Audio"),
	("Document", "Document"),
	("Photo", "Photo"),
	("Video", "Video"),
)

class MediaService(models.Model):
	service = models.CharField(max_length=50, default="", null=True, blank=True)
	media_type = models.CharField(max_length=50, default="NA", choices=MEDIA_SERVICES, null=False, blank=False)
	class Meta:
		ordering = ['service']
	def __str__(self):
		return self.service

### AUDIO

class MediaAudioFormat(models.Model):
	doc_format = models.CharField(max_length=32, null=False, blank=False, unique=True)
	doc_format_name = models.CharField(max_length=64, null=False, blank=False)
	class Meta:
		ordering = ['doc_format']
	def __str__(self):
		return str(self.doc_format) + " (" + str(self.doc_format_name) + ")"

class MediaAudioGenre(models.Model):
	genre = models.CharField(max_length=50, default="", null=True, blank=True)
	class Meta:
		ordering = ['genre']
	def __str__(self):
		return self.genre

class MediaAudio(models.Model):
	title = models.CharField(max_length=128, default="", null=True, blank=True)
	artist = models.CharField(max_length=128, default="", null=True, blank=True)
	album = models.CharField(max_length=128, default="", null=True, blank=True)	
	album_artist = models.CharField(max_length=256, default="", null=True, blank=True)	
	composer = models.CharField(max_length=256, default="", null=True, blank=True)
	genre = models.CharField(max_length=64, default="", null=True, blank=True)
	year = models.CharField(max_length=32, default="", null=True, blank=True)
	track_num = models.CharField(max_length=4, default="", null=True, blank=True)
	track_total = models.CharField(max_length=4, default="", null=True, blank=True)
	disc_num = models.CharField(max_length=2, default="", null=True, blank=True)
	disc_total = models.CharField(max_length=2, default="", null=True, blank=True)
	comments = models.CharField(max_length=512, default="", null=True, blank=True)
	duration = models.DecimalField(max_digits=12, decimal_places=3, default=0.0, null=True, blank=True)
	file_name = models.CharField(max_length=255, default="")   # file.mp3
	file_path = models.CharField(max_length=4096, default="")  # folder-path/file.mp3
	media_path = models.CharField(max_length=4096, default="")
	size = models.PositiveIntegerField(default=0)
	sha256 = models.CharField(max_length=64, default="")
	file_uuid = models.CharField(max_length=36, null=False, blank=False)
	audio_format = models.CharField(max_length=32, default="", null=True, blank=True)
	audio_bitrate = models.CharField(max_length=32, default="", null=True, blank=True)
	audio_sample_rate = models.CharField(max_length=12, default="", null=True, blank=True)
	audio_channels = models.CharField(max_length=16, default="", null=True, blank=True)
	audio_id3_tag = models.CharField(max_length=32, default="", null=True, blank=True)
	audio_codec = models.CharField(max_length=32, default="", null=True, blank=True)
	audio_encoder = models.CharField(max_length=32, default="", null=True, blank=True)
	created = models.DateTimeField(auto_now_add=True)
	is_public = models.BooleanField(default=True)
	service = models.CharField(max_length=32, default="NA", null=True, blank=True)
	short_description = models.CharField(max_length=512, default="", null=True, blank=True)
	long_description = models.TextField(max_length=2048, default="", null=True, blank=True)
	notes = models.TextField(max_length=1024, default="", null=True, blank=True)
	source = models.CharField(max_length=256, default="", null=True, blank=True)
	username = models.CharField(max_length=64, default="", null=True, blank=True)
	tags = models.JSONField(default=list, null=True, blank=True)
	image = models.TextField(max_length=262144, default="", null=True, blank=True)
	extra = models.TextField(max_length=2048, default="", null=True, blank=True)
	doc_format = models.ForeignKey("MediaAudioFormat", on_delete=models.SET_NULL, blank=True, null=True)
	rating = models.PositiveSmallIntegerField(default=0, null=False, blank=False)

	def get_absolute_url(self):
		return reverse('media-audio-detail', kwargs={'pk': self.pk})

	class Meta:
		ordering = ['-created']
		def __unicode__(self):
			return self.pk

### PHOTOS

PHOTO_SERVICES = (
	("NA", "NA"),
	("Tumblr", "Tumblr"),
	("Flickr", "Flickr"),
	("Instagram", "Instagram"),
	("Google", "Google"),
	("Dropbox", "Dropbox"),
	("Amazon", "Amazon"),
)

class MediaPhotoFormat(models.Model):
	doc_format = models.CharField(max_length=32, null=False, blank=False, unique=True)
	doc_format_name = models.CharField(max_length=64, null=False, blank=False)
	class Meta:
		ordering = ['doc_format']
	def __str__(self):
		return str(self.doc_format) + " (" + str(self.doc_format_name) + ")"

class MediaPhoto(models.Model):
	title = models.CharField(max_length=512, default="", null=True, blank=True)
	short_description = models.CharField(max_length=512, default="", null=True, blank=True)
	long_description = models.TextField(max_length=2048, default="", null=True, blank=True)
	file_name = models.CharField(max_length=255, default="")
	file_path = models.CharField(max_length=4096, default="")  # folder-path/file.jpg
	media_path = models.CharField(max_length=4096, default="")
	size = models.PositiveIntegerField(default=0)
	sha256 = models.CharField(max_length=64, default="")
	file_uuid = models.CharField(max_length=36, null=False, blank=False)
	width = models.PositiveSmallIntegerField(default=0)
	height = models.PositiveSmallIntegerField(default=0)
	photo_format = models.CharField(max_length=16, choices=MEDIA_FORMATS, default='HD')
	orientation = models.CharField(max_length=16, default="Landscape", null=False, choices=MEDIA_ORIENTATION)
	is_public = models.BooleanField(default=True)
	tags = models.JSONField(default=list, null=True, blank=True)
	service = models.CharField(max_length=32, default="NA", null=True, blank=True, choices=PHOTO_SERVICES)
	location_name = models.CharField(max_length=64, default="", null=True, blank=True)
	location_city = models.CharField(max_length=64, default="", null=True, blank=True)
	location_state = models.CharField(max_length=64, default="", null=True, blank=True)
	location_country = models.CharField(max_length=64, default="", null=True, blank=True)
	location_latitude = models.DecimalField(max_digits=12, decimal_places=9, default=0.0, null=True, blank=True)
	location_longitude = models.DecimalField(max_digits=12, decimal_places=9, default=0.0, null=True, blank=True)
	created = models.DateTimeField(auto_now_add=True)
	notes = models.TextField(max_length=1024, default="", null=True, blank=True)
	username = models.CharField(max_length=64, default="", null=True, blank=True)
	doc_format = models.ForeignKey("MediaPhotoFormat", on_delete=models.SET_NULL, blank=True, null=True)

	def get_absolute_url(self):
		return reverse('media-photo-detail', kwargs={'pk': self.pk})

	class Meta:
		ordering = ['-created']
		def __unicode__(self):
			return self.file_name


### DOCUMENTS

class MediaDocFormat(models.Model):
	doc_format = models.CharField(max_length=32, null=False, blank=False, unique=True)
	doc_format_name = models.CharField(max_length=64, null=False, blank=False)
	class Meta:
		ordering = ['doc_format']
	def __str__(self):
		return str(self.doc_format) + " (" + str(self.doc_format_name) + ")"

class MediaDocCategories(models.Model):
	category = models.CharField(max_length=64, null=False, blank=False, unique=True)
	class Meta:
		ordering = ['category']
	def __str__(self):
		return self.category

class MediaDoc(models.Model):
	title = models.CharField(max_length=512, default="", null=True, blank=True)
	short_description = models.CharField(max_length=512, default="", null=True, blank=True)
	long_description = models.TextField(max_length=2048, default="", null=True, blank=True)
	notes = models.TextField(max_length=2048, default="", null=True, blank=True)
	file_name = models.CharField(max_length=255, default="")
	file_path = models.CharField(max_length=4096, default="")
	media_path = models.CharField(max_length=4096, default="")
	size = models.PositiveIntegerField(default=0)
	sha256 = models.CharField(max_length=64, default="")
	file_uuid = models.CharField(max_length=36, null=False, blank=False)
	doi_url = models.URLField(max_length=2083, null=True, blank=True)
	source_url = models.URLField(max_length=2083, null=True, blank=True)
	### this is actually doc_format_id
	doc_format = models.ForeignKey("MediaDocFormat", on_delete=models.SET_NULL, blank=True, null=True)
	###
	category = models.ForeignKey("MediaDocCategories", on_delete=models.SET_NULL, blank=True, null=True)
	keywords = models.CharField(max_length=1024, default="", null=True, blank=True)
	created = models.DateTimeField(auto_now_add=True)
	#updated = models.DateTimeField(auto_now=True)
	is_public = models.BooleanField(default=True)
	tags = models.JSONField(default=list, null=True, blank=True)

	def get_absolute_url(self):
		return reverse('media-doc-detail', kwargs={'pk': self.pk})

	class Meta:
		ordering = ['-created']
		def __unicode__(self):
			return self.file_name

# class Settings(models.Model):
# 	upload_path = models.CharField(max_length=4096, default="", null=True, blank=True)

# 	# def get_absolute_url(self):
# 	# 	return reverse('settings-detail', kwargs={'pk': self.pk})

# 	class Meta:
# 		def __unicode__(self):
# 			return self.upload_path