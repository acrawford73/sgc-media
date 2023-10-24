from django.urls import path, re_path
from . import views

urlpatterns = [

	## Roku Support

	# Roku Content Feed
	path('roku-content-feed/create/', views.RokuContentFeedCreateView.as_view(), name='rokucontentfeed-create'),
	path('roku-content-feed/', views.RokuContentFeedListView.as_view(), name='rokucontentfeed-list'),
	path('roku-content-feed/<int:pk>/', views.RokuContentFeedDetailView.as_view(), name='rokucontentfeed-detail'),
	path('roku-content-feed/edit/<int:pk>/', views.RokuContentFeedUpdateView.as_view(), name='rokucontentfeed-update'),
	path('api/roku-content-feed/', views.RokuContentFeedListAPI.as_view(), name='rokucontentfeed-api'),

	# Roku Search Feed
	# path('roku-search-feed/create/', views.RokuSearchFeedCreateView.as_view(), name='rokusearchfeed-create'),
	# path('roku-search-feed/', views.RokuSearchFeedListView.as_view(), name='rokusearchfeed-list'),
	# path('roku-search-feed/<int:pk>/', views.RokuSearchFeedDetailView.as_view(), name='rokusearchfeed-detail'),
	# path('roku-search-feed/edit/<int:pk>/', views.RokuSearchFeedUpdateView.as_view(), name='rokusearchfeed-update'),
	# path('api/roku-search-feed/', views.RokuSearchFeedAPI.as_view(), name='rokusearchfeed-api'),

	# Language
	path('language/create/', views.LanguageCreateView.as_view(), name='language-create'),
	path('languages/', views.LanguageListView.as_view(), name='language-list'),
	path('language/<int:pk>/', views.LanguageDetailView.as_view(), name='language-detail'),
	path('language/edit/<int:pk>/', views.LanguageUpdateView.as_view(), name='language-update'),
	path('api/languages/', views.LanguageListAPI.as_view(), name='language-api'),
	
	# Category
	path('category/create/', views.CategoryCreateView.as_view(), name='category-create'),
	path('categories/', views.CategoryListView.as_view(), name='category-list'),
	path('category/<int:pk>/', views.CategoryDetailView.as_view(), name='category-detail'),
	path('category/edit/<int:pk>/', views.CategoryUpdateView.as_view(), name='category-update'),
	path('api/categories/', views.CategoryListAPI.as_view(), name='category-api'),
	# path('api/category/search/', views.CategoryAPISearch.as_view()),
	# path('api/category/<int:pk>', views.CategoryDetailAPI.as_view(), name='category-detail-api'),
	
	# Playlist
	path('playlist/create/', views.PlaylistCreateView.as_view(), name='playlist-create'),
	path('playlists/', views.PlaylistListView.as_view(), name='playlist-list'),
	path('playlist/<int:pk>/', views.PlaylistDetailView.as_view(), name='playlist-detail'),
	path('playlist/edit/<int:pk>/', views.PlaylistUpdateView.as_view(), name='playlist-update'),
	path('api/playlists/', views.PlaylistListAPI.as_view(), name='playlist-api'),
	# path('api/playlist/search/', views.PlaylistAPISearch.as_view()),
	# path('api/playlist/<int:pk>', views.PlaylistDetailAPI.as_view(), name='playlist-detail-api'),
	
	# Movie
	path('movie/create/', views.MovieCreateView.as_view(), name='movie-create'),
	path('movies/', views.MovieListView.as_view(), name='movie-list'),
	path('movie/<int:pk>/', views.MovieDetailView.as_view(), name='movie-detail'),
	path('movie/edit/<int:pk>/', views.MovieUpdateView.as_view(), name='movie-update'),
	path('api/movies/', views.MovieListAPI.as_view(), name='movie-api'),
	# path('api/movie/<int:pk>', views.MovieDetailAPI.as_view(), name='movie-detail-api'),
	
	# LiveFeed
	path('livefeed/create/', views.LiveFeedCreateView.as_view(), name='livefeed-create'),
	path('livefeeds/', views.LiveFeedListView.as_view(), name='livefeed-list'),
	path('livefeed/<int:pk>/', views.LiveFeedDetailView.as_view(), name='livefeed-detail'),
	path('livefeed/edit/<int:pk>/', views.LiveFeedUpdateView.as_view(), name='livefeed-update'),
	path('api/livefeeds/', views.LiveFeedListAPI.as_view(), name='livefeed-api'),
	# path('api/livefeed/<int:pk>', views.LiveFeedDetailAPI.as_view(), name='livefeed-detail-api'),
	
	# Series
	path('series/create/', views.SeriesCreateView.as_view(), name='series-create'),
	path('series/', views.SeriesListView.as_view(), name='series-list'),
	path('series/<int:pk>/', views.SeriesDetailView.as_view(), name='series-detail'),
	path('series/edit/<int:pk>/', views.SeriesUpdateView.as_view(), name='series-update'),
	path('api/series/', views.SeriesListAPI.as_view(), name='series-api'),
	# path('api/series/<int:pk>', views.SeriesDetailAPI.as_view(), name='series-detail-api'),
	
	# Season
	path('season/create/', views.SeasonCreateView.as_view(), name='season-create'),
	path('seasons/', views.SeasonListView.as_view(), name='season-list'),
	path('season/<int:pk>/', views.SeasonDetailView.as_view(), name='season-detail'),
	path('season/edit/<int:pk>/', views.SeasonUpdateView.as_view(), name='season-update'),
	path('api/seasons/', views.SeasonListAPI.as_view(), name='season-api'),
	# path('apepisodei/season/<int:pk>', views.SeasonDetailAPI.as_view(), name='season-detail-api'),
	
	# Episode
	path('episode/create/', views.EpisodeCreateView.as_view(), name='episode-create'),
	path('episodes/', views.EpisodeListView.as_view(), name='episode-list'),
	path('episode/<int:pk>/', views.EpisodeDetailView.as_view(), name='episode-detail'),
	path('episode/edit/<int:pk>/', views.EpisodeUpdateView.as_view(), name='episode-update'),
	path('api/episodes/', views.EpisodeListAPI.as_view(), name='episode-api'),
	# path('api/episode/<int:pk>', views.EpisodeDetailAPI.as_view(), name='episode-detail-api'),
	
	# ShortFormVideo
	path('shortformvideo/create/', views.ShortFormVideoCreateView.as_view(), name='shortformvideo-create'),
	path('shortformvideos/', views.ShortFormVideoListView.as_view(), name='shortformvideo-list'),
	path('shortformvideo/<int:pk>/', views.ShortFormVideoDetailView.as_view(), name='shortformvideo-detail'),
	path('shortformvideo/edit/<int:pk>/', views.ShortFormVideoUpdateView.as_view(), name='shortformvideo-update'),
	path('api/shortformvideos/', views.ShortFormVideoListAPI.as_view(), name='shortformvideo-api'),
	# path('api/shortformvideo/<int:pk>', views.ShortFormVideoDetailAPI.as_view(), name='shortformvideo-detail-api'),
	
	# TVSpecial
	path('tvspecial/create/', views.TVSpecialCreateView.as_view(), name='tvspecial-create'),
	path('tvspecials/', views.TVSpecialListView.as_view(), name='tvspecial-list'),
	path('tvspecial/<int:pk>/', views.TVSpecialDetailView.as_view(), name='tvspecial-detail'),
	path('tvspecial/edit/<int:pk>/', views.TVSpecialUpdateView.as_view(), name='tvspecial-update'),
	path('api/tvspecials/', views.TVSpecialListAPI.as_view(), name='tvspecial-api'),
	# path('api/tvspecial/<int:pk>', views.TVSpecialDetailAPI.as_view(), name='tvspecial-detail-api'),
	
	# Content
	path('content/create/', views.ContentCreateView.as_view(), name='content-create'),
	path('content/', views.ContentListView.as_view(), name='content-list'),
	path('content/<int:pk>/', views.ContentDetailView.as_view(), name='content-detail'),
	path('content/edit/<int:pk>/', views.ContentUpdateView.as_view(), name='content-update'),
	path('api/content/', views.ContentListAPI.as_view(), name='content-api'),
	# path('api/content/<int:pk>', views.ContentDetailAPI.as_view(), name='content-detail-api'),
	
	# Video
	path('video/create/', views.VideoCreateView.as_view(), name='video-create'),
	path('videos/', views.VideoListView.as_view(), name='video-list'),
	path('video/<int:pk>/', views.VideoDetailView.as_view(), name='video-detail'),
	path('video/edit/<int:pk>/', views.VideoUpdateView.as_view(), name='video-update'),
	path('api/videos/', views.VideoListAPI.as_view(), name='video-api'),
	# path('api/video/<int:pk>', views.VideoDetailAPI.as_view(), name='video-detail-api'),
	
	# Caption
	path('caption/create/', views.CaptionCreateView.as_view(), name='caption-create'),
	path('captions/', views.CaptionListView.as_view(), name='caption-list'),
	path('caption/<int:pk>/', views.CaptionDetailView.as_view(), name='caption-detail'),
	path('caption/edit/<int:pk>/', views.CaptionUpdateView.as_view(), name='caption-update'),
	path('api/captions/', views.CaptionListAPI.as_view(), name='caption-api'),
	# path('api/caption/<int:pk>', views.CaptionDetailAPI.as_view(), name='caption-detail-api'),
	
	# TrickPlayFile
	path('trickplayfile/create/', views.TrickPlayFileCreateView.as_view(), name='trickplayfile-create'),
	path('trickplayfiles/', views.TrickPlayFileListView.as_view(), name='trickplayfile-list'),
	path('trickplayfile/<int:pk>/', views.TrickPlayFileDetailView.as_view(), name='trickplayfile-detail'),
	path('trickplayfile/edit/<int:pk>/', views.TrickPlayFileUpdateView.as_view(), name='trickplayfile-update'),
	path('api/trickplayfiles/', views.TrickPlayFileListAPI.as_view(), name='trickplayfile-api'),
	# path('api/trickplayfile/<int:pk>', views.TrickPlayFileDetailAPI.as_view(), name='trickplayfile-detail-api'),
	
	# Genre
	path('genre/create/', views.GenreCreateView.as_view(), name='genre-create'),
	path('genres/', views.GenreListView.as_view(), name='genre-list'),
	path('genre/<int:pk>/', views.GenreDetailView.as_view(), name='genre-detail'),
	path('genre/edit/<int:pk>/', views.GenreUpdateView.as_view(), name='genre-update'),
	path('api/genres/', views.GenreListAPI.as_view(), name='genre-api'),
	# path('api/genre/<int:pk>', views.GenreDetailAPI.as_view(), name='genre-detail-api'),
	
	# ExternalID
	path('externalid/create/', views.ExternalIDCreateView.as_view(), name='externalid-create'),
	path('externalids/', views.ExternalIDListView.as_view(), name='externalid-list'),
	path('externalid/<int:pk>/', views.ExternalIDDetailView.as_view(), name='externalid-detail'),
	path('externalid/edit/<int:pk>/', views.ExternalIDUpdateView.as_view(), name='externalid-update'),
	path('api/externalids/', views.ExternalIDListAPI.as_view(), name='externalid-api'),
	# path('api/externalid/<int:pk>', views.ExternalIDDetailAPI.as_view(), name='externalid-detail-api'),
	
	# Rating
	path('rating/create/', views.RatingCreateView.as_view(), name='rating-create'),
	path('ratings/', views.RatingListView.as_view(), name='rating-list'),
	path('rating/<int:pk>/', views.RatingDetailView.as_view(), name='rating-detail'),
	path('rating/edit/<int:pk>/', views.RatingUpdateView.as_view(), name='rating-update'),
	path('api/ratings/', views.RatingListAPI.as_view(), name='rating-api'),
	# path('api/rating/<int:pk>', views.RatingDetailAPI.as_view(), name='rating-detail-api'),
	
	# RatingSource
	path('ratingsource/create/', views.RatingSourceCreateView.as_view(), name='ratingsource-create'),
	path('ratingsources/', views.RatingSourceListView.as_view(), name='ratingsource-list'),
	path('ratingsource/<int:pk>/', views.RatingSourceDetailView.as_view(), name='ratingsource-detail'),
	path('ratingsource/edit/<int:pk>/', views.RatingSourceUpdateView.as_view(), name='ratingsource-update'),
	path('api/ratingsources/', views.RatingSourceListAPI.as_view(), name='ratingsource-api'),
	# path('api/ratingsource/<int:pk>', views.RatingSourceDetailAPI.as_view(), name='ratingsource-detail-api'),
	
	# ParentalRating
	path('parentalrating/create/', views.ParentalRatingCreateView.as_view(), name='parentalrating-create'),
	path('parentalratings/', views.ParentalRatingListView.as_view(), name='parentalrating-list'),
	path('parentalrating/<int:pk>/', views.ParentalRatingDetailView.as_view(), name='parentalrating-detail'),
	path('parentalrating/edit/<int:pk>/', views.ParentalRatingUpdateView.as_view(), name='parentalrating-update'),
	path('api/parentalratings/', views.ParentalRatingListAPI.as_view(), name='parentalrating-api'),
	# path('api/parentalrating/<int:pk>', views.ParentalRatingDetailAPI.as_view(), name='parentalrating-detail-api'),
	
	# Credit
	path('credit/create/', views.CreditCreateView.as_view(), name='credit-create'),
	path('credits/', views.CreditListView.as_view(), name='credit-list'),
	path('credit/<int:pk>/', views.CreditDetailView.as_view(), name='credit-detail'),
	path('credit/edit/<int:pk>/', views.CreditUpdateView.as_view(), name='credit-update'),
	path('api/credits/', views.CreditListAPI.as_view(), name='credit-api'),
	# path('api/credit/<int:pk>', views.CreditDetailAPI.as_view(), name='credit-detail-api'),

	# Tags
	path('tag/create/', views.TagCreateView.as_view(), name='tag-create'),
	path('tags/', views.TagListView.as_view(), name='tag-list'),
	path('tag/<int:pk>/', views.TagDetailView.as_view(), name='tag-detail'),
	path('tag/edit/<int:pk>/', views.TagUpdateView.as_view(), name='tag-update'),
	path('api/tags/', views.TagListAPI.as_view(), name='tag-api'),
	
]