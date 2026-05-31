from django.urls import path

from .page_registry import REGISTRY
from .views import serve_page

app_name = "core"

# Phase 4 (US2) will wrap private entries (MERCHANT / AFFILIATE) with login_required.
# All patterns are intentionally open-access in this phase (US1 serves all pages
# unchanged; enforcement is added incrementally in the next phase).
urlpatterns = [
    path(
        entry.url_path,
        serve_page,
        {"template": entry.template},
        name="page-{}".format(entry.url_path.removesuffix(".html") or "home"),
    )
    for entry in REGISTRY
]
