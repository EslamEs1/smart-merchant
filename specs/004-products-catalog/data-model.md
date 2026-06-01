# Data Model: Products Catalog (MVP Phase 1)

**Feature**: 004-products-catalog
**Date**: 2026-06-01
**App**: `apps/products` (migration `0001_initial`)

Three new models, all owner-scoped to `accounts.User` (a Merchant). English status/badge tokens match
the prototype; all other content is Arabic/RTL. Decimal money, positive-integer stock.

---

## Entity: ProductCategory (`apps/products/models.py`)

A merchant-owned product grouping. The visible MVP is limited to the six approved physical-commerce
categories (seeded per merchant); the model itself is generic data (no hard enum) so categories remain
editable in admin.

| Field | Type | Notes |
|---|---|---|
| `merchant` | `FK(settings.AUTH_USER_MODEL, on_delete=CASCADE, related_name="product_categories")` | Owner; scopes all access |
| `name` | `CharField(max_length=120)` | Arabic display name (e.g. `إلكترونيات`) |
| `slug` | `SlugField(max_length=140, blank=True)` | Unique **per merchant**; auto from `name` if blank |
| `description` | `TextField(blank=True)` | Optional |
| `icon` | `CharField(max_length=64, blank=True)` | Optional (e.g. a Lucide icon name) |
| `status` | `CharField(choices=Status, default=ACTIVE, max_length=8)` | `active` / `inactive` |
| `sort_order` | `PositiveIntegerField(default=0)` | Manual ordering |
| `created_at` | `DateTimeField(auto_now_add=True)` | |
| `updated_at` | `DateTimeField(auto_now=True)` | |

- **`Status` (TextChoices)**: `ACTIVE="active"` (نشط), `INACTIVE="inactive"` (غير نشط).
- **Constraints**: `UniqueConstraint(fields=["merchant","slug"], name="uniq_category_slug_per_merchant")`.
- **Meta**: `ordering = ["sort_order", "name"]`; `verbose_name = "تصنيف"`.
- **Rules**: only the six approved categories appear in the visible MVP (seeded; constitution Principle VIII).
  The ProductForm category dropdown shows only the merchant's `ACTIVE` categories.
- **Relationships**: one merchant → many categories; one category → many products.

---

## Entity: Product (`apps/products/models.py`)

A merchant-owned physical-commerce item — the catalog core.

| Field | Type | Notes |
|---|---|---|
| `merchant` | `FK(AUTH_USER_MODEL, on_delete=CASCADE, related_name="products")` | Owner; scopes all access |
| `category` | `FK(ProductCategory, on_delete=PROTECT, related_name="products")` | Must belong to the same merchant (validated) |
| `name` | `CharField(max_length=200)` | Required |
| `slug` | `SlugField(max_length=220, blank=True)` | Internal; **unique per merchant**; drives `/products/<slug>/…`; auto from `name` if blank |
| `short_description` | `CharField(max_length=300, blank=True)` | Optional |
| `description` | `TextField(blank=True)` | Optional |
| `supplier_price` | `DecimalField(max_digits=10, decimal_places=2)` | Cost; ≥ 0 |
| `suggested_price` | `DecimalField(max_digits=10, decimal_places=2)` | Selling/suggested; ≥ `supplier_price` |
| `affiliate_profit` | `DecimalField(max_digits=10, decimal_places=2, blank=True)` | Defaults to `suggested−supplier` if blank; ≥ 0 |
| `currency` | `CharField(choices=Currency, default=EGP, max_length=3)` | `SAR/EGP/AED/KWD/USD` |
| `stock_quantity` | `PositiveIntegerField(default=0)` | ≥ 0; drives stock-availability filter |
| `status` | `CharField(choices=Status, default=DRAFT, max_length=8)` | `Active/Draft/Disabled` |
| `badge` | `CharField(choices=Badge, default=NONE, max_length=12)` | `Bestseller/New/Hot Offer/High Profit/None` |
| `public_link_slug` | `SlugField(max_length=220, unique=True, blank=True)` | Public `/p/…` link; **globally unique**; auto if blank |
| `seo_title` | `CharField(max_length=60, blank=True)` | Optional (UI maxlength 60) |
| `seo_description` | `CharField(max_length=160, blank=True)` | Optional (UI maxlength 160) |
| `video_url` | `URLField(blank=True)` | Optional |
| `is_featured` | `BooleanField(default=False)` | Publish-sidebar toggle |
| `is_best_seller` | `BooleanField(default=False)` | Publish-sidebar toggle |
| `is_hot_offer` | `BooleanField(default=False)` | Publish-sidebar toggle |
| `created_at` | `DateTimeField(auto_now_add=True)` | |
| `updated_at` | `DateTimeField(auto_now=True)` | |

- **`Status` (TextChoices)**: `ACTIVE="Active"`, `DRAFT="Draft"`, `DISABLED="Disabled"` (English tokens
  rendered by the prototype badges; default `DRAFT`).
- **`Badge` (TextChoices)**: `BESTSELLER="Bestseller"`, `NEW="New"`, `HOT_OFFER="Hot Offer"`,
  `HIGH_PROFIT="High Profit"`, `NONE="None"` (default `NONE`).
- **`Currency` (TextChoices)**: `SAR, EGP, AED, KWD, USD` (default `EGP`).
- **Constraints**:
  - `UniqueConstraint(fields=["merchant","slug"], name="uniq_product_slug_per_merchant")`
  - `public_link_slug` `unique=True` (global)
  - `CheckConstraint(supplier_price >= 0)`, `CheckConstraint(suggested_price >= 0)`,
    `CheckConstraint(affiliate_profit >= 0)` (defense-in-depth; friendly messages come from the form)
- **Meta**: `ordering = ["-created_at"]`; `verbose_name = "منتج"`.
- **`clean()`**: `suggested_price >= supplier_price`; default `affiliate_profit = suggested − supplier`
  when null; `category.merchant == self.merchant`.
- **Helpers**: `main_image` (the `is_main` image else first by `sort_order`);
  `is_in_stock` (`stock_quantity > 0`); `get_absolute_url()` → `products:detail`.
- **Relationships**: one merchant → many products; one category → many products; one product → many images.

### Visibility (selectors — for this phase and the later affiliate phase)

| Selector | Returns |
|---|---|
| `merchant_products(user)` | `Product.objects.filter(merchant=user)` — everything the owner manages (all statuses) |
| `public_products(qs)` | `qs.filter(status=Status.ACTIVE)` — excludes **Draft** and **Disabled** (FR-015/016); reused by the future affiliate/public surface |

### State transitions

```text
            create (default)
                 │
                 ▼
   ┌─────────►  DRAFT  ──publish──►  ACTIVE  ──disable──►  DISABLED
   │             ▲                      ▲                     │
   │             └────── edit ──────────┘                     │
   └──────────────────── enable ────────────────────────────-┘   (DISABLED → ACTIVE)
   duplicate(any) ──► new product forced to DRAFT
   delete(any)    ──► removed (when safe; no dependents this phase)
```

- `disable` → `DISABLED`; `enable` → `ACTIVE`. Draft is the default for new/duplicated products.
- Draft is owner-only visible; Disabled is owner-visible but excluded from public/affiliate listings.

---

## Entity: ProductImage (`apps/products/models.py`)

Upload-ready media for a product (MVP uses placeholders).

| Field | Type | Notes |
|---|---|---|
| `product` | `FK(Product, on_delete=CASCADE, related_name="images")` | Parent |
| `image` | `ImageField(upload_to="products/", blank=True)` | Pillow; blank allowed (MVP placeholders) |
| `alt_text` | `CharField(max_length=200, blank=True)` | Accessibility / SEO |
| `sort_order` | `PositiveIntegerField(default=0)` | Gallery order |
| `is_main` | `BooleanField(default=False)` | At most one main per product |
| `created_at` | `DateTimeField(auto_now_add=True)` | |

- **Meta**: `ordering = ["sort_order", "id"]`.
- **Rules**: at most one `is_main=True` per product (enforced in admin/save: setting one unsets others);
  list/detail render `product.main_image` else a default placeholder `{% static %}` asset.
- **Relationships**: many images per product; edited inline under Product in admin.

---

## Migration footprint (this phase)

- `products/0001_initial.py` creates `products_productcategory`, `products_product`,
  `products_productimage` with the constraints above.
- No changes to `accounts.User` (only new reverse relations `product_categories`, `products`).
- New `MEDIA_ROOT` directory is runtime state, not a migration.

## Admin (`apps/products/admin.py`)

| Model | list_display | search_fields | list_filter | extras |
|---|---|---|---|---|
| `ProductCategory` | name, merchant, status, sort_order | name, slug | status | prepopulate `slug` from `name` |
| `Product` | name, merchant, category, status, badge, suggested_price, stock_quantity | name, slug, public_link_slug | status, badge, category, currency, is_featured | `ProductImage` inline; prepopulate `slug`; `merchant` default = current user where applicable |
| `ProductImage` | (inline) | — | — | `TabularInline` on Product (image, alt_text, is_main, sort_order) |
