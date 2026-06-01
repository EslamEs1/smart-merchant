# Research & Decisions: Merchant Affiliate Management (MVP Phase 2)

**Feature**: 005-affiliate-management
**Date**: 2026-06-01

The spec carries **no `[NEEDS CLARIFICATION]`** markers; the one design fork was resolved to a default in
spec Assumptions. This document records the load-bearing technical decisions so `/speckit-tasks` and
implementation are unambiguous. Each entry: **Decision · Rationale · Alternatives considered**.

---

## D1 — Single model (`AffiliateProfile`); a Pending profile *is* the join request

**Decision**: Model the whole surface with one `AffiliateProfile`. Status `Pending` represents an
unreviewed join request; `/affiliates/requests/` lists Pending profiles; approve → `Active`, reject →
`Rejected`. Do **not** introduce a separate `AffiliateApplication` this phase.

**Rationale**: The profile already carries every field the requests page needs (full name, contact,
social handles, and `bio` which absorbs the applicant "experience" paragraph). One model keeps the
lifecycle, the roster, and the requests queue consistent by construction and avoids a second table plus a
copy-on-approve step. It directly satisfies the business rules ("affiliate starts as Pending", "merchant
can approve / reject").

**Alternatives considered**: (a) Separate `AffiliateApplication` with copy-to-profile on approval —
rejected as premature for an MVP; it duplicates fields and adds a sync seam with no current payoff. The
spec marks it "optional / if separate," so it stays an explicitly deferred extension point.

## D2 — `merchant` and `user` both target `AUTH_USER_MODEL`; `user` is optional

**Decision**: `merchant = FK(settings.AUTH_USER_MODEL, on_delete=CASCADE, related_name="affiliates")`
(the owner, role MERCHANT). `user = FK(settings.AUTH_USER_MODEL, null=True, blank=True,
on_delete=SET_NULL, related_name="affiliate_links")` — the affiliate's own login account, **optional**
this phase.

**Rationale**: The `merchants` app model is empty; `004` already scopes ownership directly to the
`accounts.User` with role MERCHANT, so reusing `AUTH_USER_MODEL` keeps the codebase consistent.
Affiliate login / the seller portal is a separate later spec, so an affiliate created or approved by a
merchant must be fully manageable **without** a linked account — hence `user` is nullable and
`SET_NULL` (deleting a user must not delete the merchant's affiliate record).

**Alternatives considered**: (a) `OneToOneField(user)` — rejected: over-constrains the (future)
case of one person affiliating under multiple merchants and adds nothing while the field is mostly empty.
(b) FK to a `merchants.Merchant` model — rejected: that model doesn't exist; introducing it is out of
scope and would diverge from `004`.

## D3 — `referral_link` is a derived property, not a stored column

**Decision**: Store only `referral_code` (globally unique). Expose `referral_link` as a model
**property** returning the prototype's `https://smartmerchant.os/r/<referral_code>` form. The base host
is a single module-level constant.

**Rationale**: A stored link would be a second source of truth that can drift from the code. The
prototype always shows `…/r/<CODE>`, so deriving it guarantees consistency on the roster, the detail
referral box, and the copy buttons. The spec lists `referral_link` as a "field" conceptually; a derived
property satisfies every display/uniqueness requirement without redundancy (recorded in spec
Assumptions).

**Alternatives considered**: stored `URLField` synced on save — rejected as redundant and drift-prone.

## D4 — Code uniqueness scopes: referral global, coupon per-merchant (blanks allowed)

**Decision**: `referral_code` → `unique=True` (global). `coupon_code` → `UniqueConstraint(fields=
["merchant","coupon_code"], condition=~Q(coupon_code=""), name="uniq_coupon_per_merchant")`, i.e. unique
per merchant **only for non-blank values** so multiple affiliates may have no coupon yet.

**Rationale**: Matches FR-017/018 precisely. A referral code resolves a public `/r/<code>` link, so it
must be globally unambiguous. A coupon is the merchant's own discount namespace, so the same string may
recur under a different merchant. The partial condition avoids a spurious collision on empty coupons
(the `004` precedent used the same "allow blanks, enforce non-blank" reasoning for slugs).

**Alternatives considered**: global coupon uniqueness — rejected as contradicting FR-018; unconditional
per-merchant uniqueness — rejected because it would forbid more than one blank-coupon affiliate per
merchant.

## D5 — Lifecycle as a guarded service layer, not model signals

**Decision**: Put the state model in `services.py`: `approve` (Pending→Active, set `approved_at`),
`reject` (Pending→Rejected, set `rejected_at`), `suspend` (Active→Suspended, set `suspended_at`),
`reactivate` (Suspended→Active), `change_level` (any status; validates the value),
`set_notes` (any status). Each transition **guards its precondition**: acting on a profile already in a
terminal/incompatible state is an idempotent no-op (or rejected) and never overwrites an existing
timestamp misleadingly. Timestamps use `django.utils.timezone.now()`.

**Rationale**: Mirrors `004`'s `services.py` (`set_product_status`, `duplicate_product`). Keeping logic
out of views and signals makes the transitions unit-testable in isolation and keeps `clean()` for pure
field validation. Guards satisfy the spec's "already-decided request" and "invalid level" edge cases.

**Alternatives considered**: a generic `set_status(status)` like `004` — rejected because each affiliate
transition also stamps a distinct timestamp and has distinct preconditions, so named services read
clearer and test better. Model `save()`/signal side-effects — rejected for testability and
explicitness.

## D6 — Clean URLs keyed by numeric id; legacy `*.html` redirects

**Decision**: `/affiliates/`, `/affiliates/requests/`, `/affiliates/<int:pk>/`, and per-affiliate action
URLs under `/affiliates/<int:pk>/…/`, with permanent redirects from `affiliates.html`,
`affiliate-detail.html`, `affiliate-requests.html`. Place `requests/` before `<int:pk>/` for clarity
(the `int` converter already excludes the word "requests").

**Rationale**: The spec mandates id-keyed URLs (`/affiliates/<id>/`). Unlike products there is no
human-facing public slug requirement for affiliates, so the numeric pk is the natural, stable key.
Legacy redirects preserve every inbound link from not-yet-converted pages (Principle I — no dead links),
exactly as `004` did.

**Alternatives considered**: slug from referral code — rejected: referral codes can change and aren't a
URL identity; pk is stable and matches the spec.

## D7 — Out-of-scope figures render as truthful zeros / empty-state

**Decision**: Every order / commission / payout figure on the three pages renders truthfully empty: the
roster's orders / sales / pending-commission / paid-commission / conversion columns show `0`; the detail
page's stat cards show `0`, and its attributed-orders table, payout-history table, and marketing-captions
sections show their existing empty-states. The commission-rule banner and `data-copy` controls are
preserved.

**Rationale**: Constitution Principle V — a converted page must show DB truth or an empty-state, never
carried-over fabricated rows. Zero orders/commissions genuinely exist this phase, so zeros/empty-states
are *true*, not placeholders-that-lie. This is the exact treatment `004` applied to the product-detail
"sales summary." The prompt's "minimal placeholders for display" is read this way.

**Alternatives considered**: deleting the widgets — rejected (Principle I markup preservation); keeping
the static sample numbers — rejected (Principle V violation, "fake dynamic data").

## D8 — In-style UI additions strictly required for backend integration

**Decision**: Supply the list page's **triggered-but-undefined** confirmation modals (approve / suspend /
change-level) as per-affiliate POST+CSRF modals (change-level carries a Level `<select>`), and add an
in-style **notes-edit** affordance to the detail page. Both in the prototype's exact style.

**Rationale**: The prototype's list dropdown references `modal-approve` / `modal-suspend` /
`modal-change-level` but ships **no modal bodies**, so the buttons are inert; FR-006/012/014 require them
to work. The detail notes block is read-only text but FR-015 requires merchant editing. Principle I
permits changes "strictly required for backend integration"; these complete the prototype's own intent
rather than redesigning it. Recorded in plan Complexity Tracking.

**Alternatives considered**: leaving the actions in the dropdown only without confirmation (riskier UX,
and the triggers already imply modals); editing notes via admin only — rejected because FR-015 is
merchant-facing.

## D9 — No new dependency; no media pipeline

**Decision**: Add nothing to `requirements/`. No `ImageField`, so no Pillow and no `MEDIA_*`/`static()`
media serving. Affiliate avatars and the QR code stay `{% static %}` placeholder assets.

**Rationale**: This phase has no uploads. Avoiding Pillow/media keeps the change minimal and the
constitution's "minimal" bar satisfied. Real QR generation is explicitly out of scope.

**Alternatives considered**: adding an avatar `ImageField` now — rejected as out of scope (no upload
requirement in the spec).

## D10 — Reuse the `004` test taxonomy

**Decision**: Test buckets: models (uniqueness/defaults/property), selectors (isolation + filters),
services (transitions + guards), and views (access, owner-scope 404, `require_POST` 405, CSRF 403,
filters, empty-state, persistence) — run via `manage.py test apps.affiliates`.

**Rationale**: `004` proved this taxonomy catches the constitution's load-bearing concerns (Principle IV
isolation, security gates, truthful empty-states). Reusing it keeps coverage consistent across the two
conversions.

**Alternatives considered**: lighter happy-path-only tests — rejected; owner isolation and CSRF are
NON-NEGOTIABLE and must be asserted, as in `004`.
