"""
Django settings for coventGarden project.

Generated by 'django-admin startproject' using Django 4.2.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import os

# Email
import environ
from dotenv import load_dotenv
env = environ.Env()
load_dotenv()

FIRST_DAY_OF_WEEK = 1

  
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
#SECRET_KEY = 'django-insecure-t6xn!i_)c0l3g08x!c7hn(f0k^d3+j_91xjsyhtibbxuov$u-p'
SECRET_KEY = env('APP_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']
CSRF_TRUSTED_ORIGINS=['https://*.new.coventgarden.fr']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'studios',
    'django_select2',
    'tempus_dominus',
    'bootstrap_datepicker_plus',
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

ROOT_URLCONF = 'coventGarden.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
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

WSGI_APPLICATION = 'coventGarden.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.sqlite3',
#        'NAME': BASE_DIR / 'db.sqlite3',
#    }
#}
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': env('DB_NAME'),
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PASSWORD'),
        'HOST': env('DB_HOST'),
        'PORT': env('DB_PORT'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Paris'

USE_I18N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

"""
New
"""
# Custom user
AUTH_USER_MODEL = "studios.CustomUser"

# Redirection if user is not authenticated
# https://docs.djangoproject.com/en/3.2/topics/auth/default/#the-loginrequired-mixin
LOGIN_URL = "account_sign_in_form"

# Email
# Set DEBUG_EMAIL to True to test sending e-mails locally
DEBUG_EMAIL = False
if DEBUG_EMAIL:
    """
    Send mail to a local directory
    """
    EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
    EMAIL_FILE_PATH = BASE_DIR / 'sent_emails'
else:
    """
    Send mail using an email account
    """
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = env('EMAIL_HOST')
    EMAIL_PORT = env('EMAIL_PORT')
    EMAIL_HOST_USER = env('EMAIL_HOST_USER')
    EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
    EMAIL_USE_SSL = False
    EMAIL_USE_TLS = True
    DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

"""
Private
"""

# Store file
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# TOUT ÇA SERA À CHANGER POUR LE COMPTE DE CGS

# Stripe

STRIPE_PUBLIC_KEY = env('STRIPE_PUBLIC_KEY')
STRIPE_SECRET_KEY = env('STRIPE_SECRET_KEY')

# PRIX EN FONCTION DES HEURES
PRODUCT_PRICE_1H = env('PRODUCT_PRICE_1H')
PRODUCT_PRICE_2H = env('PRODUCT_PRICE_2H')
PRODUCT_PRICE_3H = env('PRODUCT_PRICE_3H')
PRODUCT_PRICE_4H = env('PRODUCT_PRICE_4H')
PRODUCT_PRICE_5H = env('PRODUCT_PRICE_5H')
PRODUCT_PRICE_6H = env('PRODUCT_PRICE_6H')
PRODUCT_PRICE_7H = env('PRODUCT_PRICE_7H')
PRODUCT_PRICE_8H = env('PRODUCT_PRICE_8H')


PRODUCT_PRICE = env('PRODUCT_PRICE')
REDIRECT_DOMAIN = "home"

# ---------- Required ----------
# pip3 install django-select2
# pip3 install stripe
# pip3 install six
# pip3 install django-tempus-dominus
# pip3 install django-bootstrap-datepicker-plus
# pip3 install django-environ
# pip3 install python-dotenv
# ------------------------------
