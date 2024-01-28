"""
URL configuration for sgc project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include,path
from django.conf import settings


urlpatterns = [

    #Apps
    path('', include('roku_content.urls')),
    #path('', include('roku_search.urls')),
    path('', include('media.urls')),
    path('', include('core.urls')),
    #path('', include('core.system_config')),

    path('account/', include('django.contrib.auth.urls')),
    ## The URLs supported by auth are:
    # accounts/login/ [name='login']
    # accounts/logout/ [name='logout']
    # accounts/password_change/ [name='password_change']
    # accounts/password_change/done/ [name='password_change_done']
    # accounts/password_reset/ [name='password_reset']
    # accounts/password_reset/done/ [name='password_reset_done']
    # accounts/reset/<uidb64>/<token>/ [name='password_reset_confirm']
    # accounts/reset/done/ [name='password_reset_complete']

    # Admin
    path('admin/docs/', include('django.contrib.admindocs.urls')),
    path('admin/', admin.site.urls),

]

# Development
if settings.DEBUG:
    
    from django.conf.urls.static import static
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# else:
#     # Production
#     urlpatterns += staticfiles_urlpatterns()


# Serve the favicon
# urlpatterns += [
#     path('favicon.ico', serve, {
#             'path': 'favicon.ico',
#             'document_root': os.path.join(BASE_DIR, 'home/static/img'),
#         }
#     ),
# ]