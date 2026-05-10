<!--
SYNC IMPACT REPORT
Version change: TEMPLATE (unratified) → 1.0.0
Bump rationale: Initial ratification — first concrete constitution replacing the
unfilled template. MAJOR/MINOR/PATCH semantics begin from this baseline.

Modified principles (all newly authored from placeholders):
  - [PRINCIPLE_1_NAME] → I. Static Frontend Only (NON-NEGOTIABLE)
  - [PRINCIPLE_2_NAME] → II. Hardcoded, Client-Presentable Pages
  - [PRINCIPLE_3_NAME] → III. RTL Arabic First
  - [PRINCIPLE_4_NAME] → IV. Premium SaaS Visual Language
  - [PRINCIPLE_5_NAME] → V. Affiliate System As First-Class Differentiator
  - (added)            → VI. Consistent Dashboard Shell
  - (added)            → VII. Minimal Vanilla JS Discipline

Added sections:
  - Technical Constraints & Scope (replaces [SECTION_2_NAME])
  - Development Workflow & Quality Gates (replaces [SECTION_3_NAME])
  - Governance

Removed sections: none

Templates requiring updates:
  - ✅ .specify/templates/plan-template.md — reviewed; "Constitution Check"
        gate is generic and remains valid. No edit required; principle gates
        will be applied at /speckit-plan time.
  - ✅ .specify/templates/spec-template.md — reviewed; structure compatible
        with this constitution. No edit required.
  - ✅ .specify/templates/tasks-template.md — reviewed; task categorization
        compatible (no test-first mandate, no observability mandate added).
        No edit required.
  - ⚠ .claude/skills/speckit-plan, speckit-tasks, speckit-implement —
        downstream skills will read this constitution at execution time;
        no static edit required.

Follow-up TODOs: none — all placeholders resolved.
-->

# Smart Merchant OS Frontend Constitution

## Core Principles

### I. Static Frontend Only (NON-NEGOTIABLE)

The project MUST be a static frontend prototype built only with HTML, CSS,
TailwindCSS, and minimal vanilla JavaScript. Frontend frameworks (React, Vue,
Next.js, Angular, Svelte, etc.) and build-heavy toolchains are FORBIDDEN. The
project MUST be openable directly in a browser or via Live Server with no
`npm run dev`, no bundler, and no backend server. The frontend MUST NOT fetch
data from APIs, simulate APIs, or contain backend logic.

**Rationale**: The deliverable is a client-presentable visual prototype, not a
runnable application. Forbidding frameworks and runtimes keeps the artifact
portable, reviewable as raw HTML, and free of supply-chain or build-tooling
risk. Any deviation invalidates the prototype's purpose.

### II. Hardcoded, Client-Presentable Pages

All page data MUST be hardcoded inside the HTML pages. Every page MUST look
complete and client-presentable: tables MUST include realistic sample rows,
list pages MUST include actions dropdowns, and core entities (Products,
Orders, Affiliates, Customers, Landing Pages) MUST have create, edit, and
detail pages where the entity supports them. A page that contains only a
title or empty placeholder is NOT acceptable. Content sections, once created,
MUST NOT be removed unless the user explicitly requests their removal.

**Rationale**: This prototype's value is review-by-screenshot. Empty shells
and "we'll fill it in later" stubs defeat the purpose. Hardcoded realistic
data is what makes the deliverable demonstrable.

### III. RTL Arabic First

The UI MUST default to RTL layout direction and use clear Arabic content
across labels, navigation, page titles, table headers, and copy. English MAY
be used only for technical status tokens where convention favors it
(e.g., `Pending`, `Delivered`, `Cancelled`, `Paid`, `Refunded`). All layout
spacing, alignment, iconography, and component order MUST be verified to read
correctly right-to-left.

**Rationale**: The target merchant audience reads Arabic. Treating RTL as a
late-stage adaptation typically produces broken layouts; making it the
default forces every component to be RTL-correct from the first commit.

### IV. Premium SaaS Visual Language

The visual design MUST feel like a high-end SaaS dashboard: Apple-like
spacing, Stripe-style clarity, rounded cards, soft shadows, subtle borders,
purple/blue gradient accents, clean typography, spacious layout, and clear
visual hierarchy. A dark/light mode toggle MUST be supported. Custom CSS is
permitted only for small reusable design touches that Tailwind utilities
cannot express cleanly; bulk styling MUST go through Tailwind.

**Rationale**: "Premium SaaS" is the product promise to merchants and the
basis on which the prototype will be judged. Without an enforced design
language the deliverable degrades into generic admin-template territory.

### V. Affiliate System As First-Class Differentiator

The Affiliate System is the project's primary differentiator and MUST be
visually central in the UI. The dashboard MUST surface affiliate metrics
prominently, and the affiliate workflow MUST be representable end-to-end
through dedicated pages: Affiliates List, Affiliate Detail, Affiliate
Requests (approval queue), and Affiliate Payouts. Every affiliate-related
view MUST make referral links, QR code placeholders, coupons, and tracked
commissions visible and copyable where applicable. The Copy Referral Link
interaction MUST work via vanilla JS.

**Rationale**: Without explicit centrality the affiliate features blur into
yet-another-CRM-section. The whole reason a merchant chooses this product
over a generic dashboard is the affiliate flow — the UI must reflect that.

### VI. Consistent Dashboard Shell

Every dashboard page MUST share the same visual shell: a fixed desktop
sidebar, a mobile sidebar drawer, a top header with search input,
notifications icon, and merchant profile menu, a main content area, and
breadcrumbs where they aid navigation. The sidebar MUST contain exactly
these primary entries in this order: Dashboard, Products / Services, Orders,
Customers, Affiliates, Payouts, Landing Pages, Analytics, Settings. Sidebar
links MUST point to existing pages; broken links violate the constitution.

**Rationale**: Consistency across dozens of static pages is what makes the
prototype feel like a real product rather than a Figma export. Drift in
shell layout between pages is the most common failure mode for hand-built
HTML mockups.

### VII. Minimal Vanilla JS Discipline

Vanilla JavaScript MAY be used ONLY for: sidebar toggle, mobile menu,
dropdown menus, tabs, modals, dark/light mode toggle, copy referral link,
and simple visual chart-placeholder animations. The following are FORBIDDEN:
SPA routing, API simulation, complex state management, framework-like
abstractions, and any use of `localStorage` beyond persisting the theme
preference.

**Rationale**: Each allowed JS use case maps to a UI affordance the static
HTML cannot express alone. Crossing into routing or state management
re-introduces exactly the framework complexity Principle I exists to
prevent.

## Technical Constraints & Scope

**Required UI components** (MUST be implemented as reusable, consistent
markup patterns across pages): stat cards, data tables, status badges,
action dropdowns, filter bars, search inputs, pagination controls, empty
state cards, confirmation modals, detail summary cards, activity timeline,
commission cards, QR code placeholder, referral link copy box.

**MVP page set** (MUST all exist and be reachable from navigation):

- *Public*: Home, Features, Pricing, Login, Register.
- *Merchant Dashboard*: Dashboard Overview, Products List, Product Create,
  Product Edit, Product Detail, Orders List, Order Detail, Order Edit,
  Affiliates List, Affiliate Detail, Affiliate Requests, Affiliate Payouts,
  Customers List, Customer Detail, Customer Edit, Landing Pages List,
  Landing Page Create, Landing Page Preview, Settings, Profile,
  Notifications.

**Business flow representation** (MUST be visually traceable through the
prototype): merchant adds products → affiliates register and await approval
→ merchant approves affiliates → affiliates receive referral links and QR
codes → customers place orders → orders link to customer, product, and
optional affiliate → commissions accrue on paid/delivered orders →
merchant reviews and pays out commissions → customers persist in the CRM →
merchant publishes landing pages for offers/products.

**Per-page content baselines** (illustrative, not exhaustive):

- Dashboard: stat cards, chart placeholders, recent orders, top affiliates,
  top products.
- Products: rows for product name, type, price, stock, status, actions.
- Orders: rows for order number, customer, product, affiliate, total,
  payment status, shipping status, actions.
- Affiliates: rows for name, level, sales, orders, commission, status,
  actions.
- Customers: rows for name, phone/email, source, orders, total spent, tags,
  actions.
- Landing Pages: rows for title, product, conversion rate, visits, status,
  actions.

## Development Workflow & Quality Gates

A page or change is **acceptance-eligible** only when ALL of the following
hold:

1. All MVP pages listed above exist as files and are reachable.
2. Every navigation link (header, sidebar, in-page) resolves to an existing
   page; no dead links.
3. Tables on list pages contain realistic sample data.
4. Action dropdowns open and expose useful actions for the row's entity.
5. Create, edit, and detail pages exist for every core module that the MVP
   page set requires them for.
6. Confirmation modals are wired and dismissable.
7. The mobile sidebar drawer opens, closes, and traps focus reasonably.
8. The layout is responsive at common breakpoints (mobile, tablet, desktop).
9. RTL Arabic layout reads correctly; no flipped icons, broken alignment,
   or LTR leaks.
10. Affiliate pages prominently surface referral link, QR placeholder, and
    commission state.
11. The project opens directly in a browser or via Live Server with no
    framework server, no bundler, and no `npm run dev`.

**Constitution Check gate**: every `/speckit-plan` output MUST verify the
plan does not propose any framework, bundler, API call, or backend service.
Any such proposal MUST be either removed or recorded in the plan's
Complexity Tracking with explicit user-approved justification — and even
then is FORBIDDEN against Principle I (NON-NEGOTIABLE).

**Code review expectations**: reviewers MUST check that new pages preserve
the shared shell (Principle VI), reuse existing component patterns rather
than diverging, and do not introduce JS beyond the Principle VII allow-list.

## Governance

This constitution supersedes ad-hoc preferences and team conventions. When
this document conflicts with another instruction (including AGENTS.md or a
slash-command prompt), this document wins unless the user explicitly
overrides it in the conversation.

**Amendment procedure**: amendments are proposed by re-running
`/speckit-constitution` with the change described in the user input. The
command MUST update version, dates, and the Sync Impact Report, and MUST
propagate consequences into `.specify/templates/*` and downstream skill
prompts where applicable.

**Versioning policy** (semantic):

- **MAJOR** — a principle is removed, renumbered, or redefined in a
  backward-incompatible way; or governance rules change in a way that
  invalidates prior plans.
- **MINOR** — a new principle or new mandatory section is added, or
  guidance is materially expanded.
- **PATCH** — wording, clarifications, typo fixes, non-semantic refinements.

**Compliance review**: every `/speckit-plan`, `/speckit-tasks`, and
`/speckit-implement` invocation MUST treat this file as authoritative.
Violations of NON-NEGOTIABLE principles MUST block the workflow rather
than be tracked as deferred items.

**Version**: 1.0.0 | **Ratified**: 2026-05-10 | **Last Amended**: 2026-05-10
