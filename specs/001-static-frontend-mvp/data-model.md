# Data Model: Smart Merchant OS — Static Frontend MVP

**Feature**: 001-static-frontend-mvp
**Date**: 2026-05-10
**Purpose**: Concrete entity schemas authors use to write hardcoded sample
data into HTML pages. There is no database, no API, and no JSON file —
every record below is materialized inline in the HTML markup of the
relevant page(s).

> **Note on representation**: This document treats each entity like a
> column-and-type schema. Authors are free to interpret a "field" as an HTML
> table cell, a `<dl>` row, a styled card section, or whatever the page
> design calls for. The schema's job is to lock in **what data each entity
> carries** so that cross-page references (e.g., an order showing its
> affiliate's name) stay consistent.

---

## Entity: Product

**Surface**: `products.html` (rows), `product-detail.html`, `product-create.html`/`product-edit.html` (form fields)

| Field | Type | Required | Constraints / Notes |
|---|---|---|---|
| `id` | string | yes | Slug-like, e.g., `prd-001`; used for detail URL anchor |
| `name` | string (Arabic primary) | yes | 30–60 chars typical |
| `type` | enum | yes | One of: `منتج فعلي`, `خدمة`, `كورس`, `ديجيتال برودكت`, `اشتراك` |
| `description` | string | yes | 1–3 short Arabic paragraphs |
| `price` | number | yes | Always paired with `currency` |
| `currency` | enum | yes | `SAR` \| `EGP` \| `AED` \| `KWD` \| `USD` |
| `discountPrice` | number\|null | no | When non-null, must be < `price` |
| `stock` | integer | yes | Non-negative; for non-physical types may be `999` (effectively unlimited) |
| `status` | enum | yes | `active` \| `draft` \| `disabled` |
| `salesCount` | integer | yes | Number of units sold; used in list and detail |
| `imageUrl` | string | yes | Path to local SVG placeholder; never a broken link |
| `gallery[]` | string[] | optional | 2–4 additional image placeholders for detail page |
| `videoUrl` | string\|null | no | YouTube/Vimeo URL or null |
| `seoTitle` | string | yes (in form) | 30–60 chars |
| `seoDescription` | string | yes (in form) | 70–160 chars |
| `slug` | string | yes | Used in "Copy public link" action; format: `/p/<slug>` |
| `relatedOrders[]` | Order[] | derived | 5–8 orders shown on detail page |
| `topAffiliatesForProduct[]` | Affiliate[] | derived | 3–5 entries shown on detail page |
| `activityTimeline[]` | TimelineEvent[] | derived | 4–6 events on detail page |

**Distribution rule** (sample data): At least one row per product `type`; status
mix ≈ 70% active / 20% draft / 10% disabled; ~30% of rows have a `discountPrice`.

---

## Entity: Order

**Surface**: `orders.html` (rows), `order-detail.html`, `order-edit.html` (form fields), `dashboard.html` recent-orders card

| Field | Type | Required | Constraints / Notes |
|---|---|---|---|
| `orderNumber` | string | yes | Format `#SMO-{6-digit}` (e.g., `#SMO-100423`) |
| `customer` | Customer (FK) | yes | Reference by name; full Customer entity drives detail page |
| `product` | Product (FK) | yes | Reference by name; multi-line item products are out of MVP scope |
| `affiliate` | Affiliate (FK)\|null | no | When null, render `—` or `بدون مسوّق` |
| `total` | number | yes | Paired with `currency` |
| `currency` | enum | yes | Must match the product's currency for that order |
| `commission` | number | yes when affiliate ≠ null; else 0 | Same `currency` as total |
| `orderStatus` | enum | yes | `Pending` \| `Confirmed` \| `Processing` \| `Shipped` \| `Delivered` \| `Cancelled` |
| `paymentStatus` | enum | yes | `Unpaid` \| `Paid` \| `Partially Paid` \| `Refunded` |
| `shippingStatus` | enum | yes | `Not Shipped` \| `Preparing` \| `Shipped` \| `Delivered` \| `Returned` |
| `date` | string (date) | yes | ISO `YYYY-MM-DD` in tables; humanized Arabic-month form on detail |
| `notes` | string | optional | Internal merchant notes |
| `timeline[]` | TimelineEvent[] | yes (detail page) | 4–7 events showing lifecycle |
| `invoicePreview` | InvoiceCard | yes (detail page) | Inline component; see "InvoiceCard" below |

**Distribution rule** (orders.html: 14 rows):
- 8 with affiliate, 6 without
- Currency mix: 7 SAR, 4 EGP, 2 AED, 1 KWD/USD
- Status mix covering all six order statuses (≥1 per status)
- Payment status: 6 Paid, 3 Partially Paid, 3 Unpaid, 2 Refunded
- Shipping status: 4 Delivered, 4 Shipped, 3 Preparing, 2 Not Shipped, 1 Returned

**Cross-status validity** (sample data should respect):
- `paymentStatus=Refunded` typically pairs with `orderStatus=Cancelled` or returned.
- `shippingStatus=Delivered` requires `orderStatus∈{Shipped, Delivered}`.

---

## Entity: Affiliate

**Surface**: `affiliates.html` (rows), `affiliate-detail.html`, `dashboard.html` top-affiliates card

| Field | Type | Required | Constraints / Notes |
|---|---|---|---|
| `id` | string | yes | E.g., `aff-001` |
| `name` | string | yes | ≈80% Arabic, ≈20% Latin (per FR-038b) |
| `level` | enum | yes | `Bronze` \| `Silver` \| `Gold` \| `Platinum` |
| `status` | enum | yes | `Pending` \| `Active` \| `Suspended` \| `Rejected` |
| `referralCode` | string | yes | Format: `<3-letter-prefix>-<4-digit>` e.g., `AHM-2410` |
| `referralLink` | string | yes | Format: `https://smartmerchant.os/r/<code>` |
| `qrPlaceholderSvg` | inline SVG | yes (detail) | Static QR-pattern SVG; never a real QR |
| `couponCode` | string | yes | Uppercase, e.g., `AHMED20` |
| `clicks` | integer | yes | Lifetime click count |
| `orders` | integer | yes | Orders attributed to this affiliate |
| `salesAmount` | number | yes | Lifetime sales volume; paired with `currency` |
| `currency` | enum | yes | Affiliate's native currency for display purposes |
| `pendingCommission` | number | yes | Same `currency` |
| `paidCommission` | number | yes | Same `currency` |
| `conversionRate` | number (percent) | yes | E.g., `4.2` rendered as `4.2%` |
| `joinedDate` | string (date) | yes | When affiliate was approved |
| `socialLinks[]` | string[] | optional (detail) | Up to 3 (Instagram, TikTok, X/Twitter) |
| `marketingAssets[]` | Asset[] | yes (detail) | 3–5 banner/copy assets |
| `notes` | string | optional | Merchant's private notes |
| `activityTimeline[]` | TimelineEvent[] | yes (detail) | 5–8 events |
| `attributedOrders[]` | Order[] | yes (detail) | 6–10 orders shown on detail page |
| `payoutHistory[]` | AffiliatePayout[] | yes (detail) | 4–6 entries |

**Distribution rule** (affiliates.html: 10 rows):
- Level mix: 2 Bronze, 3 Silver, 3 Gold, 2 Platinum
- Status mix: 6 Active, 2 Pending, 1 Suspended, 1 Rejected
- Currency: distributed per spec (≈50% SAR, ≈25% EGP, ≈20% AED, ≈5% other)
- Names: ≈8 Arabic-script, ≈2 Latin

---

## Entity: AffiliateRequest

**Surface**: `affiliate-requests.html`

| Field | Type | Required | Notes |
|---|---|---|---|
| `applicantName` | string | yes | Arabic primary |
| `contact` | string | yes | Email or phone (E.164 with Arabic country) |
| `socialLinks[]` | string[] | yes | 1–3 |
| `experience` | string | yes | 1–2 short Arabic paragraphs |
| `requestedDate` | string (date) | yes | ISO |
| `actions` | enum-set | n/a | UI-only: `Approve`, `Reject`, `View details` |

**Sample volume**: 6 rows.

---

## Entity: AffiliatePayout

**Surface**: `affiliate-payouts.html`, `affiliate-detail.html` payout history

| Field | Type | Required | Notes |
|---|---|---|---|
| `affiliate` | Affiliate (FK) | yes | Reference by name |
| `requestedAmount` | number | yes | + `currency` |
| `availableBalance` | number | yes | + `currency` |
| `paymentMethod` | enum | yes | `Bank Transfer` \| `STC Pay` \| `Vodafone Cash` \| `Instapay` \| `PayPal` \| `Wise` |
| `currency` | enum | yes | Same enum as Order |
| `status` | enum | yes | `Pending` \| `Paid` \| `Rejected` |
| `requestDate` | string (date) | yes | ISO |
| `actions` | enum-set | n/a | UI-only: `Approve`, `Reject`, `View` |

**Sample volume** (per tab):
- Pending: 5 rows
- Paid: 6 rows
- Rejected: 3 rows

---

## Entity: Customer

**Surface**: `customers.html` (rows), `customer-detail.html`, `customer-edit.html` (form fields)

| Field | Type | Required | Constraints / Notes |
|---|---|---|---|
| `id` | string | yes | E.g., `cus-001` |
| `name` | string | yes | Arabic primary, ≈80/20 distribution |
| `phone` | string | yes | E.164 with Arabic country code (e.g., `+966 …`) |
| `email` | string\|null | optional | Some Manual/WhatsApp customers may have no email |
| `address` | string | yes (edit form) | One Arabic line, city + region |
| `source` | enum | yes | `Direct` \| `Affiliate` \| `WhatsApp` \| `Facebook` \| `Instagram` \| `TikTok` \| `Manual` |
| `affiliate` | Affiliate (FK)\|null | yes when source=Affiliate; else null | Render `—` if null |
| `ordersCount` | integer | yes | Lifetime |
| `totalSpent` | number | yes | Paired with `currency` |
| `currency` | enum | yes | Customer's primary currency |
| `lastOrderDate` | string (date)\|null | yes (or null if no orders yet) | ISO |
| `tags[]` | string[] | yes | 1–4 short Arabic tags (e.g., `VIP`, `جديد`, `متابعة`) |
| `notes` | string | optional | Free-form Arabic |
| `followUpStatus` | enum | yes (detail) | `Open` \| `In Progress` \| `Done` |
| `followUpDate` | string (date)\|null | yes (edit form) | When non-null, signals scheduled follow-up |
| `orderHistory[]` | Order[] | derived | 4–8 orders on detail page |
| `activityTimeline[]` | TimelineEvent[] | derived | 4–6 events |

**Distribution rule** (customers.html: 15 rows):
- Source coverage: ≥1 row per source value (7 sources × 1 = 7 minimum); remainder distributed by realism (more Affiliate, WhatsApp, Direct than Manual)
- Approximately one-third of source=Affiliate rows reference each level of affiliate
- Currency mix per spec
- Names ≈80/20 Arabic/Latin

---

## Entity: LandingPage

**Surface**: `landing-pages.html` (rows), `landing-page-create.html` (form fields), `landing-page-preview.html`

| Field | Type | Required | Constraints / Notes |
|---|---|---|---|
| `id` | string | yes | E.g., `lp-001` |
| `title` | string | yes | Arabic |
| `linkedProduct` | Product (FK) | yes | Reference by name |
| `template` | enum | yes | `Hero Classic` \| `Bold Offer` \| `Story-Driven` \| `Minimal` |
| `heroHeadline` | string | yes | Short Arabic punchy line |
| `subheadline` | string | yes | One Arabic sentence |
| `ctaText` | string | yes | Arabic button label |
| `offerPrice` | number | yes | + `currency` |
| `currency` | enum | yes | Matches the linked product's currency |
| `benefits[]` | string[] | yes | 3–5 short Arabic bullets |
| `testimonials[]` | Testimonial[] | yes (preview) | 2–3 placeholder testimonials |
| `faqs[]` | FaqEntry[] | yes (preview) | 4–6 Q&A pairs |
| `seoTitle` | string | yes (form) | |
| `seoDescription` | string | yes (form) | |
| `status` | enum | yes | `Published` \| `Draft` \| `Disabled` |
| `visits` | integer | yes | Lifetime |
| `conversionRate` | number (percent) | yes | E.g., `5.7` rendered as `5.7%` |
| `orders` | integer | yes | Conversions |
| `revenue` | number | yes | + `currency` |
| `lastUpdated` | string (date) | yes | ISO |

**Sample volume**: 8 rows.

---

## Entity: Notification

**Surface**: `notifications.html`

| Field | Type | Required | Notes |
|---|---|---|---|
| `category` | enum | yes | `new-order` \| `affiliate-request` \| `payout-request` \| `low-stock` \| `payment-update` |
| `title` | string | yes | Arabic, short |
| `summary` | string | yes | One Arabic sentence |
| `actor` | string | yes (when applicable) | E.g., customer or affiliate name |
| `timestamp` | string | yes | Relative Arabic ("منذ ٥ دقائق") with absolute fallback |
| `read` | boolean | yes | ~30% read, ~70% unread for visual variety |
| `targetUrl` | string | yes | Link to relevant detail page |
| `iconKey` | enum | yes | Maps to a Lucide icon (e.g., `shopping-bag`, `handshake`, `wallet`, `package-x`, `credit-card`) |

**Sample volume**: 12 rows covering all 5 categories.

---

## Embedded value objects

### TimelineEvent

| Field | Type | Notes |
|---|---|---|
| `iconKey` | enum (Lucide name) | E.g., `check-circle-2`, `truck`, `pencil`, `coins` |
| `tone` | enum | `info` \| `success` \| `warning` \| `danger` (drives badge color) |
| `title` | string | Arabic, short |
| `description` | string | Arabic, one sentence |
| `actor` | string\|null | Person/system who caused the event |
| `timestamp` | string | Arabic-month date or relative time |

### InvoiceCard

| Field | Type | Notes |
|---|---|---|
| `invoiceNumber` | string | Format `INV-{6-digit}` |
| `issueDate` | string (date) | ISO |
| `dueDate` | string (date) | ISO |
| `lineItems[]` | { description, qty, unitPrice, currency }[] | 1–3 lines |
| `subtotal` | number | + currency |
| `tax` | number | + currency |
| `total` | number | + currency |

### Asset (marketing asset on Affiliate detail)

| Field | Type | Notes |
|---|---|---|
| `kind` | enum | `Banner` \| `Story` \| `Reel Caption` \| `Email Template` |
| `name` | string | Arabic |
| `previewUrl` | string | Local SVG placeholder |
| `downloadAction` | enum | `Copy Caption` \| `Download Banner` (UI affordance only) |

### Testimonial

| Field | Type | Notes |
|---|---|---|
| `authorName` | string | ≈80/20 Arabic/Latin |
| `authorRole` | string | Optional |
| `quote` | string | 1–2 Arabic sentences |
| `rating` | integer 1–5 | Renders as star icons |

### FaqEntry

| Field | Type | Notes |
|---|---|---|
| `question` | string | Arabic |
| `answer` | string | Arabic, 1–3 sentences |

---

## Cross-entity reference integrity

To make the prototype feel like a coherent system, authors **MUST** ensure
sample data references are bidirectional and consistent:

- An Order's `customer.name` and `affiliate.name` MUST appear in the
  Customers list and Affiliates list respectively.
- A Customer's `orderHistory[]` Order references MUST appear in the Orders
  list.
- An Affiliate's `attributedOrders[]` and `payoutHistory[]` MUST be
  internally consistent with their summary stats (`orders`, `salesAmount`,
  `pendingCommission`, `paidCommission`).
- A LandingPage's `linkedProduct.name` MUST appear in the Products list
  with matching `currency`.
- A Notification with `category=new-order` SHOULD reference an order number
  that exists in the Orders list (when feasible).

A short shared author note at the top of `partials/_sidebar.html` (or a
`SAMPLE-DATA.md` author crib) reminds writers of this contract. Drift is
acceptable in narrow cases (a single mismatched name) but the headline
demos (top affiliate's first attributed order, dashboard's top product,
home page's testimonial author) MUST be cross-consistent.

---

## State transitions (visual representation only)

These transitions inform what the **timeline** sections show; the prototype
does not enforce them programmatically.

### Order lifecycle
```
Pending → Confirmed → Processing → Shipped → Delivered
            ↓             ↓           ↓
         Cancelled    Cancelled   Returned (rare)
```

### Payment lifecycle
```
Unpaid → Partially Paid → Paid
              ↓             ↓
          (refundable)  Refunded
```

### Shipping lifecycle
```
Not Shipped → Preparing → Shipped → Delivered
                            ↓
                         Returned
```

### Affiliate lifecycle
```
[application] → Pending →─approved─→ Active ←──→ Suspended
                  ↓
               Rejected
```

### AffiliatePayout lifecycle
```
Pending → Paid
   ↓
Rejected
```

### LandingPage lifecycle
```
Draft → Published ←→ Disabled
```

These diagrams give the timeline-event author concrete vocabulary for
sample event sequences (e.g., a Delivered order's timeline shows
*Created → Confirmed → Processing → Shipped → Delivered* as the canonical
arc).

---

**Status**: Data model is complete and ready for tasks generation.
