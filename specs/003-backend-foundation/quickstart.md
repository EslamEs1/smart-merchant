# Quickstart: Backend Foundation (Phase 0)

**Feature**: 003-backend-foundation
**Date**: 2026-05-31

How to set up and run the Smart Merchant OS Django foundation locally, and how to verify the
acceptance criteria. Assumes Python 3.12 and the repo `venv/` (already present).

---

## Run it

```bash
# from repo root
source venv/bin/activate
pip install -r requirements/local.txt          # Django + whitenoise (local set)

export DJANGO_SETTINGS_MODULE=config.settings.local   # default for dev
python manage.py migrate                        # creates accounts.User + auth/admin/session tables
python manage.py createsuperuser                # an ADMIN/staff account

# create role test accounts (shell or admin)
python manage.py shell -c "from django.contrib.auth import get_user_model as g; U=g(); \
  U.objects.create_user('merchant1','m@example.com','pass12345', role='MERCHANT'); \
  U.objects.create_user('affiliate1','a@example.com','pass12345', role='AFFILIATE')"

python manage.py runserver                      # http://127.0.0.1:8000/
```

> No Node, no npm, no bundler. Tailwind and Lucide load via CDN exactly as in the prototype.
> Local uses SQLite; production settings target PostgreSQL via env vars.

---

## Verify (maps to spec Success Criteria)

**SC-001 / SC-002 — pages render identically, assets load**
1. Open `/` , `/features.html`, `/login.html` (public/auth).
2. Open `/dashboard.html`, `/products.html`, `/orders.html` (merchant) — log in first.
3. Open `/affiliate-dashboard.html`, `/affiliate-orders.html` (affiliate) — log in as affiliate.
4. Compare each against the original static file. Confirm DevTools Network shows **no 404s**
   for `/assets/...`.

**SC-003 — interactions still work** (on converted + sampled pages)
- Toggle dark/light (persists across reloads), open a dropdown and a modal, click a copy button
  (see `تم النسخ ✓` toast), toggle a favorite heart (fills/unfills), switch a gallery thumbnail
  on `affiliate-product-detail.html`, confirm affiliate bottom-nav active state.

**SC-004 — role redirect**
- Log in as `merchant1` → lands on `/dashboard.html`.
- Log in as `affiliate1` → lands on `/affiliate-dashboard.html`.
- Log in as the superuser → lands on `/admin/`.

**SC-005 — login required**
- While logged out, request `/dashboard.html` → redirected to `/login.html?next=/dashboard.html`.

**SC-007 — link integrity**
- From served pages, click sidebar / bottom-nav / in-page links; every link resolves (no 404,
  no dead link).

**SC-008 — first conversions render via inheritance**
- View source of `/login.html`, `/dashboard.html`, `/affiliate-dashboard.html`: each is produced
  by a template that `{% extends %}` its base and `{% include %}`s the shared shell, yet looks
  identical to the static original.

---

## Project layout (after this phase)

```text
manage.py
requirements/
  base.txt          # Django, whitenoise
  local.txt         # -r base.txt
  production.txt    # -r base.txt + psycopg[binary], gunicorn
config/
  settings/{base,local,production}.py
  urls.py  wsgi.py  asgi.py
apps/
  core/             # page registry, base context, shared utils
  accounts/         # custom User + role, auth wiring, post-login dispatch
  dashboard/        # converted merchant + affiliate dashboards
  merchants/ products/ orders/ customers/ affiliates/
  commissions/ payouts/ landing_pages/ notifications/   # scaffolded, empty (later phases)
templates/
  base.html  auth_base.html  merchant_base.html  affiliate_base.html
  includes/         # merchant_header, merchant_sidebar, affiliate_header,
                    # affiliate_sidebar, affiliate_bottom_nav
  <33 prototype pages as templates>
static/
  css/  js/  img/   # the former assets/ contents; served at /assets/ (STATIC_URL='/assets/')
db.sqlite3          # local only (gitignored)
```

---

## Converting the next page (summary)

1. Remove its `PageEntry` from `apps/core/page_registry.py`.
2. Add a view in the owning app (e.g. `apps/products/views.py`) decorated with `role_required("is_merchant")` (or `"is_affiliate"` for affiliate pages), imported from `apps.core.decorators`.
3. Wire `path("products.html", views.products_list, name="products")` in the app's `urls.py`.
4. Replace the template's boilerplate with `{% extends 'merchant_base.html' %}` (or `affiliate_base.html` / `auth_base.html`), add `{% block title %}` and `{% block content %}` with the page-specific markup only.
5. Replace `assets/img/...` with `{% static 'img/...' %}`. Leave all other HTML, CSS classes, and `data-*` hooks verbatim.
6. Visual check: open the converted page side-by-side with the static original and confirm pixel equivalence.

See `CLAUDE.md` for the full four-step guide.

---

## Definition of Done (phase 0 slice)

This phase is done when SC-001…SC-008 pass: the app runs, every prototype page is served and
looks unchanged with assets loading, all interactions work, role-based login/redirect and
login-required behavior work, and one page per surface is confirmed rendering through template
inheritance — with no frontend redesign and no forbidden tech introduced.
