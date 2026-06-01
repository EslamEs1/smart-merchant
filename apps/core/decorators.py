"""Shared access-control decorators used across multiple apps."""

import functools

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied


def role_required(role_attr: str):
    """Return a decorator: login required + user must satisfy the given role property.

    Usage::

        from apps.core.decorators import role_required

        @role_required("is_merchant")
        def my_view(request): ...

        @role_required("is_affiliate")
        def affiliate_view(request): ...

    The `role_attr` must be a boolean property on the custom User model
    (e.g. ``is_merchant``, ``is_affiliate``).  Raises 403 on wrong role.
    """
    def decorator(view_func):
        @login_required
        @functools.wraps(view_func)
        def wrapped(request, *args, **kwargs):
            if not getattr(request.user, role_attr, False):
                raise PermissionDenied
            return view_func(request, *args, **kwargs)
        return wrapped
    return decorator
