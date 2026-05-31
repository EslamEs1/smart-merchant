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
    # No trailing slash on "logout" intentionally: prototype links use
    # href="logout" (no slash).  APPEND_SLASH only adds a slash when there is
    # no match WITHOUT the slash; since this pattern matches /logout directly,
    # no 301 redirect occurs.
    path("logout", views.logout_view, name="logout"),
    path("post-login/", views.post_login_redirect, name="post_login_redirect"),
]
