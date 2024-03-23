"""
Django settings for web project.

Generated by 'django-admin startproject' using Django 3.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
from .env import ENV_VARS
from dotenv import load_dotenv

from django.conf.global_settings import DATETIME_INPUT_FORMATS

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# DEV_SETTINGS = 1
# PROD_SETTINGS = 2

# # Single point setup for dev/prod changes
# CURRENT_SETTINGS = ENV_VARS.get('PRODUCTION')

# if CURRENT_SETTINGS == DEV_SETTINGS:
#     dotenv_file = os.path.join(BASE_DIR, '.env.dev')
# elif CURRENT_SETTINGS == PROD_SETTINGS:
#     dotenv_file = os.path.join(BASE_DIR, '.env.prod')

# if os.path.isfile(dotenv_file):
#     load_dotenv(dotenv_file)
# else:
#     print('.env file not found \nMake sure it is located in the kisaweb/web directory')

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ENV_VARS.get('SECRET_KEY')

# bool() is required in DEBUG for LIBSASS_SOURCE_COMMENTS (which sets internally to the value of DEBUG)
#       to be a bool value. Else, TypeError('source_comments must be bool, not 1') is raised by sass.py
#       which is called by django_compress/django_libsass.

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = not ENV_VARS.get('PRODUCTION')

ALLOWED_HOSTS = ENV_VARS.get('ALLOWED_HOSTS')
CORS_ALLOWED_ORIGINS = ENV_VARS.get('CORS_ALLOWED_ORIGINS')

# Application definition

INSTALLED_APPS = [
    # 'grappelli',
    # 'jet.dashboard',  # PyPi django-3-jet (needs to be before 'jet')
    # 'jet',  # PyPi django-3-jet (needs to be before 'django.contrib.admin')
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "corsheaders",
    'rest_framework',

    ## ---- Third Party Libraries ---- ##
    'maintenance_mode',  # PyPi django-maintenance-mode (this needs to be before any custom apps)
    'compressor',  # PyPi django-compressor
    'tinymce',  # PyPi django-richtextfield
    'crispy_forms',  # PyPi django-crispy-forms
    'docs',  # PyPi django-docs
    'phone_field',  # PyPi django-phone-field
    'adminsortable',
    "django_pagination_bootstrap", #pagination for multimedia page,
    'django_draftjs',

    ## ---- Created by KISA webteam ---- ##
    'core',  # core pages (eg. homepage, about page, etc)
    'sso',
    'events',
    'election',
    'aboutus',
    'multimedia',
    'blog',
    'faq',
    'important_links',
    'url_shortener',
    'alumni',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "django_pagination_bootstrap.middleware.PaginationMiddleware", #django_pagination_bootstrap middleware
    'maintenance_mode.middleware.MaintenanceModeMiddleware',  # PyPi django-maintenance-mode (This needs to be the last middleware)
]

ROOT_URLCONF = 'web.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'admin/templates'),
            os.path.join(BASE_DIR),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',  # required by django-3-jet
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.static',
                'django.contrib.messages.context_processors.messages',
                'maintenance_mode.context_processors.maintenance_mode',  # PyPi django-maintenance-mode
                "django.template.context_processors.request", # django_pagination_bootstrap context provider
            ],
        },
    },
]

WSGI_APPLICATION = 'web.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    # },
    'default' : {
        'ENGINE'    : 'django.db.backends.postgresql',
        'NAME'      : ENV_VARS.get('DB_NAME'),
        'USER'      : ENV_VARS.get('DB_USER'),
        'PASSWORD'  : ENV_VARS.get('DB_PASSWORD'),
        'HOST'      : ENV_VARS.get('DB_HOST'),
        'PORT'      : ENV_VARS.get('DB_PORT')
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_L10N = False

# USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'collectstatic')

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DATETIME_INPUT_FORMATS += [
    '%Y-%m-%d %I:%M %p',  # 2020-01-20 06:30 PM
    '%Y/%m/%d',  # 2020/01/20
    '%Y-%m-%d %H:%M',  # 2020-01-20 13:30
    '%Y-%m-%d',  # 2020-01-20
]

# Custom User model
AUTH_USER_MODEL = 'sso.User'

# X_FRAME_OPTIONS = 'SAMEORIGIN'  # Required by django-3-jet dashboard


## -- django-compressor settings -- ##
COMPRESS_PRECOMPILERS = [
    ('text/x-scss', 'django_libsass.SassCompiler'),
]
COMPRESS_ENABLED = True
## ------------------------------- ##


## -- django-crispy-forms settings -- ##
CRISPY_TEMPLATE_PACK = 'bootstrap4'
## ---------------------------------- ##


## -- django-docs settings -- ##
DOCS_ROOT = os.path.join(BASE_DIR, 'docs/build/html')
DOCS_ACCESS = 'staff'
## -------------------------- ##



# sso

KSSO_CLIENT_ID = os.environ['KSSO_CLIENT_ID']
KSSO_SA_AES_ID_SECRET = os.environ['KSSO_SECRET_KEY']
KSSO_LOGIN_URL = "https://iam2.kaist.ac.kr/api/sso/commonLogin"
KSSO_LOGOUT_URL = "https://iam2.kaist.ac.kr/api/sso/logout"
KSSO_ORIGIN = "https://iam2.kaist.ac.kr"

## -- django-maintenance-mode settings -- ##
# (default values in https://github.com/fabiocaccamo/django-maintenance-mode)

MAINTENANCE_MODE = None  # Toggle (True/None) this according to need
MAINTENANCE_MODE_IGNORE_ADMIN_SITE = True
MAINTENANCE_MODE_IGNORE_STAFF = False
MAINTENANCE_MODE_IGNORE_SUPERUSER = False

MAINTENANCE_MODE_IGNORE_IP_ADDRESSES = tuple(os.environ.get('MAINTENANCE_MODE_IGNORE_IP', '').split())

# Example: https://github.com/fabiocaccamo/django-maintenance-mode/issues/21
# Put comma at end (to make it a tuple if one element) and put '/' in front and at end of url (enclosed by '^...$')
MAINTENANCE_MODE_IGNORE_URLS = (r'^/$', r'^/important-links$', r'^/course-resources$')

MAINTENANCE_MODE_IGNORE_TESTS = True
MAINTENANCE_MODE_TEMPLATE = 'core/503.html'

## -------------------------------------- ##

TINYMCE_DEFAULT_CONFIG = {
    "height": "600px",
    "menubar": "file edit view insert format tools table help",
    "plugins": "advlist autolink lists link image charmap print preview anchor searchreplace visualblocks code emoticons"
    "fullscreen insertdatetime media table paste code help wordcount spellchecker",
    "toolbar": "undo redo | bold italic underline strikethrough | fontselect fontsizeselect formatselect | alignleft "
    "aligncenter alignright alignjustify | outdent indent |  numlist bullist checklist | forecolor "
    "backcolor casechange permanentpen formatpainter removeformat | pagebreak | charmap emoticons | "
    "fullscreen  preview save print | insertfile image media pageembed template link anchor codesample | "
    "a11ycheck ltr rtl | showcomments addcomment code",
    "custom_undo_redo_levels": 10,
}

X_FRAME_OPTIONS = 'DENY'

# Url Shortener Url Settings
URL_SHORTENER_PREFIX    = 'short-link'

DEFAULT_AUTO_FIELD  = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'core.utils.StrictCSRFSessionAuthentication',
    ],

    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
        ],

    'DEFAULT_THROTTLE_CLASSES': [
        'core.throttling.ScopedRateThrottle',
    ],

    'DEFAULT_THROTTLE_RATES': {
        'usernamecheck': '40/day',
        'verification': '5/day'
    },

    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
}
