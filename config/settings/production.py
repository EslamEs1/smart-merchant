import os

from django.core.exceptions import ImproperlyConfigured

from .base import *  # noqa: F401, F403

DEBUG = False

SECRET_KEY = os.environ["SECRET_KEY"]

# ── Allowed hosts ─────────────────────────────────────────────────────────────
_allowed_raw = os.environ.get("ALLOWED_HOSTS", "")
if not _allowed_raw:
    raise ImproperlyConfigured("ALLOWED_HOSTS env var is required in production.")
ALLOWED_HOSTS = [h.strip() for h in _allowed_raw.split(",") if h.strip()]
if not ALLOWED_HOSTS:
    raise ImproperlyConfigured(
        "ALLOWED_HOSTS env var produced an empty list after normalisation "
        "(check for stray commas or whitespace-only values)."
    )

# ── Database ──────────────────────────────────────────────────────────────────
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ["DB_NAME"],
        "USER": os.environ["DB_USER"],
        "PASSWORD": os.environ["DB_PASSWORD"],
        "HOST": os.environ.get("DB_HOST", "localhost"),
        "PORT": os.environ.get("DB_PORT", "5432"),
        # Reuse connections; avoids a new TCP handshake per request under gunicorn.
        "CONN_MAX_AGE": int(os.environ.get("DB_CONN_MAX_AGE", "60")),
    }
}

# ── Static files ──────────────────────────────────────────────────────────────
STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# ── CSRF / trusted origins ────────────────────────────────────────────────────
# Required since Django 4.0: browsers send Origin on form POSTs; Django validates
# it against this list. Without it every login form submission returns 403.
_csrf_origins = os.environ.get("CSRF_TRUSTED_ORIGINS", "")
if not _csrf_origins:
    raise ImproperlyConfigured("CSRF_TRUSTED_ORIGINS env var is required in production.")
CSRF_TRUSTED_ORIGINS = [o.strip() for o in _csrf_origins.split(",") if o.strip()]

# ── Security headers / TLS ────────────────────────────────────────────────────
# SECURE_PROXY_SSL_HEADER: required when running behind a TLS-terminating proxy
# (Nginx, ALB, Railway, Render, …). Without it SECURE_SSL_REDIRECT causes an
# infinite redirect loop because Django sees plain HTTP from the proxy.
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = True

SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
X_FRAME_OPTIONS = "DENY"

# Note: SECURE_BROWSER_XSS_FILTER was removed in Django 4.0 (the X-XSS-Protection
# header is deprecated in modern browsers); it is intentionally absent here.
