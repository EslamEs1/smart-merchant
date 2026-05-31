# Smart Merchant OS — Static Frontend MVP

A premium Arabic-RTL SaaS merchant dashboard prototype built with HTML, TailwindCSS, and minimal vanilla JavaScript. No frameworks, no build step — open directly in a browser.

## How to Run

### 1. Double-click (zero setup)

Open the project folder in your file explorer and double-click `index.html`. The browser opens the marketing home page.

> **Note**: The **Copy Referral Link** button may silently fail on `file://` URLs in some browsers (Clipboard API requires a secure context). Use method 2 or 3 if this matters.

### 2. VS Code Live Server (recommended)

1. Install the **Live Server** extension by Ritwick Dey.
2. Open this folder in VS Code.
3. Right-click any `.html` file → **Open with Live Server**.
4. Browser opens at `http://127.0.0.1:5500/<page>.html` with hot reload.

### 3. Python static server

```bash
python3 -m http.server 8080
# then visit http://localhost:8080/index.html
```

Other alternatives: `npx http-server`, `php -S localhost:8080`, any static-file IDE preview.

---

## How to Demo This to a Client (connected merchant → affiliate walkthrough)

Run via Live Server or `python3 -m http.server` for the best experience (the copy buttons need a
secure context — see Troubleshooting). This path shows the merchant and the affiliate seller portal
as one connected product.

| Step | Action | What to show |
|------|--------|-------------|
| 1 | Open `login.html` | Login card with the role selector — **أنا تاجر** / **أنا مسوّق بالعمولة** |
| 2 | Choose **أنا تاجر** and submit | Routes to `dashboard.html` — stat cards, recent orders, top affiliates |
| 3 | Open **المسوّقون** (`affiliates.html`) | Affiliate roster; **أحمد الشمري** (Gold, code `AHMAD20`) sits at the top |
| 4 | Click **معاينة بوابة المسوّق ↗** | Opens `affiliate-dashboard.html` — the affiliate's own portal in a new tab |
| 5 | Browse the product grid | Physical catalog; try the favorite ♥ toggle, category tabs, and search |
| 6 | Click **عرض التفاصيل** on a product | `affiliate-product-detail.html` — image gallery, sale price, your commission |
| 7 | Click **نسخ الكابشن** | "تم النسخ ✓" toast — a ready-made marketing caption is copied |
| 8 | Open **الأرباح** (`affiliate-earnings.html`) | 1,420 available / 490 pending / 405 paid; rows correspond to order numbers (not DB-verified in this demo) |
| 9 | Click **طلب سحب** | Payout modal opens; close it via the button, **Esc**, or the backdrop |
| 10 | Open the avatar → **الملف الشخصي**, click **نسخ رابط الإحالة** | Referral link `…/r/AHMAD20` and coupon `AHMAD20` copied |

See `specs/003-backend-foundation/quickstart.md` (active branch),
`specs/002-affiliate-seller-portal/quickstart.md`, and
`specs/001-static-frontend-mvp/quickstart.md`
for the full per-user-story verification checklists.

---

## Constitution (non-negotiable rules)

| Rule | Detail |
|------|--------|
| No frameworks | No React, Vue, Next.js, Angular, Svelte |
| No build step | No bundler, no `npm run dev`, no `node_modules/`, no `package.json` |
| No API calls | All data is hardcoded HTML |
| RTL Arabic | Every page has `<html dir="rtl" lang="ar">` |
| Minimal JS | One file `assets/js/main.js` for sidebar/dropdowns/modals/tabs/theme/copy only |
| Theme persistence | Only `localStorage` key is `smos:theme` |

---

## Project Tree

```
smart-merchant/
├── index.html                   # Marketing home
├── features.html                # Features explainer
├── pricing.html                 # Three-plan pricing
├── login.html                   # Login form
├── register.html                # Registration form
│
├── dashboard.html               # Dashboard overview
├── products.html                # Product catalogue list
├── product-create.html          # New product form
├── product-edit.html            # Edit product form
├── product-detail.html          # Product detail + orders + affiliates
├── orders.html                  # Orders list with filters
├── order-detail.html            # Order detail with timeline + invoice
├── order-edit.html              # Order edit form
├── affiliates.html              # Affiliate roster (core differentiator)
├── affiliate-detail.html        # Profile + referral link + QR + payouts
├── affiliate-requests.html      # Pending affiliate applications
├── affiliate-payouts.html       # Payouts: Pending / Paid / Rejected
├── customers.html               # CRM list
├── customer-detail.html         # Customer profile + order history
├── customer-edit.html           # Customer edit form
├── landing-pages.html           # Landing page list
├── landing-page-create.html     # Landing page builder (form-driven)
├── landing-page-preview.html    # Public-facing preview
├── settings.html                # Settings tabs (6 sections)
├── profile.html                 # Profile form + password + danger zone
├── notifications.html           # Notifications inbox
├── analytics.html               # Coming soon placeholder
│
├── assets/
│   ├── css/app.css              # Custom utilities (focus-ring, table-responsive, badges)
│   ├── js/main.js               # Sidebar / dropdowns / modals / tabs / theme / copy
│   └── img/
│       ├── favicon.svg
│       ├── logo.svg
│       └── placeholders/
│           ├── avatar.svg
│           ├── affiliate-avatar.svg
│           ├── product.svg
│           ├── chart-line.svg
│           ├── chart-donut.svg
│           ├── dashboard-preview.svg
│           ├── hero-art.svg
│           ├── qr-code.svg
│           ├── template-hero-classic.svg
│           ├── template-bold-offer.svg
│           ├── template-story-driven.svg
│           └── template-minimal.svg
│
├── SAMPLE-DATA.md               # Canonical sample entities (products, affiliates, orders, customers)
├── README.md                    # This file
└── specs/
    └── 001-static-frontend-mvp/
        ├── spec.md
        ├── plan.md
        ├── research.md
        ├── data-model.md
        ├── quickstart.md
        ├── tasks.md
        └── contracts/
            └── pages.md
```

---

## Pages

### Public marketing

| File | Description |
|------|-------------|
| `index.html` | Home / marketing landing |
| `features.html` | Features explainer |
| `pricing.html` | Three-plan comparison |
| `login.html` | Login form |
| `register.html` | Registration form |

### Merchant dashboard

| File | Description |
|------|-------------|
| `dashboard.html` | Overview — stats, charts, recent orders, top affiliates |
| `products.html` | Product catalogue list |
| `product-create.html` | New product form |
| `product-edit.html` | Edit product form |
| `product-detail.html` | Product detail with related orders / top affiliates |
| `orders.html` | Orders list with filters |
| `order-detail.html` | Order detail with timeline and invoice preview |
| `order-edit.html` | Order edit form |
| `affiliates.html` | Affiliate roster (core differentiator) |
| `affiliate-detail.html` | Affiliate profile + referral link + QR + payout history |
| `affiliate-requests.html` | Pending applications queue |
| `affiliate-payouts.html` | Payouts queue (Pending / Paid / Rejected tabs) |
| `customers.html` | CRM list |
| `customer-detail.html` | Customer profile with order history |
| `customer-edit.html` | Customer edit form |
| `landing-pages.html` | Landing page list |
| `landing-page-create.html` | Landing page builder (form-driven) |
| `landing-page-preview.html` | Public-facing preview render |
| `settings.html` | Settings tabs (Business / Branding / Payment / Affiliate / Notifications / Security) |
| `profile.html` | Profile form + password change + danger zone |
| `notifications.html` | Notifications inbox (5 categories, filter chips) |
| `analytics.html` | Coming-soon placeholder with chart previews |

### Affiliate seller portal

A separate lightweight, mobile-first surface for affiliate sellers (feature `002`). It reuses the
same design tokens but has its own shell (collapsible sidebar on desktop, bottom nav on mobile).

| File | Description |
|------|-------------|
| `affiliate-dashboard.html` | Affiliate home — quick earnings, search, category tabs, product grid |
| `affiliate-product-detail.html` | Product detail — image gallery, your commission, copy caption / details |
| `affiliate-orders.html` | The affiliate's attributed orders (mobile cards + desktop table) |
| `affiliate-earnings.html` | Earnings ledger + payout-request modal |
| `affiliate-saved-products.html` | Saved / favorited products |
| `affiliate-profile.html` | Profile + referral link + coupon code |

> The merchant-side affiliate management pages (`affiliate-detail.html`, `affiliate-requests.html`,
> `affiliate-payouts.html`) are listed under **Merchant dashboard** above.

---

## Design Tokens at a Glance

### Brand colors

| Token | Light | Dark | Usage |
|-------|-------|------|-------|
| `brand-primary` | `#6366f1` (indigo-500) | `#818cf8` (indigo-400) | Primary buttons, active states |
| `brand-accent` | `#8b5cf6` (violet-500) | `#a78bfa` (violet-400) | Secondary highlights, gradient end-stop |
| `brand-info` | `#3b82f6` (blue-500) | `#60a5fa` (blue-400) | Info badges, links |
| `surface-base` | `#ffffff` | `#0f172a` (slate-900) | Page background |
| `surface-card` | `#f8fafc` (slate-50) | `#1e293b` (slate-800) | Card background |
| `surface-border` | `#e2e8f0` (slate-200) | `#334155` (slate-700) | Subtle borders |
| `text-primary` | `#0f172a` (slate-900) | `#f1f5f9` (slate-100) | Body text |
| `text-muted` | `#64748b` (slate-500) | `#94a3b8` (slate-400) | Captions, placeholders |

**Brand gradient**: `linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #3b82f6 100%)`  
Used for the logo glyph, hero backgrounds, stat card highlights, and CTA buttons.

### Status badge palette

| Status | Tone | Background | Text |
|--------|------|-----------|------|
| Pending / Unpaid / Not Shipped | amber | `bg-amber-100 dark:bg-amber-900/40` | `text-amber-800 dark:text-amber-200` |
| Confirmed / Processing / Preparing | blue | `bg-blue-100 dark:bg-blue-900/40` | `text-blue-800 dark:text-blue-200` |
| Shipped / Partially Paid | indigo | `bg-indigo-100 dark:bg-indigo-900/40` | `text-indigo-800 dark:text-indigo-200` |
| Delivered / Paid / Active | emerald | `bg-emerald-100 dark:bg-emerald-900/40` | `text-emerald-800 dark:text-emerald-200` |
| Cancelled / Rejected / Suspended | rose | `bg-rose-100 dark:bg-rose-900/40` | `text-rose-800 dark:text-rose-200` |
| Refunded / Returned | slate | `bg-slate-200 dark:bg-slate-700` | `text-slate-800 dark:text-slate-200` |
| Bronze (level) | amber | `bg-amber-200/70 dark:bg-amber-900/30` | `text-amber-900 dark:text-amber-300` |
| Silver (level) | slate | `bg-slate-300/60 dark:bg-slate-600/30` | `text-slate-800 dark:text-slate-200` |
| Gold (level) | yellow | `bg-yellow-200/70 dark:bg-yellow-900/30` | `text-yellow-900 dark:text-yellow-300` |
| Platinum (level) | violet | `bg-violet-200/70 dark:bg-violet-900/30` | `text-violet-900 dark:text-violet-300` |

### Typography & icons

- **Primary font**: Cairo (400/500/600/700/800) via Google Fonts CDN
- **Fallback font**: Tajawal (400/500/700) via Google Fonts CDN
- **Icons**: Lucide via unpkg CDN — `<i data-lucide="icon-name">` pattern, initialized with `lucide.createIcons()`
- **Theme**: Class-based dark mode (`darkMode: 'class'`), toggled by `data-theme-toggle` button, persisted as `localStorage['smos:theme']`

---

## Spec Artifacts

| Document | Path |
|----------|------|
| Specification | `specs/001-static-frontend-mvp/spec.md` |
| Implementation Plan | `specs/001-static-frontend-mvp/plan.md` |
| Research & Decisions | `specs/001-static-frontend-mvp/research.md` |
| Data Model | `specs/001-static-frontend-mvp/data-model.md` |
| Quickstart & Verification | `specs/001-static-frontend-mvp/quickstart.md` |
| Page Contracts | `specs/001-static-frontend-mvp/contracts/pages.md` |
| Task List | `specs/001-static-frontend-mvp/tasks.md` |

---

## Sample Data Reference

See `SAMPLE-DATA.md` for the canonical sample entities (products, affiliates, customers, orders) used across all pages.

---

## Troubleshooting

| Issue | Cause | Fix |
|-------|-------|-----|
| Theme toggle does nothing | `assets/js/main.js` missing or 404'd | Confirm file exists at exact path; check browser DevTools console |
| Icons render as `<i>` text, not SVGs | Lucide CDN failed to load OR `lucide.createIcons()` not called | Check Network tab for the Lucide script; ensure `main.js` calls `createIcons()` after DOMContentLoaded |
| Layout flips left-to-right on one page | `<html>` element missing `dir="rtl"` | Add `dir="rtl" lang="ar"` to that page's `<html>` tag |
| Copy Referral Link silently fails | Page opened via `file://` — Clipboard API restricted | Run via Live Server or `python3 -m http.server` |
| Tailwind utilities don't apply at all | Play CDN script blocked or 404'd | Check Network tab; ensure HTTPS connectivity to `cdn.tailwindcss.com` |
| Dark mode flashes light on load | Pre-paint inline theme script missing from `<head>` | The 5-line `localStorage` check must appear in `<head>` before any other content |
| Action dropdown stays open when clicking elsewhere | Click-outside handler missing | Implement document-click handler in `main.js` that closes any open `[data-dropdown-panel]` |
| Mobile sidebar doesn't open | JS targeting wrong element ID | `main.js` looks for `[data-sidebar]` or `#sidebar`; ensure the `<aside>` has one of those |
