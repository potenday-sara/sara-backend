"""
Django settings for sara_server project.

Generated by 'django-admin startproject' using Django 4.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import os
from pathlib import Path

from celery.schedules import crontab

ENV = os.environ.get("ENV", "DEV")

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-1lzvaw1vv7s=b+21t&q85b)82jh8^js++1wg21z!3pd&_r_z7t"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True if ENV == "DEV" else False

ALLOWED_HOSTS = ["*"]

CSRF_TRUSTED_ORIGINS = ["https://api.sara-mara.com"]


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "corsheaders",
    "drf_yasg",
    "rangefilter",
    "questions",
    "status",
    "rank",
    "shop",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "corsheaders.middleware.CorsMiddleware",
]

if ENV == "DEV":
    CORS_ALLOW_ALL_ORIGINS = True
else:
    CORS_ALLOWED_ORIGINS = [
        "https://sara-mara.com",
        "https://www.sara-mara.com",
        "https://stage.sara-mara.com",
    ]

ROOT_URLCONF = "sara_server.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "sara_server.wsgi.application"

APPEND_SLASH = False

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

if ENV == "DEV":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.environ["DB_NAME"],
            "HOST": os.environ["DB_HOST"],
            "PORT": os.environ["DB_PORT"],
            "USER": os.environ["DB_USER"],
            "PASSWORD": os.environ["DB_PASSWORD"],
        }
    }


# Cache
if ENV == "DEV":
    REDIS_HOST = "localhost"
    REDIS_PORT = "63791"
else:
    REDIS_HOST = os.environ["REDIS_HOST"]
    REDIS_PORT = os.environ["REDIS_PORT"]


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "ko-kr"

TIME_ZONE = "Asia/Seoul"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
OPENAI_MODEL = "gpt-4o-2024-05-13"

CELERY_BROKER_URL = "amqp://rabbitmq:5672/"
CELERY_BEAT_SCHEDULE = {
    "send_slack_message_every_day": {
        "task": "questions.tasks.task_send_slack_message",
        "schedule": crontab(hour="9", minute="0"),  # 매일 오전 9시에 실행
    },
}

SLACK_TOKEN = os.environ["SLACK_TOKEN"]

COUPANG_API_KEY = os.environ["COUPANG_API_KEY"]
COUPANG_API_SECRET = os.environ["COUPANG_API_SECRET"]
COUPANG_API_HOST = "https://api-gateway.coupang.com"
COUPANG_API_BASE_PATH = "/v2/providers/affiliate_open_api/apis/openapi/v1"

ALIEXPRESS_API_KEY = os.environ["ALIEXPRESS_API_KEY"]
ALIEXPRESS_API_SECRET = os.environ["ALIEXPRESS_API_SECRET"]
ALIEXPRESS_API_TRACKING_ID = os.environ["ALIEXPRESS_API_TRACKING_ID"]

