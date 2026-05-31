# Data Model: Backend Foundation (Django Conversion — Phase 0)

**Feature**: 003-backend-foundation
**Date**: 2026-05-31

The foundation phase introduces the **minimum** persistent model needed to prove role-based
authentication and redirect. Domain models (Product, Order, Customer, Affiliate, Commission,
Payout, LandingPage, Notification) are explicitly **out of scope** here (FR-016) and are added
in later phases. Their apps are scaffolded empty.

---

## Entity: User (`apps/accounts/models.py`)

Custom user model, set as `AUTH_USER_MODEL = 'accounts.User'` before the first migration.

| Field | Type | Notes |
|---|---|---|
| (inherited) | `AbstractUser` fields | `username`, `email`, `password`, `first_name`, `last_name`, `is_staff`, `is_superuser`, `is_active`, `date_joined`, `last_login` |
| `role` | `CharField(choices=Role, default=Role.MERCHANT, max_length=16)` | Primary role used for post-login redirect and (later) access scoping |

### `Role` (TextChoices)

| Value | Label | Post-login landing |
|---|---|---|
| `MERCHANT` | تاجر (Merchant / Owner) | `/dashboard.html` (merchant dashboard) |
| `AFFILIATE` | مسوّق بالعمولة (Affiliate Marketer) | `/affiliate-dashboard.html` (affiliate portal) |
| `ADMIN` | مدير (Admin / Staff) | `/admin/` (Django admin) |

**Validation / rules**:
- Every user has exactly one `role`; default `MERCHANT` (registration default per spec).
- `email` is `unique=True` (required for unambiguous email-based login).
- **Authentication**: `USERNAME_FIELD` stays `username` (canonical unique identifier), but login
  accepts the **email** entered in the preserved login form via a custom email-or-username backend
  registered in `AUTHENTICATION_BACKENDS` (`apps/accounts/backends.py`).
- `role = ADMIN` SHOULD coincide with `is_staff = True` so the admin site is reachable; a
  superuser is `ADMIN` for redirect purposes (and `createsuperuser` SHOULD set `role=ADMIN`).
- An authenticated user whose `role` does not resolve to a known landing is redirected to a
  safe public page (must not error) — see auth contract.

**Helper methods (convenience, on the model or a manager)**:
- `is_merchant` / `is_affiliate` / `is_admin` boolean properties — used by access mixins and
  the role-dispatch view; keeps role checks centralized and testable. `is_admin` returns True when
  `role == ADMIN` **or** the user `is_staff`/`is_superuser`, so a default superuser is treated as
  admin for redirect/gating even before its `role` is set.

**Relationships**: none in this phase. Later phases will relate `User` to `MerchantProfile`,
`AffiliateProfile`, and owned domain records (Products, Orders, …) — not modeled here.

---

## Not modeled in this phase (deferred, apps scaffolded empty)

| App | Future entities (NOT in phase 0) |
|---|---|
| `merchants` | MerchantProfile / store settings |
| `products` | Product, Category, ProductImage |
| `orders` | Order, OrderItem (with status/payment/shipping enums from constitution) |
| `customers` | Customer (merchant-owned, PII-masked for affiliates) |
| `affiliates` | Affiliate (level, status, referral code, coupon) |
| `commissions` | Commission (state machine per constitution) |
| `payouts` | PayoutRequest (status: requested/approved/rejected/paid) |
| `landing_pages` | LandingPage |
| `notifications` | Notification |
| `dashboard` | no models — aggregates/queries only (later) |
| `core` | no models — shared utilities, page registry, base context |

These tables MUST NOT be created in phase 0; only `accounts.User` (plus Django's built-in auth/
admin/sessions/contenttypes tables) is migrated.

---

## Migration footprint (phase 0)

- `accounts` initial migration creating the custom `User` table.
- Django built-in app migrations (`auth`, `admin`, `contenttypes`, `sessions`).
- No other app produces migrations (they have no models).
