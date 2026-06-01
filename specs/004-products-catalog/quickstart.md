# Quickstart: Products Catalog (MVP Phase 1)

**Feature**: 004-products-catalog
**Date**: 2026-06-01

How to set up, seed, run, and **acceptance-test** the database-backed product catalog. Assumes the
`003-backend-foundation` setup already works (venv, settings split, custom `User`).

---

## 1. Install & migrate

```bash
# from repo root, with the project venv active
pip install -r requirements/local.txt          # now includes Pillow (base.txt)
export DJANGO_SETTINGS_MODULE=config.settings.local

python manage.py makemigrations products        # creates products/0001_initial
python manage.py migrate
```

## 2. Seed demo data (idempotent)

```bash
python manage.py seed_products
# → ensures a demo merchant, the 6 physical categories, and ~12 physical products
#   (Active/Draft/Disabled mix, placeholder images). Safe to re-run.
```

Demo merchant credentials are printed by the command (or reuse the foundation's demo merchant). A second
merchant can be created in admin to test cross-merchant isolation.

## 3. Run

```bash
python manage.py runserver
# Merchant catalog:  http://127.0.0.1:8000/products/
# Admin (internal):  http://127.0.0.1:8000/admin/   (ProductCategory, Product, ProductImage)
```

Media (uploaded images) is served from `/media/` in local settings; seeded products use placeholder
imagery so no upload is required to see the list.

---

## 4. Acceptance verification

Maps to the spec's Acceptance Criteria (#1–#12), Functional Requirements, and Success Criteria.

### A. Browse own catalog (US1 · FR-001..004 · SC-002/006/007)

- [ ] `/products/` lists **DB-backed** products for the signed-in merchant; **no** static demo rows
      remain. Layout matches `products.html` (columns, badges, action dropdown, pagination, RTL).
- [ ] Filter by `q`, category, status, **badge**, **stock availability** (and a combination) → only
      matching owned products. The badge + stock selects are present, styled like the existing selects.
- [ ] A no-match filter and a zero-product merchant both show the existing **empty-state**.

### B. Create (US2 · FR-005/007/008/009/010/011a · SC-004/005)

- [ ] `/products/create/` shows the form **extended in-style** (supplier price, affiliate profit, badge,
      featured toggles added). Valid submit → product created (owner = me) → appears in list/detail.
- [ ] `suggested_price < supplier_price` → rejected with a clear message; values preserved; nothing saved.
- [ ] Blank `affiliate_profit` → auto-filled to `suggested − supplier`.
- [ ] Duplicate per-merchant `slug` → rejected; blank `slug` → auto-generated; `public_link_slug`
      collision (global) → rejected.

### C. Edit & detail (US3/US4 · FR-006/012 · SC-001/004)

- [ ] Edit page pre-filled; valid save persists and shows in list/detail.
- [ ] Detail page shows the product's **real** data in the existing layout. Order-derived widgets
      (sales column = 0, "recent orders" empty-state) show **truthful zero/empty**, no fabricated rows.

### D. Lifecycle (US5 · FR-013/014/014a · SC-008)

- [ ] Disable (modal, POST+CSRF) → status `Disabled`, excluded from `public_products`; Enable → `Active`.
- [ ] Duplicate ("تكرار", POST) → new **Draft** copy with fresh `slug`/`public_link_slug` and copied
      images; lands on the new product's edit page.
- [ ] Delete (modal, POST+CSRF) → product removed from the list.
- [ ] Draft products never appear in `public_products`.

### E. Ownership isolation (FR-017/018/019 · SC-003) — Principle IV (NON-NEGOTIABLE)

- [ ] As merchant A, request merchant B's `/products/<B-slug>/` (detail/edit) → **404**.
- [ ] POST to B's `/disable/`, `/enable/`, `/duplicate/`, `/delete/` as A → **404**, nothing changes.
- [ ] Unauthenticated `/products/` → redirect to `/login.html`; non-merchant role → 403.
- [ ] Every mutating POST without a valid CSRF token → 403.

### F. Categories & physical-commerce constraint (FR-020/021 · SC-009) — Principle VIII

- [ ] Only the six categories (إلكترونيات، إكسسوارات موبايل، أجهزة منزلية صغيرة، عناية شخصية، ملابس،
      أدوات منزلية) appear in the filter and form selectors.
- [ ] Seed data contains **zero** educational/digital items (كورسات/كتب/PDF/تدريب/اشتراكات تعليمية).

### G. Admin (FR-023 · SC-010)

- [ ] `ProductCategory`, `Product`, `ProductImage` are registered; Product admin has list display,
      search, filters, and an inline `ProductImage`.

### H. Link integrity & visual parity (FR-025/026 · SC-001) — Principle I

- [ ] Legacy links still resolve: `/products.html`→`/products/`, `/product-create.html`→`/products/create/`,
      `/product-detail.html` & `/product-edit.html`→`/products/`. No dead links from other pages.
- [ ] Side-by-side: `product_list.html` / `product_detail.html` are pixel-equivalent to the static
      originals; the form and filter bar match except the sanctioned in-style additions. Theme toggle,
      dropdowns, modals, copy buttons, gallery, RTL all still work.

---

## 5. Automated tests (`python manage.py test apps.products`)

Suggested coverage (authored in `/speckit-tasks`):

- **Models/forms**: pricing validation (suggested ≥ supplier; non-negatives), affiliate-profit default,
  per-merchant slug uniqueness + auto-gen, global `public_link_slug` uniqueness, category-merchant match.
- **Selectors**: `merchant_products` isolation; `public_products` excludes Draft/Disabled; each filter +
  combination.
- **Views**: owner-scoping 404 on cross-merchant for detail/edit/disable/enable/duplicate/delete;
  `@role_required` redirect/403; `require_POST` on mutations; duplicate forces Draft + fresh slugs;
  empty-state rendering; CSRF on POST.

## 6. Rollback

```bash
python manage.py migrate products zero    # drop product tables
# revert config/urls.py, config/settings (MEDIA_*), requirements/base.txt (Pillow),
# apps/core/page_registry.py (restore 4 PageEntry lines), and templates/includes/merchant_sidebar.html
```
