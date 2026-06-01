# Quickstart: Merchant Affiliate Management (MVP Phase 2)

**Feature**: 005-affiliate-management
**Date**: 2026-06-01

How to set up, seed, run, and **acceptance-test** the database-backed affiliate management surface.
Assumes `003-backend-foundation` and `004-products-catalog` already work (venv, settings split, custom
`User`, demo merchant).

---

## 1. Install & migrate

```bash
# from repo root, with the project venv active
export DJANGO_SETTINGS_MODULE=config.settings.local
# No new dependency this phase (no Pillow/media).

python manage.py makemigrations affiliates       # creates affiliates/0001_initial
python manage.py migrate
```

## 2. Seed demo data (idempotent)

```bash
python manage.py seed_affiliates
# → ensures the 5 demo affiliates on the demo merchant:
#   أحمد الشمري   — Gold     — Active     — AHMAD20
#   سارة المنصور  — Silver   — Active
#   محمد العتيبي  — Bronze   — Pending
#   Nora Ahmed   — Platinum — Active
#   خالد سالم    — Suspended
# Safe to re-run (get_or_create on merchant + referral_code).
```

Reuses the foundation/`004` demo merchant. Create a second merchant in admin (with its own affiliate) to
test cross-merchant isolation.

## 3. Run

```bash
python manage.py runserver
# Roster:    http://127.0.0.1:8000/affiliates/
# Requests:  http://127.0.0.1:8000/affiliates/requests/
# Detail:    http://127.0.0.1:8000/affiliates/<id>/
# Admin:     http://127.0.0.1:8000/admin/   (AffiliateProfile)
```

---

## 4. Acceptance verification

Maps to the spec's Acceptance Criteria (#1–#12), Functional Requirements, and Success Criteria.

### A. Browse the roster (US1 · FR-001..004 · SC-001/005/007/008)

- [ ] `/affiliates/` lists **DB-backed** affiliates for the signed-in merchant; **no** static demo rows
      remain. Layout matches `affiliates.html` (columns, level/status badges, action dropdown, RTL).
- [ ] Filter by `q` (name or referral code), status, level (and a combination) → only matching owned
      affiliates. The three controls are the prototype's existing search + two selects.
- [ ] A no-match filter and a zero-affiliate merchant both show the existing **empty-state**.
- [ ] Performance columns (orders, sales, pending/paid commission, conversion) render **0** — no
      carried-over sample numbers.

### B. Join requests (US2 · FR-005..008 · SC-002)

- [ ] `/affiliates/requests/` lists the merchant's **Pending** affiliates as request cards with real
      details; the pending count is truthful.
- [ ] Approve (modal, POST+CSRF) → status `Active`, `approved_at` set, leaves the queue.
- [ ] Reject (modal, POST+CSRF, optional reason) → status `Rejected`, `rejected_at` set, leaves the queue.
- [ ] Zero pending → existing empty-state.

### C. Detail (US3 · FR-009..011 · SC-004/007/008)

- [ ] `/affiliates/<id>/` shows the affiliate's **real** identity, contact, level/status badges,
      referral link (`…/r/<code>`), coupon chip, QR placeholder, notes, social links.
- [ ] Referral-link and coupon **copy** buttons still work (`data-copy` preserved); commission-rule
      banner present.
- [ ] Attributed-orders table, payout-history table, marketing captions, and stat cards show **truthful
      empty-state / zeros** — no fabricated rows.

### D. Lifecycle (US4 · FR-012..016 · SC-003)

- [ ] Suspend (modal, POST+CSRF) → `Suspended`, `suspended_at` set, badge updates.
- [ ] Reactivate a Suspended affiliate → `Active`.
- [ ] Change level (in-style level select, POST+CSRF) → new level persists; badge updates on roster +
      detail.
- [ ] Edit notes (in-style affordance, POST+CSRF) → notes persist on the detail page.
- [ ] Acting on an already-decided request (e.g. approve a non-Pending) is a no-op — no misleading
      timestamp overwrite.

### E. Ownership isolation & access (US5 · FR-020..022 · SC-006) — Principle IV (NON-NEGOTIABLE)

- [ ] As merchant A, GET merchant B's `/affiliates/<B-id>/` → **404**.
- [ ] POST to B's `/approve/`, `/reject/`, `/suspend/`, `/reactivate/`, `/change-level/`, `/notes/` as A
      → **404**, nothing changes.
- [ ] An **affiliate-role** user opening any `/affiliates/...` page → **403**.
- [ ] Unauthenticated `/affiliates/` → redirect to `/login.html`.
- [ ] Every mutating POST via GET → **405**; without a valid CSRF token → **403**.

### F. Codes & uniqueness (FR-017..019 · SC-004)

- [ ] Two affiliates cannot share a referral code (global) — enforced.
- [ ] Two affiliates of the **same** merchant cannot share a coupon code; the same coupon string under a
      **different** merchant is allowed.
- [ ] The referral link renders as `https://smartmerchant.os/r/<referral_code>` everywhere it appears.

### G. Admin (FR-025)

- [ ] `AffiliateProfile` is registered with list display, status + level filters, and search by
      name / email / phone / referral code / coupon code.

### H. Link integrity & visual parity (FR-023/024 · SC-007) — Principle I

- [ ] Legacy links still resolve: `/affiliates.html`→`/affiliates/`, `/affiliate-requests.html`→
      `/affiliates/requests/`, `/affiliate-detail.html`→`/affiliates/`. Sidebar "المسوقون" →
      `/affiliates/`. No dead links from other pages.
- [ ] Side-by-side: `affiliate_list.html` / `affiliate_detail.html` / `affiliate_requests.html` are
      pixel-equivalent to the static originals; the only additions are the sanctioned in-style modals
      (list) and notes-edit affordance (detail). Theme toggle, dropdowns, modals, copy buttons, RTL all
      still work.

---

## 5. Automated tests (`python manage.py test apps.affiliates`)

Suggested coverage (authored in `/speckit-tasks`):

- **Models**: referral-code global uniqueness; coupon per-merchant uniqueness (blank allowed; same
  string under another merchant allowed); `referral_link` property; defaults (Pending / Bronze).
- **Selectors**: `merchant_affiliates` isolation; `pending_affiliates` / `active_affiliates`; each filter
  (`q`/`status`/`level`) + a combination.
- **Services**: approve (Pending→Active + `approved_at`); reject (+`rejected_at`); suspend
  (+`suspended_at`); reactivate; `change_level` valid + invalid; `set_notes`; guards (approve/reject on
  non-Pending, suspend on non-Active are no-ops, no timestamp overwrite).
- **Views**: `@role_required` redirect/403 (incl. affiliate-role denied); owner-scoping 404 on
  cross-merchant for detail + every mutation; `require_POST` 405; CSRF 403; roster filters + empty-state;
  requests listing + empty-state; lifecycle persistence + redirects.

## 6. Rollback

```bash
python manage.py migrate affiliates zero    # drop the affiliate table
# revert config/urls.py (remove apps.affiliates include),
# apps/core/page_registry.py (restore the 3 affiliate PageEntry lines),
# and templates/includes/merchant_sidebar.html (affiliates link).
```
