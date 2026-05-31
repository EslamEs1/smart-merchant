from django.urls import path

from . import views

app_name = "dashboard"

urlpatterns = [
    path("dashboard.html", views.merchant_dashboard, name="merchant_dashboard"),
    path("affiliate-dashboard.html", views.affiliate_dashboard, name="affiliate_dashboard"),
]
