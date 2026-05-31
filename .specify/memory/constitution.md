<!--
SYNC IMPACT REPORT
Version change: 1.0.0 → 2.0.0
Bump rationale: MAJOR. The project pivots from a "static frontend prototype with no
backend" (v1) to a "real Django backend that reuses the existing frontend as templates."
This backward-incompatibly redefines v1 Principle I (Static Frontend Only — no backend,
no APIs, no server) and supersedes the frontend-only scope. Prior plans/specs written
against v1 assumptions no longer hold.

Modified principles (old v1 → new v2):
  - I. Static Frontend Only (NON-NEGOTIABLE)         → I. Frontend Preservation (NON-NEGOTIABLE) [redefined]
  - VII. Minimal Vanilla JS Discipline               → II. Server-Rendered Django, No SPA / No API-First (NON-NEGOTIABLE) [redefined+expanded]
  - (new)                                            → III. Modular App Architecture
  - (new)                                            → IV. Role-Based Access & Owner-Scoped Data Isolation (NON-NEGOTIABLE)
  - II. Hardcoded, Client-Presentable Pages          → V. Database-Backed Truth — No Fake Dynamic Data [reversed]
  - V. Affiliate System As First-Class Differentiator→ VI. Affiliate & Commission Integrity (NON-NEGOTIABLE) [expanded to backend rules]
  - (new)                                            → VII. Customer Privacy on Affiliate Surfaces (NON-NEGOTIABLE)
  - (new)                                            → VIII. Physical-Commerce MVP Catalog
  - Retired as standalone principles (folded into Template Conversion Rules / standards):
      III. RTL Arabic First, IV. Premium SaaS Visual Language, VI. Consistent Dashboard Shell
      — these survive as preservation obligations under Principle I, not as separate principles.

Added sections:
  - Technology & Architecture Standards
  - Domain Rules: Roles, Statuses & Commission Logic
  - Template Conversion Rules
  - MVP Scope & Definition of Done

Removed sections:
  - "Technical Constraints & Scope" (v1 static page-set baselines) — superseded by
    Database-Backed Truth + MVP Scope.

Templates requiring updates:
  - ✅ .specify/templates/plan-template.md — "Constitution Check" gate is generic and
        reads this file at /speckit-plan time; web-app structure options now fit. No edit.
  - ✅ .specify/templates/spec-template.md — no static-frontend coupling. No edit.
  - ✅ .specify/templates/tasks-template.md — generic DB/auth/framework task buckets now
        align with the Django backend. No edit.
  - ✅ .claude/skills/speckit-{plan,tasks,implement,analyze} — read this file at runtime.

Follow-up TODOs: none — all placeholders resolved.
-->

# Smart Merchant OS Backend Constitution

*Smart Merchant OS is a SaaS-style merchant operating system that connects merchants with
affiliate marketers. The frontend prototype already exists as static HTML pages. The backend
mission is to turn that prototype into a real Django system — preserving the existing UI and
gradually replacing hardcoded data with database-backed data — across two surfaces: the
Merchant Portal and the Affiliate Seller Portal.*

## Core Principles

### I. Frontend Preservation (NON-NEGOTIABLE)

The existing frontend design MUST be preserved exactly. The backend MUST reuse the existing
HTML as Django templates and replace hardcoded data with database-backed data — nothing more.
The following are FORBIDDEN: redesigning the UI; replacing pages with generic Django admin
screens; removing sections; simplifying cards, tables, modals, navigation, or layouts;
changing spacing, colors, typography, or visual identity except where strictly required for
backend integration; changing the merchant dashboard shell; changing the affiliate
mobile-first shell. The RTL Arabic layout, dark/light toggle, premium SaaS visual language,
and the consistent merchant/affiliate shells from the prototype MUST remain intact.

**Rationale**: The prototype's design is a deliverable in its own right and the basis on
which the product is judged. The backend's job is to make it *real*, not to re-make it.
Visual drift during backend wiring is the single most likely way to destroy delivered value.

### II. Server-Rendered Django — No SPA, No API-First (NON-NEGOTIABLE)

The system MUST be built with Python, Django, and Django Templates against PostgreSQL-ready
models, using Django authentication and Django (model) forms where appropriate. Django admin
is for internal management ONLY — never as the user-facing UI. The following are FORBIDDEN for
the MVP: React, Next.js, Vue, Angular, any SPA router, API-first architecture, Django REST
Framework (unless an explicit later need is approved), frontend rebuilds, and any Node-based
frontend build system. Existing Tailwind/Lucide/static assets MUST be used as currently
implemented; only minimal vanilla JavaScript for the existing UI interactions is permitted.

**Rationale**: Server-rendered Django templates are the shortest, lowest-risk path from a
static prototype to a working product. Introducing a SPA or API layer would force a frontend
rebuild — the exact opposite of Principle I — and multiply MVP scope.

### III. Modular App Architecture

The backend MUST be organized into focused, modular Django apps rather than one monolith app.
Each app SHOULD own its `models.py`, `views.py`, `urls.py`, `forms.py` (where needed),
`admin.py`, `services.py` for business logic when warranted, `selectors.py` for query logic
when useful, tests, and templates under its own namespace. Project-level templates are
reserved for shared base layouts only (`base.html`, `merchant_base.html`, `affiliate_base.html`,
`auth_base.html`). Business logic MUST NOT accumulate in views when a service/selector is the
clearer home.

**Rationale**: Clear app boundaries keep the affiliate/commission/payout domain — the
product's core — independently understandable and testable, and make ownership and review
obvious as the system grows.

### IV. Role-Based Access & Owner-Scoped Data Isolation (NON-NEGOTIABLE)

The system MUST support at least three roles: Merchant (Owner), Affiliate Marketer, and
Admin/Staff. Login MUST redirect users to their role's surface. Users MUST NOT access pages
outside their role. Affiliate users MUST see ONLY their own orders, commissions, payouts,
saved products, and profile data. Merchant users MUST manage ONLY their own business data
unless they are staff/admin. Every private view MUST enforce login, role, and object-ownership
checks at the view/queryset level — never relying on the UI hiding a link.

**Rationale**: This is a multi-actor commerce platform handling money and customer data.
Cross-actor data leakage (one affiliate seeing another's earnings, one merchant editing
another's products) is a critical-severity failure, not a UI nicety.

### V. Database-Backed Truth — No Fake Dynamic Data

After a page is converted, all of its dynamic content MUST come from database records. Static
sample rows are permitted ONLY as clearly separated seed/demo data for development. Dashboard
totals, counts, and KPIs MUST be computed from records — never hardcoded. When a database
query returns nothing, the page MUST render the existing empty-state UI instead of fabricated
rows. A converted page that still shows hardcoded fake rows is NOT acceptance-eligible.

**Rationale**: The whole point of the backend is that what users see is true. Hardcoded
totals and fake rows in a "dynamic" page are silent lies that erode trust the moment real
data diverges from them.

### VI. Affiliate & Commission Integrity (NON-NEGOTIABLE)

The affiliate system is the product's core differentiator and MUST be modeled faithfully end
to end: affiliate registration/creation, approval/rejection/suspension, levels, referral
codes, referral links, coupon codes, affiliate-attributed orders, commission calculation,
affiliate earnings, payout requests, and payout approval/rejection/paid state. A commission
is created ONLY when an order is attributed to an affiliate; it starts `Pending`; it becomes
`Approved` only when the order is `Delivered` or payment is confirmed `Paid`; it becomes
`Paid` only after a payout is completed; cancelled or refunded orders MUST NOT yield approved
commission. Commission values MUST remain consistent across orders, affiliate earnings, the
merchant affiliate-detail view, and payouts.

**Rationale**: Money flows through this subsystem. An inconsistent or premature commission is
a financial error, not a display bug — the state machine and cross-view consistency are
load-bearing.

### VII. Customer Privacy on Affiliate Surfaces (NON-NEGOTIABLE)

Affiliate users MUST NOT see full customer private data. On affiliate portal pages the
customer phone MUST be masked, the customer email MUST NOT be shown, the customer address MUST
NOT be shown, and full customer identity MUST stay hidden unless explicitly approved later.
Merchant users MAY see full customer data for their own business. Masking MUST happen in the
view/serializer layer, not only in the template.

**Rationale**: Affiliates are external sellers, not data owners. Exposing buyer PII to them is
a privacy and trust violation and a likely legal liability.

### VIII. Physical-Commerce MVP Catalog

The visible MVP catalog MUST contain physical commerce products only. Allowed categories are:
إلكترونيات، إكسسوارات موبايل، أجهزة منزلية صغيرة، عناية شخصية، ملابس، أدوات منزلية. Sample data
of the following kinds is FORBIDDEN in the visible MVP: كورسات، كتب، PDF، ملفات تعليمية،
تدريب، محاضرات، اشتراكات تعليمية. The platform MAY support services or digital products in a
future phase, but MVP visible data MUST read like a physical reseller / affiliate commerce
system. (See also the project memory: physical-commerce-only.)

**Rationale**: The product is positioned as a physical reseller/affiliate commerce system;
mixed-in courses or subscriptions confuse the story and contradict the established prototype
direction.

## Technology & Architecture Standards

**Recommended apps** (use these names where they fit): `core`, `accounts`, `merchants`,
`products`, `orders`, `customers`, `affiliates`, `commissions`, `payouts`, `landing_pages`,
`dashboard`, `notifications`.

**Per-app file layout** (include what the app needs): `models.py`, `views.py`, `urls.py`,
`forms.py`, `admin.py`, `services.py` (business logic), `selectors.py` (query logic), tests,
and app-namespaced templates.

**Shared base templates** (project-level only): `templates/base.html`, `templates/auth_base.html`,
`templates/merchant_base.html`, `templates/affiliate_base.html`. Merchant and affiliate layouts
MUST stay separate.

**Allowed tech**: Python, Django, Django Templates, PostgreSQL-ready models, Django auth,
Django/model forms, Django admin (internal only), the existing HTML/CSS/JS and
Tailwind/Lucide/static assets as currently implemented, and minimal vanilla JS for existing
interactions.

**Forbidden tech (MVP)**: React, Next.js, Vue, Angular, SPA routing, API-first architecture,
DRF (unless explicitly approved later), frontend rebuilds, Node-based frontend build systems,
and replacing the frontend with Django admin.

## Domain Rules: Roles, Statuses & Commission Logic

**Roles**: Owner/Merchant · Affiliate Marketer · Admin/Staff.

**Affiliate levels**: Bronze · Silver · Gold · Platinum.
**Affiliate statuses**: Pending · Active · Suspended · Rejected.

**Order statuses**: Pending · Confirmed · Processing · Shipped · Delivered · Cancelled.
**Payment statuses**: Unpaid · Paid · Partially Paid · Refunded.
**Shipping statuses**: Not Shipped · Preparing · Shipped · Delivered · Returned.
**Commission statuses**: Pending · Approved · Paid · Rejected · Cancelled.

**Commission state machine** (authoritative — see Principle VI):

1. Created ONLY when an order is attributed to an affiliate.
2. Starts as `Pending`.
3. → `Approved` when the order is `Delivered` OR payment is confirmed `Paid`.
4. → `Paid` ONLY after a payout is completed.
5. Cancelled/refunded orders MUST NOT produce approved commission.
6. Commission values MUST stay consistent across orders, affiliate earnings, merchant
   affiliate detail, and payouts.

**Status tokens** stay in English in the UI (matching the prototype); all other content stays
Arabic and RTL.

## Template Conversion Rules

Convert the current HTML pages into Django templates gradually, preserving the UI exactly:

- Keep the merchant and affiliate layouts separate; build on the four base templates above.
- Extract repeated header / sidebar / bottom-nav into `{% include %}` partials.
- Use template inheritance deliberately; do not over-abstract.
- Do NOT break existing JavaScript hooks; keep every `data-*` attribute the JS relies on
  (theme toggle, dropdowns, modals, tabs, copy buttons, favorite toggles, gallery switches,
  bottom-nav targets, segmented tabs).
- Keep RTL Arabic and the dark/light toggle working.
- Modals, dropdowns, tabs, copy buttons, favorite toggles, and gallery switches MUST keep
  working after conversion.

## Development Workflow & Quality Gates

**Phase-by-phase delivery (MANDATORY)**: The backend MUST NOT be implemented in one pass. Each
phase MUST define a Goal, Models, Views, URLs, Templates, Forms, Admin, Services (if needed),
and a Manual acceptance test. After every phase: run migrations, start the server, manually
test the affected pages, confirm NO frontend regression, and commit when stable.

**Per-page quality checks** (every converted page, with real DB data): auth redirects correct;
role permissions enforced; empty states work; forms show validation errors clearly;
create/edit/detail/list flows work; buttons and links navigate correctly; dashboard numbers
accurate; an affiliate cannot see another affiliate's data; a merchant cannot manage another
merchant's data; no broken template paths; no broken static files; no broken JS hooks.

**Security requirements** (Django defaults, enforced): CSRF protection on all forms; login
required on private pages; role-based access via decorators/mixins; object-ownership checks;
safe file-upload handling (when uploads arrive); no sensitive data rendered where it is not
allowed (see Principle VII); `DEBUG` off in production settings; secrets via environment
variables.

**Constitution Check gate**: every `/speckit-plan` output MUST verify the plan introduces no
forbidden tech (SPA framework, API-first/DRF for MVP, Node frontend build, frontend rebuild,
Django-admin-as-UI) and no frontend redesign. Any such proposal MUST be removed, or recorded
in Complexity Tracking with explicit user-approved justification — and remains FORBIDDEN where
it violates a NON-NEGOTIABLE principle.

## MVP Scope & Definition of Done

**MVP includes**: authentication and roles; merchant dashboard with database-backed stats;
Products CRUD; Customers CRM; Orders CRUD; affiliate management; affiliate-portal dynamic data;
commission calculation; payout requests; simple landing pages; seed demo data.

**MVP excludes (not yet)**: real payment gateway integration; real WhatsApp API integration;
real shipping integration; real drag-and-drop landing page builder; mobile app; advanced AI
features; multi-tenant billing subscriptions; full API platform.

**Definition of Done** — the backend MVP is done when ALL hold:

1. Merchant can log in and see real dashboard data.
2. Affiliate can log in and see their own portal.
3. Products are database-backed.
4. Orders are database-backed.
5. Customers are database-backed.
6. Affiliate attribution works.
7. Commission calculation works.
8. Affiliate earnings reflect real commissions.
9. Affiliate can request a payout.
10. Merchant can approve/reject/mark payouts as paid.
11. The existing frontend design remains visually unchanged.
12. No static fake rows remain in converted dynamic pages.
13. Empty states render correctly.
14. Role permissions are enforced.
15. The project is ready for deployment planning.

## Governance

This constitution supersedes ad-hoc preferences and team conventions. When it conflicts with
another instruction (including CLAUDE.md/AGENTS.md or a slash-command prompt), this document
wins unless the user explicitly overrides it in the conversation.

**Amendment procedure**: amendments are proposed by re-running `/speckit-constitution` with the
change described in the user input. The command MUST update the version, dates, and Sync Impact
Report, and MUST propagate consequences into `.specify/templates/*` and downstream skill prompts
where applicable.

**Versioning policy** (semantic):

- **MAJOR** — a principle is removed, renumbered, or redefined in a backward-incompatible way;
  or governance rules change in a way that invalidates prior plans.
- **MINOR** — a new principle or new mandatory section is added, or guidance is materially
  expanded.
- **PATCH** — wording, clarifications, typo fixes, non-semantic refinements.

**Compliance review**: every `/speckit-plan`, `/speckit-tasks`, and `/speckit-implement`
invocation MUST treat this file as authoritative. Violations of NON-NEGOTIABLE principles MUST
block the workflow rather than be tracked as deferred items.

**Version**: 2.0.0 | **Ratified**: 2026-05-10 | **Last Amended**: 2026-05-31
