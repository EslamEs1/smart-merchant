# Phase 0 Research: Smart Merchant OS — Static Frontend MVP

**Feature**: 001-static-frontend-mvp
**Date**: 2026-05-10
**Purpose**: Resolve all open technical questions and design-system choices
left implicit by the spec, so authors can write pages without re-deciding
the same questions on every file.

This research consolidates the spec's clarifications session (Q1–Q5) plus the
plan's Technical Context decisions into a single source of truth. There are
**no remaining `NEEDS CLARIFICATION` items** — every entry below has a
Decision and Rationale.

---

## 1. TailwindCSS delivery via CDN

**Decision**: Use the **Tailwind Play CDN** (`<script src="https://cdn.tailwindcss.com"></script>`)
loaded in the `<head>` of every page, with an inline `tailwind.config = { … }`
declaration immediately after for theme tokens (colors, fonts, dark-mode strategy).

**Rationale**:
- Constitution Principle I bans bundlers and `npm run dev`. The Play CDN runs
  Tailwind's JIT compiler in-browser at page-load time — no build step.
- It supports inline `tailwind.config = { darkMode: 'class', theme: { extend: {…} } }`,
  which we need for the purple/blue gradient palette and Arabic font family.
- Trade-off: ~280 KB of script loads on first paint. Acceptable for a demo
  prototype; not acceptable for production (the README will note this).

**Alternatives considered**:
- *Pre-compiled Tailwind stylesheet (e.g., the official `tailwind.min.css` CDN)*
  — rejected: it ships every utility class regardless of use, ~3 MB; we lose
  the JIT.
- *Local `tailwindcss` CLI build* — rejected: requires Node and a build step,
  violating Principle I.

**Implementation notes**:
- Single inline config per page is acceptable, but we standardize on copying
  the same config block into every page from `partials/_head.html`.
- Disable Tailwind preflight only if it conflicts with RTL — it doesn't, so
  keep the default preflight.

---

## 2. RTL support strategy

**Decision**: Set `dir="rtl"` and `lang="ar"` on the `<html>` element of every
page, and use **Tailwind's logical-property utilities** (`ms-`/`me-`,
`ps-`/`pe-`, `text-start`/`text-end`, `start-0`/`end-0`) instead of physical
left/right utilities (`ml-`/`mr-`, `pl-`/`pr-`, `text-left`, `left-0`/`right-0`).

**Rationale**:
- Tailwind v3.3+ ships logical-property utilities natively — no plugin needed.
- The Play CDN runs the latest Tailwind (currently v3.4.x), so logical
  utilities are available.
- Avoids the maintenance pain of writing every layout twice with `dir`-scoped
  overrides.

**Alternatives considered**:
- *`tailwindcss-rtl` plugin* — superseded by built-in logical utilities; using
  the plugin would require a build step.
- *Manual `[dir=rtl]` selectors in custom CSS* — verbose, error-prone, hard
  to keep consistent across 30 pages.

**Implementation notes**:
- Where physical utilities are unavoidable (e.g., `transform: scaleX(-1)` for
  flipping a chevron arrow), wrap them in a small custom CSS class in
  `assets/css/app.css` rather than littering pages.
- Lucide icons that imply direction (chevron-left, chevron-right, arrow-left,
  arrow-right) are used "physically" — i.e., a "next" affordance in RTL
  uses `chevron-left` because the eye travels right-to-left.

---

## 3. Arabic typography

**Decision**: Load **Cairo** as the primary typeface (weights 400, 500, 600,
700, 800) and Tajawal as a fallback, both via Google Fonts CDN. System sans
is the final fallback.

**Rationale**:
- Cairo is a modern, clean, Latin-and-Arabic-mirrored typeface that pairs
  well with the "premium SaaS" visual goal — its proportions match Inter
  (which Stripe uses), giving a familiar look while reading native Arabic.
- Tajawal is a respected fallback with similar proportions, ensuring graceful
  degradation if Cairo fails to load.
- Both are open-source and CDN-served; no licensing or local-asset concerns.

**Alternatives considered**:
- *IBM Plex Sans Arabic* — beautiful but heavier in weight balance; rejected
  for being too "corporate."
- *Noto Sans Arabic* — too utilitarian, lacks the premium feel.
- *Custom Arabic webfont* — over-engineered for a prototype.

**Implementation notes**:
- Load via a single `<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;500;600;700;800&family=Tajawal:wght@400;500;700&display=swap">`.
- Set `fontFamily` in inline Tailwind config: `sans: ['Cairo', 'Tajawal', 'system-ui', 'sans-serif']`.
- Use `font-display: swap` so text remains visible while fonts load.

---

## 4. Color palette & gradient tokens

**Decision**: Extend Tailwind's theme with a brand palette anchored on
**indigo-violet→sky-blue gradients**:

| Token | Light theme | Dark theme | Use |
|---|---|---|---|
| `brand-primary` | `#6366f1` (indigo-500) | `#818cf8` (indigo-400) | Primary buttons, active states |
| `brand-accent` | `#8b5cf6` (violet-500) | `#a78bfa` (violet-400) | Secondary highlights, gradient end-stop |
| `brand-info` | `#3b82f6` (blue-500) | `#60a5fa` (blue-400) | Info badges, links |
| `surface-base` | `#ffffff` | `#0f172a` (slate-900) | Page background |
| `surface-card` | `#f8fafc` (slate-50) | `#1e293b` (slate-800) | Card background |
| `surface-border` | `#e2e8f0` (slate-200) | `#334155` (slate-700) | Subtle borders |
| `text-primary` | `#0f172a` (slate-900) | `#f1f5f9` (slate-100) | Body text |
| `text-muted` | `#64748b` (slate-500) | `#94a3b8` (slate-400) | Captions, placeholders |

**Brand gradient**: `linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #3b82f6 100%)`
— used for the logo glyph, the home-page hero background, the dashboard's
"Pending commissions" stat card highlight, and CTA button hover states.

**Status badge palette**:

| Status family | Tone | Background | Text |
|---|---|---|---|
| Pending / Unpaid / Not Shipped | amber | `bg-amber-100 dark:bg-amber-900/40` | `text-amber-800 dark:text-amber-200` |
| Confirmed / Processing / Preparing | blue | `bg-blue-100 dark:bg-blue-900/40` | `text-blue-800 dark:text-blue-200` |
| Shipped / Partially Paid | indigo | `bg-indigo-100 dark:bg-indigo-900/40` | `text-indigo-800 dark:text-indigo-200` |
| Delivered / Paid / Active | emerald | `bg-emerald-100 dark:bg-emerald-900/40` | `text-emerald-800 dark:text-emerald-200` |
| Cancelled / Rejected / Suspended | rose | `bg-rose-100 dark:bg-rose-900/40` | `text-rose-800 dark:text-rose-200` |
| Refunded / Returned | slate | `bg-slate-200 dark:bg-slate-700` | `text-slate-800 dark:text-slate-200` |
| Bronze (level) | amber-700 | `bg-amber-200/70 dark:bg-amber-900/30` | `text-amber-900 dark:text-amber-300` |
| Silver (level) | slate-400 | `bg-slate-300/60 dark:bg-slate-600/30` | `text-slate-800 dark:text-slate-200` |
| Gold (level) | yellow-500 | `bg-yellow-200/70 dark:bg-yellow-900/30` | `text-yellow-900 dark:text-yellow-300` |
| Platinum (level) | violet-500 | `bg-violet-200/70 dark:bg-violet-900/30` | `text-violet-900 dark:text-violet-300` |

**Rationale**: This palette satisfies Constitution Principle IV (purple/blue
gradients, premium, clean) and Spec FR-050 (≥4.5:1 contrast for body text,
≥3:1 for badges) — every text/background pair was checked against WebAIM's
contrast formula.

**Alternatives considered**:
- *Pure Stripe-style indigo monochrome* — rejected: spec mandates
  purple/blue gradient combo.
- *Saturation-led palette (saturated purples)* — rejected: hurts dark-mode
  contrast.

---

## 5. Dark mode strategy

**Decision**: Use Tailwind's **class-based dark mode** (`darkMode: 'class'`).
The `<html>` element gets/loses a `dark` class controlled by `main.js`,
which reads `localStorage.getItem('smos:theme')` on each page-load (run
before paint via a small inline `<script>` in `<head>`).

**Rationale**:
- Class-based mode lets the toggle button in the header explicitly switch
  themes, which is required by FR-041.
- Reading localStorage *before paint* (via an inline `<script>` in `<head>`,
  before the `<body>` renders) eliminates the flash-of-wrong-theme on slow
  connections.

**Implementation notes**:
- The pre-paint script is the **one** allowed inline `<script>` block per
  page besides the Lucide CDN init and the deferred `main.js` import. It is
  3 lines:
  ```html
  <script>
    try { if (localStorage.getItem('smos:theme') === 'dark') document.documentElement.classList.add('dark'); } catch (e) {}
  </script>
  ```
- This is the single allowed write/read against `localStorage`, per
  Constitution Principle VII.
- `main.js` exposes `setTheme('light' | 'dark')` to be invoked by the toggle
  button.

**Alternatives considered**:
- *Media-query dark mode* (`darkMode: 'media'`) — rejected: doesn't allow
  user override, conflicts with FR-041.
- *`matchMedia('prefers-color-scheme')` as initial default* — accepted as
  fallback when no localStorage entry exists; the pre-paint script is
  extended to check `matchMedia` if `localStorage` is empty.

---

## 6. Lucide icon catalogue (per UI region)

**Decision**: Map each UI region to a fixed Lucide icon name to keep the
visual language consistent across pages.

| Region | Lucide icon |
|---|---|
| Sidebar — Dashboard | `layout-dashboard` |
| Sidebar — Products / Services | `package` |
| Sidebar — Orders | `shopping-cart` |
| Sidebar — Customers | `users` |
| Sidebar — Affiliates | `handshake` |
| Sidebar — Payouts | `wallet` |
| Sidebar — Landing Pages | `layout-template` |
| Sidebar — Analytics | `bar-chart-3` |
| Sidebar — Settings | `settings` |
| Header — Search | `search` |
| Header — Notifications | `bell` |
| Header — Theme toggle (light) | `sun` |
| Header — Theme toggle (dark) | `moon` |
| Header — Mobile menu | `menu` |
| Header — Profile | `user-circle` |
| Action — View / Detail | `eye` |
| Action — Edit | `pencil` |
| Action — Copy link | `link` / `link-2` |
| Action — Duplicate | `copy` |
| Action — Disable | `power-off` |
| Action — Delete | `trash-2` |
| Action — Approve | `check-circle-2` |
| Action — Reject / Cancel | `x-circle` |
| Action — Suspend | `pause-circle` |
| Action — Pay commission | `banknote` |
| Action — Print invoice | `printer` |
| Action — Mark shipped | `truck` |
| Action — Mark delivered | `package-check` |
| Modal — Close | `x` |
| Modal — Confirm destructive | `alert-triangle` |
| Tab — Pending | `clock` |
| Tab — Paid | `check` |
| Tab — Rejected | `x` |
| Stat — Sales | `trending-up` |
| Stat — Orders | `shopping-bag` |
| Stat — Customers | `users` |
| Stat — Affiliates | `handshake` |
| Stat — Commissions | `coins` |
| Stat — New orders | `bell-ring` |
| QR placeholder | `qr-code` |

**Rationale**: A single canonical mapping keeps every page consistent. Lucide
v0.343+ has every icon listed above. Authors copy `<i data-lucide="…"></i>`
markers; `lucide.createIcons()` (called from `main.js` after DOMContentLoaded)
swaps them into inline SVGs.

**Implementation notes**:
- Load Lucide via `<script src="https://unpkg.com/lucide@latest"></script>`
  in `<head>` (deferred is fine; the createIcons call lives in main.js after
  DOMContentLoaded).
- After dynamic DOM updates (e.g., opening a modal that contains
  `<i data-lucide>`), re-call `lucide.createIcons()` — main.js exposes a
  `renderIcons()` helper for this.

---

## 7. Sample-data volume per list page

**Decision**: Each list page MUST hardcode a target row count, distributed
to feel "lived-in" without overwhelming the demo:

| Page | Sample rows |
|---|---|
| Dashboard — recent orders card | 6 rows |
| Dashboard — top affiliates card | 5 rows |
| Dashboard — top products card | 5 rows |
| Dashboard — pending affiliate requests card | 4 rows |
| Products list | 12 rows (covering all 5 product types) |
| Orders list | 14 rows (mix of statuses + with/without affiliate attribution) |
| Affiliates list | 10 rows (covering all 4 levels and all 4 statuses) |
| Affiliate requests | 6 rows (all Pending) |
| Affiliate payouts — Pending tab | 5 rows |
| Affiliate payouts — Paid tab | 6 rows |
| Affiliate payouts — Rejected tab | 3 rows |
| Customers list | 15 rows (covering all 7 sources) |
| Landing pages list | 8 rows |
| Notifications | 12 entries (covering all 5 categories) |

**Rationale**: SC-004 mandates "at least 6 rows" but for "lived-in"
authenticity, larger sets are needed where a viewer's eye would otherwise
land on an obvious limit (especially Orders and Customers). Smaller
dashboard cards stay short to preserve scannability.

**Currency distribution** (per spec FR-038a):
- ~50% of monetary rows show SAR
- ~25% show EGP
- ~20% show AED
- ~5%–10% show one alternative currency (e.g., KWD or USD) for variety —
  the upper bound accommodates small samples where one row is the smallest
  representable share (e.g., 1 row of 10 = 10%)
- Within a single entity (one order, one affiliate's totals), currency is
  consistent.

**Name distribution** (per spec FR-038b):
- ~80% Arabic-script names; ~20% Latin script.

---

## 8. Empty-state pattern

**Decision**: Each list page ships with rows populated, but the markup
includes a hidden empty-state card (`<div class="… hidden">`) immediately
after the table. The empty state pattern uses:
- Centered illustration (a Lucide `inbox` or `package-x` icon at 4xl size,
  brand-gradient stroke)
- H3 heading: `لا توجد عناصر بعد` (or context-specific copy)
- Body paragraph: short Arabic explainer
- Primary CTA button (e.g., `أضف منتجك الأول`) linking to the create page

**Rationale**: Keeps the design system complete (Constitution Principle II
implicit requirement that the prototype be a real-feeling product). Hidden
markup is easy to swap in for screenshots, satisfies design-completeness
reviewers without harming the populated demo.

---

## 9. Modal & dropdown accessibility patterns

**Decision**:
- **Modals**: Open with `role="dialog"` `aria-modal="true"` `aria-labelledby="<heading-id>"`. On open, move keyboard focus to the first focusable element (typically Cancel button); on close, return focus to the trigger. Trap focus inside the dialog while open. ESC and overlay-click both dismiss.
- **Dropdowns** (action menus): Open with `aria-haspopup="menu"` `aria-expanded` toggling. Items are `<a>` or `<button>` with no role overrides (semantic links). Click-outside and ESC close. No focus trap.
- **Mobile sidebar drawer**: Same focus-trap behavior as a modal.

**Rationale**: Satisfies FR-046 (focus rings), FR-047 (tab order), FR-048
(ESC dismissal) without requiring full WCAG ARIA-richness (Q4 clarification —
"visual + keyboard basics, no formal audit").

**Implementation notes**:
- Focus-trap implementation in `main.js` is a 30-line utility: query all
  focusable selectors, intercept Tab/Shift+Tab at boundaries.
- No third-party focus-trap library — Constitution Principle I forbids npm
  deps.

---

## 10. Date / number formatting

**Decision**:
- **Numbers**: Western Arabic digits (0–9) throughout, with thousands
  separator using comma (e.g., `1,250`). No use of Arabic-Indic digits
  (٠–٩) — they hurt scannability in mixed Arabic/English UI and the spec
  Assumptions explicitly skip them.
- **Dates**: Gregorian calendar in Arabic month names (e.g., `15 مايو 2026`)
  for human-friendly displays; ISO `2026-05-15` for compact table cells.
- **Currency suffix format**: `<value> <CODE>` (e.g., `1,250 SAR`) — code
  comes after the value, separated by a space. Three-letter ISO codes only
  (SAR / EGP / AED), no symbol glyphs. Reason: glyph (`ر.س`) introduces
  RTL/LTR direction-mark headaches on a static prototype; uppercase ISO
  reads cleanly in both directions.

---

## 11. Live Server / deployment story

**Decision**: README documents three ways to run the prototype:
1. **Double-click**: open `index.html` directly in a browser (file://). Fully
   functional except for the clipboard API on some browsers.
2. **VS Code Live Server extension** (recommended for development):
   right-click any HTML file → "Open with Live Server".
3. **Any static server** (e.g., `python3 -m http.server 8080`): for sharing
   over LAN.

No `package.json`, no scripts — opening the project must be zero-friction
(SC-001).

---

## 12. Authoring conventions for the team

**Decision**: To keep 30 hand-authored pages consistent, adopt these conventions:
- Every page starts with the same `<head>`: charset, viewport, title, fonts
  link, Lucide CDN script, Tailwind CDN script + inline config, pre-paint
  theme script, link to `assets/css/app.css`.
- Every dashboard page wraps the shell in this structure: `<aside>` (sidebar)
  + `<div class="flex-1">` (main column with header + content).
- Every status badge uses a single utility class set documented in
  `assets/css/app.css` as a `@layer components` shortcut (e.g.,
  `.badge-pending { @apply bg-amber-100 text-amber-800 …; }`). Authors use
  the shortcut, not the raw utilities.
- Sample data comments above each table list (e.g.,
  `<!-- 14 rows: 8 SAR, 4 EGP, 2 AED; 9 with affiliate, 5 without -->`)
  to make the distribution auditable at review time.

**Rationale**: Reduces drift across pages. The `partials/_*.html` snippets
in `partials/` give authors a copy-paste source of truth for the shell.

---

## Summary table — every research item resolved

| # | Topic | Decision summary |
|---|---|---|
| 1 | Tailwind delivery | Tailwind Play CDN with inline `tailwind.config` |
| 2 | RTL strategy | `dir="rtl"` + Tailwind logical-property utilities |
| 3 | Typography | Cairo (primary) + Tajawal (fallback) via Google Fonts |
| 4 | Color palette | Indigo→violet→blue gradient + status badge palette (10 tones) |
| 5 | Dark mode | Class-based, pre-paint inline script, `localStorage['smos:theme']` |
| 6 | Iconography | Lucide via CDN, 40+ canonical mappings documented |
| 7 | Sample-data volumes | 12–15 rows for major lists; multi-currency/multi-name distribution |
| 8 | Empty states | Hidden markup pattern shipped alongside populated tables |
| 9 | Modal & dropdown a11y | role/aria-modal/focus trap; dropdowns lighter-weight |
| 10 | Number/date formatting | Western digits, ISO/Arabic-month dual date format, `<value> CODE` currency |
| 11 | Local run | README documents 3 zero-friction methods |
| 12 | Authoring conventions | Standard `<head>`, partials folder, `@layer components` badge shortcuts |

**Status**: All technical context resolved. Plan is ready to proceed to Phase 1.
