---
description: "Task list for Merchant Affiliate Management (Database-Backed Conversion — MVP Phase 2)"
---

# Tasks: Merchant Affiliate Management (Database-Backed Conversion — MVP Phase 2)

**Input**: Design documents from `/specs/005-affiliate-management/`
**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, contracts/routes.md, quickstart.md

**Tests**: REQUESTED. plan.md ("Testing: Django test runner for models/selectors/services/forms/views —
ownership isolation, code uniqueness, filters, the approval/lifecycle state model, role+CSRF gates") and
quickstart.md §5 call for an automated suite under `apps/affiliates/tests/`, **plus** manual visual-parity
verification per story (Principle I). Both are generated below. Automated tests target the
high-value/security-critical logic (owner isolation — Principle IV; code uniqueness; the lifecycle state
model; filters; role/CSRF gates); they need not be written test-first, but the listed tests MUST pass
before a story is considered done.

**Organization**: Tasks are grouped by user story so each story is an independently testable increment.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependency on an incomplete task)
- **[Story]**: Which user story the task belongs to (US1–US5)
- Every task includes an exact file path

## Path Conventions

Single Django project at the **repository root** (per plan.md). Affiliate code lives in `apps/affiliates/`
with app-namespaced templates at `apps/affiliates/templates/affiliates/`. The three prototype root
templates (`templates/affiliates.html`, `affiliate-detail.html`, `affiliate-requests.html`) are migrated
into app templates and removed; their legacy URLs redirect to the new clean `/affiliates/…` routes.
Foundation utilities reused: `apps/core/decorators.role_required`, `templates/merchant_base.html`,
`apps/core/page_registry.py`. No new dependency, no `ImageField`/media this phase.

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Minimal prep — no new dependency this phase (no Pillow/media).

- [x] T001 Confirm `"apps.affiliates"` is in `INSTALLED_APPS` (`config/settings/base.py`) — already present; verify, no change expected.
- [x] T002 [P] Create the test package `apps/affiliates/tests/__init__.py`.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Model, migration, admin, owner-scoping selectors, the lifecycle service layer, URL/config wiring, and seed — everything every user story depends on.

**⚠️ CRITICAL**: No user story work can begin until this phase is complete.

- [x] T003 Create `AffiliateProfile` model in `apps/affiliates/models.py` per data-model.md: fields (`user` FK nullable `SET_NULL` `related_name="affiliate_links"`, `merchant` FK `CASCADE` `related_name="affiliates"`, full_name, phone, email, city, country, status, level, referral_code, coupon_code, bio, social_instagram/tiktok/facebook, notes, approved_at/rejected_at/suspended_at, created_at/updated_at); `Status` TextChoices (Pending/Active/Suspended/Rejected, default Pending) and `Level` TextChoices (Bronze/Silver/Gold/Platinum, default Bronze); `referral_code unique=True`; `UniqueConstraint(["merchant","coupon_code"], condition=~Q(coupon_code=""), name="uniq_coupon_per_merchant")`; `Meta.ordering=["-created_at"]`; `save()` auto-generates a globally-unique `referral_code` from `full_name` when blank; `REFERRAL_BASE` constant + `referral_link` property; `get_absolute_url()`; `is_active`/`is_pending` helpers.
- [x] T004 Generate and apply the migration: `python manage.py makemigrations affiliates` then `migrate` → creates `apps/affiliates/migrations/0001_initial.py`. (Depends on T003.)
- [x] T005 [P] Register `AffiliateProfile` in `apps/affiliates/admin.py`: `list_display=[full_name, merchant, level, status, referral_code, coupon_code, created_at]`, `list_filter=[status, level]`, `search_fields=[full_name, email, phone, referral_code, coupon_code]`, `readonly_fields=[created_at, updated_at, approved_at, rejected_at, suspended_at]`.
- [x] T006 [P] Create `apps/affiliates/selectors.py` with owner-scoping helpers: `merchant_affiliates(user)` (`filter(merchant=user).select_related("user")`), `get_owned_affiliate_or_404(user, pk)` (→ 404 cross-merchant), `pending_affiliates(qs)` (status=Pending), `active_affiliates(qs)` (status=Active — reused by the later commission phase).
- [x] T007 [P] Create `apps/affiliates/services.py` with the guarded lifecycle state model (research D5, data-model.md): `approve(a)` (Pending→Active + `approved_at`), `reject(a, reason="")` (Pending→Rejected + `rejected_at`, reason→notes), `suspend(a, reason="")` (Active→Suspended + `suspended_at`, reason→notes), `reactivate(a)` (Suspended→Active), `change_level(a, level)` (validate `level ∈ Level.values`), `set_notes(a, text)`. Each transition guards its precondition (wrong-state = idempotent no-op, no misleading timestamp overwrite); saves use `update_fields`; timestamps via `django.utils.timezone.now()`.
- [x] T008 Create `apps/affiliates/urls.py` skeleton: `app_name = "affiliates"`, `urlpatterns = []` (routes added per story).
- [x] T009 Wire `config/urls.py`: add `path("", include("apps.affiliates.urls"))` **before** the `apps.core.urls` include (so legacy redirects win over the page registry). (Depends on T008.)
- [x] T010 Create idempotent seed command `apps/affiliates/management/commands/seed_affiliates.py`: reuse the demo merchant (foundation/`004`), create the 5 demo affiliates from spec FR-026 — أحمد الشمري (Gold/Active/`AHMAD20`), سارة المنصور (Silver/Active), محمد العتيبي (Bronze/Pending), Nora Ahmed (Platinum/Active), خالد سالم (Suspended) — with distinct referral codes + coupon codes and physical-commerce framing only; keyed by `get_or_create(merchant, referral_code)`; set `approved_at` for active ones. (Depends on T003–T004.)
- [x] T011 [P] Tests in `apps/affiliates/tests/test_models.py`: referral-code global uniqueness; coupon per-merchant uniqueness (blank allowed; same string under a different merchant allowed); `referral_link` property format; defaults (Pending/Bronze); auto-generated referral code when blank.
- [x] T012 [P] Tests in `apps/affiliates/tests/test_services.py`: approve (Pending→Active + `approved_at`); reject (+`rejected_at`, reason→notes); suspend (+`suspended_at`); reactivate; `change_level` valid + invalid value; `set_notes`; guards (approve/reject on non-Pending and suspend on non-Active are no-ops with no timestamp overwrite).

**Checkpoint**: Model migrated, admin usable, owner-scope + lifecycle services in place, app routed, seed runs. User stories can begin.

---

## Phase 3: User Story 1 - Browse the affiliate roster (Priority: P1) 🎯 MVP

**Goal**: A signed-in merchant sees their own DB-backed affiliates with working search/status/level filters and an empty state; performance columns show truthful zeros; no static rows remain.

**Independent Test**: Seed two merchants; sign in as each and confirm each sees only their own affiliates; apply each filter + a combination; sign in as a zero-affiliate merchant and confirm the empty state.

- [x] T013 [US1] Remove the `affiliates.html` and `affiliate-detail.html` `PageEntry` lines from `apps/core/page_registry.py`, adding a comment that `apps.affiliates` now owns them. (Leave `affiliate-requests.html` — removed in US2; leave `affiliate-payouts.html` — out of scope.)
- [x] T014 [US1] Add filter logic to `apps/affiliates/selectors.py`: `list_affiliates(merchant, params)` applying `q` (`full_name` OR `referral_code` icontains), `status` (exact), `level` (exact), ordered `-created_at`, owner-scoped via `merchant_affiliates`.
- [x] T015 [US1] Implement `affiliate_list` view in `apps/affiliates/views.py` (`@role_required("is_merchant")`, build filters from GET, paginate, pass active-filter + truthful-zero stat context) and add `path("affiliates/", …, name="list")` + the legacy redirects `affiliates.html` → `affiliates:list` and `affiliate-detail.html` → `affiliates:list` (permanent) to `apps/affiliates/urls.py`.
- [x] T016 [US1] Update `templates/includes/merchant_sidebar.html`: change the affiliates link `href="affiliates.html"` → `{% url 'affiliates:list' %}` (and active state on the list page).
- [x] T017 [US1] Convert `apps/affiliates/templates/affiliates/affiliate_list.html` from `templates/affiliates.html`: `{% extends 'merchant_base.html' %}`, `{% load static %}`, loop DB rows (avatar `{% static %}` placeholder, `full_name`, level badge `badge-<level>`, `referral_code` chip, status badge `badge-<status>`, **performance columns orders/sales/pending-comm/paid-comm/conversion = 0**), preserve the action dropdown + commission-rule banner + the three existing filter controls (search + status + level selects) echoing active values, render the existing empty-state when no rows, and paginate preserving the querystring. (Action-menu modals are supplied/wired in US4.)
- [x] T018 [US1] Delete the now-replaced `templates/affiliates.html`.
- [x] T019 [P] [US1] Tests in `apps/affiliates/tests/test_selectors.py`: `merchant_affiliates` isolation; `pending_affiliates`/`active_affiliates`; each of `q`/`status`/`level` + a combination.
- [x] T020 [P] [US1] Tests in `apps/affiliates/tests/test_views_list.py`: list is owner-scoped; `@role_required` redirects anonymous / 403s non-merchant (incl. affiliate role); empty-state for zero affiliates; filter results + pagination; performance columns render 0.
- [ ] T021 [US1] Manual visual-parity check (quickstart §A/§H): `/affiliates/` vs static `affiliates.html` — layout, level/status badges, dropdown, commission banner, theme, RTL identical; list is DB-backed with no static rows and truthful-zero columns (SC-001/005/007/008).

**Checkpoint**: US1 fully functional — DB-backed roster with filters + empty state, owner-scoped. MVP.

---

## Phase 4: User Story 2 - Review and decide on join requests (Priority: P1)

**Goal**: A merchant sees their Pending affiliates as request cards and approves (→ Active) or rejects (→ Rejected, optional reason) them via the existing confirmation modals; the queue and pending count stay truthful.

**Independent Test**: Seed a Pending affiliate; open `/affiliates/requests/`; approve → status Active and it leaves the queue; on another Pending, reject → status Rejected and it leaves the queue.

- [x] T022 [US2] Remove the `affiliate-requests.html` `PageEntry` line from `apps/core/page_registry.py` (comment that `apps.affiliates` now owns it).
- [x] T023 [US2] Implement `affiliate_requests` view in `apps/affiliates/views.py` (`@role_required("is_merchant")`, owner-scoped `pending_affiliates(merchant_affiliates(user))`, **optional `q` search** narrowing Pending by `full_name`/`referral_code` icontains — FR-008, echoed back to the template — truthful count) and add `path("affiliates/requests/", …, name="requests")` (before `<int:pk>/`) + the legacy redirect `affiliate-requests.html` → `affiliates:requests` to `apps/affiliates/urls.py`.
- [x] T024 [US2] Implement `affiliate_approve` and `affiliate_reject` views in `apps/affiliates/views.py` (`@role_required("is_merchant")` outer + `@require_POST` inner + `get_owned_affiliate_or_404`; call `services.approve`/`services.reject` with optional `reason` from POST; redirect to `affiliates:requests` + message) and add `path("affiliates/<int:pk>/approve/", …, name="approve")` and `…/reject/` routes.
- [x] T025 [US2] Convert `apps/affiliates/templates/affiliates/affiliate_requests.html` from `templates/affiliate-requests.html`: `{% extends 'merchant_base.html' %}`, loop the merchant's Pending affiliates as request cards (name/contact/social/`bio` experience), wire the page's **existing** search input to the `q` param (GET form, echo the active value — FR-008), wire each card's **existing** `modal-approve-<pk>` / `modal-reject-<pk>` confirmation modals to CSRF POST forms targeting the approve/reject routes (reject modal carries an optional `reason` field), render the existing empty-state when none (incl. a no-match search).
- [x] T026 [US2] Delete the now-replaced `templates/affiliate-requests.html`.
- [x] T027 [P] [US2] Tests in `apps/affiliates/tests/test_views_requests.py`: requests page lists only owner's Pending with truthful count + empty-state + access guard; **`q` search narrows Pending by name/referral code and a no-match shows the empty-state (FR-008)**; approve POST → Active (leaves queue); reject POST → Rejected (leaves queue); cross-merchant approve/reject → 404; GET on approve/reject → 405; missing CSRF → 403.
- [ ] T028 [US2] Manual (quickstart §B): approve and reject pending requests through the modals; confirm status + queue update and truthful pending count (SC-002).

**Checkpoint**: US1 + US2 work independently — browse the roster and run the approval workflow.

---

## Phase 5: User Story 3 - Inspect an affiliate's profile (Priority: P2)

**Goal**: A merchant views an owned affiliate's real profile in the existing detail layout; out-of-scope sections render truthful empty-state/zeros; cannot view another merchant's affiliate.

**Independent Test**: Open an affiliate's detail → identity/contact/level/status/referral-link/coupon/notes match the DB record and layout matches static `affiliate-detail.html`; another merchant's detail URL → 404.

- [x] T029 [US3] Implement `affiliate_detail` view in `apps/affiliates/views.py` (`get_owned_affiliate_or_404`; context = affiliate + **zeroed/empty** order/commission/payout widgets) and add `path("affiliates/<int:pk>/", …, name="detail")` to `apps/affiliates/urls.py`.
- [x] T030 [US3] Convert `apps/affiliates/templates/affiliates/affiliate_detail.html` from `templates/affiliate-detail.html`: `{% extends 'merchant_base.html' %}`, render real profile fields (email/phone/social/country/`created_at` join date), the `referral_link` box + QR `{% static %}` placeholder + `coupon_code` chip (preserve `data-copy` hooks), the `notes` block, and the commission-rule banner; render the attributed-orders table, payout-history table, marketing captions, and stat cards as their **empty-state / 0** (Principle V); preserve the existing `modal-suspend-detail` markup + JS hooks + RTL. (Lifecycle action wiring + notes-edit affordance added in US4.)
- [x] T031 [US3] Delete the now-replaced `templates/affiliate-detail.html`.
- [x] T032 [P] [US3] Tests in `apps/affiliates/tests/test_views_detail.py`: owner's data rendered (referral link format, coupon, notes); **an affiliate with `user=None` (no linked login account) renders without error (edge case)**; cross-merchant detail → 404; anonymous → login redirect; affiliate role → 403.
- [ ] T033 [US3] Manual (quickstart §C): detail shows real data + working copy buttons; orders/payouts/marketing/stat sections show zero/empty; cross-merchant → 404 (SC-004/007/008).

**Checkpoint**: US1–US3 work independently — browse, approve/reject, and inspect.

---

## Phase 6: User Story 4 - Change an affiliate's standing (Priority: P2)

**Goal**: From the roster or detail page, a merchant suspends/reactivates an affiliate, changes its level, and edits its notes — each via the existing/in-style UI, each persisted, owner-scoped, POST + CSRF.

**Independent Test**: Suspend an Active affiliate → Suspended + `suspended_at`; reactivate → Active; change level → new badge persists on roster + detail; edit notes → persists; all cross-owner attempts → 404.

- [x] T034 [US4] Create `apps/affiliates/forms.py`: `AffiliateChangeLevelForm` (`forms.Form`, `level = ChoiceField(choices=AffiliateProfile.Level.choices)`) and `AffiliateNotesForm` (`forms.ModelForm`, `Meta.model=AffiliateProfile`, `fields=["notes"]`).
- [x] T035 [US4] Implement `affiliate_suspend`, `affiliate_reactivate`, `affiliate_change_level`, `affiliate_edit_notes` views in `apps/affiliates/views.py` (`@role_required("is_merchant")` + `@require_POST` + `get_owned_affiliate_or_404`; suspend/reactivate read optional `reason` and call services; change-level validates via `AffiliateChangeLevelForm`; edit-notes via `AffiliateNotesForm`; redirect to `affiliates:detail` + message) and add the routes `…/suspend/` (name `suspend`), `…/reactivate/` (name `reactivate`), `…/change-level/` (name `change-level`), `…/notes/` (name `notes`) to `apps/affiliates/urls.py`.
- [x] T036 [US4] Supply + wire the **list page** action modals on `apps/affiliates/templates/affiliates/affiliate_list.html`: the prototype's dropdown triggers (`modal-approve`/`modal-suspend`/`modal-change-level`) have **no modal bodies** — add per-affiliate modals (`modal-approve-<pk>` etc.) wired to CSRF POST forms targeting the row's routes (approve reuses US2's route; suspend; change-level modal carries the in-style Level `<select>`), preserving the existing dropdown/`data-*` markup. (Same file as T017 → after T017.)
- [x] T037 [US4] Wire the **detail page** actions on `apps/affiliates/templates/affiliates/affiliate_detail.html`: the existing `modal-suspend-detail` → CSRF POST to `suspend`; show the status-appropriate primary action (Pending→approve, Suspended→reactivate); add an in-style change-level modal (Level `<select>`) and an in-style notes-edit affordance (inline textarea + save → `notes`) — all POST+CSRF, in the prototype's style. (Same file as T030 → after T030.)
- [x] T038 [P] [US4] Tests in `apps/affiliates/tests/test_views_lifecycle.py`: suspend → Suspended + `suspended_at`; reactivate → Active; change-level persists + invalid level rejected (nothing saved); edit-notes persists; cross-owner → 404 on all four; GET → 405; missing CSRF → 403.
- [ ] T039 [US4] Manual (quickstart §D): suspend/reactivate/change-level/edit-notes via the UI; confirm transitions, badge updates, notes persistence, and that approving an already-decided affiliate is a no-op (SC-003).

**Checkpoint**: US1–US4 work independently — full affiliate lifecycle management.

---

## Phase 7: User Story 5 - Owner-scoped isolation and role protection (Priority: P1)

**Goal**: Prove that the enforcement built incrementally across Foundational + US1–US4 holds end-to-end: a merchant only sees/acts on their own affiliates; affiliate-role/anonymous users are denied; every mutation is POST + CSRF.

> **Note**: This P1 guarantee is *built* from Foundational onward (owner-scoped selectors; `@role_required`/`@require_POST` on every view as it is written). This phase is the consolidated **verification + hardening** pass, sequenced after the mutation routes exist so the full access matrix can be asserted.

**Independent Test**: As merchant A, GET merchant B's detail and POST every mutation URL → 404; as an affiliate-role user, every `/affiliates/...` page → 403; as anonymous → login redirect; every mutation via GET → 405 and without CSRF → 403.

- [x] T040 [P] [US5] Tests in `apps/affiliates/tests/test_views_access.py`: the full matrix — cross-merchant 404 on `detail` + all six mutations (`approve`/`reject`/`suspend`/`reactivate`/`change-level`/`notes`); affiliate-role → 403 on `list`/`requests`/`detail`; anonymous → redirect to `/login.html`; each mutation: GET → 405, missing-CSRF → 403.
- [x] T041 [US5] Ownership/security audit of `apps/affiliates/views.py`: every view has `@role_required("is_merchant")`; every read/write goes through the owner-scoped selectors (grep for any bare `AffiliateProfile.objects` in views and replace with `merchant_affiliates`/`get_owned_affiliate_or_404`); every mutation is `@require_POST`; owner is never trusted from a form — Principle IV (NON-NEGOTIABLE), FR-020/021/022.
- [ ] T042 [US5] Manual isolation check (quickstart §E): cross-merchant 404 on detail + all mutations; affiliate-role 403; anonymous redirect; CSRF/`require_POST` enforced (SC-006).

**Checkpoint**: All five user stories independently functional; isolation + role + CSRF proven end-to-end.

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Constitution/acceptance sweeps spanning all stories.

- [x] T043 [P] Physical-commerce framing audit: confirm `seed_affiliates.py` and the converted pages introduce **zero** educational/digital products or copy (كورسات/كتب/PDF/تدريب/اشتراكات تعليمية) — constitution Principle VIII, `physical-commerce-only` memory.
- [x] T044 [P] Performance check: confirm the roster query is `merchant_affiliates(...).select_related("user")` (no N+1 on the optional user) and the pending count is a single query, in `apps/affiliates/selectors.py`/`views.py`.
- [x] T045 [P] Visual-parity sweep over the three converted pages (`affiliate_list`, `affiliate_detail`, `affiliate_requests`) vs the static originals (level/status badges, dropdowns, modals, commission banner, referral/QR/coupon blocks, copy buttons, theme toggle, RTL) — SC-007, Principle I; confirm the only additions are the sanctioned in-style list modals (T036) + detail notes-edit (T037); confirm the out-of-scope affordances ("دفع عمولة" / "صرف العمولة" / "عرض الطلبات") remain visually present but **inert** — they fabricate no data and imply no money movement (Principle V).
- [x] T046 Run the full `quickstart.md` acceptance checklist (§A–§H) and the spec's 12 acceptance criteria; fix any gap.
- [x] T047 [P] Confirm no leftover legacy affiliate template files remain under `templates/` (`affiliates.html`, `affiliate-detail.html`, `affiliate-requests.html`), admin works (FR-025), and update `README.md`/`SAMPLE-DATA.md` affiliate references to the new clean URLs.
- [x] T048 Final green run: `python manage.py test apps.affiliates` all pass and `python manage.py check` clean.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: no dependencies — start immediately.
- **Foundational (Phase 2)**: depends on Setup — **BLOCKS all user stories**.
- **User Stories (Phase 3–7)**: all depend on Foundational. US1 is the MVP. US2/US3/US4 each depend only on Foundational and are independently testable. **US5 (P1, isolation)** is enforced incrementally from Foundational onward but its consolidated verification phase is sequenced after the mutation routes (US2/US4) exist. Recommended build order: US1 → US2 → US3 → US4 → US5.
- **Polish (Phase 8)**: depends on the desired user stories being complete.

### Cross-story file touchpoints (sequencing notes)

- `apps/affiliates/views.py`, `apps/affiliates/urls.py`: appended by multiple stories → edits are sequential per story (not cross-story [P]).
- `apps/affiliates/templates/affiliates/affiliate_list.html`: created in US1 (T017), action modals supplied/wired in US4 (T036).
- `apps/affiliates/templates/affiliates/affiliate_detail.html`: created in US3 (T030), actions wired in US4 (T037).
- `apps/core/page_registry.py`: `affiliates.html`+`affiliate-detail.html` lines removed in US1 (T013); `affiliate-requests.html` removed in US2 (T022) — each paired with its legacy redirect so no link gap opens.
- `apps/affiliates/services.py` is foundational (T007) and consumed by US2 (approve/reject) and US4 (suspend/reactivate/change-level/notes) — no per-story edits.

### Within Each User Story

Selectors/forms → view + route → template conversion → wiring → tests → manual parity check.

### Parallel Opportunities

- Setup: T002 with T001.
- Foundational: after model + migration (T003–T004), run T005/T006/T007 in parallel; T010 (seed) parallel with T005–T007; T011/T012 (model + service tests) parallel once their targets exist.
- Each story's test files are `[P]` with each other (different files) once their implementation is done.
- With multiple developers, US2/US3/US4 can proceed in parallel after Foundational, merging their distinct view/route/template additions.

---

## Parallel Example: Foundational Phase

```bash
# After model + migration (T003–T004) land, run in parallel:
Task: "Register AffiliateProfile in apps/affiliates/admin.py"                    # T005
Task: "Create apps/affiliates/selectors.py owner-scoping helpers"                # T006
Task: "Create apps/affiliates/services.py lifecycle state model"                 # T007
Task: "Create seed command apps/affiliates/management/commands/seed_affiliates.py" # T010
Task: "Tests apps/affiliates/tests/test_models.py"                               # T011
Task: "Tests apps/affiliates/tests/test_services.py"                             # T012
```

## Parallel Example: User Story 1 tests

```bash
Task: "Tests in apps/affiliates/tests/test_selectors.py"     # T019
Task: "Tests in apps/affiliates/tests/test_views_list.py"    # T020
```

---

## Implementation Strategy

### MVP First (User Story 1 only)

1. Phase 1 Setup → 2. Phase 2 Foundational (CRITICAL) → 3. Phase 3 US1.
4. **STOP & VALIDATE**: seed two merchants, verify owner-scoped DB-backed roster + filters + empty state + truthful-zero columns, visual parity.
5. Demo the MVP.

### Incremental Delivery

Foundation ready → US1 (browse roster, MVP) → US2 (approve/reject requests) → US3 (detail) → US4 (suspend/reactivate/level/notes) → US5 (isolation verification). Each story is a deployable increment that doesn't break the previous ones. Run that story's tests + manual parity check before moving on; commit after each story.

### Parallel Team Strategy

After Foundational: Developer A → US1; Developer B → US2; Developer C → US3; then US4 wires both US1 and US3 templates (coordinate the two template files), US5 consolidates verification. Stories integrate via the shared `views.py`/`urls.py` append points.

---

## Notes

- `[P]` = different files, no dependency on an incomplete task.
- `[Story]` label maps each task to its user story for traceability.
- Principle I (frontend preservation) is non-negotiable: the only sanctioned UI changes are the two
  in-style integration additions — completing the list page's triggered-but-undefined confirmation modals
  (T036) and the detail notes-edit affordance (T037). Every other class, `data-*` hook, modal, badge, and
  RTL detail stays verbatim. Run the visual-parity check before closing a story.
- Principle IV (owner isolation) is non-negotiable: never use a bare `AffiliateProfile.objects` in a view
  — always the owner-scoped selectors (`merchant_affiliates` / `get_owned_affiliate_or_404`).
- Principle V (truthful data): all order/commission/payout figures render as 0 / empty-state — never
  carried-over sample numbers.
- Total: **48 tasks** — Setup 2, Foundational 10, US1 9, US2 7, US3 5, US4 6, US5 3, Polish 6.
