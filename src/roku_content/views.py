from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
### Templates
from django.views.generic import TemplateView, CreateView, ListView, DetailView, UpdateView
### Models
## Roku Content Feeds, Categories, Types, Properties
from .models import RokuContentFeed
from .models import Language, Category, Playlist
from .models import Movie, LiveFeed, Series, Season, Episode, ShortFormVideo, TVSpecial
from .models import Content, Video, Caption, TrickPlayFile, Genre, ExternalID
from .models import Rating, RatingSource, RatingCountry, ParentalRating, CreditRole, Credit, Tag

## Roku Feeds

# Roku Content Feed
class RokuContentFeedCreateView(LoginRequiredMixin, CreateView):
	"""
	Roku Content Feed fields for CreateView :model:`roku_content.RokuContentFeed`.

	**Context**

	``rokucontentfeed``
		An instance of :model:`roku_content.RokuContentFeed``.

	**Template:**

	:template:`roku_content/rokucontentfeed_create.html`
	"""
	model = RokuContentFeed
	fields = ['is_public', 'short_description', 'provider_name', 'language', 'rating', \
		'categories', 'playlists', 'movies', 'live_feeds', 'series', 'short_form_videos', 'tv_specials']

class RokuContentFeedListView(LoginRequiredMixin, ListView):
	"""
	Roku Content Feed fields for ListView :model:`roku_content.RokuContentFeed`.

	**Context**

	``rokucontentfeed``
		An instance of :model:`roku_content.RokuContentFeed``.

	**Template:**

	:template:`roku_content/rokucontentfeed_list.html`
	"""
	model = RokuContentFeed
	template_name = 'roku_content/rokucontentfeed_list.html'  #<app>/<model>_<viewtype>.html
	context_object_name = 'rokucontentfeed'
	ordering = ['id']
	#paginate_by = 15

class RokuContentFeedDetailView(LoginRequiredMixin, DetailView):
	"""
	Roku Content Feed fields for DetailView :model:`roku_content.RokuContentFeed`.

	**Context**

	``rokucontentfeed``
		An instance of :model:`roku_content.RokuContentFeed``.

	**Template:**

	:template:`roku_content/rokucontentfeed_detail.html`
	"""
	model = RokuContentFeed
	context_object_name = 'rokucontentfeed'

class RokuContentFeedUpdateView(LoginRequiredMixin, UpdateView):
	"""
	Roku Content Feed fields for UpdateView :model:`roku_content.RokuContentFeed`.

	**Context**

	``rokucontentfeed``
		An instance of :model:`roku_content.RokuContentFeed``.

	**Template:**

	:template:`roku_content/rokucontentfeed_form.html`
	"""
	model = RokuContentFeed
	context_object_name = 'rokucontentfeed'
	fields = ['is_public', 'short_description', 'provider_name', 'language', 'rating', \
		'categories', 'playlists', 'movies', 'live_feeds', 'series', 'short_form_videos', 'tv_specials']


## Roku Content Categories

# Language
class LanguageCreateView(LoginRequiredMixin, CreateView):
	model = Language
	fields = ['language_name_eng', 'code_iso_639_2', 'code_iso_639_1']

class LanguageListView(LoginRequiredMixin, ListView):
	model = Language
	template_name = 'roku_content/language_list.html'  #<app>/<model>_<viewtype>.html
	context_object_name = 'language'
	ordering = ['id']
	paginate_by = 15

class LanguageDetailView(LoginRequiredMixin, DetailView):
	model = Language
	context_object_name = 'language'

class LanguageUpdateView(LoginRequiredMixin, UpdateView):
	model = Language
	context_object_name = 'language'
	fields = ['language_name_eng', 'code_iso_639_2', 'code_iso_639_1']


# Category
class CategoryCreateView(LoginRequiredMixin, CreateView):
	model = Category
	fields = ['category_name', 'playlist_name', 'query_string', 'order']

class CategoryListView(LoginRequiredMixin, ListView):
	model = Category
	template_name = 'roku_content/category_list.html'  #<app>/<model>_<viewtype>.html
	context_object_name = 'category'
	ordering = ['-id']
	paginate_by = 15

class CategoryDetailView(LoginRequiredMixin, DetailView):
	model = Category
	context_object_name = 'category'

class CategoryUpdateView(LoginRequiredMixin, UpdateView):
	model = Category
	context_object_name = 'category'
	fields = ['category_name', 'playlist_name', 'query_string', 'order']


# Playlist
class PlaylistCreateView(LoginRequiredMixin, CreateView):
	model = Playlist
	fields = ['playlist_name', 'short_description', 'item_ids']

class PlaylistListView(LoginRequiredMixin, ListView):
	model = Playlist
	template_name = 'roku_content/playlist_list.html'  #<app>/<model>_<viewtype>.html
	context_object_name = 'playlist'
	ordering = ['-id']
	paginate_by = 15

class PlaylistDetailView(LoginRequiredMixin, DetailView):
	model = Playlist
	context_object_name = 'playlist'

class PlaylistUpdateView(LoginRequiredMixin, UpdateView):
	model = Playlist
	context_object_name = 'playlist'
	fields = ['playlist_name', 'short_description', 'item_ids']


## Roku Content Types

# Movie
class MovieCreateView(LoginRequiredMixin, CreateView):
	model = Movie
	fields = ['title', 'short_description', 'long_description', 'content', \
		'thumbnail', 'release_date', 'genres', 'rating', 'tags', 'credits', 'external_ids']

class MovieListView(LoginRequiredMixin, ListView):
	model = Movie
	template_name = 'roku_content/movie_list.html'  #<app>/<model>_<viewtype>.html
	context_object_name = 'movie'
	ordering = ['-id']
	paginate_by = 15

class MovieDetailView(LoginRequiredMixin, DetailView):
	model = Movie
	context_object_name = 'movie'

class MovieUpdateView(LoginRequiredMixin, UpdateView):
	model = Movie
	context_object_name = 'movie'
	fields = ['title', 'short_description', 'long_description', 'content', \
		'thumbnail', 'release_date', 'genres', 'rating', 'tags', 'credits', 'external_ids']


# LiveFeed
class LiveFeedCreateView(LoginRequiredMixin, CreateView):
	model = LiveFeed
	fields = ['title', 'short_description', 'long_description', 'content', \
		'thumbnail', 'branded_thumbnail', 'tags', 'rating', 'genres']

class LiveFeedListView(LoginRequiredMixin, ListView):
	model = LiveFeed
	template_name = 'roku_content/livefeed_list.html'  #<app>/<model>_<viewtype>.html
	context_object_name = 'livefeed'
	ordering = ['-id']
	paginate_by = 15

class LiveFeedDetailView(LoginRequiredMixin, DetailView):
	model = LiveFeed
	context_object_name = 'livefeed'

class LiveFeedUpdateView(LoginRequiredMixin, UpdateView):
	model = LiveFeed
	context_object_name = 'livefeed'
	fields = ['title', 'short_description', 'long_description', 'content', \
		'thumbnail', 'branded_thumbnail', 'tags', 'rating', 'genres']


# Series
class SeriesCreateView(LoginRequiredMixin, CreateView):
	model = Series
	fields = ['title', 'short_description', 'long_description', 'seasons', 'episodes', \
		'thumbnail', 'release_date', 'genres', 'tags', 'credits', 'external_ids']

class SeriesListView(LoginRequiredMixin, ListView):
	model = Series
	template_name = 'roku_content/series_list.html'  #<app>/<model>_<viewtype>.html
	context_object_name = 'series'
	ordering = ['-id']
	paginate_by = 15

class SeriesDetailView(LoginRequiredMixin, DetailView):
	model = Series
	context_object_name = 'series'

class SeriesUpdateView(LoginRequiredMixin, UpdateView):
	model = Series
	context_object_name = 'series'
	fields = ['title', 'short_description', 'long_description', 'seasons', 'episodes', \
		'thumbnail', 'release_date', 'genres', 'tags', 'credits', 'external_ids']


# Season
class SeasonCreateView(LoginRequiredMixin, CreateView):
	model = Season
	fields = ['title_season', 'season_number', 'episodes']

class SeasonListView(LoginRequiredMixin, ListView):
	model = Season
	template_name = 'roku_content/season_list.html'  #<app>/<model>_<viewtype>.html
	context_object_name = 'season'
	ordering = ['-id']
	paginate_by = 15

class SeasonDetailView(LoginRequiredMixin, DetailView):
	model = Season
	context_object_name = 'season'

class SeasonUpdateView(LoginRequiredMixin, UpdateView):
	model = Season
	context_object_name = 'season'
	fields = ['title_season', 'season_number', 'episodes']


# Episode
class EpisodeCreateView(LoginRequiredMixin, CreateView):
	model = Episode
	fields = ['episode_number', 'title', 'short_description', 'long_description', \
		'content', 'thumbnail', 'release_date', 'rating', 'credits', 'external_ids']

class EpisodeListView(LoginRequiredMixin, ListView):
	model = Episode
	template_name = 'roku_content/episode_list.html'  #<app>/<model>_<viewtype>.html
	context_object_name = 'episode'
	ordering = ['title']
	paginate_by = 15

class EpisodeDetailView(LoginRequiredMixin, DetailView):
	model = Episode
	context_object_name = 'episode'

class EpisodeUpdateView(LoginRequiredMixin, UpdateView):
	model = Episode
	context_object_name = 'episode'
	fields = ['episode_number', 'title', 'short_description', 'long_description', \
		'content', 'thumbnail', 'release_date', 'rating', 'credits', 'external_ids']


# ShortFormVideo
class ShortFormVideoCreateView(LoginRequiredMixin, CreateView):
	model = ShortFormVideo
	fields = ['title', 'short_description', 'long_description', 'content', 'thumbnail', \
		'release_date', 'tags', 'genres', 'rating', 'credits']

class ShortFormVideoListView(LoginRequiredMixin, ListView):
	model = ShortFormVideo
	template_name = 'roku_content/shortformvideo_list.html'  #<app>/<model>_<viewtype>.html
	context_object_name = 'shortformvideo'
	ordering = ['-id']
	paginate_by = 15

class ShortFormVideoDetailView(LoginRequiredMixin, DetailView):
	model = ShortFormVideo
	context_object_name = 'shortformvideo'

class ShortFormVideoUpdateView(LoginRequiredMixin, UpdateView):
	model = ShortFormVideo
	context_object_name = 'shortformvideo'
	fields = ['title', 'short_description', 'long_description', 'content', 'thumbnail', \
		'release_date', 'tags', 'genres', 'rating', 'credits']


# TVSpecial
class TVSpecialCreateView(LoginRequiredMixin, CreateView):
	model = TVSpecial
	fields = ['title', 'short_description', 'long_description', 'content', \
		'thumbnail', 'genres', 'rating', 'tags', 'release_date', 'credits', 'external_ids']

class TVSpecialListView(LoginRequiredMixin, ListView):
	model = TVSpecial
	template_name = 'roku_content/tvspecial_list.html'  #<app>/<model>_<viewtype>.html
	context_object_name = 'tvspecial'
	ordering = ['-id']
	paginate_by = 15

class TVSpecialDetailView(LoginRequiredMixin, DetailView):
	model = TVSpecial
	context_object_name = 'tvspecial'

class TVSpecialUpdateView(LoginRequiredMixin, UpdateView):
	model = TVSpecial
	context_object_name = 'tvspecial'
	fields = ['title', 'short_description', 'long_description', 'content', \
		'thumbnail', 'genres', 'rating', 'tags', 'release_date', 'credits', 'external_ids']


## Roku ContentPoperties

# Content
class ContentCreateView(LoginRequiredMixin, CreateView):
	model = Content
	fields = ['title', 'language', 'duration', 'videos', 'captions', 'trick_play_files', \
		 'validity_start_period', 'validity_end_period']

class ContentListView(LoginRequiredMixin, ListView):
	model = Content
	template_name = 'roku_content/content_list.html'  #<app>/<model>_<viewtype>.html
	context_object_name = 'content'
	ordering = ['-id']
	paginate_by = 15

class ContentDetailView(LoginRequiredMixin, DetailView):
	model = Content
	context_object_name = 'content'

class ContentUpdateView(LoginRequiredMixin, UpdateView):
	model = Content
	context_object_name = 'content'
	fields = ['title', 'language', 'duration', 'videos', 'captions', 'trick_play_files', \
		 'validity_start_period', 'validity_end_period']


# Video
class VideoCreateView(LoginRequiredMixin, CreateView):
	model = Video
	fields = ['url', 'quality', 'video_type']

class VideoListView(LoginRequiredMixin, ListView):
	model = Video
	template_name = 'roku_content/video_list.html'  #<app>/<model>_<viewtype>.html
	context_object_name = 'video'
	ordering = ['-id']
	paginate_by = 15

class VideoDetailView(LoginRequiredMixin, DetailView):
	model = Video
	context_object_name = 'video'

class VideoUpdateView(LoginRequiredMixin, UpdateView):
	model = Video
	context_object_name = 'video'
	fields = ['url', 'quality', 'video_type']


# Caption
class CaptionCreateView(LoginRequiredMixin, CreateView):
	model = Caption
	fields = ['url', 'language', 'caption_type']

class CaptionListView(LoginRequiredMixin, ListView):
	model = Caption
	template_name = 'roku_content/caption_list.html'  #<app>/<model>_<viewtype>.html
	context_object_name = 'caption'
	ordering = ['-id']
	paginate_by = 15

class CaptionDetailView(LoginRequiredMixin, DetailView):
	model = Caption
	context_object_name = 'caption'

class CaptionUpdateView(LoginRequiredMixin, UpdateView):
	model = Caption
	context_object_name = 'caption'
	fields = ['url', 'language', 'caption_type']


# TrickPlayFile
class TrickPlayFileCreateView(LoginRequiredMixin, CreateView):
	model = TrickPlayFile
	fields = ['url', 'quality']

class TrickPlayFileListView(LoginRequiredMixin, ListView):
	model = TrickPlayFile
	template_name = 'roku_content/trickplayfile_list.html'  #<app>/<model>_<viewtype>.html
	context_object_name = 'trickplayfile'
	ordering = ['-id']
	paginate_by = 15

class TrickPlayFileDetailView(LoginRequiredMixin, DetailView):
	model = TrickPlayFile
	context_object_name = 'trickplayfile'

class TrickPlayFileUpdateView(LoginRequiredMixin, UpdateView):
	model = TrickPlayFile
	context_object_name = 'trickplayfile'
	fields = ['url', 'quality']


# Genre
class GenreCreateView(LoginRequiredMixin, CreateView):
	model = Genre
	fields = ['genre']

class GenreListView(LoginRequiredMixin, ListView):
	model = Genre
	template_name = 'roku_content/genre_list.html'  #<app>/<model>_<viewtype>.html
	context_object_name = 'genre'
	ordering = ['genre']
	paginate_by = 15

class GenreDetailView(LoginRequiredMixin, DetailView):
	model = Genre
	context_object_name = 'genre'

class GenreUpdateView(LoginRequiredMixin, UpdateView):
	model = Genre
	context_object_name = 'genre'
	fields = ['genre']


# ExternalID
class ExternalIDCreateView(LoginRequiredMixin, CreateView):
	model = ExternalID
	fields = ['external_id', 'id_type']

class ExternalIDListView(LoginRequiredMixin, ListView):
	model = ExternalID
	template_name = 'roku_content/externalid_list.html'  #<app>/<model>_<viewtype>.html
	context_object_name = 'externalid'
	ordering = ['external_id']
	paginate_by = 15

class ExternalIDDetailView(LoginRequiredMixin, DetailView):
	model = ExternalID
	context_object_name = 'externalid'

class ExternalIDUpdateView(LoginRequiredMixin, UpdateView):
	model = ExternalID
	context_object_name = 'externalid'
	fields = ['external_id', 'id_type']


# Rating
class RatingCreateView(LoginRequiredMixin, CreateView):
	model = Rating
	fields = ['rating', 'rating_source']

class RatingListView(LoginRequiredMixin, ListView):
	model = Rating
	template_name = 'roku_content/rating_list.html'  #<app>/<model>_<viewtype>.html
	context_object_name = 'rating'
	ordering = ['rating_source', 'rating']
	#paginate_by = 15

class RatingDetailView(LoginRequiredMixin, DetailView):
	model = Rating
	context_object_name = 'rating'

class RatingUpdateView(LoginRequiredMixin, UpdateView):
	model = Rating
	context_object_name = 'rating'
	fields = ['rating', 'rating_source']


# RatingSource
class RatingSourceCreateView(LoginRequiredMixin, CreateView):
	model = RatingSource
	fields = ['source_name', 'source_long_name', 'source_country', 'source_url']

class RatingSourceListView(LoginRequiredMixin, ListView):
	model = RatingSource
	template_name = 'roku_content/ratingsource_list.html'  #<app>/<model>_<viewtype>.html
	context_object_name = 'ratingsource'
	ordering = ['source_name']
	#paginate_by = 15

class RatingSourceDetailView(LoginRequiredMixin, DetailView):
	model = RatingSource
	context_object_name = 'ratingsource'

class RatingSourceUpdateView(LoginRequiredMixin, UpdateView):
	model = RatingSource
	context_object_name = 'ratingsource'
	fields = ['source_name', 'source_long_name', 'source_country', 'source_url']


# ParentalRating
class ParentalRatingCreateView(LoginRequiredMixin, CreateView):
	model = ParentalRating
	fields = ['parental_rating']

class ParentalRatingListView(LoginRequiredMixin, ListView):
	model = ParentalRating
	template_name = 'roku_content/parentalrating_list.html'  #<app>/<model>_<viewtype>.html
	context_object_name = 'parentalrating'
	ordering = ['parental_rating']
	#paginate_by = 15

class ParentalRatingDetailView(LoginRequiredMixin, DetailView):
	model = ParentalRating
	context_object_name = 'parentalrating'

class ParentalRatingUpdateView(LoginRequiredMixin, UpdateView):
	model = ParentalRating
	context_object_name = 'parentalrating'
	fields = ['parental_rating']


# Credit Role
class CreditRoleCreateView(LoginRequiredMixin, CreateView):
	model = CreditRole
	fields = ['credit_role']

class CreditRoleListView(LoginRequiredMixin, ListView):
	model = CreditRole
	template_name = 'roku_content/creditrole_list.html'  #<app>/<model>_<viewtype>.html
	context_object_name = 'creditrole'
	ordering = ['credit_role']
	#paginate_by = 15

class CreditRoleDetailView(LoginRequiredMixin, DetailView):
	model = CreditRole
	context_object_name = 'creditrole'

class CreditRoleUpdateView(LoginRequiredMixin, UpdateView):
	model = CreditRole
	context_object_name = 'creditrole'
	fields = ['credit_role']


# Credit
class CreditCreateView(LoginRequiredMixin, CreateView):
	model = Credit
	fields = ['credit_name', 'role', 'birth_date']

class CreditListView(LoginRequiredMixin, ListView):
	model = Credit
	template_name = 'roku_content/credit_list.html'  #<app>/<model>_<viewtype>.html
	context_object_name = 'credit'
	ordering = ['credit_name']
	#paginate_by = 15

class CreditDetailView(LoginRequiredMixin, DetailView):
	model = Credit
	context_object_name = 'credit'

class CreditUpdateView(LoginRequiredMixin, UpdateView):
	model = Credit
	context_object_name = 'credit'
	fields = ['credit_name', 'role', 'birth_date']


# Tags

class TagCreateView(LoginRequiredMixin, CreateView):
	model = Tag
	fields = ['tag_name']

class TagListView(LoginRequiredMixin, ListView):
	model = Tag
	template_name = 'roku_content/tag_list.html'  #<app>/<model>_<viewtype>.html
	context_object_name = 'tag'
	ordering = ['tag_name']

class TagDetailView(LoginRequiredMixin, DetailView):
	model = Tag
	context_object_name = 'tag'

class TagUpdateView(LoginRequiredMixin, UpdateView):
	model = Tag
	context_object_name = 'tag'
	fields = ['tag_name']
