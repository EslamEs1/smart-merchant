# Implementation Plan: Smart Merchant OS — Static Frontend MVP

**Branch**: `001-static-frontend-mvp` | **Date**: 2026-05-10 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-static-frontend-mvp/spec.md`

## Summary

Build a static, framework-free, RTL-Arabic, premium-SaaS prototype consisting of
~30 hand-authored HTML pages covering public marketing (home, features, pricing,
login, register), the merchant dashboard shell, and full CRUD-style flows for
products, orders, affiliates, customers, and landing pages — plus settings,
profile, and notifications. All data is hardcoded; the affiliate system is
visually central per Constitution Principle V; the only persisted state is the
dark/light theme preference (Principle VII). The technical approach is to
deliver each page as an independent self-contained HTML document that imports
TailwindCSS and Lucide icons via CDN and shares one `assets/js/main.js` bundle
for the limited interactivity allow-list (sidebar toggle, dropdowns, modals,
tabs, copy referral link, theme toggle).

## Technical Context

**Language/Version**: HTML5, CSS3, ES2020+ vanilla JavaScript (no transpilation, no modules — single classic `<script>` import)
**Primary Dependencies**: TailwindCSS via CDN (Play CDN, JIT-in-browser), Lucide Icons via CDN script (`<i data-lucide>` swap pattern), Google Fonts CDN for an Arabic-friendly typeface (Cairo as primary, Tajawal as fallback) — all loaded over HTTPS, no local build
**Storage**: `localStorage` — single key `smos:theme` holding `"light"` or `"dark"` (only persisted state, per Constitution Principle VII)
**Testing**: Manual visual review against the Spec Quality Checklist and per-story Independent Test sections; no automated test framework (no build system available, and Constitution Principle I bans bundlers and `npm run dev`); link-integrity verified by a one-off shell `grep` audit at acceptance time
**Target Platform**: Latest two stable versions of Chrome, Firefox, Safari, Edge; viewports 320 px → 1920 px; opens directly via `file://` double-click or via VS Code Live Server / any static file server
**Project Type**: Static web prototype (single project at repo root, no client/server split)
**Performance Goals**: First Contentful Paint ≤ 1.5 s on a throttled 3G profile from CDN-cached state; interactive widgets (sidebar toggle, modals, dropdowns) respond within 100 ms of click (matches Success Criterion SC-005); Lighthouse "Best Practices" score ≥ 90 per page
**Constraints**: No frontend frameworks; no bundler / no `node_modules` / no `package.json`; no API calls; no inline `<script>` blocks beyond the Lucide CDN init and a single `<script src="assets/js/main.js" defer>` line; AA-equivalent contrast (≥ 4.5:1 body, ≥ 3:1 large text) in both themes; RTL by default
**Scale/Scope**: ~30 HTML pages; ~500–1,200 lines per page including hardcoded sample data; one shared 200–400 line `assets/js/main.js`; one custom CSS file (`assets/css/app.css`) of ~150 lines for design touches Tailwind cannot express cleanly (e.g., scrollbar styling, RTL-specific overrides, gradient utilities)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

Evaluation against `.specify/memory/constitution.md` v1.0.0:

| Principle | Gate | Outcome |
|---|---|---|
| I. Static Frontend Only (NON-NEGOTIABLE) | Plan uses only HTML/CSS/Tailwind-CDN/vanilla JS; no React/Vue/Next/Angular/Svelte; no bundler; no `npm run dev`; no API fetches | **PASS** |
| II. Hardcoded, Client-Presentable Pages | Every list page seeds 8–15 sample rows hardcoded in HTML; create/edit/detail variants exist for all core entities; empty-state markup pattern documented but populated rows ship | **PASS** |
| III. RTL Arabic First | Every page sets `dir="rtl"` and `lang="ar"`; Arabic copy across nav, headings, table headers, labels; English only for status tokens (Pending/Delivered/etc.); Tailwind RTL handled via logical properties (`ms-`/`me-`) | **PASS** |
| IV. Premium SaaS Visual Language | Tailwind-based design tokens (rounded-xl/2xl, shadow-sm/md, border-slate-200/700, purple→blue gradients), Cairo font, dark/light parity, custom CSS only for small reusable touches | **PASS** |
| V. Affiliate System As First-Class Differentiator | 4 dedicated pages (`affiliates.html`, `affiliate-detail.html`, `affiliate-requests.html`, `affiliate-payouts.html`); commission rule banner on every affiliate page; QR placeholder + Copy Referral Link wired in main.js; dashboard surfaces top affiliates and pending requests cards | **PASS** |
| VI. Consistent Dashboard Shell | Shell extracted as a documented HTML pattern reused across every dashboard page; sidebar entries fixed in spec order (FR-006); link integrity gated by FR-045 | **PASS** |
| VII. Minimal Vanilla JS Discipline | Single `assets/js/main.js` strictly implementing the allow-listed behaviors (FR-042); only `localStorage` use is `smos:theme`; no SPA routing, no state mgmt, no API simulation | **PASS** |

**Result**: All gates PASS. No deviations to record in Complexity Tracking.

### Post-Design Re-evaluation (after Phase 1)

After producing `research.md`, `data-model.md`, `contracts/pages.md`, and `quickstart.md`, the seven principles were re-checked against every design decision:

| Principle | Post-design check | Outcome |
|---|---|---|
| I. Static Frontend Only | `research.md` §1 confirms Tailwind Play CDN (no build); §6 confirms Lucide CDN; §9 specifies a 30-line custom focus-trap (no npm dep). No framework introduced. | **PASS** |
| II. Hardcoded data | `data-model.md` defines hardcoded sample-row distributions per list page; `contracts/pages.md` requires populated tables with empty-state hidden alongside. | **PASS** |
| III. RTL Arabic First | `research.md` §2 commits to `dir="rtl"` + Tailwind logical-property utilities everywhere. | **PASS** |
| IV. Premium SaaS Visual | `research.md` §4 locks the indigo→violet→blue gradient palette, status-badge tones, and Cairo typography. | **PASS** |
| V. Affiliate First-Class | `contracts/pages.md` gives affiliate module the most detailed treatment; commission rule banner mandated on every affiliate page; dashboard surfaces top affiliates and pending requests cards. | **PASS** |
| VI. Consistent Shell | `contracts/pages.md` defines a single shared "Dashboard shell" section applying to every dashboard page (sidebar order, header regions, JS hooks). | **PASS** |
| VII. Minimal JS | `research.md` §5 confirms `smos:theme` is the only `localStorage` key; only allowed `<script>` blocks per page are: pre-paint theme (inline, 3 lines), Lucide CDN, and deferred `main.js`. No SPA, no state mgmt, no API mock. | **PASS** |

**Post-design result**: All gates STILL PASS. No deviations introduced during Phase 1.

## Project Structure

### Documentation (this feature)

```text
specs/001-static-frontend-mvp/
├── plan.md              # This file (/speckit-plan command output)
├── research.md          # Phase 0 output — design tokens, CDN choices, sample-data plan
├── data-model.md        # Phase 1 output — entity schemas authors use to write sample rows
├── quickstart.md        # Phase 1 output — how to open and verify the prototype
├── contracts/
│   └── pages.md         # Phase 1 output — page-level URL contract (file → required content shape)
├── checklists/
│   └── requirements.md  # Spec quality checklist (already passing)
├── spec.md              # Feature spec (already clarified, 5 sessions answered)
└── tasks.md             # Phase 2 output (created by /speckit-tasks, not /speckit-plan)
```

### Source Code (repository root)

The prototype is a flat static site at the repo root — no `src/`, no `dist/`,
no `node_modules/`, no build output.

```text
.
├── index.html               # Public — home / marketing landing
├── features.html            # Public — features explainer
├── pricing.html             # Public — three-plan comparison
├── login.html               # Public — auth (links to dashboard.html on submit)
├── register.html            # Public — auth (links to dashboard.html on submit)
│
├── dashboard.html           # Merchant — overview
│
├── products.html            # Merchant — catalogue list
├── product-create.html      # Merchant — new product form
├── product-edit.html        # Merchant — edit product form
├── product-detail.html      # Merchant — product detail with related orders / top affiliates
│
├── orders.html              # Merchant — orders list with filters
├── order-detail.html        # Merchant — order detail with timeline & invoice preview
├── order-edit.html          # Merchant — order edit form
│
├── affiliates.html          # Merchant — affiliate roster (CORE differentiator)
├── affiliate-detail.html    # Merchant — affiliate profile + referral link + QR + payout history
├── affiliate-requests.html  # Merchant — pending applications queue
├── affiliate-payouts.html   # Merchant — payouts queue with Pending/Paid/Rejected tabs
│
├── customers.html           # Merchant — CRM list
├── customer-detail.html     # Merchant — customer profile with order history
├── customer-edit.html       # Merchant — customer edit form
│
├── landing-pages.html       # Merchant — landing page list
├── landing-page-create.html # Merchant — landing page builder (form-driven, no DnD)
├── landing-page-preview.html# Merchant — public-facing preview render
│
├── settings.html            # Merchant — settings tabs (Business / Branding / Payment / Affiliate / Notifications / Security)
├── profile.html             # Merchant — profile form
├── notifications.html       # Merchant — notifications inbox
│
├── analytics.html           # Merchant — placeholder for the Analytics sidebar item (avoid dead link per FR-045)
│
├── assets/
│   ├── css/
│   │   └── app.css          # Small reusable design touches Tailwind cannot express cleanly
│   ├── js/
│   │   └── main.js          # Single shared JS — sidebar, dropdown, modal, tabs, copy, theme
│   └── img/
│       ├── logo.svg         # Bilingual wordmark + abstract glyph (FR-045a/b)
│       ├── favicon.svg
│       └── placeholders/    # Static SVG placeholders (product, avatar, dashboard preview, QR)
│
├── partials/                # OPTIONAL: HTML snippets the author can copy-paste into pages (sidebar, header, footer); NOT runtime-imported
│   ├── _sidebar.html
│   ├── _header.html
│   └── _footer.html
│
└── README.md                # How to run (Live Server / double-click), feature list, design notes
```

**Structure Decision**: Flat static-site layout at repo root. All HTML pages
are siblings; relative links between them are simple file references
(`<a href="affiliates.html">`). Shared CSS/JS/images live under `assets/`. The
optional `partials/` folder holds copy-paste HTML snippets for the shared
shell — they exist as authoring conveniences, not as runtime imports
(Constitution Principle I forbids bundlers and ES modules wired through a
build step). Adding `analytics.html` is a deliberate choice to honor FR-045
(no dead links) since the sidebar lists "Analytics" but the spec didn't
enumerate it as an MVP page; it will ship as a styled "coming soon" /
placeholder page consistent with the design language.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

No violations to justify. All seven principles pass without deviation.
