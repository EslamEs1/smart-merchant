from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect


@login_required
def post_login_redirect(request):
    """Dispatch the authenticated user to their role's landing page.

    Called as LOGIN_REDIRECT_URL when no ?next= is present.
    Django's LoginView already handles valid ?next= redirects before
    this view is invoked.
    """
    user = request.user
    if user.is_admin:
        return redirect("/admin/")
    if user.is_affiliate:
        return redirect("/affiliate-dashboard.html")
    if user.is_merchant:
        return redirect("/dashboard.html")
    return redirect("/")


def logout_view(request):
    """End the user session and redirect to the login page.

    Accepts GET and POST.  GET support is intentional for backwards compatibility
    with the prototype's static anchor links; a forced-logout CSRF attack is a
    minor inconvenience, not a data-integrity threat.
    """
    auth_logout(request)
    return redirect("/login.html")
