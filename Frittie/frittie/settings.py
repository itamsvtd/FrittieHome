# Django settings for Frittie project.

import os
ROOT_PATH = os.path.dirname(__file__)
WEBSITE_HOMEPAGE = "http://localhost:8000/"
WEBSITE_DOMAIN = 'localhost:8000'

import stomp
conn = stomp.Connection()
try:
    conn.start()
    conn.connect()
    conn.subscribe(destination='/update', ack='auto')
except:
    pass

import djcelery  
djcelery.setup_loader()

# from celery.schedules import crontab

# CELERYBEAT_SCHEDULE = {
#     'test-job': {
#         'task': 'app.main.tasks.test',
#         'schedule': crontab(),
#         'args': (16, 16),
#     },
# }


DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Dang Nguyen', 'dangnguyen_1712@yahoo.com'),
)

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_PASSWORD = '17121990ntd'
EMAIL_HOST_USER = 'dang.nguyen@frittie.com'
EMAIL_USE_TLS = True

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME':  os.path.join(ROOT_PATH, "db/data.db"),                     # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/New_York'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = False

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(ROOT_PATH, 'asset/media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = WEBSITE_HOMEPAGE + "asset/media/"

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
     os.path.join(os.path.abspath(ROOT_PATH), 'asset/static'),   
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '2!(mk54t367e4(9_)z_69%we=7ric+=5%am8hw=g(49jdxx6=s'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
    "django.core.context_processors.request",
    #'allauth.context_processors.allauth',
    'allauth.account.context_processors.account',
    'django_facebook.context_processors.facebook',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'frittie.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'frittie.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(ROOT_PATH, "asset/templates"),
)

FIXTURE_DIRS = (
    os.path.join(ROOT_PATH, "fixtures"),
)

INSTALLED_APPS = (
    # Django built-in apps
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    #'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.admindocs',

    # Frittie app 
    'frittie.app',
    'frittie.app.main',
    'frittie.app.member',
    'frittie.app.info',
    'frittie.app.location',
    'frittie.app.activity',
    'frittie.app.notify',
    'frittie.app.photo',
    'frittie.app.message',
    'frittie.helper',

    # Allauth app
    'emailconfirmation',
    'uni_form',
    'allauth',
    'allauth.account',

    # Other app
    'redis',
    'friends',
    'tastypie',
    'user_streams',
    'user_streams.backends.user_streams_single_table_backend',
    #'user_streams.backends.user_streams_redis_backend',
    'haystack',
    'south',
    'dajaxice',
    'django_facebook',
    'kombu.transport.django',  
    'djcelery',
    #'sorl.thumbnail',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'logfile_dajaxice': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename':  os.path.join(ROOT_PATH, "log/dajaxice.log"),
        }, 
        'logfile_facebook': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename':  os.path.join(ROOT_PATH, "log/django_facebook.log"),
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'dajaxice': {
            'handlers': ['logfile_dajaxice'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django_facebook':{
            'handlers': ['logfile_facebook'],
            'level': 'DEBUG',
            'propagate': True,
        },
    }, 
}


AUTH_PROFILE_MODULE = 'main.Member'

SERIALIZATION_MODULES = {
    'json': 'wadofstuff.django.serializers.json'
}

AUTHENTICATION_BACKENDS = (
    'allauth.account.auth_backends.AuthenticationBackend',
    'django_facebook.auth_backends.FacebookBackend',
    'django.contrib.auth.backends.ModelBackend', 
)

ACCOUNT_ACTIVATION_DAYS = 7

HAYSTACK_SITECONF = 'frittie.app.search.search_sites'
HAYSTACK_SEARCH_ENGINE = 'whoosh'
HAYSTACK_WHOOSH_PATH = os.path.join(ROOT_PATH, 'db/whoosh_index')
HAYSTACK_USE_REALTIME_SEARCH = False

#TASTYPIE_DATETIME_FORMATTING = 'rfc-2822'

DAJAXICE_MEDIA_PREFIX="dajaxice"

#USER_STREAMS_BACKEND = 'user_streams.backends.user_streams_redis_backend.RedisBackend'
USER_STREAMS_BACKEND = 'user_streams.backends.user_streams_single_table_backend.SingleTableDatabaseBackend'

ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False

MULTI_FILE_DELETE_URL = 'multi_delete'
MULTI_IMAGE_URL = 'multi_image'
MULTI_IMAGES_FOLDER = 'uploads/img/share' 

NORMAL_STREAM_LIMIT = 10
PAGE_STREAM_LIMIT = 20

FACEBOOK_APP_ID = "265377323561995"
FACEBOOK_APP_SECRET = '6affb16d935e406397b5c68a413141f5'
FACEBOOK_STORE_LIKES = False
FACEBOOK_STORE_FRIENDS = True
FACEBOOK_LOGIN_DEFAULT_REDIRECT = '/login'
FACEBOOK_DEFAULT_SCOPE = ['email', 'user_about_me', 'user_birthday', 'publish_stream', 'publish_actions', 'offline_access']
FACEBOOK_REGISTRATION_TEMPLATE = 'account/signup_init.html'
FACEBOOK_CELERY_STORE = False

BROKER_URL = "django://"  
CELERYBEAT_SCHEDULER = "djcelery.schedulers.DatabaseScheduler"  
