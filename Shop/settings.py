"""
Django settings for Shop project.

Generated by 'django-admin startproject' using Django 3.2.8.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import os
from pathlib import Path
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-1di0mc012lcd=k*)5moel7de+_g)y88!bq0g9q-hpp(8iv%!2a'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# for api and set session
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'ecommerce-django-website.herokuapp.com']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # installed apps
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'ckeditor',

    # define apps
    'billing',
    'products',
    'cart',
    'order',
    'users',
    'category',
    'wishlist',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'Shop.urls'

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'JWT_ALLOW_REFRESH': True,
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
}


CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True
# CORS_ALLOWED_ORIGINS = ['http://localhost:8000', 'http://127.0.0.1:8000']
# CSRF_TRUSTED_ORIGINS = ['http://localhost:8000',  'http://127.0.0.1:8000']

TEMPLATES = [
  {
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': ['templates',],
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

WSGI_APPLICATION = 'Shop.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

# DATABASES = {
#   'default': {
#     'ENGINE': 'django.db.backends.sqlite3',
#     'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#   }
# }

# Postgresql
DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.postgresql',
    'NAME': 'dcd3fkpkuhr8a',
    'HOST':'ec2-3-223-242-224.compute-1.amazonaws.com',
    'PORT': 5432,
    'USER': 'bvzbmluefnlvdf',
    'PASSWORD': '13ab3069bfbe9c0d7c5eccb14c2c294b597b66cfc880f3292abf6d88cdbbe918',
  }
}

# Password validation
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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

AUTH_USER_MODEL = 'users.MyUser'

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Rest Framework Settings
REST_FRAMEWORK = {
  'DEFAULT_PERMISSION_CLASSES': [
    'rest_framework.permissions.AllowAny',
  ],
  'DEFAULT_AUTHENTICATION_CLASSES': [
    'rest_framework_simplejwt.authentication.JWTAuthentication',
  ]
}

# Email Settings
SEND_GRID_API_KEY = os.environ.get('SENDGRID_API_KEY')
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'admin@gmail.com'
EMAIL_HOST_PASSWORD = ''
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'admin@gmail.com'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

# CLOUDINARY_URL = 'cloudinary://446988924392248:U6OYTDlWY7-WbSo6GdCq-lerPUw@hopkwuhy0'

STATIC_URL = '/static/'
if not DEBUG:
  STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

STATICFILES_DIRS = (os.path.join(BASE_DIR, ''),)

# STATICFILES_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

MEDIA_URL = '/media/'

# MEDIA_ROOT = 'media'
# for api reactjs

MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

# DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'



# CLOUDINARY_STORAGE = {
#   'CLOUD_NAME': 'hopkwuhy0',
#   'API_KEY': '446988924392248',
#   'API_SECRET': 'U6OYTDlWY7-WbSo6GdCq-lerPUw',
# }

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

