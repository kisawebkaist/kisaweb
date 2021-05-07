"""
Django settings for web project.

Generated by 'django-admin startproject' using Django 3.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
from dotenv import load_dotenv

from django.conf.global_settings import DATETIME_INPUT_FORMATS

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

DEV_SETTINGS = 1
PROD_SETTINGS = 2

# Single point setup for dev/prod changes
CURRENT_SETTINGS = PROD_SETTINGS

if CURRENT_SETTINGS == DEV_SETTINGS:
    dotenv_file = os.path.join(BASE_DIR, '.env.dev')
elif CURRENT_SETTINGS == PROD_SETTINGS:
    dotenv_file = os.path.join(BASE_DIR, '.env.prod')

if os.path.isfile(dotenv_file):
    load_dotenv(dotenv_file)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['SECRET_KEY']

# bool() is required in DEBUG for LIBSASS_SOURCE_COMMENTS (which sets internally to the value of DEBUG)
#       to be a bool value. Else, TypeError('source_comments must be bool, not 1') is raised by sass.py
#       which is called by django_compress/django_libsass.

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(int(os.environ.get('DJANGO_DEBUG', default=0)))

ALLOWED_HOSTS = os.environ['DJANGO_ALLOWED_HOSTS'].split()


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

    ## ---- Third Party Libraries ---- ##
    'maintenance_mode',  # PyPi django-maintenance-mode (this needs to be before any custom apps)
    'compressor',  # PyPi django-compressor
    'tinymce',  # PyPi django-richtextfield
    'crispy_forms',  # PyPi django-crispy-forms
    'docs',  # PyPi django-docs
    'phone_field',  # PyPi django-phone-field

    ## ---- Created by KISA webteam ---- ##
    'core',  # core pages (eg. homepage, about page, etc)
    'events',
    'election',
    'sso',  # contains the User model
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
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
                'django.contrib.messages.context_processors.messages',
                'maintenance_mode.context_processors.maintenance_mode',  # PyPi django-maintenance-mode

                # -- Created by KISA Team -- #
                # 'election.context_processors.navbar_election_link_visible',
                'core.context_processors.footer',
                'core.context_processors.navbar',
                'core.context_processors.empty_queryset',
                'core.context_processors.login_type',
            ],
        },
    },
]

WSGI_APPLICATION = 'web.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',
    },
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

USE_TZ = True


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


## -- SSO -- ##
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'homepage'
LOGOUT_REDIRECT_URL = 'homepage'

# TODO: Resolve dependencies on below two variables and delete them
LOGIN_DEV = DEV_SETTINGS
LOGIN_PROD = PROD_SETTINGS

KISA_AUTH_METHOD = LOGIN_DEV
## --------- ##


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