# Django settings for lib project.
import os, sys
PROJECT_ROOT_PATH = os.getcwd()

#LOCAL SETTINGS
PRODUCTION = False
DEBUG = True
TESTING = True if len(sys.argv) >= 2 and sys.argv[1] == 'test' else False

DOMAIN_NAME = 'yourdomain.com'
DOMAIN = 'http://127.0.0.1:8000'
INTERNAL_IPS = ('127.0.0.1',)

ROOT_TEMPLATE_DIR = PROJECT_ROOT_PATH + '/web/templates' #Path to '*PROJECT_DIR*/lib/public/templates'

# DB_ENGINE = 'django.db.backends.postgresql_psycopg2'
DB_ENGINE = 'django.db.backends.sqlite3'
DB_NAME = PROJECT_ROOT_PATH + '/project-db.sqlite'
DB_USER = ''
DB_PASSWORD = ''
DB_HOST = ''
DB_PORT = ''


# Heroku prefers Postgres. Setup an off-site mysql instance, http://addons.heroku.com/cleardb, or postgres.
DATABASES = {
        'default': {
            'ENGINE': DB_ENGINE, # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
            'NAME': DB_NAME,                      # Or path to database file if using sqlite3.
            'USER': DB_USER,                      # Not used with sqlite3.
            'PASSWORD': DB_PASSWORD,                  # Not used with sqlite3.
            'HOST': DB_HOST,                      # Set to empty string for localhost. Not used with sqlite3.
            'PORT': DB_PORT,                      # Set to empty string for default. Not used with sqlite3.
            }
        }


STATIC_URL = '/public/'
MEDIA_URL = '/public/media/'

# Do not change STATIC_ROOT to /web/public/, it will break both dev and production
STATIC_ROOT = '' + PROJECT_ROOT_PATH + '/web/static/'
MEDIA_ROOT = '' + PROJECT_ROOT_PATH + '/web/public/media/'

if TESTING:
    import warnings
    warnings.filterwarnings("ignore", r"DateTimeField received a naive datetime", RuntimeWarning, r'django\.db\.models\.fields') 
    SOUTH_TESTS_MIGRATE = False
    EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'

if os.environ.get('DJANGO_ENV', False) == 'production':
    #Place Heroku / Production settings in here
    PRODUCTION = True
    DEBUG = True

    MEDIA_ROOT = ''
    MEDIA_URL = '/media/'

    import dj_database_url
    DATABASES['default'] =  dj_database_url.config()

    # Live Production site on Heroku
    if DOMAIN[0:5] == 'https': 
        CSRF_COOKIE_SECURE = True
        SESSION_COOKIE_SECURE = True

    # Setting for https from Heroku: https://devcenter.heroku.com/articles/getting-started-with-django#django-settings
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


SSL_CONNECTIONS = True if os.environ.get('SSL_CONNECTIONS', 'False').lower() == 'true' else False

REST_FRAMEWORK = {
    'DEFAULT_MODEL_SERIALIZER_CLASS': 'rest_framework.serializers.ModelSerializer',

    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.UnicodeJSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),
    'TEST_REQUEST_DEFAULT_FORMAT': 'json'
}


LOGIN_REDIRECT_URL = '/profile/'
LOGIN_URL = '/login/'
LOGOUT_URL = '/logout/'

TEMPLATE_DEBUG = DEBUG

AUTH_PROFILE_MODULE = 'accounts.UserProfile'

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS


# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
USE_TZ = True
TIME_ZONE = 'US/Pacific'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
# MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
# MEDIA_URL = ''

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
ADMIN_MEDIA_PREFIX = '/public/admin/'

# Additional locations of static files
STATICFILES_DIRS = (
    '' + PROJECT_ROOT_PATH + '/web/public/',
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '8$dti!!$h97j51=d1pic^^#3f)tl$tu9b_cy)_i)%6!wg5rl^9'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

if SSL_CONNECTIONS:
    MIDDLEWARE_CLASSES = ('sslify.middleware.SSLifyMiddleware',)
else:
    MIDDLEWARE_CLASSES = ()

MIDDLEWARE_CLASSES += (
    'django.middleware.transaction.TransactionMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'util.debug.DebugFooter',
)

if DEBUG:
    MIDDLEWARE_CLASSES += ('util.debug.DisableCSRF',)

AUTHENTICATION_BACKENDS = (
    'util.backends.EmailOrUsernameModelBackend',
    'django.contrib.auth.backends.ModelBackend',
)

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    ROOT_TEMPLATE_DIR,
    ROOT_TEMPLATE_DIR + '/common',
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.request",
    "django.contrib.messages.context_processors.messages"
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.flatpages',
    'django.contrib.markup',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',

    'accounts',

	'south',
    'django_extensions',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'handlers': {
#         'mail_admins': {
#             'level': 'ERROR',
#             'class': 'django.utils.log.AdminEmailHandler'
#         }
#     },
#     'loggers': {
#         'django.request': {
#             'handlers': ['mail_admins'],
#             'level': 'ERROR',
#             'propagate': True,
#         },
#     }
# }
