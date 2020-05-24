import os
import environ

# Environment defaults
env = environ.Env(
    DJANGO_DATABASES_DEFAULT=(dict, dict()),
    SECRET_KEY=(str, ''),
    DEBUG=(bool, True),
    ALLOWED_HOSTS=(list, list()),
    CELERY_BROKER=(str, ''),
    CELERY_RESULT_BACKEND=(str, ''),
    STATICFILES_DIRS=(list, list()),
    STATIC_ROOT=(str, ''),
    MEDIA_ROOT=(str, ''),
    MAIN_APP_NAME=(str, ''),
    DJANGO_LOG_DIR=(str, ''),
    LOCAL_MAIL_DIR=(str, ''),
)

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(BASE_DIR)

# Load .env file
environ.Env.read_env(os.path.join(ROOT, '.env'))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG')

ALLOWED_HOSTS = env('ALLOWED_HOSTS')

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
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

ROOT_URLCONF = env('MAIN_APP_NAME') + '.urls'

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

WSGI_APPLICATION = 'core.wsgi.application'

# Database
DATABASES = {
    'default': env('DJANGO_DATABASES_DEFAULT')
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.'
                'UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.'
                'MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.'
                'CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.'
                'NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = env('STATICFILES_DIRS')
STATIC_ROOT = env('STATIC_ROOT')

# Media
MEDIA_ROOT = env('MEDIA_ROOT')
MEDIA_URL = '/media/'

# Celery broker
CELERY_BROKER_URL = env('CELERY_BROKER')
CELERY_RESULT_BACKEND = env('CELERY_RESULT_BACKEND')

# Logging
LOG_DIR = env('DJANGO_LOG_DIR')
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': 'django [%(asctime)s] %(levelname)s '
                      '[%(name)s:%(lineno)s] %(message)s',
            'datefmt': '%d/%b/%Y %H:%M:%S'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },
        'sql_queries': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_DIR, 'sql_queries.log'),
            'maxBytes': 50000,
            'backupCount': 2,
            'formatter': 'standard',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'propagate': True,
        }
    },
}

if DEBUG:
    LOGGING['loggers']['django.db.backends'] = {
        'handlers': ['sql_queries'],
        'level': 'DEBUG',
    }

# Email
if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
    EMAIL_FILE_PATH = env('LOCAL_MAIL_DIR')
