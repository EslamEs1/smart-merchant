<!-- SPECKIT START -->
Active feature: `003-backend-foundation` (branch: `003-backend-foundation`).

This feature begins the **Django backend conversion** of the existing static
prototype. For technologies, project structure, shell commands, and design
decisions, read the current plan and supporting design artifacts:

- Spec: `specs/003-backend-foundation/spec.md`
- Plan: `specs/003-backend-foundation/plan.md`
- Research: `specs/003-backend-foundation/research.md`
- Data model: `specs/003-backend-foundation/data-model.md`
- Routes/auth contract: `specs/003-backend-foundation/contracts/routes.md`
- Quickstart: `specs/003-backend-foundation/quickstart.md`
- Constitution (v2.0.0): `.specify/memory/constitution.md`

Foundation scope: Django project skeleton (`config/`, `apps/`, `templates/`,
`static/`), custom `accounts.User` + role, role-based login redirect, four base
templates + shared includes, serve all prototype pages, convert one page per
surface. Assets serve at `/assets/` (`STATIC_URL='/assets/'`); URLs mirror the
existing filenames so links/refs keep working. No SPA/API/DRF/Node build.

Prior features (the static prototype now being converted):
`specs/001-static-frontend-mvp/` (merchant dashboard, public pages, products/
orders/affiliates/customers/landing-pages) and `specs/002-affiliate-seller-portal/`
(affiliate seller portal). Preserve their UI exactly during conversion.

## How to convert the next page (Phase 0 pattern)

Three pages were converted in this phase as proof-of-concept
(`login.html` → auth, `dashboard.html` → merchant, `affiliate-dashboard.html` →
affiliate). All remaining pages follow the same four-step pattern:

### Step 1 — Remove from the raw page registry

In `apps/core/page_registry.py`, delete the `PageEntry(...)` line for the page.
Add a comment referencing which view now owns it (as done for the existing three).

### Step 2 — Create a real view in the owning app

In the relevant app's `views.py` (e.g. `apps/products/views.py`), add a function
view decorated with the correct role guard:

```python
from django.shortcuts import render
from apps.core.decorators import role_required  # public utility in apps/core/

@role_required("is_merchant")   # use "is_affiliate" for affiliate pages
def products_list(request):
    return render(request, "products.html")
```

### Step 3 — Wire the URL in the app's `urls.py`

```python
# Keep the .html extension — mirrors the static prototype URL so all existing
# links in other templates remain valid without any link rewriting.
path("products.html", views.products_list, name="products"),
```

Ensure `config/urls.py` already includes the app's urls (it does for the active
apps; add `path("", include("apps.<name>.urls"))` for new ones).

### Step 4 — Convert the template to template inheritance

Replace the entire `<!DOCTYPE html>…</html>` boilerplate with:

```html
{% extends 'merchant_base.html' %}   {# or affiliate_base.html / auth_base.html #}
{% load static %}

{% block title %}Page Title | Smart Merchant OS{% endblock %}

{% block content %}
  {# paste only the page-specific content from inside <main> here #}
{% endblock %}
```

Replace hardcoded `assets/img/...` paths with `{% static 'img/...' %}`.
Keep ALL other HTML, classes, `data-*` attributes, and JS hooks verbatim —
Principle I (frontend preservation) is non-negotiable.

**Visual regression check:** open the converted page side-by-side with the
static original and confirm pixel equivalence before marking the task done.
<!-- SPECKIT END -->
