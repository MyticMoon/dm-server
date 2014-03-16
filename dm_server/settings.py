"""
Django settings for dm_server project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import logging
import logging.config
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


#config for logging
# LOGGING_CONFIG = 'logging.conf' # logging configuration file
# logging.config.fileConfig(LOGGING_CONFIG)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'm3nja&87d=ki1-5(dz(bh18lpn&a90r=^fy#89-6j18!jca!d9'
#project_id;166
#job_id:25
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'dmserver',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'dm_server.urls'

WSGI_APPLICATION = 'dm_server.wsgi.application'


TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    # os.path.join(os.path.dirname(__file__),'Templates').replace('\\','/')
    os.path.realpath(os.path.dirname(__file__)) + "/dmserver/templates/"
)

UPLOAD_DIR = os.path.realpath(os.path.dirname(__file__)) + "/../dmserver/upload/"

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    #the local testing
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'shoes_db',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
API_KEY = "DqxoR5Gl6cctRj05hsQqNDlfl5F23okS3TFGFNQEz7E"