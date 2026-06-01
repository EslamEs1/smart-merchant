# Research & Technical Decisions: Products Catalog (MVP Phase 1)

**Feature**: 004-products-catalog
**Date**: 2026-06-01

The three open product-surface ambiguities were resolved during `/speckit-clarify` (see spec
Clarifications, Session 2026-06-01). This document records the **technical** decisions that turn the
clarified spec into the `apps/products` implementation. No `NEEDS CLARIFICATION` remain.

---

## 1. App ownership, file layout & templates

**Decision**: All product code lives in `apps/products` with the full constitution-III file set
(`models.py`, `views.py`, `urls.py`, `forms.py`, `admin.py`, `selectors.py`, `services.py`,
`management/commands/seed_products.py`, `migrations/`). Converted templates live app-namespaced at
`apps/products/templates/products/`: `product_list.html`, `product_form.html` (shared create+edit),
`product_detail.html`. The four prototype root templates are migrated into these and removed.

**Rationale**: Matches the spec's Template Conversion Rules (`products.html → products/product_list.html`
…) and constitution Principle III (app-owned, namespaced templates). `APP_DIRS=True` is already set, so
app templates resolve and can still `{% extends 'merchant_base.html' %}` from the root templates dir. A
single `product_form.html` for create and edit is the DRY Django norm (form pre-filled on edit).

**Alternatives considered**: Convert in place at the root `templates/` dir (as the foundation did for
`dashboard.html`) — rejected because the spec names app-namespaced target paths and the catalog is the
first app with enough templates to justify its own namespace.

---

## 2. URL strategy & legacy-link transition

**Decision**: Adopt clean URLs in `apps/products/urls.py` (`app_name = "products"`):

| Name | Path | Method |
|---|---|---|
| `list` | `products/` | GET |
| `create` | `products/create/` | GET, POST |
| `detail` | `products/<slug:slug>/` | GET |
| `edit` | `products/<slug:slug>/edit/` | GET, POST |
| `disable` | `products/<slug:slug>/disable/` | POST |
| `enable` | `products/<slug:slug>/enable/` | POST |
| `duplicate` | `products/<slug:slug>/duplicate/` | POST |
| `delete` | `products/<slug:slug>/delete/` | POST |

The 4 product `PageEntry` lines are removed from `apps/core/page_registry.py`; the freed legacy paths
are re-added in `apps/products/urls.py` as redirects: `product-create.html → products:create`;
`products.html → products:list`; `product-detail.html` and `product-edit.html → products:list` (no slug
is available from a static link). `config/urls.py` includes `apps.products.urls` **before**
`apps.core.urls`. The shared `templates/includes/merchant_sidebar.html` link is updated to
`{% url 'products:list' %}`.

**Rationale**: Fulfils the spec's clean-URL requirement while preserving Principle I's "no dead links":
~66 inbound `*.html` product links across ~32 not-yet-converted templates keep resolving via redirects,
with **zero edits** to those pages. The slug `<slug:slug>` converter matches the prototype's ASCII slugs
(`probass-x2`). Owner scoping (decision 4) disambiguates per-merchant slugs in the view.

**Alternatives considered**: (a) Rewrite all ~66 links now — rejected: high-churn, touches many
out-of-scope pages, and the prototype's generic `product-detail.html`/`product-edit.html` links carry no
slug to rewrite to. (b) Keep `*.html` URLs (foundation convention) — rejected: the spec explicitly
requests clean URLs for this surface.

---

## 3. Status, badge & currency representation

**Decision**: Model `TextChoices`:
- `Product.Status`: `ACTIVE="Active"`, `DRAFT="Draft"`, `DISABLED="Disabled"` (values are the English
  tokens the prototype badges already render; default `DRAFT`, matching the create form's checked radio).
- `Product.Badge`: `BESTSELLER="Bestseller"`, `NEW="New"`, `HOT_OFFER="Hot Offer"`,
  `HIGH_PROFIT="High Profit"`, `NONE="None"` (default `NONE`).
- `Product.Currency`: `SAR`, `EGP`, `AED`, `KWD`, `USD` (default `EGP` to match the catalog's `ج.م`
  display; the form preserves the prototype's option order).

**Rationale**: Constitution keeps status tokens in English in the UI; storing the English label as the
value lets templates render the existing badge text directly. Defaults mirror the prototype (Draft on
create; EGP in the list).

**Alternatives considered**: Short codes (`A`/`D`/`X`) with separate display labels — rejected as
needless indirection given the prototype already shows the English words.

---

## 4. Ownership scoping & access enforcement

**Decision**: Every view is decorated `@role_required("is_merchant")` (existing
`apps/core/decorators.py`). Object access uses an owner-scoped helper in `selectors.py`:
`get_owned_product_or_404(user, slug)` → `get_object_or_404(Product, merchant=user, slug=slug)`. List
reads go through `merchant_products(user)`. Cross-merchant access therefore returns **404** (spec's
"not found / forbidden"), never leaking existence.

**Rationale**: Principle IV (NON-NEGOTIABLE) demands view/queryset-level ownership checks, not UI hiding.
Centralizing the owner queryset in `selectors.py` gives one auditable source of truth reused by list,
detail, edit, and all mutations. 404 (vs 403) avoids confirming another merchant's slug exists.

**Alternatives considered**: `get_object_or_404(Product, slug=...)` then compare `merchant` in the view —
rejected: easy to forget per view; the scoped queryset makes leakage structurally impossible.

---

## 5. Pricing & affiliate-profit validation

**Decision**: Validation lives in `ProductForm.clean()` (and mirrored in `Product.clean()` for admin):
- `suggested_price >= supplier_price` (else field error on suggested price);
- `supplier_price`, `suggested_price`, `stock_quantity` ≥ 0; `affiliate_profit` ≥ 0;
- if `affiliate_profit` is left blank, set it to `suggested_price − supplier_price`
  (`services.compute_affiliate_profit`); if provided, keep the merchant's value.
Prices are `DecimalField(max_digits=10, decimal_places=2)`; stock is `PositiveIntegerField`.

**Rationale**: Satisfies FR-009/FR-010 and acceptance #9 with clear inline errors and preserved input
(Django ModelForm re-render). Mirroring in `Model.clean()` keeps admin edits honest.

**Alternatives considered**: DB `CheckConstraint`s only — kept as defense-in-depth for non-negativity
but insufficient alone (no friendly per-field message); form is the primary gate.

---

## 6. Slug & public-link uniqueness (two distinct fields)

**Decision** (per spec clarification): two independent fields.
- `slug`: internal, **unique per merchant** via `UniqueConstraint(fields=["merchant","slug"])`; drives
  `/products/<slug>/…`. Blank on submit → `slugify(name)`; if that collides for the merchant (or is
  empty for an all-Arabic name), append a short numeric/uuid suffix until unique-per-merchant.
- `public_link_slug`: the public `/p/…` link, **globally unique** via `unique=True`. Blank on submit →
  generated to a globally-unique value. Independent of `slug` (may match or differ).

Form-level uniqueness checks exclude the current instance on edit.

**Rationale**: A public `/p/<public_link_slug>` URL (built later) must resolve across all merchants →
global uniqueness; the internal route only needs per-merchant uniqueness so two merchants may share an
internal slug. Matches FR-008 and the spec clarification.

**Alternatives considered**: Single shared slug — rejected by the clarification (loses distinct
internal vs public link concepts and forces global uniqueness on the merchant-facing route).

---

## 7. Categories (per-merchant, seeded; admin-managed)

**Decision**: `ProductCategory` carries an owning `merchant` with
`UniqueConstraint(fields=["merchant","slug"])`. The six approved categories are created **per demo
merchant** by `seed_products`. The ProductForm category dropdown is scoped to the merchant's active
categories. Category CRUD is via Django admin (a lightweight `CategoryForm` is provided for admin/future
use); no new merchant-facing category page (none exists in the four converted pages).

**Rationale**: The model specifies a `merchant` FK → per-merchant categories; constitution Principle VIII fixes the
visible six. Seeding + admin discipline (not a hard DB enum) keeps categories as data while guaranteeing
the MVP shows only physical-commerce categories.

**Alternatives considered**: Global shared taxonomy (no merchant FK) — rejected: contradicts the
specified `merchant` field and the per-merchant isolation model.

---

## 8. Product images, media settings & placeholders

**Decision**: `ProductImage(product FK, image=ImageField(upload_to="products/"), alt_text, sort_order,
is_main, created_at)`. Add `Pillow` to `requirements/base.txt`; add `MEDIA_URL="/media/"` and
`MEDIA_ROOT=BASE_DIR/"media"` to `config/settings/base.py`; serve media in `local.py` via
`static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)`. MVP seed attaches the existing
per-product placeholder SVGs (under `static/img/placeholders/`) so the demo list matches the prototype;
templates render `product.main_image` when present, else a default placeholder `{% static %}` asset. A
`Product.main_image` helper returns the `is_main` image (or first by `sort_order`).

**Rationale**: Spec permits placeholder logic now while keeping the model upload-ready (FR-022). `ImageField`
needs Pillow. Dev media serving is Django's standard local pattern; production media storage is a later concern.

**Alternatives considered**: Defer `ImageField` entirely (store a path string) — rejected: spec wants the
model "ready for uploads." A real upload/storage backend (S3 etc.) — out of scope for the MVP.

---

## 9. Order-derived widgets (Principle V compliance)

**Decision**: The list "المبيعات" (sales) column renders **0** for every product, and the detail page's
"recent orders" table renders its **empty-state** (no rows), because zero orders exist this phase. No
fabricated sales numbers or order rows are emitted. Detail stats that depend on orders (revenue, sold
count) likewise show 0; a simple "related products" block, if rendered, draws from the merchant's other
products (DB-backed) rather than static rows.

**Rationale**: Principle V forbids fake dynamic data and fabricated rows; truthful zeros + empty-state
are compliant and become real in the orders phase. Keeps the markup (Principle I) without lying.

**Alternatives considered**: Keep the prototype's static sample numbers — rejected: violates Principle V
("a converted page that still shows hardcoded fake rows is NOT acceptance-eligible").

---

## 10. Lifecycle mutations as CSRF-protected POSTs

**Decision**: `disable`, `enable`, `duplicate`, `delete` are POST-only, each a small CSRF-protected form.
The preserved disable/delete modals wrap (or target) a form that POSTs to the row's action URL; the row
action menu sets the target product. `duplicate` (services.`duplicate_product`) clones fields + images,
regenerates `slug` (per-merchant) and `public_link_slug` (global), forces status `DRAFT`, and redirects
to the new product's edit page. `delete` redirects to the list with a success message; `disable`/`enable`
redirect back to the referring page (list or detail).

**Rationale**: Constitution security rules require CSRF on all mutations and login+role+ownership checks;
GET must stay side-effect-free. Modal markup and `data-*` hooks are preserved; only a form wrapper +
`{% csrf_token %}` are added.

**Alternatives considered**: Links/GET for disable/delete — rejected (unsafe, CSRF-exposed, violates
constitution).

---

## 11. Listing, filtering & pagination

**Decision**: `selectors.list_products(merchant, params)` starts from `merchant_products(merchant)` then
applies: `q` (icontains on `name` OR `public_link_slug`/`slug`), `category` (by category slug/id),
`status`, `badge`, and `stock` (`in` → `stock_quantity > 0`; `out` → `stock_quantity = 0`). Results are
`select_related("category")` + main-image prefetch, ordered by `-created_at`, paginated 12/page (Django
`Paginator`) with filter params preserved in pagination links via the querystring. Empty result →
existing empty-state block.

**Rationale**: Server-side filtering satisfies FR-004/SC-006; 12/page matches the prototype footer
("عرض 1–12 من 12"); `select_related`/prefetch keeps the list query flat.

**Alternatives considered**: Client-side JS filtering of all rows — rejected: not DB-backed, doesn't
scale, and contradicts the server-rendered model.

---

## 12. Seed data

**Decision**: `python manage.py seed_products` is idempotent (`get_or_create` keyed by merchant+slug). It
ensures a demo merchant exists (reusing the foundation's demo merchant if present, else creating one),
creates the six categories for that merchant, and creates ~12 physical-commerce products from the spec's
example list (ProBass X2, FitTime S9, WiFi cam 360, power bank, Type-C charger, Ring Light, air fryer,
shaver, waterproof backpack, hoodie, drawer organizer, laptop stand) spanning all six categories, with a
mix of statuses (Active/Draft/Disabled) and badges, and placeholder images. **No** educational/digital
items (constitution Principle VIII + `physical-commerce-only` memory).

**Rationale**: FR-024/SC-009; idempotency lets the command run repeatedly in dev without duplicates.
Aligns with `SAMPLE-DATA.md` canonical names/currencies.

**Alternatives considered**: A data migration — rejected: seed/demo data should be a re-runnable
management command, not baked into schema migrations.
