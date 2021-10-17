from django.db import models
from django.urls import reverse
from media.models import MediaVideo,MediaAudio,MediaPhoto

#

MEDIA_TYPE = (
	("Video", "Video"),
	("Audio", "Audio"),
	("Photo", "Photo"),
)


# Playlists named
class Playlist(models.Model)
	#playlist_id = models.PositiveBigIntegerField(primary_key=True)
	title = models.CharField(max_length=64, default="", null=True, blank=True)
	short_description = models.CharField(max_length=200, default="", null=True, blank=True)
	notes = models.TextField(max_length=1024, default="", null=True, blank=True)
	created = models.DateTimeField()
	is_public = models.BooleanField(default=True)

	def get_absolute_url(self):
		return reverse('playlists', kwargs={'pk': self.pk})

	class Meta:
		ordering = ['-id']
		def __unicode__(self):
			return self.title


# Playlist items for each playlist
class PlaylistItemsVideo(models.Model)
	playlist_id = models.ForeignKey('Playlist', on_delete=models.CASCADE,)
	media_id = models.ForeignKey('MediaVideo', on_delete=models.CASCADE,)

	def get_absolute_url(self):
		return reverse('playlist-item', kwargs={'pk': self.pk})

	class Meta:
		ordering = ['id']
		def __unicode__(self):
			return self.id


class PlaylistItemsAudio(models.Model)
	playlist_id = models.ForeignKey('Playlist', on_delete=models.CASCADE,)
	media_id = models.ForeignKey('MediaAudio', on_delete=models.CASCADE,)
	def get_absolute_url(self):
		return reverse('playlist-item', kwargs={'pk': self.pk})
	class Meta:
		ordering = ['id']
		def __unicode__(self):
			return self.id


class PlaylistItemsPhoto(models.Model)
	playlist_id = models.ForeignKey('Playlist', on_delete=models.CASCADE,)
	media_id = models.ForeignKey('MediaPhoto', on_delete=models.CASCADE,)

	def get_absolute_url(self):
		return reverse('playlist-item', kwargs={'pk': self.pk})

	class Meta:
		ordering = ['id']
		def __unicode__(self):
			return self.id

