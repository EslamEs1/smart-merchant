# Implementation Plan: Backend Foundation (Django Conversion — Phase 0)

**Branch**: `003-backend-foundation` | **Date**: 2026-05-31 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/003-backend-foundation/spec.md`

## Summary

Stand up the Django foundation that turns the existing static Smart Merchant OS prototype into a
served application **without changing how anything looks**. Establish the project skeleton
(`config/` settings split, `apps/` modular packages, `templates/`, `static/`), a custom
`accounts.User` with a `role` field, Django auth with a role-based post-login redirect and
login-required gating, four base layouts plus shared shell includes, and serve all 33 prototype
pages — converting exactly one page per surface (login, merchant dashboard, affiliate dashboard)
to template inheritance to prove the gradual conversion path. Assets serve at `/assets/`
(`STATIC_URL='/assets/'`) and URLs mirror filenames, so every existing reference and link keeps
working untouched. No framework, SPA, API, DRF, or Node build is introduced.

## Technical Context

**Language/Version**: Python 3.12 (repo `venv/`)
**Primary Dependencies**: Django 5.x (server-rendered templates); WhiteNoise (static serving);
production-only: psycopg[binary], gunicorn. No DRF, no Node/bundler, no SPA framework.
**Storage**: SQLite for local development; PostgreSQL-ready for production (env-configured).
**Testing**: Django test runner (`manage.py test`) — pytest-django optional later; phase-0
acceptance is primarily manual per quickstart (visual + behavioral parity).
**Target Platform**: Linux server (WSGI/gunicorn in production); local `runserver` for dev.
**Project Type**: Web application (server-rendered Django + existing static frontend).
**Performance Goals**: Parity with the static prototype — pages load and interactions respond
as before; no measurable regression from serving through Django.
**Constraints**: Frontend MUST remain visually unchanged (Principle I); existing asset refs
(`assets/...`) and inter-page links (`*.html`) MUST keep resolving with zero edits to
un-converted pages; no forbidden tech; secrets via env; DEBUG off in production.
**Scale/Scope**: 33 served pages; 3 converted this phase; 1 persistent model (`User`); 12 app
packages (3 with code, 9 empty scaffolds).

*No NEEDS CLARIFICATION remain — see research.md for resolved decisions.*

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

Evaluated against constitution **v2.0.0**:

| Principle | Status | Notes |
|---|---|---|
| I. Frontend Preservation (NON-NEGOTIABLE) | ✅ PASS | HTML moved into `templates/` unchanged; only 3 pages gain minimal `{% extends %}`/`{% include %}`/`{% static %}`/`{% csrf_token %}` tags while staying visually identical. Assets at `/assets/`, links mirror filenames → no visual or link change. |
| II. Server-Rendered Django — No SPA/API-First (NON-NEGOTIABLE) | ✅ PASS | Django + templates only. No React/Vue/Next/Angular, no SPA router, no API/DRF, no Node build. Admin is internal-only. |
| III. Modular App Architecture | ✅ PASS | `apps/` with the recommended apps; project-level base templates only; logic in views/services as needed. |
| IV. Role-Based Access & Owner-Scoped Data Isolation (NON-NEGOTIABLE) | ✅ PASS (structural) | Role model + login-required + role redirect established now; the 3 converted private dashboards enforce role-specific access, while raw registry pages are login-required only and carry no owner-scoped data (FR-016) so no isolation is breached. Exhaustive per-page gating + object-ownership land as pages are data-converted (recorded in Complexity Tracking; spec Assumptions). |
| V. Database-Backed Truth — No Fake Dynamic Data | ✅ PASS | "Converted" this phase means **template conversion**, not **data conversion**: no domain page is made DB-backed. Un-converted *and* template-converted pages keep their hardcoded prototype content, which is allowed *until* a page is data-converted. No dashboard totals are claimed as real yet. |
| VI. Affiliate & Commission Integrity (NON-NEGOTIABLE) | ➖ N/A | Out of scope this phase; `affiliates`/`commissions`/`payouts` apps are empty scaffolds. |
| VII. Customer Privacy on Affiliate Surfaces (NON-NEGOTIABLE) | ➖ N/A | No affiliate↔customer data binding yet; affiliate pages still show prototype content. |
| VIII. Physical-Commerce MVP Catalog | ✅ PASS | No product data changes; catalog content untouched. |

**Tech allow/deny**: SQLite (local) + PostgreSQL-ready (prod) ✅; WhiteNoise ✅ (not a build
system); env-based secrets ✅; no forbidden tech proposed ✅; Django admin internal-only ✅.

**Result**: PASS — no violations, no Complexity Tracking entries required.

### Post-Design Re-evaluation (after Phase 1)

Re-checked after producing research.md, data-model.md, contracts/routes.md, quickstart.md:

- No new dependency or pattern crosses a constitution line. WhiteNoise + psycopg + gunicorn are
  runtime/deploy libraries, not frontend frameworks or build tooling.
- The asset decision (`STATIC_URL='/assets/'`, contents under `static/`) is specifically chosen
  to avoid editing HTML — reinforcing Principle I rather than threatening it.
- The page-registry serves un-converted pages verbatim; conversions are additive and visual-
  parity-gated. Principle I holds by construction.
- **Result**: PASS (unchanged). Ready for `/speckit-tasks`.

## Project Structure

### Documentation (this feature)

```text
specs/003-backend-foundation/
├── plan.md              # This file (/speckit-plan output)
├── spec.md              # Feature specification
├── research.md          # Phase 0 — resolved technical decisions
├── data-model.md        # Phase 1 — User + Role (domain models deferred)
├── contracts/
│   └── routes.md        # Phase 1 — URL→template→access map + auth contract
├── quickstart.md        # Phase 1 — setup, run, and acceptance verification
└── checklists/
    └── requirements.md  # Spec quality checklist (from /speckit-specify)
```

### Source Code (repository root)

Web-application layout introduced by this phase. Existing root `*.html` pages move into
`templates/`; existing `assets/` contents move under `static/` (served at `/assets/`).

```text
manage.py
requirements/
├── base.txt                     # Django, whitenoise
├── local.txt                    # -r base.txt
└── production.txt               # -r base.txt + psycopg[binary], gunicorn
config/
├── __init__.py
├── settings/
│   ├── __init__.py
│   ├── base.py                  # shared: INSTALLED_APPS, TEMPLATES, STATIC, AUTH_USER_MODEL
│   ├── local.py                 # DEBUG=True, SQLite
│   └── production.py            # DEBUG=False, PostgreSQL via env, WhiteNoise, security headers
├── urls.py                      # root URLConf: includes apps + core page registry + admin
├── wsgi.py
└── asgi.py
apps/
├── __init__.py
├── core/                        # page registry (serves raw prototype pages), base context, utils
│   ├── apps.py urls.py views.py page_registry.py
├── accounts/                    # custom User + Role, auth wiring, post-login dispatch
│   ├── apps.py models.py views.py urls.py forms.py admin.py migrations/
├── dashboard/                   # converted merchant + affiliate dashboards
│   ├── apps.py views.py urls.py
├── merchants/ products/ orders/ customers/ affiliates/
├── commissions/ payouts/ landing_pages/ notifications/   # scaffolded empty (apps.py only)
templates/
├── base.html                    # <head>: Tailwind CDN, Lucide CDN, theme pre-paint, app.css, main.js
├── auth_base.html
├── merchant_base.html
├── affiliate_base.html
├── includes/
│   ├── merchant_header.html  merchant_sidebar.html
│   ├── affiliate_header.html affiliate_sidebar.html affiliate_bottom_nav.html
├── login.html dashboard.html affiliate-dashboard.html   # CONVERTED (extend bases)
└── <remaining 30 prototype pages, served verbatim by the registry>
static/
├── css/  js/  img/              # former assets/ contents — served at /assets/ (STATIC_URL)
db.sqlite3                       # local only (gitignored)
```

**Structure Decision**: Single Django project at repo root (web application). The static
prototype is absorbed: HTML → `templates/`, `assets/` → `static/`. URLs mirror filenames and
`STATIC_URL='/assets/'` so the prototype's references and links keep working without edits.
Modular `apps/` are all created now (constitution III); only `core`, `accounts`, and `dashboard`
carry code in phase 0.

## Complexity Tracking

> No forbidden tech and no frontend redesign. One NON-NEGOTIABLE principle (IV) is satisfied only
> *structurally* this phase; the deliberate, user-approved scope deferral is recorded below so it is
> not a silent PASS.

| Violation / Deferral | Why Needed | Why Acceptable (not a NON-NEGOTIABLE breach) |
|-----------|------------|-------------------------------------|
| Principle IV per-page **role** gating + object-ownership deferred on the raw registry pages (login-required only) | Phase-0 scope is the auth/redirect skeleton; the raw pages carry no DB data to isolate yet (FR-016) | Served pages show only static prototype content, so cross-role access leaks no owner-scoped data — Principle IV's data-isolation rationale is not yet engaged. The 3 **converted** private dashboards DO enforce role; full gating + ownership land per-page as pages are data-converted. |
