"""
Django settings for project.
Generated by 'django-admin startproject' using Django 4.2.
For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/
For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

import os
from pathlib import Path
from decouple import config
from decouple import Csv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
# ~/<virtualenv-folder>/
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: Keep the secret key used in production secret!
# SECURITY WARNING: Don't run with debug turned on in production!

if config('PRODUCTION', default=False, cast=bool) == True:
    DEBUG = False
    SECRET_KEY = config('PROD_SECRET_KEY')
    SECRET_KEY_FALLBACK = config('PROD_SECRET_KEY_FALLBACK')
    ALLOWED_HOSTS = config('PROD_ALLOWED_HOSTS', cast=Csv())
    # Security
    SECURE_SSL_HOST = config('SECURE_SSL_HOST')
    SECURE_SSL_REDIRECT = config('SECURE_SSL_REDIRECT', default=True, cast=bool)
    SECURE_REFERRER_POLICY = config('SECURE_REFERRER_POLICY')
    SECURE_HSTS_SECONDS = config('SECURE_HSTS_SECONDS')
    SECURE_HSTS_PRELOAD = config('SECURE_HSTS_PRELOAD', default=True, cast=bool)
    SECURE_HSTS_INCLUDE_SUBDOMAINS = config('SECURE_HSTS_INCLUDE_SUBDOMAINS', default=True, cast=bool)
    X_FRAME_OPTIONS = config('X_FRAME_OPTIONS')
    # Cookies
    CSRF_COOKIE_SECURE = config('CSRF_COOKIE_SECURE', default=True, cast=bool)
    SESSION_COOKIE_SECURE = config('SESSION_COOKIE_SECURE', default=True, cast=bool)
    SESSION_COOKIE_AGE = config('SESSION_COOKIE_AGE')
    SESSION_COOKIE_NAME = config('SESSION_COOKIE_NAME')
    SESSION_COOKIE_DOMAIN = config('SESSION_COOKIE_DOMAIN')
    SESSION_COOKIE_SAMESITE = config('SESSION_COOKIE_SAMESITE')
    # Proxy Use Only
    # SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    # USE_X_FORWARDED_HOST = False
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    # EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    # EMAIL_HOST = 'email-host.com'
    # EMAIL_PORT = 587
    # EMAIL_USE_TLS = True
    # EMAIL_HOST_USER = 'email@example.com'
    # EMAIL_HOST_PASSWORD = 'email-password'
else:
    DEBUG = True
    SECRET_KEY = config('DEBUG_SECRET_KEY')
    ALLOWED_HOSTS = config('DEBUG_ALLOWED_HOSTS', cast=Csv())
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    INTERNAL_IPS = ['192.168.0.15']

    SWAGGER_SETTINGS = {
        'SECURITY_DEFINITIONS': {
            'Token': {
                'type': 'apiKey', 
                'name': 'Authorization',
                'in': 'header'
            },
            'Basic': {'type': 'basic'},
        }
    }


### USER AUTHENTICATION

SITE_ID = int(config('SITE_ID'))
AUTH_USER_MODEL = 'custom_auth.User'
ACCOUNT_ACTIVATION_DAYS = 7
REGISTRATION_OPEN = True
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"


### APPLICATION DEFINITION

INSTALLED_APPS = [
    'custom_auth',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admindocs',
    ## django-allauth
    'django.contrib.sites',
    # 'allauth',
    # 'allauth.account',
    # 'allauth.socialaccount',
    # 'allauth.socialaccount.providers.google',
    #'taggit',
    'rest_framework',
    #'rest_framework.authtoken',
    'crispy_forms',
    'crispy_bootstrap3', # DRF
    'crispy_bootstrap5',
    'bootstrap_datepicker_plus',
    'django_filters',
    'media',
    'core',
    #'versatileimagefield',
    
]

if DEBUG == True:
    INSTALLED_APPS += ['debug_toolbar', 'drf_yasg',]


MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'sgc.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates", os.path.join(BASE_DIR, "templates")],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.media',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'sgc.wsgi.application'


### DATABASE
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': config('DB_ENGINE'),
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT'),
        'CONN_MAX_AGE': 600,
    }
}


### PASSWORD VALIDATION
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
]


### INTERNATIONALIZATION
# https://docs.djangoproject.com/en/4.2/topics/i18n/
LANGUAGE_CODE = 'en-us'
USE_I18N = True
USE_THOUSAND_SEPARATOR = True
THOUSAND_SEPARATOR = ','


### TIME ZONE
# https://en.wikipedia.org/wiki/List_of_tz_database_time_zones
TIME_ZONE = 'UTC'
USE_TZ = True


### STATIC FILES (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/`
if config('PRODUCTION', default=False, cast=bool) == True:
    LOCAL_STATIC_CDN = os.path.join(os.path.dirname(BASE_DIR), 'static_cdn')
    STATIC_URL = '/static_cdn/'
else:
    LOCAL_STATIC_CDN = os.path.join(os.path.dirname(BASE_DIR), 'static_cdn')
    STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(LOCAL_STATIC_CDN, 'static')

STATICFILES_DIRS = [
   os.path.join(BASE_DIR, 'static_files')
]

# AWS_STORAGE_BUCKET_NAME = 'your-s3-bucket-name'
# AWS_S3_CUSTOM_DOMAIN = 'cdn.mydomain.com'
# STATIC_URL = 'https://%s/static/' % AWS_S3_CUSTOM_DOMAIN
# MEDIA_URL = 'https://%s/media/' % AWS_S3_CUSTOM_DOMAIN
# DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# print(os.path.dirname(BASE_DIR))
# print(LOCAL_STATIC_CDN)
# print(STATIC_ROOT)
# print(os.path.join(BASE_DIR, 'static_files'))


### FILE UPLOADS
# FILE_UPLOAD_HANDLERS = [
#     'django.core.files.uploadhandler.TemporaryFileUploadHandler',
#     'django.core.files.uploadhandler.MemoryFileUploadHandler',
# ]

# # The maximum size (in bytes) that an upload will be before it gets streamed to the file system.
# # Default: 2621440
# FILE_UPLOAD_MAX_MEMORY_SIZE = 4194304  #4M
# # The directory to store upload data to.
# FILE_UPLOAD_TEMP_DIR = '/tmp'
# # The numeric mode (ex. 0o644) to set newly uploaded files to. Doesn't apply to temporary files.
# FILE_UPLOAD_PERMISSIONS = 0o640  # Default: 0o644
# # The numeric mode to apply to directories created in the process of uploading files.
# FILE_UPLOAD_DIRECTORY_PERMISSIONS = 0o640  # Default: None


### MEDIA FILES
# MEDIA_ROOT is the path to the root directory where the files are getting stored.
# MEDIA_URL is the URL that will serve the media files.
if config('PRODUCTION', default=False, cast=bool) == True:
    MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'media_assets/')
    MEDIA_URL = '/media/'
else:
    MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'media_assets/')
    MEDIA_URL = '/media/'


### FIXTURES
# Data files for database defaults
# Load data by calling manage.py loaddata app/fixtures/app/<fixturename> or * 
#  where <fixturename> is the name of the fixture file.
FIXTURE_DIRS = [
    os.path.join(BASE_DIR, '/media/fixtures/media/'),
    os.path.join(BASE_DIR, '/system_config/fixtures/system_config/')
]


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


### FORMS
CRISPY_ALLOWED_TEMPLATE_PACKS = 'bootstrap5'
CRISPY_TEMPLATE_PACK = 'bootstrap5'


### TAGGING
#TAGGIT_CASE_INSENSITIVE = True


### CACHING
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'django-local-cache',
        #'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        #'LOCATION': '/var/tmp/django_cache',
    }
}


### DJANGO REST FRAMEWORK
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
        # SimpleJWT
        #'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        # APIs only accessible with authentication
        #'rest_framework.permissions.IsAuthenticated',
        'rest_framework.permissions.IsAuthenticatedOrReadOnly'
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer', 
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
    'DEFAULT_THROTTLE_CLASSES': [
        'media.api.throttling.AnonSustainedThrottle',
        'media.api.throttling.AnonBurstThrottle',
        'media.api.throttling.UserSustainedThrottle',
        'media.api.throttling.UserBurstThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon_sustained': '500/day',
        'anon_burst': '10/minute',
        'user_sustained': '2000/day',
        'user_burst': '100/minute',
    },
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.OrderingFilter',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 100,
    'DEFAULT_LIMIT': 100,
    'UNICODE_JSON': True,
    'COMPACT_JSON': True,
}


## Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    # 'filters': {
    #     'require_debug_false': {
    #         '()': 'django.utils.log.RequireDebugFalse',
    #     },
    # },
    'formatters': {
        'verbose': {
            #'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        # 'file': {
        #     'class': 'logging.FileHandler',
        #     'filename': '/home/ubuntu/django.log',
        #     'formatter': 'verbose',
        # },
        'console': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
            'formatter': 'verbose',
        },
        # 'mail_admins': {
        #     'level': 'ERROR',
        #     'class': 'django.utils.log.AdminEmailHandler',
        #     'filters': ['require_debug_false'],
        # },
    },
    'loggers': {
        'django': {
            #'handlers': ['file', 'console'],
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
    },
    'root': {
        #'handlers': ['file', 'console'],
        'handlers': ['console'],
        'level': 'INFO',
    },
}


# BOOTSTRAP_DATEPICKER_PLUS = {
#     "showTodayButton": True,
#     "variant_options": {
#         "date": {
#             "format": "YYYY-MM-DD",
#         },
#     }
# }


### MONITORING
# DJANGO_MONITORING_ALERTS = {
#     'ERROR_THRESHOLD': 10,
#     'NOTIFICATION_CHANNELS': ['email'],
# }
