# Feature Specification: Merchant Affiliate Management

**Feature Branch**: `005-affiliate-management`
**Created**: 2026-06-01
**Status**: Draft
**Input**: User description: "Smart Merchant OS Backend MVP — Merchant Affiliate Management. Convert the merchant-side affiliate management pages (`affiliates.html`, `affiliate-detail.html`, `affiliate-requests.html`) into database-backed Django pages while preserving the existing frontend design. Focus on affiliate profiles, approval workflow, levels, referral codes, coupon codes, affiliate status, and merchant visibility. Do not implement the full order/commission engine — minimal placeholders are acceptable for display only."

## Overview

This feature is the **second data conversion** on top of the Django foundation (after `004-products-catalog`).
It turns the three merchant-side affiliate management pages into a database-backed, merchant-owned
affiliate roster in `apps/affiliates`. The affiliate system is the product's stated core differentiator
(constitution Principle VI), so faithful modeling of the affiliate lifecycle — registration → approval /
rejection → levels → suspension — is the heart of this phase.

The phase deliberately stops short of the commission/order/payout machinery. The prototype's affiliate
pages display order counts, sales totals, pending/paid commission, conversion rates, attributed-order
tables, and payout histories — **all of which depend on subsystems that do not exist yet**. Per
constitution Principle V (Database-Backed Truth — No Fake Dynamic Data), those out-of-scope figures MUST
render as **truthful zeros / empty states**, never as carried-over hardcoded sample numbers. This mirrors
how `004` rendered the product-detail "sales summary" as truthful zeros.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Browse the affiliate roster (Priority: P1)

A merchant opens the المسوقون (affiliates) page and sees every affiliate connected to **their own**
business, drawn from the database — name, level badge, referral code, status badge, and the
(currently-zero) performance columns — with working search, status filter, and level filter. When the
merchant has no affiliates, the existing empty-state UI appears instead of fabricated rows.

**Why this priority**: The roster is the landing surface for the entire affiliate subsystem and the
minimum viable slice — without a real, owner-scoped list there is nothing to act on. It is independently
demonstrable on its own.

**Independent Test**: Seed two merchants with distinct affiliates, log in as one, load `/affiliates/`,
and confirm only that merchant's affiliates render, that the three filters narrow the list correctly, and
that a merchant with zero affiliates sees the empty state.

**Acceptance Scenarios**:

1. **Given** a merchant with 5 seeded affiliates, **When** they open `/affiliates/`, **Then** all 5
   render from the database with correct name, level badge, referral code, and status badge.
2. **Given** the roster, **When** the merchant filters by status = `Active`, **Then** only Active
   affiliates remain; filtering by level = `Gold` shows only Gold affiliates; searching a name or
   referral code narrows to matching rows.
3. **Given** a merchant with no affiliates, **When** they open `/affiliates/`, **Then** the existing
   empty-state UI is shown and no fabricated rows appear.
4. **Given** the roster, **When** it renders, **Then** the performance columns (orders, sales, pending
   commission, paid commission, conversion rate) display truthful zeros — not carried-over sample data.

---

### User Story 2 - Review and decide on join requests (Priority: P1)

A merchant opens the طلبات الانضمام (join requests) page, reviews each pending applicant's details
(name, contact, social presence, experience note), and either **approves** (activating the affiliate) or
**rejects** (with an optional reason) using the existing confirmation modals. The request count badge and
the list reflect the real number of pending affiliates.

**Why this priority**: Approval/rejection is the affiliate lifecycle's entry gate and the core
differentiator's defining workflow (constitution Principle VI). It is independently valuable: a merchant
can grow their affiliate network the moment this works.

**Independent Test**: Seed a Pending affiliate, log in as its merchant, open `/affiliates/requests/`,
approve it, and confirm its status becomes Active and it leaves the requests list; repeat with reject and
confirm status becomes Rejected.

**Acceptance Scenarios**:

1. **Given** a merchant with pending applicants, **When** they open `/affiliates/requests/`, **Then**
   each Pending affiliate renders as a request card with its real details, and the request count reflects
   the true pending total.
2. **Given** a pending request, **When** the merchant confirms approval, **Then** the affiliate's status
   becomes `Active`, its `approved_at` is set, and it disappears from the requests list.
3. **Given** a pending request, **When** the merchant confirms rejection (optionally with a reason),
   **Then** the affiliate's status becomes `Rejected`, its `rejected_at` is set, and it disappears from
   the requests list.
4. **Given** no pending requests, **When** the merchant opens `/affiliates/requests/`, **Then** the
   existing empty-state UI is shown.

---

### User Story 3 - Inspect an affiliate's profile (Priority: P2)

A merchant opens an affiliate's detail page and sees their real profile: identity and contact, level and
status badges, referral link, coupon code chip, QR placeholder, notes, and social links. Sections that
depend on out-of-scope subsystems (attributed orders, payout history, marketing captions, performance
stat cards) render as truthful empty states / zeros, preserving the page's layout exactly.

**Why this priority**: The detail view is where a merchant verifies an affiliate's identity and shares
their referral assets. It builds on US1 but is a distinct, demonstrable surface.

**Independent Test**: Seed an affiliate, open `/affiliates/<id>/`, and confirm the profile, referral
link (derived from the referral code), coupon chip, and notes render real data while the orders/payouts
sections show empty states.

**Acceptance Scenarios**:

1. **Given** an existing affiliate, **When** the merchant opens `/affiliates/<id>/`, **Then** name,
   contact, level badge, status badge, referral link, coupon code, and notes render from the database.
2. **Given** the detail page, **When** it renders, **Then** the referral link, QR placeholder, and coupon
   chip copy controls keep working (the `data-copy` hooks are preserved).
3. **Given** the detail page, **When** it renders, **Then** the attributed-orders table, payout-history
   table, and performance stat cards show truthful empty states / zeros rather than sample rows.

---

### User Story 4 - Change an affiliate's standing (Priority: P2)

From the roster or the detail page, a merchant **suspends** an active affiliate (optionally with a
reason), **reactivates** a suspended one, **changes an affiliate's level** (Bronze / Silver / Gold /
Platinum), and **edits the affiliate's notes** — each through the existing dropdown/modal UI, each
persisted to the database.

**Why this priority**: Ongoing lifecycle management keeps the roster accurate over time. It depends on the
roster (US1) existing but adds clearly separable value.

**Independent Test**: For a seeded Active affiliate, suspend it and confirm status = Suspended +
`suspended_at` set; change its level and confirm the new level persists and its badge updates; edit notes
and confirm they persist.

**Acceptance Scenarios**:

1. **Given** an Active affiliate, **When** the merchant confirms suspension, **Then** status becomes
   `Suspended`, `suspended_at` is set, and the status badge updates.
2. **Given** a Suspended affiliate, **When** the merchant reactivates it, **Then** status returns to
   `Active`.
3. **Given** any affiliate, **When** the merchant changes its level, **Then** the new level persists and
   the level badge reflects it across the roster and detail page.
4. **Given** any affiliate, **When** the merchant edits the notes, **Then** the new notes persist and
   render on the detail page.

---

### User Story 5 - Owner-scoped isolation and role protection (Priority: P1)

A merchant can only see and act on affiliates connected to their own merchant account. Attempting to view
or mutate another merchant's affiliate fails (not found). Affiliate-role and anonymous users cannot reach
any merchant affiliate-management page.

**Why this priority**: This is constitution Principle IV (NON-NEGOTIABLE). Cross-actor data leakage on a
money-adjacent subsystem is a critical-severity failure, not a polish item, so it is verified as a
first-class, independently testable story.

**Independent Test**: As merchant A, request merchant B's affiliate detail and every mutation URL and
confirm each returns 404; log in as an affiliate-role user and confirm every `/affiliates/...` page is
forbidden; as anonymous, confirm redirect to login.

**Acceptance Scenarios**:

1. **Given** merchant A logged in, **When** A opens or POSTs to any URL for merchant B's affiliate,
   **Then** the response is 404 (object-ownership enforced at the queryset level).
2. **Given** an affiliate-role user, **When** they open any `/affiliates/...` management page, **Then**
   access is denied (403 / role guard), never the page.
3. **Given** an anonymous visitor, **When** they open any `/affiliates/...` page, **Then** they are
   redirected to login.
4. **Given** any state-changing action (approve, reject, suspend, reactivate, change level, edit notes),
   **When** it is requested via GET or without a valid CSRF token, **Then** it is rejected (405 / 403)
   and no data changes.

### Edge Cases

- **Already-decided request**: approving/rejecting an affiliate that is no longer Pending (e.g.
  double-submit) MUST NOT corrupt state — the action is a no-op or is rejected, and timestamps already set
  are not overwritten misleadingly.
- **Invalid level value**: a change-level request with a value outside Bronze/Silver/Gold/Platinum MUST be
  rejected without persisting.
- **Duplicate referral code**: creating/seeding an affiliate whose referral code already exists (globally)
  MUST be prevented.
- **Duplicate coupon code within one merchant**: two affiliates of the same merchant MUST NOT share a
  coupon code; the same coupon string MAY exist under a different merchant.
- **Affiliate without a linked user account**: an affiliate that has no login account yet (created/approved
  by the merchant) MUST still display and be manageable; the missing account MUST NOT break the page.
- **Empty filter result**: a filter combination that matches nothing MUST show the empty-state UI, not a
  broken/zero-row table.
- **Out-of-scope action affordances**: prototype affordances that point at not-yet-built subsystems
  (e.g. "دفع عمولة" / pay commission, "عرض الطلبات" / view orders, "صرف العمولة" / disburse commission)
  MUST remain visually present (Principle I) but MUST NOT fabricate data or imply completed money
  movement.

## Requirements *(mandatory)*

### Functional Requirements

**Roster & filtering**

- **FR-001**: The system MUST render `/affiliates/` with one row per affiliate owned by the logged-in
  merchant, sourced entirely from the database.
- **FR-002**: The roster MUST support server-side filtering by free-text search (name and referral code),
  by status (Pending / Active / Suspended / Rejected), and by level (Bronze / Silver / Gold / Platinum),
  reflecting the existing filter-bar controls.
- **FR-003**: When the merchant owns no affiliates (or a filter matches none), the roster MUST render the
  existing empty-state UI and MUST NOT render fabricated rows.
- **FR-004**: The roster's performance columns (orders, sales, pending commission, paid commission,
  conversion rate) MUST display truthful zeros for this phase (commission/order subsystems are out of
  scope), never carried-over sample values.

**Join requests & approval workflow**

- **FR-005**: The system MUST render `/affiliates/requests/` listing the merchant's Pending affiliates as
  request cards showing their real details, with the pending count reflected truthfully.
- **FR-006**: A merchant MUST be able to **approve** a Pending affiliate, transitioning it to `Active` and
  recording `approved_at`.
- **FR-007**: A merchant MUST be able to **reject** a Pending affiliate with an optional reason,
  transitioning it to `Rejected` and recording `rejected_at`.
- **FR-008**: The requests page MUST support search; date-of-request and status affordances MAY be
  surfaced where the prototype provides them.

**Detail view**

- **FR-009**: The system MUST render `/affiliates/<id>/` showing the affiliate's identity, contact, level
  badge, status badge, referral link, coupon code, QR placeholder, notes, and social links from the
  database.
- **FR-010**: The detail view's out-of-scope sections (attributed-orders table, payout-history table,
  marketing captions, performance stat cards) MUST render truthful empty states / zeros.
- **FR-011**: The detail view MUST preserve the commission-rule banner and all `data-copy` controls
  (referral link, coupon code) so copy interactions keep working.

**Lifecycle mutations**

- **FR-012**: A merchant MUST be able to **suspend** an affiliate with an optional reason, transitioning it
  to `Suspended` and recording `suspended_at`.
- **FR-013**: A merchant MUST be able to **reactivate** a Suspended affiliate back to `Active`.
- **FR-014**: A merchant MUST be able to **change an affiliate's level** to any of Bronze / Silver / Gold /
  Platinum; invalid values MUST be rejected.
- **FR-015**: A merchant MUST be able to **edit an affiliate's notes**, persisting the change.
- **FR-016**: Affiliate status MUST follow a defined state model: new affiliates start `Pending`; Pending →
  Active (approve) or Rejected (reject); Active → Suspended (suspend); Suspended → Active (reactivate);
  level changes are allowed independent of status. Transitions that are not defined MUST NOT be silently
  applied.

**Codes & links**

- **FR-017**: Each affiliate's referral code MUST be unique across the whole system.
- **FR-018**: Each affiliate's coupon code MUST be unique per merchant (the same string MAY recur under a
  different merchant).
- **FR-019**: The referral link MUST be derived consistently from the referral code (the existing
  `…/r/<code>` form) and displayed wherever the prototype shows it.

**Access control & integrity**

- **FR-020**: Every affiliate-management page and action MUST require login and the merchant role;
  affiliate-role and anonymous users MUST be denied (role guard), never shown the page.
- **FR-021**: Every read and write MUST be owner-scoped: a merchant MUST only see and mutate affiliates
  connected to their own merchant account, enforced at the queryset level; cross-merchant access MUST
  return not-found.
- **FR-022**: All state-changing actions (approve, reject, suspend, reactivate, change level, edit notes)
  MUST be performed via POST with CSRF protection; GET or missing-CSRF requests MUST be rejected without
  changing data.

**Conversion fidelity, URLs, admin, seed**

- **FR-023**: The converted pages MUST preserve the existing frontend exactly — affiliate table, level
  badges, status badges, action dropdowns, confirmation modals, commission-rule banner, referral-link
  display, QR placeholder, coupon-code chip, RTL layout, theme toggle, and every `data-*` JS hook
  (constitution Principle I).
- **FR-024**: The affiliate surface MUST adopt clean URLs (`/affiliates/`, `/affiliates/<id>/`,
  `/affiliates/requests/`, and the per-affiliate action URLs) with legacy redirects from `affiliates.html`,
  `affiliate-detail.html`, and `affiliate-requests.html` so no inbound link breaks.
- **FR-025**: The system MUST register `AffiliateProfile` (and `AffiliateApplication` if introduced) in
  Django admin with list display, status filter, level filter, and search by name / email / phone /
  referral code / coupon code.
- **FR-026**: The system MUST provide an idempotent seed of demo affiliates connected to the demo merchant:
  أحمد الشمري (Gold / Active / `AHMAD20`), سارة المنصور (Silver / Active), محمد العتيبي (Bronze / Pending),
  Nora Ahmed (Platinum / Active), خالد سالم (Suspended) — physical-commerce affiliate context only.

### Key Entities *(include if feature involves data)*

- **AffiliateProfile**: a marketer connected to one merchant. Attributes: optional linked user account,
  owning merchant, full name, phone, email, city, country, status (Pending / Active / Suspended /
  Rejected), level (Bronze / Silver / Gold / Platinum), globally-unique referral code, referral link
  (derived from code), per-merchant-unique coupon code, bio, social handles (Instagram / TikTok /
  Facebook), merchant notes, lifecycle timestamps (`approved_at`, `rejected_at`, `suspended_at`), and
  created/updated timestamps. A Pending profile doubles as a join request for this phase.
- **AffiliateApplication** *(optional, deferred)*: a separate intake record (merchant, contact, social
  links, experience, status Pending/Approved/Rejected, submitted/reviewed timestamps, reviewer). Not
  introduced in this phase unless review determines the single-model approach is insufficient — see
  Assumptions.
- **Merchant (existing)**: the owner account (`accounts.User` with the merchant role); every affiliate is
  scoped to exactly one merchant.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A merchant can view their affiliate roster from the database, and 100% of rows shown belong
  to that merchant (zero cross-merchant rows).
- **SC-002**: A merchant can approve a pending affiliate and reject another, with the affiliate's status
  and the requests list updating to match in the same session.
- **SC-003**: A merchant can suspend an active affiliate, reactivate a suspended one, and change an
  affiliate's level, with every change persisted and reflected on reload.
- **SC-004**: Referral code and coupon code display correctly on the roster and detail page for every
  affiliate, and duplicate referral codes (globally) or duplicate coupon codes (within a merchant) are
  prevented.
- **SC-005**: All three filters (search, status, level) return correct subsets, and any zero-result view
  shows the empty state.
- **SC-006**: 100% of cross-merchant access attempts (view or mutate another merchant's affiliate) return
  not-found, and 100% of affiliate-role/anonymous access attempts to management pages are denied.
- **SC-007**: The converted pages are visually indistinguishable from the static originals (RTL, badges,
  dropdowns, modals, commission banner, referral/QR/coupon blocks, theme toggle) with no broken JS hooks.
- **SC-008**: No converted page renders any hardcoded sample affiliate, order, commission, or payout row;
  out-of-scope figures read as truthful zeros / empty states.

## Assumptions

- **Single-model approval (default)**: this phase models a join request as an `AffiliateProfile` with
  status `Pending`; the requests page lists Pending profiles, approval flips to `Active`, rejection to
  `Rejected`. A separate `AffiliateApplication` model is treated as optional/deferred because the prompt
  marks it "optional / if separate" and the profile already carries the needed fields (bio, social
  handles, notes). This can be revisited in `/speckit-clarify` if a distinct intake record is required.
- **Out-of-scope figures render as truthful zeros / empty states** (constitution Principle V), matching the
  `004` product-detail precedent. The prompt's "minimal placeholders … for display" is interpreted as
  truthful zeros, not fabricated numbers.
- **Affiliate login accounts are out of scope here**: the `user` link is optional and may be empty; the
  affiliate **seller portal** (its own login/surface) is a separate, later spec. "Affiliate cannot access
  merchant pages" is enforced via the merchant role guard, consistent with `003`/`004`.
- **Identifier in URLs**: affiliate detail/action URLs use the affiliate's numeric id (`/affiliates/<id>/`)
  as stated in the prompt, with legacy `*.html` redirects — consistent with the clean-URL + legacy-redirect
  approach established in `004`.
- **Two endpoints added beyond the source URL list**: a `reactivate` action (`/affiliates/<id>/reactivate/`)
  and a `notes` action (`/affiliates/<id>/notes/`) are added to satisfy **FR-013** (reactivate a suspended
  affiliate) and **FR-015** (edit affiliate notes), which the prompt's URL list omitted. Both are
  POST + CSRF + owner-scoped like the other mutations (see contracts/routes.md).
- **Referral link form** follows the prototype's `https://smartmerchant.os/r/<referral_code>` pattern and
  is derived from the code rather than stored as an independent source of truth.
- **Status tokens stay in English** in the UI (Pending / Active / Suspended / Rejected; Bronze / Silver /
  Gold / Platinum), matching the prototype and constitution; all other copy stays Arabic/RTL.
- **Reuse of the foundation**: `accounts.User` + role, `@role_required("is_merchant")`, the merchant base
  template/shell, the page registry, and static-asset serving from `003`/`004` are prerequisites and are
  reused as-is.

## Dependencies

- **Backend foundation** (`003-backend-foundation`): Django skeleton, `accounts.User` + role, role-based
  access guards, merchant base layout, and static serving.
- **Products catalog** (`004-products-catalog`): established the data-conversion pattern (owner-scoped
  selectors/services, clean URLs + legacy redirects, POST+CSRF mutations, truthful empty states, idempotent
  seed) that this phase follows.
- **Static prototype** (`001`/`002`): the three pages `affiliates.html`, `affiliate-detail.html`,
  `affiliate-requests.html` are the input artifacts whose markup, classes, `data-*` hooks, modals, badges,
  and RTL layout are preserved.
- **Project constitution** (v2.0.0): governs frontend preservation (Principle I), modular apps (III),
  data-isolation (IV), database-backed truth (V), affiliate integrity (VI), and physical-commerce framing
  (VIII).

## Out of Scope

- The full commission engine: commission creation, the Pending→Approved→Paid state machine, affiliate
  earnings calculation, and any real money movement.
- Order attribution and the affiliate-attributed orders data behind the detail page's tables.
- Payout requests and payout approval/rejection/paid flow.
- The affiliate **seller portal** dynamic pages (`affiliate-dashboard.html`, `affiliate-earnings.html`,
  etc.) — a separate spec.
- Real QR-code generation (the QR placeholder image is preserved as-is).
- Real WhatsApp / email / notification integrations (approval "sends an email" copy is cosmetic only).
- Affiliate self-registration from a public page; merchant-driven creation/management is the surface here.
