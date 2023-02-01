from datetime import timedelta
import os
from pathlib import Path
import logging.config

BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-q-222jl54e)8c$5mdij2061g5p(sbfst%@o$h@@l&b+321!(5^"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


ROOT_URLCONF = "core.urls"
WSGI_APPLICATION = "core.wsgi.application"

# Application definition

THIRD_PARTY_APPS = [
    "rest_framework",
    "django_filters",
    "drf_spectacular",
    "djoser",
    "corsheaders",
]

LOCAL_APPS = [
    "users",
]

INSTALLED_APPS = (
    [
        "django.contrib.admin",
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.messages",
        "django.contrib.staticfiles",
    ]
    + THIRD_PARTY_APPS
    + LOCAL_APPS
)

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "core.middlewares.RequestResponseLoggerMiddleware",
]


TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(BASE_DIR, "core", "templates"),
        ],
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


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# ---------------------------------MEDIA AND STATIC ROOT AND URL-------------------------------------------------#
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATIC_URL = "/static/"

# ---------------------------------DEFAULT PRIMARY KEY FIELD TYPE-------------------------------------------------#
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ---------------------------------Auth User-------------------------------------------------#
AUTH_USER_MODEL = "users.User"

# ----------------------------------REST FRAMEWORK SETTINGS----------------------------------#

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
    ),
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_FILTER_BACKENDS": (
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ),
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": 10,
}


# ------------------------------SPECTACULAR CONFIG---------------------------------------------#
SPECTACULAR_SETTINGS = {
    "TITLE": "Core API",
    "DESCRIPTION": "Your project description",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "SCHEMA_PATH_PREFIX": "/api/",
}


# ---------------------------------SIMPLE JWT CONFIG-----------------------------------------#
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60000000),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "SOCIAL_TOKEN_DELTA": timedelta(days=1),
    "ALLOW_REFRESH_SOCIAL": False,
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": False,
    "UPDATE_LAST_LOGIN": True,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "VERIFYING_KEY": None,
    "AUDIENCE": None,
    "ISSUER": None,
    "AUTH_HEADER_TYPES": ("Bearer", "JWT"),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "JTI_CLAIM": "jti",
    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": timedelta(minutes=120),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),
}

# ----------------------------------------------LOGGING SETTINGS------------------------------------------------------
LOGGING_CONFIG = None  # This empties out Django's logging config

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "timed_file": {
            "level": "DEBUG",
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": "debug.log",
            "when": "midnight",  # Rotate log files at midnight
            "interval": 1,  # Rotate log files every day
            "backupCount": 7,  # Keep up to 7 backup log files
            "formatter": "verbose",
        },
    },
    "formatters": {
        "verbose": {
            "format": "%(asctime)s [%(levelname)s] %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "loggers": {
        "info_logger": {
            "handlers": ["timed_file"],
            "level": "INFO",
            "propagate": True,
        },
    },
}

logging.config.dictConfig(LOGGING)


# ----------------------------------------------EMAIL SETTINGS------------------------------------------------------
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.elasticemail.com"
EMAIL_USE_TLS = False
EMAIL_PORT = 2525
EMAIL_HOST_USER = "your-email"
EMAIL_HOST_PASSWORD = "your-password"

# ---------------------------------------------REDIS SETTINGS------------------------------------------------------
REDIS_HOST = "redis_server"
REDIS_PORT = 6379
REDIS_DB = 0
REDIS_PASSWORD = "redis-password"

# ---------------------------------------------CELERY SETTINGS------------------------------------------------------
import urllib.parse

encoded_password = urllib.parse.quote_plus(REDIS_PASSWORD)
CELERY_BROKER_URL = f"redis://:{encoded_password}@{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"
CELERY_RESULT_BACKEND = (
    f"redis://:{encoded_password}@{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"
)
CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = "Asia/Kathmandu"


# ------------------------------DJOSER CONFIG---------------------------------------------#
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
DOMAIN = "your-frontend-url.com"
SITE_NAME = "Core API"
DJOSER = {
    "SEND_ACTIVATION_EMAIL": True,
    "ACTIVATION_URL": "activate/{uid}/{token}/",
    "PASSWORD_RESET_CONFIRM_URL": "password/reset/confirm/{uid}/{token}/",
    "activation": "activation.html",
    "SERIALIZERS": {
        "user_create": "users.serializers.CustomUserSerializer",
        "current_user": "users.serializers.CurrentUserSerializer",
    },
}

# -------------------------------CORS CONFIG------------------------------------------------#
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = True
ALLOWED_HOSTS = ["*"]