---
description: "Task list for Backend Foundation (Django Conversion — Phase 0)"
---

# Tasks: Backend Foundation (Django Conversion — Phase 0)

**Input**: Design documents from `/specs/003-backend-foundation/`
**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, contracts/routes.md, quickstart.md

**Tests**: NOT requested. Per plan.md, phase-0 acceptance is **manual** (visual + behavioral parity
per quickstart.md). No automated test tasks are generated; instead each story ends with manual
verification tasks mapped to the spec Success Criteria (SC-001…SC-008).

**Organization**: Tasks are grouped by user story so each story is an independently testable increment.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies on incomplete tasks)
- **[Story]**: Which user story the task belongs to (US1, US2, US3)
- Every task includes an exact file path

## Path Conventions

Single Django project at the **repository root** (per plan.md "Project Structure"). The static
prototype is absorbed: root `*.html` → `templates/`, `assets/` contents → `static/` (served at
`/assets/` via `STATIC_URL='/assets/'`). URLs mirror filenames so existing refs/links keep working.

**Authoritative page count**: 33 prototype pages (5 public/auth, 22 merchant, 6 affiliate) per
`contracts/routes.md` and the filesystem. 3 are converted to template inheritance this phase
(`login.html`, `dashboard.html`, `affiliate-dashboard.html`); 30 remain served verbatim.

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Stand up the Django project skeleton, settings, app packages, and absorb the prototype
assets/pages — without yet adding models, auth, or template inheritance.

- [x] T001 Create Django entry points at repo root: `manage.py` and `config/` package
  (`config/__init__.py`), with `DJANGO_SETTINGS_MODULE` defaulting to `config.settings.local` in
  `manage.py`.
- [x] T002 [P] Create `requirements/base.txt` (`Django>=5.0,<6.0`, `whitenoise`), `requirements/local.txt`
  (`-r base.txt`), `requirements/production.txt` (`-r base.txt` + `psycopg[binary]`, `gunicorn`).
- [x] T003 [P] Scaffold all 12 app packages under `apps/` (with `apps/__init__.py`): `core`, `accounts`,
  `merchants`, `products`, `orders`, `customers`, `affiliates`, `commissions`, `payouts`,
  `landing_pages`, `dashboard`, `notifications` — each with `__init__.py`, `apps.py`
  (`AppConfig.name = "apps.<x>"`), and empty `models.py`. (Code is added later only to `core`,
  `accounts`, `dashboard`.)
- [x] T004 Create the settings split `config/settings/{__init__,base,local,production}.py`:
  `base.py` = shared `INSTALLED_APPS` (django.contrib.* + whitenoise + the 12 `apps.*`), `TEMPLATES`
  pointing at `templates/`, `STATIC_URL='/assets/'`, `STATICFILES_DIRS=[BASE_DIR/'static']`,
  `AUTH_USER_MODEL='accounts.User'`, secrets via `os.environ`; `local.py` = `DEBUG=True` + SQLite
  (`db.sqlite3`) + permissive `ALLOWED_HOSTS`; `production.py` = `DEBUG=False` + PostgreSQL via env +
  WhiteNoise middleware + security headers + env `ALLOWED_HOSTS`. (Depends on T003 for app names.)
- [x] T005 [P] Create `config/urls.py` (root URLConf: `/admin/`, plus `include()` for `apps.core`,
  `apps.accounts`, `apps.dashboard`, and dev static serving), `config/wsgi.py`, `config/asgi.py`.
- [x] T006 [P] Relocate `assets/` contents into `static/` preserving names: `static/css/app.css`,
  `static/js/main.js`, `static/img/placeholders/*.svg` (51 SVGs). Remove the now-empty `assets/`.
- [x] T007 [P] Move all 33 prototype `*.html` files from the repo root into `templates/` **byte-for-byte
  unchanged** (no content edits in this phase; conversions happen in Phase 5).
- [x] T008 [P] Add `.gitignore` entries for `db.sqlite3`, `venv/`, `__pycache__/`, and `*.pyc`.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Make the project boot and migrate. The custom user model MUST exist before the first
migration (research §4), and `AUTH_USER_MODEL='accounts.User'` makes the model a hard startup
prerequisite for every story.

**⚠️ CRITICAL**: No user story work can begin until this phase is complete.

- [x] T009 Implement the custom user model in `apps/accounts/models.py`: `User(AbstractUser)` with a
  `Role` `TextChoices` (`MERCHANT` تاجر / `AFFILIATE` مسوّق بالعمولة / `ADMIN` مدير), a
  `role = CharField(choices=Role, default=Role.MERCHANT, max_length=16)`, and convenience properties
  `is_merchant` / `is_affiliate` / `is_admin` (per data-model.md), where `is_admin` is also True for
  `is_staff`/`is_superuser`. Set `email = EmailField(unique=True)`. `username` stays the canonical
  unique identifier; login is accepted **by email** via the auth backend wired in T019.
- [x] T010 [P] Register `User` in `apps/accounts/admin.py` for internal user management only (Django
  admin is the Admin/Staff landing target; never a customer-facing UI).
- [x] T011 Create and apply the initial migration: `python manage.py makemigrations accounts` then
  `python manage.py migrate` — produces the `accounts.User` table plus built-in
  `auth`/`admin`/`contenttypes`/`sessions` tables. No other app produces migrations. (Depends on T009.)
- [x] T012 Verify the project boots: `python manage.py check` passes with no system-check errors and
  `python manage.py runserver` starts cleanly (confirms `AUTH_USER_MODEL` resolves and settings load).

**Checkpoint**: App boots, DB migrated, `/admin/` reachable with a superuser. Stories can now begin.

---

## Phase 3: User Story 1 - The prototype runs as a served application, visually unchanged (Priority: P1) 🎯 MVP

**Goal**: Serve every prototype page through Django with assets loading and zero visual/behavioral
change versus the static files. This is the non-negotiable core (frontend preservation).

**Independent Test**: Start the app and open a representative page from each surface
(public, auth, merchant, affiliate) directly by URL; confirm pixel-equivalent appearance to the
static file, working interactions, resolving internal links, and no failed asset requests.

- [x] T013 [US1] Create `apps/core/page_registry.py`: a declarative list of all 33 pages as
  `(url path = filename, template, access-level)` tuples per `contracts/routes.md` (public / auth /
  merchant / affiliate), with `/` and `/index.html` both mapping to `index.html`. Access level is
  recorded as metadata now; enforcement is added in US2.
- [x] T014 [US1] Create the generic page-registry view and `apps/core/urls.py` in `apps/core/views.py`
  that renders each registry entry's template at a URL equal to its filename; wire `apps.core.urls`
  at the project root in `config/urls.py`. All 33 pages are served (open) at this stage.
- [x] T015 [US1] Preserve the JS hook attributes consumed by `static/js/main.js` in every served
  template (verbatim move already does this — confirm no template accidentally altered them):
  `[data-theme-toggle]`, `[data-sidebar-toggle]`, `[data-sidebar-overlay]`, `#sidebar`,
  `[data-actions-dropdown]`, `[data-modal-*]`, `[data-tab]/[data-tabs]`, `[data-copy*]`,
  `[data-favorite-toggle]`, `[data-gallery*]`, `[data-segments]/[data-segment]`,
  `[data-bottom-nav]/[data-nav-target]`, `#copied-toast` (per `contracts/routes.md` static-asset contract).
- [x] T016 [US1] **Verify SC-002**: open the served pages with DevTools Network and confirm every
  `assets/...` reference resolves to a 200 under `/assets/...` (css/app.css, js/main.js, img/placeholders
  SVGs) with **zero 404s** on a representative set from all three surfaces.
- [x] T017 [US1] **Verify SC-001 / SC-003 / SC-007** per quickstart.md: visual parity vs the static
  originals; interactions work (theme toggle persists, dropdown, modal, tabs, copy-button toast,
  favorite toggle, gallery thumbnail switch, affiliate bottom-nav active state); and every internal
  link resolves (no dead links) on sampled pages from each surface.

**Checkpoint**: Every prototype page is served and looks/behaves identically with assets loading —
a complete, demoable MVP on its own.

---

## Phase 4: User Story 2 - Role-based login and redirect skeleton (Priority: P2)

**Goal**: Real login routes users to their role home, login-required gating protects private pages,
and logout ends the session. Role is taken from the **account** (selector is informational).

**Independent Test**: With one merchant and one affiliate test account, log in as each and confirm
the correct landing surface; request a private page while logged out and confirm redirect to login;
log out and confirm the session ends.

- [x] T018 [US2] Implement the post-login role-dispatch view `post_login_redirect` in
  `apps/accounts/views.py`: `MERCHANT`→`/dashboard.html`, `AFFILIATE`→`/affiliate-dashboard.html`,
  `ADMIN`/staff→`/admin/`, unknown role→`/index.html`; honor a safe `?next=` when the user may view it.
  Key the admin branch off `is_staff`/`is_superuser` (a default superuser has `role=MERCHANT` but must
  still land on `/admin/`).
- [x] T019 [US2] Wire auth URLs in `apps/accounts/urls.py`: Django `LoginView` at `/login.html`
  (`template_name='login.html'`) and `LogoutView` at `/logout`; in `config/settings/base.py` set
  `LOGIN_URL='/login.html'` and `LOGIN_REDIRECT_URL` to the dispatch view (T018). Remove `login.html`
  from the raw page registry (now served by `LoginView`). Add an **email-or-username authentication
  backend** in `apps/accounts/backends.py` and register it in `AUTHENTICATION_BACKENDS` so the email a
  user types in the preserved login field authenticates them (`email` is unique per T009).
- [x] T020 [US2] Make the login form functional in `templates/login.html` (still flat, not yet
  extending a base): `<form method="post">` posting to the login URL, add `{% csrf_token %}`, keep the
  existing **email** input but give it Django's credential field name `username` (it carries the email
  value, resolved by the T019 backend) and name the password input `password`; keep the role selector
  **informational only**. The email label/placeholder and overall visual appearance MUST stay identical.
- [x] T021 [US2] Enforce login-required gating: in `apps/core/views.py` apply `login_required`
  (redirecting to `LOGIN_URL` with `?next=`) to registry entries whose access level is `merchant` or
  `affiliate`, reading the access metadata from `page_registry.py` (T013). Public/auth pages stay open.
  This phase gates raw registry pages by **login only** (not role); cross-role access to them is
  acceptable because they serve no owner-scoped data (FR-016). Role-specific gating is applied to the
  converted dashboards (T029/T030) and to each page as it is later data-converted.
- [x] T022 [US2] Confirm logout in `apps/accounts/urls.py`/settings ends the session and redirects to a
  public/auth page (`/login.html` or `/index.html`), and that all POST forms carry CSRF (FR-014).
- [x] T023 [US2] **Verify SC-004 / SC-005** per quickstart.md: create role test accounts (merchant1,
  affiliate1, a superuser), then confirm merchant→`/dashboard.html`, affiliate→`/affiliate-dashboard.html`,
  superuser→`/admin/`; logged-out request to `/dashboard.html`→`/login.html?next=/dashboard.html`;
  logout ends the session. Also **verify FR-018**: a bad-credentials login re-renders `login.html` with
  one generic error and never reveals which field was wrong.

**Checkpoint**: Login, role-based redirect, login-required gating, and logout all work — independently
testable on top of US1.

---

## Phase 5: User Story 3 - Separated base layouts with the first converted routes (Priority: P3)

**Goal**: Establish the four base layouts + shared shell includes and prove the gradual-conversion
mechanism by converting exactly one page per surface to template inheritance, visually identical.

**Independent Test**: Convert one public/auth, one merchant, and one affiliate page to extend their
bases; confirm each renders identically to its static original, edit a shared include once and see it
reflected across pages (de-dup proof), and confirm merchant/affiliate shells stay independent.

- [x] T024 [US3] Create `templates/base.html`: the shared `<head>` extracted verbatim from the
  prototype (Tailwind CDN, Lucide CDN, theme pre-paint script, `{% static 'css/app.css' %}`,
  `{% static 'js/main.js' %}`) plus the common `{% block %}`s (title, head_extra, body, content).
- [x] T025 [P] [US3] Create `templates/auth_base.html` extending `base.html` for the public/auth surface
  (minimal centered shell matching `login.html`/`register.html`).
- [x] T026 [P] [US3] Create `templates/merchant_base.html` extending `base.html`, plus
  `templates/includes/merchant_header.html` and `templates/includes/merchant_sidebar.html` extracted
  verbatim from the existing merchant shell (`dashboard.html`).
- [x] T027 [P] [US3] Create `templates/affiliate_base.html` extending `base.html`, plus
  `templates/includes/affiliate_header.html`, `templates/includes/affiliate_sidebar.html`, and
  `templates/includes/affiliate_bottom_nav.html` extracted verbatim from the affiliate shell
  (`affiliate-dashboard.html`), preserving the mobile-first layout.
- [x] T028 [US3] Convert `templates/login.html` to `{% extends 'auth_base.html' %}` (template
  inheritance), preserving the functional auth form from T020 and exact visuals.
- [x] T029 [US3] Convert `templates/dashboard.html` to `{% extends 'merchant_base.html' %}` +
  `{% include %}` the merchant header/sidebar; serve it via a real view in `apps/dashboard/views.py` +
  `apps/dashboard/urls.py` (login-required **and merchant-role-gated** via a role mixin/check), and
  remove `dashboard.html` from the raw registry.
- [x] T030 [US3] Convert `templates/affiliate-dashboard.html` to `{% extends 'affiliate_base.html' %}` +
  `{% include %}` the affiliate header/sidebar/bottom-nav; serve via `apps/dashboard` (login-required
  **and affiliate-role-gated** via a role mixin/check), and remove `affiliate-dashboard.html` from the
  raw registry.
- [x] T031 [US3] **Verify SC-008** per quickstart.md: view-source the 3 converted pages to confirm they
  render via `{% extends %}`/`{% include %}` yet look identical to the static originals; edit one
  include once and confirm all consumers reflect it (de-dup); confirm merchant vs affiliate shells stay
  visually independent (no cross-contamination).

**Checkpoint**: All three stories work; the gradual page-by-page conversion mechanism is proven.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Verify the constitution/spec guardrails and run the full acceptance pass.

- [x] T032 [P] Verify production hardening in `config/settings/production.py` (FR-015): `DEBUG=False`,
  `SECRET_KEY`/DB creds from env (no secrets committed), security headers, WhiteNoise static serving,
  env-driven `ALLOWED_HOSTS`.
- [x] T033 [P] Confirm scope guardrails (FR-016 / FR-017): no domain CRUD added (products/orders/
  customers/affiliates/commissions/payouts/landing-pages still serve hardcoded prototype content), and
  no forbidden tech introduced (no SPA/API/DRF/Node build); `merchants/products/orders/customers/
  affiliates/commissions/payouts/landing_pages/notifications` remain empty scaffolds.
- [x] T034 [P] Update `CLAUDE.md` (and `quickstart.md` if needed) with a short "how to convert the next
  page" note (registry → real view + `{% extends %}`), reflecting the 3 pages converted this phase.
- [x] T035 Run the full `quickstart.md` validation end-to-end (SC-001…SC-008) from a clean checkout and
  confirm the **Definition of Done** holds (SC-006: clean-checkout setup completes in a handful of
  documented commands).

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — start immediately. T004 depends on T003 (app names for
  `INSTALLED_APPS`); T001 precedes T004/T005 (config package must exist). T002/T006/T007/T008 are
  independent of the rest.
- **Foundational (Phase 2)**: Depends on Setup. T011 (migrate) depends on T009 (User model). **BLOCKS
  all user stories** (project must boot and migrate first).
- **User Stories (Phase 3–5)**: All depend on Foundational. They are designed to layer in priority
  order (US1 → US2 → US3) but each is independently testable:
  - US1 serves all pages openly.
  - US2 adds auth + flips private routes to login-required (reads US1's registry metadata).
  - US3 converts 3 pages to inheritance (login.html builds on US2's functional form).
- **Polish (Phase 6)**: Depends on all desired stories being complete.

### User Story Dependencies

- **US1 (P1)**: Only needs Foundational. Fully standalone MVP.
- **US2 (P2)**: Needs Foundational; reuses US1's page registry to apply gating, but its own
  login/redirect/logout behavior is independently testable.
- **US3 (P3)**: Needs Foundational; `login.html` conversion (T028) builds on US2's functional form
  (T020), and dashboard conversions are the redirect targets — but base layouts + de-dup are
  independently verifiable.

### Within Each User Story

- Registry/data before views; views before gating; base templates + includes before page conversions;
  manual verification (SC checks) last in each story.

### Parallel Opportunities

- Setup: T002, T003, T005, T006, T007, T008 can run in parallel (different files); T004 waits on T003.
- Foundational: T010 (admin) can run in parallel with T009 (model); T011 waits on T009.
- US3 base layouts T025, T026, T027 are parallel (different files) after T024 (`base.html`); the three
  page conversions T028/T029/T030 are largely parallel (different templates/apps).
- Polish: T032, T033, T034 are parallel; T035 runs last.

---

## Parallel Example: Phase 1 Setup

```bash
# After T001 (config package exists), launch these together (different files):
Task: "T002 Create requirements/{base,local,production}.txt"
Task: "T003 Scaffold all 12 apps/ packages"
Task: "T005 Create config/urls.py, wsgi.py, asgi.py"
Task: "T006 Relocate assets/ -> static/"
Task: "T007 Move 33 *.html -> templates/"
Task: "T008 Add .gitignore entries"
# Then T004 (settings) once T003 finishes.
```

## Parallel Example: Phase 5 base layouts

```bash
# After T024 (base.html), launch the surface bases together:
Task: "T025 templates/auth_base.html"
Task: "T026 templates/merchant_base.html + includes/merchant_*.html"
Task: "T027 templates/affiliate_base.html + includes/affiliate_*.html"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup.
2. Complete Phase 2: Foundational (CRITICAL — boots + migrates; blocks all stories).
3. Complete Phase 3: User Story 1.
4. **STOP and VALIDATE**: every prototype page served and visually unchanged, assets load, links work.
5. This is a shippable MVP (the "served application" milestone).

### Incremental Delivery

1. Setup + Foundational → project boots and migrates.
2. Add US1 → all pages served unchanged → **demo MVP**.
3. Add US2 → login + role redirect + gating → demo.
4. Add US3 → base layouts + 3 conversions → demo the gradual-conversion mechanism.
5. Polish → verify guardrails + full quickstart acceptance.

### Parallel Team Strategy

After Foundational, US1 (registry/serving), US2 (auth/redirect), and US3 (templates/includes) touch
mostly distinct files and can be split across developers, integrating at the registry (US1↔US2) and at
`login.html` (US2↔US3).

---

## Notes

- Tests are NOT included (not requested); acceptance is manual per quickstart.md. The `Verify …` tasks
  are the acceptance gates mapped to SC-001…SC-008.
- [P] tasks = different files, no incomplete-task dependencies.
- Frontend preservation is non-negotiable: move HTML/assets verbatim; only the 3 converted pages gain
  minimal `{% extends %}`/`{% include %}`/`{% static %}`/`{% csrf_token %}` tags, staying pixel-identical.
- **"Converted" = template conversion only** this phase (extends a base + includes); pages are NOT made
  database-backed (FR-016), so the template-converted dashboards keep their hardcoded prototype content
  and are not yet judged against constitution Principle V (database-backed truth).
- Commit after each task or logical group. Stop at any checkpoint to validate a story independently.
