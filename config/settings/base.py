import os
from pathlib import Path

from django.core.exceptions import ImproperlyConfigured

BASE_DIR = Path(__file__).resolve().parent.parent.parent

# SECRET_KEY is not set here.  Each environment file (local.py, production.py)
# is responsible for setting it before Django processes any request.
# local.py   → os.environ.get("SECRET_KEY", "django-insecure-dev-fallback")
# production.py → os.environ["SECRET_KEY"]  (raises KeyError if missing)
#
# If base.py is imported as the final DJANGO_SETTINGS_MODULE directly (which
# should never happen), Django's system check will raise ImproperlyConfigured
# because SECRET_KEY will be absent/empty.
_secret = os.environ.get("SECRET_KEY", "")
if not _secret and os.environ.get("DJANGO_SETTINGS_MODULE", "").endswith(".base"):
    raise ImproperlyConfigured(
        "SECRET_KEY is not set. "
        "Use DJANGO_SETTINGS_MODULE=config.settings.local for development."
    )
SECRET_KEY = _secret

DEBUG = False

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "whitenoise.runserver_nostatic",
    "django.contrib.staticfiles",
    # Project apps
    "apps.core",
    "apps.accounts",
    "apps.merchants",
    "apps.products",
    "apps.orders",
    "apps.customers",
    "apps.affiliates",
    "apps.commissions",
    "apps.payouts",
    "apps.landing_pages",
    "apps.dashboard",
    "apps.notifications",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

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

WSGI_APPLICATION = "config.wsgi.application"

AUTH_USER_MODEL = "accounts.User"

# EmailOrUsernameBackend extends ModelBackend and handles both email and username
# lookups, so ModelBackend is redundant and would double DB queries on every failed
# login attempt.
AUTHENTICATION_BACKENDS = [
    "apps.accounts.backends.EmailOrUsernameBackend",
]

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "ar"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/assets/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOGIN_URL = "/login.html"
LOGIN_REDIRECT_URL = "/post-login/"
LOGOUT_REDIRECT_URL = "/login.html"

# ── Logging ───────────────────────────────────────────────────────────────────
# Minimal structured config: request errors (5xx) and security events go to
# stderr with timestamps.  Production deployments should extend this with a
# dedicated handler (file, Sentry, CloudWatch, etc.).
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{asctime} {levelname} {name} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "WARNING",
        },
        "django.security": {
            "handlers": ["console"],
            "level": "WARNING",
            "propagate": False,
        },
        "apps": {
            "handlers": ["console"],
            "level": "WARNING",
        },
    },
}
