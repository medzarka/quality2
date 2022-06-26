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

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ')sk)#f&8op^k11%jc+e3=%=5se^$4q9_y3+ligklee=*m1035a'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'quotes'
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
        'DIRS': [],
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

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'mzarka_quotes',
        'USER': 'mzarka_quotes',
        'PASSWORD': 'mzarka_quotes',
        'HOST': 'localhost',
        'PORT': '3306',
    }
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

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)
STATIC_ROOT = '/home/mzarka/subdomains/sites/quality.bluewaves.online/static'
