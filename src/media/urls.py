from django.urls import path
from . import views

urlpatterns = [

	# Video
	path('', views.MediaVideoListView.as_view()),
	path('video/', views.MediaVideoListView.as_view(), name='media-video-list'),
	path('video/<int:pk>/', views.MediaVideoDetailView.as_view(), name='media-video-detail'), 
	path('video/edit/<int:pk>/', views.MediaVideoUpdateView.as_view(), name='media-video-update'),
	path('api/video/', views.MediaVideoListAPI.as_view(), name='media-video-list-api'),
	path('api/video/<int:pk>', views.MediaVideoDetailAPI.as_view(), name='media-video-detail-api'),

	# Audio
	path('music/', views.MediaAudioListView.as_view(), name='media-audio-list'),
	path('music/<int:pk>/', views.MediaAudioDetailView.as_view(), name='media-audio-detail'), 
	path('music/edit/<int:pk>/', views.MediaAudioUpdateView.as_view(), name='media-audio-update'),
	path('api/music/', views.MediaAudioListAPI.as_view(), name='media-audio-list-api'),
	path('api/music/<int:pk>', views.MediaAudioDetailAPI.as_view(), name='media-audio-detail-api'),

	# Photo
	# path('photo/<int:pk>', views.MediaPhotoView.as_view(), name='photo')
	path('photos/', views.MediaPhotoListView.as_view(), name='media-photo-list'),
	path('photos/<int:pk>/', views.MediaPhotoDetailView.as_view(), name='media-photo-detail'), 
	path('photos/edit/<int:pk>/', views.MediaPhotoUpdateView.as_view(), name='media-photo-update'),
	path('api/photos/', views.MediaPhotoListAPI.as_view(), name='media-photo-list-api'),
	path('api/photos/<int:pk>', views.MediaPhotoDetailAPI.as_view(), name='media-photo-detail-api'),

]
