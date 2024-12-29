from django.urls import path, re_path
from . import views

urlpatterns = [

	# Upload
	path('upload/', views.MediaUploadView.as_view(), name='upload'),

	# Transcriptions
	#path('transcription/create/', views.TranscriptionCreateView.as_view(), name='transcription-create'),
	#path('transcriptions/', views.TranscriptionListView.as_view(), name='transcription-list'),
	#path('transcription/<int:pk>/', views.TranscriptionDetailView.as_view(), name='transcription-detail'), 
	#path('transcription/edit/<int:pk>/', views.TranscriptionUpdateView.as_view(), name='transcription-update'),

	# Video
	path('media-video/upload/', views.MediaVideoCreateView.as_view(), name='media-video-create'),
	path('media-videos/', views.MediaVideoListView.as_view(), name='media-video-list'),
	path('media-videos/<int:pk>/', views.MediaVideoDetailView.as_view(), name='media-video-detail'), 
	path('media-videos/edit/<int:pk>/', views.MediaVideoUpdateView.as_view(), name='media-video-update'),
	path('api/media-videos/', views.MediaVideoListAPI.as_view(), name='media-video-list-api'),
	path('api/media-videos/genres/', views.MediaVideoGenreListAPI.as_view()),
	path('api/media-videos/search/', views.MediaVideoListAPISearch.as_view()),
	path('api/media-videos/<int:pk>/', views.MediaVideoDetailAPI.as_view(), name='media-video-detail-api'),
	path('media-videos/gallery/', views.MediaVideoGalleryListView.as_view(), name='media-video-list-gallery'),
	path('videos/atom/', views.MediaVideoAtomFeed(), name='video-atom'),
	path('videos/rss/', views.MediaVideoRSSFeed(), name='video-rss'),
	re_path('^api/media-videos/(?P<username>.+)/$', views.MediaVideoListAPI.as_view()),
	re_path('^api/media-videos/(?P<service>.+)/$', views.MediaVideoListAPI.as_view()),
	re_path('^api/media-videos/(?P<orientation>.+)/$', views.MediaVideoListAPI.as_view()),
	re_path('^api/media-videos/(?P<doc_format>.+)/$', views.MediaVideoListAPI.as_view()),
	path('video-service/create/', views.MediaVideoServiceCreateView.as_view(), name='video-service-create'),
	path('video-services/', views.MediaVideoServiceListView.as_view(), name='video-service-list'),
	path('video-service/<int:pk>/', views.MediaVideoServiceDetailView.as_view(), name='video-service-detail'), 
	path('video-service/edit/<int:pk>/', views.MediaVideoServiceUpdateView.as_view(), name='video-service-update'),
	path('api/video-services/', views.MediaVideoServiceListAPI.as_view(), name='video-service-list-api'),
	path('api/video-service/search/', views.MediaVideoServiceListAPISearch.as_view()),
	path('api/video-service/<int:pk>/', views.MediaVideoServiceDetailAPI.as_view(), name='video-service-detail-api'),

	# Photo
	path('media-photo/upload/', views.MediaPhotoCreateView.as_view(), name='media-photo-create'),
	path('photos/', views.MediaPhotoListView.as_view(), name='media-photo-list'),
	path('photos/<int:pk>/', views.MediaPhotoDetailView.as_view(), name='media-photo-detail'), 
	path('photos/edit/<int:pk>/', views.MediaPhotoUpdateView.as_view(), name='media-photo-update'),
	path('api/photos/', views.MediaPhotoListAPI.as_view(), name='media-photo-list-api'),
	path('api/photos/search/', views.MediaPhotoListAPISearch.as_view()),
	path('api/photos/<int:pk>/', views.MediaPhotoDetailAPI.as_view(), name='media-photo-detail-api'),
	path('photos/gallery/', views.MediaPhotoGalleryListView.as_view(), name='media-photo-list-gallery'),
	path('photos/atom/', views.MediaPhotoAtomFeed(), name='photo-atom'),
	path('photos/rss/', views.MediaPhotoRSSFeed(), name='photo-rss'),
	re_path('^api/photos/(?P<username>.+)/$', views.MediaPhotoListAPI.as_view()),
	re_path('^api/photos/(?P<service>.+)/$', views.MediaPhotoListAPI.as_view()),
	re_path('^api/photos/(?P<orientation>.+)/$', views.MediaPhotoListAPI.as_view()),
	path('photo-service/create/', views.MediaPhotoServiceCreateView.as_view(), name='photo-service-create'),
	path('photo-services/', views.MediaPhotoServiceListView.as_view(), name='photo-service-list'),
	path('photo-service/<int:pk>/', views.MediaPhotoServiceDetailView.as_view(), name='photo-service-detail'), 
	path('photo-service/edit/<int:pk>/', views.MediaPhotoServiceUpdateView.as_view(), name='photo-service-update'),
	path('api/photo-services/', views.MediaPhotoServiceListAPI.as_view(), name='photo-service-list-api'),
	path('api/photo-service/search/', views.MediaPhotoServiceListAPISearch.as_view()),
	path('api/photo-service/<int:pk>/', views.MediaPhotoServiceDetailAPI.as_view(), name='photo-service-detail-api'),

	# Audio
	path('media-audio/upload/', views.MediaAudioCreateView.as_view(), name='media-audio-create'),
	path('audio/', views.MediaAudioListView.as_view(), name='media-audio-list'),
	path('audio/<int:pk>/', views.MediaAudioDetailView.as_view(), name='media-audio-detail'), 
	path('audio/edit/<int:pk>/', views.MediaAudioUpdateView.as_view(), name='media-audio-update'),
	path('api/audio/', views.MediaAudioListAPI.as_view(), name='media-audio-list-api'),
	path('api/audio/search/', views.MediaAudioListAPISearch.as_view()),
	path('api/audio/<int:pk>/', views.MediaAudioDetailAPI.as_view(), name='media-audio-detail-api'),
	path('api/audio/artists/', views.MediaAudioListAPIArtists.as_view()),
	path('api/audio/albums/', views.MediaAudioListAPIAlbums.as_view()),
	path('audio/gallery/', views.MediaAudioGalleryListView.as_view(), name='media-audio-list-gallery'),
	path('audio/atom/', views.MediaAudioAtomFeed(), name='audio-atom'),
	path('audio/rss/', views.MediaAudioRSSFeed(), name='audio-rss'),
	#path('audio/delete/<int:pk>/', views.MediaAudioDeleteView.as_view(), name='media-audio-delete'),
	re_path('^api/audio/(?P<title>.+)/$', views.MediaAudioListAPI.as_view()),
	re_path('^api/audio/(?P<artist>.+)/$', views.MediaAudioListAPI.as_view()),
	re_path('^api/audio/(?P<album>.+)/$', views.MediaAudioListAPI.as_view()),
	re_path('^api/audio/(?P<genre>.+)/$', views.MediaAudioListAPI.as_view()),
	re_path('^api/audio/(?P<year>.+)/$', views.MediaAudioListAPI.as_view()),
	path('audio-service/create/', views.MediaAudioServiceCreateView.as_view(), name='audio-service-create'),
	path('audio-services/', views.MediaAudioServiceListView.as_view(), name='audio-service-list'),
	path('audio-service/<int:pk>/', views.MediaAudioServiceDetailView.as_view(), name='audio-service-detail'), 
	path('audio-service/edit/<int:pk>/', views.MediaAudioServiceUpdateView.as_view(), name='audio-service-update'),
	path('api/audio-services/', views.MediaAudioServiceListAPI.as_view(), name='audio-service-list-api'),
	path('api/audio-service/search/', views.MediaAudioServiceListAPISearch.as_view()),
	path('api/audio-service/<int:pk>/', views.MediaAudioServiceDetailAPI.as_view(), name='audio-service-detail-api'),

	# Documents
	path('media-doc/upload/', views.MediaDocCreateView.as_view(), name='media-doc-create'),
	path('docs/', views.MediaDocListView.as_view(), name='media-doc-list'),
	path('docs/<int:pk>/', views.MediaDocDetailView.as_view(), name='media-doc-detail'), 
	path('docs/edit/<int:pk>/', views.MediaDocUpdateView.as_view(), name='media-doc-update'),
	path('api/docs/', views.MediaDocListAPI.as_view(), name='media-doc-list-api'),
	path('api/docs/search/', views.MediaDocListAPISearch.as_view()),
	path('api/docs/<int:pk>/', views.MediaDocDetailAPI.as_view(), name='media-doc-detail-api'),
	re_path('^api/docs/(?P<doc_format>.+)/$', views.MediaDocListAPI.as_view()),
	path('doc-service/create/', views.MediaDocServiceCreateView.as_view(), name='doc-service-create'),
	path('doc-services/', views.MediaDocServiceListView.as_view(), name='doc-service-list'),
	path('doc-service/<int:pk>/', views.MediaDocServiceDetailView.as_view(), name='doc-service-detail'), 
	path('doc-service/edit/<int:pk>/', views.MediaDocServiceUpdateView.as_view(), name='doc-service-update'),
	path('api/doc-services/', views.MediaDocServiceListAPI.as_view(), name='doc-service-list-api'),
	path('api/doc-service/search/', views.MediaDocServiceListAPISearch.as_view()),
	path('api/doc-service/<int:pk>/', views.MediaDocServiceDetailAPI.as_view(), name='doc-service-detail-api'),
	path('docs/atom/', views.MediaDocAtomFeed(), name='doc-atom'),
	path('docs/rss/', views.MediaDocRSSFeed(), name='doc-rss'),
	
	# Tags
	path('tag/create/', views.MediaTagCreateView.as_view(), name='media-tag-create'),
	path('tag/', views.MediaTagListView.as_view(), name='media-tag-list'),
	path('tag/<int:pk>/', views.MediaTagDetailView.as_view(), name='media-tag-detail'),
	path('tag/edit/<int:pk>/', views.MediaTagUpdateView.as_view(), name='media-tag-update'),
	path('api/tag/', views.MediaTagListAPI.as_view(), name='media-tag-list-api'),

	# Categories
	path('category/create/', views.MediaCategoryCreateView.as_view(), name='media-category-create'),
	path('category/', views.MediaCategoryListView.as_view(), name='media-category-list'),
	path('category/<int:pk>/', views.MediaCategoryDetailView.as_view(), name='media-category-detail'),
	path('category/edit/<int:pk>/', views.MediaCategoryUpdateView.as_view(), name='media-category-update'),
	path('api/category/', views.MediaCategoryListAPI.as_view(), name='media-category-list-api'),
	
# 	# Settings
# 	path('settings/', views.SettingsUpdateView.as_view(), name='settings-update'),
#

]
