---
description: "Task list for Products Catalog (Database-Backed Conversion — MVP Phase 1)"
---

# Tasks: Products Catalog (Database-Backed Conversion — MVP Phase 1)

**Input**: Design documents from `/specs/004-products-catalog/`
**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, contracts/routes.md, quickstart.md

**Tests**: REQUESTED. plan.md ("Testing: Django test runner for models/forms/selectors/views — ownership
isolation, pricing validation, filters, lifecycle") and quickstart.md §5 call for an automated suite
under `apps/products/tests/`, **plus** manual visual-parity verification per story (Principle I). Both
are generated below. Automated tests target the high-value/security-critical logic (owner isolation —
Principle IV; pricing/slug validation; filters; lifecycle); they need not be written test-first, but the
listed tests MUST pass before a story is considered done.

**Organization**: Tasks are grouped by user story so each story is an independently testable increment.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependency on an incomplete task)
- **[Story]**: Which user story the task belongs to (US1–US5)
- Every task includes an exact file path

## Path Conventions

Single Django project at the **repository root** (per plan.md). Product code lives in `apps/products/`
with app-namespaced templates at `apps/products/templates/products/`. The four prototype root templates
(`templates/product*.html`) are migrated into the app templates and removed; their legacy URLs redirect
to the new clean `/products/…` routes. Foundation utilities reused: `apps/core/decorators.role_required`,
`templates/merchant_base.html`, `apps/core/page_registry.py`.

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Add the dependencies and media configuration the products app needs, before any models.

- [x] T001 [P] Add `Pillow` (for `ImageField`) to `requirements/base.txt`; confirm `requirements/local.txt` pulls it via `-r base.txt` and install into the venv.
- [x] T002 [P] Add `MEDIA_URL = "/media/"` and `MEDIA_ROOT = BASE_DIR / "media"` to `config/settings/base.py`.
- [x] T003 [P] Add `media/` (and `staticfiles/` if absent) to `.gitignore`.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Models, migration, admin, owner-scoping selectors/services, URL/media wiring, and seed data — everything every user story depends on.

**⚠️ CRITICAL**: No user story work can begin until this phase is complete.

- [x] T004 Create `ProductCategory` model in `apps/products/models.py` per data-model.md: fields (merchant FK `related_name="product_categories"`, name, slug, description, icon, status, sort_order, timestamps), `Status` TextChoices (`active`/`inactive`), `UniqueConstraint(["merchant","slug"])`, `Meta.ordering=["sort_order","name"]`, auto-slug from name.
- [x] T005 Add `Product` model to `apps/products/models.py` per data-model.md: all fields; `Status` (Active/Draft/Disabled, default Draft), `Badge` (Bestseller/New/Hot Offer/High Profit/None), `Currency` (SAR/EGP/AED/KWD/USD, default EGP) TextChoices; `UniqueConstraint(["merchant","slug"])`; `public_link_slug unique=True`; non-negative `CheckConstraint`s; `clean()` (suggested ≥ supplier, affiliate_profit default, category.merchant match); helpers `main_image`/`is_in_stock`/`get_absolute_url`; `Meta.ordering=["-created_at"]`. (Same file as T004 → after T004.)
- [x] T006 Add `ProductImage` model to `apps/products/models.py` per data-model.md: product FK `related_name="images"`, `ImageField(upload_to="products/", blank=True)`, alt_text, sort_order, is_main, created_at; single-`is_main`-per-product enforcement on save; `Meta.ordering=["sort_order","id"]`. (Same file → after T005.)
- [x] T007 Generate and apply the migration: `python manage.py makemigrations products` then `migrate` → creates `apps/products/migrations/0001_initial.py`. (Depends on T004–T006.)
- [x] T008 [P] Register models in `apps/products/admin.py`: `ProductCategory` (list_display, search, prepopulated slug), `Product` (list_display, search on name/slug/public_link_slug, list_filter on status/badge/category/currency/is_featured, prepopulated slug) with a `ProductImage` `TabularInline`.
- [x] T009 [P] Create `apps/products/selectors.py` with owner-scoping helpers: `merchant_products(user)`, `get_owned_product_or_404(user, slug)` (→ 404 cross-merchant), `public_products(qs)` (excludes Draft + Disabled — FR-015/016).
- [x] T010 [P] Create `apps/products/services.py` with `compute_affiliate_profit(suggested, supplier)` (used by the form; `duplicate_product`/`set_product_status` are added in US5).
- [x] T011 Create `apps/products/urls.py` skeleton: `app_name = "products"`, `urlpatterns = []` (routes added per story).
- [x] T012 Wire `config/urls.py`: add `path("", include("apps.products.urls"))` **before** the `apps.core.urls` include; under `if settings.DEBUG:` append `static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)`. (Depends on T011.)
- [x] T013 Create idempotent seed command `apps/products/management/commands/seed_products.py`: ensure a demo merchant (reuse foundation's if present), create the 6 physical categories per merchant, and ~12 physical products from the spec example list (Active/Draft/Disabled + badge mix, placeholder images), keyed by `get_or_create(merchant, slug)`. **No** educational/digital items. (Depends on T004–T007.)

**Checkpoint**: Models migrated, admin usable, seed runs, app routed. User stories can begin.

---

## Phase 3: User Story 1 - Merchant browses their own product catalog (Priority: P1) 🎯 MVP

**Goal**: A signed-in merchant sees their own DB-backed products with working filters and an empty state; no static rows remain.

**Independent Test**: Seed two merchants; sign in as each and confirm each sees only their own products; apply each filter + a combination; sign in as a zero-product merchant and confirm the empty state.

- [ ] T014 [US1] Remove the 4 product `PageEntry` lines (`products.html`, `product-create.html`, `product-detail.html`, `product-edit.html`) from `apps/core/page_registry.py`, adding a comment that `apps.products` now owns them.
- [ ] T015 [US1] Add filter logic to `apps/products/selectors.py`: `list_products(merchant, params)` applying `q` (name/slug/public_link_slug icontains), `category`, `status`, `badge`, `stock` (in=`>0`/out=`=0`), ordered `-created_at`, with `select_related("category")` + main-image prefetch.
- [ ] T016 [US1] Implement `product_list` view in `apps/products/views.py` (`@role_required("is_merchant")`, build filters from GET, paginate 12/page, pass active-filter context) and add the `path("products/", …, name="list")` route to `apps/products/urls.py`.
- [ ] T017 [US1] Add legacy redirects to `apps/products/urls.py`: `products.html`, `product-detail.html`, `product-edit.html` → `RedirectView`/view to `products:list` (permanent). (`product-create.html` redirect is added in US2.)
- [ ] T018 [US1] Update `templates/includes/merchant_sidebar.html`: change the products link `href="products.html"` → `{% url 'products:list' %}`.
- [ ] T019 [US1] Convert `apps/products/templates/products/product_list.html` from `templates/products.html`: `{% extends 'merchant_base.html' %}`, `{% load static %}`, loop DB rows (image via `main_image` else placeholder, name, public link, category badge, prices/currency, stock, status badge, **sales column = 0**), preserve the action dropdown + disable/delete modals + RTL, add the two **in-style** filter selects (badge, stock-availability) echoing active values, render the existing empty-state when no rows, and paginate preserving the querystring.
- [ ] T020 [US1] Delete the now-replaced `templates/products.html`.
- [ ] T021 [P] [US1] Tests in `apps/products/tests/test_selectors.py`: `merchant_products` isolation; `public_products` excludes Draft/Disabled; each of q/category/status/badge/stock + a combination.
- [ ] T022 [P] [US1] Tests in `apps/products/tests/test_views_list.py`: list is owner-scoped; `@role_required` redirects anonymous / 403s non-merchant; empty-state for zero products; filter results + pagination.
- [ ] T023 [US1] Manual visual-parity check (quickstart §A/§H): `/products/` vs static `products.html` — layout, badges, dropdown, modals, theme, RTL identical; list is DB-backed with no static rows (SC-001/002/006/007).

**Checkpoint**: US1 fully functional — DB-backed list with filters + empty state, owner-scoped. MVP.

---

## Phase 4: User Story 2 - Merchant creates a product (Priority: P2)

**Goal**: A merchant creates a product via the in-style-extended form with full validation; it appears in their list/detail.

**Independent Test**: Submit valid data → product persists under the merchant and shows in the list; submit invalid pricing + duplicate slug → form re-renders with errors, nothing created.

- [ ] T024 [US2] Create `apps/products/forms.py` `ProductForm` (ModelForm): all FR-011a fields; `category` queryset scoped to the merchant's `ACTIVE` categories; `clean()` → suggested ≥ supplier, non-negative prices/stock/profit, affiliate_profit default via `services.compute_affiliate_profit`, per-merchant `slug` uniqueness + auto-gen, global `public_link_slug` uniqueness + auto-gen, category-merchant match.
- [ ] T025 [US2] Implement `product_create` view in `apps/products/views.py` (GET blank form scoped to `request.user`; POST valid → set `merchant=request.user` server-side → save → redirect `products:detail`; invalid → re-render) and add `path("products/create/", …, name="create")` to `apps/products/urls.py`; add the `product-create.html` → `products:create` legacy redirect.
- [ ] T026 [US2] Convert `apps/products/templates/products/product_form.html` from `templates/product-create.html`: `{% extends 'merchant_base.html' %}`, render `ProductForm`, add the **in-style** fields (supplier price + affiliate profit in the pricing section, badge select + is-featured/is-best-seller/is-hot-offer toggles in the publish sidebar), `{% csrf_token %}`, preserve all sections/SEO/sidebar; bound for create.
- [ ] T027 [US2] Delete the now-replaced `templates/product-create.html`.
- [ ] T028 [P] [US2] Tests in `apps/products/tests/test_forms.py`: suggested ≥ supplier; non-negatives; affiliate_profit default; slug auto-gen + per-merchant uniqueness; `public_link_slug` global uniqueness; category scoping.
- [ ] T029 [P] [US2] Tests in `apps/products/tests/test_views_create.py`: valid POST persists with `merchant` from `request.user` (not trusted from form); invalid POST creates nothing and preserves values.
- [ ] T030 [US2] Manual (quickstart §B): create a product through the form; confirm it appears in list/detail; confirm invalid pricing/slug rejected with clear messages (SC-004/005).

**Checkpoint**: US1 + US2 work independently — browse and create.

---

## Phase 5: User Story 3 - Merchant edits a product (Priority: P2)

**Goal**: A merchant edits an owned product through the pre-filled form; cannot edit another merchant's product.

**Independent Test**: Edit one of your products → change persists in list/detail; open another merchant's edit URL → access denied (404).

- [ ] T031 [US3] Implement `product_edit` view in `apps/products/views.py` (`get_owned_product_or_404`; GET → `ProductForm(instance=…)` pre-filled; POST valid → save → redirect `products:detail`; invalid → re-render; uniqueness checks exclude self) and add `path("products/<slug:slug>/edit/", …, name="edit")`.
- [ ] T032 [US3] Update `apps/products/templates/products/product_form.html` to bind for edit (instance values + correct form `action`), keeping it the single shared create/edit template. (Same file as T026 → after T026.)
- [ ] T033 [P] [US3] Tests in `apps/products/tests/test_views_edit.py`: edit pre-fills and persists; cross-merchant edit GET/POST → 404; invalid rejected; slug uniqueness excludes self.
- [ ] T034 [US3] Manual (quickstart §C): edit a product → change shows in list/detail; another merchant's edit URL → 404.

**Checkpoint**: US1–US3 work independently — browse, create, edit.

---

## Phase 6: User Story 4 - Merchant views product detail (Priority: P3)

**Goal**: A merchant views an owned product's real data in the existing detail layout.

**Independent Test**: Open a product's detail → every product value matches the DB record and layout matches static `product-detail.html`; another merchant's detail URL → 404.

- [ ] T035 [US4] Implement `product_detail` view in `apps/products/views.py` (`get_owned_product_or_404`; context = product + images + **zeroed** order-derived widgets) and add `path("products/<slug:slug>/", …, name="detail")`.
- [ ] T036 [US4] Convert `apps/products/templates/products/product_detail.html` from `templates/product-detail.html`: `{% extends 'merchant_base.html' %}`, render real product fields, build the gallery from `product.images` (placeholder fallback), render the "recent orders" table as its **empty-state** and order-stats as **0** (Principle V), preserve gallery/JS hooks/modals/RTL.
- [ ] T037 [US4] Delete the now-replaced `templates/product-detail.html`.
- [ ] T038 [P] [US4] Tests in `apps/products/tests/test_views_detail.py`: owner's data rendered; cross-merchant detail → 404.
- [ ] T039 [US4] Manual (quickstart §C): detail shows real data; order widgets show zero/empty; cross-merchant → 404 (SC-001).

**Checkpoint**: US1–US4 work independently — full read + create/edit.

---

## Phase 7: User Story 5 - Merchant disables/enables, duplicates, and deletes a product (Priority: P3)

**Goal**: From the action menu/detail, a merchant disables/enables, duplicates (→ new Draft), and deletes products — all owner-scoped, POST + CSRF.

**Independent Test**: Disable → Disabled & excluded from `public_products`; enable → Active; duplicate → new Draft copy with fresh slugs/images; delete → removed; all cross-owner attempts → 404.

- [ ] T040 [US5] Add to `apps/products/services.py`: `set_product_status(product, status)`; `duplicate_product(product)` (clone fields + images, new per-merchant `slug` + global `public_link_slug`, status forced `Draft`); a delete-safety check (no dependents this phase).
- [ ] T041 [US5] Implement `product_disable`, `product_enable`, `product_duplicate`, `product_delete` views in `apps/products/views.py` (`@role_required("is_merchant")` + `@require_POST` + `get_owned_product_or_404`; duplicate → redirect new product's edit; delete → redirect list; disable/enable → redirect back) and add the 4 routes to `apps/products/urls.py`.
- [ ] T042 [US5] Wire the disable/delete modals and the duplicate/enable menu items in `apps/products/templates/products/product_list.html` to CSRF-protected POST forms targeting the row's action URLs, preserving the existing modal markup and `data-*` hooks. (Same file as T019 → after T019.)
- [ ] T043 [US5] Wire the disable/enable/duplicate/delete actions on `apps/products/templates/products/product_detail.html` as CSRF POST forms, preserving markup. (Same file as T036 → after T036.)
- [ ] T044 [P] [US5] Tests in `apps/products/tests/test_views_lifecycle.py`: disable→Disabled (excluded from `public_products`); enable→Active; duplicate→new Draft + fresh slugs + copied images; delete→removed; cross-owner → 404 on all four; non-POST → 405; missing CSRF → 403.
- [ ] T045 [US5] Manual (quickstart §D): exercise disable/enable/duplicate/delete via the UI modals/menu; confirm transitions, Draft duplicate, and deletion (SC-008).

**Checkpoint**: All five user stories independently functional — full merchant catalog CRUD + lifecycle.

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Constitution/acceptance sweeps spanning all stories.

- [ ] T046 [P] Physical-commerce audit: confirm seed + categories contain **zero** educational/digital items (`apps/products/management/commands/seed_products.py`) — SC-009, constitution VIII, `physical-commerce-only` memory.
- [ ] T047 [P] Ownership/security sweep across `apps/products/views.py`: every view has `@role_required("is_merchant")`, every read/write goes through the owner-scoped selectors (grep for any bare `Product.objects` in views), and every mutation is `@require_POST` + CSRF — Principle IV (NON-NEGOTIABLE), FR-017/018/019.
- [ ] T048 [P] Performance check: confirm the list query uses `select_related("category")` + main-image prefetch (no N+1) in `apps/products/selectors.py`.
- [ ] T049 [P] Visual-parity sweep over all four converted pages vs the static originals (theme toggle, dropdowns, modals, copy buttons, gallery, RTL) — SC-001, Principle I.
- [ ] T050 Run the full `quickstart.md` acceptance checklist (§A–§H) and the spec's 12 acceptance criteria; fix any gap.
- [ ] T051 [P] Confirm no leftover legacy product template files remain under `templates/`, admin works (SC-010), and update `README.md`/`SAMPLE-DATA.md` references to the catalog if needed.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: no dependencies — start immediately.
- **Foundational (Phase 2)**: depends on Setup — **BLOCKS all user stories**.
- **User Stories (Phase 3–7)**: all depend on Foundational. US1 is the MVP. US2/US3/US4/US5 each depend only on Foundational and are independently testable; recommended order is priority order (US1 → US2 → US3 → US4 → US5).
- **Polish (Phase 8)**: depends on the desired user stories being complete.

### Cross-story file touchpoints (sequencing notes)

- `apps/products/views.py`, `apps/products/urls.py`, `apps/products/services.py`: appended by multiple stories → edits are sequential per story (not cross-story [P]).
- `apps/products/templates/products/product_list.html`: created in US1 (T019), wired for actions in US5 (T042).
- `apps/products/templates/products/product_form.html`: created in US2 (T026), bound for edit in US3 (T032).
- `apps/products/templates/products/product_detail.html`: created in US4 (T036), wired for actions in US5 (T043).

### Within Each User Story

Selectors/forms/services → view + route → template conversion → tests → manual parity check.

### Parallel Opportunities

- Setup: T001, T002, T003 in parallel.
- Foundational: after models+migration (T004–T007), run T008/T009/T010 in parallel; T013 (seed) parallel with T008–T010.
- Each story's test files are `[P]` with each other (different files) once their implementation is done.
- With multiple developers, US2–US5 can proceed in parallel after Foundational, merging their distinct view/route/template additions.

---

## Parallel Example: Foundational Phase

```bash
# After models + migration (T004–T007) land, run in parallel:
Task: "Register models in apps/products/admin.py"                 # T008
Task: "Create apps/products/selectors.py owner-scoping helpers"   # T009
Task: "Create apps/products/services.py compute_affiliate_profit" # T010
Task: "Create seed command apps/products/management/commands/seed_products.py"  # T013
```

## Parallel Example: User Story 1 tests

```bash
Task: "Tests in apps/products/tests/test_selectors.py"    # T021
Task: "Tests in apps/products/tests/test_views_list.py"   # T022
```

---

## Implementation Strategy

### MVP First (User Story 1 only)

1. Phase 1 Setup → 2. Phase 2 Foundational (CRITICAL) → 3. Phase 3 US1.
4. **STOP & VALIDATE**: seed two merchants, verify owner-scoped DB-backed list + filters + empty state, visual parity.
5. Demo the MVP.

### Incremental Delivery

Foundation ready → US1 (browse, MVP) → US2 (create) → US3 (edit) → US4 (detail) → US5 (lifecycle). Each
story is a deployable increment that doesn't break the previous ones. Run that story's tests + manual
parity check before moving on; commit after each story.

---

## Notes

- `[P]` = different files, no dependency on an incomplete task.
- `[Story]` label maps each task to its user story for traceability.
- Principle I (frontend preservation) is non-negotiable: the only sanctioned UI changes are the two
  user-approved in-style extensions (form fields T026; filter selects T019) — every other class,
  `data-*` hook, modal, and RTL detail stays verbatim. Run the visual-parity check before closing a story.
- Principle IV (owner isolation) is non-negotiable: never use a bare `Product.objects` in a view — always
  the owner-scoped selectors.
- Total: **51 tasks** — Setup 3, Foundational 10, US1 10, US2 7, US3 4, US4 5, US5 6, Polish 6.
