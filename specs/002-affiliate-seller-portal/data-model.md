# Data Model: Affiliate Seller Portal — Static Frontend

**Feature**: 002-affiliate-seller-portal
**Date**: 2026-05-11
**Purpose**: There is no database and no API. This document defines the **shape of the hardcoded content** each affiliate page must contain, so authors write consistent, internally-coherent sample data across all six pages. It complements `SAMPLE-DATA.md` (project-wide conventions) and `data-model.md` of feature `001`.

All fields are written directly into HTML. "Currency token" means a value carries its currency inline, e.g. `280 ر.س`, `850 ج.م`, `320 د.إ` — and is **consistent across all monetary fields of one entity** (one product, one order row, one earnings row).

---

## 1. Affiliate (the logged-in user — single instance)

| Field | Type / values | Notes |
|---|---|---|
| `name` | string | `أحمد الشمري` (persona "أحمد"); consistent with `AFF-001` |
| `avatar` | image ref | `assets/img/placeholders/affiliate-avatar.svg`, `alt="صورة أحمد الشمري"` |
| `level` | `Bronze` \| `Silver` \| `Gold` \| `Platinum` | `Gold` → `.badge-gold` |
| `referralLink` | URL string | `https://smartmerchant.os/r/AHMAD20` |
| `couponCode` | string | `AHMAD20` |
| `qrPlaceholder` | image ref | `assets/img/placeholders/qr-code.svg`, `alt="رمز QR لرابط الإحالة"` |
| `accountStatus` | `Active` \| `Pending` \| `Suspended` | `Active` → `.badge-active` |
| `paymentMethod` | string | e.g. `محفظة STC Pay — 0555•••41` (masked) |
| `contact.email` | string (masked) | e.g. `ahm•••@gmail.com` |
| `contact.phone` | string (masked) | e.g. `0555 •• •• 41` |
| `contact.city` / `contact.country` | string | e.g. `الرياض` / `السعودية` |
| `availableBalance` | currency token | `1,420 ر.س` — MUST equal Σ earnings where status = `Approved` |
| `totalEarnings` | currency token | MUST equal Σ earnings where status ∈ {Approved, Paid, Pending} (i.e., excludes Rejected) |
| `underReviewEarnings` | currency token | MUST equal Σ earnings where status = `Pending` |
| `paidEarnings` | currency token | MUST equal Σ earnings where status = `Paid` |
| `successfulOrdersCount` | int | MUST equal count of orders where status = `Delivered` |
| `savedProductsCount` | int | MUST equal the number of cards on `affiliate-saved-products.html` |

Appears on: `affiliate-dashboard.html` (welcome header, quick-earnings card, top header), `affiliate-profile.html` (full), every page's top header (name + availableBalance pill + avatar).

---

## 2. Product (sellable item — ≥16 distinct instances, defined once, reused everywhere)

| Field | Type / values | Notes |
|---|---|---|
| `id` | string | e.g. `AP-001` … `AP-016+` (affiliate-product) |
| `name` | string (Arabic, ~80%) / Latin (~20%) | e.g. `سماعات بلوتوث لاسلكية`, `Smart Watch Pro` |
| `category` | one of: `الأكثر مبيعًا` \| `عروض` \| `إلكترونيات` \| `ملابس` \| `أدوات منزلية` \| `إكسسوارات` | drives which category tab "owns" it; `الكل` shows all |
| `badge` | `Bestseller` \| `New` \| `Hot Offer` \| _none_ | → `.badge-bestseller` / `.badge-new` / `.badge-hot`; a card with no badge must still align in its row |
| `images` | list of image refs (≥3) | all `assets/img/placeholders/product.svg` for now; each with `alt` = product name; first is the card image & gallery main |
| `videoThumbs` | list of image refs (≥2) | placeholder thumbnails (reuse `product.svg` or `dashboard-preview.svg`) with a play-icon overlay; product-detail page only |
| `shortDescription` | string (1–2 sentences) | product-detail page only — NEVER on the card |
| `supplierPrice` | currency token | `سعر المورد`, e.g. `180 ر.س` |
| `suggestedPrice` | currency token | `سعر البيع المقترح`, e.g. `280 ر.س` — same currency as `supplierPrice` |
| `wasPrice` | currency token \| null | optional strikethrough "كان" for `Hot Offer` products only |
| `affiliateProfit` | currency token | `صافي ربحك` ≈ `suggestedPrice − supplierPrice`, roughly 15–25% of suggested; "ربح عالي" products ≥ `60` in their currency |
| `readyCaption` | multi-line string | 2–4 lines, friendly tone, 1–3 emoji, 2–4 hashtags — the value behind the caption box's `[data-copy]` |
| `readyDetails` | multi-line string | bullet-style specs/benefits — the value behind the details box's `[data-copy]` |
| `sellingTips` | list of 2–3 strings | shown in the "نصائح للبيع" section |
| `relatedIds` | list of 4 product ids | same `category` preferably; powers the related-products section |
| `currency` | `SAR` \| `EGP` \| `AED` \| other | the single currency for all monetary fields of this product |
| `isFavorited` | bool | initial DOM state of the heart; ~3–5 products start favorited (these are the ones shown on the saved page) |

### Dashboard section assignment (so the 4 sections are populated and distinct)

| Section heading | Cards | Rule |
|---|---|---|
| `الأكثر مبيعًا` | 5 | mostly `Bestseller` badge; high `suggestedPrice` variety |
| `عروض قوية اليوم` | 5 | all `Hot Offer` badge + `wasPrice` strikethrough |
| `منتجات جديدة` | 5 | all `New` badge |
| `ربح عالي` | 5 | all have `affiliateProfit` ≥ `60` (in their own currency) |

Products may repeat across sections (a bestseller can also be high-profit). Each section has a `عرض الكل` link → `affiliate-dashboard.html#<section-anchor>` (or `affiliate-saved-products.html` is NOT a substitute — these are browse links; pointing them at the dashboard anchor is acceptable since no standalone catalogue page is in scope; document this in the contract).

### Product card — the EXACT field set rendered on a card (and nowhere more)

`images[0]` → · `badge` (if any) → · `name` → · `suggestedPrice` (labeled "سعر البيع") → · `affiliateProfit` (labeled "أرباحك", emphasized) → · favorite heart (`[data-favorite-toggle]`, reflects `isFavorited`) → · `عرض التفاصيل` button → `affiliate-product-detail.html`. **No** `shortDescription`, **no** ratings, **no** stock, **no** supplier price on the card.

Appears on: `affiliate-dashboard.html` (4 sections), `affiliate-saved-products.html` (grid), `affiliate-product-detail.html` (related-products section), and one Product is the subject of `affiliate-product-detail.html` (full field set).

---

## 3. Affiliate Order (current affiliate's orders only — ≥12 rows)

| Field | Type / values | Notes |
|---|---|---|
| `orderNumber` | string | `AO-2026-0001` … |
| `customerMasked` | string | EITHER masked name (`أحمد ا***`, `Sara H***`) OR masked phone (`055•• ••• 41`) — mix both styles; **never** a full name + full phone + address together; **never** an email |
| `productName` | string | references a Product `name` |
| `status` | `Pending` \| `Confirmed` \| `Processing` \| `Delivered` \| `Cancelled` | → `.badge-pending` / `.badge-confirmed` / `.badge-processing` / `.badge-delivered` / `.badge-cancelled`; `Cancelled` visually distinct (rose) |
| `commission` | currency token | consistent currency within the row |
| `date` | date string | Arabic-friendly, e.g. `12 مايو 2026` or `2026-05-12`; range ≈ 2026-04-01 → 2026-05-11 |

### Status distribution (≈12 rows) & summary-card math

| Status | ≈ count |
|---|---|
| `Delivered` | 4 |
| `Processing` | 2 |
| `Confirmed` | 1 |
| `Pending` | 2 |
| `Cancelled` | 2–3 |

Summary cards on `affiliate-orders.html` (must add up):
- `كل الطلبات` = total rows
- `قيد التنفيذ` = Pending + Confirmed + Processing
- `تم التسليم` = Delivered
- `ملغية` = Cancelled

Rendering: stacked **cards** on mobile (`<lg`), **table** on desktop (`lg:`). Filter bar: status chips (`الكل` / `قيد التنفيذ` / `تم التسليم` / `ملغية` or per-status) using `[data-segment]` — visual active state only; a search input (placeholder `ابحث برقم الطلب أو المنتج...`) — visual only.

Appears on: `affiliate-orders.html`.

---

## 4. Earning / Commission record (≥12 rows)

| Field | Type / values | Notes |
|---|---|---|
| `productName` | string | references a Product `name` |
| `orderNumber` | string | references an Order `orderNumber` where sensible (cross-consistency boosts credibility) |
| `commission` | currency token | consistent currency within the row; should match the referenced order's commission when cross-referenced |
| `status` | `Pending` \| `Approved` \| `Paid` \| `Rejected` | → `.badge-pending` / `.badge-confirmed` / `.badge-paid` / `.badge-rejected`; `Rejected` visually distinct (rose) |
| `date` | date string | same format/range as orders |

### Status distribution (≈12 rows) & card math

| Status | ≈ count |
|---|---|
| `Paid` | 4 |
| `Approved` | 4 |
| `Pending` | 3 |
| `Rejected` | 1 |

Cards on `affiliate-earnings.html` (must be internally coherent):
- `الأرباح المتاحة للسحب` (main card, gradient) = Σ commissions where status = `Approved`  → equals Affiliate.`availableBalance` (`1,420 ر.س`)
- `إجمالي الأرباح` = Σ commissions where status ∈ {Approved, Paid, Pending}
- `أرباح قيد المراجعة` = Σ commissions where status = `Pending`
- `أرباح مدفوعة` = Σ commissions where status = `Paid`

Mandatory notice text on the page: **"يتم اعتماد العمولة بعد تأكيد الدفع أو تسليم الطلب."**

Rendering: stacked cards on mobile, table on desktop (same pattern as orders).

Appears on: `affiliate-earnings.html`.

---

## 5. Payout request (transient — modal only, not persisted)

| Field | Type | Notes |
|---|---|---|
| `amount` | number input | placeholder/prefill `1,420`; helper text "الحد الأدنى للسحب 100 ر.س" |
| `paymentMethod` | select | options: `محفظة STC Pay` / `تحويل بنكي` / `محفظة فودافون كاش` / `PayPal` |
| `walletOrAccount` | text input | placeholder "رقم المحفظة أو الحساب البنكي (IBAN)" |
| `notes` | textarea | optional |
| (controls) | — | `تأكيد طلب السحب` (primary, no-op / shows the copy toast or closes), `إلغاء` (`[data-modal-close]`) |

Modal id: `payout-modal`; opened by `[data-modal-trigger="payout-modal"]` from the "طلب سحب" button on `affiliate-earnings.html` (and optionally surfaced on `affiliate-profile.html`). Dismiss: backdrop click, `[data-modal-close]`, ESC — all already handled by `initModals()`.

---

## 6. Navigation model (the affiliate shell)

| Surface | Items (RTL order) | Targets |
|---|---|---|
| Mobile bottom nav (`lg:hidden`) | الرئيسية · المنتجات · المحفوظات · الطلبات · الأرباح | `affiliate-dashboard.html` · `affiliate-dashboard.html#products` · `affiliate-saved-products.html` · `affiliate-orders.html` · `affiliate-earnings.html` |
| Desktop sidebar (`hidden lg:flex`) | same 5 + الملف الشخصي | + `affiliate-profile.html` |
| Top header | profile avatar (→ `affiliate-profile.html`) · name · earnings pill · search · notification bell dropdown · (lg) "بوابة المسوّق" wordmark | — |

Active item: the one matching the current page gets `is-active` + `aria-current="page"`. Every link MUST resolve to a file that ships in this feature (or an existing file). No dead links (FR-072).

---

## Cross-entity consistency checklist (authors verify before "done")

1. Affiliate.`availableBalance` == Σ Earnings[status=Approved] == `الأرباح المتاحة للسحب` card == payout modal prefill.
2. Affiliate.`successfulOrdersCount` == count Orders[status=Delivered] == dashboard "الطلبات الناجحة" == orders "تم التسليم" card.
3. Affiliate.`savedProductsCount` == cards on `affiliate-saved-products.html` == dashboard "المنتجات المحفوظة".
4. Orders summary cards add up to `كل الطلبات`.
5. Earnings cards are mutually coherent (Pending + Approved + Paid sums into "إجمالي الأرباح"; "أرباح مدفوعة" = Σ Paid; etc.).
6. Every Earnings row that cites an `orderNumber` cites one that exists in the Orders list with the same `commission` and currency.
7. Currency tokens never mix within a row/entity; overall mix ≈ SAR 50% / EGP 25% / AED 20% / other 5–10% across the prototype.
8. Names ≈ 80% Arabic-script, 20% Latin-script; persona is "أحمد الشمري", Gold.
9. Product cards render exactly the §2 field set — no extra fields, no descriptions.
10. The product featured on `affiliate-product-detail.html` has all of: ≥3 gallery images, ≥2 video thumbs, badges, short description, pricing trio (supplier/suggested/profit), ready caption, ready details, 2–3 tips, 4 related cards.
