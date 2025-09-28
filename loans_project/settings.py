"""
Django settings for loans_project project.

Environment variables handled via python-decouple (.env file)
"""

from pathlib import Path
import os
from decouple import config, Csv

# ------------------------
# Base Directory
# ------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# ------------------------
# Security
# ------------------------
SECRET_KEY = config("SECRET_KEY")
DEBUG = config("DEBUG", default=False, cast=bool)
ALLOWED_HOSTS = config("ALLOWED_HOSTS", default="", cast=Csv())

# ------------------------
# Email Configuration
# ------------------------
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config("EMAIL_HOST")
EMAIL_PORT = config("EMAIL_PORT", default=587, cast=int)
EMAIL_USE_TLS = config("EMAIL_USE_TLS", default=True, cast=bool)
EMAIL_HOST_USER = config("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = config("EMAIL_PASS")
DEFAULT_FROM_EMAIL = config("DEFAULT_FROM_EMAIL")

# ------------------------
# Installed Apps
# ------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party apps
    'rest_framework',
    'django_rq',

    # Local apps
    'loans_project',
]

# ------------------------
# Custom User Model
# ------------------------
AUTH_USER_MODEL = 'loans_project.Client'

# ------------------------
# Middleware
# ------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ------------------------
# URLs and WSGI
# ------------------------
ROOT_URLCONF = 'loans_project.urls'
WSGI_APPLICATION = 'loans_project.wsgi.application'

# ------------------------
# Templates
# ------------------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'loans_project/templates')],
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

# ------------------------
# Database
# ------------------------
# Default: SQLite, can be replaced with Postgres/MySQL via .env
DATABASES = {
    'default': {
        'ENGINE': config("DB_ENGINE", default="django.db.backends.sqlite3"),
        'NAME': config("DB_NAME", default=BASE_DIR / "db.sqlite3"),
        'USER': config("DB_USER", default=""),
        'PASSWORD': config("DB_PASSWORD", default=""),
        'HOST': config("DB_HOST", default=""),
        'PORT': config("DB_PORT", default=""),
    }
}

# ------------------------
# Password Validators
# ------------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

# ------------------------
# Internationalization
# ------------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ------------------------
# Static and Media
# ------------------------
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'loans_project/static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# ------------------------
# REST Framework
# ------------------------
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

# ------------------------
# Redis Cache
# ------------------------
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": config("REDIS_URL"),
        "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient"},
    }
}

# ------------------------
# Django RQ Queues
# ------------------------
RQ_QUEUES = {
    "default": {
        "URL": config("REDIS_URL", default="redis://localhost:6379/0"),
        "DEFAULT_TIMEOUT": 360,
    }
}

# ------------------------
# Default Auto Field
# ------------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
