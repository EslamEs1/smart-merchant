# Pages Contract: Affiliate Seller Portal — Static Frontend

**Feature**: 002-affiliate-seller-portal
**Date**: 2026-05-11
**Purpose**: For a static prototype the only "interface contract" is the URL → file → required-content commitment plus the JS hook attributes `assets/js/main.js` expects. This document is the authoritative list of every HTML file this feature ships (and the two it edits), the content shape each MUST satisfy, the `data-*` hooks it MUST expose, and the inbound links it MUST honor.

Every link in any affiliate-shell nav, header, in-page CTA, "عرض التفاصيل" / "عرض الكل" button, or empty-state CTA MUST resolve to a file in this list or an already-shipping file. Conversely every file in this list is the target of at least one such inbound link (FR-072, FR-075).

---

## Conventions

- **URL** = path relative to repo root (`file://` or `http://host/<URL>`).
- **Shell** = the shared affiliate layout (defined once below); every affiliate page includes it.
- **JS hooks** = the `data-*` attributes / element ids that `main.js` (existing + the 4 new functions from `research.md` §3) looks for.
- **Inbound** = pages that MUST link here.
- Status tokens stay English; everything else Arabic; `dir="rtl" lang="ar"`; head block = `partials/_head.html` verbatim (only `<title>` changes); single `<script src="assets/js/main.js" defer></script>` before `</body>`; Lucide CDN tag from the head block; the pre-paint theme `<script>` from the head block — **no other inline scripts**.

---

## The Affiliate Shell (shared by all 6 affiliate pages)

**Required regions** (RTL order):

1. **Top header** — `sticky top-0 z-30`, white/blur, bottom border. Contains:
   - profile avatar (`assets/img/placeholders/affiliate-avatar.svg`, rounded-full, `alt`) — link → `affiliate-profile.html`
   - affiliate name `أحمد` + an earnings pill `متاح للسحب: 1,420 ر.س`
   - a search input — placeholder `ابحث عن منتج للبيع...` on the dashboard; `ابحث...` (page-appropriate) elsewhere
   - a notification bell icon button — `[data-actions-dropdown="affiliate-notifications"]` with a small unread dot and a dropdown panel listing 3–4 sample notifications
   - on `lg:` a "بوابة المسوّق" wordmark at the start and a wider search
   - theme toggle button `[data-theme-toggle]` (icon `moon`/`sun`)
2. **Mobile bottom navigation** — `fixed bottom-0 inset-x-0 z-30`, `lg:hidden`, `[data-bottom-nav]`. Exactly 5 items, in this order, each `<a data-nav-target="…">` with an icon + label:
   | Label | `data-nav-target` / href | Icon |
   |---|---|---|
   | الرئيسية | `affiliate-dashboard.html` | `home` |
   | المنتجات | `affiliate-dashboard.html#products` | `shopping-bag` |
   | المحفوظات | `affiliate-saved-products.html` | `bookmark` |
   | الطلبات | `affiliate-orders.html` | `package` |
   | الأرباح | `affiliate-earnings.html` | `wallet` |
   The current page's item gets `is-active` + `aria-current="page"`.
3. **Desktop sidebar** — `hidden lg:flex`, narrow rail, same 5 entries (vertical) **plus** `الملف الشخصي` → `affiliate-profile.html`; same active treatment; when shown, bottom nav is hidden (they never coexist).
4. **Main content** — `<main>` with `pb-24 lg:pb-8` so the fixed bottom nav never overlaps the last row/button.

**Shell JS hooks**: `[data-theme-toggle]`, `[data-actions-dropdown]` (notifications + any header menu), `[data-bottom-nav]` + `[data-nav-target]` (active-state helper), `[data-copy]`/`[data-copy-container]`/`[data-copy-value]` wherever copy buttons appear.

A copy-paste reference of this markup lives in `partials/_affiliate-shell.html` (documentation partial; not loaded at runtime).

---

## `affiliate-dashboard.html`

- **URL**: `/affiliate-dashboard.html`
- **Required components**:
  - Affiliate shell (header search placeholder = `ابحث عن منتج للبيع...`; bottom-nav active = الرئيسية)
  - Welcome header — exact lines `أهلاً يا أحمد 👋` and `ابدأ بيع المنتجات الجاهزة واربح عمولتك فورًا`
  - Quick-earnings card (gradient, white text) — three figures: `الأرباح المتاحة` (`1,420 ر.س`), `الطلبات الناجحة` (count = Delivered orders), `المنتجات المحفوظة` (= saved-page card count)
  - In-body search bar (may be the header search on mobile; an in-content one is also fine) — placeholder `ابحث عن منتج للبيع...`
  - Horizontal scrollable category tabs `[data-segments="categories"]` with `[data-segment]` buttons, exactly: `الكل` (active by default), `الأكثر مبيعًا`, `عروض`, `إلكترونيات`, `ملابس`, `أدوات منزلية`, `إكسسوارات`
  - 4 product sections, in order, each with an `<h2>` heading and a `عرض الكل` link (→ `affiliate-dashboard.html#<anchor>`), each containing a horizontal scroller or grid of small product cards: `الأكثر مبيعًا` (5 cards) · `عروض قوية اليوم` (5 cards) · `منتجات جديدة` (5 cards) · `ربح عالي` (5 cards). The "المنتجات" bottom-nav anchor `#products` resolves to the first product section's wrapper.
  - Every product card = the exact field set from `data-model.md` §2 (image, optional badge, name, suggested price labeled `سعر البيع`, affiliate profit labeled `أرباحك`, favorite heart, `عرض التفاصيل` button). **No descriptions on cards.**
- **JS hooks**: `[data-segments="categories"]` + `[data-segment]`; `[data-favorite-toggle]` on every card; shell hooks. `عرض التفاصيل` → `affiliate-product-detail.html`.
- **Inbound**: `login.html` (affiliate role option), `affiliates.html` (cross-link), every affiliate page's bottom nav / sidebar (الرئيسية), `affiliate-product-detail.html` (back link).

## `affiliate-product-detail.html`

- **URL**: `/affiliate-product-detail.html`
- **Required components** (subject = one fully-populated representative Product):
  - Affiliate shell
  - Breadcrumb / back link → `affiliate-dashboard.html`
  - **Image gallery** `[data-gallery]`: main `<img data-gallery-main>` + ≥3 thumbnails `[data-gallery-thumb]` carrying `data-src`/`data-alt`
  - **Video preview placeholder** — ≥1 thumbnail with a play-icon overlay (no real video)
  - Product name + badges (`Bestseller`/`New`/`Hot Offer` pills as applicable) + favorite heart `[data-favorite-toggle]`
  - Short description (1–2 sentences)
  - **Sales/pricing card** — `سعر المورد`, `سعر البيع المقترح`, `صافي ربحك` (consistent currency)
  - **Quick action buttons** — exactly these six, visibly grouped: `تحميل الصور` (link with `download` to a placeholder, or no-op), `تحميل الفيديوهات` (same), `نسخ الكابشن` (`[data-copy]` → caption box value), `نسخ تفاصيل المنتج` (`[data-copy]` → details box value), `مشاركة واتساب` (`<a href="https://wa.me/?text=…">`), `طلب أوردر` (`[data-modal-trigger="order-modal"]` opening a simple confirm-style modal, or a link to a placeholder)
  - **Ready caption box** — a styled block (`[data-copy-container]`) containing the caption text (`[data-copy-value]`) and a copy button (`[data-copy]`) → triggers the `#copied-toast` `تم النسخ ✓`
  - **Product details box** — same pattern, separate copy button
  - **Suggested selling tips** section — 2–3 tips
  - **Related products** section — 4 product cards (same card component, same `[data-favorite-toggle]`, `عرض التفاصيل` → `affiliate-product-detail.html`)
  - *(optional)* a product-detail modal `[data-modal="product-modal"]` if used — must open/close via trigger, backdrop, `[data-modal-close]`, ESC
- **JS hooks**: `[data-gallery]` + `[data-gallery-main]` + `[data-gallery-thumb]`; `[data-favorite-toggle]`; `[data-copy]` (×2 minimum) + `[data-copy-container]`/`[data-copy-value]`; `[data-modal-trigger]`/`[data-modal]`/`[data-modal-close]` (order &/or product modal); shell hooks.
- **Inbound**: every product card's `عرض التفاصيل` across `affiliate-dashboard.html`, `affiliate-saved-products.html`, and this page's own related section.

## `affiliate-orders.html`

- **URL**: `/affiliate-orders.html`
- **Required components**:
  - Affiliate shell (bottom-nav active = الطلبات)
  - Page heading `طلباتي`
  - **4 summary cards**: `كل الطلبات`, `قيد التنفيذ`, `تم التسليم`, `ملغية` — counts that add up (see `data-model.md` §3)
  - **Search / filter bar** — status chips `[data-segments="order-status"]` with `[data-segment]` (`الكل` active by default + per-status options) + a search input (placeholder `ابحث برقم الطلب أو المنتج...`); visual-only
  - **Orders list** — ≥12 rows; rendered as stacked **cards** at `<lg` and as a **table** at `lg:` (e.g., two sibling containers, one `lg:hidden`, one `hidden lg:block`). Each order shows: order number, masked customer (name OR phone — never full PII, never email), product name, status badge (`.badge-pending/.badge-confirmed/.badge-processing/.badge-delivered/.badge-cancelled`), commission (currency token), date. `Cancelled` uses the rose `.badge-cancelled`.
- **JS hooks**: `[data-segments="order-status"]` + `[data-segment]`; shell hooks. No modal required.
- **Inbound**: bottom nav / sidebar (الطلبات) from every affiliate page; optionally `affiliate-dashboard.html` quick-earnings "الطلبات الناجحة" links here.

## `affiliate-earnings.html`

- **URL**: `/affiliate-earnings.html`
- **Required components**:
  - Affiliate shell (bottom-nav active = الأرباح)
  - Page heading `الأرباح`
  - **Main earnings card** (gradient, prominent) — `الأرباح المتاحة للسحب` + amount (`1,420 ر.س`) + a `طلب سحب` button `[data-modal-trigger="payout-modal"]`
  - **3 secondary cards** — `إجمالي الأرباح`, `أرباح قيد المراجعة`, `أرباح مدفوعة` (coherent figures per `data-model.md` §4)
  - **Commission notice** — exact text `يتم اعتماد العمولة بعد تأكيد الدفع أو تسليم الطلب.` (styled as an info note)
  - **Earnings history** — ≥12 rows; cards at `<lg`, table at `lg:`. Each row: product, order number, commission (currency token), status badge (`.badge-pending` for Pending, `.badge-confirmed` for Approved, `.badge-paid` for Paid, `.badge-rejected` for Rejected), date. `Rejected` uses the rose `.badge-rejected`.
  - **Payout request modal** `[data-modal="payout-modal"]` — fields: amount (number, prefill `1,420`), payment method (select), wallet/account number (text), notes (textarea); buttons `تأكيد طلب السحب` (primary, no-op/close) and `إلغاء` (`[data-modal-close]`). Dismiss via backdrop, close button, ESC.
- **JS hooks**: `[data-modal-trigger="payout-modal"]` / `[data-modal="payout-modal"]` / `[data-modal-close]`; shell hooks.
- **Inbound**: bottom nav / sidebar (الأرباح) from every affiliate page; `affiliate-dashboard.html` quick-earnings "الأرباح المتاحة" links here; optionally `affiliate-profile.html` surfaces the payout modal trigger too.

## `affiliate-saved-products.html`

- **URL**: `/affiliate-saved-products.html`
- **Required components**:
  - Affiliate shell (bottom-nav active = المحفوظات)
  - Header `المنتجات المحفوظة` + a short subline
  - Search input — placeholder `ابحث في محفوظاتك...` (visual only)
  - **Product cards grid** — the *identical* card component from the dashboard, populated with the 3–5 products whose `isFavorited` = true; each card's heart starts in the filled state
  - **Empty-state block** — present in the markup (may be `hidden` when the grid is populated, OR shown as a documented variant): an illustration/icon (e.g., Lucide `bookmark` large), a message (`لا توجد منتجات محفوظة بعد`), and a CTA button `تصفّح المنتجات` → `affiliate-dashboard.html`
- **JS hooks**: `[data-favorite-toggle]` on every card; shell hooks. `عرض التفاصيل` → `affiliate-product-detail.html`.
- **Inbound**: bottom nav / sidebar (المحفوظات) from every affiliate page; `affiliate-dashboard.html` quick-earnings "المنتجات المحفوظة" links here; empty-state CTA targets `affiliate-dashboard.html`.

## `affiliate-profile.html`

- **URL**: `/affiliate-profile.html`
- **Required components**:
  - Affiliate shell (sidebar active = الملف الشخصي; bottom nav has no profile item — header avatar is the entry point)
  - **Profile card** — avatar, name `أحمد الشمري`, and an **affiliate level badge** (`.badge-gold` "Gold") — the four possible levels are Bronze/Silver/Gold/Platinum
  - **Referral link box** — `[data-copy-container]` with the link text (`[data-copy-value]` = `https://smartmerchant.os/r/AHMAD20`) and a copy button (`[data-copy]`) → `تم النسخ ✓` toast
  - **QR code placeholder** — `assets/img/placeholders/qr-code.svg` with `alt="رمز QR لرابط الإحالة"`
  - **Coupon code** — displayed code `AHMAD20` with its own copy button (`[data-copy]`) → toast
  - **Basic info form** — fields الاسم, البريد (masked), الجوال (masked), المدينة, الدولة, pre-filled; a `حفظ التعديلات` button (no-op)
  - **Payment method info** — e.g. `محفظة STC Pay — 0555•••41`, with a `طلب سحب` button `[data-modal-trigger="payout-modal"]` reusing the payout modal markup (the modal block must be present on this page too)
  - **Account status** — `Active` (`.badge-active`)
- **JS hooks**: `[data-copy]` (×2: referral link + coupon) + `[data-copy-container]`/`[data-copy-value]`; `[data-modal-trigger="payout-modal"]` / `[data-modal="payout-modal"]` / `[data-modal-close]`; `[data-theme-toggle]`; `[data-favorite-toggle]` (only if any product card is shown here — optional); shell hooks.
- **Inbound**: header avatar link from every affiliate page; desktop sidebar (الملف الشخصي).

---

## Edited existing pages (entry point — additive only)

### `login.html` — EDIT

- Add a role selector ("أنا تاجر" / "أنا مسوّق بالعمولة"); the affiliate option's primary submit/CTA links to `affiliate-dashboard.html` (the merchant option keeps linking to `dashboard.html`). No existing content removed.
- **Inbound to affiliate portal**: this is the primary entry point → `affiliate-dashboard.html`.

### `affiliates.html` (merchant) — EDIT

- Add a header link `معاينة بوابة المسوّق ↗` → `affiliate-dashboard.html`. No existing content removed; the merchant affiliate pages are otherwise unchanged.

---

## New documentation partial

### `partials/_affiliate-shell.html` — NEW (not loaded at runtime)

Copy-paste reference markup for the affiliate top header + mobile bottom nav + desktop sidebar, mirroring the existing `partials/_*.html` style (with paste instructions). Authors copy this into each of the 6 affiliate pages so the shell stays identical.

---

## Link-integrity matrix (must all resolve)

| From | To |
|---|---|
| `login.html` (affiliate option) | `affiliate-dashboard.html` |
| `affiliates.html` (cross-link) | `affiliate-dashboard.html` |
| Every affiliate page bottom nav | `affiliate-dashboard.html`, `affiliate-dashboard.html#products`, `affiliate-saved-products.html`, `affiliate-orders.html`, `affiliate-earnings.html` |
| Every affiliate page desktop sidebar | the 5 above + `affiliate-profile.html` |
| Every affiliate page header avatar | `affiliate-profile.html` |
| Every product card `عرض التفاصيل` | `affiliate-product-detail.html` |
| Every section `عرض الكل` | `affiliate-dashboard.html#<anchor>` |
| Saved-products empty-state CTA | `affiliate-dashboard.html` |
| `affiliate-product-detail.html` back link | `affiliate-dashboard.html` |
| `affiliate-earnings.html` / `affiliate-profile.html` `طلب سحب` | opens `#payout-modal` (in-page) |

No affiliate-shell link may point to a non-existent file.
