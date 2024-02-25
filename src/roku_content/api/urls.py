# from django.urls import path, include, re_path
# from rest_framework.urlpatterns import format_suffix_patterns
# from roku_content.api.views import 
# from rest_framework.authtoken import views
# from rest_framework.routers import DefaultRouter
# from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
# from drf_yasg import openapi
# from drf_yasg.views import get_schema_view
# import os

# router = DefaultRouter()
# router.register("tags", TagViewSet)
# router.register("posts", PostViewSet)


# schema_view = get_schema_view(
#     openapi.Info(
#         title="Blango API",
#         default_version="v1",
#         description="API for Blango Blog",
#     ),
#     url=f"https://{os.environ.get('CODIO_HOSTNAME')}-8000.codio.io/api/v1/",
#     public=True,
# )

# urlpatterns = [

#     # disabled after PostViewSet was added
#     #path("posts/", PostList.as_view(), name="api_post_list"),
#     #path("posts/<int:pk>", PostDetail.as_view(), name="api_post_detail"),
#     path("users/<str:email>", UserDetail.as_view(), name="api_user_detail"),
# ]

# # Authentication
# urlpatterns += [
#     path("auth/", include("rest_framework.urls")),
#     path("token-auth/", views.obtain_auth_token),
#     path("jwt/", TokenObtainPairView.as_view(), name="jwt_obtain_pair"),
#     path("jwt/refresh/", TokenRefreshView.as_view(), name="jwt_refresh"),
#     # this re_path doesn't work
#     # re_path(
#     #     r"^swagger(?P<format>\.json|\.yaml)$",
#     #     schema_view.without_ui(cache_timeout=0),
#     #     name="schema-json",
#     # ),
#     path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui",),
#     path("", include(router.urls)),
#     path("posts/by-time/<str:period_name>/", PostViewSet.as_view({"get": "list"}), name="posts-by-time",),

# ]

# # Avoids using ending '/' on a URL
# #urlpatterns = format_suffix_patterns(urlpatterns)
# # ^ this causes issues with swagger and routers