<!-- SPECKIT START -->
Active feature: `005-affiliate-management` (branch: `005-affiliate-management`).

This feature is the second **data conversion** on top of the Django foundation: it
turns the three merchant-side affiliate pages into a database-backed, merchant-owned
affiliate roster in `apps/affiliates`. For technologies, project structure, shell
commands, and design decisions, read the current plan and supporting design artifacts:

- Spec: `specs/005-affiliate-management/spec.md`
- Plan: `specs/005-affiliate-management/plan.md`
- Research: `specs/005-affiliate-management/research.md`
- Data model: `specs/005-affiliate-management/data-model.md`
- Routes/action contract: `specs/005-affiliate-management/contracts/routes.md`
- Quickstart: `specs/005-affiliate-management/quickstart.md`
- Constitution (v2.0.0): `.specify/memory/constitution.md`

Phase scope: one `AffiliateProfile` model (a Pending profile *is* the join request —
no separate `AffiliateApplication`); merchant views for the roster (list with
search/status/level filtering + empty state), the join-requests queue, the detail
page, and lifecycle mutations (approve, reject, suspend, reactivate, change level,
edit notes) — all owner-scoped (Principle IV), all mutations POST+CSRF. Referral code
is globally unique; coupon code is unique per merchant. The surface adopts **clean
URLs** (`/affiliates/…`) with legacy `*.html` redirects. Order/commission/payout
figures render as **truthful zeros / empty-state** (Principle V — those subsystems are
out of scope). Two bounded **in-style** additions required for backend integration:
the list page's triggered-but-undefined confirmation modals are supplied, and the
detail notes block gains an edit affordance (see plan Complexity Tracking). Out of
scope: commission engine, order attribution, payouts, affiliate seller portal, real
QR/WhatsApp.

Prior features: `004-products-catalog` (first data conversion — `apps/products`),
`003-backend-foundation` (Django skeleton, `accounts.User` + role, role-based login,
base templates, page registry), and the static prototype `001-static-frontend-mvp` /
`002-affiliate-seller-portal`. Preserve their UI exactly.

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
