# Feature Specification: Affiliate Seller Portal — Static Frontend

**Feature Branch**: `002-affiliate-seller-portal`
**Created**: 2026-05-11
**Status**: Draft
**Input**: User description: "Design and implement the Affiliate Seller frontend pages for Smart Merchant OS. Static frontend prototype only. HTML, CSS, TailwindCSS, minimal vanilla JS. Arabic RTL, mobile-first, hardcoded data, no backend. The affiliate interface must feel like a fast selling app, not a complex admin dashboard. Required pages: affiliate-dashboard.html, affiliate-product-detail.html, affiliate-orders.html, affiliate-earnings.html, affiliate-saved-products.html, affiliate-profile.html."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Browse Catalogue and Grab Selling Assets (Priority: P1)

An affiliate marketer ("أحمد") opens the affiliate app, lands on a product-first
home screen, scans horizontal category tabs, taps a product card, opens the
product detail page, and copies the ready-made caption and product details so
they can immediately post and start selling — no setup, no admin complexity.

**Why this priority**: This is the entire product thesis stated in the brief —
"Login → choose category → pick product → copy assets/caption → start selling
immediately." If only this slice ships, the affiliate has a viable fast-selling
tool. Everything else (orders, earnings, profile) supports this loop.

**Independent Test**: Open `affiliate-dashboard.html` directly. Verify the first
mobile screen shows the welcome line, quick-earnings card, search bar, category
tabs, and product cards without scrolling past a dashboard chrome. Tap a
"عرض التفاصيل" button → land on `affiliate-product-detail.html`. On the detail
page, click "نسخ الكابشن" and "نسخ تفاصيل المنتج" → text is copied to clipboard
and a transient "تم النسخ" confirmation appears. Click the favorite icon → it
toggles its filled/outline state. Click a gallery thumbnail → the main image
switches.

**Acceptance Scenarios**:

1. **Given** the affiliate dashboard on a mobile viewport, **When** the page first renders, **Then** the welcome header ("أهلاً يا أحمد 👋" + "ابدأ بيع المنتجات الجاهزة واربح عمولتك فورًا"), the quick-earnings card, the "ابحث عن منتج للبيع..." search bar, the horizontal category tabs, and at least one product card are all visible within the first viewport-and-a-bit (no heavy admin chrome above them).
2. **Given** the dashboard, **When** the affiliate taps a category tab (الكل / الأكثر مبيعًا / عروض / إلكترونيات / ملابس / أدوات منزلية / إكسسوارات), **Then** the tapped tab becomes visually active (filled/underlined) and the other tabs become inactive — a visual-only state change, no data fetch.
3. **Given** the dashboard, **When** the affiliate scans the product sections, **Then** they see the sections "الأكثر مبيعًا", "عروض قوية اليوم", "منتجات جديدة", and "ربح عالي", each with a "عرض الكل" link and a row/grid of small product cards.
4. **Given** any product card, **When** the affiliate scans it, **Then** it shows ONLY: product image, an optional badge (Bestseller / New / Hot Offer), product name, suggested selling price, expected affiliate profit, a favorite icon, and a "عرض التفاصيل" button — no long description text.
5. **Given** a product card, **When** the affiliate clicks "عرض التفاصيل", **Then** they navigate to `affiliate-product-detail.html`.
6. **Given** the product detail page, **When** the affiliate clicks "نسخ الكابشن", **Then** the ready caption text is copied to the clipboard and a transient "تم النسخ" indicator appears; the same holds for "نسخ تفاصيل المنتج" and the product details box.
7. **Given** the product detail page, **When** the affiliate clicks a gallery thumbnail, **Then** the main product image switches to that image.
8. **Given** the product detail page, **When** the affiliate clicks the favorite icon, **Then** it toggles between an outline and a filled (saved) state.

---

### User Story 2 - Track My Orders (Priority: P2)

The affiliate wants to know the status of orders they generated — without seeing
full customer data — so they open the orders page, glance at summary counts,
optionally filter by status, and read each order's number, masked customer,
product, status, commission, and date.

**Why this priority**: Trust and motivation. An affiliate who can't see whether
their orders landed won't keep selling. It's second only to the core
browse-and-sell loop.

**Independent Test**: Open `affiliate-orders.html` directly. Verify four summary
cards (كل الطلبات / قيد التنفيذ / تم التسليم / ملغية) with realistic counts; a
search/filter bar; on mobile, orders rendered as cards (no wide table); on
desktop, orders rendered as a table. Each order shows order number, masked
customer name or masked phone, product name, a status badge (Pending /
Confirmed / Processing / Delivered / Cancelled), commission amount with
currency, and a date. Confirm no full customer phone or address is shown.

**Acceptance Scenarios**:

1. **Given** the orders page, **When** it renders, **Then** the affiliate sees four summary cards labeled كل الطلبات, قيد التنفيذ, تم التسليم, ملغية, each with a realistic count.
2. **Given** the orders page on a mobile viewport, **When** it renders, **Then** orders are shown as stacked cards, not a horizontally-scrolling table.
3. **Given** the orders page on a desktop viewport, **When** it renders, **Then** orders are shown as a table with columns for order number, customer, product, status, commission, date.
4. **Given** any order row/card, **When** the affiliate reads it, **Then** the customer is shown masked (e.g., "أحمد ا***" or "05•• ••• 234") — never a full name+phone+address — and the status is one of Pending, Confirmed, Processing, Delivered, Cancelled.
5. **Given** the orders page, **When** the affiliate uses the search/filter control, **Then** a filter affordance (status chips or a select) is present and visibly responds to interaction (active state); functional filtering is not required for the prototype.

---

### User Story 3 - Understand Earnings and Request a Payout (Priority: P2)

The affiliate wants to see how much they can withdraw, how much is still under
review, how much has been paid, understand the rule for when commission is
approved, review their earnings history, and submit a payout request.

**Why this priority**: Getting paid is the affiliate's ultimate goal. A clear,
honest earnings view plus a working payout request modal closes the loop on
motivation.

**Independent Test**: Open `affiliate-earnings.html` directly. Verify a
prominent main earnings card ("الأرباح المتاحة للسحب" + amount + "طلب سحب"
button); three secondary cards (إجمالي الأرباح / أرباح قيد المراجعة / أرباح
مدفوعة); the notice "يتم اعتماد العمولة بعد تأكيد الدفع أو تسليم الطلب."; an
earnings history list/table where each row shows product, order number,
commission, status (Pending / Approved / Paid / Rejected), and date. Click
"طلب سحب" → a modal opens with fields: amount, payment method, wallet/account
number, notes; ESC or a cancel/close control dismisses it.

**Acceptance Scenarios**:

1. **Given** the earnings page, **When** it renders, **Then** the affiliate sees a main card showing "الأرباح المتاحة للسحب" with an amount and currency and a "طلب سحب" button.
2. **Given** the earnings page, **When** it renders, **Then** the affiliate also sees three cards: إجمالي الأرباح, أرباح قيد المراجعة, أرباح مدفوعة, each with a realistic amount.
3. **Given** the earnings page, **When** the affiliate reads the page, **Then** the commission rule notice "يتم اعتماد العمولة بعد تأكيد الدفع أو تسليم الطلب." is visibly displayed.
4. **Given** the earnings history, **When** the affiliate scans it, **Then** each entry shows product, order number, commission amount, a status badge from {Pending, Approved, Paid, Rejected}, and a date.
5. **Given** the earnings page, **When** the affiliate clicks "طلب سحب", **Then** a payout request modal opens with input fields for amount, payment method, wallet/account number, and notes, plus confirm and cancel/close controls.
6. **Given** the payout modal is open, **When** the affiliate presses ESC or clicks the close/cancel control or the backdrop, **Then** the modal closes and focus returns to the page.

---

### User Story 4 - Saved Products Shortlist (Priority: P3)

The affiliate keeps a shortlist of products to sell later, so they open the
saved-products page, see their favorited products as the same cards used on the
dashboard, search within them, and — if they've saved nothing — see a friendly
empty state.

**Why this priority**: A convenience layer over the core loop. Valuable for
retention but not required to demonstrate the product.

**Independent Test**: Open `affiliate-saved-products.html` directly. Verify a
header, a search input, and a grid of product cards using the identical card
design from the dashboard. Confirm an empty-state block exists in the markup
(shown when the list is empty) with an illustration/icon, a message, and a CTA
back to browsing.

**Acceptance Scenarios**:

1. **Given** the saved-products page, **When** it renders with saved items, **Then** the affiliate sees a grid of product cards identical in design to the dashboard cards (image, optional badge, name, suggested price, expected profit, favorite icon, "عرض التفاصيل").
2. **Given** the saved-products page, **When** there are no saved products, **Then** an empty-state card is displayed with a message and a CTA linking to `affiliate-dashboard.html`.
3. **Given** the saved-products page, **When** the affiliate clicks a card's favorite icon, **Then** the icon toggles its filled/outline state (visual only).

---

### User Story 5 - Account, Level, and Referral Tools (Priority: P3)

The affiliate wants to see their account standing — affiliate level, referral
link, coupon code, payment method, account status — and copy their referral link
and coupon to share.

**Why this priority**: Identity and sharing tools. Important for a complete
affiliate experience, but the selling loop works without it.

**Independent Test**: Open `affiliate-profile.html` directly. Verify a profile
card; an affiliate level badge (one of Bronze / Silver / Gold / Platinum); a
referral link box with a copy button; a QR code placeholder; a coupon code with
a copy button; a basic info form; payment method info; an account status
indicator. Click the referral-link copy button and the coupon copy button → each
copies to the clipboard with a transient "تم النسخ" confirmation. If a theme
toggle exists in the shared layout, it works here too.

**Acceptance Scenarios**:

1. **Given** the profile page, **When** it renders, **Then** the affiliate sees a profile card with their name, avatar, and an affiliate level badge labeled one of Bronze, Silver, Gold, or Platinum.
2. **Given** the profile page, **When** the affiliate clicks the referral-link copy button, **Then** the referral link is copied to the clipboard and a transient "تم النسخ" indicator appears.
3. **Given** the profile page, **When** the affiliate clicks the coupon-code copy button, **Then** the coupon code is copied to the clipboard and a transient "تم النسخ" indicator appears.
4. **Given** the profile page, **When** it renders, **Then** a QR code placeholder, a basic info form (name, email, phone, etc.), payment method info, and an account status indicator are all present.
5. **Given** the profile page, **When** the affiliate triggers the payout modal entry point (if surfaced here) or the theme toggle (if present in the shared layout), **Then** the modal opens/closes and the theme toggle switches dark/light — consistent with the rest of the prototype.

---

### Edge Cases

- **Empty saved products**: the saved-products page must render a deliberate empty state, not a blank area.
- **Long product names**: product cards must truncate (ellipsis) rather than break the small-card grid layout.
- **No badge applicable**: a product card with no badge must still align cleanly with badged cards in the same row.
- **Cancelled / Rejected states**: orders with status Cancelled and earnings with status Rejected must use a clearly distinct (e.g., red/muted) badge so they aren't mistaken for active items.
- **Clipboard unavailable**: if the browser blocks clipboard access, the copy buttons must fail gracefully (e.g., select the text / show a non-blocking hint) rather than throw a visible error.
- **Mobile bottom navigation overlap**: page content must have enough bottom padding that the fixed bottom navigation never covers the last row of content or a primary button.
- **Desktop sidebar present**: on large screens the optional desktop sidebar must not double up with the mobile bottom navigation (bottom nav hidden on desktop, sidebar hidden on mobile).
- **Direct page entry**: every affiliate page must look complete when opened directly (no "select a product first" dead ends) — the product detail page shows a fully populated representative product.

## Requirements *(mandatory)*

### Functional Requirements

#### Shared affiliate layout

- **FR-001**: The system MUST provide a lightweight affiliate layout, visually distinct from the merchant admin dashboard shell, applied consistently across all six affiliate pages.
- **FR-002**: The affiliate layout MUST include a top header showing the affiliate's name, a quick-earnings indicator (available balance), a search bar, a notification icon, and a profile avatar.
- **FR-003**: The affiliate layout MUST include a fixed mobile bottom navigation with exactly these items in order: الرئيسية, المنتجات, المحفوظات, الطلبات, الأرباح — each linking to its corresponding affiliate page, with the current page's item shown in an active state.
- **FR-004**: On large (desktop) viewports the affiliate layout MAY render a simple sidebar with the same navigation entries; when shown, the mobile bottom navigation MUST be hidden, and vice versa.
- **FR-005**: The affiliate layout MUST default to RTL direction with Arabic labels and copy; English MAY appear only for technical status tokens (Pending, Confirmed, Processing, Delivered, Cancelled, Approved, Paid, Rejected) and level names (Bronze, Silver, Gold, Platinum) where convention favors them.
- **FR-006**: The affiliate layout MUST be mobile-first and responsive across mobile, tablet, and desktop breakpoints; the first mobile screen MUST surface search, category tabs, and product cards quickly, without heavy admin chrome pushing them below the fold.
- **FR-007**: The visual style MUST be minimal, premium, clean, and uncluttered: soft cards, rounded corners, a predominantly white background with subtle gradients, clear product previews, and no heavy dashboard complexity.
- **FR-008**: If the existing prototype provides a dark/light theme toggle, the affiliate layout MUST honor it; theme preference MAY be persisted only via the existing mechanism (no other client-side storage).

#### Affiliate Dashboard (`affiliate-dashboard.html`)

- **FR-010**: The dashboard MUST show a welcome header with the lines "أهلاً يا أحمد 👋" and "ابدأ بيع المنتجات الجاهزة واربح عمولتك فورًا".
- **FR-011**: The dashboard MUST show a quick-earnings card surfacing: الأرباح المتاحة, الطلبات الناجحة, المنتجات المحفوظة — each with a realistic value.
- **FR-012**: The dashboard MUST show a search bar with the placeholder "ابحث عن منتج للبيع...".
- **FR-013**: The dashboard MUST show horizontal, scrollable category tabs with exactly: الكل, الأكثر مبيعًا, عروض, إلكترونيات, ملابس, أدوات منزلية, إكسسوارات; tapping a tab MUST update the active visual state.
- **FR-014**: The dashboard MUST show product sections titled "الأكثر مبيعًا", "عروض قوية اليوم", "منتجات جديدة", and "ربح عالي", each with a "عرض الكل" link and a row/grid of product cards.
- **FR-015**: Each product card MUST contain ONLY: product image (with `alt`), an optional badge from {Bestseller, New, Hot Offer}, product name, suggested selling price, expected affiliate profit, a favorite icon, and a "عرض التفاصيل" button — and MUST NOT contain a long product description.
- **FR-016**: The favorite icon on a product card MUST toggle its visual saved/unsaved state on click.
- **FR-017**: The "عرض التفاصيل" button on a product card MUST link to `affiliate-product-detail.html`.

#### Affiliate Product Detail (`affiliate-product-detail.html`)

- **FR-020**: The product detail page MUST include a product image gallery with a main image and selectable thumbnails; clicking a thumbnail MUST switch the main image.
- **FR-021**: The product detail page MUST include a video preview placeholder.
- **FR-022**: The product detail page MUST display the product name, its badges, and a short description.
- **FR-023**: The product detail page MUST include a sales/pricing card showing سعر المورد, سعر البيع المقترح, and صافي ربحك — with consistent currency within the card.
- **FR-024**: The product detail page MUST include quick action buttons: تحميل الصور, تحميل الفيديوهات, نسخ الكابشن, نسخ تفاصيل المنتج, مشاركة واتساب, طلب أوردر.
- **FR-025**: The product detail page MUST include a ready caption box with a copy button; clicking it MUST copy the caption text to the clipboard and show a transient "تم النسخ" indicator.
- **FR-026**: The product detail page MUST include a product details box with a copy button; clicking it MUST copy the details text to the clipboard and show a transient "تم النسخ" indicator.
- **FR-027**: The product detail page MUST include a suggested-selling-tips section and a related-products section (related products reuse the dashboard product-card design).
- **FR-028**: The product detail page MUST include a favorite toggle for the current product.
- **FR-029**: If a product detail modal is used, it MUST open and dismiss (close control, backdrop click, and ESC).

#### Affiliate Orders (`affiliate-orders.html`)

- **FR-030**: The orders page MUST show four summary cards: كل الطلبات, قيد التنفيذ, تم التسليم, ملغية — each with a realistic count.
- **FR-031**: The orders page MUST include a search/filter bar with a visible, interactive filter affordance (status chips or a select); functional filtering is not required.
- **FR-032**: The orders page MUST render orders as stacked cards on mobile viewports and as a table on desktop viewports.
- **FR-033**: Each order MUST display: order number, customer name OR masked phone (masked, never full), product name, an order status badge from {Pending, Confirmed, Processing, Delivered, Cancelled}, a commission amount with currency, and a date.
- **FR-034**: The orders page MUST NOT display full sensitive customer data (no full phone numbers, no addresses, no emails); customer identity MUST be partially masked.
- **FR-035**: Cancelled orders MUST use a visually distinct (warning/muted) badge style versus active statuses.

#### Affiliate Earnings (`affiliate-earnings.html`)

- **FR-040**: The earnings page MUST show a prominent main earnings card with "الأرباح المتاحة للسحب", an amount with currency, and a "طلب سحب" button.
- **FR-041**: The earnings page MUST show three secondary cards: إجمالي الأرباح, أرباح قيد المراجعة, أرباح مدفوعة — each with a realistic amount.
- **FR-042**: The earnings page MUST display the notice "يتم اعتماد العمولة بعد تأكيد الدفع أو تسليم الطلب." visibly.
- **FR-043**: The earnings page MUST include an earnings history list/table where each row shows: product, order number, commission amount, a status badge from {Pending, Approved, Paid, Rejected}, and a date.
- **FR-044**: Clicking "طلب سحب" MUST open a payout request modal with input fields for: amount, payment method, wallet/account number, and notes — plus confirm and cancel/close controls.
- **FR-045**: The payout modal MUST be dismissable via ESC, a close/cancel control, and a backdrop click; on dismiss, focus returns to the page.
- **FR-046**: Rejected earnings MUST use a visually distinct (warning/muted) badge style versus Pending/Approved/Paid.

#### Affiliate Saved Products (`affiliate-saved-products.html`)

- **FR-050**: The saved-products page MUST include a header, a search input, and a grid of product cards using the identical card design from the dashboard.
- **FR-051**: The saved-products page MUST include an empty-state card (markup present) with an icon/illustration, a message, and a CTA linking to `affiliate-dashboard.html`, shown when there are no saved products.
- **FR-052**: The favorite icon on saved-product cards MUST toggle its visual state on click.

#### Affiliate Profile (`affiliate-profile.html`)

- **FR-060**: The profile page MUST include a profile card (name, avatar) and an affiliate level badge labeled one of Bronze, Silver, Gold, Platinum.
- **FR-061**: The profile page MUST include a referral link box with a copy button; clicking it copies the link to the clipboard with a transient "تم النسخ" indicator.
- **FR-062**: The profile page MUST include a QR code placeholder.
- **FR-063**: The profile page MUST include a coupon code with a copy button; clicking it copies the code to the clipboard with a transient "تم النسخ" indicator.
- **FR-064**: The profile page MUST include a basic info form (e.g., name, email, phone), payment method info, and an account status indicator.
- **FR-065**: The profile page MUST honor the shared layout's theme toggle (if present), mobile nav active state, payout modal (if surfaced here), and favorite toggle behavior — consistent with the rest of the prototype.

#### Cross-cutting

- **FR-070**: All page data MUST be hardcoded in the HTML; the prototype MUST NOT make API calls, fetch remote data, or contain backend logic, and MUST open directly in a browser or via Live Server with no bundler or dev server.
- **FR-071**: Vanilla JavaScript usage MUST be limited to: copy-to-clipboard (caption, product details, referral link, coupon), favorite toggle, image gallery switching, category tab active state, mobile bottom-nav active state, modal open/close (payout and optional product modal), and the existing theme toggle. SPA routing, API simulation, and complex state management are FORBIDDEN.
- **FR-072**: Every navigation link in the affiliate layout (bottom nav, desktop sidebar, header, in-page CTAs, "عرض التفاصيل", "عرض الكل", empty-state CTA) MUST resolve to an existing file; no dead links.
- **FR-073**: Every image MUST have an `alt` attribute; interactive elements MUST have visible focus styles and a logical tab order; modals and any drawer MUST be ESC-dismissable.
- **FR-074**: Sample data (affiliate name, product names, prices, commissions, order numbers, dates) MUST be realistic and follow the project's existing conventions for currency mix (SAR-majority, with EGP/AED and occasional other regional currencies; consistent currency within a single row/entity) and name mix (~80% Arabic-script, ~20% Latin-script). The primary affiliate persona is "أحمد".
- **FR-075**: The affiliate pages MUST be reachable via a documented entry point in the existing prototype (e.g., a role selector on the login page or a link from the merchant affiliates view) so the affiliate portal is discoverable; the merchant dashboard's existing affiliate-related pages remain unchanged.

### Key Entities *(include if feature involves data)*

- **Affiliate (current user)**: name (e.g., "أحمد"), avatar, affiliate level (Bronze | Silver | Gold | Platinum), referral link, coupon code, account status, payment method info, contact info; aggregate figures: available balance, total earnings, under-review earnings, paid earnings, successful orders count, saved products count.
- **Product (sellable item)**: id, name, image gallery (multiple images), optional video preview, optional badge (Bestseller | New | Hot Offer), category (الأكثر مبيعًا/عروض/إلكترونيات/ملابس/أدوات منزلية/إكسسوارات), short description, supplier price (سعر المورد), suggested selling price (سعر البيع المقترح), affiliate net profit (صافي ربحك), ready caption text, ready product-details text, suggested selling tips, related product ids, currency, saved/favorite flag.
- **Affiliate Order**: order number, masked customer name or masked phone, product name, order status (Pending | Confirmed | Processing | Delivered | Cancelled), commission amount, currency, date. Belongs to the current affiliate only.
- **Earning / Commission record**: product, order number, commission amount, currency, status (Pending | Approved | Paid | Rejected), date.
- **Payout request (transient, modal only)**: amount, payment method, wallet/account number, notes. Not persisted — the modal is a visual affordance.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: From opening `affiliate-dashboard.html`, a new affiliate can reach a product's selling assets and copy a caption in at most 3 taps (dashboard → product card "عرض التفاصيل" → "نسخ الكابشن").
- **SC-002**: On a 375px-wide viewport, the welcome header, quick-earnings card, search bar, category tabs, and at least one full product card are all visible within the first 1.25 screen heights — i.e., the affiliate is browsing products almost immediately, not scrolling through dashboard widgets.
- **SC-003**: All six affiliate pages (`affiliate-dashboard.html`, `affiliate-product-detail.html`, `affiliate-orders.html`, `affiliate-earnings.html`, `affiliate-saved-products.html`, `affiliate-profile.html`) exist, render complete with realistic hardcoded data, and contain zero dead navigation links.
- **SC-004**: Every interactive behavior in scope works on first click in a modern browser: copy caption, copy product details, copy referral link, copy coupon (each with a visible "تم النسخ" confirmation), favorite toggle, gallery thumbnail switch, category-tab active state, bottom-nav active state, and payout modal open/close (including ESC and backdrop).
- **SC-005**: On any affiliate page at mobile width, no order, earning, or other primary data list is presented in a horizontally-scrolling table; such data is presented as cards.
- **SC-006**: No affiliate orders or earnings view exposes a full customer phone number, full address, or email; customer identity is always at least partially masked.
- **SC-007**: A first-time reviewer, shown the affiliate dashboard next to a typical reseller/affiliate platform, rates it as cleaner, more premium, and faster to use — concretely: no more than the specified fields per product card, no admin-style data grids on the home screen, and a single clear primary action ("عرض التفاصيل") per product.
- **SC-008**: The prototype opens and runs correctly by double-clicking the HTML files or via Live Server, with no build step, no dev server, and no network requests for application data.

## Assumptions

- **Distinct layout vs. constitution shell**: Constitution Principle VI describes the *merchant* dashboard shell (fixed sidebar with Dashboard/Products/Orders/... entries). The brief explicitly asks for a *lightweight affiliate layout that is different from the merchant admin dashboard*; this spec treats the affiliate portal as a separate surface with its own shell (top header + mobile bottom nav + optional simple desktop sidebar) and does not change the merchant shell. This is an intentional, user-requested addition, not a violation.
- **Reuse of existing assets**: The affiliate pages reuse the existing prototype's TailwindCSS setup, icon system (Lucide via CDN), placeholder images (`assets/img/placeholders/*`, including `affiliate-avatar.svg`, `product.svg`, `qr-code.svg`), `assets/css/app.css`, and the `assets/js/main.js` patterns where applicable; new affiliate-specific JS hooks are added in the same minimal-vanilla style.
- **Single persona**: The portal is presented from one logged-in affiliate's perspective ("أحمد", Gold level by default, consistent with `AFF-001` in the existing sample data) — no login flow, no account switching.
- **No real downloads/sharing**: "تحميل الصور / تحميل الفيديوهات / مشاركة واتساب / طلب أوردر" are visual affordances; they may link to placeholders or no-op with a hint. They are not required to perform real file downloads or open WhatsApp, though a `wa.me` link or a `download` attribute on a placeholder asset is acceptable.
- **Filtering is visual**: Category tabs, order status filters, and search inputs are visual controls with active/hover states; live client-side filtering of the hardcoded lists is allowed but not required.
- **Currency & names**: Follow the existing `SAMPLE-DATA.md` conventions (SAR-majority currency mix, ~80% Arabic-script names), with prices/commissions consistent within each row/entity.
- **Empty state is demonstrable**: The saved-products empty state is included in markup and styled so reviewers can see it without code edits (e.g., a visible "empty" variant or a documented toggle); at minimum the markup exists.
- **Entry point**: A link to `affiliate-dashboard.html` is added somewhere discoverable in the existing prototype (e.g., the login page role selector, or the merchant affiliates page); exact placement is decided in the implementation plan.
