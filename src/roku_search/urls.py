from django.urls import path, re_path
from . import views

urlpatterns = [

	# Roku Search Feed

	path('roku-search-feed/', views.RokuSearchFeedListView.as_view(), name='rokusearchfeed-list'),
	path('roku-search-feed/<int:pk>/', views.RokuSearchFeedDetailView.as_view(), name='rokusearchfeed-detail'),
	path('roku-search-feed/edit/<int:pk>/', views.RokuSearchFeedUpdateView.as_view(), name='rokusearchfeed-update'),
	path('api/roku-search-feed/', views.RokuSearchFeedAPI.as_view(), name='rokusearchfeed-api'),
	# #path('api/roku-search-feed/search/', views.RokuSearchFeedAPISearch.as_view()),
	# #path('api/roku-search-feed/<int:pk>', views.RokuSearchFeedDetailAPI.as_view(), name='rokusearchfeed-detail-api'),

]