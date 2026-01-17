from pathlib import Path

import os
import urllib

from dotenv import load_dotenv

import sentry_sdk

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

SECRET_KEY = os.environ["SECRET_KEY"]

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(int(os.environ.get("DEBUG", default=0)))


THIRD_PARTY_APPS = [
    "rest_framework",
    "django_filters",
    "drf_spectacular",
    "corsheaders",
    "django_celery_beat",
    "django_celery_results",
    "whitenoise",
    "storages",
    "pgtrigger",
    "pghistory",
    "pghistory.admin",
    "django_extensions",
    "admin_auto_filters",
    "django_object_actions",
    "more_admin_filters",
    "colorfield",
    "admin_interface",
    # Allauth – headless stack
    "allauth",
    "allauth.account",
    "allauth.headless",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
    "allauth.socialaccount.providers.microsoft",
]

LOCAL_APPS = [
    "core.apps.CoreConfig",
    "common.apps.CommonConfig",
]

INSTALLED_APPS = (
    [
        "django.contrib.admin",
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.messages",
        "django.contrib.staticfiles",
        "django.contrib.postgres",
        "django.contrib.sites",
    ]
    + THIRD_PARTY_APPS
    + LOCAL_APPS
)


SESSION_SAVE_EVERY_REQUEST = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_ENGINE = "django.contrib.sessions.backends.db"
SESSION_COOKIE_AGE = 3600
SESSION_COOKIE_SECURE = False


DJANGO_ADMIN_LOGS_DELETABLE = False
DJANGO_ADMIN_LOGS_ENABLED = True


SITE_ID = 1

MIDDLEWARE = [
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "allauth.account.middleware.AccountMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "core.middleware.session.HeadlessSessionCookieMiddleware",
    "core.middleware.allauth_conflict.AllAuthConflictMiddleware",
]

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

CSRF_COOKIE_SECURE = False

ROOT_URLCONF = "backend.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(BASE_DIR, "backend", "templates"),
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

WSGI_APPLICATION = "backend.wsgi.application"

INTERNAL_IPS = [
    "127.0.0.1",
]

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": os.environ.get("SQL_ENGINE", "django.db.backends.sqlite3"),
        "NAME": os.environ.get("DB_NAME", BASE_DIR / "db.sqlite3"),
        "USER": os.environ.get("DB_USER", "user"),
        "PASSWORD": os.environ.get("DB_PASSWORD", "password"),
        "HOST": os.environ.get("DB_HOST", "localhost"),
        "PORT": os.environ.get("DB_PORT", "5432"),
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True


# ---------------------------------MEDIA AND STATIC ROOT AND URL-------------------------------------------------#
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "static"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "mediafiles"
X_FRAME_OPTIONS = "SAMEORIGIN"

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}


# ---------------------------------DEFAULT PRIMARY KEY FIELD TYPE-------------------------------------------------#
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# ---------------------------------Auth User-------------------------------------------------#
AUTH_USER_MODEL = "core.User"


# ----------------------------------------------EMAIL SETTINGS------------------------------------------------------
EMAIL_HOST = os.environ["EMAIL_HOST"]
EMAIL_PORT = int(os.environ["EMAIL_PORT"])
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ["EMAIL_HOST_USER"]
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = os.environ["EMAIL_HOST_PASSWORD"]
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_DEBUG = True


# ----------------------------------REST FRAMEWORK SETTINGS----------------------------------#
REST_FRAMEWORK = {
    "DEFAULT_TIMEOUT": 600,
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.TokenAuthentication",
    ),
    "DEFAULT_FILTER_BACKENDS": (
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ),
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_PAGINATION_CLASS": "common.pagination.HTTPSLimitOffsetPagination",
    "PAGE_SIZE": 10,
}


# -------------------------------CORS CONFIG------------------------------------------------#
CORS_ALLOW_HEADERS = [
    "X-CSRFToken",  # Add any other headers you need to allow
    "Content-Type",  # Include Content-Type header
]

ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS").split(" ") or ["*"]
CSRF_TRUSTED_ORIGINS = os.environ.get("CSRF_TRUSTED_ORIGINS").split(" ") or [
    "*"
]
CORS_ALLOWED_ORIGINS = CSRF_TRUSTED_ORIGINS
CSRF_ALLOWED_ORIGINS = CORS_ALLOWED_ORIGINS
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True
SESSION_COOKIE_SAMESITE = "Lax"
CSRF_COOKIE_SAMESITE = "Lax"
CSRF_COOKIE_HTTPONLY = False
USE_X_FORWARDED_HOST = True
SESSION_HEADER_NAME = "X-Session-Token"


# ---------------------------------------------REDIS SETTINGS------------------------------------------------------
REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = int(os.getenv("REDIS_PORT"))
REDIS_PASSWORD = os.environ.get("REDIS_PASSWORD", "")

REDIS_DB = 0

if REDIS_PASSWORD:
    encoded_password = urllib.parse.quote_plus(REDIS_PASSWORD)
    REDIS_URL = f"redis://:{encoded_password}@{REDIS_HOST}:{REDIS_PORT}"
else:
    REDIS_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}"

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"{REDIS_URL}/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    },
    "localcache": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "unique-snowflake",
    },
}
DJANGO_REDIS_IGNORE_EXCEPTIONS = True


# ------------------------- Sentry Configuration ------------------------- #
sentry_sdk.init(
    dsn=os.environ.get("SENTRY_SECRET_KEY"),
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
)


# ------------------------------SPECTACULAR CONFIG---------------------------------------------#
SPECTACULAR_SETTINGS = {
    "TITLE": "Culture API",
    "DESCRIPTION": "Your project description",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "SCHEMA_PATH_PREFIX": "/api/",
}


# ----------------------------------------------LOGGING SETTINGS------------------------------------------------------
# LOGGING = {
#     "version": 1,
#     "disable_existing_loggers": False,
#     "formatters": {
#         "simple": {
#             "format": "%(asctime)s - %(filename)s - %(module)s - %(funcName)s - %(lineno)d - "
#             "[%(levelname)s] - %(message)s",
#             "datefmt": "%y %b %d, %H:%M:%S",
#         },
#     },
#     "handlers": {
#         "console": {
#             "level": "DEBUG",
#             "class": "logging.StreamHandler",
#             "formatter": "simple",
#         },
#         "celery": {
#             "level": "DEBUG",
#             "class": "logging.handlers.RotatingFileHandler",
#             "filename": "logs/celery.log",
#             "formatter": "simple",
#             "maxBytes": 1024 * 1024 * 100,  # 100 mb
#         },
#         "file": {
#             "level": "DEBUG",
#             "class": "logging.handlers.RotatingFileHandler",
#             "filename": "logs/debug.log",
#             "maxBytes": 1024 * 1024 * 100,  # 100 mb
#         },
#     },
#     "loggers": {
#         "celery": {
#             "handlers": ["celery", "console"],
#             "level": "DEBUG",
#         },
#         "django": {
#             "handlers": ["file", "console"],
#             "level": "INFO",
#             "propagate": True,
#         },
#     },
#     "root": {
#         "handlers": ["console"],
#         "level": "DEBUG",
#     },
# }

# ---------------------------------------------CELERY SETTINGS------------------------------------------------------
CELERY_BROKER_URL = f"{REDIS_URL}/2"
CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = "UTC"
CELERY_RESULT_BACKEND = "django-db"
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers.DatabaseScheduler"


# ---------------------------------------------OAUTH 2.0------------------------------------------------------
FRONTEND_DOMAIN = os.getenv("DOMAIN")
HEADLESS_ONLY = True
ACCOUNT_ADAPTER = "core.backends.allauth.AccountAdapter"
SOCIALACCOUNT_ADAPTER = "core.backends.allauth.SocialAccountAdapter"
HEADLESS_ADAPTER = "core.backends.allauth.HeadlessAdapter"


ACCOUNT_PASSWORD_MIN_LENGTH = 8
ACCOUNT_PASSWORD_COMPLEXITY = {
    "UPPER": 1,
    "LOWER": 1,
    "DIGITS": 1,
    "SPECIAL": 1,
    "MIN_LENGTH": 8,
}
ACCOUNT_PASSWORD_VALIDATORS = [
    "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    "django.contrib.auth.password_validation.MinimumLengthValidator",
    "django.contrib.auth.password_validation.CommonPasswordValidator",
    "django.contrib.auth.password_validation.NumericPasswordValidator",
]

ACCOUNT_EMAIL_VERIFICATION = "none"
SOCIALACCOUNT_EMAIL_VERIFICATION = "none"
SOCIALACCOUNT_AUTO_SIGNUP = True
ACCOUNT_PASSWORD_RESET_BY_CODE_ENABLED = False

HEADLESS_FRONTEND_URLS = {
    "account_confirm_email": f"http://{FRONTEND_DOMAIN}/verify-email/?key="
    + "{key}",
    "account_reset_password_from_key": f"http://{FRONTEND_DOMAIN}/update-password/?key="
    + "{key}",
    "account_reset_password": f"http://{FRONTEND_DOMAIN}/password/reset",
    "account_signup": f"http://{FRONTEND_DOMAIN}/signup",
    "socialaccount_login_redirect": f"http://{FRONTEND_DOMAIN}/social/success",
    "socialaccount_login_success": f"http://{FRONTEND_DOMAIN}/social/success",  # explicitly add this
    "socialaccount_signup_success": f"http://{FRONTEND_DOMAIN}/social/success",  # and this
    "socialaccount_login_error": f"http://{FRONTEND_DOMAIN}/social/error",
    "socialaccount_login_cancelled": f"http://{FRONTEND_DOMAIN}/social/cancelled",
}

SOCIALACCOUNT_EMAIL_AUTHENTICATION = False
SOCIALACCOUNT_EMAIL_AUTHENTICATION_AUTO_CONNECT = False

ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_USER_MODEL_EMAIL_FIELD = "email"
ACCOUNT_LOGIN_METHODS = ["email"]
ACCOUNT_SIGNUP_FIELDS = [
    "email*",
    # "password*",
    "password1*",
    "token",
    "first_name",
    "last_name",
]
