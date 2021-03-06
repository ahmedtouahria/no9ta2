from datetime import timedelta
from pathlib import Path
import os
from decouple import  config
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
#SECRET_KEY = 'django-insecure-u18h_^r=k@i0o4cf1&t3=f68c8zjiqi(7gj0p0&z*-961hy%jw'
#DEBUG = False

SECRET_KEY=config('SECRET_KEY')
DEBUG=config('DEBUG')

STRIPE_PRICE_TYPE_89="price_1KYoQjCJpuKCK5IlLCjlRa0n"
STRIPE_PRICE_TYPE_130="price_1KYoRVCJpuKCK5IlewSj4Ovx"
STRIPE_PRICE_TYPE_220="price_1KYoS1CJpuKCK5IlaTxi1KSR"
STRIPE_LIVE_MODE = False
STRIPE_LIVE_SECRET_KEY = os.environ.get("STRIPE_LIVE_SECRET_KEY", "sk_live_XXXXXXX")
STRIPE_TEST_SECRET_KEY = os.environ.get("STRIPE_TEST_SECRET_KEY", "sk_test_51KYo2HCJpuKCK5IlMLXTu0WmchAFF0ahb7vJxoOm3la1TZvnfztLBZn4fAVRNcA8yvTxpk2K94bKX5S58O6jGLSH00q6XCanRF")
DJSTRIPE_WEBHOOK_SECRET = os.environ.get(
    "DJSTRIPE_TEST_WEBHOOK_SECRET", "whsec_d327c7908d4b0da54186a7a93b31e501e25fd2752feeb4b3b0cf0ec414ea37e1"
)
DJSTRIPE_FOREIGN_KEY_TO_FIELD = "id"
DJSTRIPE_USE_NATIVE_JSONFIELD = True
# SECURITY WARNING: don't run with debug turned on in production!

ALLOWED_HOSTS = ['noqtaa.herokuapp.com','127.0.0.1']


# Application definition

INSTALLED_APPS = [
   # 'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'rest_framework',
    'knox',
    "djstripe",
    'django_countries',
    'user',
    'resto',
    'admin_interface', 
    'colorfield', 
    'django.contrib.admin',
    'location_field.apps.DefaultConfig',

]
X_FRAME_OPTIONS='SAMEORIGIN'
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        # 'rest_framework.authentication.BasicAuthentication',
        # 'rest_framework.authentication.SessionAuthentication',
        'knox.auth.TokenAuthentication',
    ]
}
CORS_ALLOWED_ORIGINS = [
        "https://example.com",
        "https://sub.example.com",
        "http://localhost:8080",
        "http://127.0.0.1:9000"
    ]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
AUTH_USER_MODEL='user.User'

ROOT_URLCONF = 'No9ta.urls'

REST_KNOX = {
  'TOKEN_TTL': timedelta(hours=1200),
}
''' LOCATION_FIELD = {
'provider.google.api': '//maps.google.com/maps/api/js?sensor=false',
'provider.google.api_key': '<PLACE YOUR API KEY HERE>',
'provider.google.api_libraries': '',
'provider.google.map.type': 'ROADMAP',
} '''

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
                'DIRS': [os.path.join(BASE_DIR,'templates')],

        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'No9ta.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

""" DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
} """

from dj_database_url import parse as dburl

default_dburl = 'sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3')
DATABASES = {
                'default': config('DATABASE_URL', default=default_dburl, cast=dburl),
            }
# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/
#STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR,'static')
STATICFILES_DIRS = [os.path.join(BASE_DIR,'No9ta/static')]
MEDIA_ROOT = os.path.join(BASE_DIR, '') # 'data' is my media folder
MEDIA_URL = '/media/'
# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
