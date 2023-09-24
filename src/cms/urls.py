from django.urls import path, re_path
from . import views

urlpatterns = [

	# Playlists
	path('playlist/', views.PlaylistListView.as_view(), name='playlist-list'),
	path('playlist/<int:pk>/', views.PlaylistDetailView.as_view(), name='playlist-detail'), 
	path('playlist/edit/<int:pk>/', views.PlaylistUpdateView.as_view(), name='playlist-update'),
	path('api/playlist/', views.PlaylistAPI.as_view(), name='playlist-api'),
	path('api/playlist/search/', views.PlaylistAPISearch.as_view()),
	path('api/playlist/<int:pk>', views.PlaylistDetailAPI.as_view(), name='playlist-detail-api'),
	#re_path('^api/playlist/(?P<username>.+)/$', views.PlaylistAPI.as_view()),
	#re_path('^api/playlist/(?P<service>.+)/$', views.PlaylistAPI.as_view()),
	#re_path('^api/playlist/(?P<orientation>.+)/$', views.PlaylistAPI.as_view()),

]