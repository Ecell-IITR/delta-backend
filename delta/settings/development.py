"""
Django settings for delta project.

Generated by 'django-admin startproject' using Django 2.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

from delta.restconf.main import *
import os

from dotenv import load_dotenv

load_dotenv(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = "*yw0)r$l96pfky+khaf%z$&a=pr2o%asf$au-u(1_rmwm0g^zq"

DEBUG = True

ALLOWED_HOSTS = ["*"]
# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",  # required for serving swagger ui's css/js files
    # Installed packages
    "rest_framework",
    "rest_framework.authtoken",
    "corsheaders",
    "drf_yasg",
    # Docs
    "rest_framework_swagger",
    "ckeditor",
    "ckeditor_uploader",
    # Apps
    # "dal",
    # "dal_select2",
    "users",
    "post",
    "utilities",
]

# CORS Settings
CORS_ORIGIN_ALLOW_ALL = True

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}


MIDDLEWARE = [
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "corsheaders.middleware.CorsMiddleware",
]

ROOT_URLCONF = "delta.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "delta.wsgi.application"


AUTH_USER_MODEL = "users.Person"

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

CORS_ORIGIN_ALLOW_ALL = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = "/static/"

STATIC_ROOT = os.path.join(BASE_DIR, "static")

MEDIA_URL = "/media/"

MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# CKEDITOR media path relative to media url
CKEDITOR_UPLOAD_PATH = "ckeditor_uploads/"

CKEDITOR_FILENAME_GENERATOR = "common.get_file_path.get_ckeditor_filename"

CKEDITOR_IMAGE_BACKEND = "pillow"

CKEDITOR_JQUERY_URL = "https://ajax.googleapis.com/ajax/libs/jquery/2.1.1/jquery.min.js"

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

# REST_FRAMEWORK = { 'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema' }
