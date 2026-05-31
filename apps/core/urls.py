from django.contrib.auth.decorators import login_required
from django.urls import path

from .page_registry import REGISTRY, Access
from .views import serve_page

app_name = "core"

_PRIVATE = (Access.MERCHANT, Access.AFFILIATE)

# Cache one wrapped view per access level rather than creating N identical
# login_required wrappers (one per private entry).
_serve_page_login_required = login_required(serve_page)


def _view(entry):
    """Return the appropriate view callable for a registry entry.

    Phase 4 (US2): private pages require login but NOT a specific role.
    Raw registry pages serve no owner-scoped data (FR-016), so cross-role
    access is acceptable at this stage.

    TODO Phase 5: apply role-level enforcement to each page as it is
    data-converted (T029/T030 already gate the converted dashboards by role).
    """
    if entry.access in _PRIVATE:
        return _serve_page_login_required
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
