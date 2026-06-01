# Feature Specification: Products Catalog (Database-Backed Conversion — MVP Phase 1)

**Feature Branch**: `004-products-catalog`  
**Created**: 2026-06-01  
**Status**: Draft  
**Input**: User description: "Smart Merchant OS Backend MVP — Products Catalog: convert the existing static product pages (products.html, product-create.html, product-edit.html, product-detail.html) into database-backed Django pages while preserving the current frontend design. Scope is limited to product categories, products, product media placeholders, pricing, stock, status, and merchant-owned product CRUD. Orders, affiliates, commissions, payouts, customers, and landing pages are explicitly out of scope."

## User Scenarios & Testing *(mandatory)*

This is the first **data conversion** phase after the backend foundation. Its value is turning the
product surface from a static mock into a real, merchant-owned catalog: a merchant signs in and
manages *their own* physical-commerce products — listing, creating, editing, viewing, disabling, and
deleting them — through the exact same pages they see today, now backed by a database instead of
hardcoded rows. Every page must remain visually indistinguishable from the static prototype
(Principle I, non-negotiable), and a merchant must never see or touch another merchant's products
(Principle IV, data isolation).

### User Story 1 - Merchant browses their own product catalog (Priority: P1)

A signed-in merchant opens the products page and sees a list of *their own* products pulled from the
database — not the hardcoded demo rows. Each row shows the product image, name, public link, category,
price, discount, stock, status, and the same per-row action menu as today. The merchant filters the
list by keyword, category, status, badge, and stock availability, and the list narrows accordingly.
If the merchant has no products yet, the existing empty-state ("لا توجد منتجات / ابدأ بإضافة منتجك
الأول") appears instead of an empty table.

**Why this priority**: This is the foundational read surface and the proof that the page is now
database-backed and owner-scoped. Everything else (create/edit/detail/lifecycle) writes into the data
this list reads. Without it there is no catalog.

**Independent Test**: Seed two merchants with different products, sign in as each, and confirm each
sees only their own products; apply each filter and a combination of filters and confirm the result
set is correct; sign in as a merchant with zero products and confirm the empty state renders.

**Acceptance Scenarios**:

1. **Given** a merchant with seeded products, **When** they open the products page, **Then** the table
   lists their products from the database with no leftover hardcoded demo rows, rendered identically to
   the static `products.html` layout (columns, badges, action dropdown, pagination, RTL).
2. **Given** a merchant with zero products, **When** they open the products page, **Then** the existing
   empty-state block is shown (and the table/pagination are not).
3. **Given** a populated list, **When** the merchant filters by a keyword, category, status, badge, or
   stock availability (or a combination), **Then** only matching products of that merchant are shown.
4. **Given** two merchants each owning products, **When** merchant A views the list, **Then** none of
   merchant B's products appear.

---

### User Story 2 - Merchant creates a product (Priority: P2)

A merchant opens the "add product" page and fills in the existing form — name, category, description,
pricing, stock, status, media, and SEO fields — then saves. A new product is created under their
ownership and appears in their list. Invalid input is rejected with clear, inline feedback while the
entered values are preserved.

**Why this priority**: Creating products is the primary write action that gives the catalog its
contents. It depends on the list (US1) existing to confirm the result and is the next most valuable
slice after being able to read.

**Independent Test**: As a signed-in merchant, submit the create form with valid data and confirm the
product persists and appears in the list; submit with invalid pricing and a duplicate slug and confirm
the form re-renders with errors and no product is created.

**Acceptance Scenarios**:

1. **Given** the create form, **When** the merchant submits valid data, **Then** a product is created,
   owned by that merchant, and is visible in their list and detail pages.
2. **Given** the create form, **When** the merchant leaves a required field empty or enters an invalid
   price relationship, **Then** the submission is rejected with a clear message and the entered values
   are preserved (no product created).
3. **Given** a slug the merchant already uses on another product, **When** they submit, **Then** the
   form reports the slug must be unique for that merchant (no product created).
4. **Given** a blank slug, **When** the merchant submits, **Then** the system generates a unique slug
   for that merchant from the product name.

---

### User Story 3 - Merchant edits a product (Priority: P2)

A merchant opens a product's edit page, sees the form pre-filled with that product's current values,
changes some of them, and saves. The product is updated and the changes are reflected in the list and
detail pages. A merchant cannot open or submit the edit page for a product they do not own.

**Why this priority**: Editing is the natural counterpart to creating and is required for real catalog
management, but it is only meaningful once products exist (US2).

**Independent Test**: As a merchant, edit one of your products, save, and confirm the change persists;
attempt to open the edit page for another merchant's product and confirm access is denied.

**Acceptance Scenarios**:

1. **Given** a product the merchant owns, **When** they open its edit page, **Then** the form is
   pre-filled with the product's current values.
2. **Given** the edit form, **When** the merchant saves valid changes, **Then** the product is updated
   and the changes appear in the list and detail.
3. **Given** a product owned by another merchant, **When** the merchant tries to open or submit its edit
   page, **Then** access is denied (not found / forbidden) and nothing changes.
4. **Given** the edit form, **When** the merchant submits invalid pricing or a slug that collides with
   another of their products, **Then** the update is rejected with a clear message.

---

### User Story 4 - Merchant views product detail (Priority: P3)

A merchant opens a product's detail page and sees that product's real information — name, category,
status, pricing, stock, description, media — rendered in the existing detail layout (gallery, info
cards, quick actions). The page reflects the database record, not the demo content.

**Why this priority**: Detail is a read convenience that reuses data already created/edited; valuable
but not blocking for catalog management.

**Independent Test**: Open the detail page for a known product and confirm every product-specific value
matches the database record and the layout matches the static `product-detail.html`.

**Acceptance Scenarios**:

1. **Given** a product the merchant owns, **When** they open its detail page, **Then** the product's
   real data is shown in the existing detail layout.
2. **Given** a product owned by another merchant, **When** the merchant requests its detail page,
   **Then** access is denied (not found / forbidden).

---

### User Story 5 - Merchant disables/enables, duplicates, and deletes a product (Priority: P3)

From the list action menu (or detail page), a merchant disables a product — it stays in their catalog
but is marked Disabled and must not appear in any public/affiliate browsing — and can re-enable it
later. The merchant can duplicate a product to quickly start a similar one, and can delete a product
when it is safe to do so, confirmed through the existing delete modal.

**Why this priority**: Lifecycle controls complete the CRUD story and protect catalog hygiene, but the
catalog is already usable without them.

**Independent Test**: Disable a product and confirm its status becomes Disabled and it is excluded from
any public/affiliate-facing query; re-enable it and confirm it returns; delete a product via the modal
and confirm it is removed from the list.

**Acceptance Scenarios**:

1. **Given** an Active product, **When** the merchant confirms "تعطيل" in the disable modal, **Then** the
   product's status becomes Disabled and it is excluded from public/affiliate-facing listings.
2. **Given** a Disabled product, **When** the merchant re-enables it, **Then** its status returns to
   Active and it becomes eligible for public/affiliate listings again.
3. **Given** a product that is safe to delete, **When** the merchant confirms "حذف" in the delete modal,
   **Then** the product is removed and no longer appears in their list.
4. **Given** a product the merchant owns, **When** they choose "تكرار" (Duplicate), **Then** a new
   Draft product owned by them is created with the source's fields and images copied and fresh unique
   `slug` / `public_link_slug` values, and it appears in their list.
5. **Given** any disable/enable/duplicate/delete action, **When** it targets a product the merchant does
   not own, **Then** the action is denied and nothing changes.

---

### Edge Cases

- **Empty catalog**: a merchant with zero products sees the existing empty-state, never an empty table
  shell or leftover demo rows.
- **Cross-merchant access**: directly requesting another merchant's product detail/edit/disable/delete
  URL (by guessing a slug) MUST be denied; product slugs are only unique *per merchant*, so the same
  slug may exist for two merchants and each resolves only within its owner's scope.
- **Invalid pricing**: a suggested/selling price lower than the supplier price, or any negative price or
  negative stock, MUST be rejected with a clear message.
- **Slug collisions**: a slug that duplicates one the same merchant already uses MUST be rejected; a
  blank slug MUST be auto-generated uniquely from the name.
- **Draft visibility**: a Draft product appears only to its owning merchant — never in public/affiliate
  browsing.
- **Disabled visibility**: a Disabled product is excluded from public/affiliate browsing but remains
  visible and manageable to its owning merchant.
- **Out-of-scope columns**: the list's "المبيعات" (sales) column and the detail page's "recent orders"
  table reflect order data that does not exist in this phase; they MUST remain present (frontend
  preservation) showing neutral placeholder values rather than fabricated per-product sales (see
  Assumptions).
- **Filter combinations**: combining filters (e.g., category + status + stock availability + keyword)
  MUST narrow correctly, including returning an empty result that still shows the empty/zero-results
  presentation rather than stale rows.
- **Category constraint**: only the six approved physical-commerce categories are offered; no
  educational/digital category or sample data is ever introduced (see Dependencies → physical-commerce
  constraint).

## Requirements *(mandatory)*

### Functional Requirements

**Catalog list & filtering**

- **FR-001**: The products list page MUST display products read from the database, scoped to the
  authenticated merchant, replacing all hardcoded demo rows; no fabricated static product rows may
  remain in the converted page.
- **FR-002**: The list MUST preserve the existing table structure, columns, category/status badges,
  per-row action dropdown, pagination control, modals, RTL layout, and JS hooks exactly as in
  `products.html`.
- **FR-003**: When the authenticated merchant owns no products, the page MUST show the existing
  empty-state block instead of the table/pagination.
- **FR-004**: The list MUST support backend filtering by search keyword (matching product name and
  public link/slug), category, status, badge, and stock availability, individually and in combination,
  returning only the merchant's matching products. The filter bar is **extended in-style**: the existing
  search box, category select, and status select are retained, and a **badge select** and a
  **stock-availability select** are added next to them in the prototype's current visual style.
  Stock availability is defined as **In stock = stock quantity > 0** and **Out of stock = stock
  quantity = 0**.

**Product create / edit**

- **FR-005**: A merchant MUST be able to create a product through the existing create form; the new
  product MUST be owned by that merchant.
- **FR-006**: A merchant MUST be able to edit a product they own through the existing edit form,
  pre-filled with the product's current values.
- **FR-007**: The product form MUST validate input and, on failure, re-render the form with clear
  messages while preserving entered values and creating/changing nothing.
- **FR-008**: A product's internal `slug` MUST be unique per merchant and drives the merchant-facing
  routes (`/products/<slug>/`, `/edit/`, `/disable/`, `/delete/`); if the merchant leaves it blank, the
  system MUST generate a slug unique for that merchant from the product name. The separate
  `public_link_slug` (the public `/p/...` link) MUST be **globally unique** across all merchants so it
  can resolve unambiguously when the public product page is built in a later phase; if left blank it MUST
  be generated to a globally-unique value. The two fields are independent (they may hold the same or
  different values).
- **FR-009**: The system MUST validate the pricing relationship so that the suggested/selling price is
  greater than or equal to the supplier price, and MUST reject negative prices, negative affiliate
  profit, and negative stock.
- **FR-010**: Affiliate profit MUST default to the difference between the suggested price and the
  supplier price unless a value is explicitly provided.
- **FR-011**: Product status MUST be one of Active, Draft, or Disabled; product badge MUST be one of
  Bestseller, New, Hot Offer, High Profit, or None.
- **FR-011a**: The visible create/edit form MUST expose, as merchant-editable inputs added to the
  existing form sections in the prototype's current visual style, all required product fields: category,
  name, short description, description, supplier price, suggested price, affiliate profit, currency,
  stock quantity, status, badge, public link slug, SEO title, SEO description, video URL, and the
  is-featured / is-best-seller / is-hot-offer flags. The existing "السعر الأصلي" input maps to the
  suggested/selling price; supplier price and affiliate profit are added to the pricing section
  (affiliate profit pre-filled from suggested − supplier and editable); the badge selector and flag
  toggles are added to the publish/status sidebar.

**Detail**

- **FR-012**: The product detail page MUST render the selected product's real database values in the
  existing detail layout (gallery, info cards, description, quick actions), with no demo content for
  product-specific fields.

**Lifecycle (disable / enable / delete)**

- **FR-013**: A merchant MUST be able to disable a product they own (status → Disabled) via the existing
  disable modal, and re-enable it (status → Active).
- **FR-014**: A merchant MUST be able to delete a product they own when it is safe to do so, confirmed
  through the existing delete modal; in this phase a product is considered safe to delete when no other
  records depend on it (none do yet, as orders/commissions are out of scope).
- **FR-014a**: A merchant MUST be able to duplicate a product they own via the existing "تكرار"
  (Duplicate) action in the row action menu. Duplication MUST create a new product owned by the same
  merchant, copying the source product's fields and images, generating a new internal `slug` (unique per
  merchant) and a new globally-unique `public_link_slug`, and forcing the new product's status to Draft
  so the copy is not unintentionally published. A merchant MUST NOT be able to duplicate another
  merchant's product.

**Visibility rules**

- **FR-015**: Draft products MUST be visible only to their owning merchant and MUST NOT appear in any
  public or affiliate-facing listing.
- **FR-016**: Disabled products MUST be excluded from public and affiliate-facing browsing while
  remaining visible and manageable to their owning merchant.

**Ownership & security**

- **FR-017**: Every product list, detail, create, edit, disable, enable, and delete operation MUST be
  scoped to the authenticated merchant; a merchant MUST NOT be able to view or manage another
  merchant's products, and attempts to do so MUST be denied (not found / forbidden).
- **FR-018**: All product create/edit/disable/enable/delete submissions MUST include cross-site request
  forgery protection.
- **FR-019**: The product pages MUST be reachable only by authenticated merchant users; unauthenticated
  access MUST redirect to login and non-merchant roles MUST be denied.

**Categories**

- **FR-020**: The category options offered throughout the product surface MUST be limited to the six
  approved physical-commerce categories — إلكترونيات, إكسسوارات موبايل, أجهزة منزلية صغيرة, عناية شخصية,
  ملابس, أدوات منزلية — and MUST NOT include any educational or digital category (كورسات، كتب، PDF،
  ملفات تعليمية، تدريب، محاضرات، اشتراكات تعليمية).
- **FR-021**: A category MUST carry an owning merchant, name, slug, optional description, optional icon,
  active/inactive status, and a sort order, and the active categories MUST drive the category filter and
  the create/edit category selector.

**Media**

- **FR-022**: A product MUST support one or more associated images, each with alt text, a sort order,
  and a "main image" flag; the data model MUST be ready for real image uploads even if this MVP uses
  placeholder images for seeded/demo content.

**Administration**

- **FR-023**: Product categories, products, and product images MUST be manageable through the
  administrative back office with list display, search, and relevant filters, and product images
  editable inline within a product.

**Seed / demo data**

- **FR-024**: Seed/demo data MUST contain only physical-commerce products (e.g., the listed examples
  such as سماعة بلوتوث ProBass X2, ساعة ذكية FitTime S9, قلاية هوائية 4 لتر, شاحن سريع Type-C 65W) and
  MUST NOT contain any course/book/PDF/training/subscription/educational items.

**Scope guardrails**

- **FR-025**: This phase MUST NOT implement orders, affiliate attribution, commission creation, payouts,
  customers, landing pages, real payment, or real shipping; order-derived UI already present on the
  converted pages MUST be preserved visually but left non-functional/placeholder (see Assumptions).
- **FR-026**: The conversion MUST NOT alter the rendered appearance or interactive behavior of the four
  product pages versus their static originals (Principle I), with two sanctioned exceptions, both added
  in the prototype's existing visual style: (a) the create/edit form gains additional merchant-editable
  fields per FR-011a, and (b) the list page's filter bar gains a badge select and a stock-availability
  select per FR-004. The detail page retains its exact markup; the list page retains its exact table,
  columns, action dropdown, pagination, modals, classes, `data-*` hooks, and RTL layout aside from the
  two added filter controls.

### Key Entities *(include if feature involves data)*

- **Product Category**: A merchant-owned grouping of products. Attributes: owning merchant, name, slug,
  optional description, optional icon, status (active/inactive), sort order, created/updated timestamps.
  Constrained in this phase to the six approved physical-commerce categories. Relationship: one merchant
  has many categories; one category has many products.
- **Product**: A merchant-owned physical-commerce item. Attributes: owning merchant, category, name,
  slug (internal, unique per merchant — drives merchant routes), short description, description, supplier
  price, suggested price, affiliate profit, currency, stock quantity, status (Active/Draft/Disabled),
  badge (Bestseller/New/Hot Offer/High Profit/None), public link slug (globally unique — the public
  `/p/...` link), SEO title, SEO description, optional video URL, and the flags is-featured /
  is-best-seller / is-hot-offer, plus created/updated timestamps. Relationship: one merchant has many
  products; one product belongs to one category and has many images.
- **Product Image**: A media item for a product. Attributes: parent product, image (upload-ready), alt
  text, sort order, is-main flag, created timestamp. Relationship: many images per product, at most one
  marked main.
- **Merchant (existing)**: The owning user (from the accounts/role foundation) whose ownership scopes
  every category, product, and image. No new merchant data is introduced here.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of the four converted product pages render visually identical to their static
  originals (verified by side-by-side comparison), with all existing interactions still working.
- **SC-002**: Zero fabricated/static product rows remain in the converted pages — the list reflects only
  database records for the signed-in merchant.
- **SC-003**: In 100% of attempts, a merchant sees and can act on only their own products; every attempt
  to view or manage another merchant's product is denied.
- **SC-004**: A merchant can create a valid product and see it in their list, and edit it and see the
  change, each in a single form submission.
- **SC-005**: 100% of invalid submissions (missing required field, suggested price below supplier price,
  negative price/stock, duplicate per-merchant slug) are rejected with a clear message and create/change
  nothing.
- **SC-006**: Each filter (keyword, category, status, badge, stock availability) and any combination
  returns exactly the merchant's matching products; a no-match result shows the empty/zero presentation,
  not stale rows.
- **SC-007**: A merchant with zero products always sees the empty-state.
- **SC-008**: Disabling a product removes it from public/affiliate-facing listings in 100% of cases while
  keeping it visible to its owner; re-enabling restores it. Draft products never appear in
  public/affiliate-facing listings.
- **SC-009**: Only the six approved physical-commerce categories are selectable anywhere on the product
  surface; zero educational/digital categories or sample products exist in seed data.
- **SC-010**: Product categories, products, and product images are each manageable in the admin back
  office with working list display, search, filters, and inline images.

## Assumptions

- **Authentication & roles** are provided by the existing accounts/role foundation (feature
  `003-backend-foundation`); "merchant" means a user whose stored role is Merchant, and product pages
  use the existing merchant role guard.
- **Categories are per-merchant** (each category carries an owning merchant, as specified) and are
  seeded with the six approved physical-commerce categories for the demo merchant(s). Category
  create/edit is handled through the admin back office (and an optional category form) rather than a new
  merchant-facing category-management page, since none of the four converted pages includes one.
- **Pricing field reconciliation** — *resolved (see Clarifications)*: the form is **extended in-style**.
  The existing "السعر الأصلي" input maps to the **suggested/selling price**; a new **supplier (cost)
  price** input and an auto-filled-but-editable **affiliate profit** input are added to the pricing
  section in the prototype's current style. All three prices are merchant-editable and validated in the
  form (suggested ≥ supplier; non-negative; affiliate profit defaults to suggested − supplier).
- **Order-derived UI is preserved but inert**: the list's "المبيعات" (sales) column and the detail
  page's "recent orders" table show order/sales data that does not exist this phase; per frontend
  preservation they remain in place displaying neutral placeholder values (e.g., zero / dashes / the
  existing static sample left clearly as a non-product placeholder) and become real in a later orders
  phase. They are not treated as "fake product rows" under FR-001/SC-002.
- **Currency** is stored per product with the existing selector options (SAR/EGP/AED/KWD/USD); the
  prototype's list display convention (e.g., "ج.م") is preserved.
- **Clean URLs** are adopted for the product surface as requested (`/products/`, `/products/create/`,
  `/products/<slug>/`, `/products/<slug>/edit/`, `/products/<slug>/disable/`, `/products/<slug>/delete/`,
  plus `/products/<slug>/duplicate/` for the duplicate action).
  Internal links that previously pointed to the `*.html` product pages are updated to the new paths
  (and/or the old `*.html` paths redirect to them) so no internal link is broken — superseding, for these
  four pages only, the foundation phase's filename-mirroring convention.
- **Delete safety**: because orders, commissions, and other dependents are out of scope, no product has
  blocking dependents in this phase, so a confirmed delete proceeds; disabling is presented as the
  preferred, reversible alternative.
- **Image uploads** may use placeholder logic in this MVP; seeded products reuse the existing placeholder
  SVGs, and the image model is built upload-ready for a later phase.
- **Visual "identical"** is judged by human side-by-side review of each converted page against its static
  original (no automated pixel-diff harness exists).
- **The "badge" field and the is-featured / is-best-seller / is-hot-offer flags** exist on the model as
  specified and, per the Clarifications resolution, are **merchant-editable in the visible form** — a
  badge selector and the three flag toggles are added to the publish/status sidebar in the prototype's
  current style (also remaining manageable via the admin back office).

## Dependencies

- **Backend foundation** (`003-backend-foundation`): Django project skeleton, `accounts.User` + role,
  merchant base template/layout, role-based access guards, and static asset serving are prerequisites.
- **Static prototype** (`001-static-frontend-mvp`): the four product pages (`products.html`,
  `product-create.html`, `product-edit.html`, `product-detail.html`) are the input artifacts whose
  markup, classes, `data-*` hooks, modals, and RTL layout are preserved.
- **Project constitution** (`.specify/memory/constitution.md`, v2.0.0): governs frontend preservation
  (Principle I), data-isolation (Principle IV), database-backed truth (Principle V), and the forbidden
  technologies.
- **Physical-commerce constraint** (persistent project rule): the catalog and all sample data must never
  reintroduce course/book/PDF/digital/subscription/educational products or copy.

## Out of Scope

- Orders, order items, sales metrics, and the order-derived UI's real data.
- Affiliate attribution, affiliate product browsing implementation, commissions, and payouts.
- Customers, landing pages, real payment gateways, and real shipping.
- Public/customer-facing product storefront pages (only the merchant-facing catalog surface is in scope).
- Real image upload pipeline/storage tuning beyond an upload-ready model (placeholders acceptable now).

## Clarifications

### Session 2026-06-01

- Q: The existing visible product form exposes only "السعر الأصلي" (original price) and "سعر الخصم"
  (discount price) plus a currency selector, but the required model/form lists supplier price, suggested
  price, affiliate profit, a badge value, and is-featured/is-best-seller/is-hot-offer flags. How should
  the merchant-facing form reconcile this gap with the frontend-preservation principle? → A: **Extend the
  form in-style.** The visible merchant form is extended to expose all required fields, added into the
  existing form sections using the prototype's current visual style (same spacing, controls, RTL): the
  existing "السعر الأصلي" input maps to the **suggested/selling price**; a new **supplier (cost) price**
  input and an auto-filled, editable **affiliate profit** input are added to the pricing section; a
  **badge** selector and **is-featured / is-best-seller / is-hot-offer** toggles are added to the publish
  sidebar. This fully satisfies the required ProductForm field list and the pricing/affiliate-profit
  validation (acceptance criterion #9). The form's *field set* therefore grows relative to the static
  prototype while its *visual style* is preserved; this is the one sanctioned deviation from strict
  markup preservation, limited to the create/edit form pages (the list and detail pages keep their exact
  markup).
- Q: FR-004 requires filtering by badge and stock availability, but the existing filter bar only has
  search, category, and status controls. Add the missing filter controls or preserve the bar as-is? →
  A: **Extend the filter bar in-style.** Add a badge select and a stock-availability select (In stock =
  qty > 0 / Out of stock = qty = 0) alongside the existing search/category/status controls, styled like
  the current selects; all five filters are implemented. This is the second sanctioned in-style UI
  extension (see FR-004, FR-026).
- Q: `Product` has both `slug` and a separate `public_link_slug`; what is each one's uniqueness scope and
  which drives the merchant URL? → A: **Two distinct fields.** The internal `slug` is unique per merchant
  and drives the merchant-facing routes (`/products/<slug>/`…); `public_link_slug` (the public `/p/...`
  link) is **globally unique** across all merchants so it resolves unambiguously when the public product
  page is built later. The fields are independent and may hold the same or different values (see FR-008).
- Q: The list action menu has a "تكرار" (Duplicate) item not in the required view set — implement it or
  leave it inert? → A: **Implement Duplicate.** The action clones a product the merchant owns into a new
  product owned by the same merchant, copying its fields and images, generating a fresh per-merchant
  `slug` and globally-unique `public_link_slug`, and forcing the new product's status to Draft (see
  FR-014a, US5; route `/products/<slug>/duplicate/`).
