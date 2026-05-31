from django.urls import path

from .page_registry import REGISTRY
from .views import serve_page

app_name = "core"

urlpatterns = [
    path(
        entry.url_path,
        serve_page,
        {"template": entry.template},
        name="page-{}".format(entry.url_path.removesuffix(".html") or "home"),
    )
    for entry in REGISTRY
]
