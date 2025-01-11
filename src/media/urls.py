from django.urls import path, re_path
from . import views

urlpatterns = [

	path('', views.MediaVideoListView.as_view()),
	
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
	path('media-videos/gallery/', views.MediaVideoGalleryListView.as_view(), name='media-video-list-gallery'),
	path('videos/atom/', views.MediaVideoAtomFeed(), name='video-atom'),
	path('videos/rss/', views.MediaVideoRSSFeed(), name='video-rss'),
	path('video-service/create/', views.MediaVideoServiceCreateView.as_view(), name='video-service-create'),
	path('video-services/', views.MediaVideoServiceListView.as_view(), name='video-service-list'),
	path('video-service/<int:pk>/', views.MediaVideoServiceDetailView.as_view(), name='video-service-detail'), 
	path('video-service/edit/<int:pk>/', views.MediaVideoServiceUpdateView.as_view(), name='video-service-update'),

	# Photo
	path('media-photo/upload/', views.MediaPhotoCreateView.as_view(), name='media-photo-create'),
	path('photos/', views.MediaPhotoListView.as_view(), name='media-photo-list'),
	path('photos/<int:pk>/', views.MediaPhotoDetailView.as_view(), name='media-photo-detail'), 
	path('photos/edit/<int:pk>/', views.MediaPhotoUpdateView.as_view(), name='media-photo-update'),
	path('photos/gallery/', views.MediaPhotoGalleryListView.as_view(), name='media-photo-list-gallery'),
	path('photos/atom/', views.MediaPhotoAtomFeed(), name='photo-atom'),
	path('photos/rss/', views.MediaPhotoRSSFeed(), name='photo-rss'),
	path('photo-service/create/', views.MediaPhotoServiceCreateView.as_view(), name='photo-service-create'),
	path('photo-services/', views.MediaPhotoServiceListView.as_view(), name='photo-service-list'),
	path('photo-service/<int:pk>/', views.MediaPhotoServiceDetailView.as_view(), name='photo-service-detail'), 
	path('photo-service/edit/<int:pk>/', views.MediaPhotoServiceUpdateView.as_view(), name='photo-service-update'),

	# Audio
	path('media-audio/upload/', views.MediaAudioCreateView.as_view(), name='media-audio-create'),
	path('audio/', views.MediaAudioListView.as_view(), name='media-audio-list'),
	path('audio/<int:pk>/', views.MediaAudioDetailView.as_view(), name='media-audio-detail'), 
	path('audio/edit/<int:pk>/', views.MediaAudioUpdateView.as_view(), name='media-audio-update'),
	path('audio/gallery/', views.MediaAudioGalleryListView.as_view(), name='media-audio-list-gallery'),
	path('audio/atom/', views.MediaAudioAtomFeed(), name='audio-atom'),
	path('audio/rss/', views.MediaAudioRSSFeed(), name='audio-rss'),
	#path('audio/delete/<int:pk>/', views.MediaAudioDeleteView.as_view(), name='media-audio-delete'),
	path('audio-service/create/', views.MediaAudioServiceCreateView.as_view(), name='audio-service-create'),
	path('audio-services/', views.MediaAudioServiceListView.as_view(), name='audio-service-list'),
	path('audio-service/<int:pk>/', views.MediaAudioServiceDetailView.as_view(), name='audio-service-detail'), 
	path('audio-service/edit/<int:pk>/', views.MediaAudioServiceUpdateView.as_view(), name='audio-service-update'),

	# Documents
	path('media-doc/upload/', views.MediaDocCreateView.as_view(), name='media-doc-create'),
	path('docs/', views.MediaDocListView.as_view(), name='media-doc-list'),
	path('docs/<int:pk>/', views.MediaDocDetailView.as_view(), name='media-doc-detail'), 
	path('docs/edit/<int:pk>/', views.MediaDocUpdateView.as_view(), name='media-doc-update'),
	path('doc-service/create/', views.MediaDocServiceCreateView.as_view(), name='doc-service-create'),
	path('doc-services/', views.MediaDocServiceListView.as_view(), name='doc-service-list'),
	path('doc-service/<int:pk>/', views.MediaDocServiceDetailView.as_view(), name='doc-service-detail'), 
	path('doc-service/edit/<int:pk>/', views.MediaDocServiceUpdateView.as_view(), name='doc-service-update'),
	path('docs/atom/', views.MediaDocAtomFeed(), name='doc-atom'),
	path('docs/rss/', views.MediaDocRSSFeed(), name='doc-rss'),
	
	# Tags
	path('tag/create/', views.MediaTagCreateView.as_view(), name='media-tag-create'),
	path('tag/', views.MediaTagListView.as_view(), name='media-tag-list'),
	path('tag/<int:pk>/', views.MediaTagDetailView.as_view(), name='media-tag-detail'),
	path('tag/edit/<int:pk>/', views.MediaTagUpdateView.as_view(), name='media-tag-update'),

	# Categories
	path('category/create/', views.MediaCategoryCreateView.as_view(), name='media-category-create'),
	path('category/', views.MediaCategoryListView.as_view(), name='media-category-list'),
	path('category/<int:pk>/', views.MediaCategoryDetailView.as_view(), name='media-category-detail'),
	path('category/edit/<int:pk>/', views.MediaCategoryUpdateView.as_view(), name='media-category-update'),
	
# 	# Settings
# 	path('settings/', views.SettingsUpdateView.as_view(), name='settings-update'),
#

]
