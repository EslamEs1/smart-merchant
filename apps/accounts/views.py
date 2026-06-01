import logging

from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

logger = logging.getLogger(__name__)


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
    # Fallback: role is neither ADMIN, AFFILIATE, nor MERCHANT — should not
    # happen with the current schema (role has a non-null default), but log it
    # so a misconfigured account is visible in the server log rather than silent.
    logger.warning(
        "User %s has unrecognised role %r; redirecting to /",
        user.pk,
        getattr(user, "role", None),
    )
    return redirect("/")


def logout_view(request):
    """End the user session and redirect to the login page.

    Accepts GET and POST.  GET support is intentional for backwards compatibility
    with the prototype's static anchor links.

    Security note: a CSRF-forced GET logout logs the user out without their
    consent, which is a minor inconvenience (not a data-integrity threat) because
    Django 5 regenerates the session key on logout, preventing session fixation.
    Django's own security docs acknowledge this trade-off for GET-based logout.
    Full CSRF protection will be applied when templates are converted to use
    POST forms in Phase 5.
    """
    auth_logout(request)
    return redirect("/login.html")
