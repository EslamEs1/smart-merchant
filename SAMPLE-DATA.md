# Sample Data Reference — Smart Merchant OS

All HTML pages MUST use these canonical entities for cross-page consistency. See `specs/001-static-frontend-mvp/research.md` §7 and `specs/001-static-frontend-mvp/data-model.md` for full context.

## Currency Distribution Targets

Per `research.md` §7:

| Currency | Target Share | Symbol | Example |
|----------|-------------|--------|---------|
| SAR (Saudi Riyal) | ~50% | ر.س | `1,250 SAR` |
| EGP (Egyptian Pound) | ~25% | ج.م | `850 EGP` |
| AED (UAE Dirham) | ~20% | د.إ | `320 AED` |
| Other (KWD, BHD, QAR, JOD) | ~5–10% | — | `75 KWD` |

Within a single entity (one order, one affiliate row) the currency must be **consistent across all monetary fields** — never mix SAR and EGP on the same row.

## Name Distribution Targets

Per `research.md` §7:

- **~80% Arabic-script names**: e.g., أحمد الشمري، فاطمة البلوشي، محمد الغامدي
- **~20% Latin names**: e.g., Sara Hassan, Omar Khalil, Layla Nasser

Use realistic Gulf/Levant/Egyptian name patterns for authenticity.

---

## Canonical Sample Products (3)

| ID | Name (AR) | Type | Price | Currency | Status |
|----|-----------|------|-------|----------|--------|
| PRD-001 | سماعات بلوتوث لاسلكية | إلكترونيات | 890 | SAR | Active |
| PRD-002 | ساعة ذكية Smart Watch Pro | إلكترونيات | 920 | SAR | Active |
| PRD-003 | شاحن سريع Type-C 65W | إكسسوارات موبايل | 149 | AED | Active |

**Extended list for `/products/`** (feature 004 — DB-backed; seeded via `manage.py seed_products`) covers the 6 physical categories:
- إلكترونيات (electronics): e.g., سماعة بلوتوث ProBass X2, 750 EGP
- إكسسوارات موبايل (mobile accessories): e.g., شاحن سريع Type-C 65W, 149 AED
- أجهزة منزلية صغيرة (small appliances): e.g., قلاية هوائية 4 لتر, 1,800 EGP
- عناية شخصية (personal care): e.g., ماكينة حلاقة كهربائية, 899 EGP
- ملابس (clothing): e.g., تيشيرت قطن Basic Fit, 350 EGP
- أدوات منزلية (home tools): e.g., سجادة فاخرة, 550 SAR

---

## Canonical Sample Affiliates (3)

| ID | Name (AR) | Level | Code | Orders | Sales | Pending Comm. | Currency | Status |
|----|-----------|-------|------|--------|-------|---------------|----------|--------|
| AFF-001 | أحمد الشمري | Gold | AHMAD20 | 47 | 28,400 | 1,420 | SAR | Active |
| AFF-002 | سارة الخالدي | Silver | SARA15 | 23 | 9,800 | 490 | SAR | Active |
| AFF-003 | Omar Khalil | Bronze | OMAR10 | 8 | 2,950 | 295 | EGP | Pending |

**Extended list for affiliates.html** (10+ rows) should cover all 4 levels (Bronze/Silver/Gold/Platinum) and all 4 statuses (Pending/Active/Suspended/Rejected).

---

## Canonical Sample Customers (2)

| ID | Name (AR) | Phone | Source | Orders | Total Spent | Currency |
|----|-----------|-------|--------|--------|-------------|----------|
| CST-001 | فاطمة البلوشي | +966 50 123 4567 | Affiliate (AFF-001) | 5 | 3,450 | SAR |
| CST-002 | محمد الغامدي | +966 55 987 6543 | Direct | 2 | 1,100 | SAR |

**Extended list for customers.html** (15+ rows) should cover all 7 sources (Direct, Affiliate, WhatsApp, Facebook, Instagram, TikTok, Manual).

---

## Canonical Sample Orders (2)

| ID | Customer | Product | Affiliate | Total | Commission | Order Status | Payment | Shipping | Currency |
|----|----------|---------|-----------|-------|------------|-------------|---------|----------|----------|
| ORD-2024-0091 | CST-001 / فاطمة البلوشي | PRD-001 | AFF-001 / أحمد الشمري | 890 | 420 | Delivered | Paid | Delivered | SAR |
| ORD-2024-0092 | CST-002 / محمد الغامدي | PRD-002 | — | 920 | — | Confirmed | Unpaid | Preparing | SAR |

**Extended list for orders.html** (14+ rows) should cover all 6 order statuses, all 4 payment statuses, all 5 shipping statuses. Some rows must have an affiliate; some must show "—" for no affiliate.

---

## Cross-Page Consistency Rules

1. When PRD-001 appears on `product-detail.html`, the related-orders table MUST include ORD-2024-0091.
2. When AFF-001 appears on `affiliate-detail.html`, the attributed orders table MUST include ORD-2024-0091.
3. When CST-001 appears on `customer-detail.html`, the order history MUST include ORD-2024-0091.
4. The commission on ORD-2024-0091 (420 SAR) must appear in AFF-001's payout history on `affiliate-payouts.html`.
5. On `dashboard.html`, the "top affiliates" card must feature AFF-001 (أحمد الشمري).
6. On `dashboard.html`, the "recent orders" table must include ORD-2024-0091 and ORD-2024-0092.
