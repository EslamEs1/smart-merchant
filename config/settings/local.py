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

# Dev-only fallback — never used by production.py (which requires os.environ["SECRET_KEY"]).
SECRET_KEY = os.environ.get(
    "SECRET_KEY", "django-insecure-local-dev-key-change-in-production"
)

# Print emails to the console in development so password-reset links are visible
# without an SMTP server. production.py should configure a real EMAIL_BACKEND.
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
