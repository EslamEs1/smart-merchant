# Research: Affiliate Seller Portal — Static Frontend

**Feature**: 002-affiliate-seller-portal
**Date**: 2026-05-11
**Purpose**: Resolve every "NEEDS CLARIFICATION" implied by the spec/plan and lock the design decisions the page authors will follow. Format per decision: **Decision / Rationale / Alternatives considered**.

There were no open `[NEEDS CLARIFICATION]` markers in `spec.md`; the items below are the design choices that the plan's Technical Context deliberately deferred to here.

---

## §1. Tech stack & loading strategy

**Decision**: Reuse the exact CDN stack already used by the rest of the prototype — Tailwind Play CDN (with the shared `tailwind.config` block from `partials/_head.html`, including `darkMode: 'class'`, `brand-primary/#6366f1`, `brand-accent/#8b5cf6`, `brand-info/#3b82f6`, `font-sans: Cairo,Tajawal`, and `bg-gradient-brand`), Lucide Icons via `https://unpkg.com/lucide@latest` with `<i data-lucide="…">` placeholders converted by `lucide.createIcons()` from `main.js`, Google Fonts (Cairo 400–800, Tajawal 400/500/700), `assets/css/app.css`, and a single deferred `assets/js/main.js`. Each affiliate page pastes the `partials/_head.html` block verbatim (only `<title>` changed) so the design tokens stay identical.

**Rationale**: Constitution Principle I forbids bundlers/builds; Principle IV requires visual consistency. Reusing the established head block guarantees both with zero new dependencies.

**Alternatives considered**: (a) A standalone Tailwind build for just the affiliate pages — rejected, introduces a build step. (b) A separate lighter CSS file with no Tailwind — rejected, breaks token consistency and duplicates utility logic. (c) Inlining a custom icon set — rejected, Lucide is already wired and consistent.

---

## §2. RTL & responsive strategy

**Decision**: Every affiliate page is `<html lang="ar" dir="rtl">`. All directional spacing uses Tailwind logical-property utilities (`ms-*`, `me-*`, `ps-*`, `pe-*`, `start-*`, `end-*`, `text-start/end`) — never `ml/mr/pl/pr/left/right`. New CSS for the bottom nav and segmented tabs uses logical CSS (`inset-inline`, `padding-inline`, `border-inline-start`). Mobile-first: base styles target ~375 px; `sm:`/`md:`/`lg:`/`xl:` add tablet/desktop refinements. The mobile bottom navigation is `fixed bottom-0 inset-x-0` and hidden at `lg:` (`lg:hidden`); the optional desktop sidebar is hidden below `lg:` (`hidden lg:flex`). Page `<main>` gets `pb-24 lg:pb-8` so the fixed bottom nav never overlaps content (Edge Case).

**Rationale**: The brief is "mobile-first" and "Arabic RTL by default"; logical properties are the only way to keep one set of utilities correct in RTL. Matches the approach already used project-wide (`001` research §2).

**Alternatives considered**: Physical-property utilities with manual RTL overrides in `app.css` — rejected, error-prone and against the existing convention.

---

## §3. JavaScript additions (allow-list compliance)

**Decision**: Extend `assets/js/main.js` with four small functions, all pure DOM-class toggles, registered in the existing `DOMContentLoaded` boot sequence:

1. **`initFavoriteToggle()`** — delegated click on `[data-favorite-toggle]`; toggles a `is-favorited` class on the button and swaps the Lucide icon between `heart` (outline) and a filled state (CSS `fill-current text-rose-500` when `.is-favorited`); also flips `aria-pressed`. Used on dashboard cards, saved-products cards, related-products cards, and the product-detail page. No persistence.
2. **`initGallery()`** — delegated click on `[data-gallery-thumb]` inside `[data-gallery]`; sets the main `<img data-gallery-main>`'s `src`/`alt` from the clicked thumb's `data-src`/`data-alt`; moves an `is-active` ring class among thumbs.
3. **`initSegmentedTabs()`** — delegated click on `[data-segment]` inside `[data-segments="<group>"]`; moves `is-active` among the segment buttons in the group and updates `aria-selected`. Used for the dashboard category tabs and the orders status filter. (This is the existing `[data-tab]` pattern generalized to a "segmented control" visual; if `[data-tab]` panels are desired, the existing `initTabs()` already covers panel show/hide — no change needed there.)
4. **`initBottomNavActive()`** — on load, compares `location.pathname`'s basename to each `[data-bottom-nav] a[data-nav-target]`'s `data-nav-target`; adds `is-active` to the match. (Alternatively each page hardcodes the active item — both are acceptable; the helper keeps markup identical across pages.)

Everything else reuses existing hooks: `[data-copy]` + `[data-copy-container]`/`[data-copy-value]` for the caption box, product-details box, referral link, and coupon code (`initCopy()` already shows the `#copied-toast` "تم النسخ ✓"); `[data-modal-trigger="payout-modal"]` / `[data-modal="payout-modal"]` / `[data-modal-close]` for the payout request modal and the optional product-detail modal (`initModals()` already handles backdrop click + ESC + focus trap + focus restore); `[data-theme-toggle]` for dark/light; `[data-actions-dropdown]` for the header profile menu / notifications.

**Rationale**: Constitution Principle VII allows copy-to-clipboard, modals, tabs, theme toggle, and "simple visual" toggles; favorite toggle and gallery switch are exactly that class of UI affordance the static HTML can't express alone. No routing, no state management, no API mock, no new `localStorage` key.

**Alternatives considered**: (a) Per-page inline `<script>` for these toggles — rejected, Constitution forbids extra inline scripts and it would duplicate logic. (b) A separate `affiliate.js` file — rejected, the project standard is one shared `main.js`; appending keeps the single-file discipline.

---

## §4. Visual design — the affiliate shell & product card

**Decision**:

- **Palette / surfaces**: Predominantly white (`bg-white dark:bg-slate-950`) with *subtle* gradients only as accents — e.g., the quick-earnings card and the main payout card use `bg-gradient-brand` (indigo→violet→blue) with white text; page background uses a very faint top gradient (`bg-gradient-to-b from-indigo-50/40 to-white dark:from-slate-900 dark:to-slate-950`). Soft cards: `rounded-2xl border border-slate-200 dark:border-slate-800 shadow-sm`. No heavy borders, no dense data grids on the home screen.
- **Top header (all pages)**: sticky, white/blur (`sticky top-0 z-30 bg-white/80 dark:bg-slate-950/80 backdrop-blur border-b border-slate-200/70`); contains, in RTL order: profile avatar (`assets/img/placeholders/affiliate-avatar.svg`, 36–40 px, rounded-full) + affiliate name "أحمد" + a small "متاح للسحب: 1,420 ر.س" earnings pill; center/inline a search input (`ابحث عن منتج للبيع...` on the dashboard, generic elsewhere); a notification bell `[data-actions-dropdown]` icon button with a dot; on `lg:` the search widens and a "بوابة المسوّق" wordmark sits at the start.
- **Bottom navigation (mobile, `lg:hidden`)**: `fixed bottom-0 inset-x-0 z-30` bar, white with top border and `shadow-[0_-1px_3px_rgba(0,0,0,0.06)]`; 5 equal items, each an icon + 11px label, active item gets `text-brand-primary` + a small filled pill behind the icon; items & icons & targets:
  - الرئيسية → `affiliate-dashboard.html` (icon `home`)
  - المنتجات → `affiliate-dashboard.html#products` (icon `shopping-bag`) — there is no separate "all products" page in scope, so this anchors to the dashboard's product sections; documented in the contract
  - المحفوظات → `affiliate-saved-products.html` (icon `bookmark`)
  - الطلبات → `affiliate-orders.html` (icon `package`)
  - الأرباح → `affiliate-earnings.html` (icon `wallet`)
- **Desktop sidebar (optional, `hidden lg:flex`)**: a narrow (`w-64`) left rail (visually at the *end* in RTL — i.e., `dir=rtl` puts it on the right; that is correct and intentional, matching Arabic reading) with the same 5 entries as vertical items plus a "الملف الشخصي" entry → `affiliate-profile.html`; same active-state treatment. When shown, the bottom nav is hidden.
- **Product card** (the single most reused component — identical on dashboard, saved-products, related-products): a `rounded-2xl border shadow-sm overflow-hidden` card, max ~170–200 px wide in horizontal scrollers / fluid in grids; top: 1:1 product image (`assets/img/placeholders/product.svg`, `object-cover`, `alt` = product name) with an absolutely-positioned badge top-start (`Bestseller` / `New` / `Hot Offer` → small pill, tones below) and a favorite heart button top-end (`[data-favorite-toggle]`); body (`p-3 space-y-1`): product name (`text-sm font-semibold line-clamp-2`), a "سعر البيع: 280 ر.س" line (`text-xs text-slate-500`), an "أرباحك: 45 ر.س" line emphasized (`text-sm font-bold text-emerald-600`); footer: a full-width `عرض التفاصيل` button (`bg-brand-primary text-white rounded-xl py-1.5 text-xs`) → `affiliate-product-detail.html`. Nothing else — no description, no rating, no stock.
- **Card badge tones** (new small classes in `app.css`, mirroring the existing `.badge` system): `.badge-bestseller { background:#fef3c7; color:#92400e; }`, `.badge-new { background:#d1fae5; color:#065f46; }`, `.badge-hot { background:#ffe4e6; color:#9f1239; }` plus `.dark` variants matching the existing pattern.
- **Status badges** (orders & earnings): reuse existing `.badge` classes — `Pending → .badge-pending`, `Confirmed → .badge-confirmed`, `Processing → .badge-processing`, `Delivered → .badge-delivered`, `Cancelled → .badge-cancelled`; for earnings `Approved → .badge-confirmed` (blue), `Paid → .badge-paid` (green), `Rejected → .badge-rejected` (rose). Cancelled/Rejected are visually distinct (rose) per the Edge Cases.
- **Affiliate level chips**: reuse existing `.badge-bronze/.badge-silver/.badge-gold/.badge-platinum`.
- **Typography & spacing**: Cairo; generous whitespace; section headings `text-base font-bold` with a `عرض الكل` link (`text-xs text-brand-primary`) on the opposite end; Apple-like breathing room (`gap-4`, `py-6` between sections).

**Rationale**: Directly encodes the brief's design language ("minimal, premium, clean, fast, soft cards, rounded corners, white background with subtle gradients, no clutter, modern affiliate platform look") and the visual-priority order (image → expected profit → details button → selling tools). Reusing `.badge-*` keeps order/earnings statuses consistent with the merchant side.

**Alternatives considered**: (a) Bigger e-commerce-style product cards with descriptions and ratings — explicitly rejected by the brief ("must not look like a crowded ecommerce store", "no long descriptions inside product cards"). (b) Reusing the merchant sidebar/header — rejected per the brief and recorded in plan Complexity Tracking. (c) Heavy gradient backgrounds — rejected, brief says *subtle*.

---

## §5. Persisted state

**Decision**: The only persisted state remains `localStorage['smos:theme']` (`"light"`/`"dark"`), managed by the existing pre-paint script in `_head.html` and `initTheme()` in `main.js`. Favorite/saved toggles, the active category tab, and the active order filter are **in-DOM only** and reset on reload. The saved-products page is hand-authored with a fixed set of "saved" products.

**Rationale**: Constitution Principle VII permits `localStorage` *only* for theme. Persisting favorites would cross into state management.

**Alternatives considered**: Persisting favorites in `localStorage` so they survive reload and appear on the saved page — rejected on Constitution grounds; the static prototype simulates this with hand-authored data instead.

---

## §6. Sample-data plan (hardcoded content)

**Decision**: Follow `SAMPLE-DATA.md` conventions — currency mix SAR-majority (~50%), then EGP (~25%), AED (~20%), occasional KWD/BHD/QAR; *consistent currency within a single row/entity*; names ~80% Arabic-script, ~20% Latin-script; the logged-in affiliate is **أحمد الشمري**, Gold level, code `AHMAD20`, available balance ≈ `1,420 ر.س`, consistent with `AFF-001`.

- **Products** (≥16 distinct products defined once, reused across the 4 dashboard sections, the saved page, related-products, and as the subject of the detail page): cover the brief's categories (الأكثر مبيعًا / عروض / إلكترونيات / ملابس / أدوات منزلية / إكسسوارات), each with name, image (`product.svg`), optional badge, supplier price (سعر المورد), suggested price (سعر البيع المقترح), affiliate profit (صافي ربحك ≈ 15–25% of suggested), a ready caption (2–4 lines, emoji, hashtags), a ready details block (bullet specs), 2–3 selling tips, and 2 video-thumbnail placeholders. Section assignment: الأكثر مبيعًا (5 cards), عروض قوية اليوم (5 cards, all with `Hot Offer` badge + a strikethrough "كان"), منتجات جديدة (5 cards, `New` badge), ربح عالي (5 cards, profit ≥ 60). The detail page features one representative product fully populated; its "related products" block shows 4 cards from the same category.
- **Orders** (≥12 rows, current affiliate only): order number (`AO-2026-0xxx`), masked customer (`أحمد ا***` style for names, `055•• ••• 41` style for phones — mix of the two), product name, status across all five values (skewed: ~4 Delivered, ~3 Processing/Confirmed, ~2 Pending, ~2 Cancelled), commission with currency (consistent per row), date (recent, 2026-04 → 2026-05). Summary cards: كل الطلبات = total, قيد التنفيذ = Pending+Confirmed+Processing, تم التسليم = Delivered, ملغية = Cancelled — numbers must add up.
- **Earnings** (≥12 rows): product, order number (cross-referencing the orders list where sensible), commission with currency, status across Pending/Approved/Paid/Rejected (skewed: ~4 Paid, ~4 Approved, ~3 Pending, ~1 Rejected), date. Cards: الأرباح المتاحة للسحب ≈ `1,420 ر.س` (= sum of Approved), إجمالي الأرباح ≈ sum of all non-rejected, أرباح قيد المراجعة ≈ sum of Pending, أرباح مدفوعة ≈ sum of Paid — numbers must be internally coherent.
- **Profile**: name أحمد الشمري, avatar `affiliate-avatar.svg`, level Gold, referral link `https://smartmerchant.os/r/AHMAD20`, coupon `AHMAD20`, QR placeholder `qr-code.svg`, account status `Active` (`.badge-active`), payment method "محفظة STC Pay — 0555•••41", basic info form (الاسم, البريد, الجوال masked, المدينة, الدولة) pre-filled, "تعديل المعلومات" save button (no-op).

**Rationale**: Constitution Principle II requires every page to look complete with realistic data; cross-page consistency is mandated by `SAMPLE-DATA.md`. Internally-coherent totals make the prototype credible in a demo.

**Alternatives considered**: A single shared JS data array rendered into the DOM — rejected; Constitution Principle I/II favor literally hardcoded HTML, and a JS-render approach edges toward an SPA pattern. Each page hardcodes its rows.

---

## §7. Entry point / discoverability

**Decision**: Add a small "أنا مسوّق بالعمولة" / "أنا تاجر" role toggle on `login.html` whose affiliate option's submit links to `affiliate-dashboard.html` (the merchant option keeps linking to `dashboard.html`); additionally add a "معاينة بوابة المسوّق ↗" link on the merchant `affiliates.html` page header pointing to `affiliate-dashboard.html`. Both are minimal, additive edits — no change to existing content, no removed sections.

**Rationale**: FR-075 requires the portal to be reachable from the existing prototype; the constitution forbids dead links and orphan pages. The login role toggle is the natural place; the merchant cross-link aids demoing both sides.

**Alternatives considered**: A new public nav link — rejected, the affiliate portal is "post-login" conceptually and a public nav entry would clutter the marketing nav. Leaving the pages unlinked — rejected, violates FR-075 and the constitution's link-integrity gate.

---

## §8. Accessibility scope

**Decision**: Inherit `001`'s scope — visible focus rings on all interactive elements (`focus-visible` ring from `app.css`), logical tab order, ESC dismissal on the payout modal / optional product modal (already in `initModals()`), `alt` on every image (placeholder or not), AA-equivalent contrast in both themes, `aria-pressed` on favorite buttons, `aria-selected` on segment/tab buttons, `aria-current="page"` on the active bottom-nav item, and `aria-live="polite"` on the copy toast (already present). No formal WCAG audit, no ARIA-rich landmark scaffolding beyond `<header>`/`<main>`/`<nav>`.

**Rationale**: Consistency with the established project a11y baseline (`001` clarifications) and FR-073.

**Alternatives considered**: Full WCAG 2.1 AA certification — out of scope for a static prototype, same as `001`.

---

## Resolved unknowns summary

| Topic | Resolution |
|---|---|
| CSS/JS stack | Reuse Tailwind Play CDN + Lucide + Cairo/Tajawal + `app.css` + `main.js`; paste `partials/_head.html` verbatim |
| New JS | 4 small functions appended to `main.js`: favorite toggle, gallery switch, segmented tabs, bottom-nav active state |
| Affiliate shell | New lightweight shell: sticky top header (avatar+name+earnings pill+search+bell) + fixed mobile bottom nav (5 items) + optional `lg:` desktop sidebar; documented in `contracts/affiliate-pages.md` and `partials/_affiliate-shell.html` |
| Product card | Image + optional badge + name + suggested price + affiliate profit + favorite heart + "عرض التفاصيل" — nothing else |
| Persisted state | Only `smos:theme`; favorites are in-DOM |
| Sample data | ≥16 products, ≥12 orders, ≥12 earnings rows, full أحمد الشمري / Gold / AHMAD20 profile; SAR-majority currency, ~80% Arabic names; internally-coherent totals |
| Entry point | Role toggle on `login.html` → `affiliate-dashboard.html`; cross-link on `affiliates.html` |
| "المنتجات" bottom-nav target | `affiliate-dashboard.html#products` (no standalone all-products page in scope) |
| Downloads / WhatsApp / order actions | Visual affordances — `download` attr on a placeholder asset and a `wa.me` link are acceptable; "طلب أوردر" opens a simple confirm-style modal or links to a placeholder; no real backend |
| a11y | Inherit `001` baseline: focus rings, tab order, ESC on modals, `alt` everywhere, AA contrast, `aria-pressed`/`aria-selected`/`aria-current` |
