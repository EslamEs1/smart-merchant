# Implementation Plan: Affiliate Seller Portal — Static Frontend

**Branch**: `002-affiliate-seller-portal` | **Date**: 2026-05-11 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/002-affiliate-seller-portal/spec.md`

## Summary

Add six static, framework-free, RTL-Arabic HTML pages that form a **separate, lightweight "affiliate seller" surface** distinct from the existing merchant admin shell: `affiliate-dashboard.html`, `affiliate-product-detail.html`, `affiliate-orders.html`, `affiliate-earnings.html`, `affiliate-saved-products.html`, `affiliate-profile.html`. The portal feels like a fast mobile selling app — product-first home, horizontal category tabs, small clean product cards, one-tap "copy caption / copy product details", a payout request modal, and a referral/level profile. It reuses the project's existing CDN stack (Tailwind Play CDN, Lucide, Cairo/Tajawal fonts), `assets/css/app.css`, and `assets/js/main.js` hook patterns (`[data-copy]`, `[data-modal-trigger]`, `[data-tab]`, `[data-theme-toggle]`), adding only a small, allow-list-compliant set of new behaviors (favorite toggle, image-gallery switch, category-tab active state, bottom-nav active state). A discoverable entry point is added (role selector on `login.html`) and the merchant `affiliates.html` view links across to the affiliate portal preview. No backend, no API calls, no bundler.

## Technical Context

**Language/Version**: HTML5, CSS3, ES2020+ vanilla JavaScript (no transpilation, no ES modules — classic `<script defer>` import only)
**Primary Dependencies**: TailwindCSS via CDN (Play CDN, JIT in-browser, shared `tailwind.config` from `partials/_head.html`), Lucide Icons via CDN (`<i data-lucide>` swap), Google Fonts CDN (Cairo primary, Tajawal fallback) — all over HTTPS, no local build
**Storage**: `localStorage` — only the existing `smos:theme` key (`"light"`/`"dark"`); no new persisted state (Constitution Principle VII). Favorite/saved state is in-DOM only, not persisted
**Testing**: Manual visual review against the Spec Quality Checklist and each user story's Independent Test; link-integrity verified by a one-off `grep` audit at acceptance time; no automated test framework (Constitution Principle I bans bundlers/`npm run dev`)
**Target Platform**: Latest two stable versions of Chrome, Firefox, Safari, Edge; viewports 320 px → 1920 px; opens via `file://` double-click or VS Code Live Server / any static file server
**Project Type**: Static web prototype — flat site at repo root, no client/server split, no `src/`
**Performance Goals**: First Contentful Paint ≤ 1.5 s on a throttled 3G profile from CDN-cached state; interactive widgets (copy, favorite, gallery switch, tab switch, modal open/close) respond within 100 ms of click; first mobile screen of `affiliate-dashboard.html` shows welcome + quick-earnings + search + category tabs + ≥1 product card within ~1.25 viewport heights at 375 px (SC-002)
**Constraints**: No frontend frameworks; no bundler / `node_modules` / `package.json`; no API calls or API simulation; no inline `<script>` blocks beyond the existing pre-paint theme line, the Lucide CDN tag, and a single `<script src="assets/js/main.js" defer>`; AA-equivalent contrast (≥ 4.5:1 body, ≥ 3:1 large text/UI) in both themes; RTL by default; no full customer PII in orders/earnings views (mask names/phones)
**Scale/Scope**: 6 new HTML pages (~500–1,100 lines each incl. hardcoded sample data); extends `assets/js/main.js` by ~80–140 lines (favorite toggle, gallery switch, segmented category tabs, bottom-nav active highlighting) and `assets/css/app.css` by ~80–150 lines (bottom-nav, product card, affiliate-level chips already exist, segmented tabs, earnings/commission badge tones reuse existing `.badge-*`); 1 new contract doc; minor edits to `login.html` and `affiliates.html` for the entry point

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

Evaluation against `.specify/memory/constitution.md` v1.0.0:

| Principle | Gate | Outcome |
|---|---|---|
| I. Static Frontend Only (NON-NEGOTIABLE) | Only HTML/CSS/Tailwind-CDN/vanilla JS; no React/Vue/Next/Angular/Svelte; no bundler; no `npm run dev`; no API fetches or mocks | **PASS** |
| II. Hardcoded, Client-Presentable Pages | Every affiliate page ships fully populated with realistic hardcoded data (≥12 product cards across the dashboard sections, ≥10 orders, ≥10 earnings rows, full profile); the saved-products empty state ships as styled markup *in addition to* a populated grid | **PASS** |
| III. RTL Arabic First | Every new page sets `dir="rtl" lang="ar"`; Arabic across nav, headings, labels, copy; English only for status tokens (Pending/Confirmed/Processing/Delivered/Cancelled/Approved/Paid/Rejected) and level names (Bronze/Silver/Gold/Platinum); Tailwind logical-property utilities (`ms-`/`me-`/`ps-`/`pe-`) for spacing | **PASS** |
| IV. Premium SaaS Visual Language | Reuses brand tokens (`brand-primary`/`brand-accent`/`brand-info`, `bg-gradient-brand`), rounded-2xl soft cards, shadow-sm/md, Cairo type, dark/light parity; new CSS limited to small reusable touches (bottom-nav, product-card, segmented tabs) Tailwind can't express cleanly | **PASS** |
| V. Affiliate System As First-Class Differentiator | This feature *is* the affiliate experience taken end-to-end from the affiliate's own side; referral link + QR placeholder + coupon + commission state + the commission-approval rule notice are all surfaced and copyable; the merchant-side affiliate pages remain unchanged and are cross-linked | **PASS** |
| VI. Consistent Dashboard Shell | The affiliate portal is intentionally a **separate surface**, not a merchant dashboard page — the brief explicitly requires a lightweight layout different from the merchant admin shell. It does NOT alter the merchant shell or its sidebar order. The affiliate shell is itself internally consistent across all 6 affiliate pages (same top header + bottom nav + optional desktop sidebar). Recorded in Complexity Tracking as a scoped, user-mandated divergence. | **PASS (scoped divergence — see Complexity Tracking)** |
| VII. Minimal Vanilla JS Discipline | New JS strictly within the spirit of the allow-list: copy-to-clipboard (reuses `[data-copy]`), modals (reuses `[data-modal-*]`), tabs (reuses `[data-tab]` for category tabs / segmented filters), theme toggle (reuses `[data-theme-toggle]`); the only genuinely new behaviors are favorite toggle and image-gallery thumbnail switch — both pure DOM class toggles, no state mgmt, no routing, no API mock, no new `localStorage` key | **PASS** |

**Result**: All gates PASS. One scoped divergence (Principle VI) is user-mandated by the spec brief and recorded below; it adds a sibling surface without modifying the governed merchant shell, so it does not violate the principle's intent.

### Post-Design Re-evaluation (after Phase 1)

After producing `research.md`, `data-model.md`, `contracts/affiliate-pages.md`, and `quickstart.md`, all seven principles were re-checked against every design decision:

| Principle | Post-design check | Outcome |
|---|---|---|
| I. Static Frontend Only | `research.md` §1 reaffirms Tailwind Play CDN + Lucide CDN (no build); §3 the new JS additions are listed and bounded; no framework, no fetch. | **PASS** |
| II. Hardcoded data | `data-model.md` fixes per-section product counts, ≥10 orders, ≥10 earnings rows, full affiliate profile; `contracts/affiliate-pages.md` requires populated content + the empty-state markup alongside. | **PASS** |
| III. RTL Arabic First | `research.md` §2 commits to `dir="rtl"` + logical-property utilities; the bottom-nav and segmented-tabs CSS use logical insets. | **PASS** |
| IV. Premium SaaS Visual | `research.md` §4 locks the affiliate-shell palette (white + subtle brand-tinted gradients), product-card spec, and badge-tone reuse. | **PASS** |
| V. Affiliate First-Class | `contracts/affiliate-pages.md` gives the product-detail page the richest treatment (all selling assets); the commission-approval notice is mandated on the earnings page; referral/QR/coupon mandated on the profile page. | **PASS** |
| VI. Consistent Shell | `contracts/affiliate-pages.md` defines a single "Affiliate shell" section applied to all 6 pages; the merchant shell contract in `001`'s `contracts/pages.md` is untouched. | **PASS (scoped divergence as above)** |
| VII. Minimal JS | `research.md` §3 enumerates exactly the added handlers; only `smos:theme` is persisted; allowed `<script>` blocks per page unchanged from the project baseline. | **PASS** |

**Post-design result**: All gates STILL PASS. No new deviations introduced during Phase 1.

## Project Structure

### Documentation (this feature)

```text
specs/002-affiliate-seller-portal/
├── plan.md                    # This file (/speckit-plan command output)
├── research.md                # Phase 0 — shell design, CDN reuse, JS additions, sample-data plan
├── data-model.md              # Phase 1 — entity schemas authors use to write the hardcoded data
├── quickstart.md              # Phase 1 — how to open and verify the affiliate portal
├── contracts/
│   └── affiliate-pages.md     # Phase 1 — page-level contract (file → required content shape + JS hooks + inbound links)
├── checklists/
│   └── requirements.md        # Spec quality checklist (passing)
├── spec.md                    # Feature spec
└── tasks.md                   # Phase 2 — created by /speckit-tasks, not /speckit-plan
```

### Source Code (repository root)

The prototype stays a flat static site at the repo root — no `src/`, no build output. This feature adds six HTML files and extends two shared asset files; it edits two existing pages for the entry point.

```text
.
├── affiliate-dashboard.html        # NEW — product-first home (welcome, quick-earnings, search, category tabs, 4 product sections)
├── affiliate-product-detail.html   # NEW — gallery + video placeholder + pricing card + quick actions + caption box + details box + tips + related
├── affiliate-orders.html           # NEW — 4 summary cards + filter bar + orders (cards on mobile / table on desktop, masked customer)
├── affiliate-earnings.html         # NEW — main payout card + 3 stat cards + commission-rule notice + earnings history + payout modal
├── affiliate-saved-products.html   # NEW — header + search + product-card grid + empty-state markup
├── affiliate-profile.html          # NEW — profile card + level badge + referral box + QR placeholder + coupon + info form + payment + status
│
├── login.html                      # EDIT — add an affiliate/merchant role selector linking to affiliate-dashboard.html (entry point)
├── affiliates.html                 # EDIT — add a "معاينة بوابة المسوّق" cross-link to affiliate-dashboard.html
│
├── assets/
│   ├── css/app.css                 # EDIT — append: .affiliate-bottom-nav, .product-card, .segmented-tabs, .empty-state touches (badge tones reused)
│   ├── js/main.js                  # EDIT — append: initFavoriteToggle(), initGallery(), initSegmentedTabs() (category/order filters), initBottomNavActive(); register in boot
│   └── img/placeholders/           # REUSE — product.svg, affiliate-avatar.svg, qr-code.svg, chart-line.svg, chart-donut.svg (no new assets required)
│
└── partials/
    └── _affiliate-shell.html       # NEW (optional doc partial) — copy-paste reference for the affiliate top header + bottom nav + desktop sidebar
```

**Structure Decision**: Single flat static-site project at the repo root (same as feature `001`). No new directories; six new top-level HTML pages plus appends to the two shared asset files and one optional documentation partial. The affiliate portal is a sibling surface to the merchant dashboard, not a sub-app.

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| Separate "affiliate shell" alongside the merchant dashboard shell (deviates from Constitution Principle VI's single-shell expectation) | The feature brief explicitly requires "a lightweight affiliate layout different from the merchant admin dashboard" with mobile bottom navigation — the whole product point is that an affiliate gets a fast selling app, not the admin console | Reusing the merchant shell (fixed admin sidebar, merchant nav order, no bottom nav) would directly contradict the brief's UX requirements and the "feels faster/cleaner than traditional reseller platforms" success criterion. The divergence is scoped: it adds a new shell used only by the 6 affiliate pages and changes nothing about the merchant shell, so Principle VI's stated concern (drift *within* the merchant dashboard) is unaffected. |
