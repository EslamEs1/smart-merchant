import os

from .base import *  # noqa: F401, F403

DEBUG = True

ALLOWED_HOSTS = ["*"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",  # noqa: F405
    }
}

SECRET_KEY = os.environ.get(
    "SECRET_KEY", "django-insecure-local-dev-key-change-in-production"
)
