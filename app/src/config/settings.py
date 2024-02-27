import os
from dotenv import load_dotenv
from pathlib import Path

# load .env file
load_dotenv('.env')

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-@-=!bat0wx^&qtziu8go(09(z5k(b(jb2(d_^v9l9v$)b1)q6-')

DEBUG = os.getenv('DEBUG', True)

# production state
PRODUCTION = os.getenv('PRODUCTION', False)

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '127.0.0.1').split('|')

CSRF_TRUSTED_ORIGINS = os.getenv('CSRF_TRUSTED', 'http://127.0.0.1:8000').split('|')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Apps
    'core',
    'account',
    'public',
    'support',
    'notification',

    # Department apps
    'departments.general',
    'departments.financial',
    'departments.control_project',
    'departments.control_quality',
    'departments.commerce',
    'departments.warehouse',
    'departments.production',
    'departments.technical',

    # Third party apps
    'django_q',
    'django_render_partial',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'core.middleware.UserIsAuthenticated'
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
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

WSGI_APPLICATION = 'config.wsgi.application'

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('DATABASE_NAME'),
        'USER': os.getenv('DATABASE_USER'),
        'PASSWORD': os.getenv('DATABASE_PASSWORD'),
        'HOST': os.getenv('DATABASE_HOST'),
        'PORT': os.getenv('DATABASE_PORT'),
    }
}



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

LANGUAGE_CODE = 'fa-ir'

TIME_ZONE = 'Asia/Tehran'

USE_I18N = True

USE_L10N = False

USE_TZ = False

STATIC_URL = 'static/'
STATIC_ROOT = '/app/volumes/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static'
]

MEDIA_URL = 'media/'
MEDIA_ROOT = '/app/volumes/media/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

Q_CLUSTER = {
    'name': 'django-q',
    'timeout': 60,
    'orm': 'default',
}

REDIS_CONFIG = {
    'HOST': os.getenv('REDIS_HOST', 'localhost'),
    'PORT': os.getenv('REDIS_PORT', '6379')
}

AUTH_USER_MODEL = 'account.User'  # custom user model

LOGIN_URL = '/u/login'

EXCEPT_USER_AUTH_URLS = [
    '/u/login',
    '/u/reset-password',
    '/u/reset-password/send-link',
    '/admin',
    '/project',
]

DATE_FORMAT = "Y-m-d"
