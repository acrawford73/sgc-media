from django.db import models
from django.urls import reverse

#

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

VIDEO_GENRES = (
	("Action","Action"),
	("Adventure","Adventure"),
	("Animals","Animals"),
	("Animated","Animated"),
	("Anime","Anime"),
	("Children","Children"),
	("Comedy","Comedy"),
	("Crime","Crime"),
	("Documentary","Documentary"),
	("Drama","Drama"),
	("Educational","Educational"),
	("Fantasy","Fantasy"),
	("Faith","Faith"),
	("Food","Food"),
	("Fashion","Fashion"),
	("Gaming","Gaming"),
	("Health","Health"),
	("History","History"),
	("Horror","Horror"),
	("Miniseries","Miniseries"),
	("Mystery","Mystery"),
	("Nature","Nature"),
	("News","News"),
	("Reality","Reality"),
	("Romance","Romance"),
	("Science","Science"),
	("Science Fiction","Science Fiction"),
	("Sitcom","Sitcom"),
	("Special","Special"),
	("Sports","Sports"),
	("Thriller","Thriller"),
	("Technology","Technology"),
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
	("NAS", "NAS"),
)


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
	media_video_frame_rate = models.CharField(max_length=32, default="")
	media_video_codec = models.CharField(max_length=32, default="")
	media_video_duration = models.DecimalField(max_digits=12, decimal_places=3, default=0.0, null=True, blank=True)
	media_audio_codec = models.CharField(max_length=32, default="")
	media_audio_channels = models.PositiveSmallIntegerField(default=0)
	media_audio_sample_rate = models.CharField(max_length=16, default="")
	location_name = models.CharField(max_length=64, default="", null=True, blank=True)
	location_city = models.CharField(max_length=64, default="", null=True, blank=True)
	location_state = models.CharField(max_length=64, default="", null=True, blank=True)
	location_country = models.CharField(max_length=64, default="", null=True, blank=True)
	location_latitude = models.DecimalField(max_digits=12, decimal_places=9, default=0.0, null=True, blank=True)
	location_longitude = models.DecimalField(max_digits=12, decimal_places=9, default=0.0, null=True, blank=True)
	created = models.DateTimeField()
	is_public = models.BooleanField(default=True)
	tags = models.JSONField(default=list, null=True, blank=True)
	service = models.CharField(max_length=32, default="NA", null=True, blank=True, choices=VIDEO_SERVICES)
	username = models.CharField(max_length=64, default="", null=True, blank=True)

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
	title = models.CharField(max_length=128, default="", null=True, blank=True)
	artist = models.CharField(max_length=128, default="", null=True, blank=True)
	album = models.CharField(max_length=128, default="", null=True, blank=True)	
	album_artist = models.CharField(max_length=128, default="", null=True, blank=True)	
	composer = models.CharField(max_length=128, default="", null=True, blank=True)
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
	created = models.DateTimeField()
	is_public = models.BooleanField(default=True)
	service = models.CharField(max_length=32, default="NA", null=True, blank=True)
	short_description = models.CharField(max_length=512, default="", null=True, blank=True)
	long_description = models.TextField(max_length=2048, default="", null=True, blank=True)
	source = models.TextField(max_length=512, default="", null=True, blank=True)
	notes = models.TextField(max_length=1024, default="", null=True, blank=True)
	username = models.CharField(max_length=64, default="", null=True, blank=True)
	tags = models.JSONField(default=list, null=True, blank=True)
	image = models.TextField(max_length=262144, default="", null=True, blank=True)
	extra = models.TextField(max_length=2048, default="", null=True, blank=True)

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

class MediaPhoto(models.Model):
	title = models.CharField(max_length=512, default="", null=True, blank=True)
	short_description = models.CharField(max_length=512, default="", null=True, blank=True)
	long_description = models.TextField(max_length=2048, default="", null=True, blank=True)
	file_name = models.CharField(max_length=255, default="")
	file_path = models.CharField(max_length=4096, default="")  # folder-path/file.mp4
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
	created = models.DateTimeField()
	notes = models.TextField(max_length=1024, default="", null=True, blank=True)
	username = models.CharField(max_length=64, default="", null=True, blank=True)

	def get_absolute_url(self):
		return reverse('media-photo-detail', kwargs={'pk': self.pk})

	class Meta:
		ordering = ['-created']
		def __unicode__(self):
			return self.file_name


DOC_FORMATS = (
	("NA", "NA"),
	("TXT", "Text"),
	("PDF", "Adobe PDF"),
	("EPUB", "eBook"),
	("DOC", "Microsoft Word"),
	("DOCX", "Microsoft Word"),
	("XLS", "Microsoft Excel"),
	("XLSX", "Microsoft Excel"),
	("PPT", "Microsoft Powerpoint"),
	("PPTX", "Microsoft Powerpoint"),
	("ODT", "LibreOffice Writer"),
	("ODS", "LibreOffice Calc"),
	("ODG", "LibreOffice Draw"),
	("ODP", "LibreOffice Impress"),
)

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
	doc_format = models.CharField(max_length=32, choices=DOC_FORMATS, default='PDF')
	keywords = models.CharField(max_length=1024, default="", null=True, blank=True)
	created = models.DateTimeField()
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