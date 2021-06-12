from django.db import models
from django.urls import reverse
import uuid

#

MEDIA_FORMATS = (
	("SD", "SD"),
	("HD720", "HD720"),
	("HD1080", "HD1080"),
	("4K", "4K"),
)

class MediaVideo(models.Model):
	title = models.CharField(max_length=64, default="", null=True, blank=True)
	short_description = models.CharField(max_length=256, default="", null=True, blank=True)
	long_description = models.TextField(max_length=512, default="", null=True, blank=True)
	notes = models.TextField(max_length=512, default="", null=True, blank=True)
	file_name = models.CharField(max_length=255, default="")
	file_path = models.CharField(max_length=4096, default="")  # folder-path/file.mp4
	media_path = models.CharField(max_length=4096, default="")
	file_size = models.PositiveIntegerField(default=0)
	file_sha256 = models.CharField(max_length=64, default="")
	file_uuid = models.CharField(max_length=36, null=False, blank=False)
	media_video_width = models.PositiveSmallIntegerField(default=0)
	media_video_height= models.PositiveSmallIntegerField(default=0)
	media_video_format = models.CharField(max_length=16, choices=MEDIA_FORMATS, default='HD720')
	media_video_frame_rate = models.CharField(max_length=32, default="")
	media_video_codec = models.CharField(max_length=32, default="")
	media_video_aspect_ratio = models.CharField(max_length=16, default="")
	#media_video_duration = models.PositiveIntegerField(default=0)
	media_audio_codec = models.CharField(max_length=32, default="")
	media_audio_channels = models.PositiveSmallIntegerField(default=0)
	media_audio_sample_rate = models.CharField(max_length=16, default="")
	created = models.DateTimeField()
	is_published = models.BooleanField(default=False)

	def get_absolute_url(self):
		return reverse('media-video-detail', kwargs={'pk': self.pk})

	class Meta:
		ordering = ['-created']
		def __unicode__(self):
			return self.file_name


class AudioGenre(models.Model):
	genre = models.CharField(max_length=50, default="", null=True, blank=True)
	class Meta:
		ordering = ['genre']
		def __unicode__(self):
			return self.genre


class MediaService(models.Model):
	service = models.CharField(max_length=50, default="", null=True, blank=True)
	class Meta:
		ordering = ['service']
		def __unicode__(self):
			return self.service


class MediaAudio(models.Model):
	title = models.CharField(max_length=64, default="", null=True, blank=True)
	artist = models.CharField(max_length=64, default="", null=True, blank=True)
	album = models.CharField(max_length=64, default="", null=True, blank=True)	
	composer = models.CharField(max_length=64, default="", null=True, blank=True)
	genre = models.CharField(max_length=64, default="", null=True, blank=True)
	year = models.CharField(max_length=4, default="", null=True, blank=True)
	track_num = models.CharField(max_length=4, default="", null=True, blank=True)
	track_total = models.CharField(max_length=4, default="", null=True, blank=True)
	disk_num = models.CharField(max_length=2, default="", null=True, blank=True)
	disk_total = models.CharField(max_length=2, default="", null=True, blank=True)
	comments = models.CharField(max_length=64, default="", null=True, blank=True)
	artwork = models.CharField(max_length=64, default="", null=True, blank=True)
	duration = models.CharField(max_length=16, default="", null=True, blank=True)
	file_name = models.CharField(max_length=255, default="")   # file.mp3
	file_path = models.CharField(max_length=4096, default="")  # folder-path/file.mp3
	media_path = models.CharField(max_length=4096, default="")
	file_size = models.PositiveIntegerField(default=0)
	file_sha256 = models.CharField(max_length=64, default="")
	file_uuid = models.CharField(max_length=36, null=False, blank=False)
	audio_format = models.CharField(max_length=32, default="")
	audio_bitrate = models.CharField(max_length=32, default="")
	audio_sample_rate = models.CharField(max_length=8, default="")
	audio_channels = models.CharField(max_length=16, default="", null=True, blank=True)
	audio_id3_tag = models.CharField(max_length=32, default="")
	audio_codec = models.CharField(max_length=32, default="")
	audio_encoder = models.CharField(max_length=32, default="")
	created = models.DateTimeField()
	is_published = models.BooleanField(default=False)
	short_description = models.CharField(max_length=256, default="", null=True, blank=True)
	long_description = models.TextField(max_length=512, default="", null=True, blank=True)
	notes = models.TextField(max_length=512, default="", null=True, blank=True)

	def get_absolute_url(self):
		return reverse('media-audio-detail', kwargs={'pk': self.pk})

	class Meta:
		ordering = ['-created']
		def __unicode__(self):
			return self.file_name


PHOTO_SERVICES = (
	("NA", "NA"),
	("Tumblr", "Tumblr"),
	("Flickr", "Flickr"),
	("Instagram", "Instagram"),
	("Google", "Google"),
	("Dropbox", "Dropbox"),
	("Amazon", "Amazon"),
	("NAS", "NAS"),
)

PHOTO_ORIENTATION = (
	("Landscape", "Landscape"),
	("Portrait", "Portrait"),
	("Square", "Square"),
)

class MediaPhoto(models.Model):
	title = models.CharField(max_length=64, default="", null=True, blank=True)
	short_description = models.CharField(max_length=128, default="", null=True, blank=True)
	long_description = models.TextField(max_length=256, default="", null=True, blank=True)
	full_name = models.CharField(max_length=255, default="")
	file_name = models.CharField(max_length=255, default="")
	file_path = models.CharField(max_length=4096, default="")  # folder-path/file.mp4
	media_path = models.CharField(max_length=4096, default="")
	file_size = models.PositiveIntegerField(default=0)
	file_sha256 = models.CharField(max_length=64, default="")
	file_uuid = models.CharField(max_length=36, null=False, blank=False)
	width = models.PositiveSmallIntegerField(default=0)
	height = models.PositiveSmallIntegerField(default=0)
	orientation = models.CharField(max_length=16, default="Landscape", null=False, choices=PHOTO_ORIENTATION)
	tags = models.CharField(max_length=32, default="", null=True, blank=True)
	is_public = models.BooleanField(default=True)
	service = models.CharField(max_length=32, default="NA", null=True, blank=True, choices=PHOTO_SERVICES)
	location_name = models.CharField(max_length=64, default="", null=True, blank=True)
	location_latitude = models.CharField(max_length=64, default="", null=True, blank=True)
	location_longitude = models.CharField(max_length=64, default="", null=True, blank=True)
	created = models.DateTimeField()
	notes = models.TextField(max_length=512, default="", null=True, blank=True)

	def get_absolute_url(self):
		return reverse('media-photo-detail', kwargs={'pk': self.pk})

	class Meta:
		ordering = ['-created']
		def __unicode__(self):
			return self.file_name


