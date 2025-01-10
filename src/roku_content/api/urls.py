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
        title="Roku Content API",
        default_version="v1",
        description="API for Roku Content",
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


    ### Roku Content API
    #path('api/roku-content-feed/', views.RokuContentFeedListAPI.as_view(), name='rokucontentfeed-api'),
    #path('api/roku-content-feed/search/', views.RokuContentFeedListSearchAPI.as_view()),
    #re_path('api/roku-content-feed/search/(?P<language>.+)/$', views.RokuContentFeedListSearchAPI.as_view()),
    path('api/rcf/<int:pk>/', views.RokuContentFeedDetailAPI.as_view(), name='rokucontentfeed-detail-api'),
    #re_path('^api/roku-content-feed/(?P<language>.+)/$', views.RokuContentFeedListAPI.as_view()),

    # path('roku-search-feed/create/', views.RokuSearchFeedCreateView.as_view(), name='rokusearchfeed-create'),
    # path('roku-search-feed/', views.RokuSearchFeedListView.as_view(), name='rokusearchfeed-list'),
    # path('roku-search-feed/<int:pk>/', views.RokuSearchFeedDetailView.as_view(), name='rokusearchfeed-detail'),
    # path('roku-search-feed/edit/<int:pk>/', views.RokuSearchFeedUpdateView.as_view(), name='rokusearchfeed-update'),
    # path('api/roku-search-feed/', views.RokuSearchFeedAPI.as_view(), name='rokusearchfeed-api'),

    path('api/languages/', views.LanguageListAPI.as_view(), name='language-api'),

    path('api/categories/', views.CategoryListAPI.as_view(), name='category-api'),
    # path('api/category/search/', views.CategoryAPISearch.as_view()),
    # path('api/category/<int:pk>', views.CategoryDetailAPI.as_view(), name='category-detail-api'),

    path('api/playlists/', views.PlaylistListAPI.as_view(), name='playlist-api'),
    # path('api/playlist/search/', views.PlaylistAPISearch.as_view()),
    # path('api/playlist/<int:pk>', views.PlaylistDetailAPI.as_view(), name='playlist-detail-api'),

    path('api/movies/', views.MovieListAPI.as_view(), name='movie-api'),
    # path('api/movie/<int:pk>', views.MovieDetailAPI.as_view(), name='movie-detail-api'),

    path('api/livefeeds/', views.LiveFeedListAPI.as_view(), name='livefeed-api'),
    # path('api/livefeed/<int:pk>', views.LiveFeedDetailAPI.as_view(), name='livefeed-detail-api'),

    path('api/series/', views.SeriesListAPI.as_view(), name='series-api'),
    # path('api/series/<int:pk>', views.SeriesDetailAPI.as_view(), name='series-detail-api'),

    path('api/seasons/', views.SeasonListAPI.as_view(), name='season-api'),
    # path('api/season/<int:pk>', views.SeasonDetailAPI.as_view(), name='season-detail-api'),

    path('api/episodes/', views.EpisodeListAPI.as_view(), name='episode-api'),
    # path('api/episode/<int:pk>', views.EpisodeDetailAPI.as_view(), name='episode-detail-api'),

    path('api/shortformvideos/', views.ShortFormVideoListAPI.as_view(), name='shortformvideo-api'),
    # path('api/shortformvideo/<int:pk>', views.ShortFormVideoDetailAPI.as_view(), name='shortformvideo-detail-api'),

    path('api/tvspecials/', views.TVSpecialListAPI.as_view(), name='tvspecial-api'),
    # path('api/tvspecial/<int:pk>', views.TVSpecialDetailAPI.as_view(), name='tvspecial-detail-api'),

    path('api/content/', views.ContentListAPI.as_view(), name='content-api'),
    # path('api/content/<int:pk>', views.ContentDetailAPI.as_view(), name='content-detail-api'),

    path('api/videos/', views.VideoListAPI.as_view(), name='video-api'),
    # path('api/video/<int:pk>', views.VideoDetailAPI.as_view(), name='video-detail-api'),

    path('api/captions/', views.CaptionListAPI.as_view(), name='caption-api'),
    # path('api/caption/<int:pk>', views.CaptionDetailAPI.as_view(), name='caption-detail-api'),

    path('api/trickplayfiles/', views.TrickPlayFileListAPI.as_view(), name='trickplayfile-api'),
    # path('api/trickplayfile/<int:pk>', views.TrickPlayFileDetailAPI.as_view(), name='trickplayfile-detail-api'),

    path('api/genres/', views.GenreListAPI.as_view(), name='genre-api'),
    # path('api/genre/<int:pk>', views.GenreDetailAPI.as_view(), name='genre-detail-api'),

    path('api/externalids/', views.ExternalIDListAPI.as_view(), name='externalid-api'),
    # path('api/externalid/<int:pk>', views.ExternalIDDetailAPI.as_view(), name='externalid-detail-api'),

    path('api/ratings/', views.RatingListAPI.as_view(), name='rating-api'),
    # path('api/rating/<int:pk>', views.RatingDetailAPI.as_view(), name='rating-detail-api'),

    path('api/rating-sources/', views.RatingSourceListAPI.as_view(), name='ratingsource-api'),
    # path('api/ratingsource/<int:pk>', views.RatingSourceDetailAPI.as_view(), name='ratingsource-detail-api'),

    path('api/rating-countries/', views.RatingCountryListAPI.as_view(), name='rating-countries-api'),

    path('api/parental-ratings/', views.ParentalRatingListAPI.as_view(), name='parentalrating-api'),
    # path('api/parentalrating/<int:pk>', views.ParentalRatingDetailAPI.as_view(), name='parentalrating-detail-api'),

    path('api/credit-roles/', views.CreditRoleListAPI.as_view(), name='creditrole-api'),

    path('api/credits/', views.CreditListAPI.as_view(), name='credit-api'),

    path('api/tags/', views.TagListAPI.as_view(), name='tag-api'),

]

### NOTE:
# This code avoids using ending '/' on a URL
# It causes issues with swagger and routers so don't use it
# urlpatterns = format_suffix_patterns(urlpatterns)
