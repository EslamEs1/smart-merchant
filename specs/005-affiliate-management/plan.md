# Implementation Plan: Merchant Affiliate Management (Database-Backed Conversion — MVP Phase 2)

**Branch**: `005-affiliate-management` | **Date**: 2026-06-01 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/005-affiliate-management/spec.md`

## Summary

Convert the three merchant-side affiliate pages (`affiliates.html`, `affiliate-detail.html`,
`affiliate-requests.html`) into a real, database-backed, **merchant-owned** affiliate roster inside the
`apps/affiliates` Django app — the second *data conversion* after `004-products-catalog`. Introduce one
model (`AffiliateProfile`) that captures the affiliate lifecycle the constitution calls the product's
core differentiator (Principle VI): identity/contact, status (Pending / Active / Suspended / Rejected),
level (Bronze / Silver / Gold / Platinum), globally-unique referral code, per-merchant-unique coupon
code, social handles, merchant notes, and lifecycle timestamps. A **Pending profile doubles as a join
request**, so no separate `AffiliateApplication` is needed this phase.

Merchant views cover the roster (list with server-side search/status/level filtering + empty state), the
join-requests queue, the affiliate detail page, and the lifecycle mutations (approve, reject, suspend,
reactivate, change level, edit notes) — every read and write **owner-scoped** at the queryset level
(Principle IV) and every mutation **POST + CSRF** (security gate). The surface moves to **clean URLs**
(`/affiliates/…`) with legacy `*.html` redirects so no inbound link breaks.

Because orders, commissions, and payouts do **not** exist yet, every order/commission/payout figure on
these pages (roster performance columns; detail stat cards, attributed-orders and payout-history tables,
marketing captions) renders as **truthful zeros / empty state** (Principle V) — never carried-over sample
data. The prototype UI is preserved exactly, with bounded **in-style additions** required for backend
integration (recorded in Complexity Tracking): the list page's *triggered-but-undefined* confirmation
modals are supplied, and the detail page gains an in-style notes-edit affordance. No SPA, API, DRF,
Pillow, or Node build is introduced.

## Technical Context

**Language/Version**: Python 3.12 (repo `venv/`).
**Primary Dependencies**: Django 5.x (server-rendered templates + ModelForms + admin). **No new runtime
dependency** — unlike `004` there is no `ImageField`, so no Pillow/media additions. No DRF, no Node/
bundler, no SPA framework.
**Storage**: SQLite for local dev; PostgreSQL-ready for production (env-configured). One new table:
`affiliates_affiliateprofile` (migration `0001_initial`).
**Testing**: Django test runner (`manage.py test apps.affiliates`) for models/selectors/services/forms/
views (ownership isolation, code uniqueness, filters, the approval/lifecycle state model, role+CSRF
gates); manual visual-parity acceptance per `quickstart.md`.
**Target Platform**: Linux server (WSGI/gunicorn in production); local `runserver` for dev.
**Project Type**: Web application (server-rendered Django + existing static frontend).
**Performance Goals**: Parity with the static prototype; roster query paginated with `select_related`
on the optional `user` and ordered by `-created_at`; counts (pending badge) computed, not hardcoded.
**Constraints**: Frontend visually unchanged except the bounded in-style additions required for backend
integration (Principle I); merchant data isolation at the queryset level (Principle IV, NON-NEGOTIABLE);
all dynamic content DB-backed with truthful empty/zero states (Principle V); affiliate lifecycle modeled
faithfully while commission/order/payout machinery stays out of scope and never fabricated (Principle
VI); CSRF on every mutation; secrets via env; no forbidden tech.
**Scale/Scope**: 1 model; 1 app gains full code; 3 templates converted; 12 routes (9 clean — incl.
`requests` — + 3 legacy redirects); 5 seeded demo affiliates; 1 seed command.

*No NEEDS CLARIFICATION remain — the one design fork (single-model vs. `AffiliateApplication`) is resolved
to single-model in spec Assumptions; see research.md for the technical decisions.*

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

Evaluated against constitution **v2.0.0**:

| Principle | Status | Notes |
|---|---|---|
| I. Frontend Preservation (NON-NEGOTIABLE) | ✅ PASS (w/ recorded deviations) | List/detail/requests markup, classes, `data-*` hooks, badges, RTL, theme toggle, commission banner, referral/QR/coupon blocks preserved exactly. **Bounded in-style additions required for backend integration** (Complexity Tracking): (a) the list page's confirmation modals are *triggered but never defined* in the prototype — supplying them is completing the prototype's own `data-modal-trigger` contract; (b) the detail page's static notes gains an in-style edit affordance (FR-015). Both rendered in the prototype's exact style. |
| II. Server-Rendered Django — No SPA/API-First (NON-NEGOTIABLE) | ✅ PASS | Django views + ModelForms + templates only. No React/Vue/Next/Angular, no SPA router, no API/DRF, no Node build. Admin internal-only. |
| III. Modular App Architecture | ✅ PASS | `apps/affiliates` owns `models.py`, `views.py`, `urls.py`, `forms.py`, `admin.py`, `selectors.py` (owner-scope + filtering), `services.py` (approve/reject/suspend/reactivate/change-level/notes + lifecycle guards), `management/commands/seed_affiliates.py`, `migrations/`, `tests/`, and app-namespaced templates under `affiliates/`. |
| IV. Role-Based Access & Owner-Scoped Data Isolation (NON-NEGOTIABLE) | ✅ PASS | Every view `@role_required("is_merchant")`; every read/write through owner-scoped querysets (`AffiliateProfile.objects.filter(merchant=request.user)` / `get_owned_affiliate_or_404`); cross-merchant object access → 404. Affiliate-role users denied (403). No reliance on UI hiding. |
| V. Database-Backed Truth — No Fake Dynamic Data | ✅ PASS | All affiliate content DB-backed; zero static rows remain; empty query → existing empty-state. Order/commission/payout-derived widgets (roster performance columns; detail stat cards, attributed-orders + payout tables, marketing captions) render **truthful zeros / empty-state**, not fabricated rows. |
| VI. Affiliate & Commission Integrity (NON-NEGOTIABLE) | ✅ PASS (in-scope slice) | The in-scope half of the affiliate domain — registration/creation, approval/rejection/suspension, levels, referral codes, referral links, coupon codes — is modeled faithfully end-to-end with a defined status state model. The **commission half** (attributed orders, commission state machine, earnings, payouts) is deferred and is rendered as truthful zeros, never premature/fabricated commission. Selectors (`active_affiliates`) are shaped for the later commission phase. |
| VII. Customer Privacy on Affiliate Surfaces (NON-NEGOTIABLE) | ➖ N/A | These are merchant-facing pages showing the merchant's own affiliates; no customer PII is rendered. (The affiliate seller portal, where masking applies, is a separate later spec.) |
| VIII. Physical-Commerce MVP Catalog | ✅ PASS | Seeded affiliates carry physical-commerce framing only; no educational/digital data or copy introduced (also guarded by the `physical-commerce-only` project memory). |

**Tech allow/deny**: Django only; no Pillow/media (no `ImageField` this phase); SQLite (local) +
PostgreSQL-ready (prod); no SPA/API/DRF/Node ✅; Django admin internal-only ✅.

**Result**: PASS — two recorded, in-style, integration-required UI additions (Complexity Tracking); no
NON-NEGOTIABLE breach.

### Post-Design Re-evaluation (after Phase 1)

Re-checked after producing research.md, data-model.md, contracts/routes.md, quickstart.md:

- No new dependency or pattern crosses a constitution line; the app reuses the exact `004` shape
  (selectors as the single owner-scope source; services for state changes; `@role_required` + `require_POST`
  + CSRF on mutations; clean URLs + legacy redirects; idempotent seed).
- The clean-URL move plus legacy `*.html` redirects keeps Principle I's "no dead links" intact; the
  merchant sidebar's affiliates link is repointed to `{% url 'affiliates:list' %}`; not-yet-converted
  pages are untouched.
- Owner scoping lives in `selectors.py` and is consumed by every view — Principle IV holds by construction.
- The two in-style additions (completing the list page's undefined modals; the detail notes-edit control)
  remain the only deviations from strict markup preservation, are required for the actions to function,
  and are confined to those two spots.
- Out-of-scope figures are specified as truthful zeros/empty-state throughout — Principle V holds.
- **Result**: PASS (unchanged). Ready for `/speckit-tasks`.

## Project Structure

### Documentation (this feature)

```text
specs/005-affiliate-management/
├── plan.md              # This file (/speckit-plan output)
├── spec.md              # Feature specification
├── research.md          # Phase 0 — resolved technical decisions
├── data-model.md        # Phase 1 — AffiliateProfile (+ lifecycle state model)
├── contracts/
│   └── routes.md        # Phase 1 — URL→view→access map + form/action + legacy-redirect contract
├── quickstart.md        # Phase 1 — setup, seed, run, and acceptance verification
└── checklists/
    └── requirements.md  # Spec quality checklist (from /speckit-specify)
```

### Source Code (repository root)

Builds on the foundation + `004` layout. **New/changed paths** are marked; everything else is unchanged.

```text
config/
└── urls.py                          # CHANGED: include apps.affiliates.urls before apps.core.urls
apps/affiliates/
├── __init__.py
├── apps.py                          # exists (AffiliatesConfig); already in INSTALLED_APPS
├── models.py                        # NEW: AffiliateProfile (+ Status, Level TextChoices)
├── forms.py                         # NEW: AffiliateChangeLevelForm, AffiliateNotesForm (+ optional reason handling)
├── selectors.py                     # NEW: owner-scoped querysets + filter application + pending/active helpers
├── services.py                      # NEW: approve / reject / suspend / reactivate / change_level / set_notes (+ guards)
├── views.py                         # NEW: list, requests, detail, approve, reject, suspend, reactivate, change_level, edit_notes, legacy redirects
├── urls.py                          # NEW: clean /affiliates/… routes + legacy *.html redirects
├── admin.py                         # NEW: register AffiliateProfile; list_display/search/filters
├── migrations/
│   └── 0001_initial.py              # NEW
├── management/
│   └── commands/
│       └── seed_affiliates.py       # NEW: idempotent seed (5 demo affiliates on the demo merchant)
├── templates/affiliates/            # NEW app-namespaced templates (constitution III)
│   ├── affiliate_list.html          # from affiliates.html        (extends merchant_base.html)
│   ├── affiliate_detail.html        # from affiliate-detail.html  (extends merchant_base.html)
│   └── affiliate_requests.html      # from affiliate-requests.html(extends merchant_base.html)
└── tests/
    ├── test_models.py               # code uniqueness, defaults, referral_link property
    ├── test_selectors.py            # owner isolation, pending/active, filters
    ├── test_services.py             # lifecycle transitions + guards
    ├── test_views_list.py           # access, owner-scope, filters, empty state, pagination
    ├── test_views_requests.py       # pending listing, empty state, access
    ├── test_views_detail.py         # owner-scope 404, real-data render, empty-state sections
    └── test_views_lifecycle.py      # approve/reject/suspend/reactivate/change-level/notes: owner-scope, require_POST, CSRF, persistence
templates/
├── includes/merchant_sidebar.html   # CHANGED: affiliates.html link → {% url 'affiliates:list' %} (+ active state on list)
├── affiliates.html  affiliate-detail.html  affiliate-requests.html   # REMOVED (replaced by app templates; legacy URLs redirect)
apps/core/page_registry.py           # CHANGED: remove the 3 affiliate PageEntry lines (now owned by apps.affiliates); affiliate-payouts.html stays (out of scope)
```

**Structure Decision**: Single Django project at repo root (web application), extending the foundation
and mirroring `004` exactly. The pre-scaffolded `apps/affiliates` app gains the full constitution-III
file set and owns its templates under `apps/affiliates/templates/affiliates/` (discoverable via
`APP_DIRS=True`). The three raw prototype root templates are migrated into app templates and removed;
their old `*.html` URLs are served as redirects to the new clean URLs so inbound links from
not-yet-converted pages keep resolving. No `ImageField`/media is introduced — affiliate avatars and the
QR image remain `{% static %}` placeholders.

## Complexity Tracking

> No forbidden tech and no frontend redesign. Two bounded, **in-style** UI additions that are *required
> for backend integration* (so they are not a silent PASS of Principle I) and one scope deferral rendered
> as truthful data.

| Item | Why Needed | Why Acceptable (not a NON-NEGOTIABLE breach) |
|---|---|---|
| **List-page confirmation modals supplied** (approve / suspend / change-level), per-affiliate, wired to POST+CSRF; the change-level modal carries an in-style Level `<select>` | The prototype's list dropdown has `data-modal-trigger="modal-approve\|modal-suspend\|modal-change-level"` but **no matching modal bodies exist** — the buttons currently do nothing; FR-006/012/014 require these actions to work | Principle I permits changes "strictly required for backend integration." This *completes the prototype's own (dangling) modal contract* in its exact visual style rather than redesigning; mirrors the per-row modal approach already used in `004`. |
| **Detail-page notes-edit affordance** (in-style inline textarea + save) | The detail "ملاحظات" block is static text; FR-015 requires a merchant to edit notes from the UI | Same Principle-I carve-out; a minimal in-style edit control added to the existing notes card; persisted via a POST+CSRF action. |
| Order/commission/payout widgets (roster performance columns; detail stat cards, attributed-orders + payout tables, marketing captions) shown as **truthful zero / empty-state** rather than removed | Those subsystems are out of scope (Out of Scope); the widgets are part of the preserved markup | Not fabricated data: zero orders/commissions/payouts genuinely exist, so zeros/empty-states are *true* (Principle V). They become real in the later orders/commission phase. |
