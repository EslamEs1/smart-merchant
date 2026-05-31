import functools

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render


def _role_required(role_attr: str):
    """Return a decorator that enforces login + a specific role property."""
    def decorator(view_func):
        @login_required
        @functools.wraps(view_func)
        def wrapped(request, *args, **kwargs):
            if not getattr(request.user, role_attr, False):
                raise PermissionDenied
            return view_func(request, *args, **kwargs)
        return wrapped
    return decorator


@_role_required("is_merchant")
def merchant_dashboard(request):
    return render(request, "dashboard.html")


@_role_required("is_affiliate")
def affiliate_dashboard(request):
    return render(request, "affiliate-dashboard.html")
