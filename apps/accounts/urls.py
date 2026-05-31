from django.contrib.auth.views import LoginView
from django.urls import path

from . import views

app_name = "accounts"

urlpatterns = [
    path(
        "login.html",
        LoginView.as_view(template_name="login.html"),
        name="login",
    ),
    path("logout", views.logout_view, name="logout"),
    path("post-login/", views.post_login_redirect, name="post_login_redirect"),
]
