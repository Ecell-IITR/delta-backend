import os
import dj_database_url

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEBUG = False

prod_db = dj_database_url.config(conn_max_age=500)

DATABASES = {
    'default': {
        'NAME': os.getenv('DATABASE_NAME', 'delta'),
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'USER': os.getenv('DATABASE_USER', 'delta_user'),
        'PASSWORD': os.getenv('DATABASE_PASSWORD', 'delta_user'),
        'HOST': os.getenv('DATABASE_HOST', 'localhost'),
        'PORT': '5432',
    }
}

DATABASES['default'].update(prod_db)
