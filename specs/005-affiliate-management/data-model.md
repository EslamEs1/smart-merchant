# Data Model: Merchant Affiliate Management (MVP Phase 2)

**Feature**: 005-affiliate-management
**Date**: 2026-06-01
**App**: `apps/affiliates` (migration `0001_initial`)

One new model, owner-scoped to `accounts.User` (a Merchant). English status/level tokens match the
prototype badges; all other content is Arabic/RTL. A Pending profile doubles as a join request (research
D1). No `ImageField`/media this phase.

---

## Entity: AffiliateProfile (`apps/affiliates/models.py`)

A marketer connected to exactly one merchant — the in-scope half of the affiliate domain (identity,
status, level, codes). Commission/order/payout data is out of scope and rendered as truthful zeros.

| Field | Type | Notes |
|---|---|---|
| `user` | `FK(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=SET_NULL, related_name="affiliate_links")` | The affiliate's own login account — **optional** this phase (seller portal is a later spec). Deleting the user keeps the merchant's record. |
| `merchant` | `FK(settings.AUTH_USER_MODEL, on_delete=CASCADE, related_name="affiliates")` | Owner (role MERCHANT); scopes **all** access |
| `full_name` | `CharField(max_length=150)` | Required; display name (Arabic or Latin) |
| `phone` | `CharField(max_length=32, blank=True)` | Optional |
| `email` | `EmailField(blank=True)` | Optional |
| `city` | `CharField(max_length=80, blank=True)` | Optional |
| `country` | `CharField(max_length=80, blank=True)` | Optional |
| `status` | `CharField(choices=Status, default=PENDING, max_length=10)` | `Pending/Active/Suspended/Rejected` |
| `level` | `CharField(choices=Level, default=BRONZE, max_length=10)` | `Bronze/Silver/Gold/Platinum` |
| `referral_code` | `CharField(max_length=32, unique=True)` | **Globally unique**; auto-generated (upper-cased slug + suffix) if blank |
| `coupon_code` | `CharField(max_length=32, blank=True)` | **Unique per merchant** for non-blank values |
| `bio` | `TextField(blank=True)` | Doubles as the applicant "experience" note on the requests page |
| `social_instagram` | `CharField(max_length=120, blank=True)` | Handle or URL |
| `social_tiktok` | `CharField(max_length=120, blank=True)` | Handle or URL |
| `social_facebook` | `CharField(max_length=120, blank=True)` | Handle or URL |
| `notes` | `TextField(blank=True)` | Merchant-private notes (editable — FR-015) |
| `approved_at` | `DateTimeField(null=True, blank=True)` | Set on approve |
| `rejected_at` | `DateTimeField(null=True, blank=True)` | Set on reject |
| `suspended_at` | `DateTimeField(null=True, blank=True)` | Set on suspend |
| `created_at` | `DateTimeField(auto_now_add=True)` | Join date shown on detail |
| `updated_at` | `DateTimeField(auto_now=True)` | |

- **`Status` (TextChoices)**: `PENDING="Pending"` (قيد المراجعة), `ACTIVE="Active"` (نشط),
  `SUSPENDED="Suspended"` (موقوف), `REJECTED="Rejected"` (مرفوض). Default `PENDING`. English tokens are
  rendered by the prototype badges (`badge-pending/active/suspended/...`).
- **`Level` (TextChoices)**: `BRONZE="Bronze"`, `SILVER="Silver"`, `GOLD="Gold"`, `PLATINUM="Platinum"`.
  Default `BRONZE`. Rendered by `badge-bronze/silver/gold/platinum`.
- **Constraints**:
  - `referral_code` `unique=True` (global).
  - `UniqueConstraint(fields=["merchant","coupon_code"], condition=~Q(coupon_code=""),
    name="uniq_coupon_per_merchant")` — per-merchant coupon uniqueness, blanks exempt.
- **Meta**: `ordering = ["-created_at"]`; `verbose_name = "مسوّق"`, `verbose_name_plural = "المسوّقون"`.
- **`save()`**: if `referral_code` is blank, generate a globally-unique code from `full_name`
  (upper-cased slug, numeric suffix on collision) — same auto-unique pattern as `004`'s slug generation.
- **Helpers / properties**:
  - `referral_link` → `f"{REFERRAL_BASE}/{referral_code}"` where `REFERRAL_BASE =
    "https://smartmerchant.os/r"` (module constant) — derived, never stored (research D3).
  - `get_absolute_url()` → `reverse("affiliates:detail", kwargs={"pk": self.pk})`.
  - `is_active` → `status == Status.ACTIVE`; `is_pending` → `status == Status.PENDING` (template
    convenience for badge/affordance branching).
- **Relationships**: one merchant → many affiliates; one (optional) user ↔ affiliate link.

### Visibility & filtering (selectors — this phase and the later commission phase)

| Selector | Returns |
|---|---|
| `merchant_affiliates(user)` | `AffiliateProfile.objects.filter(merchant=user).select_related("user")` — everything the owner manages (all statuses) |
| `get_owned_affiliate_or_404(user, pk)` | `get_object_or_404(AffiliateProfile, merchant=user, pk=pk)` — never leaks cross-merchant existence |
| `pending_affiliates(qs)` | `qs.filter(status=Status.PENDING)` — drives the requests queue + pending count |
| `active_affiliates(qs)` | `qs.filter(status=Status.ACTIVE)` — reused by the future affiliate-portal/commission phase |
| `list_affiliates(merchant, params)` | owner-scoped + optional filters: `q` (full_name OR referral_code, icontains), `status` (exact), `level` (exact) |

### State model (authoritative — implemented in `services.py`, research D5)

```text
            create / seed (default)
                  │
                  ▼
              ┌─ PENDING ─┐
       approve│           │reject
              ▼           ▼
            ACTIVE      REJECTED  (terminal this phase)
              │  ▲
       suspend│  │reactivate
              ▼  │
           SUSPENDED

   change_level(any status)  → level := {Bronze|Silver|Gold|Platinum}  (validated; status unchanged)
   set_notes(any status)     → notes := text                            (status unchanged)
```

| Transition (service) | Precondition (guard) | Effect | Idempotency / failure |
|---|---|---|---|
| `approve` | status == `Pending` | → `Active`, set `approved_at` | non-Pending → no-op (no timestamp overwrite) |
| `reject(reason="")` | status == `Pending` | → `Rejected`, set `rejected_at`, optional reason appended to notes | non-Pending → no-op |
| `suspend(reason="")` | status == `Active` | → `Suspended`, set `suspended_at`, optional reason appended to notes | non-Active → no-op |
| `reactivate` | status == `Suspended` | → `Active` | non-Suspended → no-op |
| `change_level(level)` | `level in Level.values` | set `level`, save | invalid value → reject (form/400), nothing saved |
| `set_notes(text)` | — | set `notes`, save | — |

- Saves use `update_fields` (e.g. `["status","approved_at","updated_at"]`) for precision, matching `004`.
- Level changes and notes edits are independent of status (allowed in any state).

---

## Migration footprint (this phase)

- `affiliates/0001_initial.py` creates `affiliates_affiliateprofile` with the two constraints above.
- No changes to `accounts.User` (only new reverse relations `affiliates`, `affiliate_links`).
- No `MEDIA_*` / no new dependency.

## Admin (`apps/affiliates/admin.py`)

| Model | list_display | search_fields | list_filter | extras |
|---|---|---|---|---|
| `AffiliateProfile` | full_name, merchant, level, status, referral_code, coupon_code, created_at | full_name, email, phone, referral_code, coupon_code | status, level | `readonly_fields` = created_at, updated_at, approved_at, rejected_at, suspended_at |

Admin is internal-only (constitution II); merchant management happens on the converted pages.

## Field → prototype mapping (preservation reference)

| Prototype element | Source |
|---|---|
| Roster: المسوق name + avatar | `full_name` (+ `{% static %}` avatar placeholder) |
| Roster: المستوى badge | `level` → `badge-<level>` |
| Roster: كود الإحالة chip | `referral_code` |
| Roster: الحالة badge | `status` → `badge-<status>` |
| Roster: الطلبات / المبيعات / عمولة معلقة / عمولة مدفوعة / معدل التحويل | **truthful zeros** (out of scope, research D7) |
| Detail: معلومات المسوق (البريد/الجوال/انستغرام/الدولة/تاريخ الانضمام) | `email`, `phone`, `social_instagram`, `country`, `created_at` |
| Detail: رابط الإحالة box + copy | `referral_link` property (`data-copy` preserved) |
| Detail: QR | `{% static %}` placeholder (no real generation) |
| Detail: كود الخصم chip + copy | `coupon_code` (`data-copy` preserved) |
| Detail: ملاحظات | `notes` (+ in-style edit affordance, FR-015) |
| Detail: stat cards / attributed orders / payouts / marketing captions | **truthful zeros / empty-state** |
| Requests card: name/contact/social/experience | `full_name`/contact/`social_*`/`bio` of Pending profiles |
