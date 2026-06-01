from django.urls import path
from django.views.generic import RedirectView

from . import views

app_name = "affiliates"

urlpatterns = [
    # Clean affiliate routes
    path("affiliates/", views.affiliate_list, name="list"),
    path("affiliates/requests/", views.affiliate_requests, name="requests"),
    path("affiliates/<int:pk>/", views.affiliate_detail, name="detail"),
    path("affiliates/<int:pk>/approve/", views.affiliate_approve, name="approve"),
    path("affiliates/<int:pk>/reject/", views.affiliate_reject, name="reject"),
    path("affiliates/<int:pk>/suspend/", views.affiliate_suspend, name="suspend"),
    path("affiliates/<int:pk>/reactivate/", views.affiliate_reactivate, name="reactivate"),
    path("affiliates/<int:pk>/change-level/", views.affiliate_change_level, name="change-level"),
    path("affiliates/<int:pk>/notes/", views.affiliate_edit_notes, name="notes"),
    # Legacy redirects — preserve inbound *.html links from not-yet-converted templates
    path(
        "affiliates.html",
        RedirectView.as_view(pattern_name="affiliates:list", permanent=True),
    ),
    path(
        "affiliate-detail.html",
        RedirectView.as_view(pattern_name="affiliates:list", permanent=True),
    ),
    path(
        "affiliate-requests.html",
        RedirectView.as_view(pattern_name="affiliates:requests", permanent=True),
    ),
]
