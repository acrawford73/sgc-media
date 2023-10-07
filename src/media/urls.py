from django.urls import path, re_path
from . import views

urlpatterns = [

	# Upload
	path('upload/', views.MediaUploadView.as_view(), name='upload'),

	# Video
	path('video/upload/', views.MediaVideoCreateView.as_view(), name='media-video-create'),
	path('', views.MediaVideoListView.as_view()),
	path('videos/', views.MediaVideoListView.as_view(), name='media-video-list'),
	path('videos/<int:pk>/', views.MediaVideoDetailView.as_view(), name='media-video-detail'), 
	path('videos/edit/<int:pk>/', views.MediaVideoUpdateView.as_view(), name='media-video-update'),
	path('api/videos/', views.MediaVideoListAPI.as_view(), name='media-video-list-api'),
	path('api/videos/genres/', views.MediaVideoGenreListAPI.as_view()),
	path('api/videos/search/', views.MediaVideoListAPISearch.as_view()),
	path('api/videos/<int:pk>', views.MediaVideoDetailAPI.as_view(), name='media-video-detail-api'),
	path('videos/gallery/', views.MediaVideoGalleryListView.as_view(), name='media-video-list-gallery'),
	path('videos/atom/', views.MediaVideoAtomFeed()),
	path('videos/rss/', views.MediaVideoRSSFeed()),
	re_path('^api/videos/(?P<username>.+)/$', views.MediaVideoListAPI.as_view()),
	re_path('^api/videos/(?P<service>.+)/$', views.MediaVideoListAPI.as_view()),
	re_path('^api/videos/(?P<orientation>.+)/$', views.MediaVideoListAPI.as_view()),
	re_path('^api/videos/(?P<doc_format>.+)/$', views.MediaVideoListAPI.as_view()),

	# Photo
	path('photos/', views.MediaPhotoListView.as_view(), name='media-photo-list'),
	path('photos/<int:pk>/', views.MediaPhotoDetailView.as_view(), name='media-photo-detail'), 
	path('photos/edit/<int:pk>/', views.MediaPhotoUpdateView.as_view(), name='media-photo-update'),
	path('api/photos/', views.MediaPhotoListAPI.as_view(), name='media-photo-list-api'),
	path('api/photos/search/', views.MediaPhotoListAPISearch.as_view()),
	path('api/photos/<int:pk>', views.MediaPhotoDetailAPI.as_view(), name='media-photo-detail-api'),
	path('photos/gallery/', views.MediaPhotoGalleryListView.as_view(), name='media-photo-list-gallery'),
	re_path('^api/photos/(?P<username>.+)/$', views.MediaPhotoListAPI.as_view()),
	re_path('^api/photos/(?P<service>.+)/$', views.MediaPhotoListAPI.as_view()),
	re_path('^api/photos/(?P<orientation>.+)/$', views.MediaPhotoListAPI.as_view()),

	# Audio
	path('audio/', views.MediaAudioListView.as_view(), name='media-audio-list'),
	path('audio/<int:pk>/', views.MediaAudioDetailView.as_view(), name='media-audio-detail'), 
	path('audio/edit/<int:pk>/', views.MediaAudioUpdateView.as_view(), name='media-audio-update'),
	path('api/audio/', views.MediaAudioListAPI.as_view(), name='media-audio-list-api'),
	path('api/audio/search/', views.MediaAudioListAPISearch.as_view()),
	path('api/audio/<int:pk>', views.MediaAudioDetailAPI.as_view(), name='media-audio-detail-api'),
	path('api/audio/artists/', views.MediaAudioListAPIArtists.as_view()),
	path('api/audio/albums/', views.MediaAudioListAPIAlbums.as_view()),
	path('audio/gallery/', views.MediaAudioGalleryListView.as_view(), name='media-audio-list-gallery'),
	#path('audio/delete/<int:pk>/', views.MediaAudioDeleteView.as_view(), name='media-audio-delete'),
	re_path('^api/audio/(?P<title>.+)/$', views.MediaAudioListAPI.as_view()),
	re_path('^api/audio/(?P<artist>.+)/$', views.MediaAudioListAPI.as_view()),
	re_path('^api/audio/(?P<album>.+)/$', views.MediaAudioListAPI.as_view()),
	re_path('^api/audio/(?P<genre>.+)/$', views.MediaAudioListAPI.as_view()),
	re_path('^api/audio/(?P<year>.+)/$', views.MediaAudioListAPI.as_view()),

	# Documents
	path('docs/', views.MediaDocListView.as_view(), name='media-doc-list'),
	path('docs/<int:pk>/', views.MediaDocDetailView.as_view(), name='media-doc-detail'), 
	path('docs/edit/<int:pk>/', views.MediaDocUpdateView.as_view(), name='media-doc-update'),
	path('api/docs/', views.MediaDocListAPI.as_view(), name='media-doc-list-api'),
	path('api/docs/search/', views.MediaDocListAPISearch.as_view()),
	path('api/docs/<int:pk>', views.MediaDocDetailAPI.as_view(), name='media-doc-detail-api'),
	re_path('^api/docs/(?P<doc_format>.+)/$', views.MediaDocListAPI.as_view()),



# 	# Settings
# 	path('settings/', views.SettingsUpdateView.as_view(), name='settings-update'),
#

]
