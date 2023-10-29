from django.urls import path, re_path
from . import views

urlpatterns = [

	# Roku Search Feed

	path('search-feed/create/', views.SearchFeedCreateView.as_view(), name='searchfeed-create'),
	path('search-feed/', views.SearchFeedListView.as_view(), name='searchfeed-list'),
	path('search-feed/<int:pk>/', views.SearchFeedDetailView.as_view(), name='searchfeed-detail'),
	path('search-feed/edit/<int:pk>/', views.SearchFeedUpdateView.as_view(), name='searchfeed-update'),
	#path('api/search-feed/', views.RokuSearchFeedAPI.as_view(), name='rokusearchfeed-api'),
	path('api/search-feed/<uuid:pk>', views.SearchFeedDetailAPI.as_view(), name='searchfeed-detail-api'),
	#path('api/search-feed/<uuid:search_feed_id>', views.SearchFeedDetailAPI.as_view(), name='searchfeed-detail-api'),
	#re_path('^api/search-feed/(?P<search_feed_id>.+)/$', views.SearchFeedDetailAPI.as_view()),

]
#http://192.168.0.13:8000/api/search-feed/b6ebc29d-ca40-4b07-acc3-60d96c9de345/