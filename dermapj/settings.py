import os
import sys
import re
from pathlib import Path
from datetime import timedelta
from decouple import config
from corsheaders.defaults import default_headers
# AUTH_USER_MODEL = 'users.User'

# Build paths inside the project like this: BASE_DIR / 'subdir'.
# We keep os.path wrapper for compatibility with your old logic
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR_PATH = Path(__file__).resolve().parent.parent

# Directories
STATIC_DIR = os.path.join(BASE_DIR, "static")
MEDIA_DIR = os.path.join(BASE_DIR, "media")
LOGS_ROOT = config("LOGS_ROOT", default=os.path.join(BASE_DIR, "log"))


# =========================================================
#  SECURITY & ENV CONFIGURATION
# =========================================================

SECRET_KEY = config("SECRET_KEY")

DEBUG = config("DEBUG", cast=bool, default=False)

ALLOWED_HOSTS = config(
    "ALLOWED_HOSTS", 
    cast=lambda v: [s.strip() for s in v.split(",") if s],
    default="*"
)

ENVIRONMENT = config("ENVIRONMENT", default="development")

# Admins & Managers
ADMINS = config(
    "ADMINS", default="", cast=lambda v: [s.split(",") for s in v.split(";") if s]
)
MANAGERS = config(
    "MANAGERS", default="", cast=lambda v: [s.split(",") for s in v.split(";") if s]
)

# =========================================================
#  APPLICATIONS
# =========================================================

DJANGO_APPS = [
    # 'modeltranslation', # Uncomment if installed
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.gis", # Required for PostGIS
]

THIRD_PARTY_APPS = [
    # Add your pip installed apps here
    "rest_framework",
    "rest_framework.authtoken",
    "corsheaders",
    "django_filters",
    "django_prometheus",
    "versatileimagefield",
    "rest_framework_simplejwt",
    "rest_framework_simplejwt.token_blacklist",
    # "fcm_django",
    # "django_celery_beat",
]

# Apps specific to dermapj
CUSTOM_APPS = [
    "core",
    "derma",
    "users",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + CUSTOM_APPS

if DEBUG and ENVIRONMENT == "development":
    try:
        import debug_toolbar
        INSTALLED_APPS += ["debug_toolbar"]
    except ImportError:
        pass

# =========================================================
#  MIDDLEWARE
# =========================================================

MIDDLEWARE = [
    "django_prometheus.middleware.PrometheusBeforeMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware", # CORS must be before Common
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    
    # Custom Middlewares (Uncomment when you copy the files over)
    # "utils.middlewares.AppVersionMiddleware",
    # "api_logger.middleware.api_logger_middleware.APILoggerMiddleware",
]

if DEBUG and ENVIRONMENT == "development":
    try:
        MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]
    except:
        pass

MIDDLEWARE.append("django_prometheus.middleware.PrometheusAfterMiddleware")

ROOT_URLCONF = "dermapj.urls"

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

WSGI_APPLICATION = "dermapj.wsgi.application"
ASGI_APPLICATION = "dermapj.asgi.application"

# =========================================================
#  DATABASES
# =========================================================

# Default options logic from your old project
DEFAULT_DB_OPTIONS = config('DEFAULT_OPTIONS', default='public').replace(' ', '')

DATABASES = {
    "default": {
        # Using standard PostGIS engine initially. 
        # Change to "django_prometheus.db.backends.postgis" if prometheus is set up
        "ENGINE": "django.contrib.gis.db.backends.postgis", 
        "NAME": config("DEFAULT_DATABASE"),
        "USER": config("DEFAULT_DATABASE_USER"),
        "PASSWORD": config("DEFAULT_DATABASE_PASSWORD"),
        "HOST": config("DEFAULT_DATABASE_HOST"),
        "PORT": config("DEFAULT_DATABASE_PORT"),
        "OPTIONS": {
            "options": f"-c search_path={DEFAULT_DB_OPTIONS}"
        },
    }
}

# If you have the router file, uncomment this
# DATABASE_ROUTERS = [
#     "odk_app.odkrouter.DatabaseRouter",
# ]

# =========================================================
#  PASSWORD VALIDATION
# =========================================================

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# =========================================================
#  INTERNATIONALIZATION
# =========================================================

LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Kathmandu" # Updated to match your .env context
USE_I18N = True
USE_TZ = True

LANGUAGES = (
    ("en", "English"),
    ("ne", "Nepali"),
)

LOCALE_PATHS = [
    os.path.join(BASE_DIR, "locale"),
]

# =========================================================
#  STATIC & MEDIA FILES
# =========================================================

STATIC_URL = "/static/"
STATICFILES_DIRS = [STATIC_DIR]
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")



# Base URL for serving files
MEDIA_URL = '/media/'

# Where files are physically stored on your computer
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
AUTH_USER_MODEL = "users.User"


# =========================================================
#  REST FRAMEWORK
# =========================================================

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.TokenAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_VERSIONING_CLASS": "rest_framework.versioning.QueryParameterVersioning",
    "DEFAULT_FILTER_BACKENDS": ("django_filters.rest_framework.DjangoFilterBackend",),
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=365 * 3), # From your old config
    "REFRESH_TOKEN_LIFETIME": timedelta(days=365 * 3),
    "AUTH_HEADER_TYPES": ("Bearer",),
}

# =========================================================
#  CORS
# =========================================================

CORS_ALLOW_ALL_ORIGINS = config("CORS_ORIGIN_ALLOW_ALL", cast=bool, default=False)
CORS_ALLOWED_ORIGINS = config(
    "ALLOWED_HOSTS", # Mapping allowed hosts to CORS for simplicity, adjust as needed
    cast=lambda v: [f"https://{s.strip()}" for s in v.split(",") if s] + [f"http://{s.strip()}" for s in v.split(",") if s],
    default=[]
)
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = list(default_headers) + [
    "app-type",
    "app-version",
]

# =========================================================
#  LOGGING
# =========================================================

LOG_LEVEL = config("LOG_LEVEL", default="INFO")
os.makedirs(LOGS_ROOT, exist_ok=True)
LOG_FILE = "django.log"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "root": {"level": LOG_LEVEL, "handlers": ["file"]},
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s"
        },
        "simple": {"format": "%(levelname)s %(asctime)s %(message)s"},
        "file": {
            "format": ("[%(levelname)s] %(asctime)s (%(name)s.%(lineno)s) %(message)s"),
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "file": {
            "level": "DEBUG",
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": os.path.join(LOGS_ROOT, LOG_FILE),
            "when": "D",
            "interval": 1,
            "backupCount": 10,
            "formatter": "file",
        },
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["file", "console"],
            "level": LOG_LEVEL,
            "propagate": True,
        },
        "dermapj.logger": {
            "handlers": ["console", "file"],
            "level": "INFO",
            "propagate": True,
        },
    },
}

# =========================================================
#  EMAIL SETTINGS
# =========================================================

if ENVIRONMENT == "production":
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_HOST = config("EMAIL_HOST")
    EMAIL_USE_TLS = config("EMAIL_USE_TLS", cast=bool)
    EMAIL_PORT = config("EMAIL_PORT")
    EMAIL_HOST_USER = config("EMAIL_HOST_USER")
    EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD")
else:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

DEFAULT_FROM_EMAIL = config("DEFAULT_FROM_EMAIL")

# =========================================================
#  CELERY & REDIS
# =========================================================

BROKER_URL = config("BROKER_URL", default="redis://redis:6379")
CELERY_RESULT_BACKEND = config("CELERY_RESULT_BACKEND", default="redis://redis:6379")
CACHE_LOCATION = config("CACHE_LOCATION", default="redis://redis:6379")

CACHES = {
    "default": {
        "BACKEND": "django_prometheus.cache.backends.redis.RedisCache",
        "LOCATION": CACHE_LOCATION,
        "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient"},
    }
}

# =========================================================
#  3RD PARTY API KEYS (From .env)
# =========================================================

GOOGLE_MAP_API_KEY = config("GOOGLE_MAP_API_KEY")
FCM_SERVER_KEY = config("FCM_SERVER_KEY")

# Payment
KHALTI_PUBLIC_KEY = config("KHALTI_PUBLIC_KEY", default="")
KHALTI_SECRET_KEY = config("KHALTI_SECRET_KEY", default="")
ESEWA_URL = config("ESEWA_URL", default="https://esewa.com.np")
ESEWA_MERCHANT_ID = config("ESEWA_MERCHANT_ID", default="")
ESEWA_MERCHANT_SECRET_KEY = config("ESEWA_MERCHANT_SECRET_KEY", default="")

# AI
GEMINI_API_KEY = config("GEMINI_API_KEY", default="")
DEEPSEEK_API_KEY = config("DEEPSEEK_API_KEY", default="")

# Import local settings if available
try:
    from dermapj.local_settings import *
except ImportError:
    pass

# Default Primary Key
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'