# Implementation Plan: Products Catalog (Database-Backed Conversion — MVP Phase 1)

**Branch**: `004-products-catalog` | **Date**: 2026-06-01 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/004-products-catalog/spec.md`

## Summary

Convert the four static product pages (`products.html`, `product-create.html`, `product-edit.html`,
`product-detail.html`) into a real, database-backed, **merchant-owned** product catalog inside the
`apps/products` Django app — the first *data conversion* on top of the `003-backend-foundation`
skeleton. Introduce three models (`ProductCategory`, `Product`, `ProductImage`), full merchant CRUD
(list with server-side filtering + empty state, create, edit, detail, disable/enable, duplicate,
delete), per-merchant ownership scoping enforced at the queryset/view level, pricing + affiliate-profit
validation, an admin registration with inline images, and an idempotent physical-commerce seed command.
The product surface moves to **clean URLs** (`/products/…`) while legacy `*.html` paths redirect so no
existing inter-page link breaks. The prototype UI is preserved exactly, with the two **user-approved
in-style extensions** recorded in the spec: the create/edit form gains the model's missing fields, and
the list filter bar gains a badge select and a stock-availability select. No SPA, API, DRF, or Node
build is introduced.

## Technical Context

**Language/Version**: Python 3.12 (repo `venv/`)
**Primary Dependencies**: Django 5.x (server-rendered templates + ModelForms + admin); Pillow (new —
`ImageField` for `ProductImage`); WhiteNoise (static); production-only: psycopg[binary], gunicorn. No
DRF, no Node/bundler, no SPA framework.
**Storage**: SQLite for local development; PostgreSQL-ready for production (env-configured). New tables:
`products_productcategory`, `products_product`, `products_productimage`.
**Testing**: Django test runner (`manage.py test apps.products`) for models/forms/selectors/views
(ownership isolation, pricing validation, filters, lifecycle); manual visual-parity acceptance per
`quickstart.md`.
**Target Platform**: Linux server (WSGI/gunicorn in production); local `runserver` for dev.
**Project Type**: Web application (server-rendered Django + existing static frontend).
**Performance Goals**: Parity with the static prototype; list query bounded by pagination (12/page) with
`select_related('category')` + prefetch of the main image to avoid N+1.
**Constraints**: Frontend visually unchanged except the two sanctioned in-style form/filter extensions
(Principle I + spec Clarifications); merchant data isolation enforced at queryset level (Principle IV,
NON-NEGOTIABLE); all dynamic content DB-backed with truthful empty/zero states (Principle V); catalog is
physical-commerce only (Principle VIII); CSRF on every mutation; no forbidden tech; secrets via env.
**Scale/Scope**: 3 models; 1 app gains full code; 4 templates converted (1 shared create/edit form);
~8 routes + 4 legacy redirects; ~12 seeded demo products across the 6 categories; 1 seed command.

*No NEEDS CLARIFICATION remain — three spec clarifications resolved; see research.md for technical decisions.*

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

Evaluated against constitution **v2.0.0**:

| Principle | Status | Notes |
|---|---|---|
| I. Frontend Preservation (NON-NEGOTIABLE) | ✅ PASS (w/ recorded deviation) | List & detail markup, classes, `data-*` hooks, modals, RTL preserved exactly. **Two user-approved in-style extensions** (spec Clarifications, FR-011a/FR-004/FR-026): create/edit form gains the model's missing fields; filter bar gains badge + stock-availability selects — both required for backend integration and rendered in the prototype's existing style. Recorded in Complexity Tracking. |
| II. Server-Rendered Django — No SPA/API-First (NON-NEGOTIABLE) | ✅ PASS | Django views + ModelForms + templates only. No React/Vue/Next/Angular, no SPA router, no API/DRF, no Node build. Admin internal-only. |
| III. Modular App Architecture | ✅ PASS | `apps/products` owns `models.py`, `views.py`, `urls.py`, `forms.py`, `admin.py`, `selectors.py` (filtering/ownership queries), `services.py` (duplicate/status/profit logic), `management/commands/seed_products.py`, `migrations/`, and app-namespaced templates under `products/`. |
| IV. Role-Based Access & Owner-Scoped Data Isolation (NON-NEGOTIABLE) | ✅ PASS | First real ownership enforcement: every view `@role_required("is_merchant")`; every read/write goes through owner-scoped querysets (`Product.objects.filter(merchant=request.user)`); cross-merchant object access returns 404. No reliance on UI hiding. |
| V. Database-Backed Truth — No Fake Dynamic Data | ✅ PASS | All product content is DB-backed; zero static product rows remain; empty query → existing empty-state. Order-derived widgets (sales column, detail "recent orders") render **truthful zeros / empty-state** (0 orders exist this phase), not fabricated rows. |
| VI. Affiliate & Commission Integrity (NON-NEGOTIABLE) | ➖ N/A (modeled-for) | No commission/affiliate logic. Visibility rules FR-015/016 (Draft & Disabled excluded from affiliate/public browsing) are implemented as reusable selectors for the later affiliate phase; no attribution here. |
| VII. Customer Privacy on Affiliate Surfaces (NON-NEGOTIABLE) | ➖ N/A | No customer PII on product pages. |
| VIII. Physical-Commerce MVP Catalog | ✅ PASS | Six approved categories seeded; ProductForm category selector is limited to the merchant's (seeded) physical categories; seed contains only physical products; forbidden educational/digital data excluded (also guarded by the `physical-commerce-only` project memory). |

**Tech allow/deny**: Pillow (image handling for `ImageField`) ✅ not forbidden; SQLite (local) + PostgreSQL-ready (prod) ✅; WhiteNoise ✅; dev media served via Django's `static()` helper ✅; no SPA/API/DRF/Node ✅; Django admin internal-only ✅.

**Result**: PASS — one recorded, user-approved, in-style UI extension (Complexity Tracking); no NON-NEGOTIABLE breach.

### Post-Design Re-evaluation (after Phase 1)

Re-checked after producing research.md, data-model.md, contracts/routes.md, quickstart.md:

- No new dependency or pattern crosses a constitution line. Pillow is an image library, not a frontend framework/build system. Dev-only media serving uses Django's built-in helper.
- The clean-URL move plus legacy `*.html` redirects keeps Principle I's "no dead links" intact while adopting the spec's requested URLs; not-yet-converted pages are untouched.
- Ownership scoping is enforced in `selectors.py` (single source of truth for the owner queryset), consumed by every view — Principle IV holds by construction.
- The two in-style UI extensions remain the only deviation from strict markup preservation and are explicitly user-approved (spec Clarifications) and confined to the form + filter bar.
- **Result**: PASS (unchanged). Ready for `/speckit-tasks`.

## Project Structure

### Documentation (this feature)

```text
specs/004-products-catalog/
├── plan.md              # This file (/speckit-plan output)
├── spec.md              # Feature specification (+ 3 resolved clarifications)
├── research.md          # Phase 0 — resolved technical decisions
├── data-model.md        # Phase 1 — ProductCategory, Product, ProductImage
├── contracts/
│   └── routes.md        # Phase 1 — URL→view→access map + form/validation contract
├── quickstart.md        # Phase 1 — setup, seed, run, and acceptance verification
└── checklists/
    └── requirements.md  # Spec quality checklist (from /speckit-specify)
```

### Source Code (repository root)

Builds on the foundation layout. **New/changed paths** are marked; everything else is unchanged.

```text
config/
├── settings/
│   └── base.py                     # CHANGED: add MEDIA_URL, MEDIA_ROOT
│   └── local.py                    # CHANGED: serve MEDIA in dev (urlpatterns += static(...))
├── urls.py                         # CHANGED: include apps.products.urls before apps.core.urls
requirements/
└── base.txt                        # CHANGED: add Pillow
apps/products/
├── __init__.py
├── apps.py
├── models.py                       # NEW: ProductCategory, Product, ProductImage (+ TextChoices)
├── forms.py                        # NEW: ProductForm (validation), CategoryForm (admin/optional)
├── selectors.py                    # NEW: owner-scoped querysets + filter application
├── services.py                     # NEW: duplicate / set_status / delete / affiliate-profit calc
├── views.py                        # NEW: list, detail, create, edit, disable, enable, duplicate, delete, legacy redirects
├── urls.py                         # NEW: clean /products/… routes + legacy *.html redirects
├── admin.py                        # NEW: register 3 models; ProductImage inline; list_display/search/filters
├── migrations/
│   └── 0001_initial.py             # NEW
└── management/
    └── commands/
        └── seed_products.py        # NEW: idempotent physical-commerce seed (categories + ~12 products)
apps/products/templates/products/   # NEW app-namespaced templates (constitution III)
├── product_list.html               # from products.html  (extends merchant_base.html)
├── product_form.html               # from product-create.html / product-edit.html (shared create+edit)
└── product_detail.html             # from product-detail.html
templates/
├── includes/merchant_sidebar.html  # CHANGED: products.html link → {% url 'products:list' %}
├── products.html  product-create.html  product-detail.html  product-edit.html   # REMOVED (replaced by app templates; legacy URLs redirect)
apps/core/page_registry.py          # CHANGED: remove the 4 product PageEntry lines (now owned by apps.products)
media/                              # NEW (dev, gitignored): uploaded product images
```

**Structure Decision**: Single Django project at repo root (web application), extending the foundation.
The `apps/products` app gains the full constitution-III file set and owns its templates under
`apps/products/templates/products/` (discoverable via `APP_DIRS=True`). The four prototype root
templates are migrated into the app templates and removed; their old `*.html` URLs are served as
redirects to the new clean URLs so the ~66 inbound links from not-yet-converted pages keep resolving.
`ProductImage` uses an `ImageField` (Pillow) with new `MEDIA_*` settings; the MVP seeds with the
existing placeholder imagery so no real upload pipeline is required yet.

## Complexity Tracking

> No forbidden tech and no frontend redesign. Two deliberate, **user-approved** in-style UI extensions
> (recorded here so they are not a silent PASS of Principle I) and one bounded scope deferral.

| Item | Why Needed | Why Acceptable (not a NON-NEGOTIABLE breach) |
|---|---|---|
| Create/edit **form gains fields** (supplier price, affiliate profit, badge, featured flags) beyond the static prototype's inputs (FR-011a) | The model/feature require these fields and acceptance #9 requires in-form price/profit validation; they cannot be captured without inputs | Principle I explicitly permits changes "strictly required for backend integration"; fields are added in the prototype's exact visual style; user chose "Extend form in-style" (spec Clarifications, 2026-06-01). |
| List **filter bar gains** a badge select + stock-availability select (FR-004) | FR-004 requires filtering by badge and stock availability, with no existing controls | Same Principle-I carve-out; controls match the existing selects' style; user chose "Extend the filter bar in-style" (spec Clarifications). |
| Order-derived widgets (sales column, detail "recent orders") shown as **truthful zero / empty-state** rather than removed | Orders are out of scope (FR-025); the widgets are part of the preserved markup | Not fabricated data: 0 orders genuinely exist, so zeros/empty-state are *true* (Principle V). They become real in the later orders phase. |
