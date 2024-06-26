from django import forms
from .models import RokuContentFeed, Playlist


class RokuContentFeedForm(forms.Form):
	# is_public = models.BooleanField(label='Is Public?', default=False)
	# provider_name = models.CharField(label='Provider Name', max_length=50, default="", blank=False)
	# short_description = models.CharField(label='Description', max_length=200, default="", null=False, blank=True)
	# language = models.ForeignKey(label='Language', default=1, blank=False)
	# rating = models.ForeignKey('Rating', on_delete=models.PROTECT, null=False, blank=False)
	# categories = models.ManyToManyField('Category', through='RokuContentFeedCategory', related_name='category', blank=True)
	# playlists = models.ManyToManyField('Playlist', through='RokuContentFeedPlaylist', blank=True)
	# movies = models.ManyToManyField('Movie', through='RokuContentFeedMovie', blank=True)
	# live_feeds = models.ManyToManyField('LiveFeed', through='RokuContentFeedLiveFeed', blank=True)
	# series = models.ManyToManyField('Series', through='RokuContentFeedSeries', blank=True)
	# short_form_videos = models.ManyToManyField('ShortFormVideo', through='RokuContentFeedShortFormVideo', blank=True)
	# tv_specials = models.ManyToManyField('TVSpecial', through='RokuContentFeedTVSpecial', blank=True)
	class Meta:
		model = RokuContentFeed
		fields = '__all__'


class PlaylistForm(forms.Form):
	# playlist_name = models.CharField(max_length=50, default="", blank=False)
	# short_description = models.CharField(max_length=200, default="", blank=True)
	# item_ids = models.ManyToManyField(label='Item IDs', blank=True)
	class Meta:
		model = Playlist
		fields = ['playlist_name', 'short_description']

