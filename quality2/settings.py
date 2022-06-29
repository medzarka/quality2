"""
Django settings for base project.

Generated by 'django-admin startproject' using Django 2.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import sys
from pathlib import Path
import environ
import os


def createDir(dirname):
    try:
        os.makedirs(dirname)
    except FileExistsError:
        pass



sys.setdefaultencoding('utf-8')

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if 'env_file' in os.environ.keys():
    env_file = os.path.join(BASE_DIR, 'env', os.getenv('env_file'))
    print(f'Configuration Site in file {env_file}.')
else:
    env_file = 'env'
    env_file = os.path.join(BASE_DIR, 'env', 'env')
    print(f'Configuration Site in file {env_file}.')

if env_file is None:
    print(f'The env filename "env_file" is not set !')
    sys.exit(-1)

if not os.path.exists(os.path.join(BASE_DIR, env_file)):
    print(f'The env filename {env_file} does not exist!')
    sys.exit(-1)

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False),
    SITE_DATA_PATH=(str, 'data'),
    SESSION_EXPIRE_AT_BROWSER_CLOSE=(bool, False),
    SESSION_COOKIE_AGE=(int, 3600),
    FILE_UPLOAD_MAX_MEMORY_SIZE=(int, 104857600),
    SESSION_COOKIE_SECURE=(bool, True),
    CSRF_COOKIE_SECURE=(bool, True),
    SECURE_SSL_REDIRECT=(bool, True),
    SECURE_HSTS_SECONDS=(int, 2592000),
    SECURE_HSTS_INCLUDE_SUBDOMAINS=(bool, True),
    SECURE_HSTS_PRELOAD=(bool, True),
    SITE_ADMIN_TEMPLATE=(str, 'GRAPPELLI'),
    SITE_ADMIN_SITE_TITLE=(str, 'uKKU2 Quality Document Manager'),
    SITE_ADMIN_SITE_HEADER=(str, 'uKKU (ver.2) Admin'),
    SITE_ADMIN_SITE_INDEX_TITLE=(str, 'Welcome to uKKU2 Admin'),
)
env.read_env(os.path.join(BASE_DIR, env_file))

SITE_DATA_DIR = os.path.join(os.environ['HOME'], env('SITE_DATA_PATH'))
SITE_FILES_DIR = os.path.join(os.environ['HOME'], env('SITE_FILES_PATH'))
createDir(SITE_DATA_DIR)
createDir(SITE_FILES_DIR)
print(f'[DIR] the base dir is {BASE_DIR}')
print(f'[DIR] the data dir is {SITE_DATA_DIR}')
print(f'[DIR] the files (static and media) dir is {SITE_FILES_DIR}')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool('DEBUG')

ALLOWED_HOSTS = ['localhost', '127.0.0.1', env.str('SITE_URL')]

# Application definition
INSTALLED_APPS = []
if env.str('SITE_ADMIN_TEMPLATE') == 'GRAPPELLI':
    INSTALLED_APPS = ['grappelli', ]
if env.str('SITE_ADMIN_TEMPLATE') == 'ADMIN_INTERFACE':
    INSTALLED_APPS = ['admin_interface',
                      'colorfield', ]

# Application definition

INSTALLED_APPS += [

    'django_db_logger',
    'import_export',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'quotes',

    '_data.apps.DataConfig',
    '_web.apps.WebConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'quality2.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'), ],
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

WSGI_APPLICATION = 'quality2.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases


if env.str('DATABASE_URL', default=''):
    DATABASES = {
        'default': env.db(),
    }

    DATABASES['default']['OPTION'] = {
        'init_command': "SET sql_mode='STRICT_TRANS_TABLES', innodb_strict_mode=1",
        'charset': 'utf8mb4',
        "autocommit": True,
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': SITE_DATA_DIR.path('db')('django.sqlite3'),
        },
    }

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Riyadh'
USE_I18N = True
USE_L10N = True
USE_TZ = True

####### Media and Static files
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/
# createDir(SITE_DATA_DIR)
# createDir(SITE_FILES_DIR)

createDir(os.path.join(SITE_FILES_DIR, 'static/'))
createDir(os.path.join(SITE_FILES_DIR, 'media/'))
STATIC_ROOT = os.path.join(os.path.join(SITE_FILES_DIR, 'static/'))
STATIC_URL = f'{env.str("SITE_URL_PREFIX")}/static/'
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static/'),)
MEDIA_ROOT = os.path.join(os.path.join(SITE_FILES_DIR, 'media/'))
MEDIA_URL = f'{env.str("SITE_URL_PREFIX")}/media/'
print(f'[DIR] the static files are in {os.path.join(SITE_FILES_DIR, "static/")}')
print(f'[DIR] the media files are in {os.path.join(SITE_FILES_DIR, "media/")}')

###### Login & Session Age
# LOGIN_URL = '/web/login/'
# LOGIN_REDIRECT_URL = '/web/dashboard'
# AUTH_USER_MODEL = '_data.User'
# AUTH_LOGIN_URL = 'web_auth_login'
# AUTH_LOGOUT_URL = 'web_auth_logout'
# AUTH_DASHBOARD_URL = 'web_dashboard'
LOGIN_URL = '/web/login/'
LOGIN_REDIRECT_URL = '/web/dashboard'
# print(f'[AUTH] the class {AUTH_USER_MODEL} is used as users backend.')

###### allow upload big file
FILE_UPLOAD_MAX_MEMORY_SIZE = env.int('FILE_UPLOAD_MAX_MEMORY_SIZE')
print(f'[FILES] the maximum size for file upload is  {FILE_UPLOAD_MAX_MEMORY_SIZE / (1024 * 1024)} MBytes.')

# createDir(SITE_DATA_DIR)
# createDir(SITE_FILES_DIR)
###### Loggin
createDir(os.path.join(SITE_DATA_DIR, 'log'))
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(asctime)s %(message)s'
        },
    },
    'handlers': {
        'db_log': {
            'level': 'DEBUG',
            'class': 'django_db_logger.db_log_handler.DatabaseLogHandler'
        },
    },
    'loggers': {
        'db': {
            'handlers': ['db_log'],
            'level': 'DEBUG'
        },
        'django.request': {  # logging 500 errors to database
            'handlers': ['db_log'],
            'level': 'ERROR',
            'propagate': False,
        }
    }
}
DJANGO_DB_LOGGER_ENABLE_FORMATTER = env.bool('DJANGO_DB_LOGGER_ENABLE_FORMATTER')
DJANGO_DB_LOGGER_ADMIN_LIST_PER_PAGE = env.int('DJANGO_DB_LOGGER_ADMIN_LIST_PER_PAGE')

print(f'[DIR] the log file is in {os.path.join(SITE_DATA_DIR, "log")}')

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

#######  Sending emails
# The email() method is an alias for email_url().
EMAIL_CONFIG = env.email(
    'EMAIL_URL',
    default='smtp://user:password@localhost:25'
)
vars().update(EMAIL_CONFIG)

# only if django version >= 3.0
X_FRAME_OPTIONS = "SAMEORIGIN"
SILENCED_SYSTEM_CHECKS = ["security.W019"]

from django.contrib.messages import constants as messages

MESSAGE_TAGS = {
    messages.ERROR: 'danger',
}

##### Admin Title configuration
SITE_ADMIN_TEMPLATE = env.str('SITE_ADMIN_TEMPLATE')
GRAPPELLI_ADMIN_TITLE = env.str('SITE_ADMIN_SITE_TITLE')
ADMIN_SITE_SITE_HEADER = env.str('SITE_ADMIN_SITE_HEADER')
ADMIN_SITE_INDEX_TITLE = env.str('SITE_ADMIN_SITE_INDEX_TITLE')
ADMIN_SITE_SITE_TITLE = env.str('SITE_ADMIN_SITE_TITLE')

###### Session management. The session will close after
SESSION_EXPIRE_AT_BROWSER_CLOSE = env.bool('SESSION_EXPIRE_AT_BROWSER_CLOSE')
SESSION_COOKIE_AGE = env.int('SESSION_COOKIE_AGE')
print(f'[Sessions] the maximum time to keep the session cookie is {SESSION_COOKIE_AGE / 60} minute(s).')

###### SSL Session
SESSION_COOKIE_SECURE = env.bool('SESSION_COOKIE_SECURE')
CSRF_COOKIE_SECURE = env.bool('CSRF_COOKIE_SECURE')
SECURE_SSL_REDIRECT = env.bool('SECURE_SSL_REDIRECT')

SECURE_HSTS_SECONDS = env.int('SECURE_HSTS_SECONDS')
SECURE_HSTS_INCLUDE_SUBDOMAINS = env.bool('SECURE_HSTS_INCLUDE_SUBDOMAINS')
SECURE_HSTS_PRELOAD = env.bool('SECURE_HSTS_PRELOAD')
