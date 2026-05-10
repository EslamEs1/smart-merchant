---

description: "Task list for Smart Merchant OS — Static Frontend MVP"
---

# Tasks: Smart Merchant OS — Static Frontend MVP

**Input**: Design documents from `/specs/001-static-frontend-mvp/`
**Prerequisites**: plan.md (✅), spec.md (✅), research.md (✅), data-model.md (✅), contracts/pages.md (✅), quickstart.md (✅)

**Tests**: Not requested. The Constitution forbids build tooling and the prototype is verified by manual visual review against `quickstart.md` checks. No automated test tasks are generated.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1 = Affiliate System, US2 = Dashboard, US3 = Products, US4 = Orders, US5 = Customers, US6 = Public Marketing, US7 = Landing Pages, US8 = Settings/Profile/Notifications)
- File paths are relative to the repo root

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project root structure and authoring crib. No HTML pages yet.

- [x] T001 Create repo-root folder layout per `plan.md` Project Structure: `assets/css/`, `assets/js/`, `assets/img/`, `assets/img/placeholders/`, `partials/` (use `mkdir -p`)
- [x] T002 [P] Create `README.md` at repo root with project overview, three run methods (double-click / VS Code Live Server / `python3 -m http.server`), Constitution summary (no frameworks, no build), and links to `specs/001-static-frontend-mvp/{spec,plan,research,data-model,quickstart}.md` plus `contracts/pages.md`
- [x] T003 [P] Create `SAMPLE-DATA.md` at repo root summarizing per `research.md` §7: currency distribution targets (~50% SAR, ~25% EGP, ~20% AED, ~5% other), name distribution (~80% Arabic / ~20% Latin), and a list of 10 canonical sample entities (3 products, 3 affiliates, 2 customers, 2 orders) with names, IDs, and currencies that all later pages MUST reference for cross-page consistency per `data-model.md` cross-entity reference rules

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Shared shell partials, CSS, JS, and imagery that every dashboard page reuses. No story-level work can begin until this phase completes.

**⚠️ CRITICAL**: Phase 3+ pages depend on `partials/_head.html`, `partials/_sidebar.html`, `partials/_header.html`, `assets/css/app.css`, and `assets/js/main.js` existing.

- [x] T004 [P] Author **two** brand artifacts to satisfy FR-045a/b's no-external-image-dependency clause: (a) `assets/img/logo.svg` — bilingual "Smart Merchant OS / سمارت مرتشانت" wordmark + abstract geometric glyph in indigo→violet→blue gradient per `research.md` §4 (used as a reference / favicon source / fallback only); (b) `partials/_logo-svg.html` — the SAME glyph as a copy-paste-ready inline `<svg>…</svg>` block that downstream tasks (T008 sidebar, T010 footer, T031/T032 brand panels, T028 marketing nav) MUST inline directly into their HTML rather than reference via `<img src=…>`. The inline snippet MUST size cleanly via Tailwind utilities (e.g., `class="h-8 w-8"`) and inherit theme color via `currentColor` where applicable
- [x] T005 [P] Author `assets/img/favicon.svg` — glyph-only version of the T004 logo, 64×64 viewBox
- [x] T006 [P] Author the placeholder image set under `assets/img/placeholders/`: `product.svg`, `avatar.svg` (generic person avatar — used for both customers and the merchant's own profile), `affiliate-avatar.svg`, `dashboard-preview.svg`, `qr-code.svg`, `hero-art.svg`, `chart-line.svg`, `chart-donut.svg`, `template-hero-classic.svg`, `template-bold-offer.svg`, `template-story-driven.svg`, `template-minimal.svg` — all premium-styled inline SVG (gradients/grids/shapes), never gray boxes
- [x] T007 [P] Author **two** copy-paste templates that downstream per-page tasks reuse: (a) `partials/_page-skeleton.html` — a complete page skeleton beginning with `<!DOCTYPE html><html dir="rtl" lang="ar" class="font-sans bg-surface-base text-text-primary">…</html>` (satisfies FR-037), with `<head>` and `<body>` slot markers and a deferred `<script src="assets/js/main.js" defer>` bootstrap before `</body>`; (b) `partials/_head.html` — the `<head>` block content that every page inlines into the skeleton, containing: meta charset/viewport, `<title>` placeholder, Google Fonts CDN link for Cairo (400/500/600/700/800) + Tajawal (400/500/700), Tailwind Play CDN script + immediately-following inline `tailwind.config = { darkMode: 'class', theme: { extend: { colors: {brand-primary, brand-accent, brand-info, surface-*, text-*}, fontFamily: {sans: ['Cairo','Tajawal','system-ui','sans-serif']}, backgroundImage: {'gradient-brand': 'linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #3b82f6 100%)'} } } }` per `research.md` §4, Lucide CDN script (`<script src="https://unpkg.com/lucide@latest">`), `<link rel="stylesheet" href="assets/css/app.css">`, pre-paint inline theme `<script>` (≤5-line localStorage `smos:theme` check that adds `dark` class to `<html>` before paint per `research.md` §5). Per-page tasks (T013–T038) MUST copy-paste both partials together — the page-skeleton wrapper FIRST so the `<html dir="rtl" lang="ar">` element is present, then the head content inside it
- [x] T008 [P] Author `partials/_sidebar.html` — fixed-desktop / mobile-drawer sidebar with the **inline logo `<svg>` block copied from `partials/_logo-svg.html`** (NOT `<img src="logo.svg">`, per FR-045b) + bilingual wordmark text at top, then 9 nav items in exact `spec.md` FR-006 order (Dashboard, Products / Services, Orders, Customers, Affiliates, Payouts, Landing Pages, Analytics, Settings), each with the Lucide icon mapping from `research.md` §6 (`layout-dashboard`, `package`, `shopping-cart`, `users`, `handshake`, `wallet`, `layout-template`, `bar-chart-3`, `settings`), active-state via `aria-current="page"` and a brand-gradient accent strip
- [x] T009 [P] Author `partials/_header.html` — top header with `[data-sidebar-toggle]` mobile-menu hamburger (Lucide `menu`), search input (Lucide `search`), `[data-theme-toggle]` button (swaps Lucide `sun`/`moon`), notifications icon (Lucide `bell`) linking to `notifications.html`, `[data-profile-menu]` profile button (Lucide `user-circle`) opening a dropdown with links to `profile.html`, `settings.html`, and `login.html` (logout)
- [x] T010 [P] Author `partials/_footer.html` — marketing-page footer with the **inline logo `<svg>` block copied from `partials/_logo-svg.html`** + bilingual wordmark text (per FR-045b), 3-column link list (Product / Resources / Company), social icons row, copyright line; used on `index.html`, `features.html`, `pricing.html` only
- [x] T011 Create `assets/css/app.css` containing: `@layer components` definitions for status-badge classes (`.badge-pending`, `.badge-confirmed`, `.badge-processing`, `.badge-shipped`, `.badge-delivered`, `.badge-cancelled`, `.badge-paid`, `.badge-unpaid`, `.badge-partially-paid`, `.badge-refunded`, `.badge-not-shipped`, `.badge-preparing`, `.badge-returned`, `.badge-active`, `.badge-suspended`, `.badge-rejected`, `.badge-bronze`, `.badge-silver`, `.badge-gold`, `.badge-platinum`) using the palette from `research.md` §4; `.focus-ring` utility (`@apply focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-brand-primary focus-visible:ring-offset-2 focus-visible:ring-offset-surface-base`); `.gradient-brand` utility; **`.table-responsive` wrapper class implementing FR-040** — at viewports ≥640 px applies `overflow-x-auto` plus a sticky-first-column rule (`tbody td:first-child { position: sticky; inset-inline-start: 0; background: inherit; }` and matching `thead th:first-child`), and at viewports `<640 px` collapses the table into a stacked card list using `display: block` on rows + pseudo-element `data-label` headers (or, simpler alternative also acceptable: keep `overflow-x-auto` at all sizes — pick one approach and use it consistently across every list page); `.copied-toast` transient animation; modal/drawer enter/exit transitions; print styles for `[data-print-area="invoice"]`; small RTL-specific adjustments for Lucide directional chevrons
- [x] T012 Create `assets/js/main.js` implementing exactly the FR-042 allow-list: (1) `initTheme()` and `setTheme(mode)` reading/writing `localStorage.getItem('smos:theme')` and toggling `html.classList`; (2) sidebar drawer open/close with focus-trap, overlay-click dismiss, ESC dismiss; (3) `[data-actions-dropdown]` click toggling `aria-expanded` with click-outside-closes and ESC-closes; (4) modal open/close (`[data-modal-trigger]`, `[data-modal]`, `[data-modal-close]`) with focus-trap, ESC dismiss, overlay-click dismiss, return focus to trigger on close; (5) tab switcher for `[data-tabs="<group>"]` swapping `.hidden` between panels; (6) `[data-copy="<key>"]` writing to clipboard via `navigator.clipboard.writeText()` then showing a transient `تم النسخ` toast for ~1.5 s; (7) profile menu dropdown; (8) 30-line custom focus-trap helper; (9) `lucide.createIcons()` invoked on `DOMContentLoaded` and exposed as `window.renderIcons()` for use after dynamic DOM insertions; (10) date-range selector toggle (visual only — opens a popover that closes on outside click). NO other behaviors. NO npm modules. NO ES module syntax — single classic `<script>` file

**Checkpoint**: Foundation ready — all dashboard pages can now be authored in parallel.

---

## Phase 3: User Story 1 - Affiliate-Centric Merchant Demo (Priority: P1) 🎯 MVP

**Goal**: Deliver the affiliate workflow end-to-end so a reviewer can see the project's core differentiator on its own.

**Independent Test**: Open `affiliates.html`, `affiliate-detail.html`, `affiliate-requests.html`, `affiliate-payouts.html` directly. Verify all four render complete with realistic data, the referral-link copy box copies to clipboard, action dropdowns expose 7 actions, approve/suspend/pay confirmation modals work, and the commission rule banner is visible on every page.

### Implementation for User Story 1

- [x] T013 [P] [US1] Author `affiliates.html` using `partials/_page-skeleton.html` + `_head.html` + `_sidebar.html` + `_header.html` (copy-pasted, page-skeleton first to satisfy FR-037 `<html dir="rtl" lang="ar">`), page header `نظام المسوقين`, commission rule banner with FR-026 string, filter bar (search input, status filter, level filter), affiliates table **wrapped in `<div class="table-responsive">`** (per T011 FR-040 pattern) with **10 hardcoded rows** per `research.md` §7 distribution (level mix 2 Bronze / 3 Silver / 3 Gold / 2 Platinum; status mix 6 Active / 2 Pending / 1 Suspended / 1 Rejected; ~50% SAR / 25% EGP / 20% AED / 5–10% other; ~80% Arabic-script names) with columns per `spec.md` FR-019, row-level `[data-actions-dropdown]` exposing the 7 actions per FR-021 (View profile, Approve, Suspend, Change level, View orders, Pay commission, Copy referral link), confirmation `[data-modal]` markup for Approve/Suspend/Change-level/Pay-commission, pagination UI, hidden empty-state markup, single deferred `<script src="assets/js/main.js" defer>` import
- [x] T014 [P] [US1] Author `affiliate-detail.html` using `partials/_page-skeleton.html` + shell partials, breadcrumb, H1 with affiliate name + level badge + status badge, profile summary card, prominent referral link copy box `[data-copy="referral-link"]` displaying `https://smartmerchant.os/r/<code>`, QR code placeholder (inline `<img src="assets/img/placeholders/qr-code.svg" alt="QR للرابط التسويقي">`), coupon code chip `[data-copy="coupon-code"]`, 6-stat grid (clicks/orders/sales/pending/paid/conversion) per FR-022 with Lucide icons, commission rule banner, attributed orders table **wrapped in `<div class="table-responsive">`** with **8 rows** referencing order numbers that will exist in `orders.html`, payout history table **wrapped in `<div class="table-responsive">`** with **5 rows**, marketing assets section with **4 cards** (Banner / Story / Reel Caption / Email Template) — each card image MUST carry an Arabic `alt` attribute per FR-049, notes textarea (read-only display), activity timeline with **6 events** showing canonical lifecycle from `data-model.md`
- [x] T015 [P] [US1] Author `affiliate-requests.html` using shell partials, breadcrumb, H1 `طلبات الانضمام للمسوقين`, commission rule banner, **6 pending applicant cards** (or table rows) — each with applicant name, contact (email or phone), 1–3 social links, 1–2 paragraph experience snippet, requested date, per-row action buttons Approve / Reject (each opens a `[data-modal]` for confirmation) and View details (linking to `affiliate-detail.html`)
- [x] T016 [P] [US1] Author `affiliate-payouts.html` using shell partials, breadcrumb, H1 `طلبات السحب والعمولات`, commission rule banner, `[data-tabs="payouts"]` with three tabs — **Pending: 5 rows, Paid: 6 rows, Rejected: 3 rows** — each tab's table per FR-025 columns (affiliate, requested amount + currency, available balance + currency, payment method ∈ {Bank Transfer, STC Pay, Vodafone Cash, Instapay, PayPal, Wise}, status, request date), per-tab status-appropriate per-row actions with confirmation modals (Pending → Approve/Reject; Paid → View; Rejected → View)

**Checkpoint**: User Story 1 (the core differentiator) is functional and demoable on its own per `quickstart.md` Section D.

---

## Phase 4: User Story 2 - Merchant Dashboard Overview (Priority: P1)

**Goal**: Deliver the dashboard home page so reviewers see the product's full surface area at a glance.

**Independent Test**: Open `dashboard.html` directly. Verify all 6 stat cards display values, both chart placeholders are visually rich (not empty boxes), recent orders table shows ≥6 realistic rows, top affiliates / top products / pending requests cards each populated, and all 4 quick actions navigate correctly.

### Implementation for User Story 2

- [x] T017 [US2] Author `dashboard.html` using `partials/_page-skeleton.html` + shell partials, welcome header (`أهلاً بك، <merchant business name from SAMPLE-DATA.md>`), date-range selector UI `[data-date-range]` (button + popover, visual only), **6 stat cards** with FR-008 Arabic labels (إجمالي المبيعات / عدد الطلبات / عدد العملاء / عدد المسوقين / العمولات المستحقة / الطلبات الجديدة), each card with placeholder value + trend indicator (Lucide `trending-up`/`trending-down` + delta percent) + Lucide stat icon per `research.md` §6, gradient-brand background accent on the "العمولات المستحقة" card to spotlight the affiliate differentiator; **2 chart placeholders** — `<img src="assets/img/placeholders/chart-line.svg" alt="رسم بياني لمبيعات آخر ٣٠ يوم">` for the sales overview line and `<img src="assets/img/placeholders/chart-donut.svg" alt="توزيع الطلبات حسب الحالة">` for the orders-by-status donut (Arabic alt attributes mandated by FR-049); **recent orders table wrapped in `<div class="table-responsive">`** with 6 rows referencing order numbers that exist in `orders.html`; **top affiliates card** with 5 rows referencing names in `affiliates.html`; **top products card** with 5 rows referencing names in `products.html`; **pending affiliate requests card** with 4 rows referencing applicants in `affiliate-requests.html`, each with quick `View` link; **4 quick-action buttons** linking to `product-create.html`, `orders.html`, `affiliate-requests.html`, `landing-page-create.html`

**Checkpoint**: User Story 2 is functional. With US1 + US2 complete, the affiliate-centric MVP is demonstrable.

---

## Phase 5: User Story 3 - Products & Services Management (Priority: P1)

**Goal**: Deliver the product catalogue with create/edit/detail flows so the dashboard's "Products" and the affiliate's "products sold" references resolve.

**Independent Test**: Open `products.html`, `product-create.html`, `product-edit.html`, `product-detail.html`. Verify list shows 12 rows covering all 5 product types, action dropdown exposes 6 actions, create/edit forms include all required fields, detail page shows summary card + image gallery + sales summary + related orders + top affiliates + timeline.

### Implementation for User Story 3

- [x] T018 [P] [US3] Author `products.html` using `partials/_page-skeleton.html` + shell partials, page header with H1 `المنتجات والخدمات` and "Add product" button → `product-create.html`, filter bar (search input, type filter exposing all 5 product types from FR-013 — منتج فعلي / خدمة / كورس / ديجيتال برودكت / اشتراك, status filter), products table **wrapped in `<div class="table-responsive">`** with **12 hardcoded rows** (≥1 per product type, status mix ~70% active / 20% draft / 10% disabled, ~30% with discount, currency distribution per `research.md` §7), columns per FR-009 (image / name / type badge / price / discount / stock / status badge / sales count / actions) — each row's product `<img>` MUST carry an Arabic `alt` of the product name per FR-049, row-level `[data-actions-dropdown]` with 6 actions per FR-010 (View details, Edit, Copy public link, Duplicate, Disable, Delete), confirmation `[data-modal]` markup for Disable and Delete, pagination UI, hidden empty-state markup
- [x] T019 [P] [US3] Author `product-create.html` using shell partials, breadcrumb, H1 `إضافة منتج جديد`, form per FR-011 with: name input, type select with 5 values, description textarea, price input + currency select (SAR/EGP/AED/KWD/USD), discount price input + currency select, stock number input, status select (active/draft/disabled), image upload affordance (UI-only drag-drop zone with preview thumbnails using `assets/img/placeholders/product.svg`), video URL input, SEO title input, SEO description textarea, slug input with `/p/` prefix preview, Save and Cancel buttons in sticky footer; right-side helper card titled `نصائح لتحسين SEO`
- [x] T020 [P] [US3] Author `product-edit.html` using shell partials, breadcrumb, H1 `تعديل المنتج: <name>`, same form structure as T019 pre-filled with one canonical product's sample data from `SAMPLE-DATA.md`, Save and Cancel buttons, additional "حذف المنتج" destructive button in form footer opening `[data-modal="delete-product"]`
- [x] T021 [P] [US3] Author `product-detail.html` using `partials/_page-skeleton.html` + shell partials, breadcrumb, H1 = product name, status badge, image gallery placeholder (4 thumbnails using `assets/img/placeholders/product.svg`, each `<img>` with an Arabic `alt` per FR-049), product summary card with price + discount + stock + status + public link `[data-copy="public-link"]`, sales summary card (units sold / revenue / pending units), related orders table **wrapped in `<div class="table-responsive">`** with **6 rows** linking to `order-detail.html`, top-affiliates-who-sold-this-product list with **4 rows** linking to `affiliate-detail.html`, activity timeline with **5 events**

**Checkpoint**: User Story 3 is functional. P1 trio (US1 + US2 + US3) is now complete — this is the demo-ready MVP slice.

---

## Phase 6: User Story 4 - Orders Management with Attribution (Priority: P2)

**Goal**: Deliver the orders module so the affiliate-attribution chain (customer → product → affiliate → commission) is end-to-end traceable.

**Independent Test**: Open `orders.html`, `order-detail.html`, `order-edit.html`. Verify orders list has both affiliate-attributed and unattributed rows, all three status families render correctly, filter UI is present, detail page shows attribution chain + invoice preview.

### Implementation for User Story 4

- [x] T022 [P] [US4] Author `orders.html` using `partials/_page-skeleton.html` + shell partials, page header with H1 `الطلبات`, filter bar (search by order number/customer, order-status filter, payment-status filter, affiliate filter, date filter UI), orders table **wrapped in `<div class="table-responsive">`** with **14 hardcoded rows** per `research.md` §7 distribution (8 with affiliate / 6 without; coverage of all 6 order statuses / all 4 payment statuses / all 5 shipping statuses; currency mix 7 SAR / 4 EGP / 2 AED / 1 KWD-or-USD; affiliate names matching `affiliates.html`; product names matching `products.html`; customer names matching `customers.html`), columns per FR-014 (order# / customer / product / affiliate or `—` / total + currency / commission + currency / order status badge / payment status badge / shipping status badge / date / actions), row-level `[data-actions-dropdown]` with 7 actions per FR-015 (View details, Edit order, Confirm order, Mark as shipped, Mark as delivered, Cancel order, Print invoice), confirmation `[data-modal]` markup for Confirm/Mark-shipped/Mark-delivered/Cancel, pagination UI
- [x] T023 [P] [US4] Author `order-detail.html` using shell partials, breadcrumb, H1 = order number `#SMO-100423`, three status badges (order/payment/shipping), order summary card, customer info card linking to `customer-detail.html`, product info card with thumbnail linking to `product-detail.html`, affiliate attribution card linking to `affiliate-detail.html` (or rendering `بدون مسوّق` panel when null), commission info card, payment status panel, shipping status panel, chronological timeline with **6 events** showing the canonical Order lifecycle from `data-model.md` (Created → Confirmed → Processing → Shipped → Delivered or Cancelled), merchant notes display block, invoice preview card with line items (1–3) + subtotal + tax + total inside `[data-print-area="invoice"]` and a print button calling `window.print()`
- [x] T024 [P] [US4] Author `order-edit.html` using shell partials, breadcrumb, H1 `تعديل الطلب #SMO-100423`, form per FR-018 with: order status select (6 values), payment status select (4 values), shipping status select (5 values), customer info edit panel (name / phone / email / address), notes textarea, affiliate attribution selector (dropdown listing affiliate names with a "بدون مسوّق" option), commission amount input + currency select, Save and Cancel buttons

**Checkpoint**: User Story 4 functional. The affiliate attribution chain is now visually complete from order → affiliate → commission → payout.

---

## Phase 7: User Story 5 - Customers CRM (Priority: P2)

**Goal**: Deliver the customer CRM so customer-source attribution (especially affiliate-sourced customers) closes the loop on the affiliate story.

**Independent Test**: Open `customers.html`, `customer-detail.html`, `customer-edit.html`. Verify list has 15 rows across all 7 sources, source filter exposes all 7 values, detail page shows full order history + timeline, edit form has every required field.

### Implementation for User Story 5

- [x] T025 [P] [US5] Author `customers.html` using `partials/_page-skeleton.html` + shell partials, page header with H1 `العملاء`, filter bar (search input, source filter exposing all 7 values per FR-028 — Direct/Affiliate/WhatsApp/Facebook/Instagram/TikTok/Manual, tags filter), customers table **wrapped in `<div class="table-responsive">`** with **15 hardcoded rows** (≥1 per source, ~80% Arabic-script names, currency distribution per `research.md` §7, ~6 of the rows have source=Affiliate referencing affiliates that exist in `affiliates.html`), columns per FR-027 (name / phone or email / source badge / affiliate or `—` / orders count / total spent + currency / last order date / tags chips / actions), row-level `[data-actions-dropdown]` (View details / Edit / Add note / Set follow-up / Delete), confirmation `[data-modal]` markup for Delete, pagination UI
- [x] T026 [P] [US5] Author `customer-detail.html` using `partials/_page-skeleton.html` + shell partials, breadcrumb, H1 = customer name, customer avatar (`assets/img/placeholders/avatar.svg`, with Arabic `alt` per FR-049), profile card with phone/email/address, source card showing source badge + "كيف وجدنا" explainer, affiliate attribution card linking to `affiliate-detail.html` (rendered only when source=Affiliate), order history table **wrapped in `<div class="table-responsive">`** with **6 rows** linking to `order-detail.html`, total spent stat + lifetime value, tags chips section, merchant notes display block, follow-up status panel (Open/In Progress/Done) with follow-up date, activity timeline with **5 events**
- [x] T027 [P] [US5] Author `customer-edit.html` using shell partials, breadcrumb, H1 `تعديل بيانات العميل: <name>`, form per FR-030 with: name input, phone input, email input, address textarea, source select (7 values), tags multi-select (chip-style with 6+ pre-defined tag options + free-add), notes textarea, follow-up date input, Save and Cancel buttons

**Checkpoint**: User Story 5 functional. All P2 stories (US4 + US5) are complete. The dashboard ↔ products ↔ orders ↔ affiliates ↔ customers references all resolve.

---

## Phase 8: User Story 6 - Public Marketing Website (Priority: P3)

**Goal**: Deliver the public-facing marketing pages so the prototype includes a credible client-onboarding experience.

**Independent Test**: Open `index.html`, `features.html`, `pricing.html`, `login.html`, `register.html`. Verify home page has all required sections in order, features page explains all 10 features, pricing shows exactly 3 plans, login/register render with brand-panel split layout.

### Implementation for User Story 6

- [x] T028 [P] [US6] Author `index.html` (NOT using dashboard shell — uses marketing nav) with `partials/_page-skeleton.html` + `partials/_head.html` + `partials/_footer.html`. Marketing top nav with the **inline logo `<svg>` block from `partials/_logo-svg.html`** (per FR-045b) + bilingual wordmark text + links to `features.html`, `pricing.html`, `login.html`, `register.html` and CTA button → `register.html`; hero section with H1, subheading, primary CTA "ابدأ إدارة تجارتك بذكاء" → `register.html`, secondary CTA "شاهد لوحة التحكم" → `dashboard.html`; visual dashboard preview mockup using `<img src="assets/img/placeholders/dashboard-preview.svg" alt="لقطة من لوحة التحكم">` (Arabic `alt` per FR-049); affiliate growth section (3-column explainer with Lucide icons `handshake`/`link`/`coins`); products/orders/customers section; commissions/payouts section; features grid (6 cards each with Lucide icon + heading + 1-paragraph blurb); pricing teaser with 3 plan cards linking to `pricing.html`; testimonials placeholder with ≥3 cards (each: quote / author name / role / star rating); FAQ section with ≥5 Q&A using `<details>` accordions; footer
- [x] T029 [P] [US6] Author `features.html` (NOT dashboard shell) using marketing nav + footer, intro hero, **10 feature explainer sections** per FR-002 (Dashboard / Products / Orders / Customers CRM / Affiliate System / Referral Links / QR Codes / Commissions / Landing Pages / Reports), each section alternating left-image/right-text layout, each with Lucide icon + 2-paragraph Arabic description + visual placeholder; CTA banner near the end → `register.html`; footer
- [x] T030 [P] [US6] Author `pricing.html` (NOT dashboard shell) using marketing nav + footer, intro headline, **3 plan cards** (Starter / Growth / Pro) per FR-003 with monthly price placeholder, products limit, affiliates limit, orders limit, feature list (5–8 bullets each), CTA button → `register.html` (Growth plan visually marked as "موصى به" with brand-gradient border); comparison table beneath cards (rows: products / affiliates / orders / landing pages / reports / support level / commission rate); monthly/yearly billing toggle UI (visual only); FAQ section with 4–5 Q&A; footer
- [x] T031 [P] [US6] Author `login.html` using `partials/_page-skeleton.html` + `partials/_head.html` (no dashboard shell, no marketing nav) — split-panel layout: brand panel on the start side containing the **inline logo `<svg>` block from `partials/_logo-svg.html`** (per FR-045b) + bilingual wordmark text + tagline + small dashboard preview thumbnail (`<img alt="لقطة من لوحة التحكم">` per FR-049) using gradient-brand background, form card on the end side with email-or-phone input, password input + visibility toggle button, remember-me toggle, primary CTA button "تسجيل الدخول" → `dashboard.html`, link "لا تملك حساب؟ سجل الآن" → `register.html`, condensed footer (copyright line)
- [x] T032 [P] [US6] Author `register.html` using same split-panel shell as T031 with brand panel containing the **inline logo `<svg>` block from `partials/_logo-svg.html`** (per FR-045b) and form card containing: name input, email-or-phone input, password input, confirm password input, terms-and-conditions checkbox, primary CTA "إنشاء الحساب" → `dashboard.html`, link "لديك حساب؟ سجل دخول" → `login.html`, condensed footer

**Checkpoint**: User Story 6 functional. The marketing → auth → dashboard onboarding flow is now end-to-end navigable.

---

## Phase 9: User Story 7 - Simple Landing Pages Module (Priority: P3)

**Goal**: Deliver the form-based landing-page builder so the prototype demonstrates the depth advertised on the marketing site.

**Independent Test**: Open `landing-pages.html`, `landing-page-create.html`, `landing-page-preview.html`. Verify list shows 8 rows with conversion metrics, create page has form-based editor with template selection, preview page renders complete public-facing landing page.

### Implementation for User Story 7

- [x] T033 [P] [US7] Author `landing-pages.html` using `partials/_page-skeleton.html` + shell partials, page header with H1 `صفحات الهبوط` and "Add landing page" button → `landing-page-create.html`, landing pages table **wrapped in `<div class="table-responsive">`** with **8 hardcoded rows** per FR-031 columns (title / linked product matching `products.html` names / status badge / visits / conversion rate as `X.X%` / orders / revenue + currency matching the linked product's currency / last updated date / actions), row-level `[data-actions-dropdown]` with 6 actions per FR-031 (Preview, Edit, Copy link, Duplicate, Disable, Delete), confirmation `[data-modal]` markup for Disable and Delete, pagination UI
- [x] T034 [P] [US7] Author `landing-page-create.html` using shell partials, breadcrumb, H1 `إنشاء صفحة هبوط`, form per FR-032 with: title input, product selector (dropdown listing 8–10 product names from `SAMPLE-DATA.md`), template selection — 4 radio-card options (Hero Classic / Bold Offer / Story-Driven / Minimal) each previewing `assets/img/placeholders/template-*.svg`, hero headline input, subheadline input, CTA text input, offer price input + currency select, benefits list editor (start with 3 rows; add/remove buttons), testimonials placeholder section (3 placeholder cards labeled `Testimonial 1/2/3`), FAQ placeholder section (3 placeholder Q&A), SEO title input, SEO description textarea, Save button + Preview button → `landing-page-preview.html`
- [x] T035 [P] [US7] Author `landing-page-preview.html` (NO dashboard shell, NO marketing top nav — public-facing preview) using only `partials/_head.html`, minimal sticky top bar with brand glyph + wordmark + a "العودة للوحة التحكم" link → `dashboard.html`, hero section with headline + subheadline + primary CTA "اطلب الآن", product image placeholder, benefits list (4 bullets with `check-circle-2` icons), offer card with price (gradient-brand accent), testimonials section (3 cards with star ratings), FAQ section (5 `<details>` Q&A), public-style footer

**Checkpoint**: User Story 7 functional.

---

## Phase 10: User Story 8 - Settings, Profile & Notifications (Priority: P3)

**Goal**: Deliver the secondary dashboard pages that round out the prototype's completeness.

**Independent Test**: Open `settings.html`, `profile.html`, `notifications.html`. Verify settings has 6 tabs that swap content without reload, profile has all required fields, notifications shows entries spanning all 5 categories.

### Implementation for User Story 8

- [x] T036 [P] [US8] Author `settings.html` using shell partials, breadcrumb, H1 `الإعدادات`, `[data-tabs="settings"]` left-side tab navigation (or top tabs on `<lg`) with **6 tabs** per FR-034 (معلومات النشاط / الهوية البصرية / إعدادات الدفع / إعدادات عمولة المسوقين / إعدادات الإشعارات / الأمان), right-side panel rendering all 6 tab contents with only the first one initially active and the others `.hidden` (per the JS-only tab-switch contract from `assets/js/main.js`); each tab body must be a complete form with at least 4 fields and a Save button — Business info: business name / merchant phone / address / tax number; Branding: primary color picker / secondary color picker / logo upload affordance / favicon upload affordance; Payment: bank account / Instapay / STC Pay / PayPal / withdrawal threshold; Affiliate commission: default rate % / level overrides table (Bronze/Silver/Gold/Platinum rates) / cookie window days; Notifications: email-on-new-order toggle / email-on-affiliate-request toggle / SMS toggle / WhatsApp toggle; Security: change password trio (current/new/confirm) / 2FA toggle / sessions list with revoke buttons
- [x] T037 [P] [US8] Author `profile.html` using `partials/_page-skeleton.html` + shell partials, breadcrumb, H1 `الملف الشخصي`, avatar placeholder (`assets/img/placeholders/avatar.svg` with Arabic `alt="صورة الحساب"` per FR-049) with "تغيير الصورة" affordance, fields: name input, email input, phone input, password change section (current / new / confirm), Save and Cancel buttons in sticky footer
- [x] T038 [P] [US8] Author `notifications.html` using shell partials, breadcrumb, H1 `الإشعارات`, filter chips `[data-filter-chips]` (الكل / غير مقروء / طلبات / مسوقين / مدفوعات / مخزون / دفع — uses tab-switcher behavior under the hood), inbox list with **12 entries** spanning all 5 categories from FR-036 (4 new-order, 3 affiliate-request, 2 payout-request, 2 low-stock, 1 payment-update; ~30% read / 70% unread; mix of Arabic-month and relative timestamps), each entry: category icon (Lucide per `research.md` §6 stat mappings) / title / 1-sentence summary / actor / timestamp / unread dot, click area linking to relevant detail page (e.g., new-order entries link to `order-detail.html`); "Mark all as read" affordance at top right (visual only)

**Checkpoint**: User Story 8 functional. All 8 user stories complete.

---

## Phase 11: Polish & Cross-Cutting Concerns

**Purpose**: Acceptance-gate work that requires multiple stories to exist before it can run.

- [x] T039 [P] Author `analytics.html` using shell partials with the sidebar Analytics link visually active, breadcrumb, H1 `التحليلات`, styled "قريباً" coming-soon hero card with Lucide `bar-chart-3` icon and a 1-paragraph Arabic explainer, 3 placeholder chart illustrations using `assets/img/placeholders/chart-line.svg` and `chart-donut.svg`, CTA `العودة للوحة التحكم` → `dashboard.html`. Honors FR-045 by giving the sidebar Analytics link a real target instead of a dead link
- [x] T040 Update `README.md` (originally drafted in T002) with: a finalized project tree reflecting all generated files; a step-by-step "How to demo this to a client" walkthrough mirroring `quickstart.md` smoke test; a "Design tokens at a glance" table from `research.md` §4; a "Troubleshooting" copy of `quickstart.md` "Common issues & fixes"
- [x] T041 Run link-integrity audit against FR-045 / SC-002: from repo root run `grep -rEho 'href="[^"#]+\.html"' . --include='*.html' | sed -E 's/^href="//; s/"$//' | sort -u > /tmp/links.txt`, then verify every entry exists with `while read -r f; do test -f "$f" || echo "DEAD: $f"; done < /tmp/links.txt`; fix any reported dead links (typically by adding the missing page or correcting the href)
- [x] T042 Run accessibility audit per FR-046 / FR-047 / FR-048 / FR-049 / SC-012: (a) tab through `dashboard.html`, `products.html`, `orders.html`, `affiliates.html`, `affiliate-detail.html`, `index.html`, `pricing.html` — confirm visible focus rings on every interactive element and logical tab order; (b) open every modal type (delete-product / cancel-order / suspend-affiliate / reject-affiliate / pay-commission) and the mobile sidebar drawer, confirm ESC dismissal works; (c) verify every `<img>` has an `alt` attribute by running `grep -rEho '<img[^>]*>' . --include='*.html' | grep -v 'alt='` and confirming the result is empty; fix any deficiencies in `assets/css/app.css` and `assets/js/main.js` or in the offending HTML files
- [x] T043 Run color-contrast audit per FR-050: open `dashboard.html`, `affiliate-detail.html`, `orders.html`, and `index.html` in light theme then dark theme; use a browser DevTools contrast checker on body text, badge text, button labels, and link text in each combination; verify ≥ 4.5:1 for body text and ≥ 3:1 for large text (≥18 pt or ≥14 pt bold) and UI components; if any pair fails, adjust the offending color in the inline `tailwind.config` block of `partials/_head.html` and propagate the change to all pages that have already inlined the config
- [x] T044 Run cross-page sample-data consistency review per `data-model.md` cross-entity reference rules: pick the top 3 affiliates by sales from `affiliates.html` and verify they appear in `dashboard.html` top-affiliates card, `customers.html` source=Affiliate rows, and `orders.html` affiliate column with consistent names and currency; pick the top 3 products from `products.html` and verify appearance in `dashboard.html` top-products, `orders.html` product column, and `landing-pages.html` linked-product column; reconcile any drift back to the canonical entries in `SAMPLE-DATA.md`
- [ ] T045 Run `quickstart.md` Section "Smoke test (60-second sanity check)" 8-step pass in Chrome (latest), Firefox (latest), and Safari (latest if on macOS); document any browser-specific issues found in `README.md` Troubleshooting; verify SC-010 specifically — the Copy Referral Link button on `affiliate-detail.html` writes to clipboard and shows the "تم النسخ" toast — when served via a local HTTP server (`python3 -m http.server`) since `file://` may block the Clipboard API; verify SC-005 by recording a Chrome DevTools Performance trace while clicking any confirmation modal trigger (Delete product / Cancel order / Suspend affiliate) and confirming the modal's first paint occurs within 100 ms of the click event (≤6 frames at 60 Hz)
- [ ] T046 Run responsive layout pass per FR-040 / SC-006 at viewports 320 px, 414 px, 768 px, 1280 px, and 1920 px on `dashboard.html`, `products.html`, `orders.html`, `affiliates.html`, `affiliate-detail.html`, `customers.html`, `index.html`, `pricing.html`, `landing-page-preview.html`; verify no horizontal scroll on mobile, tables either scroll-x or collapse to mobile-card pattern, mobile sidebar drawer opens correctly with focus-trap on each viewport; fix any breakages in the offending pages or in `assets/css/app.css`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — start immediately.
- **Foundational (Phase 2)**: Depends on Setup. **BLOCKS all user stories** (T013–T038) because they all reuse `partials/_head.html`, `partials/_sidebar.html`, `partials/_header.html`, `partials/_footer.html`, `assets/css/app.css`, and `assets/js/main.js`.
- **User Story phases (Phase 3–10)**: Each depends on Foundational completing. After Foundational, stories may proceed in parallel (if staffed) or sequentially in priority order. Recommended sequential order: **US1 → US2 → US3 → US4 → US5 → US6 → US7 → US8** (P1 trio first to lock in MVP demo).
- **Polish (Phase 11)**: Audit tasks (T041, T042, T043, T044, T045, T046) require all user stories complete. T039 (analytics.html) requires Foundational only and can run in parallel with any user story. T040 (final README) builds on T002.

### User Story Dependencies (when running stories sequentially in priority order)

- **US1 (P1, Affiliates)**: First. No upstream dependencies beyond Foundational.
- **US2 (P1, Dashboard)**: Should run after US1 so the `dashboard.html` top-affiliates and pending-affiliate-requests cards reference real names from `affiliates.html` and `affiliate-requests.html` (cross-consistency rule from `data-model.md`).
- **US3 (P1, Products)**: Can run in parallel with US2; the dashboard's top-products card references `products.html` names but the canonical list is in `SAMPLE-DATA.md` from T003, so authoring order doesn't strictly matter.
- **US4 (P2, Orders)**: After US1 and US3 (orders reference both affiliates and products in their rows). May run in parallel with US5.
- **US5 (P2, Customers)**: After US1 (some customers reference affiliates as source). May run in parallel with US4.
- **US6 (P3, Marketing)**: Independent of all dashboard stories. May run any time after Foundational.
- **US7 (P3, Landing Pages)**: After US3 (linked-product references). May run in parallel with US8.
- **US8 (P3, Settings)**: Independent. May run any time after Foundational.

### Within Each User Story

- The pages within a story can almost always be authored in parallel (they live in different files).
- Exception: US2 has a single page (`dashboard.html`) that aggregates references from multiple other pages — author it last in its phase, or first as a placeholder and refine once cross-references settle.

### Parallel Opportunities

- All Phase 1 [P] tasks (T002, T003): can run in parallel.
- All Phase 2 [P] tasks (T004, T005, T006, T007, T008, T009, T010): can run in parallel; T011 and T012 sequential (they consolidate decisions from the [P] partials).
- Within every user story (Phase 3–10), all [P] tasks can run in parallel — different files, no dependencies.
- Phase 11: T039 [P] independent; T041, T042, T043, T044, T045, T046 should run sequentially (each is a multi-page audit and a finding from one may invalidate work seen in another).

---

## Parallel Example: User Story 1 (Affiliates)

```bash
# Once Foundational (Phase 2) is complete, launch all four affiliate pages in parallel:
Task: "Author affiliates.html with 10 rows and 7-action dropdown"
Task: "Author affiliate-detail.html with referral copy box, QR, stats grid, attributed orders, payouts, marketing assets, timeline"
Task: "Author affiliate-requests.html with 6 pending applicants and Approve/Reject modals"
Task: "Author affiliate-payouts.html with Pending/Paid/Rejected tabs and per-tab tables"
```

---

## Implementation Strategy

### MVP First (User Stories 1 + 2 + 3 — the P1 trio)

1. Complete Phase 1: Setup (T001–T003)
2. Complete Phase 2: Foundational (T004–T012) — **CRITICAL**, blocks all user stories
3. Complete Phase 3: User Story 1 (T013–T016) — Affiliates module
4. Complete Phase 4: User Story 2 (T017) — Dashboard
5. Complete Phase 5: User Story 3 (T018–T021) — Products
6. Run partial audit: link integrity + smoke test on the demo path (Sidebar → Affiliates → Affiliate detail → Dashboard → Products)
7. **STOP and VALIDATE**: Demo to client. Iterate. The P1 trio alone proves the product thesis (Constitution Principle V).

### Incremental Delivery

1. Setup + Foundational → Foundation ready (12 tasks).
2. Add US1 (Affiliates) → Affiliate-only demo possible (4 tasks).
3. Add US2 (Dashboard) → Dashboard-only demo (1 task).
4. Add US3 (Products) → MVP complete; ship for client review (4 tasks).
5. Add US4 (Orders) → Attribution chain demoable (3 tasks).
6. Add US5 (Customers) → CRM closed loop (3 tasks).
7. Add US6 (Marketing) → Onboarding flow (5 tasks).
8. Add US7 (Landing Pages) → Depth demo (3 tasks).
9. Add US8 (Settings) → Completeness (3 tasks).
10. Polish → Acceptance audits (8 tasks).

### Parallel Team Strategy

With 3 developers, after T012 completes:

- Dev A: US1 (Affiliates) → US4 (Orders) → polish T046 responsive
- Dev B: US3 (Products) → US5 (Customers) → polish T044 consistency
- Dev C: US2 (Dashboard) → US6 (Marketing) → US7 (Landing Pages) → US8 (Settings) → polish T041 link audit

T039 (analytics.html) can be picked up by whoever finishes a story phase first.

---

## Notes

- [P] tasks = different files, no dependencies on incomplete tasks.
- [Story] label maps each task to its user story for traceability.
- Every list page MUST hardcode the row counts specified in `research.md` §7 to satisfy SC-004.
- Cross-page name and currency consistency is a **strict acceptance gate** (T044 audits this).
- **Every `<img>` element on every page MUST carry an `alt` attribute** — Arabic for content images, `alt=""` for purely decorative ones (FR-049). T042 audits this post-hoc, but each per-page task is responsible for getting it right at authoring time.
- **Every page begins with `<!DOCTYPE html><html dir="rtl" lang="ar">`** (FR-037) — copy from `partials/_page-skeleton.html`.
- **Tables on list pages MUST be wrapped in `<div class="table-responsive">`** (FR-040) — the wrapper class is defined in `assets/css/app.css` per T011.
- **The brand glyph MUST be inlined as `<svg>` markup** copied from `partials/_logo-svg.html`, never referenced via `<img src="logo.svg">` (FR-045b).
- **Per-page allowed `<script>` set is exhaustively listed in FR-043** (5 elements: Tailwind CDN + Tailwind config inline + Lucide CDN + pre-paint theme inline + main.js bootstrap). Any deviation is a constitution-adjacent violation.
- No automated tests exist; verification is exclusively against `quickstart.md` checks.
- Commit after each task or logical group; never skip pre-commit hooks.
- Stop at any checkpoint to validate the partial deliverable.
- Avoid: introducing any framework / bundler / npm dep / API call (Constitution Principle I — NON-NEGOTIABLE).
