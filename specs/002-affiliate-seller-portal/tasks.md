---
description: "Task list for Affiliate Seller Portal — Static Frontend"
---

# Tasks: Affiliate Seller Portal — Static Frontend

**Input**: Design documents from `/specs/002-affiliate-seller-portal/`
**Prerequisites**: `plan.md`, `spec.md`, `research.md`, `data-model.md`, `contracts/affiliate-pages.md`, `quickstart.md`

**Tests**: None requested. This is a static, framework-free prototype with no build system; verification is manual (per `quickstart.md` and each user story's Independent Test). No automated test tasks are generated.

**Organization**: Tasks are grouped by user story (US1–US5 from `spec.md`) so each story can be implemented and demoed independently.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependency on an incomplete task)
- **[Story]**: US1–US5 (user-story phases only)
- Exact file paths are included in every task

## Path Conventions

Flat static site at the repository root (no `src/`, no build output). New HTML pages live at the root; shared assets are `assets/css/app.css` and `assets/js/main.js`; documentation partials live in `partials/`.

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Establish the reusable affiliate shell so all six pages stay identical.

- [x] T001 Create `partials/_affiliate-shell.html` — copy-paste reference markup (with paste instructions, in the same style as the other `partials/_*.html`) for the shared affiliate layout per `contracts/affiliate-pages.md` "The Affiliate Shell": sticky top header (`sticky top-0 z-30 bg-white/80 dark:bg-slate-950/80 backdrop-blur` with profile avatar `assets/img/placeholders/affiliate-avatar.svg` linking to `affiliate-profile.html`, name "أحمد", a "متاح للسحب: 1,420 ر.س" pill, a search `<input>`, a notification bell `[data-actions-dropdown="affiliate-notifications"]` with a dot + dropdown panel of 3–4 sample notifications, a `[data-theme-toggle]` button, and on `lg:` a "بوابة المسوّق" wordmark + wider search); the mobile bottom nav `[data-bottom-nav]` (`fixed bottom-0 inset-x-0 z-30 lg:hidden`) with exactly 5 `<a data-nav-target>` items in RTL order — الرئيسية→`affiliate-dashboard.html` (icon `home`), المنتجات→`affiliate-dashboard.html#products` (icon `shopping-bag`), المحفوظات→`affiliate-saved-products.html` (icon `bookmark`), الطلبات→`affiliate-orders.html` (icon `package`), الأرباح→`affiliate-earnings.html` (icon `wallet`); and a `hidden lg:flex` desktop sidebar with those 5 entries plus الملف الشخصي→`affiliate-profile.html`. Active item carries `is-active` + `aria-current="page"`. Note that pages set `<main class="… pb-24 lg:pb-8">`.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Shared CSS, shared JS, and the canonical hardcoded data set. **No affiliate page can be built until this phase is complete.**

- [x] T002 [P] Append affiliate styles to `assets/css/app.css` (raw CSS only — no `@apply`): `.affiliate-bottom-nav` (fixed bottom bar using logical insets `inset-inline-start/end:0`, top border, `box-shadow:0 -1px 3px rgba(0,0,0,.06)`, 5 equal flex items, active item `color: var(--brand) / #6366f1` + filled pill behind the icon) and its `.dark` variant; `.product-card` small touches (1:1 image wrapper, `line-clamp-2` helper if not already present); `.segmented-tabs` + `[data-segment]` resting state and `[data-segment].is-active` (filled pill / underline) + `.dark`; `.empty-state` centering touches; and card-badge tones mirroring the existing `.badge` system — `.badge-bestseller{background:#fef3c7;color:#92400e}`, `.badge-new{background:#d1fae5;color:#065f46}`, `.badge-hot{background:#ffe4e6;color:#9f1239}` plus `.dark .badge-bestseller/.badge-new/.badge-hot` matching the established pattern. Reuse existing `.badge-pending/.badge-confirmed/.badge-processing/.badge-delivered/.badge-cancelled/.badge-paid/.badge-rejected/.badge-active/.badge-bronze/.badge-silver/.badge-gold/.badge-platinum` for order/earnings/level/account states — do not redefine them.
- [x] T003 [P] Append four functions to `assets/js/main.js` and register them in the existing `DOMContentLoaded` boot block (alongside `initTheme/initSidebar/...`): `initFavoriteToggle()` — delegated click on `[data-favorite-toggle]`, toggles `is-favorited` on the button, flips `aria-pressed`, and swaps the Lucide heart between outline and filled (`fill-current text-rose-500` when `.is-favorited`); `initGallery()` — delegated click on `[data-gallery-thumb]` inside `[data-gallery]`, sets `[data-gallery-main]`'s `src`/`alt` from the thumb's `data-src`/`data-alt`, moves an `is-active` ring class among thumbs; `initSegmentedTabs()` — delegated click on `[data-segment]` inside `[data-segments="<group>"]`, moves `is-active` among the group's segments and updates `aria-selected` (visual-only — no panel switching); `initBottomNavActive()` — on load, compares `location.pathname`'s basename to each `[data-bottom-nav] a[data-nav-target]`'s `data-nav-target` and adds `is-active` + `aria-current="page"` to the match. No new `localStorage` keys; no routing/state/fetch; do not modify the existing functions.
- [x] T004 Author the canonical sample-data set and append it as a reference block (HTML comment) at the end of `partials/_affiliate-shell.html`: ≥16 distinct products with every `data-model.md` §2 field (`id`, `name`, `category` ∈ {الأكثر مبيعًا/عروض/إلكترونيات/ملابس/أدوات منزلية/إكسسوارات}, `badge`, ≥3 `images` = `assets/img/placeholders/product.svg`, ≥2 `videoThumbs`, `shortDescription`, `supplierPrice`, `suggestedPrice`, optional `wasPrice` for Hot-Offer items, `affiliateProfit`, multi-line `readyCaption`, multi-line `readyDetails`, 2–3 `sellingTips`, 4 `relatedIds`, `currency`, `isFavorited` for ~3–5 items) with section assignment (الأكثر مبيعًا ×5, عروض قوية اليوم ×5 all Hot-Offer+`wasPrice`, منتجات جديدة ×5 all New, ربح عالي ×5 all profit≥60); ≥12 affiliate orders (`AO-2026-0xxx`, masked customer = masked name OR masked phone, product name, status across all five values skewed ~4 Delivered/2 Processing/1 Confirmed/2 Pending/2–3 Cancelled, commission with consistent currency, date 2026-04→2026-05); ≥12 earnings rows (product, cross-referenced `orderNumber`, commission, status across Pending/Approved/Paid/Rejected skewed ~4 Paid/4 Approved/3 Pending/1 Rejected, date); and the أحمد الشمري profile (Gold, code `AHMAD20`, referral `https://smartmerchant.os/r/AHMAD20`, payment "محفظة STC Pay — 0555•••41", status Active, masked email/phone). Verify every item in the `data-model.md` "Cross-entity consistency checklist": `availableBalance`=Σ Approved=`1,420 ر.س`; `successfulOrdersCount`=count Delivered; `savedProductsCount`=count `isFavorited`; orders summary cards add up; earnings cards mutually coherent; currency mix ≈ SAR 50% / EGP 25% / AED 20% / other; names ≈ 80% Arabic-script / 20% Latin. (Depends on T001.)

**Checkpoint**: Shell partial + affiliate CSS + affiliate JS + canonical data are ready — page authoring can begin.

---

## Phase 3: User Story 1 — Browse Catalogue and Grab Selling Assets (Priority: P1) 🎯 MVP

**Goal**: Product-first home screen + a product-detail page with all selling assets, so an affiliate can go login → category → product → copy caption → start selling.

**Independent Test**: Open `affiliate-dashboard.html` directly — welcome line + quick-earnings card + search + category tabs + ≥1 product card visible within the first ~1.25 screens at 375 px; tapping a category tab moves the active state; the 4 sections each have a "عرض الكل" link and small cards; each card shows only image/badge/name/suggested price/profit/heart/"عرض التفاصيل". Click "عرض التفاصيل" → `affiliate-product-detail.html`; "نسخ الكابشن" and "نسخ تفاصيل المنتج" copy text and show "تم النسخ ✓"; a gallery thumbnail switches the main image; the favorite heart toggles.

### Implementation for User Story 1

- [x] T005 [US1] Create `affiliate-dashboard.html` — paste `partials/_head.html` verbatim (only `<title>` → "بوابة المسوّق — الرئيسية"), then the affiliate shell from `partials/_affiliate-shell.html` (header search placeholder `ابحث عن منتج للبيع...`, bottom-nav active = الرئيسية, `<main class="pb-24 lg:pb-8">`); welcome header with the exact lines `أهلاً يا أحمد 👋` and `ابدأ بيع المنتجات الجاهزة واربح عمولتك فورًا`; a gradient quick-earnings card (`bg-gradient-brand text-white rounded-2xl`) showing `الأرباح المتاحة` (`1,420 ر.س`, links → `affiliate-earnings.html`), `الطلبات الناجحة` (Delivered count, links → `affiliate-orders.html`), `المنتجات المحفوظة` (saved count, links → `affiliate-saved-products.html`) — figures from T004; an in-body search bar (placeholder `ابحث عن منتج للبيع...`); horizontal scrollable category tabs `[data-segments="categories"]` with exactly 7 `[data-segment]` buttons — `الكل` (`.is-active` by default), `الأكثر مبيعًا`, `عروض`, `إلكترونيات`, `ملابس`, `أدوات منزلية`, `إكسسوارات`; four product sections in order — `<section id="products">` "الأكثر مبيعًا", then "عروض قوية اليوم", "منتجات جديدة", "ربح عالي" — each with an `<h2>` heading and a `عرض الكل` link (→ `affiliate-dashboard.html#<section-anchor>`) and a horizontal scroller / grid placeholder for 5 cards (cards added in T006); a single `<script src="assets/js/main.js" defer></script>` before `</body>` and the Lucide CDN + pre-paint theme scripts (already in the head block) — no other inline scripts.
- [x] T006 [US1] Build the reusable product-card component and populate all 20 cards in `affiliate-dashboard.html` (5 per section, from T004's canonical products): each card = `rounded-2xl border border-slate-200 dark:border-slate-800 shadow-sm overflow-hidden`; a 1:1 `<img src="assets/img/placeholders/product.svg" alt="<product name>" class="object-cover">`; an absolutely-positioned badge pill top-start when applicable (`Bestseller`→`.badge-bestseller`, `New`→`.badge-new`, `Hot Offer`→`.badge-hot`) and for Hot-Offer cards a small strikethrough "كان <wasPrice>"; a `[data-favorite-toggle]` heart button top-end with `aria-pressed` reflecting `isFavorited`; body `p-3 space-y-1` — name `text-sm font-semibold line-clamp-2`, `سعر البيع: <suggestedPrice>` (`text-xs text-slate-500`), `أرباحك: <affiliateProfit>` emphasized (`text-sm font-bold text-emerald-600`); footer — a full-width `عرض التفاصيل` button (`bg-brand-primary text-white rounded-xl py-1.5 text-xs`) → `affiliate-product-detail.html`. **Nothing else on the card** — no description, no rating, no stock, no supplier price. (Same file as T005; do after T005.)
- [x] T007 [US1] Create `affiliate-product-detail.html` for one fully-populated representative product (from T004) — `partials/_head.html` (`<title>` → "بوابة المسوّق — تفاصيل المنتج") + the affiliate shell (`<main class="pb-24 lg:pb-8">`) + a back link → `affiliate-dashboard.html`; an image gallery `[data-gallery]` with a main `<img data-gallery-main alt>` and ≥3 thumbnails `[data-gallery-thumb data-src data-alt]`; ≥1 video-preview placeholder thumbnail with a play-icon overlay (reuse `product.svg` / `assets/img/placeholders/dashboard-preview.svg`, no real video); the product name + applicable badge pills + a `[data-favorite-toggle]` heart; a short description (1–2 sentences); a sales/pricing card showing `سعر المورد`, `سعر البيع المقترح`, `صافي ربحك` (consistent currency); a grouped row of exactly six quick-action buttons — `تحميل الصور` (`<a download href="assets/img/placeholders/product.svg">` or no-op), `تحميل الفيديوهات` (same), `نسخ الكابشن` (`[data-copy="caption"]`), `نسخ تفاصيل المنتج` (`[data-copy="details"]`), `مشاركة واتساب` (`<a href="https://wa.me/?text=…">`), `طلب أوردر` (`[data-modal-trigger="order-modal"]`); a ready caption box (`[data-copy-container]` wrapping the caption text in `[data-copy-value]` plus a `[data-copy]` copy button → fires the existing `#copied-toast`); a product details box (same `[data-copy-container]`/`[data-copy-value]`/`[data-copy]` pattern, separate button); a "نصائح للبيع" section listing 2–3 selling tips; a related-products section of 4 cards reusing the T006 product-card component (`عرض التفاصيل` → `affiliate-product-detail.html`); and an optional `[data-modal="order-modal"]` (and/or `[data-modal="product-modal"]`) with a `[data-modal-close]` — relying on the existing `initModals()` for backdrop/ESC/focus-trap. Single deferred `main.js` script; no other inline scripts. (Reuses the card component from T006.)

**Checkpoint**: User Story 1 is fully functional — the dashboard and product-detail pages work and demo independently. **This is the MVP.**

---

## Phase 4: User Story 2 — Track My Orders (Priority: P2)

**Goal**: An orders page showing the affiliate's own orders with summary counts, a status filter, mobile cards / desktop table, and masked customer data.

**Independent Test**: Open `affiliate-orders.html` directly — 4 summary cards (كل الطلبات / قيد التنفيذ / تم التسليم / ملغية) with counts that add up; orders are cards on mobile and a table on desktop; each order shows number, masked customer (name or phone — never full PII/email), product, status badge (Cancelled distinct), commission with currency, date; the filter chips and search respond visually.

### Implementation for User Story 2

- [x] T008 [P] [US2] Create `affiliate-orders.html` — `partials/_head.html` (`<title>` → "بوابة المسوّق — طلباتي") + the affiliate shell (bottom-nav active = الطلبات, `<main class="pb-24 lg:pb-8">`); a `طلباتي` heading; four summary cards `كل الطلبات` / `قيد التنفيذ` / `تم التسليم` / `ملغية` with the coherent counts from T004 (`قيد التنفيذ` = Pending+Confirmed+Processing, `تم التسليم` = Delivered, `ملغية` = Cancelled, total = `كل الطلبات`); a filter bar with status chips `[data-segments="order-status"]` (`الكل` `.is-active` + per-status options) and a search `<input>` (placeholder `ابحث برقم الطلب أو المنتج...`) — both visual-only; the orders list rendered twice from T004's ≥12 rows — a `lg:hidden` stack of cards and a `hidden lg:block` `<table>` — each order showing order number, **masked** customer (`أحمد ا***` style name OR `055•• ••• 41` style phone; never a full name+phone+address; never an email), product name, a status badge (`.badge-pending`/`.badge-confirmed`/`.badge-processing`/`.badge-delivered`/`.badge-cancelled`), commission as a currency token, and a date; `Cancelled` rows use the rose `.badge-cancelled`. Single deferred `main.js`.

**Checkpoint**: User Stories 1 and 2 both work independently.

---

## Phase 5: User Story 3 — Understand Earnings and Request a Payout (Priority: P2)

**Goal**: An earnings page with the available-balance card + "طلب سحب", three stat cards, the commission-approval notice, an earnings history, and a working payout request modal.

**Independent Test**: Open `affiliate-earnings.html` directly — a prominent main card (`الأرباح المتاحة للسحب` + amount + `طلب سحب`); 3 cards (إجمالي الأرباح / أرباح قيد المراجعة / أرباح مدفوعة) with coherent figures; the notice `يتم اعتماد العمولة بعد تأكيد الدفع أو تسليم الطلب.`; an earnings history (cards on mobile, table on desktop) where each row shows product, order number, commission, status (Pending/Approved/Paid/Rejected — Rejected distinct), date; clicking `طلب سحب` opens a modal with amount / payment method / wallet-or-account / notes that dismisses on ESC, the close button, and a backdrop click with focus restored.

### Implementation for User Story 3

- [x] T009 [P] [US3] Create `affiliate-earnings.html` — `partials/_head.html` (`<title>` → "بوابة المسوّق — الأرباح") + the affiliate shell (bottom-nav active = الأرباح, `<main class="pb-24 lg:pb-8">`); an `الأرباح` heading; a prominent gradient main card (`bg-gradient-brand text-white rounded-2xl`) showing `الأرباح المتاحة للسحب` + `1,420 ر.س` + a `طلب سحب` button `[data-modal-trigger="payout-modal"]`; three secondary cards `إجمالي الأرباح` / `أرباح قيد المراجعة` / `أرباح مدفوعة` with the coherent figures from T004; an info note containing the exact text `يتم اعتماد العمولة بعد تأكيد الدفع أو تسليم الطلب.`; an earnings history rendered twice from T004's ≥12 rows — a `lg:hidden` card stack and a `hidden lg:block` `<table>` — each row showing product, order number, commission as a currency token, a status badge (`Pending`→`.badge-pending`, `Approved`→`.badge-confirmed`, `Paid`→`.badge-paid`, `Rejected`→`.badge-rejected`), and a date; `Rejected` rows use the rose `.badge-rejected`. Single deferred `main.js`.
- [x] T010 [US3] Add the payout request modal to `affiliate-earnings.html`: `<div data-modal="payout-modal" class="hidden …">` containing a form with an amount `<input type="number">` (prefill `1420`, helper text `الحد الأدنى للسحب 100 ر.س`), a payment-method `<select>` (`محفظة STC Pay` / `تحويل بنكي` / `محفظة فودافون كاش` / `PayPal`), a wallet/account `<input type="text">` (placeholder `رقم المحفظة أو الحساب البنكي (IBAN)`), a notes `<textarea>` (optional), and two buttons — `تأكيد طلب السحب` (primary, no-op or `[data-modal-close]`) and `إلغاء` (`[data-modal-close]`); a header close button `[data-modal-close]`; rely on the existing `initModals()` for the backdrop, ESC dismissal, focus-trap, and focus restoration — add no new JS. (Same file as T009; do after T009.)

**Checkpoint**: User Stories 1, 2, and 3 all work independently.

---

## Phase 6: User Story 4 — Saved Products Shortlist (Priority: P3)

**Goal**: A saved-products page reusing the dashboard product card, with a search and an empty-state.

**Independent Test**: Open `affiliate-saved-products.html` directly — a header, a search input, and a grid of product cards identical to the dashboard cards (hearts start filled); an empty-state block is present in the markup with a message and a CTA → `affiliate-dashboard.html`; the heart toggle works on the cards.

### Implementation for User Story 4

- [x] T011 [P] [US4] Create `affiliate-saved-products.html` — `partials/_head.html` (`<title>` → "بوابة المسوّق — المحفوظات") + the affiliate shell (bottom-nav active = المحفوظات, `<main class="pb-24 lg:pb-8">`); a header `المنتجات المحفوظة` + a short subline; a search `<input>` (placeholder `ابحث في محفوظاتك...`) — visual-only; a responsive grid of the **identical** product-card component from T006 populated with the 3–5 canonical products where `isFavorited`=true, with each card's heart in the filled state (`.is-favorited`, `aria-pressed="true"`) and `عرض التفاصيل` → `affiliate-product-detail.html`; and an empty-state block present in the markup (a large Lucide `bookmark` icon, the message `لا توجد منتجات محفوظة بعد`, and a `تصفّح المنتجات` button → `affiliate-dashboard.html`) — placed after the grid, kept `hidden` with an HTML comment noting "remove `hidden` to preview the empty state" (or shown as a clearly-labelled secondary variant). Single deferred `main.js`. (Reuses the card component from T006.)

**Checkpoint**: User Stories 1–4 all work independently.

---

## Phase 7: User Story 5 — Account, Level, and Referral Tools (Priority: P3)

**Goal**: A profile page with the affiliate's level, copyable referral link & coupon, QR placeholder, info form, payment method, and account status.

**Independent Test**: Open `affiliate-profile.html` directly — a profile card with name, avatar, and a level badge (Bronze/Silver/Gold/Platinum); a referral-link box with a copy button and a coupon-code copy button (each copies and shows `تم النسخ ✓`); a QR placeholder, a basic info form, payment method info, and an account status indicator are all present; the theme toggle works; if the payout modal is surfaced here it opens/closes correctly.

### Implementation for User Story 5

- [x] T012 [P] [US5] Create `affiliate-profile.html` — `partials/_head.html` (`<title>` → "بوابة المسوّق — الملف الشخصي") + the affiliate shell (desktop sidebar active = الملف الشخصي; the header avatar is the entry point on mobile; `<main class="pb-24 lg:pb-8">`); a profile card with the avatar `assets/img/placeholders/affiliate-avatar.svg` (`alt="صورة أحمد الشمري"`), the name `أحمد الشمري`, and an affiliate level badge `<span class="badge badge-gold">Gold</span>` (the four possible levels are Bronze/Silver/Gold/Platinum); a referral-link box `[data-copy-container]` containing the link in `[data-copy-value]` (`https://smartmerchant.os/r/AHMAD20`, e.g. in a readonly `<input>`) and a `[data-copy]` copy button; a QR code placeholder `<img src="assets/img/placeholders/qr-code.svg" alt="رمز QR لرابط الإحالة">`; a coupon-code display showing `AHMAD20` with its own `[data-copy]` copy button (a second `[data-copy-container]`); a basic info form with prefilled fields `الاسم` / `البريد الإلكتروني` (masked) / `الجوال` (masked) / `المدينة` / `الدولة` and a `حفظ التعديلات` button (no-op); a payment-method section showing `محفظة STC Pay — 0555•••41` plus a `طلب سحب` button `[data-modal-trigger="payout-modal"]`; an account-status indicator `<span class="badge badge-active">Active</span>`; and the payout modal markup copied from T010 (`[data-modal="payout-modal"]` with the same fields and `[data-modal-close]` controls) so the trigger on this page works. The shell's `[data-theme-toggle]` works here unchanged. Single deferred `main.js`. (Reuses the payout modal from T010.)

**Checkpoint**: All five user stories work independently.

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Make the portal discoverable from the rest of the prototype and verify it end-to-end.

- [x] T013 [P] Edit `login.html` (additive only — remove no existing content): add a role selector ("أنا تاجر" / "أنا مسوّق بالعمولة"); when "أنا مسوّق بالعمولة" is chosen the primary submit/CTA links to `affiliate-dashboard.html` (the merchant option keeps linking to `dashboard.html`) — per `research.md` §7 and `contracts/affiliate-pages.md` "Edited existing pages".
- [x] T014 [P] Edit `affiliates.html` (merchant view, additive only): add a header link `معاينة بوابة المسوّق ↗` → `affiliate-dashboard.html`. Do not change any existing merchant affiliate content.
- [x] T015 Link-integrity audit: run `grep -ohE 'href="[^"#?]+\.html' affiliate-*.html login.html affiliates.html | sort -u` and confirm every target file exists; then walk the `contracts/affiliate-pages.md` "Link-integrity matrix" — the 5 bottom-nav links, the 6 desktop-sidebar links, the header avatar link, every `عرض التفاصيل`, every `عرض الكل` anchor, the saved-products empty-state CTA, and the `طلب سحب` / `طلب أوردر` modal triggers on every affiliate page — and fix any dead or wrong link.
- [x] T016 RTL / responsive / theme pass across all 6 affiliate pages: confirm `<html lang="ar" dir="rtl">`; only logical-property spacing utilities (`ms-/me-/ps-/pe-/start-/end-`) — no `ml/mr/pl/pr/left/right`; the mobile bottom nav (`lg:hidden`) and the desktop sidebar (`hidden lg:flex`) never appear together; `<main>` has `pb-24 lg:pb-8` so the bottom bar never overlaps content; orders and earnings render as cards (not horizontally-scrolling tables) below `lg:`; the gradients are subtle (white-dominant background); dark/light parity holds (all `.badge-*`, gradient cards, header blur) and contrast is AA-equivalent in both themes.
- [x] T017 Accessibility & interaction pass across all 6 affiliate pages: every `<img>` has a meaningful `alt`; all interactive elements show a visible focus ring and the tab order is logical; favorite hearts expose `aria-pressed`; segment buttons expose `aria-selected`; the active nav item exposes `aria-current="page"`; the payout modal (and the optional order/product modals) dismiss via ESC, the close button, and a backdrop click with focus restored to the trigger; the `[data-copy]` buttons copy the right text, show the `#copied-toast` `تم النسخ ✓`, and fall back to the `execCommand`/textarea path without `navigator.clipboard`; `lucide.createIcons()` runs (icons render, not raw `<i data-lucide>` tags).
- [x] T018 Run the `specs/002-affiliate-seller-portal/quickstart.md` verification checklist end-to-end (Shell + US1–US5 + General sections) both via `file://` (double-click) and via Live Server / `python3 -m http.server`, and fix any gap; confirm no network requests are made for application data.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Setup)**: T001 — no dependencies; start immediately.
- **Phase 2 (Foundational)**: T002 and T003 depend on nothing (parallelizable); T004 depends on T001. **All of Phase 2 must finish before any page in Phases 3–7.**
- **Phase 3 (US1)**: depends on Phase 2. T005 → T006 (same file) → T007 (reuses T006's card).
- **Phase 4 (US2)**: depends on Phase 2. T008 is independent of US1/US3/US4/US5.
- **Phase 5 (US3)**: depends on Phase 2. T009 → T010 (same file).
- **Phase 6 (US4)**: depends on Phase 2; reuses the product-card component from T006 (US1) — copy its markup, so US4 is still independently testable but is best built after T006.
- **Phase 7 (US5)**: depends on Phase 2; reuses the payout-modal markup from T010 (US3) — copy it, so US5 is still independently testable but is best built after T010.
- **Phase 8 (Polish)**: T013 and T014 are independent of each other and of the affiliate pages (additive edits to existing files); T015–T018 require all six affiliate pages to exist.

### User Story Dependencies

- **US1 (P1)** — depends only on Foundational. No dependency on other stories. **MVP.**
- **US2 (P2)** — depends only on Foundational. Fully independent.
- **US3 (P2)** — depends only on Foundational. Fully independent.
- **US4 (P3)** — depends on Foundational; soft reuse of US1's card component (markup copy).
- **US5 (P3)** — depends on Foundational; soft reuse of US3's payout modal (markup copy).

### Parallel Opportunities

- T002 and T003 (different files) can run in parallel within Phase 2.
- Once Phase 2 is done, the page-creation tasks for different stories — T005 (US1), T008 (US2), T009 (US3), T011 (US4), T012 (US5) — are all different files and can be worked in parallel by different people (mind the soft reuses: T011 wants T006 first; T012 wants T010 first).
- T013 and T014 (Polish) are different files and can run in parallel; they can also run any time after the affiliate pages exist.

---

## Parallel Example: after Phase 2 completes

```text
# Different files, no hard cross-story dependency — can be developed concurrently:
Task T005: "Create affiliate-dashboard.html (shell + welcome + quick-earnings + category tabs + 4 product sections)"
Task T008: "Create affiliate-orders.html (4 summary cards + filter bar + mobile cards / desktop table)"
Task T009: "Create affiliate-earnings.html (main card + 3 stat cards + commission notice + earnings history)"
# Then, once T006 (card component) and T010 (payout modal) exist:
Task T011: "Create affiliate-saved-products.html (reuses the product card)"
Task T012: "Create affiliate-profile.html (reuses the payout modal)"
```

---

## Implementation Strategy

### MVP First (User Story 1 only)

1. Phase 1: T001 (affiliate shell partial).
2. Phase 2: T002 (CSS) ∥ T003 (JS), then T004 (canonical data).
3. Phase 3: T005 → T006 → T007.
4. **STOP and VALIDATE**: run US1's Independent Test and the `quickstart.md` "US1" checklist.
5. Demo the affiliate dashboard + product detail.

### Incremental Delivery

1. Setup + Foundational → infrastructure ready.
2. + US1 (T005–T007) → test → demo (MVP).
3. + US2 (T008) → test → demo.
4. + US3 (T009–T010) → test → demo.
5. + US4 (T011) → test → demo.
6. + US5 (T012) → test → demo.
7. Polish (T013–T018) → discoverable, audited, validated.

---

## Notes

- No tests are generated — static prototype, no build, manual verification per `quickstart.md`.
- `[P]` = different files, no dependency on an incomplete task.
- `[Story]` labels (US1–US5) trace each task to its user story.
- Every affiliate page pastes `partials/_head.html` verbatim (only `<title>` changes) and includes exactly one `<script src="assets/js/main.js" defer></script>` — no other inline scripts beyond the pre-paint theme line and the Lucide CDN tag already in the head block (Constitution Principle I & VII).
- Reuse the existing `.badge-*` classes and the existing `main.js` hooks (`[data-copy]`, `[data-modal-*]`, `[data-actions-dropdown]`, `[data-theme-toggle]`) — only T002/T003 add new CSS/JS, and only as described.
- Keep all sample data hardcoded in the HTML and internally coherent (see the `data-model.md` cross-entity checklist); never expose full customer PII on the orders or earnings pages.
- Commit after each task or logical group; stop at any checkpoint to validate a story independently.
