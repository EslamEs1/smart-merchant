# Pages Contract: Smart Merchant OS — Static Frontend MVP

**Feature**: 001-static-frontend-mvp
**Date**: 2026-05-10
**Purpose**: For a static prototype, the only "interface contracts" are the
URL → file → required content commitments. This document is the single
authoritative list of every HTML file that ships, the URL it answers to,
the content shape it MUST satisfy, and the inbound links it MUST honor.

If a link in any sidebar, header, action dropdown, button, or in-page CTA
points to a file in this list, that link MUST resolve. Conversely, every
file in this list is a target of at least one such inbound link
(spec FR-045).

---

## Conventions

- **URL** is the path relative to the repo root (i.e., file:// or
  http://host/<URL>).
- **Required Components** lists the components/sections every page of this
  type MUST include — sourced from spec.md FRs and User Stories.
- **JS hooks** lists the `data-*` attributes / element IDs that
  `assets/js/main.js` looks for on this page (e.g., dropdowns, modals).
- **Inbound** lists the pages from which a navigational link to this page
  is required (a non-exhaustive but representative set).

---

## Public marketing pages (User Story 6)

### `index.html`

- **URL**: `/index.html` (or `/`)
- **Required Components**:
  - Marketing top nav (Logo, links to `features.html`, `pricing.html`, `login.html`, `register.html`)
  - Hero section: H1, subheading, primary CTA `ابدأ إدارة تجارتك بذكاء` → `register.html`, secondary CTA `شاهد لوحة التحكم` → `dashboard.html`
  - Visual dashboard preview mockup (inline SVG illustration or placeholder)
  - Affiliate growth section
  - Products / Orders / Customers section
  - Commissions / Payouts section
  - Features grid (~6 cards)
  - Pricing teaser (~3 plan cards) → `pricing.html`
  - Testimonials placeholder (≥3 cards)
  - FAQ section (≥5 Q&A)
  - Footer with brand glyph + bilingual wordmark + social links
- **JS hooks**: theme toggle button (`[data-theme-toggle]`), mobile nav toggle
- **Inbound**: external entry point; sidebar/header logo across the whole site

### `features.html`

- **URL**: `/features.html`
- **Required Components**: Top nav, intro hero, ten feature explainer sections (Dashboard, Products, Orders, Customers CRM, Affiliate System, Referral Links, QR Codes, Commissions, Landing Pages, Reports), CTA banner → `register.html`, footer
- **JS hooks**: theme toggle, mobile nav
- **Inbound**: `index.html` nav, `pricing.html` nav

### `pricing.html`

- **URL**: `/pricing.html`
- **Required Components**: Top nav, intro headline, three plan cards (Starter / Growth / Pro) — each with monthly price, products limit, affiliates limit, orders limit, feature list, CTA button → `register.html`; comparison table (optional but recommended); FAQ; footer
- **JS hooks**: theme toggle, mobile nav, plan-period toggle (monthly/yearly UI affordance — visual only)
- **Inbound**: `index.html` nav, `features.html` nav, `index.html` pricing teaser

### `login.html`

- **URL**: `/login.html`
- **Required Components**: Brand panel (left in LTR, right in RTL = visually start-side) with bilingual wordmark + glyph + tagline; form card with email/phone field, password field, remember-me toggle, primary CTA → `dashboard.html`, link to `register.html`; footer condensed
- **JS hooks**: theme toggle, password visibility toggle (allowed UI affordance under Principle VII)
- **Inbound**: `index.html` nav, `register.html` cross-link

### `register.html`

- **URL**: `/register.html`
- **Required Components**: Same shell as `login.html`; form fields: name, email/phone, password, confirm password, terms toggle, primary CTA → `dashboard.html`, link to `login.html`
- **JS hooks**: same as `login.html`
- **Inbound**: `index.html` hero CTA, `pricing.html` plan CTAs, `features.html` CTA, `login.html` cross-link

---

## Dashboard shell (applies to ALL dashboard pages below)

Every page in this section MUST render the **shared dashboard shell**
(spec FR-005, FR-006, FR-007, Constitution Principle VI):

| Region | Required content |
|---|---|
| Sidebar (fixed on desktop, drawer on mobile) | Brand glyph + wordmark, then links in this exact order: Dashboard, Products / Services, Orders, Customers, Affiliates, Payouts, Landing Pages, Analytics, Settings. Active link visually highlighted. |
| Top header | Mobile menu hamburger (mobile only), search input, theme toggle, notifications icon (links to `notifications.html`), profile menu (dropdown linking to `profile.html`, `settings.html`, logout → `login.html`) |
| Main content area | Page-specific content; breadcrumbs above H1 where useful |

JS hooks present on every dashboard shell:
- `[data-sidebar-toggle]` — mobile drawer open
- `[data-sidebar-overlay]` — drawer dim/close
- `[data-theme-toggle]` — light/dark switch
- `[data-profile-menu]` — header profile dropdown trigger

---

## Dashboard overview (User Story 2)

### `dashboard.html`

- **URL**: `/dashboard.html`
- **Required Components**: Welcome header with merchant name + greeting; date range selector UI; **6 stat cards** (إجمالي المبيعات, عدد الطلبات, عدد العملاء, عدد المسوقين, العمولات المستحقة, الطلبات الجديدة) each with value + trend indicator + Lucide icon; **2 chart placeholders** (sales overview line chart, orders by status donut) rendered as styled inline SVG; **recent orders table** (6 rows); **top affiliates card** (5 rows); **top products card** (5 rows); **pending affiliate requests card** (4 rows with quick approve/view actions); **4 quick action buttons** linking to `product-create.html`, `orders.html`, `affiliate-requests.html`, `landing-page-create.html`
- **JS hooks**: dashboard shell hooks; date-range selector toggle (`[data-date-range]`); modal triggers if any quick approve confirms
- **Inbound**: `login.html` and `register.html` primary CTAs; sidebar Dashboard link from every dashboard page

---

## Products module (User Story 3)

### `products.html`

- **URL**: `/products.html`
- **Required Components**: Page header with H1 + breadcrumb + "Add product" button → `product-create.html`; filter bar (search input, type filter, status filter); products data table (12 rows) with columns: image, name, type badge, price, discount, stock, status badge, sales count, actions dropdown; pagination control (visual only); hidden empty-state markup
- **JS hooks**: dashboard shell; `[data-actions-dropdown]` (one per row); `[data-confirm-modal="delete-product"]`; `[data-confirm-modal="disable-product"]`
- **Inbound**: sidebar; dashboard top-products card row links; dashboard "Add product" quick action

### `product-create.html`

- **URL**: `/product-create.html`
- **Required Components**: Breadcrumb + H1 (`إضافة منتج جديد`); form with all fields per FR-011 (name, type, description, price, discount price, stock, status, images placeholder, video URL, SEO title, SEO description, slug); Save and Cancel buttons in footer; right-side helper card (e.g., "نصائح لتحسين SEO")
- **JS hooks**: dashboard shell; image-upload affordance (UI only, no actual upload)
- **Inbound**: `products.html` "Add product" button; dashboard "Add product" quick action

### `product-edit.html`

- **URL**: `/product-edit.html`
- **Required Components**: Same as `product-create.html` but H1 = `تعديل المنتج`; pre-filled with sample data; Save and Cancel buttons; "Delete product" destructive button (opens confirmation modal)
- **JS hooks**: dashboard shell; `[data-confirm-modal="delete-product"]`
- **Inbound**: `products.html` row "Edit" action; `product-detail.html` "Edit" button

### `product-detail.html`

- **URL**: `/product-detail.html`
- **Required Components**: Breadcrumb; H1 = product name; status badge; image gallery placeholder; product summary card (price, discount, stock, status, public link with copy button); sales summary card; related orders table (5–8 rows); top-affiliates-who-sold-this-product list (3–5 rows); activity timeline (4–6 events)
- **JS hooks**: dashboard shell; `[data-copy="public-link"]`; `[data-actions-dropdown]` on related orders rows
- **Inbound**: `products.html` row "View details" action

---

## Orders module (User Story 4)

### `orders.html`

- **URL**: `/orders.html`
- **Required Components**: Page header; filter bar (search by order# or customer, order-status filter, payment-status filter, affiliate filter, date filter); orders data table (14 rows) per spec FR-014; pagination
- **JS hooks**: dashboard shell; `[data-actions-dropdown]` per row; confirmation modals for Cancel order, Confirm order, Mark shipped, Mark delivered, Print invoice
- **Inbound**: sidebar; dashboard "Create order" quick action; dashboard recent-orders card row links; `customer-detail.html` order history rows; `affiliate-detail.html` attributed orders rows; `product-detail.html` related orders rows

### `order-detail.html`

- **URL**: `/order-detail.html`
- **Required Components**: Breadcrumb; H1 = order number; three status badges; order summary card; customer info card; product info card (with thumbnail); affiliate attribution card (or "بدون مسوّق" state); commission info card; payment status panel; shipping status panel; chronological timeline (4–7 events); merchant notes textarea (read-only here); invoice preview card
- **JS hooks**: dashboard shell; print button (`[data-print-invoice]` triggers `window.print()`)
- **Inbound**: `orders.html` row "View details" action

### `order-edit.html`

- **URL**: `/order-edit.html`
- **Required Components**: Breadcrumb; H1 = `تعديل الطلب`; form with editable order status, payment status, shipping status, customer info, notes, affiliate attribution selector, commission amount; Save and Cancel buttons
- **JS hooks**: dashboard shell
- **Inbound**: `orders.html` row "Edit order" action; `order-detail.html` "Edit" button

---

## Affiliates module (User Story 1 — CORE differentiator)

### `affiliates.html`

- **URL**: `/affiliates.html`
- **Required Components**: Page header with prominent "نظام المسوقين" wording; commission rule banner (FR-026 string); filter bar (search, status filter, level filter); affiliates data table (10 rows) per FR-019 columns; pagination
- **JS hooks**: dashboard shell; `[data-actions-dropdown]` per row; `[data-copy="referral-link"]`; modals for Approve, Suspend, Pay commission, Change level
- **Inbound**: sidebar; dashboard top-affiliates card; `customer-detail.html` affiliate-attribution link; `order-detail.html` affiliate-attribution link

### `affiliate-detail.html`

- **URL**: `/affiliate-detail.html`
- **Required Components**: Breadcrumb; H1 = affiliate name with level + status badges; profile summary card; **referral link copy box** (large, prominent, with copy button); **QR code placeholder** (inline SVG); coupon code chip; stats grid (clicks, orders, sales, pending commission, paid commission, conversion rate); commission rule banner (FR-026); attributed orders table (6–10 rows); payout history table (4–6 rows); marketing assets section (3–5 cards); merchant notes; activity timeline (5–8 events)
- **JS hooks**: dashboard shell; `[data-copy="referral-link"]`; `[data-copy="coupon-code"]`; modals for Suspend, Pay commission, Change level, Approve
- **Inbound**: `affiliates.html` row "View profile" action; dashboard top-affiliates rows; `affiliate-requests.html` "View details" action

### `affiliate-requests.html`

- **URL**: `/affiliate-requests.html`
- **Required Components**: Breadcrumb; H1 = `طلبات الانضمام للمسوقين`; commission rule banner; cards or table of 6 pending applicants — each with name, contact, social links, experience snippet, requested date; per-row actions: Approve (modal), Reject (modal), View details (→ `affiliate-detail.html`)
- **JS hooks**: dashboard shell; modals for Approve, Reject
- **Inbound**: sidebar (Affiliates section, secondary nav); dashboard pending-affiliate-requests card; dashboard "Review affiliates" quick action

### `affiliate-payouts.html`

- **URL**: `/affiliate-payouts.html`
- **Required Components**: Breadcrumb; H1 = `طلبات السحب والعمولات`; commission rule banner; tabs: Pending / Paid / Rejected (one active at a time, others rendered hidden but in DOM); per-tab table per FR-025; per-row actions per status (Approve/Reject for Pending; View for Paid/Rejected)
- **JS hooks**: dashboard shell; `[data-tabs="payouts"]`; modals for Approve, Reject, Mark Paid
- **Inbound**: sidebar Payouts link; `affiliate-detail.html` "Pay commission" action

---

## Customers module (User Story 5)

### `customers.html`

- **URL**: `/customers.html`
- **Required Components**: Page header; filter bar (search, source filter with all 7 values, tags filter); customers data table (15 rows) per FR-027; pagination
- **JS hooks**: dashboard shell; `[data-actions-dropdown]` per row; modals for Delete customer (or status changes if any)
- **Inbound**: sidebar; `affiliate-detail.html` and `order-detail.html` customer references

### `customer-detail.html`

- **URL**: `/customer-detail.html`
- **Required Components**: Breadcrumb; H1 = customer name; profile card (phone, email, address); source card; affiliate attribution card (when applicable); order history table (4–8 rows linking to `order-detail.html`); total spent stat; tags chips; merchant notes; follow-up status panel; activity timeline (4–6 events)
- **JS hooks**: dashboard shell; `[data-actions-dropdown]` on order history rows
- **Inbound**: `customers.html` row "View details" action

### `customer-edit.html`

- **URL**: `/customer-edit.html`
- **Required Components**: Breadcrumb; H1 = `تعديل بيانات العميل`; form with name, phone, email, address, source select, tags multi-select, notes textarea, follow-up date; Save and Cancel buttons
- **JS hooks**: dashboard shell
- **Inbound**: `customers.html` row "Edit" action; `customer-detail.html` "Edit" button

---

## Landing Pages module (User Story 7)

### `landing-pages.html`

- **URL**: `/landing-pages.html`
- **Required Components**: Page header with "Add landing page" button → `landing-page-create.html`; landing pages data table (8 rows) per FR-031; pagination
- **JS hooks**: dashboard shell; `[data-actions-dropdown]` per row; modals for Disable, Delete
- **Inbound**: sidebar; dashboard "Create landing page" quick action

### `landing-page-create.html`

- **URL**: `/landing-page-create.html`
- **Required Components**: Breadcrumb; H1 = `إنشاء صفحة هبوط`; form per FR-032 (title, product selector, template selection cards, hero headline, subheadline, CTA text, offer price, benefits list, testimonials placeholder, FAQ placeholder, SEO title, SEO description); Save and Preview buttons (Preview → `landing-page-preview.html`)
- **JS hooks**: dashboard shell; benefit list add/remove (light DOM manipulation, allowed under "tab switching" / form interactions)
- **Inbound**: `landing-pages.html` "Add landing page"; dashboard quick action

### `landing-page-preview.html`

- **URL**: `/landing-page-preview.html`
- **Required Components**: NO dashboard shell (this is a public-facing preview); marketing-style top nav (minimal); hero with headline + subheadline + CTA; product image placeholder; benefits list (3–5 bullets); offer card with price; testimonials section; FAQ section; footer
- **JS hooks**: theme toggle (optional); CTA opens a placeholder confirmation
- **Inbound**: `landing-pages.html` row "Preview" action; `landing-page-create.html` "Preview" button

---

## Settings, Profile, Notifications, Analytics (User Story 8 + FR-045 honoring)

### `settings.html`

- **URL**: `/settings.html`
- **Required Components**: Breadcrumb; H1 = `الإعدادات`; left-side tab navigation (or top tabs on mobile) with: Business info, Branding, Payment settings, Affiliate commission settings, Notification settings, Security; right-side panel rendering the active tab's form (only one tab pre-rendered "active"; others rendered as hidden DOM siblings to keep tab switching JS-only)
- **JS hooks**: dashboard shell; `[data-tabs="settings"]`
- **Inbound**: sidebar; header profile menu

### `profile.html`

- **URL**: `/profile.html`
- **Required Components**: Breadcrumb; H1 = `الملف الشخصي`; avatar placeholder upload affordance; name, email, phone fields; password change placeholder section; Save and Cancel buttons
- **JS hooks**: dashboard shell
- **Inbound**: header profile menu

### `notifications.html`

- **URL**: `/notifications.html`
- **Required Components**: Breadcrumb; H1 = `الإشعارات`; filter chips (All / Unread / by category); inbox list (12 entries) covering all 5 categories; per-entry click area links to relevant detail page; "Mark all as read" affordance (visual only)
- **JS hooks**: dashboard shell; `[data-filter-chips]` (light tab-like behavior, allowed under tabs allow-list)
- **Inbound**: header notifications icon

### `analytics.html` (placeholder, honors FR-045)

- **URL**: `/analytics.html`
- **Required Components**: Dashboard shell with sidebar Analytics link active; H1 = `التحليلات`; styled "coming soon" card explaining the feature; placeholder chart illustrations to suggest future content; CTA pointing to `dashboard.html` for current analytics-style data
- **JS hooks**: dashboard shell only
- **Inbound**: sidebar Analytics link

---

## Inbound link audit table (top-level invariants for FR-045)

| From | To | Trigger |
|---|---|---|
| sidebar (every dashboard page) | `dashboard.html` | Dashboard nav item |
| sidebar | `products.html` | Products nav item |
| sidebar | `orders.html` | Orders nav item |
| sidebar | `customers.html` | Customers nav item |
| sidebar | `affiliates.html` | Affiliates nav item |
| sidebar | `affiliate-payouts.html` | Payouts nav item |
| sidebar | `landing-pages.html` | Landing Pages nav item |
| sidebar | `analytics.html` | Analytics nav item |
| sidebar | `settings.html` | Settings nav item |
| header profile menu | `profile.html`, `settings.html`, `login.html` | Profile dropdown |
| header notifications icon | `notifications.html` | Bell click |
| `dashboard.html` quick actions | `product-create.html`, `orders.html`, `affiliate-requests.html`, `landing-page-create.html` | 4 quick-action buttons |
| `index.html` hero CTAs | `register.html`, `dashboard.html` | Primary + secondary CTA |
| `index.html`, `features.html`, `pricing.html` nav | `index.html`, `features.html`, `pricing.html`, `login.html`, `register.html` | Marketing nav |
| `login.html` ↔ `register.html` | Each other | Cross-link footer of form card |
| `login.html`, `register.html` primary CTA | `dashboard.html` | Form submit (visual only) |
| Each list page row Action menu | Corresponding detail / edit page | "View details" / "Edit" |

A simple `grep -rE 'href="[^"]+\.html"' .` against the repo at acceptance
time, cross-referenced with the file list in this contract, validates
SC-002 (zero broken links).

---

**Status**: Pages contract is complete. Every URL the prototype offers is
documented with required content shape, JS hooks, and inbound link sources.
