from django.contrib import admin

## Roku Content Feed, Categories, Types, Properties
from .models import RokuContentFeed
from .models import Language, Category, Playlist
from .models import Movie, LiveFeed, Series, Season, Episode, ShortFormVideo, TVSpecial
from .models import Content, Video, VideoType, Caption, TrickPlayFile, Genre, ExternalID
from .models import ExternalIDType,	Rating, RatingSource, RatingCountry, ParentalRating, CreditRole, Credit, Tag

# Roku Content Feed

class RokuContentFeedAdmin(admin.ModelAdmin):
	fields = ['is_public', 'roku_content_feed_id', 'provider_name', 'language', \
		'rating', 'short_description', 'last_updated', 'created']
	list_display = ['provider_name', 'language', 'last_updated', 'created']
	search_fields = ['provider_name', 'roku_content_feed_id']
	list_filter = ['language']
	readonly_fields = ['roku_content_feed_id', 'last_updated', 'created']
	class Meta:
		model = RokuContentFeed

# Roku Content Categories

class CategoryAdmin(admin.ModelAdmin):
	list_display = ['category_name', 'playlist_name', 'order']
	search_fields = ['category_name']
	list_filter = ['order']
	class Meta:
		model = Category

class PlaylistAdmin(admin.ModelAdmin):
	list_display = ['playlist_name', 'created']
	search_fields = ['playlist_name']
	readonly_fields = ['created']
	class Meta:
		model = Playlist

# Roku Content Types

class MovieAdmin(admin.ModelAdmin):
	list_display = ['title', 'release_date']
	search_fields = ['uuid_id', 'title', 'release_date']
	list_filter = ['genres']
	readonly_fields = ['uuid_id', 'thumbnail_width', 'thumbnail_height']
	class Meta:
		model = Movie

class LiveFeedAdmin(admin.ModelAdmin):
	list_display = ['uuid_id', 'title']
	search_fields = ['uuid_id', 'title']
	list_filter = ['genres']
	readonly_fields = ['uuid_id']
	class Meta:
		model = LiveFeed

class SeriesAdmin(admin.ModelAdmin):
	list_display = ['id', 'title', 'release_date']
	search_fields = ['uuid_id', 'title', 'release_date']
	#list_filter = ['seasons', 'episodes', 'genres']
	readonly_fields = ['uuid_id']
	class Meta:
		model = Series

class SeasonAdmin(admin.ModelAdmin):
	list_display = ['id', 'title_season', 'season_number']
	search_fields = ['title_season', 'season_number']
	list_filter = ['season_number']
	class Meta:
		model = Season

class EpisodeAdmin(admin.ModelAdmin):
	list_display = ['id', 'title', 'episode_number', 'release_date']
	search_fields = ['uuid_id', 'title', 'episode_number', 'short_description', \
		'long_description', 'credits', 'rating', 'external_ids', 'release_date']
	list_filter = ['episode_number', 'external_ids']
	readonly_fields = ['uuid_id']
	class Meta:
		model = Episode

class ShortFormVideoAdmin(admin.ModelAdmin):
	list_display = ['id', 'title', 'release_date']
	search_fields = ['uuid_id', 'title', 'short_description', \
		'long_description', 'credits', 'rating', 'tags', 'release_date']
	list_filter = ['title', 'tags']
	readonly_fields = ['uuid_id']
	class Meta:
		model = ShortFormVideo

class TVSpecialAdmin(admin.ModelAdmin):
	list_display = ['id', 'title', 'release_date']
	search_fields = ['uuid_id', 'title', 'short_description', 'long_description', \
		'genres', 'rating', 'tags', 'release_date']
	list_filter = ['title', 'genres', 'tags']
	readonly_fields = ['uuid_id']
	class Meta:
		model = TVSpecial

# Roku Content Properties

class ContentAdmin(admin.ModelAdmin):
	list_display = ['id', 'title', 'language', 'date_added']
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

class VideoTypeAdmin(admin.ModelAdmin):
	list_display = ['video_type_short', 'video_type_long']
	search_fields = ['video_type_short', 'video_type_long']
	class Meta:
		model = VideoType

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
	list_display = ['source_name', 'source_long_name', 'source_country', 'source_url']
	search_fields = ['source_name', 'source_long_name']
	list_filter = ['source_name']
	class Meta:
		model = RatingSource

class RatingCountryAdmin(admin.ModelAdmin):
	list_display = ['country_name', 'country_code']
	search_fields = ['country_name', 'country_code']
	class Meta:
		model = RatingCountry

class ParentalRatingAdmin(admin.ModelAdmin):
	list_display = ['parental_rating']
	search_fields = ['parental_rating']
	class Meta:
		model = ParentalRating

class CreditRoleAdmin(admin.ModelAdmin):
	list_display = ['credit_role']
	search_fields = ['credit_role']
	class Meta:
		model = CreditRole

class CreditAdmin(admin.ModelAdmin):
	list_display = ['credit_name', 'role', 'birth_date']
	search_fields = ['credit_name', 'role', 'birth_date']
	list_filter = ['role']
	class Meta:
		model = Credit

class TagAdmin(admin.ModelAdmin):
	list_display = ['tag_name']
	search_fields = ['tag_name']
	class Meta:
		model = Tag

class LanguageAdmin(admin.ModelAdmin):
	list_display = ['language_name_eng', 'code_iso_639_2', 'code_iso_639_1']
	search_fields = ['language_name_eng', 'code_iso_639_2', 'code_iso_639_1']
	class Meta:
		model = Language


# Register with Admin
admin.site.register(RokuContentFeed, RokuContentFeedAdmin)

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
admin.site.register(VideoType, VideoTypeAdmin)
admin.site.register(Caption, CaptionAdmin)
admin.site.register(TrickPlayFile, TrickPlayFileAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(ExternalID, ExternalIDAdmin)
admin.site.register(ExternalIDType, ExternalIDTypeAdmin)
admin.site.register(Rating, RatingAdmin)
admin.site.register(RatingSource, RatingSourceAdmin)
admin.site.register(RatingCountry, RatingCountryAdmin)
admin.site.register(ParentalRating, ParentalRatingAdmin)
admin.site.register(CreditRole, CreditRoleAdmin)
admin.site.register(Credit, CreditAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Language, LanguageAdmin)
