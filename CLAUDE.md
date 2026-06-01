<!-- SPECKIT START -->
Active feature: `004-products-catalog` (branch: `004-products-catalog`).

This feature is the first **data conversion** on top of the Django foundation: it
turns the four static product pages into a database-backed, merchant-owned catalog
in `apps/products`. For technologies, project structure, shell commands, and design
decisions, read the current plan and supporting design artifacts:

- Spec: `specs/004-products-catalog/spec.md`
- Plan: `specs/004-products-catalog/plan.md`
- Research: `specs/004-products-catalog/research.md`
- Data model: `specs/004-products-catalog/data-model.md`
- Routes/form contract: `specs/004-products-catalog/contracts/routes.md`
- Quickstart: `specs/004-products-catalog/quickstart.md`
- Constitution (v2.0.0): `.specify/memory/constitution.md`

Phase scope: `ProductCategory` + `Product` + `ProductImage` models; merchant CRUD
(list with server-side filtering + empty state, create, edit, detail,
disable/enable, duplicate, delete) — all owner-scoped (Principle IV); pricing +
affiliate-profit validation; admin with inline images; idempotent physical-commerce
seed. The product surface adopts **clean URLs** (`/products/…`) with legacy `*.html`
redirects so no inbound link breaks. Two user-approved **in-style** UI extensions
(create/edit form fields; filter bar badge + stock selects) — see spec Clarifications.
Out of scope: orders, affiliates, commissions, payouts, customers, landing pages.

Prior features: `003-backend-foundation` (Django skeleton, `accounts.User` + role,
role-based login, base templates, page registry) and the static prototype
`001-static-frontend-mvp` / `002-affiliate-seller-portal`. Preserve their UI exactly.

## How to convert the next page

> **Data conversion (this phase, 004):** product pages are made database-backed,
> not just template-inherited. Follow `plan.md` + `contracts/routes.md`: add
> models/forms/selectors/services in the owning app, enforce owner-scoped querysets,
> and use **clean URLs** (`/products/…`) with legacy `*.html` redirects. The
> four-step pattern below remains the baseline for *template-only* conversions.

The foundation converted three pages as proof-of-concept
(`login.html` → auth, `dashboard.html` → merchant, `affiliate-dashboard.html` →
affiliate). Template-only conversions follow the same four-step pattern:

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
# Template-only conversions keep the .html path (mirrors the prototype URL so
# inbound links keep resolving). Data conversions (e.g. 004 products) adopt clean
# URLs and add legacy *.html redirects instead — see contracts/routes.md.
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
