import logging
logger = logging.getLogger(__name__)

from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy

### Rest Framework
from rest_framework.response import Response
from rest_framework.reverse import reverse, reverse_lazy
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import filters
from rest_framework.renderers import JSONRenderer
from django_filters.rest_framework import DjangoFilterBackend

### Models
from media.models import MediaVideo, MediaAudio, MediaPhoto, MediaDoc, MediaVideoGenre
from media.models import MediaVideoService, MediaAudioService, MediaPhotoService, MediaDocService
from media.models import MediaTag, MediaCategory

### Serializers
from .serializers import MediaVideoSerializerList, MediaVideoServiceSerializerList, MediaVideoSerializerDetail, MediaVideoServiceSerializerDetail,  MediaVideoGenreSerializerList
from .serializers import MediaAudioSerializerList, MediaAudioServiceSerializerList, MediaAudioSerializerDetail,MediaAudioServiceSerializerDetail
from .serializers import MediaPhotoSerializerList,MediaPhotoServiceSerializerList, MediaPhotoSerializerDetail, MediaPhotoServiceSerializerDetail
from .serializers import MediaDocSerializerList, MediaDocServiceSerializerList, MediaDocSerializerDetail, MediaDocServiceSerializerDetail
from .serializers import MediaTagSerializerList, MediaCategorySerializerList
from .serializers import MediaAudioSerializerListArtists, MediaAudioSerializerListAlbums



# Video

class MediaVideoListAPI(generics.ListAPIView):
	queryset = MediaVideo.objects.all().filter(is_public=True)
	serializer_class = MediaVideoSerializerList
	filter_backends = [DjangoFilterBackend]
	filterset_fields = ['service', 'orientation', 'category', 'service_source']
	ordering_fields = ['id', 'created']
	ordering = ['-id']

class MediaVideoListAPISearch(generics.ListAPIView):
	queryset = MediaVideo.objects.all().filter(is_public=True)
	serializer_class = MediaVideoSerializerList
	filter_backends = [filters.SearchFilter]
	search_fields = ['title', 'short_description', 'long_description', \
		'service', 'orientation', 'username', '@tags', 'location_name', \
		'location_city', 'location_state', 'location_country']
	ordering_fields = ['id', 'created']
	ordering = ['-id']

class MediaVideoGenreListAPI(generics.ListAPIView):
	queryset = MediaVideoGenre.objects.all()
	serializer_class = MediaVideoGenreSerializerList
	filter_backends = [DjangoFilterBackend]
	filterset_fields = ['genre']

class MediaVideoDetailAPI(generics.RetrieveAPIView):
	queryset = MediaVideo.objects.all().filter(is_public=True)
	serializer_class = MediaVideoSerializerDetail

class MediaVideoServiceListAPI(generics.ListAPIView):
	queryset = MediaVideoService.objects.all()
	serializer_class = MediaVideoServiceSerializerList
	filter_backends = [DjangoFilterBackend]
	filterset_fields = ['service_source']
	ordering_fields = ['id', 'service_source']
	ordering = ['-id']

class MediaVideoServiceListAPISearch(generics.ListAPIView):
	queryset = MediaVideoService.objects.all()
	serializer_class = MediaVideoServiceSerializerList
	filter_backends = [filters.SearchFilter]
	search_fields = ['service_source'] 
	ordering_fields = ['id', 'service_source']
	ordering = ['service_source']

class MediaVideoServiceDetailAPI(generics.RetrieveAPIView):
	queryset = MediaVideoService.objects.all()
	serializer_class = MediaVideoServiceSerializerDetail


# Audio

class MediaAudioListAPI(generics.ListAPIView):
	queryset = MediaAudio.objects.all().filter(is_public=True)
	serializer_class = MediaAudioSerializerList
	filter_backends = [DjangoFilterBackend]
	filterset_fields = ['service', 'artist', 'album', 'album_artist', 'composer', 'genre', 'year']
	ordering_fields = ['id', 'created']
	ordering = ['-id']

class MediaAudioListAPIArtists(generics.ListAPIView):
	queryset = MediaAudio.objects.order_by("artist").distinct("artist").filter(is_public=True)
	serializer_class = MediaAudioSerializerListArtists
	filter_backends = [DjangoFilterBackend]
	filterset_fields = ['artist']

class MediaAudioListAPIAlbums(generics.ListAPIView):
	queryset = MediaAudio.objects.order_by("album").distinct("album").filter(is_public=True)
	serializer_class = MediaAudioSerializerListAlbums
	filter_backends = [DjangoFilterBackend]
	filterset_fields = ['album']

class MediaAudioListAPISearch(generics.ListAPIView):
	queryset = MediaAudio.objects.all().filter(is_public=True)
	serializer_class = MediaAudioSerializerList
	filter_backends = [filters.SearchFilter]
	search_fields = ['title', 'artist', 'album', 'genre', 'year', 'service', '@tags']
	ordering_fields = ['id', 'created']
	ordering = ['-id']

class MediaAudioDetailAPI(generics.RetrieveAPIView):
	queryset = MediaAudio.objects.all()
	serializer_class = MediaAudioSerializerDetail

class MediaAudioServiceListAPI(generics.ListAPIView):
	queryset = MediaAudioService.objects.all()
	serializer_class = MediaAudioServiceSerializerList
	filter_backends = [DjangoFilterBackend]
	filterset_fields = ['service_source']
	ordering_fields = ['id', 'service_source']
	ordering = ['-id']

class MediaAudioServiceListAPISearch(generics.ListAPIView):
	queryset = MediaAudioService.objects.all()
	serializer_class = MediaAudioServiceSerializerList
	filter_backends = [filters.SearchFilter]
	search_fields = ['service_source'] 
	ordering_fields = ['id', 'service_source']
	ordering = ['service_source']

class MediaAudioServiceDetailAPI(generics.RetrieveAPIView):
	queryset = MediaAudioService.objects.all()
	serializer_class = MediaAudioServiceSerializerDetail


# Photo

class MediaPhotoListAPI(generics.ListAPIView):
	queryset = MediaPhoto.objects.all().filter(is_public=True)
	serializer_class = MediaPhotoSerializerList
	filter_backends = [DjangoFilterBackend]
	filterset_fields = ['service', 'orientation', 'username']
	ordering_fields = ['id', 'created']
	ordering = ['-id']

class MediaPhotoListAPISearch(generics.ListAPIView):
	queryset = MediaPhoto.objects.all().filter(is_public=True)
	serializer_class = MediaPhotoSerializerList
	filter_backends = [filters.SearchFilter]
	search_fields = ['title', 'short_description', 'long_description', 'service', 'orientation', 'photo_format', 'username', '@tags', 'location_name', 'location_city', 'location_state', 'location_country']
	ordering_fields = ['id', 'created']
	ordering = ['-id']

class MediaPhotoDetailAPI(generics.RetrieveAPIView):
	queryset = MediaPhoto.objects.all()
	serializer_class = MediaPhotoSerializerDetail

class MediaPhotoServiceListAPI(generics.ListAPIView):
	queryset = MediaPhotoService.objects.all()
	serializer_class = MediaPhotoServiceSerializerList
	filter_backends = [DjangoFilterBackend]
	filterset_fields = ['service_source']
	ordering_fields = ['id', 'service_source']
	ordering = ['-id']

class MediaPhotoServiceListAPISearch(generics.ListAPIView):
	queryset = MediaPhotoService.objects.all()
	serializer_class = MediaPhotoServiceSerializerList
	filter_backends = [filters.SearchFilter]
	search_fields = ['service_source'] 
	ordering_fields = ['id', 'service_source']
	ordering = ['service_source']

class MediaPhotoServiceDetailAPI(generics.RetrieveAPIView):
	queryset = MediaPhotoService.objects.all()
	serializer_class = MediaPhotoServiceSerializerDetail


# Documents

class MediaDocListAPI(generics.ListAPIView):
	queryset = MediaDoc.objects.all().filter(is_public=True)
	serializer_class = MediaDocSerializerList
	filter_backends = [DjangoFilterBackend]
	filterset_fields = ['service', 'keywords', 'publication', 'doc_format']
	ordering_fields = ['id', 'created']
	ordering = ['-id']

class MediaDocListAPISearch(generics.ListAPIView):
	queryset = MediaDoc.objects.all().filter(is_public=True)
	serializer_class = MediaDocSerializerList
	filter_backends = [filters.SearchFilter]
	search_fields = ['title', 'short_description', 'long_description', 'abstract', 'notes', 'doc_format', \
		'publications', 'authors', 'keywords', '@tags'] 
	ordering_fields = ['id', 'created']
	ordering = ['-id']

class MediaDocDetailAPI(generics.RetrieveAPIView):
	queryset = MediaDoc.objects.all()
	serializer_class = MediaDocSerializerDetail

class MediaDocServiceListAPI(generics.ListAPIView):
	queryset = MediaDocService.objects.all()
	serializer_class = MediaDocServiceSerializerList
	filter_backends = [DjangoFilterBackend]
	filterset_fields = ['service_source']
	ordering_fields = ['id', 'service_source']
	ordering = ['-id']

class MediaDocServiceListAPISearch(generics.ListAPIView):
	queryset = MediaDocService.objects.all()
	serializer_class = MediaDocServiceSerializerList
	filter_backends = [filters.SearchFilter]
	search_fields = ['service_source'] 
	ordering_fields = ['id', 'service_source']
	ordering = ['service_source']

class MediaDocServiceDetailAPI(generics.RetrieveAPIView):
	queryset = MediaDocService.objects.all()
	serializer_class = MediaDocServiceSerializerDetail

# Tags

class MediaTagListAPI(generics.ListAPIView):
	queryset = MediaTag.objects.all()
	serializer_class = MediaTagSerializerList
	filter_backends = [DjangoFilterBackend]
	filterset_fields = ['tag_name']
	ordering_fields = ['id', 'tag_name']
	ordering = ['tag_name']

class MediaTagListAPISearch(generics.ListAPIView):
	queryset = MediaTag.objects.all()
	serializer_class = MediaTagSerializerList
	filter_backends = [filters.SearchFilter]
	search_fields = ['tag_name'] 
	ordering_fields = ['id', 'tag_name']
	ordering = ['tag_name']


# Category

class MediaCategoryListAPI(generics.ListAPIView):
	queryset = MediaCategory.objects.all()
	serializer_class = MediaCategorySerializerList
	filter_backends = [DjangoFilterBackend]
	filterset_fields = ['category']
	ordering_fields = ['id', 'category']
	ordering = ['category']

# ---------------------------------------------------------------

### HTTP Status Codes
### https://www.django-rest-framework.org/api-guide/status-codes/

# Informational - 1xx
# This class of status code indicates a provisional response. 
# There are no 1xx status codes used in REST framework by default.
# HTTP_100_CONTINUE
# HTTP_101_SWITCHING_PROTOCOLS

# Successful - 2xx
# This class of status code indicates that the client's request was successfully received, understood, and accepted.
# HTTP_200_OK
# HTTP_201_CREATED
# HTTP_202_ACCEPTED
# HTTP_203_NON_AUTHORITATIVE_INFORMATION
# HTTP_204_NO_CONTENT
# HTTP_205_RESET_CONTENT
# HTTP_206_PARTIAL_CONTENT
# HTTP_207_MULTI_STATUS
# HTTP_208_ALREADY_REPORTED
# HTTP_226_IM_USED

# Redirection - 3xx
# This class of status code indicates that further action needs to be taken by the user agent
# in order to fulfill the request.
# HTTP_300_MULTIPLE_CHOICES
# HTTP_301_MOVED_PERMANENTLY
# HTTP_302_FOUND
# HTTP_303_SEE_OTHER
# HTTP_304_NOT_MODIFIED
# HTTP_305_USE_PROXY
# HTTP_306_RESERVED
# HTTP_307_TEMPORARY_REDIRECT
# HTTP_308_PERMANENT_REDIRECT

# Client Error - 4xx
# The 4xx class of status code is intended for cases in which the client seems to have erred. 
# Except when responding to a HEAD request, the server SHOULD include an entity containing an 
# explanation of the error situation, and whether it is a temporary or permanent condition.
# HTTP_400_BAD_REQUEST
# HTTP_401_UNAUTHORIZED
# HTTP_402_PAYMENT_REQUIRED
# HTTP_403_FORBIDDEN
# HTTP_404_NOT_FOUND
# HTTP_405_METHOD_NOT_ALLOWED
# HTTP_406_NOT_ACCEPTABLE
# HTTP_407_PROXY_AUTHENTICATION_REQUIRED
# HTTP_408_REQUEST_TIMEOUT
# HTTP_409_CONFLICT
# HTTP_410_GONE
# HTTP_411_LENGTH_REQUIRED
# HTTP_412_PRECONDITION_FAILED
# HTTP_413_REQUEST_ENTITY_TOO_LARGE
# HTTP_414_REQUEST_URI_TOO_LONG
# HTTP_415_UNSUPPORTED_MEDIA_TYPE
# HTTP_416_REQUESTED_RANGE_NOT_SATISFIABLE
# HTTP_417_EXPECTATION_FAILED
# HTTP_422_UNPROCESSABLE_ENTITY
# HTTP_423_LOCKED
# HTTP_424_FAILED_DEPENDENCY
# HTTP_426_UPGRADE_REQUIRED
# HTTP_428_PRECONDITION_REQUIRED
# HTTP_429_TOO_MANY_REQUESTS
# HTTP_431_REQUEST_HEADER_FIELDS_TOO_LARGE
# HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS

# Server Error - 5xx
# Response status codes beginning with the digit "5" indicate cases in which the server is aware 
# that it has erred or is incapable of performing the request. Except when responding to a HEAD request, 
# the server SHOULD include an entity containing an explanation of the error situation, 
# and whether it is a temporary or permanent condition.
# HTTP_500_INTERNAL_SERVER_ERROR
# HTTP_501_NOT_IMPLEMENTED
# HTTP_502_BAD_GATEWAY
# HTTP_503_SERVICE_UNAVAILABLE
# HTTP_504_GATEWAY_TIMEOUT
# HTTP_505_HTTP_VERSION_NOT_SUPPORTED
# HTTP_506_VARIANT_ALSO_NEGOTIATES
# HTTP_507_INSUFFICIENT_STORAGE
# HTTP_508_LOOP_DETECTED
# HTTP_509_BANDWIDTH_LIMIT_EXCEEDED
# HTTP_510_NOT_EXTENDED
# HTTP_511_NETWORK_AUTHENTICATION_REQUIRED

# Helper functions
# The following helper functions are available for identifying the category of the response code.
#  is_informational()  # 1xx
#  is_success()        # 2xx
#  is_redirect()       # 3xx
#  is_client_error()   # 4xx
#  is_server_error()   # 5xx
