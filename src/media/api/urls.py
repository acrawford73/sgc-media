from . import views
from django.urls import path, include, re_path
#from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.authtoken import views as authtoken_views
# from rest_framework.routers import DefaultRouter
# from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
import os
from sgc import settings

# router = DefaultRouter()
# router.register("tags", TagViewSet)
# router.register("posts", PostViewSet)


schema_view = get_schema_view(
    openapi.Info(
        title="Content API",
        default_version="v1",
        description="API for Media Content",
    ),
    url=f"http://{settings.INTERNAL_IPS[0]}:8000/api/",
    public=True,
)

urlpatterns = [

    path('auth/', include('rest_framework.urls')),
    path('token-auth/', authtoken_views.obtain_auth_token),
    #path("jwt/", TokenObtainPairView.as_view(), name="jwt_obtain_pair"),
    #path("jwt/refresh/", TokenRefreshView.as_view(), name="jwt_refresh"),

    # Enable this for Swagger browsable API
    # path('api/swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

    #path("", include(router.urls)),
    #path("posts/by-time/<str:period_name>/", PostViewSet.as_view({"get": "list"}), name="posts-by-time",),

    # Video
    path('api/media-videos/', views.MediaVideoListAPI.as_view(), name='media-video-list-api'),
    path('api/media-videos/genres/', views.MediaVideoGenreListAPI.as_view()),
    path('api/media-videos/search/', views.MediaVideoListAPISearch.as_view()),
    path('api/media-videos/<int:pk>/', views.MediaVideoDetailAPI.as_view(), name='media-video-detail-api'),
    re_path('^api/media-videos/(?P<username>.+)/$', views.MediaVideoListAPI.as_view()),
    re_path('^api/media-videos/(?P<service>.+)/$', views.MediaVideoListAPI.as_view()),
    re_path('^api/media-videos/(?P<orientation>.+)/$', views.MediaVideoListAPI.as_view()),
    re_path('^api/media-videos/(?P<doc_format>.+)/$', views.MediaVideoListAPI.as_view()),
    path('api/video-services/', views.MediaVideoServiceListAPI.as_view(), name='video-service-list-api'),
    path('api/video-service/search/', views.MediaVideoServiceListAPISearch.as_view()),
    path('api/video-service/<int:pk>/', views.MediaVideoServiceDetailAPI.as_view(), name='video-service-detail-api'),

    # Audio
    path('api/audio/', views.MediaAudioListAPI.as_view(), name='media-audio-list-api'),
    path('api/audio/search/', views.MediaAudioListAPISearch.as_view(), name='media-audio-search-api'),
    path('api/audio/<int:pk>/', views.MediaAudioDetailAPI.as_view(), name='media-audio-detail-api'),
    path('api/audio/artists/', views.MediaAudioListAPIArtists.as_view(), name='media-audio-artists-api'),
    path('api/audio/albums/', views.MediaAudioListAPIAlbums.as_view(), name='media-audio-albums-api'),
    re_path('^api/audio/(?P<title>.+)/$', views.MediaAudioListAPI.as_view()),
    re_path('^api/audio/(?P<artist>.+)/$', views.MediaAudioListAPI.as_view()),
    re_path('^api/audio/(?P<album>.+)/$', views.MediaAudioListAPI.as_view()),
    re_path('^api/audio/(?P<genre>.+)/$', views.MediaAudioListAPI.as_view()),
    re_path('^api/audio/(?P<year>.+)/$', views.MediaAudioListAPI.as_view()),
    path('api/audio-services/', views.MediaAudioServiceListAPI.as_view(), name='audio-service-list-api'),
    path('api/audio-service/search/', views.MediaAudioServiceListAPISearch.as_view()),
    path('api/audio-service/<int:pk>/', views.MediaAudioServiceDetailAPI.as_view(), name='audio-service-detail-api'),

    # Photo
    path('api/photos/', views.MediaPhotoListAPI.as_view(), name='media-photo-list-api'),
    path('api/photos/search/', views.MediaPhotoListAPISearch.as_view()),
    path('api/photos/<int:pk>/', views.MediaPhotoDetailAPI.as_view(), name='media-photo-detail-api'),
    re_path('^api/photos/(?P<username>.+)/$', views.MediaPhotoListAPI.as_view()),
    re_path('^api/photos/(?P<service>.+)/$', views.MediaPhotoListAPI.as_view()),
    re_path('^api/photos/(?P<orientation>.+)/$', views.MediaPhotoListAPI.as_view()),
    path('api/photo-services/', views.MediaPhotoServiceListAPI.as_view(), name='photo-service-list-api'),
    path('api/photo-service/search/', views.MediaPhotoServiceListAPISearch.as_view()),
    path('api/photo-service/<int:pk>/', views.MediaPhotoServiceDetailAPI.as_view(), name='photo-service-detail-api'),

    # Documents
    path('api/docs/', views.MediaDocListAPI.as_view(), name='media-doc-list-api'),
    path('api/docs/search/', views.MediaDocListAPISearch.as_view()),
    path('api/docs/<int:pk>/', views.MediaDocDetailAPI.as_view(), name='media-doc-detail-api'),
    re_path('^api/docs/(?P<doc_format>.+)/$', views.MediaDocListAPI.as_view()),
    path('api/doc-services/', views.MediaDocServiceListAPI.as_view(), name='doc-service-list-api'),
    path('api/doc-service/search/', views.MediaDocServiceListAPISearch.as_view()),
    path('api/doc-service/<int:pk>/', views.MediaDocServiceDetailAPI.as_view(), name='doc-service-detail-api'),

    # Tags
    path('api/tag/', views.MediaTagListAPI.as_view(), name='media-tag-list-api'),

    # Categories
    path('api/category/', views.MediaCategoryListAPI.as_view(), name='media-category-list-api'),

]

### NOTE:
# This code avoids using ending '/' on a URL
# It causes issues with swagger and routers so don't use it
# urlpatterns = format_suffix_patterns(urlpatterns)
