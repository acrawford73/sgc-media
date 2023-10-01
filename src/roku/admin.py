from django.contrib import admin

## Roku Content Categories, Types, Properties
from .models import Category, Playlist
from .models import Movie, LiveFeed, Series, Season, Episode, ShortFormVideo, TVSpecial
from .models import Content, Video, Caption, TrickPlayFile, Genre, ExternalID, Rating, RatingSource, ParentalRating, Credit

# Roku Categories

class CategoryAdmin(admin.ModelAdmin):
	list_display = ['category_name', 'playlist_name', 'order']
	search_fields = ['category_name']
	list_filter = ['order']
	class Meta:
		model = Category

class PlaylistAdmin(admin.ModelAdmin):
	list_display = ['playlist_name', 'created', 'is_public']
	search_fields = ['playlist_name', 'is_public']
	list_filter = ['is_public']
	readonly_fields = ['created']
	class Meta:
		model = Playlist

# Roku Types

class MovieAdmin(admin.ModelAdmin):
	list_display = ['movie_id', 'title']
	search_fields = ['movie_id', 'title', 'release_date', 'tags', 'credits', 'rating']
	class Meta:
		model = Movie

class LiveFeedAdmin(admin.ModelAdmin):
	list_display = ['livefeed_id', 'title']
	search_fields = ['livefeed_id', 'title', 'tags', 'rating', 'genres']
	class Meta:
		model = LiveFeed

class SeriesAdmin(admin.ModelAdmin):
	list_display = ['file_name', 'size', 'media_video_format', 'service', 'created']
	search_fields = ['file_name', 'media_video_format']
	list_filter = ['media_video_format', 'service', 'is_public']
	readonly_fields = ['size', 'sha256', 'file_uuid', 'created']
	class Meta:
		model = Series

class SeasonAdmin(admin.ModelAdmin):
	list_display = ['file_name', 'size', 'media_video_format', 'service', 'created']
	search_fields = ['file_name', 'media_video_format']
	list_filter = ['media_video_format', 'service', 'is_public']
	readonly_fields = ['size', 'sha256', 'file_uuid', 'created']
	class Meta:
		model = Season

class EpisodeAdmin(admin.ModelAdmin):
	list_display = ['file_name', 'size', 'media_video_format', 'service', 'created']
	search_fields = ['file_name', 'media_video_format']
	list_filter = ['media_video_format', 'service', 'is_public']
	readonly_fields = ['size', 'sha256', 'file_uuid', 'created']
	class Meta:
		model = Episode

class ShortFormVideoAdmin(admin.ModelAdmin):
	list_display = ['file_name', 'size', 'media_video_format', 'service', 'created']
	search_fields = ['file_name', 'media_video_format']
	list_filter = ['media_video_format', 'service', 'is_public']
	readonly_fields = ['size', 'sha256', 'file_uuid', 'created']
	class Meta:
		model = ShortFormVideo

class TVSpecialAdmin(admin.ModelAdmin):
	list_display = ['file_name', 'size', 'media_video_format', 'service', 'created']
	search_fields = ['file_name', 'media_video_format']
	list_filter = ['media_video_format', 'service', 'is_public']
	readonly_fields = ['size', 'sha256', 'file_uuid', 'created']
	class Meta:
		model = TVSpecial

# Roku Properties

class ContentAdmin(admin.ModelAdmin):
	list_display = ['file_name', 'size', 'media_video_format', 'service', 'created']
	search_fields = ['file_name', 'media_video_format']
	list_filter = ['media_video_format', 'service', 'is_public']
	readonly_fields = ['size', 'sha256', 'file_uuid', 'created']
	class Meta:
		model = Content

class VideoAdmin(admin.ModelAdmin):
	list_display = ['file_name', 'size', 'media_video_format', 'service', 'created']
	search_fields = ['file_name', 'media_video_format']
	list_filter = ['media_video_format', 'service', 'is_public']
	readonly_fields = ['size', 'sha256', 'file_uuid', 'created']
	class Meta:
		model = Video

class CaptionAdmin(admin.ModelAdmin):
	list_display = ['file_name', 'size', 'media_video_format', 'service', 'created']
	search_fields = ['file_name', 'media_video_format']
	list_filter = ['media_video_format', 'service', 'is_public']
	readonly_fields = ['size', 'sha256', 'file_uuid', 'created']
	class Meta:
		model = Caption

class TrickPlayFileAdmin(admin.ModelAdmin):
	list_display = ['file_name', 'size', 'media_video_format', 'service', 'created']
	search_fields = ['file_name', 'media_video_format']
	list_filter = ['media_video_format', 'service', 'is_public']
	readonly_fields = ['size', 'sha256', 'file_uuid', 'created']
	class Meta:
		model = TrickPlayFile

class GenreAdmin(admin.ModelAdmin):
	list_display = ['file_name', 'size', 'media_video_format', 'service', 'created']
	search_fields = ['file_name', 'media_video_format']
	list_filter = ['media_video_format', 'service', 'is_public']
	readonly_fields = ['size', 'sha256', 'file_uuid', 'created']
	class Meta:
		model = Genre

class ExternalIDAdmin(admin.ModelAdmin):
	list_display = ['file_name', 'size', 'media_video_format', 'service', 'created']
	search_fields = ['file_name', 'media_video_format']
	list_filter = ['media_video_format', 'service', 'is_public']
	readonly_fields = ['size', 'sha256', 'file_uuid', 'created']
	class Meta:
		model = ExternalID

class RatingAdmin(admin.ModelAdmin):
	list_display = ['file_name', 'size', 'media_video_format', 'service', 'created']
	search_fields = ['file_name', 'media_video_format']
	list_filter = ['media_video_format', 'service', 'is_public']
	readonly_fields = ['size', 'sha256', 'file_uuid', 'created']
	class Meta:
		model = Rating

class RatingSourceAdmin(admin.ModelAdmin):
	list_display = ['file_name', 'size', 'media_video_format', 'service', 'created']
	search_fields = ['file_name', 'media_video_format']
	list_filter = ['media_video_format', 'service', 'is_public']
	readonly_fields = ['size', 'sha256', 'file_uuid', 'created']
	class Meta:
		model = RatingSource

class ParentalRatingAdmin(admin.ModelAdmin):
	list_display = ['file_name', 'size', 'media_video_format', 'service', 'created']
	search_fields = ['file_name', 'media_video_format']
	list_filter = ['media_video_format', 'service', 'is_public']
	readonly_fields = ['size', 'sha256', 'file_uuid', 'created']
	class Meta:
		model = ParentalRating

class CreditAdmin(admin.ModelAdmin):
	list_display = ['file_name', 'size', 'media_video_format', 'service', 'created']
	search_fields = ['file_name', 'media_video_format']
	list_filter = ['media_video_format', 'service', 'is_public']
	readonly_fields = ['size', 'sha256', 'file_uuid', 'created']
	class Meta:
		model = Credit
