from django.urls import path
from django.views.generic import RedirectView

from . import views

app_name = "products"

urlpatterns = [
    # Clean product routes
    path("products/", views.product_list, name="list"),
    path("products/create/", views.product_create, name="create"),
    path("products/<slug:slug>/", views.product_detail, name="detail"),
    path("products/<slug:slug>/edit/", views.product_edit, name="edit"),
    path("products/<slug:slug>/disable/", views.product_disable, name="disable"),
    path("products/<slug:slug>/enable/", views.product_enable, name="enable"),
    path("products/<slug:slug>/duplicate/", views.product_duplicate, name="duplicate"),
    path("products/<slug:slug>/delete/", views.product_delete, name="delete"),
    # Legacy redirects — preserve inbound *.html links from not-yet-converted templates
    path(
        "products.html",
        RedirectView.as_view(pattern_name="products:list", permanent=True),
    ),
    path(
        "product-create.html",
        RedirectView.as_view(pattern_name="products:create", permanent=True),
    ),
    path(
        "product-detail.html",
        RedirectView.as_view(pattern_name="products:list", permanent=True),
    ),
    path(
        "product-edit.html",
        RedirectView.as_view(pattern_name="products:list", permanent=True),
    ),
]
