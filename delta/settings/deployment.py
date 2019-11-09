import os
import dj_database_url

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['delta-backend.herokuapp.com']

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

prod_db = dj_database_url.config(conn_max_age=500)

DATABASES = {
    'default': {
    }
}

DATABASES['default'].update(prod_db)
