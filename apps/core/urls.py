from django.contrib.auth.decorators import login_required
from django.urls import path

from .page_registry import REGISTRY, Access
from .views import serve_page

app_name = "core"

_PRIVATE = (Access.MERCHANT, Access.AFFILIATE)


def _view(entry):
    """Return serve_page wrapped with login_required for private pages."""
    if entry.access in _PRIVATE:
        return login_required(serve_page)
    return serve_page


urlpatterns = [
    path(
        entry.url_path,
        _view(entry),
        {"template": entry.template},
        name="page-{}".format(entry.url_path.removesuffix(".html") or "home"),
    )
    for entry in REGISTRY
]
