from django.http import Http404
from django.shortcuts import render
from django.template.exceptions import TemplateDoesNotExist


def serve_page(request, template: str):
    """Render a raw prototype page from the page registry.

    The `template` kwarg is injected by urls.py via the extra-options dict on
    each path() entry — it is a compile-time constant, not user-supplied.

    Access enforcement (login_required / role check) is layered on in Phase 4
    (US2) by wrapping the relevant entries.  A missing template file surfaces as
    404 rather than 500 so a stale registry entry doesn't take the site down.
    """
    try:
        return render(request, template)
    except TemplateDoesNotExist:
        raise Http404(f"Page not found: {template}")
