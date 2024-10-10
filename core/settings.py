"""
Django settings for core project.

"""

from datetime import timedelta
from pathlib import Path

import dj_database_url
from environ import Env

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

env = Env()
env.read_env(BASE_DIR / ".env")

DEBUG = env("DEBUG", cast=bool)
SECRET_KEY = env("SECRET_KEY")
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")

# CORS settings
CORS_ALLOW_ALL_ORIGINS = env("CORS_ALLOW_ALL_ORIGINS", cast=bool, default=True)
# CORS_ALLOWED_ORIGINS = env.list("CORS_ALLOWED_ORIGINS")

# Application definition

INSTALLED_APPS = [
    # "daphne",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # third-party apps
    "storages",
    "rest_framework",
    "phonenumber_field",
    "channels",
    "django_celery_beat",
    "django_celery_results",
    "drf_spectacular",
    "drf_spectacular_sidecar",
    # native apps
    "apps.user.apps.UserConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "core.urls"


TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
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


# WSGI and ASGI Applications
WSGI_APPLICATION = "core.wsgi.application"
ASGI_APPLICATION = "core.asgi.application"

DB_URL = (
    f"{env('DB_SCHEMA', cast=str)}://"  # Databse Schema
    f"{env('DB_USER', cast=str)}:"  # Database User
    f"{env('DB_PASSWORD', cast=str)}"  # Database User password
    f"@{env('DB_HOST')}:"  # Database Host (IP)
    f"{env('DB_PORT', cast=int)}/"  # Database Port
    f"{env('DB_NAME', cast=str)}"  # Database Name
)
if not DEBUG:
    DB_URL = env("DB_URL", cast=str)

DATABASES = {
    "default": dj_database_url.parse(
        DB_URL,
        conn_max_age=600,
        conn_health_checks=True,
    ),
}

ADMINS = [
    ("Atef Hesham", "atefhesham45@gmail.com"),
]

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

# DRF settings

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly"
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_FILTER_BACKENDS": ["django_filters.rest_framework.DjangoFilterBackend"],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

ACCESS_TOKEN_EXPIRY_MINUTES = env("ACCESS_TOKEN_EXPIRY_MINUTES", cast=int)
REFRESH_TOKEN_EXPIRY_DAYS = env("REFRESH_TOKEN_EXPIRY_DAYS", cast=int)
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=ACCESS_TOKEN_EXPIRY_MINUTES),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=REFRESH_TOKEN_EXPIRY_DAYS),
}


SPECTACULAR_SETTINGS = {
    "TITLE": "Django Starterkit API",
    "DESCRIPTION": "Django Starterkit API schema and documentation.",
    "VERSION": "0.1.0",
    "CONTACT": {
        "name": "Atef hesham",
        "url": "https://atfhshm.com",
        "email": "its.atfhshm@gmail.com",
    },
    "SERVE_INCLUDE_SCHEMA": False,
    "COMPONENT_SPLIT_REQUEST": True,
    "SWAGGER_UI_DIST": "SIDECAR",
    "SWAGGER_UI_FAVICON_HREF": "SIDECAR",
    "REDOC_DIST": "SIDECAR",
}


# Django silk settings (dev and staging only)
if DEBUG:
    MIDDLEWARE.append(
        "silk.middleware.SilkyMiddleware",
    )
    INSTALLED_APPS.append(
        "silk",
    )


LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static assets (image, css, js, fonts, icons, etc.)

STATICFILE_DIR = BASE_DIR.joinpath("static/")
STATICFILES_DIRS = (STATICFILE_DIR,)

# Static all static assets (uploads and static assets)
STATIC_ROOT = BASE_DIR.joinpath("staticfiles/")

STATIC_URL = "/static/"

# User media uploads

MEDIA_URL = "/uploads/"
MEDIA_ROOT = BASE_DIR.joinpath("uploads/")

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "user.User"

# Frontend url
FRONTEND_URL = env("FRONTEND_BASE_URL", cast=str, default="localhost:3000")

# The password reset time is 2 hours
PASSWORD_RESET_TIMEOUT = 60 * 60 * 2

# Redis
REDIS_URL = env("REDIS_URL", cast="str", default="redis://redis:6379")

# Caching
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_URL + "/0",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    }
}

# Celery
CELERY_BROKER_URL = REDIS_URL
CELERY_RESULT_BACKEND = REDIS_URL
CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = TIME_ZONE
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60

CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers.DatabaseScheduler"


# Emails
if DEBUG:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

if not DEBUG:
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_HOST = env("EMAIL_HOST", cast=str)
    EMAIL_PORT = env("EMAIL_PORT", cast=int)
    EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD", cast=str)
    EMAIL_HOST_USER = env("EMAIL_HOST_USER", cast=str)
    DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL", cast=str)
    SERVER_EMAIL = env("SERVER_EMAIL", cast=str)
    EMAIL_USE_TLS = False
    EMAIL_USE_SSL = False


# production staticfile and media file storage configuration
if not DEBUG:
    # AWS S3 (simple storage service) configurations
    AWS_ACCESS_KEY_ID = env("AWS_ACCESS_KEY_ID", default="minio")
    AWS_SECRET_ACCESS_KEY = env("AWS_SECRET_ACCESS_KEY", default="minio123")
    AWS_STORAGE_BUCKET_NAME = env("AWS_STORAGE_BUCKET_NAME", default="uploads")
    AWS_S3_ENDPOINT_URL = env("AWS_S3_ENDPOINT_URL", default="http://minio:9000")
    AWS_S3_USE_SSL = False
    AWS_S3_OBJECT_PARAMETERS = {
        "CacheControl": "max-age=86400",
    }
    AWS_S3_FILE_OVERWRITE = False
    AWS_DEFAULT_ACL = "public-read"
    AWS_QUERYSTRING_AUTH = False
    AWS_S3_VERITY = True

    # Dirty fix for minio in local development
    MINIO_ACCESS_URL = env("MINIO_ACCESS_URL", default=None)
    if MINIO_ACCESS_URL:
        AWS_S3_URL_PROTOCOL = "http:"
        AWS_S3_CUSTOM_DOMAIN = MINIO_ACCESS_URL

    STORAGES = {
        "default": {
            "BACKEND": "core.storages.UploadS3Storage",
        },
        "staticfiles": {
            "BACKEND": "core.storages.StaticS3Storage",
        },
    }

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "root": {"level": "INFO", "handlers": ["default"]},
    "formatters": {
        "django.server": {
            "()": "django.utils.log.ServerFormatter",
            "format": "[{server_time}] {message}",
            "style": "{",
        },
        "json": {
            "()": "core.logging.JsonFormatter",
            "datefmt": "%Y-%m-%dT%H:%M:%SZ",
            "format": (
                "%(asctime)s %(levelname)s %(lineno)s %(message)s %(name)s "
                + "%(pathname)s %(process)d %(threadName)s"
            ),
        },
        "celery_json": {
            "()": "core.logging.JsonCeleryFormatter",
            "datefmt": "%Y-%m-%dT%H:%M:%SZ",
            "format": (
                "%(asctime)s %(levelname)s %(celeryTaskId)s %(celeryTaskName)s "
            ),
        },
        "celery_task_json": {
            "()": "core.logging.JsonCeleryTaskFormatter",
            "datefmt": "%Y-%m-%dT%H:%M:%SZ",
            "format": (
                "%(asctime)s %(levelname)s %(celeryTaskId)s %(celeryTaskName)s "
                "%(message)s "
            ),
        },
        "verbose": {
            "format": (
                "%(asctime)s %(levelname)s %(name)s %(message)s "
                "[PID:%(process)d:%(threadName)s]"
            )
        },
    },
    "handlers": {
        "default": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose" if DEBUG else "json",
        },
        "django.server": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "django.server" if DEBUG else "json",
        },
        "celery_app": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "verbose" if DEBUG else "celery_json",
        },
        "celery_task": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "verbose" if DEBUG else "celery_task_json",
        },
        "null": {
            "class": "logging.NullHandler",
        },
        "mail_admins": {
            "level": "ERROR",
            "class": "django.utils.log.AdminEmailHandler",
            "include_html": True,
        },
    },
    "loggers": {
        "django": {"level": "INFO", "propagate": True},
        "django.server": {
            "handlers": ["django.server"],
            "level": "INFO",
            "propagate": False,
        },
        "celery.app.trace": {
            "handlers": ["celery_app"],
            "level": "INFO",
            "propagate": False,
        },
        "celery.task": {
            "handlers": ["celery_task"],
            "level": "INFO",
            "propagate": False,
        },
        "core": {"level": "DEBUG", "propagate": True},
    },
}
