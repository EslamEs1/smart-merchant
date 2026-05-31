from django.shortcuts import render


def serve_page(request, template: str):
    """Render a raw prototype page from the page registry.

    The `template` kwarg is injected by urls.py via the extra-options dict on
    each path() entry.  Access enforcement (login_required / role check) is
    layered on in Phase 4 (US2) by wrapping the relevant entries.
    """
    return render(request, template)
