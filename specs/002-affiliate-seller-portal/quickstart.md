# Quickstart: Affiliate Seller Portal — Static Frontend

**Feature**: 002-affiliate-seller-portal
**Date**: 2026-05-11

## What this is

Six static HTML pages forming a lightweight "affiliate seller" app inside the Smart Merchant OS prototype. No backend, no build, no framework — just open the files.

## Run it

Option A — double-click:

```text
Open affiliate-dashboard.html in a browser (Chrome/Firefox/Safari/Edge).
```

Option B — Live Server (recommended; clipboard APIs behave better over `http://`):

```text
VS Code → right-click affiliate-dashboard.html → "Open with Live Server"
# or any static server, e.g.:
python3 -m http.server 5500   # then visit http://localhost:5500/affiliate-dashboard.html
```

Entry points within the prototype:

- `login.html` → choose "أنا مسوّق بالعمولة" → lands on `affiliate-dashboard.html`
- `affiliates.html` (merchant view) → "معاينة بوابة المسوّق ↗" → `affiliate-dashboard.html`

## The pages

| File | What you see |
|---|---|
| `affiliate-dashboard.html` | Welcome ("أهلاً يا أحمد 👋"), gradient quick-earnings card, search, horizontal category tabs, 4 product sections (الأكثر مبيعًا / عروض قوية اليوم / منتجات جديدة / ربح عالي) of small product cards |
| `affiliate-product-detail.html` | Image gallery + video placeholder, pricing card (سعر المورد / سعر البيع المقترح / صافي ربحك), 6 quick-action buttons, ready caption box + product details box (each with a copy button), selling tips, related products |
| `affiliate-orders.html` | 4 summary cards (كل الطلبات / قيد التنفيذ / تم التسليم / ملغية), status filter chips + search, orders as cards on mobile / table on desktop, masked customers |
| `affiliate-earnings.html` | Main payout card ("الأرباح المتاحة للسحب" + "طلب سحب"), 3 stat cards, the commission notice, earnings history, payout request modal |
| `affiliate-saved-products.html` | Header + search + grid of saved product cards (same card as the dashboard) + an empty-state block |
| `affiliate-profile.html` | Profile card + Gold level badge, referral link box (copy), QR placeholder, coupon code (copy), basic info form, payment method + "طلب سحب", account status |

## Verify it (manual acceptance — maps to spec Success Criteria & User Stories)

**Shell (every affiliate page)**

- [ ] `dir="rtl" lang="ar"`; Arabic copy throughout; status tokens (Pending/…/Cancelled, Approved/Paid/Rejected) and level names (Bronze/Silver/Gold/Platinum) may stay English.
- [ ] Top header shows: avatar (→ profile), name "أحمد", "متاح للسحب: 1,420 ر.س" pill, a search input, a notification bell (opens a dropdown), a theme toggle.
- [ ] Mobile (≤ ~1024 px): a fixed bottom nav with exactly الرئيسية / المنتجات / المحفوظات / الطلبات / الأرباح; the current page's item is highlighted; content isn't covered by the bar.
- [ ] Desktop (≥ 1024 px): the bottom nav is hidden and a simple sidebar (same items + الملف الشخصي) is shown; they never appear together.
- [ ] No dead links anywhere in nav/header/CTAs (run `grep -oE 'href="affiliate-[a-z-]+\.html' *.html | sort -u` and confirm each target file exists).
- [ ] Theme toggle flips dark/light and persists on reload (only `localStorage` key is `smos:theme`).

**US1 — browse & grab assets (P1)**

- [ ] On a 375 px viewport, `affiliate-dashboard.html` shows the welcome line, quick-earnings card, search, category tabs, and ≥1 full product card within ~1.25 screen heights (SC-002).
- [ ] Tapping a category tab moves the active state; other tabs deactivate (visual only).
- [ ] All 4 product sections render with a "عرض الكل" link and a row/grid of cards.
- [ ] Each product card shows ONLY: image, optional badge (Bestseller/New/Hot Offer), name, suggested selling price, expected profit, favorite heart, "عرض التفاصيل" — no descriptions.
- [ ] "عرض التفاصيل" → `affiliate-product-detail.html`.
- [ ] On the detail page: "نسخ الكابشن" and "نسخ تفاصيل المنتج" copy text and show the "تم النسخ ✓" toast; a gallery thumbnail click switches the main image; the favorite heart toggles filled/outline (SC-001, SC-004).

**US2 — my orders (P2)**

- [ ] 4 summary cards with counts that add up.
- [ ] Mobile: orders are cards, not a horizontally-scrolling table. Desktop: a table.
- [ ] Each order: number, **masked** customer (name or phone — never full PII, never email), product, status badge (Cancelled is visibly distinct), commission with currency, date (SC-005, SC-006).
- [ ] Filter chips / search respond visually.

**US3 — earnings & payout (P2)**

- [ ] Prominent main card: "الأرباح المتاحة للسحب" + amount + "طلب سحب".
- [ ] 3 cards: إجمالي الأرباح / أرباح قيد المراجعة / أرباح مدفوعة (internally coherent figures).
- [ ] The notice "يتم اعتماد العمولة بعد تأكيد الدفع أو تسليم الطلب." is visible.
- [ ] Earnings history: each row has product, order number, commission, status (Pending/Approved/Paid/Rejected — Rejected distinct), date.
- [ ] "طلب سحب" opens a modal with amount / payment method / wallet-or-account / notes; ESC, the close button, and a backdrop click all dismiss it; focus returns to the page (SC-004).

**US4 — saved products (P3)**

- [ ] Header + search + a grid of product cards using the dashboard card design; their hearts start filled.
- [ ] An empty-state block exists with a message and a CTA → `affiliate-dashboard.html`.
- [ ] Heart toggle works on the cards.

**US5 — profile / referral (P3)**

- [ ] Profile card with name, avatar, and a level badge (one of Bronze/Silver/Gold/Platinum).
- [ ] Referral-link copy button and coupon-code copy button each copy and show the toast (SC-004).
- [ ] QR placeholder, basic info form, payment method info, account status all present.
- [ ] Theme toggle works here too; if the payout modal is surfaced here it opens/closes correctly.

**General**

- [ ] Every image has an `alt`; interactive elements have visible focus rings; tab order is logical.
- [ ] No API calls / no `fetch` / no network requests for app data; opens fine via `file://` and via Live Server (SC-008).
- [ ] Sample data follows `SAMPLE-DATA.md` (SAR-majority currency mix with consistent currency per row; ~80% Arabic names; persona "أحمد الشمري", Gold).

## Files touched by this feature

- **New**: `affiliate-dashboard.html`, `affiliate-product-detail.html`, `affiliate-orders.html`, `affiliate-earnings.html`, `affiliate-saved-products.html`, `affiliate-profile.html`, `partials/_affiliate-shell.html`
- **Edited (additive)**: `login.html` (role selector → affiliate portal), `affiliates.html` (cross-link), `assets/css/app.css` (append: bottom-nav, product-card, segmented-tabs, card-badge tones), `assets/js/main.js` (append: favorite toggle, gallery switch, segmented tabs, bottom-nav active state — registered in the existing `DOMContentLoaded` boot)
- **Reused as-is**: `partials/_head.html`, `assets/img/placeholders/{product,affiliate-avatar,qr-code,chart-line,chart-donut,dashboard-preview}.svg`, the existing `main.js` hooks (`[data-copy]`, `[data-modal-*]`, `[data-tab]`, `[data-actions-dropdown]`, `[data-theme-toggle]`)
