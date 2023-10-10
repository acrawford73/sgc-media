from django.contrib import admin

## Roku Content Feed, Categories, Types, Properties
from .models import RokuContentFeed
from .models import Language, Category, Playlist
from .models import Movie, LiveFeed, Series, Season, Episode, ShortFormVideo, TVSpecial
from .models import Content, Video, Caption, TrickPlayFile, Genre, ExternalID, ExternalIDType, \
					Rating, RatingSource, ParentalRating, Credit

# Roku Content Feed

class RokuContentFeedAdmin(admin.ModelAdmin):
	list_display = ['provider_name']
	search_fields = ['provider_name']
	list_filter = ['language']
	readonly_fields = ['last_updated']
	class Meta:
		model = RokuContentFeed

# Roku Categories

class LanguageAdmin(admin.ModelAdmin):
	list_display = ['language_name_eng', 'code_iso_639_2', 'code_iso_639_1']
	search_fields = ['language_name_eng', 'code_iso_639_2', 'code_iso_639_1']
	class Meta:
		model = Language

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
	list_display = ['movie_id', 'title', 'release_date']
	search_fields = ['movie_id', 'title', 'tags', 'credits', 'rating', 'release_date']
	list_filter = ['genres', 'tags', 'rating']
	class Meta:
		model = Movie

class LiveFeedAdmin(admin.ModelAdmin):
	list_display = ['livefeed_id', 'title']
	search_fields = ['livefeed_id', 'title', 'tags', 'rating', 'genres']
	list_filter = ['genres', 'tags', 'rating']
	class Meta:
		model = LiveFeed

class SeriesAdmin(admin.ModelAdmin):
	list_display = ['series_id', 'title', 'seasons', 'episodes', 'genres', 'release_date']
	search_fields = ['series_id', 'title', 'genres', 'short_description', \
		'long_description', 'credits', 'tags', 'external_ids', 'release_date']
	list_filter = ['seasons', 'episodes', 'genres', 'tags', 'external_ids']
	class Meta:
		model = Series

class SeasonAdmin(admin.ModelAdmin):
	list_display = ['id', 'season_number', 'episodes']
	search_fields = ['season_number', 'episodes']
	list_filter = ['season_number', 'episodes']
	class Meta:
		model = Season

class EpisodeAdmin(admin.ModelAdmin):
	list_display = ['id', 'title', 'episode_number', 'release_date']
	search_fields = ['episode_id', 'title', 'episode_number', 'short_description', \
		'long_description', 'credits', 'rating', 'external_ids', 'release_date']
	list_filter = ['episode_number', 'rating', 'external_ids']
	class Meta:
		model = Episode

class ShortFormVideoAdmin(admin.ModelAdmin):
	list_display = ['id', 'title', 'genres', 'release_date']
	search_fields = ['short_form_video_id', 'title', 'short_description', \
		'long_description', 'genres', 'credits', 'rating', 'tags', 'release_date']
	list_filter = ['title', 'genres', 'rating', 'tags']
	class Meta:
		model = ShortFormVideo

class TVSpecialAdmin(admin.ModelAdmin):
	list_display = ['id', 'title', 'genres', 'release_date']
	search_fields = ['tv_special_id', 'title', 'short_description', 'long_description', \
		'genres', 'rating', 'tags', 'release_date']
	list_filter = ['title', 'genres', 'rating', 'tags']
	class Meta:
		model = TVSpecial

# Roku Properties

class ContentAdmin(admin.ModelAdmin):
	list_display = ['id', 'duration', 'language', 'date_added']
	search_fields = ['language', 'date_added']
	list_filter = ['language', 'date_added']
	readonly_fields = ['date_added']
	class Meta:
		model = Content

class VideoAdmin(admin.ModelAdmin):
	list_display = ['url', 'quality', 'video_type']
	search_fields = ['quality', 'video_type']
	list_filter = ['quality', 'video_type']
	class Meta:
		model = Video

class CaptionAdmin(admin.ModelAdmin):
	list_display = ['url', 'language', 'caption_type']
	search_fields = ['url', 'language', 'caption_type']
	list_filter = ['language', 'caption_type']
	class Meta:
		model = Caption

class TrickPlayFileAdmin(admin.ModelAdmin):
	list_display = ['url', 'quality']
	search_fields = ['url', 'quality']
	list_filter = ['quality']
	class Meta:
		model = TrickPlayFile

class GenreAdmin(admin.ModelAdmin):
	list_display = ['genre']
	search_fields = ['genre']
	class Meta:
		model = Genre

class ExternalIDAdmin(admin.ModelAdmin):
	list_display = ['external_id', 'id_type']
	search_fields = ['external_id', 'id_type']
	list_filter = ['id_type']
	class Meta:
		model = ExternalID

class ExternalIDTypeAdmin(admin.ModelAdmin):
	list_display = ['external_id_type', 'external_id_long_name']
	search_fields = ['external_id_type', 'external_id_long_name']
	class Meta:
		model = ExternalIDType

class RatingAdmin(admin.ModelAdmin):
	list_display = ['rating', 'rating_source']
	search_fields = ['rating', 'rating_source']
	list_filter = ['rating_source']
	class Meta:
		model = Rating

class RatingSourceAdmin(admin.ModelAdmin):
	list_display = ['source_name', 'source_long_name']
	search_fields = ['source_name', 'source_long_name']
	list_filter = ['source_name']
	class Meta:
		model = RatingSource

class ParentalRatingAdmin(admin.ModelAdmin):
	list_display = ['parental_rating']
	search_fields = ['parental_rating']
	class Meta:
		model = ParentalRating

class CreditAdmin(admin.ModelAdmin):
	list_display = ['credit_name', 'role', 'birth_date']
	search_fields = ['credit_name', 'role', 'birth_date']
	list_filter = ['role']
	class Meta:
		model = Credit


# Register with Admin
admin.site.register(RokuContentFeed, RokuContentFeedAdmin)

admin.site.register(Language, LanguageAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Playlist, PlaylistAdmin)

admin.site.register(Movie, MovieAdmin)
admin.site.register(LiveFeed, LiveFeedAdmin)
admin.site.register(Series, SeriesAdmin)
admin.site.register(Season, SeasonAdmin)
admin.site.register(Episode, EpisodeAdmin)
admin.site.register(ShortFormVideo, ShortFormVideoAdmin)
admin.site.register(TVSpecial, TVSpecialAdmin)

admin.site.register(Content, ContentAdmin)
admin.site.register(Video, VideoAdmin)
admin.site.register(Caption, CaptionAdmin)
admin.site.register(TrickPlayFile, TrickPlayFileAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(ExternalID, ExternalIDAdmin)
admin.site.register(ExternalIDType, ExternalIDTypeAdmin)
admin.site.register(Rating, RatingAdmin)
admin.site.register(RatingSource, RatingSourceAdmin)
admin.site.register(ParentalRating, ParentalRatingAdmin)
admin.site.register(Credit, CreditAdmin)
