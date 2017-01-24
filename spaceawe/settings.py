"""
Django settings for spaceawe project.

Generated by 'django-admin startproject' using Django 1.8.8.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/

Deployment checklist:
https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/
"""

import os
import sys
import json
import copy
import operator

SHORT_NAME = 'spaceawe'
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PARENT_DIR = os.path.dirname(BASE_DIR)

sys.path.append(os.path.join(PARENT_DIR, 'django-apps'))

SECRETS_FILE = os.path.join(BASE_DIR, 'secrets.json')
if os.path.isfile(SECRETS_FILE):
    fdata = open(SECRETS_FILE)
    secrets = json.load(fdata)
    fdata.close()
else:
    raise 'No secrets found!'


DEBUG = False
DJANGO_SETTINGS_CONFIG = os.environ.get('DJANGO_SETTINGS_CONFIG', None)
if DJANGO_SETTINGS_CONFIG == 'DEV':
    DEBUG = True

# cannonical base URL for the website
SITE_URL = 'http://www.space-awareness.org'

ADMINS = (
    ('Vaclav Ehrlich', secrets['ADMIN_EMAIL']),
)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = secrets['SECRET_KEY']

ALLOWED_HOSTS = [
    'www.space-awareness.org',
    'www.space-awareness.eu',
    'beta.space-awareness.org',
    '10.10.10.10',
    '52.48.240.232',
    '50.17.214.96',
    '188.166.22.9',
    'spaceawe',
    'spaceawe.local',
    'localhost',  # for when I set DEBUG = False in development
]


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.redirects',

    'pipeline',

    'parler',
    'ckeditor',
    'taggit',
    'taggit_autosuggest',
    'el_pagination',

    'sorl.thumbnail',

    'django_mistune',

    'django_ext',
    'smartpages',
    'institutions',
    'spaceawe',
    'news',
    'spacescoops',
    'glossary',
    'activities',
    'games',
    'develop',
    'careers',
    'search',
    # 'spaceawe.apps.SpaceScoopConfig',
    # 'spaceawe.search',

)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    # 'CacheMiddleware'
    'django.middleware.locale.LocaleMiddleware',  # see https://docs.djangoproject.com/en/1.8/topics/i18n/translation/#how-django-discovers-language-preference
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.redirects.middleware.RedirectFallbackMiddleware',
)

SITE_ID = 1

ROOT_URLCONF = 'spaceawe.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # 'DIRS': [],
        'DIRS': [os.path.join(BASE_DIR, 'templates'), ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                # debug, sql_queries
                'django.template.context_processors.debug',
                # request
                'django.template.context_processors.request',
                # user, perms
                'django.contrib.auth.context_processors.auth',
                # messages, DEFAULT_MESSAGE_LEVELS
                'django.contrib.messages.context_processors.messages',
                # LANGUAGES, LANGUAGE_CODE
                'django.template.context_processors.i18n',
                # THUMBNAIL_ALIASES
                'django_ext.context_processors.thumbnail_aliases',
                # SITE_URL
                'django_ext.context_processors.site_url',
                # SECTIONS, CATEGORIES (spaceawe)
                'django_ext.context_processors.texts',
            ],
            'debug': False,
        },
    },
]

WSGI_APPLICATION = 'spaceawe.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'spaceawe',
        'USER': secrets['DATABASE_USER_PROD'],
        'PASSWORD': secrets['DATABASE_PASSWORD_PROD'],
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': 'spaceawe.sqlite3',
#     }
# }


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en'

LANGUAGES = (
    ('cs', 'Czech'),
    ('nl', 'Dutch'),
    ('en', 'English'),
    ('fr', 'French'),
    ('de', 'German'),
    ('el', 'Greek'),
    ('it', 'Italian'),
    ('pl', 'Polish'),
    ('ro', 'Romanian'),
    ('es', 'Spanish'),
    ('pt', 'Portuguese'),
)
LANGUAGES = sorted(LANGUAGES, key=operator.itemgetter(0))

# TIME_ZONE = 'UTC'
TIME_ZONE = 'Europe/Amsterdam'

USE_I18N = True
LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

USE_L10N = True
FORMAT_MODULE_PATH = (
    'formats',
)
# DATETIME_FORMAT = 'Y-m-d H:i:s'

USE_TZ = True


# Media

MEDIA_ROOT = os.path.join(PARENT_DIR, 'spaceawe_uploads')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = os.path.join(PARENT_DIR, 'spaceawe_static')

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(BASE_DIR, 'static/'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.FileSystemFinder',
    # 'django.contrib.staticfiles.finders.DefaultStorageFinder',
    'pipeline.finders.PipelineFinder',
)

STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'


# Email
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = secrets['EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD = secrets['EMAIL_HOST_PASSWORD']
EMAIL_PORT = 587
EMAIL_USE_TLS = True

DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
SERVER_EMAIL = DEFAULT_FROM_EMAIL
EMAIL_SUBJECT_PREFIX = '[space awareness] '


# Caching
USE_ETAGS = True  # Note: disable debug toolbar while testing!

# Pipeline
PIPELINE = {
    # 'PIPELINE_ENABLED': True,
    # 'JS_COMPRESSOR': None,
    # 'CSS_COMPRESSOR': None,
    'STYLESHEETS': {
        'styles': {
            'source_filenames': [
                'js/slick/slick.css',
                'js/slick/slick-theme.css',
                'css/main.css',
            ],
            'output_filename': 'css/spaceawe.min.css',
            'extra_context': {
                'media': 'screen',
            },
        },
        'print': {
            'source_filenames': [
                'css/print-activities.css',
            ],
            'output_filename': 'css/spaceawe.print.min.css',
            'extra_context': {
                'media': 'print',
            },
        }
    },
    'JAVASCRIPT': {
        'scripts': {
            'source_filenames': [
                'js/jquery-1.10.1.min.js',
                #'js/jquery-migrate-3.0.0.min.js',
                #'js/jquery.scrollTo.js',
                'js/jquery.event.special.js',
                #'js/jquery.scrollsnap.js',
                #'js/jquery.cycle2.js',
                'js/slick/slick.min.js',
                'el-pagination/js/el-pagination.js',
                'js/jquery.sharrre.min.js',
                'js/jquery.matchHeight.js',
                'js/scripts.js',
            ],
            'output_filename': 'js/spaceawe.min.js',
        }
    },
}

# Thumbnails
# http://sorl-thumbnail.readthedocs.org/en/latest/reference/settings.html
THUMBNAIL_KVSTORE = 'sorl.thumbnail.kvstores.redis_kvstore.KVStore'
THUMBNAIL_DBM_FILE = os.path.join(PARENT_DIR, 'usr/redis/thumbnails_spaceawe')
# THUMBNAIL_ENGINE = 'sorl.thumbnail.engines.convert_engine.Engine'  #TODO: revisit this choice
THUMBNAIL_ENGINE = 'sorl.thumbnail.engines.pil_engine.Engine'  #TODO: revisit this choice
THUMBNAIL_KEY_PREFIX = 'sorl-thumbnail-spaceawe'
THUMBNAIL_PRESERVE_FORMAT = 'True'
# THUMBNAIL_ALTERNATIVE_RESOLUTIONS = [1.5, 2]
THUMBNAIL_ALIASES = {
    # 'article_feature': '880x410',
    # 'article_cover': '680x400',
    # 'article_thumb': '320',
    # 'article_thumb_inline': '198x200',
    'scoop_source': 'x60',
    'list_thumb': '380x250',
    'spread': '1024',
}

# CK editor
CKEDITOR_CONFIGS = {
    ## see http://docs.cksource.com/CKEditor_3.x/Developers_Guide/Toolbar

    # 'default': {
    #     'fillEmptyBlocks': False,
    #     'toolbar': 'Custom',
    #     'toolbar_Custom': [
    #         ['Source', ],
    #         ['Bold', 'Italic', '-', 'Subscript', 'Superscript', '-', 'Undo', 'Redo', 'RemoveFormat', ],
    #         ['Glossary', ],
    #         ['Link', 'Unlink', ],
    #         # ['Image', ],
    #         ['BidiLtr', 'BidiRtl', ],
    #     ],
    #     # 'extraPlugins': 'codesnippet',
    #     'extraPlugins': 'glossary',
    #     'contentsCss': ['%sckeditor/ckeditor/contents.css' % STATIC_URL, '%scss/ckeditor-content.css' % STATIC_URL],
    # },
    # 'small': {
    #     'fillEmptyBlocks': False,
    #     'toolbar': 'Custom',
    #     'toolbar_Custom': [
    #         ['Source', ],
    #         ['Bold', 'Italic', '-', 'Subscript', 'Superscript', '-', 'Undo', 'Redo', 'RemoveFormat', ],
    #         ['Link', 'Unlink', ],
    #         # ['Image', ],
    #         ['BidiLtr', 'BidiRtl', ],
    #     ],
    #     'height': 100,
    # },
    'smartpages': {
        'fillEmptyBlocks': False,
        'toolbar': 'Custom',
        'toolbar_Custom': [
            ['Source', ],
            ['Format', ],
            ['Bold', 'Italic', '-', 'Underline', 'Subscript', 'Superscript', '-', 'Undo', 'Redo', 'RemoveFormat', ],
            ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', ],
            ['Link', 'Unlink', ],
            ['Image', 'Table', 'SpecialChar', ],
            ['Maximize', 'ShowBlocks', ],
            ['BidiLtr', 'BidiRtl', ],
        ],
        'width': 845,
    },
    'default': {
        'fillEmptyBlocks': False,
        'toolbar': 'Custom',
        'toolbar_Custom': [
            ['Source', ],
            ['Format', ],
            ['Bold', 'Italic', '-', 'Subscript', 'Superscript', '-', 'Undo', 'Redo', 'RemoveFormat', ],
            ['Link', 'Unlink', ],
            # ['Image', ],
            ['BidiLtr', 'BidiRtl', ],
        ],
    },
}
CKEDITOR_CONFIGS['small'] = copy.deepcopy(CKEDITOR_CONFIGS['default'])
CKEDITOR_CONFIGS['small']['height'] = 100

CKEDITOR_CONFIGS['spacescoop'] = copy.deepcopy(CKEDITOR_CONFIGS['default'])
# CKEDITOR_CONFIGS['spacescoop']['extraPlugins'] = 'glossary'
# CKEDITOR_CONFIGS['spacescoop']['contentsCss'] = ['%sckeditor/ckeditor/contents.css' % STATIC_URL, '%scss/ckeditor-content.css' % STATIC_URL]
# CKEDITOR_CONFIGS['spacescoop']['toolbar_Custom'].insert(2, ['Glossary', ])

# Bleach
BLEACH_ALLOWED_TAGS = ('sup', 'sub', 'br', )
BLEACH_ALLOWED_ATTRIBUTES = {}
BLEACH_ALLOWED_STYLES = {}

# Woosh Search
WHOOSH_INDEX_PATH = os.path.join(PARENT_DIR, '/home/web/usr/whoosh_index')

# # Celery
# BROKER_URL = 'redis://localhost:6379/0'
# # CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
# CELERY_TASK_SERIALIZER = 'pickle'  # default serializer used by the decorators
# CELERY_ACCEPT_CONTENT = ['pickle']  # serializers accepted by the deamon
# # TODO: use celery

# parler
# http://django-parler.readthedocs.org/en/latest/
# https://github.com/edoburu/django-parler
PARLER_LANGUAGES = {
    # SITE_ID: ( {'code':'en'}, { ...
    1: [({'code': code}) for (code, name) in LANGUAGES],
    'default': {
        'fallbacks': ['en'],
        'hide_untranslated': False,   # False is the default; let .active_translations() return fallbacks too.
    }
}

if DJANGO_SETTINGS_CONFIG == 'DEV':
    # TIME_ZONE = 'Europe/Lisbon'
    STATIC_ROOT = '/tmp'
    TEMPLATES[0]['OPTIONS']['debug'] = True  # TEMPLATE_DEBUG
    # debug toolbar
    # DEBUG_TOOLBAR_PATCH_SETTINGS = False
    # INTERNAL_IPS = ('127.0.0.1',)
    # MIDDLEWARE_CLASSES += (
    #     'debug_toolbar.middleware.DebugToolbarMiddleware',
    # )
    INSTALLED_APPS += (
        'debug_toolbar',
    )
    DEBUG_TOOLBAR_CONFIG = {
        'INTERCEPT_REDIRECTS': False,
        'JQUERY_URL':'',
    }
    EMAIL_SUBJECT_PREFIX = '[spaceawe dev] '

    THUMBNAIL_KVSTORE = 'sorl.thumbnail.kvstores.dbm_kvstore.KVStore'  # in-memory sorl KV store
    THUMBNAIL_DUMMY = True
    # THUMBNAIL_DUMMY_SOURCE = 'http://placekitten.com/%(width)s/%(height)s'
    # THUMBNAIL_DUMMY_RATIO = 1.5

    WHOOSH_INDEX_PATH = os.path.join(PARENT_DIR, 'usr/whoosh_index')
    CELERY_ALWAYS_EAGER = True  # Tasks are run synchronously
elif DJANGO_SETTINGS_CONFIG == 'PROD':
    pass

else:
    if DJANGO_SETTINGS_CONFIG:
        raise EnvironmentError(1, 'DJANGO_SETTINGS_CONFIG environment variable set to invalid value: %s' % DJANGO_SETTINGS_CONFIG)
    else:
        raise EnvironmentError(1, 'DJANGO_SETTINGS_CONFIG environment variable not set')


from django.contrib import admin
admin.site.site_header = 'Space Awareness: Administration'
