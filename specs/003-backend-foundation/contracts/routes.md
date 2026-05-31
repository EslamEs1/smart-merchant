# Routes & Auth Contract: Backend Foundation (Phase 0)

**Feature**: 003-backend-foundation
**Date**: 2026-05-31

For a server-rendered Django app the "interface contract" is the **URL → template/view →
access** mapping plus the **authentication behavior**. This document is authoritative for what
this phase must serve. URLs mirror existing filenames (research §2); assets serve at `/assets/`
(research §1).

---

## Access levels

- **public** — anyone (no login).
- **merchant** — login required; intended for `role=MERCHANT` (full role gating per-page is
  completed in later phases; phase 0 guarantees login-required + correct landing).
- **affiliate** — login required; intended for `role=AFFILIATE`.
- **auth** — public auth pages (login/register).
- **converted** — page rendered via template inheritance in this phase (vs. raw registry).

---

## Auth contract

| URL | Method | Behavior |
|---|---|---|
| `/login.html` | GET | Render converted login page (extends `auth_base.html`) with Django auth form + `{% csrf_token %}`. |
| `/login.html` | POST | Authenticate via Django auth. On success → role-dispatch redirect. On failure → re-render with error, no leak of which field failed. |
| `/logout` (or Django default) | POST | End session, redirect to `/login.html` (or `/index.html`). |
| post-login dispatch | — | `accounts.views.post_login_redirect`: `MERCHANT`→`/dashboard.html`, `AFFILIATE`→`/affiliate-dashboard.html`, `ADMIN`/staff→`/admin/`, unknown→`/index.html`. |
| any **merchant**/**affiliate** URL while unauthenticated | GET | 302 → `/login.html?next=<url>`. After login, dispatch honors `next` when the user may view it, else role landing. |

Rules:
- All POST forms include CSRF protection (FR-014).
- `LOGIN_URL = '/login.html'`; `LOGIN_REDIRECT_URL` → the dispatch view.
- The login page's visual role selector is **informational**; the authoritative role is the
  authenticated account's `role`.
- Login accepts the **email** entered in the preserved form, resolved via an email-or-username
  authentication backend; `username` remains the canonical unique identifier (`email` is unique).

---

## Page map (URL → template → access)

### Public / auth (open)

| URL | Template | Access | Converted? |
|---|---|---|---|
| `/` and `/index.html` | `index.html` | public | raw |
| `/features.html` | `features.html` | public | raw |
| `/pricing.html` | `pricing.html` | public | raw |
| `/login.html` | `login.html` | auth | **converted** |
| `/register.html` | `register.html` | auth | raw |

### Merchant surface (login required)

| URL | Template | Access | Converted? |
|---|---|---|---|
| `/dashboard.html` | `dashboard.html` | merchant | **converted** |
| `/products.html` | `products.html` | merchant | raw |
| `/product-create.html` | `product-create.html` | merchant | raw |
| `/product-detail.html` | `product-detail.html` | merchant | raw |
| `/product-edit.html` | `product-edit.html` | merchant | raw |
| `/orders.html` | `orders.html` | merchant | raw |
| `/order-detail.html` | `order-detail.html` | merchant | raw |
| `/order-edit.html` | `order-edit.html` | merchant | raw |
| `/customers.html` | `customers.html` | merchant | raw |
| `/customer-detail.html` | `customer-detail.html` | merchant | raw |
| `/customer-edit.html` | `customer-edit.html` | merchant | raw |
| `/affiliates.html` | `affiliates.html` | merchant | raw |
| `/affiliate-detail.html` | `affiliate-detail.html` | merchant | raw |
| `/affiliate-requests.html` | `affiliate-requests.html` | merchant | raw |
| `/affiliate-payouts.html` | `affiliate-payouts.html` | merchant | raw |
| `/landing-pages.html` | `landing-pages.html` | merchant | raw |
| `/landing-page-create.html` | `landing-page-create.html` | merchant | raw |
| `/landing-page-preview.html` | `landing-page-preview.html` | merchant | raw |
| `/analytics.html` | `analytics.html` | merchant | raw |
| `/settings.html` | `settings.html` | merchant | raw |
| `/profile.html` | `profile.html` | merchant | raw |
| `/notifications.html` | `notifications.html` | merchant | raw |

### Affiliate surface (login required)

| URL | Template | Access | Converted? |
|---|---|---|---|
| `/affiliate-dashboard.html` | `affiliate-dashboard.html` | affiliate | **converted** |
| `/affiliate-product-detail.html` | `affiliate-product-detail.html` | affiliate | raw |
| `/affiliate-orders.html` | `affiliate-orders.html` | affiliate | raw |
| `/affiliate-earnings.html` | `affiliate-earnings.html` | affiliate | raw |
| `/affiliate-saved-products.html` | `affiliate-saved-products.html` | affiliate | raw |
| `/affiliate-profile.html` | `affiliate-profile.html` | affiliate | raw |

### Internal

| URL | Purpose | Access |
|---|---|---|
| `/admin/` | Django admin (User management only) | staff/superuser |
| `/assets/...` | Static assets (CSS/JS/img), `STATIC_URL='/assets/'` | public |

---

## Static-asset contract

- Every page's relative references (`assets/css/app.css`, `assets/js/main.js`,
  `assets/img/...`) MUST resolve to a 200 response under `/assets/...`.
- The JS hook attributes consumed by `assets/js/main.js` MUST remain intact in templates:
  `[data-theme-toggle]`, `[data-sidebar-toggle]`, `[data-sidebar-overlay]`, `#sidebar`,
  `[data-actions-dropdown]` + `.dropdown-panel`, `[data-modal-trigger]`/`[data-modal]`/
  `[data-modal-close]`, `[data-tab]`/`[data-tabs]`, `[data-copy]`/`[data-copy-container]`/
  `[data-copy-value]`, `[data-favorite-toggle]`, `[data-gallery]`/`[data-gallery-main]`/
  `[data-gallery-thumb]`, `[data-segments]`/`[data-segment]`, `[data-bottom-nav]`/
  `[data-nav-target]`, `#copied-toast`.

---

## Link-integrity rule

Every internal link in any served page MUST resolve to a URL in the page map above (or `/admin/`
or an `/assets/...` resource). No dead links may be introduced by the conversion (FR-013,
SC-007). Because URLs mirror filenames, the prototype's existing links already satisfy this.
