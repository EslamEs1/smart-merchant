# Research: Backend Foundation (Django Conversion — Phase 0)

**Feature**: 003-backend-foundation
**Date**: 2026-05-31
**Input**: spec.md, constitution v2.0.0

This document records the technical decisions for the foundation phase. Every decision is
constrained by the constitution: preserve the frontend exactly, server-rendered Django only,
no SPA/API/DRF/Node build, modular apps, role-based access, and physical-commerce scope.

---

## 1. Serving the existing static assets so references keep working

**Decision**: Serve the existing asset tree at the URL prefix **`/assets/`** by setting
`STATIC_URL = '/assets/'` and relocating the on-disk asset *contents* under `static/`
(`static/css/`, `static/js/`, `static/img/`). Use Django's `staticfiles` app; in production
serve them with **WhiteNoise**.

**Rationale**: Every existing page references assets relatively, e.g.
`<link href="assets/css/app.css">` and `<script src="assets/js/main.js">`. From a page served
at a root-level URL like `/dashboard.html`, the browser resolves `assets/css/app.css` to
`/assets/css/app.css`. A file on disk at `static/css/app.css` is served by Django at
`STATIC_URL + 'css/app.css'`. Setting `STATIC_URL = '/assets/'` therefore makes
`/assets/css/app.css` resolve with **zero edits to any HTML** — so even pages that have not yet
been converted to templates render with full styling from day one (satisfies FR-002, SC-002,
and Principle I). Converted templates reference assets as `{% static 'css/app.css' %}`, which
renders to the identical `/assets/css/app.css`.

**Reconciliation with the requested structure**: The user sketch shows `static/assets/`. We
place the asset *contents* directly under `static/` (so the static-relative path is
`css/app.css`, not `assets/css/app.css`) and set `STATIC_URL='/assets/'`. This deviates from
the literal `static/assets/` nesting specifically to preserve every existing reference without
rewriting HTML — which is the whole point of the foundation. The intent (assets live under
`static/`, served from the app) is honored.

**Alternatives considered**:
- `STATIC_URL='/static/'` with files at `static/assets/...` → existing refs (`/assets/...`)
  would 404 on every un-converted page. Rejected: breaks Principle I before conversion even
  starts.
- `STATIC_URL='/'` with files at `static/assets/...` → resolves refs but makes the static root
  shadow application routes. Rejected: fragile and surprising.
- Rewriting all asset refs to `{% static %}` up front → mass edit of 33 files, contradicts the
  "gradual, non-invasive" mandate. Rejected for the foundation.

---

## 2. URL strategy & inter-page links

**Decision**: Application URLs **mirror the existing page filenames** (e.g. `/dashboard.html`,
`/affiliate-dashboard.html`, `/login.html`), served from the project root URL space. The home
page (`/`) maps to `index.html`.

**Rationale**: Existing pages link to one another by filename (`href="dashboard.html"`,
`href="affiliate-product-detail.html"`). Serving each page at a URL equal to its filename means
every existing relative link resolves unchanged (FR-013, SC-007), with no link rewriting and no
risk of dead links. This is the lowest-risk path and matches the spec's chosen default. Clean
URLs (`/dashboard/`) can be layered in later as pages are converted, by adding aliases — out of
scope here.

**Alternatives considered**: Clean URLs now (`/dashboard/`, `/affiliate/dashboard/`) with link
rewriting → larger, riskier change touching every `href`. Rejected for the foundation.

---

## 3. Serving un-converted pages as templates

**Decision**: Move the 33 existing HTML files into `templates/` (preserving content
byte-for-byte except for the 3 pages converted in this phase). Serve each page through a small
**page registry** in `apps/core`: a declarative list of `(url_name, template, access)` tuples
rendered by a generic template view. Public pages are open; private pages require login.

**Rationale**: A registry avoids 33 hand-written near-identical URL/view pairs (DRY), makes the
public-vs-private access map explicit and reviewable in one place, and lets later phases "graduate"
a page from the registry to a real app view without touching other routes. The 3 converted pages
(see §6) get real views in their owning apps and are removed from the raw registry.

**Alternatives considered**:
- 33 explicit `TemplateView` URL entries → verbose, error-prone, scatters the access map.
- Flatpages app → adds DB rows and an editing model not needed for static prototype pages.
Both rejected.

---

## 4. Custom user model & role

**Decision**: Define a **custom user model** `accounts.User(AbstractUser)` with a
`role` field (`CharField` + `TextChoices`: `MERCHANT`, `AFFILIATE`, `ADMIN`) set
**before the first migration**. `ADMIN` aligns with Django's `is_staff`/`is_superuser` for the
admin site. Add `AUTH_USER_MODEL = 'accounts.User'`.

**Rationale**: Django strongly recommends a custom user model from the project's first migration —
swapping later is painful. A single `role` field gives unambiguous, testable post-login routing
(FR-006/FR-007) and a foundation for later per-surface authorization (Principle IV). Roles map
cleanly to the constitution's three roles.

**Alternatives considered**:
- Groups/permissions only → role redirect logic becomes implicit and harder to test; still
  fine later for fine-grained perms, but a first-class `role` field is clearer for routing.
- Separate `MerchantProfile`/`AffiliateProfile` with role inferred → deferred to later phases;
  not needed to prove the redirect skeleton.

---

## 5. Role-based login redirect & auth wiring

**Decision**: Use Django's built-in auth views for login/logout. Set `LOGIN_URL='/login.html'`
and `LOGIN_REDIRECT_URL` to a **role-dispatch view** (`accounts.views.post_login_redirect`)
that inspects `request.user.role` and redirects: Merchant → `/dashboard.html`, Affiliate →
`/affiliate-dashboard.html`, Admin/staff → the admin area (`/admin/` or a staff landing). An
account with no resolvable role falls back to a safe public page. Convert `login.html` to POST
to the Django login URL with `{% csrf_token %}` and correctly named username/password fields;
the page's existing role *selector* becomes informational (the authoritative role is the
account's `role`).

**Rationale**: A dispatch view is the standard, testable way to do role-based landing because
`LOGIN_REDIRECT_URL` is static. Reusing Django's auth views keeps the surface minimal and
secure (CSRF, session handling) per Principle II and the security rules. Login-required
redirects (FR-008) come for free from `LoginRequiredMixin`/`login_required` + `LOGIN_URL`.

**Alternatives considered**: Custom full login view → unnecessary; the built-in view plus a
redirect target is simpler. Storing intended role in session from the selector → contradicts
"role comes from the account"; rejected.

---

## 6. First route conversions (one per surface)

**Decision**: Convert exactly three pages to template inheritance in this phase:
- **Public/auth**: `login.html` → extends `auth_base.html`, real Django login form.
- **Merchant**: `dashboard.html` → extends `merchant_base.html`, served by `apps/dashboard`.
- **Affiliate**: `affiliate-dashboard.html` → extends `affiliate_base.html`, served by
  `apps/dashboard` (or `apps/affiliates`).

Each converted page MUST render visually identical to its static original (FR-012, SC-008). The
remaining 30 pages stay raw in the registry until later phases.

**Rationale**: Three conversions prove the inheritance + includes mechanism across all three
shells without taking on whole-app scope. `login.html` must convert anyway (it needs the real
auth form). Dashboards are the natural landing targets of the redirect skeleton.

---

## 7. Base templates & shared includes

**Decision**: Create four project-level base templates — `templates/base.html` (head, theme
pre-paint script, asset links, common `{% block %}`s), `templates/auth_base.html`,
`templates/merchant_base.html`, `templates/affiliate_base.html`. Extract repeated shell regions
into `templates/includes/`: `includes/merchant_sidebar.html`, `includes/merchant_header.html`,
`includes/affiliate_sidebar.html`, `includes/affiliate_header.html`,
`includes/affiliate_bottom_nav.html`. Merchant and affiliate bases stay visually independent
(FR-010, FR-011).

**Rationale**: The prototype already has a consistent merchant shell and a consistent affiliate
shell (the recent QA pass unified all 6 affiliate pages on one shell), so the shells extract
cleanly into includes. Bases centralize the `<head>` (Tailwind CDN, Lucide CDN, theme
pre-paint script, `app.css`, `main.js`) so every converted page inherits identical asset wiring.

---

## 8. Settings layout, database, and secrets

**Decision**: Split settings into `config/settings/{base,local,production}.py`.
- `base.py`: shared config, `INSTALLED_APPS`, templates, static, `AUTH_USER_MODEL`,
  middleware (incl. WhiteNoise in production via base + production toggle).
- `local.py`: `DEBUG=True`, **SQLite** (`db.sqlite3`), permissive `ALLOWED_HOSTS`.
- `production.py`: `DEBUG=False`, **PostgreSQL** via environment variables, security headers,
  WhiteNoise static, `ALLOWED_HOSTS` from env.
Secrets (SECRET_KEY, DB credentials) come from **environment variables** (stdlib `os.environ`
with safe defaults only in `local`). `DJANGO_SETTINGS_MODULE` defaults to
`config.settings.local` for development.

**Rationale**: Satisfies "PostgreSQL-ready, SQLite for local" and the security rules (no secrets
in source, DEBUG off in production, env-based config) with minimal dependencies. Stdlib
`os.environ` avoids adding `django-environ` for the foundation (kept as an optional later
convenience).

**Dependencies (this phase)**: `Django>=5.0,<6.0`, `whitenoise` (static serving). Production
adds `psycopg[binary]` and `gunicorn` (declared but only required at deploy time; not installed
in the local SQLite venv). No Node, no bundler, no DRF.

**Alternatives considered**: Single `settings.py` with env switches → muddier; the 3-file split
is the constitution's recommended shape. `django-environ`/`dj-database-url` → nice but extra
deps; deferred.

---

## 9. App scaffolding scope

**Decision**: Create all recommended apps as Python packages under `apps/` so the modular
structure exists: `core`, `accounts`, `merchants`, `products`, `orders`, `customers`,
`affiliates`, `commissions`, `payouts`, `landing_pages`, `dashboard`, `notifications`. In this
phase only `core` (page registry, base context), `accounts` (User model, auth wiring), and
`dashboard` (the two converted dashboards) carry real code. The rest are empty, registered
scaffolds (`apps.py` with `name='apps.<x>'`, empty `models.py`) awaiting their phase. Each app's
`AppConfig.name` uses the `apps.` prefix; `apps/` has an `__init__.py` (or apps are referenced
as `apps.<name>`).

**Rationale**: Establishes the architecture the constitution mandates without implementing
domain logic prematurely (FR-016). Empty apps add negligible cost and make later phases drop-in.

**Alternatives considered**: Create apps lazily per phase → leaves the structure incomplete now,
contrary to the explicit "establish project structure" goal.

---

## 10. Admin site

**Decision**: Enable Django admin **for internal user management only** (register `User`).
Admin is the Admin/Staff landing target. It is never used as a customer-facing product UI.

**Rationale**: Matches the constitution (Django admin internal only) and gives the Admin/Staff
role a destination for the redirect skeleton without building a custom staff UI in phase 0.

---

## Open questions

None. All foundation decisions are resolved; no `NEEDS CLARIFICATION` remain.
