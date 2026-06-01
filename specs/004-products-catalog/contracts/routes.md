# Routes & Form Contract: Products Catalog (MVP Phase 1)

**Feature**: 004-products-catalog
**Date**: 2026-06-01

For this server-rendered Django app the "interface contract" is the **URL → view → template → access**
map plus the **form/validation** behaviour and the **legacy-redirect** contract. Authoritative for what
this phase must serve. All product views require an authenticated **Merchant** and are **owner-scoped**.

---

## Access levels

- **merchant** — `@role_required("is_merchant")`: login required + `request.user.is_merchant`. Non-merchant
  roles → 403; unauthenticated → redirect to `LOGIN_URL` (`/login.html`).
- **owner-scoped** — the object must belong to `request.user`; otherwise **404** (existence not leaked).

---

## Clean routes (`apps/products/urls.py`, `app_name = "products"`)

| Name | URL | Method(s) | View | Template | Access | Behaviour |
|---|---|---|---|---|---|---|
| `list` | `/products/` | GET | `product_list` | `products/product_list.html` | merchant | Owner's products, filtered + paginated (12/page). Empty → empty-state. |
| `create` | `/products/create/` | GET, POST | `product_create` | `products/product_form.html` | merchant | GET: blank form. POST valid → create (owner = user) → redirect `detail`; invalid → re-render with errors. |
| `detail` | `/products/<slug:slug>/` | GET | `product_detail` | `products/product_detail.html` | merchant, owner-scoped | Render owner's product; order-derived widgets show zero/empty-state. |
| `edit` | `/products/<slug:slug>/edit/` | GET, POST | `product_edit` | `products/product_form.html` | merchant, owner-scoped | GET: pre-filled form. POST valid → update → redirect `detail`; invalid → re-render. |
| `disable` | `/products/<slug:slug>/disable/` | POST | `product_disable` | — | merchant, owner-scoped | status → `Disabled`; redirect back (list/detail) + message. |
| `enable` | `/products/<slug:slug>/enable/` | POST | `product_enable` | — | merchant, owner-scoped | status → `Active`; redirect back + message. |
| `duplicate` | `/products/<slug:slug>/duplicate/` | POST | `product_duplicate` | — | merchant, owner-scoped | Clone fields+images, new per-merchant `slug` + global `public_link_slug`, status forced `Draft`; redirect to new product's `edit` + message. |
| `delete` | `/products/<slug:slug>/delete/` | POST | `product_delete` | — | merchant, owner-scoped | Delete when safe (no dependents this phase); redirect `list` + message. |

**Notes**
- `<slug:slug>` is resolved within the owner queryset (`get_owned_product_or_404(user, slug)`), so
  per-merchant slug duplicates never collide across merchants.
- All POST routes are CSRF-protected (`{% csrf_token %}` in the modal/menu forms). GET routes are
  side-effect-free.
- Mutations reject non-POST with 405 (`require_POST`).

## Legacy redirects (preserve inbound `*.html` links; removed from `apps/core/page_registry.py`)

| Legacy URL | Redirect → | Type |
|---|---|---|
| `/products.html` | `products:list` | permanent (301) |
| `/product-create.html` | `products:create` | permanent (301) |
| `/product-detail.html` | `products:list` | permanent (301) — no slug in static link |
| `/product-edit.html` | `products:list` | permanent (301) — no slug in static link |

Registered in `apps/products/urls.py` so the ~66 inbound links from not-yet-converted pages keep
resolving with zero edits to those pages. `config/urls.py` includes `apps.products.urls` **before**
`apps.core.urls`.

---

## Filter contract (list view query params)

| Param | Values | Effect |
|---|---|---|
| `q` | free text | `name__icontains` OR `public_link_slug__icontains` / `slug__icontains` |
| `category` | category slug (or id) | exact category, owner-scoped |
| `status` | `Active` / `Draft` / `Disabled` | exact status |
| `badge` | `Bestseller` / `New` / `Hot Offer` / `High Profit` / `None` | exact badge |
| `stock` | `in` / `out` | `stock_quantity > 0` / `stock_quantity = 0` |
| `page` | integer | Django Paginator page |

- Unknown/blank params are ignored. Filters combine with AND. Active filters are echoed back into the
  controls and preserved in pagination links via the querystring. No-match → empty/zero-results state.
- The **badge** select and **stock-availability** select are the two new in-style controls (FR-004).

---

## Form contract — `ProductForm` (`apps/products/forms.py`)

**Fields (all merchant-editable, in-style additions per FR-011a)**: `category`, `name`,
`short_description`, `description`, `supplier_price`, `suggested_price`, `affiliate_profit`, `currency`,
`stock_quantity`, `status`, `badge`, `public_link_slug`, `seo_title`, `seo_description`, `video_url`,
`is_featured`, `is_best_seller`, `is_hot_offer`, plus the internal `slug` (optional input).

**Querysets / scoping**: `category` choices limited to `request.user`'s `ACTIVE` categories.

**Validation (`clean`)**:

| Rule | Error surfaced on |
|---|---|
| `name` required | `name` |
| `suggested_price >= supplier_price` | `suggested_price` |
| `supplier_price, suggested_price >= 0`; `stock_quantity >= 0`; `affiliate_profit >= 0` | respective field |
| `affiliate_profit` blank → set to `suggested_price − supplier_price` | (auto, no error) |
| `slug` unique per merchant (exclude self on edit); blank → `slugify(name)` (+suffix if needed) | `slug` |
| `public_link_slug` globally unique (exclude self on edit); blank → generated globally-unique | `public_link_slug` |
| `category` belongs to the same merchant | `category` |

On any failure the form re-renders with messages and preserves entered values; nothing is
created/changed (FR-007). On success the owner is set server-side from `request.user` (never trusted
from the form).

**`CategoryForm`** (optional, admin/back-office): `name`, `slug`, `description`, `icon`, `status`,
`sort_order`; `slug` unique per merchant. Category management is admin-only this phase.

---

## Manual acceptance hooks (see quickstart.md)

1. Owner-scoping: merchant A cannot GET/POST any of merchant B's product URLs → 404.
2. Pricing: `suggested < supplier` rejected; blank `affiliate_profit` auto-fills to the difference.
3. Slug: duplicate per-merchant `slug` rejected; blank `slug` auto-generated; `public_link_slug` global
   uniqueness enforced.
4. Filters: each of `q`/`category`/`status`/`badge`/`stock` and a combination narrows correctly;
   no-match shows empty state.
5. Lifecycle: disable→Disabled (hidden from `public_products`); enable→Active; duplicate→new Draft copy;
   delete→removed. All POST + CSRF; cross-owner denied.
6. Empty state renders for a merchant with zero products.
7. Visual parity: list/detail identical to prototype; form/filter-bar identical except the sanctioned
   in-style additions.
