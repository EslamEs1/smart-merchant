# Feature Specification: Backend Foundation (Django Conversion — Phase 0)

**Feature Branch**: `003-backend-foundation`  
**Created**: 2026-05-31  
**Status**: Draft  
**Input**: User description: "Smart Merchant OS Backend MVP — Foundation: establish the Django project structure, settings, authentication foundation, role model, base templates, static file integration, and the first working route conversion. The existing static frontend must remain visually unchanged. This phase must not implement the entire system."

## User Scenarios & Testing *(mandatory)*

This is the foundation phase of converting the existing static Smart Merchant OS prototype
into a real server-driven application. Its value is *proving the conversion path works*: the
prototype now runs as a served application, assets and interactions still work, login routes
users by role, and the merchant/affiliate layouts are wired for gradual page-by-page
conversion — all without changing how anything looks.

### User Story 1 - The prototype runs as a served application, visually unchanged (Priority: P1)

A visitor (or developer) opens the running application and browses the existing pages — public
marketing pages, the login/register pages, the merchant pages, and the affiliate portal pages.
Every page looks exactly like the static prototype: same layout, spacing, colors, typography,
RTL Arabic direction, and dark/light theme. CSS, JavaScript, icons, and image placeholders all
load, and every existing interaction still works (theme toggle with persistence, dropdown
menus, modals, tabs, copy buttons, favorite toggles, image-gallery switching, affiliate
bottom-nav active state).

**Why this priority**: This is the non-negotiable core of the whole backend effort. If serving
the pages through the application changes their appearance or breaks their behavior, the
project has failed its first principle (frontend preservation). Everything else builds on this.

**Independent Test**: Start the application, open a representative page from each surface
(public, auth, merchant, affiliate), and confirm pixel-equivalent appearance to the static
file plus working interactions and no failed asset requests.

**Acceptance Scenarios**:

1. **Given** the application is running, **When** a visitor opens the merchant dashboard page,
   **Then** it renders visually identical to the static `dashboard.html`, with all styles,
   icons, and scripts loaded and no broken asset requests.
2. **Given** the application is running, **When** a visitor opens an affiliate portal page,
   **Then** the mobile-first affiliate shell, RTL layout, and bottom navigation render
   identically to the static page.
3. **Given** a served page with interactive elements, **When** the user toggles the theme,
   opens a dropdown/modal, clicks a copy button, toggles a favorite, or switches a gallery
   thumbnail, **Then** each interaction behaves exactly as it did in the static prototype.
4. **Given** any served page, **When** the user follows an existing internal navigation link,
   **Then** the link resolves to the correct served page (no dead links introduced).

---

### User Story 2 - Role-based login and redirect skeleton (Priority: P2)

A user logs in through the existing login page. On success, the application sends them to the
home of their role: a merchant lands on the merchant dashboard, an affiliate lands on the
affiliate dashboard, and an admin/staff user lands on the administrative area (Django's built-in
admin site). Trying to reach a private page without being logged in redirects to login; logging
out ends the session.

**Why this priority**: The role and redirect skeleton is the backbone every later MVP phase
depends on (merchant-only data, affiliate-only data). It can be added after the pages are
servable (US1), and on its own it demonstrates the access model end to end.

**Independent Test**: With one merchant test account and one affiliate test account, log in as
each and confirm the correct landing surface; attempt to open a private page while logged out
and confirm redirect to login; log out and confirm the session ends.

**Acceptance Scenarios**:

1. **Given** a registered merchant account, **When** the user logs in, **Then** they are
   redirected to the merchant dashboard.
2. **Given** a registered affiliate account, **When** the user logs in, **Then** they are
   redirected to the affiliate dashboard.
3. **Given** an admin/staff account, **When** the user logs in, **Then** they are redirected to
   the administrative area (Django's built-in admin site at `/admin/`).
4. **Given** an unauthenticated visitor, **When** they request a private page directly,
   **Then** they are redirected to the login page.
5. **Given** a logged-in user, **When** they log out, **Then** the session ends and they return
   to a public/auth page.

---

### User Story 3 - Separated base layouts with the first converted routes (Priority: P3)

The merchant surface and the affiliate surface each have their own base layout, and the
public/auth surface has its own; the merchant and affiliate shells stay visually independent.
The repeated shell regions (merchant header/sidebar; affiliate header/sidebar/bottom-nav) live
in shared, reusable includes instead of being duplicated in every page. At least one page per
surface is converted to render through template inheritance (extending its base) while looking
exactly like the static original — proving that the rest of the pages can be converted the same
way, gradually.

**Why this priority**: This establishes and validates the *gradual conversion mechanism*. It
is sequenced last among the three because it depends on pages being servable (US1) and benefits
from the auth skeleton (US2), but it is the proof that future phases can convert page-by-page
without regressions.

**Independent Test**: Convert one public/auth page, one merchant page, and one affiliate page
to extend their respective base layouts, then confirm each converted page renders identically
to its static original and that non-converted pages still work.

**Acceptance Scenarios**:

1. **Given** the base layouts exist, **When** the converted merchant page is rendered, **Then**
   it extends the merchant base and is visually identical to the static original.
2. **Given** the base layouts exist, **When** the converted affiliate page is rendered, **Then**
   it extends the affiliate base, keeps the mobile-first shell, and is visually identical.
3. **Given** a shared shell region is edited in its include, **When** pages that use that
   include are rendered, **Then** they all reflect the change consistently (proving
   de-duplication).
4. **Given** the merchant and affiliate bases, **When** both surfaces are compared, **Then**
   each keeps its own distinct shell with no cross-contamination of layout.

---

### Edge Cases

- **Asset path resolution**: existing pages reference assets with relative paths
  (e.g., `assets/...`); the served application MUST resolve these so nothing 404s.
- **Inter-page links**: existing pages link to each other by filename
  (e.g., `href="dashboard.html"`); routing MUST keep these links resolving (see Assumptions).
- **Unauthenticated access** to a private page → redirect to login, then (optionally) return to
  the originally requested page after successful login.
- **Account with no/ambiguous role** → routed to a safe default (public/auth) rather than
  erroring; this case must not crash login.
- **Theme persistence**: the dark/light preference stored client-side MUST still persist across
  served pages.
- **Direct access to a converted page vs. a not-yet-converted page** MUST both work during the
  gradual transition.
- **Failed login (invalid credentials)** → the login page re-renders with a single generic error;
  the system MUST NOT reveal whether the identifier or the password was wrong.

## Clarifications

### Session 2026-05-31

- Q: After successful login, what determines the redirect — the account's role or the login page's
  role selector? → A: The authenticated account's stored role is authoritative; the login-page
  role selector is informational/cosmetic only and MUST NOT influence access or routing.
- Q: Which field uniquely identifies a user at login? → A: `username` is the canonical unique
  identifier (Django default `AbstractUser`). Because the preserved login form collects an email,
  login is **accepted by email** — resolved to the account via an email-or-username authentication
  backend — so the existing email-labeled field works unchanged; `email` MUST therefore be unique.
- Q: Where do Admin/Staff users land after login (the "administrative area")? → A: Django's built-in
  admin site at `/admin/`; no custom administrative UI is built in this phase.
- Q: How should the page respond when login fails (bad credentials)? → A: Re-render the login page
  with a single generic error message; never disclose which field (identifier or password) was wrong.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The application MUST serve every existing prototype page (public, auth, merchant,
  affiliate) through the running web application with no change to its rendered appearance
  versus the corresponding static file.
- **FR-002**: All existing static assets (CSS, JavaScript, images/SVG placeholders, fonts) MUST
  load successfully for every served page, with no missing-asset (404) requests.
- **FR-003**: All existing client-side interactions MUST continue to function on served pages:
  dark/light theme toggle (with persistence), dropdown menus, modals, tabs, copy buttons,
  favorite toggles, image-gallery thumbnail switching, and affiliate bottom-nav active state.
- **FR-004**: The RTL Arabic layout direction and the dark/light theme MUST be preserved on
  every served page.
- **FR-005**: The application MUST present the existing login page and accept a login attempt
  submitted from it.
- **FR-006**: On successful login the application MUST redirect the user to their role's home,
  determined solely by the authenticated account's stored role (the login page's role selector is
  informational only and MUST NOT influence access or routing): Merchant → merchant dashboard,
  Affiliate → affiliate dashboard, Admin/Staff → Django's built-in admin site (`/admin/`). No
  custom administrative UI is built in this phase.
- **FR-007**: The system MUST model at least three user roles — Merchant (Owner), Affiliate
  Marketer, and Admin/Staff — and associate each user account with a primary role.
- **FR-008**: Unauthenticated requests to private (role-restricted) pages MUST redirect to the
  login page; after successful login the user MUST arrive at their role home (or the originally
  requested page if they are permitted to view it).
- **FR-009**: Users MUST be able to log out, which ends their session and returns them to a
  public/auth page.
- **FR-010**: The application MUST provide separate base layouts for the public/auth surface,
  the merchant surface, and the affiliate surface, keeping the merchant and affiliate shells
  visually independent.
- **FR-011**: Repeated shell regions (merchant header/sidebar; affiliate header/sidebar/
  bottom-nav) MUST be expressed as shared, reusable includes rather than duplicated per page.
- **FR-012**: At least one page on each surface (public/auth, merchant, affiliate) MUST be
  converted to render through template inheritance (extending its base) while remaining visually
  identical to the static original.
- **FR-013**: Existing inter-page navigation links MUST continue to resolve to the correct
  served pages; the conversion MUST NOT introduce dead links.
- **FR-014**: All form submissions handled by the application (e.g., login) MUST include
  cross-site request forgery protection.
- **FR-015**: Configuration MUST support a relational database — a lightweight local database
  for development and a production-grade relational database for deployment — with secrets
  supplied via environment configuration, no secrets committed to source, and debug behavior
  disabled in the production configuration.
- **FR-016**: This phase MUST NOT implement domain data management (create/edit/delete for
  products, orders, customers, affiliates, commissions, payouts, or landing pages) beyond
  serving their existing pages; those pages keep their hardcoded prototype content until later
  phases convert them.
- **FR-017**: The conversion MUST NOT introduce any frontend framework, single-page-app routing,
  client-facing API layer, or Node/JavaScript build system, and MUST NOT replace any product
  page with an administrative/back-office screen.
- **FR-018**: When a login attempt fails (invalid credentials), the application MUST re-render the
  login page with a single generic error message and MUST NOT disclose which field (login
  identifier or password) was incorrect.
- **FR-019**: The login form MUST authenticate using the credential the preserved UI collects (an
  email address) without altering that field's appearance: the application MUST resolve the entered
  email to its account via an email-or-username authentication backend. `username` remains the
  canonical unique identifier; `email` MUST be unique to allow unambiguous email login.

### Key Entities *(include if feature involves data)*

- **User Account**: An authenticatable identity with credentials and a primary role. `username` is
  the canonical unique identifier (Django default `AbstractUser`), but users authenticate by
  entering their **email** in the preserved login form, resolved to the account via an
  email-or-username authentication backend; `email` MUST be unique. Foundation scope only requires
  identity + role; rich per-role profiles are added in later phases.
- **Role**: The access category of a user — one of Merchant (Owner), Affiliate Marketer, or
  Admin/Staff — used to drive post-login redirect and access scoping.
- **Surface (conceptual)**: One of three rendering contexts — public/auth, merchant, affiliate —
  each with its own base layout and shared shell includes. Not persisted data, but the
  organizing concept for the template architecture.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of the existing prototype pages are reachable through the running application
  and render visually identical to their static versions (verified by visual comparison across
  a representative set from all three surfaces).
- **SC-002**: Zero broken static-asset requests (no missing CSS, JS, icons, or images) across
  the served pages.
- **SC-003**: Zero regressions in interactive behavior — theme toggle, dropdowns, modals, tabs,
  copy buttons, favorite toggles, gallery switching, and affiliate bottom-nav all work on the
  converted pages and a sampled set of served pages.
- **SC-004**: A merchant test account always lands on the merchant dashboard and an affiliate
  test account always lands on the affiliate dashboard after login (correct redirect in 100% of
  attempts).
- **SC-005**: An unauthenticated request to a private page redirects to login in 100% of
  attempts.
- **SC-006**: A developer can start the application from a clean checkout and load the home page
  using a short, documented setup (no more than 6 documented commands, completing in minutes).
- **SC-007**: Zero dead internal links across served pages — internal navigation integrity
  matches the static prototype.
- **SC-008**: At least one page per surface (3 total) is confirmed rendering through template
  inheritance while remaining visually identical to its static original.

## Assumptions

- The technology stack is fixed by the project constitution: Python + Django + Django templates,
  a relational database (a lightweight local database for development, production-grade
  relational database ready for deployment), the existing HTML/CSS/JS assets, and Tailwind/
  Lucide via CDN as already present in the HTML. This spec treats the stack as a constraint, not
  an open choice.
- **Inter-page link strategy (chosen default)**: the application's URLs will initially mirror the
  existing page filenames so the prototype's `href="…​.html"`-style links keep resolving without
  rewriting. Cleaner URL paths may be introduced later as pages are converted. (Alternative
  considered: rewrite all links to clean URLs now — rejected for this phase as higher-risk and
  unnecessary for the foundation.)
- The "first working route conversion" targets are the login/auth page (public/auth surface),
  the merchant dashboard (merchant surface), and the affiliate dashboard (affiliate surface).
- In this phase **"converted" means converted to template inheritance only** (extending a base +
  shared includes), NOT made database-backed. The template-converted dashboards intentionally keep
  their hardcoded prototype content (FR-016); constitution Principle V's database-backed-truth rule
  applies only when a page is later **data-converted**, so these pages are not judged against it yet.
- Registration creates a Merchant account by default; affiliate accounts are primarily created
  and approved through the affiliate flow in a later phase. The login page's existing role
  selector is **informational only**; post-login routing is determined by the authenticated
  account's stored role, not by the selector.
- Full role-based authorization (per-page role gating across every page and object-ownership
  checks) is established *structurally* in this phase (role model + login-required + redirect
  skeleton) and completed surface-by-surface in later phases. The three **converted** private pages
  (merchant + affiliate dashboards) DO enforce role-specific access now; the remaining
  login-required raw registry pages enforce login only — cross-role access to them is acceptable in
  this phase **because they serve no owner-scoped data** (only static prototype content, per FR-016
  and Principle V), so Principle IV's data-isolation rationale is not yet engaged. Exhaustive
  per-page role gating and object-ownership checks land as each page is data-converted.
- The existing `assets/` folder is served unchanged; asset references in the HTML are not
  rewritten.
- Seed/demo data and the full domain models (products, orders, commissions, payouts, etc.) are
  out of scope for this foundation phase and arrive in subsequent phases.
- Visual "identical" is judged by human review/screenshot comparison of representative pages,
  not an automated pixel-diff harness (none exists in the prototype).

## Dependencies

- The existing static prototype (features `001-static-frontend-mvp` and
  `002-affiliate-seller-portal`) is the input artifact; this phase reuses its HTML/CSS/JS as-is.
- The project constitution (`.specify/memory/constitution.md`, v2.0.0) governs the allowed and
  forbidden technologies and the frontend-preservation rule.
