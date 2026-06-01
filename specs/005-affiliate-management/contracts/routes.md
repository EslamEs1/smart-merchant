# Routes & Action Contract: Merchant Affiliate Management (MVP Phase 2)

**Feature**: 005-affiliate-management
**Date**: 2026-06-01

The "interface contract" for this server-rendered Django app is the **URL → view → template → access**
map plus the **action/validation** behaviour and the **legacy-redirect** contract. Authoritative for what
this phase must serve. All affiliate views require an authenticated **Merchant** and are **owner-scoped**.

---

## Access levels

- **merchant** — `@role_required("is_merchant")`: login required + `request.user.is_merchant`.
  Non-merchant roles (incl. affiliate) → 403; unauthenticated → redirect to `LOGIN_URL` (`/login.html`).
- **owner-scoped** — the affiliate must belong to `request.user`; otherwise **404** (existence not
  leaked) via `get_owned_affiliate_or_404(user, pk)`.

---

## Clean routes (`apps/affiliates/urls.py`, `app_name = "affiliates"`)

| Name | URL | Method(s) | View | Template | Access | Behaviour |
|---|---|---|---|---|---|---|
| `list` | `/affiliates/` | GET | `affiliate_list` | `affiliates/affiliate_list.html` | merchant | Owner's affiliates, filtered (q/status/level) + paginated. Empty → empty-state. Performance columns = truthful zeros. |
| `requests` | `/affiliates/requests/` | GET | `affiliate_requests` | `affiliates/affiliate_requests.html` | merchant | Owner's **Pending** affiliates as request cards, optionally narrowed by `q` search (FR-008); pending count truthful. Empty → empty-state. |
| `detail` | `/affiliates/<int:pk>/` | GET | `affiliate_detail` | `affiliates/affiliate_detail.html` | merchant, owner-scoped | Render owner's affiliate; order/commission/payout sections show zero/empty-state. |
| `approve` | `/affiliates/<int:pk>/approve/` | POST | `affiliate_approve` | — | merchant, owner-scoped | Pending → `Active`, set `approved_at`; redirect back (requests/detail) + message. |
| `reject` | `/affiliates/<int:pk>/reject/` | POST | `affiliate_reject` | — | merchant, owner-scoped | Pending → `Rejected`, set `rejected_at`; optional `reason`; redirect + message. |
| `suspend` | `/affiliates/<int:pk>/suspend/` | POST | `affiliate_suspend` | — | merchant, owner-scoped | Active → `Suspended`, set `suspended_at`; optional `reason`; redirect to `detail` + message. |
| `reactivate` | `/affiliates/<int:pk>/reactivate/` | POST | `affiliate_reactivate` | — | merchant, owner-scoped | Suspended → `Active`; redirect to `detail` + message. *(adds FR-013; not in the spec's URL list)* |
| `change-level` | `/affiliates/<int:pk>/change-level/` | POST | `affiliate_change_level` | — | merchant, owner-scoped | Validate `level ∈ {Bronze,Silver,Gold,Platinum}` → set; redirect to `detail` + message; invalid → reject, no change. |
| `notes` | `/affiliates/<int:pk>/notes/` | POST | `affiliate_edit_notes` | — | merchant, owner-scoped | Set `notes`; redirect to `detail` + message. *(satisfies FR-015; not in the spec's URL list)* |

**Notes**
- `<int:pk>` is resolved within the owner queryset, so cross-merchant ids → 404.
- Place `requests/` before `<int:pk>/` for readability (the `int` converter already excludes
  non-numeric "requests").
- All POST routes are CSRF-protected (`{% csrf_token %}` in the modal/menu forms) and reject non-POST
  with 405 (`require_POST`). GET routes are side-effect-free.
- Decorator order on mutations: `@role_required("is_merchant")` **outer**, `@require_POST` **inner**
  (role/auth checked before method — matches `004`).
- `reactivate` and `notes` URLs are **added** beyond the spec's listed set because FR-013 (reactivate)
  and FR-015 (edit notes) require them; recorded here and in the plan.

## Legacy redirects (preserve inbound `*.html` links; removed from `apps/core/page_registry.py`)

| Legacy URL | Redirect → | Type |
|---|---|---|
| `/affiliates.html` | `affiliates:list` | permanent (301) |
| `/affiliate-detail.html` | `affiliates:list` | permanent (301) — no id in the static link |
| `/affiliate-requests.html` | `affiliates:requests` | permanent (301) |

Registered in `apps/affiliates/urls.py`; `config/urls.py` includes `apps.affiliates.urls` **before**
`apps.core.urls` so these win over the page registry. `affiliate-payouts.html` stays in the registry
(out of scope). The merchant sidebar's affiliates link is repointed to `{% url 'affiliates:list' %}`.

---

## Filter contract (list view query params)

| Param | Values | Effect |
|---|---|---|
| `q` | free text | `full_name__icontains` OR `referral_code__icontains` |
| `status` | `Pending` / `Active` / `Suspended` / `Rejected` | exact status |
| `level` | `Bronze` / `Silver` / `Gold` / `Platinum` | exact level |
| `page` | integer | Django Paginator page |

- Unknown/blank params ignored; filters combine with AND; active filters echoed back into the controls
  and preserved across pagination via the querystring. No-match → empty-state.
- These three controls already exist in the prototype filter bar (search + status `<select>` + level
  `<select>`) — **no new filter controls are added** (unlike `004`).

### Requests view query param (FR-008)

| Param | Values | Effect |
|---|---|---|
| `q` | free text | within the owner's **Pending** affiliates: `full_name__icontains` OR `referral_code__icontains` |

- The requests page's **existing** search input (`affiliate-requests.html`) is wired to this `q` — no new
  control is added; the value is echoed back. Date-of-request / status affordances are **not** surfaced
  (all rows are Pending; FR-008 marks them MAY and the prototype provides only the search box).

---

## Action / form contract (`apps/affiliates/forms.py` + POST handlers)

Lifecycle actions follow `004`'s pattern: thin `@require_POST` views calling `services.py`, owner-scoped
via `get_owned_affiliate_or_404`. Two actions carry validated input via light forms; the rest read an
optional free-text `reason`.

| Action | Input | Validation | On success | On invalid |
|---|---|---|---|---|
| approve | — | guard: status == Pending | Active + `approved_at`; redirect; message | non-Pending → no-op + message |
| reject | `reason` (optional) | guard: status == Pending | Rejected + `rejected_at`; reason → notes; redirect | non-Pending → no-op |
| suspend | `reason` (optional) | guard: status == Active | Suspended + `suspended_at`; reason → notes; redirect | non-Active → no-op |
| reactivate | — | guard: status == Suspended | Active; redirect | non-Suspended → no-op |
| change-level | `level` | `AffiliateChangeLevelForm`: `level ∈ Level.choices` | level set; redirect; message | re-render/redirect with error; nothing saved |
| edit-notes | `notes` | `AffiliateNotesForm` (`ModelForm`, fields=["notes"]) | notes set; redirect; message | redirect with error |

- **`AffiliateChangeLevelForm`** (`forms.Form`): `level = ChoiceField(choices=AffiliateProfile.Level.choices)`.
- **`AffiliateNotesForm`** (`forms.ModelForm`): `Meta.model = AffiliateProfile`, `fields = ["notes"]`.
- The owner is **never** trusted from the form; it is the scoped object's existing `merchant`.
- There is **no public create form** this phase (no affiliate self-registration); affiliates arrive via
  seed/admin and are managed by the merchant. (A merchant-facing create form is out of scope per spec.)

---

## In-style UI additions wired by this contract (Principle I carve-out — see plan Complexity Tracking)

- **List page**: the dropdown's existing `data-modal-trigger="modal-approve|modal-suspend|modal-change-level"`
  buttons get **per-affiliate** modal bodies (`modal-approve-<pk>` etc.) wired to the POST forms above —
  the prototype ships these triggers with **no modal definitions**, so this completes its own contract.
- **Detail page**: the existing `modal-suspend-detail` is wired to `suspend`; an in-style notes-edit
  affordance is added for `edit-notes`; the status-appropriate primary action is shown (Pending→approve,
  Suspended→reactivate); `change-level` reuses an in-style level `<select>` modal.
- Out-of-scope affordances ("صرف العمولة" / disburse, "دفع عمولة" / pay commission, "عرض الطلبات" / view
  orders) remain visually present but inert (no fabricated money movement).

---

## Manual acceptance hooks (see quickstart.md)

1. Owner-scoping: merchant A cannot GET/POST any of merchant B's affiliate URLs → 404.
2. Roster: DB-backed rows, three filters + combination narrow correctly; no-match & zero-affiliate → empty-state; performance columns = 0.
3. Requests: Pending listed with truthful count; the search box narrows by name/referral code (FR-008); approve → Active (leaves queue); reject → Rejected (leaves queue).
4. Lifecycle: suspend → Suspended; reactivate → Active; change-level persists + badge updates; edit-notes persists. All POST + CSRF; GET → 405.
5. Codes: duplicate referral code (global) rejected; duplicate coupon within a merchant rejected; same coupon under another merchant allowed.
6. Access: affiliate-role → 403 on every page; anonymous → redirect to `/login.html`.
7. Link integrity & visual parity: legacy `*.html` redirect to clean URLs; pages pixel-equivalent to the static originals except the sanctioned in-style additions; badges, dropdowns, modals, copy buttons, theme toggle, RTL all work.
