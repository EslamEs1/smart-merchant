# Feature Specification: Smart Merchant OS — Static Frontend MVP

**Feature Branch**: `001-static-frontend-mvp`
**Created**: 2026-05-10
**Status**: Draft
**Input**: User description: "Build a static frontend MVP for Smart Merchant OS — a premium merchant operating system with public marketing pages, merchant dashboard, products, orders, affiliates, commissions, customers CRM, and simple landing pages. RTL Arabic, no frameworks, client-presentable prototype."

## Clarifications

### Session 2026-05-10

- Q: Which currency should sample data use across prices, totals, commissions, and balances? → A: Multi-currency — sample rows distribute across SAR, EGP, AED, and one or two additional regional currencies to demonstrate the platform's localization range; each numeric cell carries an explicit currency token (e.g., `1,250 SAR`, `350 EGP`, `90 AED`); within a single entity (e.g., one order's total + commission), the currency is consistent.
- Q: What language should sample person/business names use in tables and detail pages? → A: Mostly Arabic (~80%) with ~20% Latin-script for variety — applies to customer names, affiliate names, merchant business names, testimonial author names, and notification author names; Latin-script samples are intentional realism (e.g., walk-in customers from Direct/Manual sources, English-named brands).
- Q: Which icon system should be used across sidebar, header, status badges, and action dropdowns? → A: Lucide via CDN — single `<script src="…lucide…">` tag, `<i data-lucide="<name>"></i>` placeholder syntax that the script auto-swaps into inline SVG. No bundler, no icon font.
- Q: What accessibility scope should the prototype target? → A: Visual + keyboard basics — visible focus rings on all interactive elements, logical tab order, ESC dismissal on modals and the mobile drawer, `alt` attributes on every image (placeholder or real), and AA-equivalent color contrast (≥4.5:1 for body text, ≥3:1 for large text and UI components). No formal WCAG audit, no ARIA-rich landmarks, no screen-reader certification.
- Q: How should the "Smart Merchant OS" brand be represented? → A: Bilingual wordmark + abstract glyph — wordmark "Smart Merchant OS" / "سمارت مرتشانت" in a bilingual lockup paired with an inline-SVG abstract geometric glyph (e.g., stacked-cube or circuit-node mark) rendered in a purple/blue gradient. The glyph appears in the sidebar header, marketing site nav, login/register brand panel, footer, and favicon. Both Arabic and English wordmarks are visible together where space allows; in tight spaces (favicon, mobile sidebar collapsed), only the glyph appears.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Affiliate-Centric Merchant Demo (Priority: P1)

A merchant evaluating Smart Merchant OS opens the prototype and walks through the
affiliate workflow end-to-end: they see the affiliate roster, review pending
applications, approve a marketer, open an affiliate's profile to inspect their
referral link, QR code, coupon, sales, and commission balances, then visit the
payouts queue and trigger a payout action.

**Why this priority**: The affiliate system is the project's stated core
differentiator (Constitution Principle V). Without it the prototype is just
another generic admin dashboard. Demoing this story alone proves the product
thesis.

**Independent Test**: Open `affiliates.html`, `affiliate-detail.html`,
`affiliate-requests.html`, and `affiliate-payouts.html` directly. Verify each
page renders complete with realistic data, the referral-link copy box copies
to clipboard, action dropdowns open, approve/suspend/pay confirmation modals
open and dismiss, and navigation between the four pages works.

**Acceptance Scenarios**:

1. **Given** a merchant on the Affiliates List, **When** they open any row's actions dropdown, **Then** they see actions: View profile, Approve, Suspend, Change level, View orders, Pay commission, Copy referral link.
2. **Given** a merchant on the Affiliate Detail page, **When** they click the Copy Referral Link button, **Then** the link is copied to the clipboard and a transient "Copied" indicator appears.
3. **Given** a merchant on the Affiliate Requests page, **When** they click Approve on a pending application, **Then** a confirmation modal appears with affiliate name and a confirm/cancel pair.
4. **Given** a merchant on the Affiliate Payouts page, **When** they switch tabs between Pending / Paid / Rejected, **Then** the table content swaps to show realistic rows for that tab without a page reload.
5. **Given** any affiliate-system page, **When** the merchant scans the layout, **Then** the commission rule "يتم اعتماد العمولة بعد وصول الطلب إلى Delivered أو تأكيد الدفع." is visibly displayed in context.

---

### User Story 2 - Merchant Dashboard Overview (Priority: P1)

The merchant lands on the dashboard after login and immediately understands their
business performance: total sales, order count, customer count, affiliate count,
pending commissions, and new orders, plus visualizations of sales over time and
orders by status, plus the latest activity (recent orders, top affiliates, top
products, pending affiliate requests).

**Why this priority**: The dashboard is the home page of the product. A
prospective customer's first impression is formed here; if the dashboard
looks empty or generic, the entire prototype fails its client-demo purpose.

**Independent Test**: Open `dashboard.html` directly. Verify all six stat
cards display realistic numbers, both chart placeholders are present and
visually distinct, the recent orders table contains realistic rows with
status badges, top affiliates and top products cards each show at least
three entries, the pending affiliate requests card shows a queue with a
review action, and all four quick-action buttons link to the correct pages.

**Acceptance Scenarios**:

1. **Given** the dashboard is open, **When** the merchant scans the top of the page, **Then** they see six stat cards labeled in Arabic for total sales, orders, customers, affiliates, pending commissions, and new orders, each with a placeholder value and trend indicator.
2. **Given** the dashboard is open, **When** the merchant scans the middle, **Then** they see two chart placeholders (sales overview and orders by status) presented as visually rich graphics, not empty boxes.
3. **Given** the dashboard is open, **When** the merchant clicks any quick action ("Add product", "Create order", "Review affiliates", "Create landing page"), **Then** they navigate to the matching page (`product-create.html`, `orders.html`, `affiliate-requests.html`, `landing-page-create.html`).
4. **Given** the dashboard is open, **When** the merchant uses the date-range selector UI, **Then** the selector opens a date-range picker UI affordance (no functional filtering required, only the visual control).

---

### User Story 3 - Products & Services Management (Priority: P1)

The merchant manages their catalogue: physical products, services, courses,
digital products, and subscriptions. They browse the catalogue list, filter by
type and status, open a product detail to see sales summary and which affiliates
moved the most units, then create a new product or edit an existing one through
a structured form.

**Why this priority**: Without a product catalogue, none of the orders,
affiliate, or commission flows have any anchoring entity to talk about.
Products are the seed data that makes every other module believable.

**Independent Test**: Open `products.html`, `product-create.html`,
`product-edit.html`, and `product-detail.html`. Verify the list shows rows
for each of the five product types (منتج فعلي، خدمة، كورس، ديجيتال برودكت،
اشتراك), the search input and type/status filters are present, every row's
actions dropdown opens with the seven required actions, and the create/edit
forms render every required field.

**Acceptance Scenarios**:

1. **Given** the products list, **When** the merchant scans the table, **Then** every row shows: product image, product name, type badge, price, discount, stock, status badge, sales count, and an actions dropdown.
2. **Given** the products list, **When** the merchant opens a row's actions dropdown, **Then** they see: View details, Edit, Copy public link, Duplicate, Disable, Delete.
3. **Given** the product create page, **When** the merchant scans the form, **Then** they see fields for name, type, description, price, discount price, stock, status, images placeholder, video URL, SEO title, SEO description, public URL slug, plus Save and Cancel buttons.
4. **Given** the product detail page, **When** the merchant scans the page, **Then** they see a product summary card, an image gallery placeholder, price and stock, status, public link, sales summary, related orders table, top-affiliates-who-sold-this-product list, and an activity timeline.
5. **Given** the products list, **When** the merchant clicks Delete in any row's dropdown, **Then** a confirmation modal opens with a destructive-action style and confirm/cancel actions.

---

### User Story 4 - Orders Management with Attribution (Priority: P2)

The merchant tracks orders through their lifecycle and reviews how each order
attributes to a customer, a product, and (when applicable) an affiliate. They
filter by order status, payment status, and affiliate; open an individual order
to see the full timeline including invoice preview; and edit attribution or
status on an existing order.

**Why this priority**: Orders are the connective tissue between products,
customers, and affiliates. Demonstrating attribution proves the affiliate
commission model works end-to-end. Comes after P1 because it depends on
products and affiliates being already representable.

**Independent Test**: Open `orders.html`, `order-detail.html`, `order-edit.html`.
Verify the orders list table includes affiliate-attributed rows and
non-attributed rows side by side, all three status badge families render
correctly (order/payment/shipping), filter UI for status/payment/affiliate/date
is visible, and the order detail shows the full attribution chain plus an
invoice preview card.

**Acceptance Scenarios**:

1. **Given** the orders list, **When** the merchant scans the table, **Then** every row shows: order number, customer, product, affiliate (or a "—" indicator if none), total, commission, order status, payment status, shipping status, date, and an actions dropdown.
2. **Given** the orders list, **When** the merchant opens an actions dropdown, **Then** they see: View details, Edit order, Confirm order, Mark as shipped, Mark as delivered, Cancel order, Print invoice.
3. **Given** the order detail page, **When** the merchant scans it, **Then** they see order summary, customer info, product info, affiliate attribution, commission info, payment status, shipping status, a chronological timeline, notes, and an invoice preview card.
4. **Given** the order edit page, **When** the merchant scans the form, **Then** they see editable fields for order status, payment status, shipping status, customer info, notes, affiliate attribution, and commission amount.
5. **Given** the orders list, **When** the merchant uses the affiliate filter, **Then** the filter UI exposes the list of affiliates and is keyboard-dismissable.

---

### User Story 5 - Customers CRM (Priority: P2)

The merchant maintains a CRM-like view of their customers, including how the
customer was acquired (direct, affiliate, or one of the social-media channels)
and the affiliate who referred them when applicable. They review per-customer
order history, lifetime spend, tags, and notes, and edit a customer's profile
and follow-up date.

**Why this priority**: Customer attribution closes the loop on the affiliate
story (which affiliate brought which customer). Important but secondary to
the dashboard/products/affiliate triple.

**Independent Test**: Open `customers.html`, `customer-detail.html`,
`customer-edit.html`. Verify the customer list shows rows tagged across all
seven sources (Direct, Affiliate, WhatsApp, Facebook, Instagram, TikTok,
Manual), the source filter exposes all seven values, customer detail shows
full order history and timeline, and the edit form has every required field.

**Acceptance Scenarios**:

1. **Given** the customers list, **When** the merchant scans the table, **Then** every row shows: name, phone/email, source, affiliate (or "—"), orders count, total spent, last order date, tags, and an actions dropdown.
2. **Given** the customers list, **When** the merchant opens the source filter, **Then** they see the seven sources: Direct, Affiliate, WhatsApp, Facebook, Instagram, TikTok, Manual.
3. **Given** the customer detail page, **When** the merchant scans it, **Then** they see profile card, contact info, source, affiliate attribution if any, order history, total spent, notes, tags, follow-up status, and a timeline.
4. **Given** the customer edit page, **When** the merchant scans the form, **Then** they see editable fields for name, phone, email, address, source, tags, notes, and follow-up date.

---

### User Story 6 - Public Marketing Website (Priority: P3)

A prospective merchant arrives at the marketing site, understands what Smart
Merchant OS does, sees pricing and feature details, and lands on the auth
flow.

**Why this priority**: Marketing pages are necessary for a credible
client-demo handoff but they don't prove the dashboard's value. They can
ship after the dashboard core is solid.

**Independent Test**: Open `index.html`, `features.html`, `pricing.html`,
`login.html`, `register.html`. Verify the home page contains every required
section (hero with primary/secondary CTA, dashboard preview mockup,
affiliate-growth section, products/orders/customers section, commissions/
payouts section, features grid, pricing teaser, testimonials, FAQ, footer),
the features page explains all ten listed features, the pricing page shows
three plans, and login/register render with the brand-panel split layout.

**Acceptance Scenarios**:

1. **Given** the home page, **When** the merchant scans it, **Then** they see the hero with primary CTA "ابدأ إدارة تجارتك بذكاء" and secondary CTA "شاهد لوحة التحكم".
2. **Given** the home page, **When** the merchant scrolls through, **Then** they encounter, in order, sections explaining: dashboard preview, affiliate growth, products/orders/customers, commissions/payouts, features grid, pricing teaser, testimonials, FAQ, footer.
3. **Given** the pricing page, **When** the merchant compares plans, **Then** they see exactly three plans (Starter, Growth, Pro) and each card shows monthly price, products limit, affiliates limit, orders limit, included features, and a CTA button.
4. **Given** the features page, **When** the merchant scans it, **Then** they see distinct, illustrated explanations for: dashboard, products, orders, customers CRM, affiliate system, referral links, QR codes, commissions, landing pages, reports.
5. **Given** the login or register page, **When** the merchant scans it, **Then** they see a brand panel on one side and a form card with email/phone field, password field, remember-me toggle, primary action button, and a link to switch between login and register.

---

### User Story 7 - Simple Landing Pages Module (Priority: P3)

The merchant creates a static-UI landing page for a product or offer, fills in
a form-driven editor (no drag-and-drop), and previews the resulting public
landing page.

**Why this priority**: Landing pages widen the prototype's surface area and
demonstrate the product's depth, but the affiliate/order/customer triangle
already proves the core value. P3 is appropriate.

**Independent Test**: Open `landing-pages.html`, `landing-page-create.html`,
`landing-page-preview.html`. Verify the list shows realistic conversion
metrics, the create page presents form-based editing with template
selection, and the preview page renders a complete public-facing landing
page (hero, image, benefits, offer, CTA, testimonials, FAQ, footer).

**Acceptance Scenarios**:

1. **Given** the landing pages list, **When** the merchant scans the table, **Then** every row shows: title, linked product, status, visits, conversion rate, orders, revenue, last updated, and an actions dropdown.
2. **Given** the landing pages list, **When** the merchant opens an actions dropdown, **Then** they see: Preview, Edit, Copy link, Duplicate, Disable, Delete.
3. **Given** the create page, **When** the merchant scans the form, **Then** they see fields for title, product selector, template selection cards, hero headline, subheadline, CTA text, offer price, benefits list, testimonials placeholder, FAQ placeholder, SEO title, SEO description, plus Save and Preview actions.
4. **Given** the preview page, **When** the merchant scans the rendered preview, **Then** they see a complete public-facing layout with hero, product image, benefits, offer, CTA, testimonials, FAQ, and footer.

---

### User Story 8 - Settings, Profile & Notifications (Priority: P3)

The merchant adjusts their business settings, edits their profile, and reviews
the notifications inbox.

**Why this priority**: Settings/profile/notifications round out the
prototype's completeness but rarely drive demo decisions. Lowest priority
of the dashboard modules.

**Independent Test**: Open `settings.html`, `profile.html`,
`notifications.html`. Verify settings includes all six tabbed sections,
profile shows the four required fields plus avatar placeholder, and
notifications shows entries spanning all five notification categories.

**Acceptance Scenarios**:

1. **Given** the settings page, **When** the merchant scans the tabs/sections, **Then** they see: Business info, Branding, Payment settings, Affiliate commission settings, Notification settings, Security.
2. **Given** the profile page, **When** the merchant scans the form, **Then** they see fields for name, email, phone, password change placeholder, and an avatar placeholder.
3. **Given** the notifications page, **When** the merchant scans the inbox, **Then** they see entries spanning new orders, affiliate requests, payout requests, low stock alerts, and payment updates.

---

### Edge Cases

- **Empty states**: Each list page MUST show at least one realistic non-empty data row in the prototype, but the markup MAY also include a hidden empty-state card pattern that could replace the table when zero rows are present.
- **RTL alignment of action dropdowns**: Action dropdowns on tables MUST open toward the start (right) of the page in RTL and MUST NOT clip off-screen on the last row.
- **Mobile sidebar trapping**: Opening the mobile sidebar drawer MUST dim the page background and MUST be dismissable by tapping the dim overlay or pressing Escape.
- **Theme toggle persistence**: Toggling dark/light mode on one page MUST persist when navigating to another page (the only allowed `localStorage` use per Constitution Principle VII).
- **Confirmation modals on destructive actions**: Delete, Cancel order, Suspend affiliate, Reject affiliate, and Pay commission actions MUST each open a confirmation modal before completing the visual action; the modal MUST be dismissable via Cancel button, ESC key, or clicking the overlay.
- **Affiliate without sales**: The affiliate detail page MUST gracefully render an affiliate whose orders, sales, and commissions are all zero — without breaking layout or showing "NaN" / blank stat cards.
- **Order without affiliate**: Order rows and order detail MUST visually represent the "no affiliate" case (e.g., an explicit "—" or "بدون مسوّق" indicator) rather than blank cells.
- **Long Arabic content**: Long product names, affiliate names, and customer names MUST truncate gracefully in tables (ellipsis on overflow) and expand fully on detail pages.
- **Image placeholders**: Every required image (product images, avatar, QR code, dashboard preview) MUST use a styled placeholder graphic — never a broken-image icon.

## Requirements *(mandatory)*

### Functional Requirements

#### Public Marketing Pages

- **FR-001**: System MUST provide a `index.html` home page containing all sections listed in User Story 6 acceptance scenarios in the documented order.
- **FR-002**: System MUST provide a `features.html` page that visually explains the ten features (dashboard, products, orders, customers CRM, affiliate system, referral links, QR codes, commissions, landing pages, reports), each with its own card or section.
- **FR-003**: System MUST provide a `pricing.html` page with exactly three plans (Starter, Growth, Pro), each card showing monthly price placeholder, products limit, affiliates limit, orders limit, feature list, and CTA button.
- **FR-004**: System MUST provide `login.html` and `register.html` pages using a brand-panel-plus-form-card split layout, each with the documented form fields and a cross-link to the other page.

#### Shared Dashboard Shell

- **FR-005**: All dashboard pages MUST share the same visual shell: fixed/desktop sidebar, mobile sidebar drawer, top header with search input, notifications icon, merchant profile menu, main content area, and breadcrumbs where useful.
- **FR-006**: The sidebar MUST contain the following entries in this order, each linking to an existing page: Dashboard, Products / Services, Orders, Customers, Affiliates, Payouts, Landing Pages, Analytics, Settings.
- **FR-007**: The mobile sidebar drawer MUST open via a hamburger button in the header and dismiss via overlay tap or ESC.

#### Dashboard

- **FR-008**: System MUST provide `dashboard.html` containing: welcome header, date range selector UI, six stat cards (إجمالي المبيعات، عدد الطلبات، عدد العملاء، عدد المسوقين، العمولات المستحقة، الطلبات الجديدة), two chart placeholders (sales overview, orders by status), recent orders table, top affiliates card, top products card, pending affiliate requests card, and four quick-action buttons (Add product, Create order, Review affiliates, Create landing page) each linking to the relevant page.

#### Products

- **FR-009**: System MUST provide `products.html` with a search input, type filter, status filter, "Add product" button, and a data table whose rows show: image, name, type badge, price, discount, stock, status badge, sales count, and an actions dropdown.
- **FR-010**: Each products list row's actions dropdown MUST expose: View details, Edit, Copy public link, Duplicate, Disable, Delete.
- **FR-011**: System MUST provide `product-create.html` and `product-edit.html` whose forms include: name, type, description, price, discount price, stock, status, images placeholder, video URL, SEO title, SEO description, public URL slug, plus Save and Cancel buttons.
- **FR-012**: System MUST provide `product-detail.html` containing: product summary card, image gallery placeholder, price and stock, status, public link, sales summary, related orders table, top-affiliates-who-sold-this-product list, and an activity timeline.
- **FR-013**: Product types displayed in filters and badges MUST include: منتج فعلي، خدمة، كورس، ديجيتال برودكت، اشتراك.

#### Orders

- **FR-014**: System MUST provide `orders.html` with search by order number/customer, status filter, payment filter, affiliate filter, date filter UI, and a data table showing: order number, customer, product, affiliate (or "—"), total, commission, order status, payment status, shipping status, date, and an actions dropdown.
- **FR-015**: Each orders list row's actions dropdown MUST expose: View details, Edit order, Confirm order, Mark as shipped, Mark as delivered, Cancel order, Print invoice.
- **FR-016**: Status badges MUST cover the documented enums: Order ∈ {Pending, Confirmed, Processing, Shipped, Delivered, Cancelled}; Payment ∈ {Unpaid, Paid, Partially Paid, Refunded}; Shipping ∈ {Not Shipped, Preparing, Shipped, Delivered, Returned}.
- **FR-017**: System MUST provide `order-detail.html` containing: order summary, customer info, product info, affiliate attribution, commission info, payment status, shipping status, timeline, notes, and an invoice preview card.
- **FR-018**: System MUST provide `order-edit.html` with editable fields for: order status, payment status, shipping status, customer info, notes, affiliate attribution, and commission amount.

#### Affiliates (Core Differentiator)

- **FR-019**: System MUST provide `affiliates.html` with header, search, status filter, level filter, and a data table showing: affiliate name, level badge, referral code, orders, sales amount, pending commission, paid commission, conversion rate, status badge, and an actions dropdown.
- **FR-020**: Affiliate statuses MUST be one of {Pending, Active, Suspended, Rejected}; affiliate levels MUST be one of {Bronze, Silver, Gold, Platinum}.
- **FR-021**: Each affiliates list row's actions dropdown MUST expose: View profile, Approve, Suspend, Change level, View orders, Pay commission, Copy referral link.
- **FR-022**: System MUST provide `affiliate-detail.html` containing: profile summary, level badge, status badge, referral link copy box, QR code placeholder, coupon code, total clicks, orders, sales, pending commission, paid commission, conversion rate, orders-generated-by-affiliate table, payout history, marketing assets section, notes, and activity timeline.
- **FR-023**: The Copy Referral Link button on the affiliate detail page MUST copy the link to the system clipboard and display a transient "Copied" confirmation.
- **FR-024**: System MUST provide `affiliate-requests.html` listing pending affiliate applications with name, contact, social links, experience, requested date, and per-row actions: Approve, Reject, View details.
- **FR-025**: System MUST provide `affiliate-payouts.html` with tabs/sections for Pending payouts, Paid payouts, and Rejected payouts, and a table per state showing affiliate, requested amount, available balance, payment method, status, request date, and actions.
- **FR-026**: All affiliate pages MUST visibly display the commission rule: "يتم اعتماد العمولة بعد وصول الطلب إلى Delivered أو تأكيد الدفع."

#### Customers

- **FR-027**: System MUST provide `customers.html` with search, source filter, tags filter, and a data table showing: name, phone/email, source, affiliate (or "—"), orders count, total spent, last order, tags, and an actions dropdown.
- **FR-028**: Customer source filter values MUST cover: Direct, Affiliate, WhatsApp, Facebook, Instagram, TikTok, Manual.
- **FR-029**: System MUST provide `customer-detail.html` containing: profile card, contact info, source, affiliate attribution if exists, order history, total spent, notes, tags, follow-up status, and timeline.
- **FR-030**: System MUST provide `customer-edit.html` with editable fields: name, phone, email, address, source, tags, notes, follow-up date.

#### Landing Pages

- **FR-031**: System MUST provide `landing-pages.html` with a data table showing: title, linked product, status, visits, conversion rate, orders, revenue, last updated, and an actions dropdown exposing Preview, Edit, Copy link, Duplicate, Disable, Delete.
- **FR-032**: System MUST provide `landing-page-create.html` with a form containing: title, product selector, template selection cards, hero headline, subheadline, CTA text, offer price, benefits list, testimonials placeholder, FAQ placeholder, SEO title, SEO description, plus Save and Preview actions.
- **FR-033**: System MUST provide `landing-page-preview.html` rendering a complete public-facing landing page composed of: hero, product image, benefits, offer, CTA, testimonials, FAQ, and footer.

#### Settings, Profile, Notifications

- **FR-034**: System MUST provide `settings.html` with tabs/sections for: Business info, Branding, Payment settings, Affiliate commission settings, Notification settings, Security.
- **FR-035**: System MUST provide `profile.html` with fields for: name, email, phone, password change placeholder, avatar placeholder.
- **FR-036**: System MUST provide `notifications.html` with entries spanning: new orders, affiliate requests, payout requests, low stock alerts, payment updates.

#### Localization & Direction

- **FR-037**: All HTML pages MUST set `dir="rtl"` and `lang="ar"` and use Arabic copy for navigation, headings, table headers, button labels, and body text.
- **FR-038**: English MAY be used only for technical status tokens (e.g., Pending, Delivered, Cancelled, Paid, Refunded, Bronze, Silver, Gold, Platinum) where business convention favors them.
- **FR-038a**: Sample data MUST showcase multi-currency support: list-page rows (orders, affiliates, customers, landing pages, products) MUST distribute across at least three currencies — SAR, EGP, AED — with optional additional regional currencies; every numeric cell representing money MUST display an explicit currency token (e.g., `1,250 SAR`, `350 EGP`, `90 AED`); within a single entity (one order, one affiliate's totals, one landing page's revenue), the currency MUST remain consistent across all related fields.
- **FR-038b**: Sample person and business names MUST be predominantly Arabic-script (~80% of rows in customer, affiliate, testimonial, notification author, and merchant-business sample data), with the remaining ~20% in Latin script to reflect realistic mixed audiences (e.g., walk-in customers, English-branded businesses).

#### Visual & Design Constraints

- **FR-039**: Pages MUST use a unified visual language consistent with Constitution Principle IV: rounded cards, soft shadows, subtle borders, purple/blue gradient accents, clean typography, spacious layout, clear hierarchy.
- **FR-040**: Tables MUST be responsive — on narrow viewports they MUST either scroll horizontally with a sticky first column or collapse into mobile-friendly card lists.
- **FR-041**: A dark/light theme toggle MUST be present in the header on every dashboard page; toggling it MUST switch the document's theme class and persist the choice across page loads via the only permitted `localStorage` key (theme).

#### JavaScript Scope

- **FR-042**: A single `assets/js/main.js` file MUST implement: mobile sidebar toggle, action dropdown open/close, modal open/close, tab switching, copy-referral-link, and theme toggle.
- **FR-043**: No JavaScript files other than `assets/js/main.js` are permitted, and no use of frameworks, bundlers, or `npm run dev` is permitted (per Constitution Principle I). The **complete and exhaustive** list of `<script>` elements allowed on any page is:
  1. One `<script src="https://cdn.tailwindcss.com">` (Tailwind Play CDN, in `<head>`).
  2. One inline `<script>` block containing the `tailwind.config = { … }` configuration, immediately after item 1.
  3. One `<script src="https://unpkg.com/lucide@latest">` (Lucide CDN, in `<head>`); the corresponding `lucide.createIcons()` initialization MUST live inside `main.js`, NOT inline.
  4. One ≤5-line inline `<script>` block in `<head>` that reads `localStorage.getItem('smos:theme')` and toggles `document.documentElement.classList` to set the theme **before paint** (eliminates flash of incorrect theme).
  5. One `<script src="assets/js/main.js" defer>` bootstrap import.

  Any additional inline `<script>` block, any additional external script tag, or any module-style `<script type="module">` is FORBIDDEN.
- **FR-043a**: Icons across sidebar, header, status badges, action dropdowns, quick-action buttons, and feature illustrations MUST use Lucide via CDN. Pages MUST embed the Lucide CDN `<script>` and use `<i data-lucide="<icon-name>"></i>` placeholders that the Lucide runtime swaps into inline SVG on load. No other icon font, no other icon library.

#### Confirmation & Modal Patterns

- **FR-044**: Destructive actions (Delete, Cancel order, Suspend affiliate, Reject affiliate, Pay commission, Disable product/landing page) MUST open a confirmation modal with a clear destructive-style confirm button, a cancel button, and ESC/overlay dismissal.

#### Sidebar Link Integrity

- **FR-045**: Every sidebar link, every header link, every quick-action link, and every "View"/"Edit"/"Detail" link in any list page MUST resolve to a file that exists in the project — no dead links.

#### Brand Identity

- **FR-045a**: A bilingual wordmark "Smart Merchant OS" / "سمارت مرتشانت" paired with an inline-SVG abstract geometric glyph (rendered in a purple/blue gradient consistent with FR-039) MUST appear in: the dashboard sidebar header, the marketing site top navigation, the login and register brand panels, the marketing site footer, and the browser favicon. The full bilingual lockup MUST be used wherever horizontal space allows; in compact contexts (collapsed sidebar, favicon, mobile header), the glyph alone MAY appear.
- **FR-045b**: The abstract glyph MUST be defined as a single inline SVG component reused across all pages (no external image dependency for the logo) so the brand renders consistently regardless of network conditions.

#### Accessibility Baseline

- **FR-046**: Every interactive element (links, buttons, form inputs, dropdown triggers, tabs, modal close buttons, sidebar items) MUST display a visible focus ring when reached via keyboard.
- **FR-047**: Tab order on every page MUST follow the visual reading order (top-to-bottom, right-to-left in RTL) without unreachable interactive elements.
- **FR-048**: Modal dialogs and the mobile sidebar drawer MUST close on ESC key press in addition to overlay click and explicit close button.
- **FR-049**: Every `<img>` tag (including placeholder graphics, QR code placeholders, dashboard preview, product thumbnails, avatars, and landing-page hero images) MUST carry a meaningful `alt` attribute describing the depicted content; purely decorative images MUST use `alt=""`.
- **FR-050**: Body text and UI text MUST achieve at least 4.5:1 color contrast against their background; large text (≥18 pt or ≥14 pt bold) and UI components/state indicators MUST achieve at least 3:1, in both light and dark themes.

### Key Entities *(include if feature involves data)*

- **Product**: Catalogue item with name, type (one of five), price, discount, stock, status, sales count, image, description, SEO fields, public URL slug. Related to Orders and Affiliates (via sales).
- **Order**: Transaction with order number, customer reference, product reference, optional affiliate reference, total, commission, three independent statuses (order, payment, shipping), date, notes, timeline, invoice details.
- **Affiliate**: Marketer with name, level (Bronze/Silver/Gold/Platinum), status (Pending/Active/Suspended/Rejected), referral code, referral link, QR code, coupon, click count, sales aggregates, commission balances (pending and paid), conversion rate.
- **Affiliate Request**: Pending application with applicant name, contact, social links, experience description, requested date.
- **Affiliate Payout**: Withdrawal request with affiliate reference, requested amount, available balance, payment method, status (Pending/Paid/Rejected), request date.
- **Customer**: CRM record with name, phone, email, address, source (one of seven), optional affiliate attribution, order count, total spent, last order date, tags, notes, follow-up status and date.
- **Landing Page**: Marketing artifact with title, linked product, template selection, hero/subheadline/CTA copy, offer price, benefits, testimonials, FAQ, SEO fields, status, visits, conversion rate, orders, revenue, last updated.
- **Notification**: Inbox entry with category (new order / affiliate request / payout / low stock / payment update), summary text, timestamp, read state.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A reviewer can open the project directly by double-clicking `index.html` or via a Live Server extension, with zero install or build steps required.
- **SC-002**: A reviewer can navigate from any sidebar entry to its target page and back within a single click, with 0 broken links across all pages.
- **SC-003**: A first-time client viewer, after spending 5 minutes on the dashboard alone, can correctly explain in their own words what role affiliates play in the system and how commissions are earned and paid.
- **SC-004**: A reviewer scrolling through any list page (products, orders, affiliates, customers, landing pages) sees at least 6 realistic sample rows that include all required columns populated with non-placeholder content.
- **SC-005**: All confirmation modals open within 100 ms of clicking their trigger and close cleanly on Cancel, ESC, and overlay click without leaving the page in a stuck state.
- **SC-006**: The mobile sidebar drawer opens, dims the background, and dismisses correctly on at least three viewports (320 px, 414 px, 768 px) without horizontal scroll.
- **SC-007**: An Arabic-reading client reviewer can read every navigation label, table header, and form label in clear Arabic; English appears only for pre-agreed status tokens.
- **SC-008**: Toggling dark/light mode on one page persists the choice when navigating to any other page in the same browser session.
- **SC-009**: A reviewer auditing the project tree finds zero `package.json`, no `node_modules/`, no bundler config, and no framework code — only HTML, CSS, Tailwind references, and a single `assets/js/main.js`.
- **SC-010**: The Copy Referral Link button on the affiliate detail page successfully writes to the system clipboard on at least Chrome, Firefox, and Safari, and shows a visible "Copied" confirmation.
- **SC-011**: A client demoing the prototype can complete a guided affiliate-system tour (list → request approve → detail → payout) in under 90 seconds without encountering an empty placeholder page.
- **SC-012**: A keyboard-only user can navigate from the sidebar through the dashboard's primary tasks and back, with every focused element showing a visible focus indicator and no focus traps outside of modals/the mobile drawer (which deliberately trap focus and release it on ESC or overlay click).

## Assumptions

- **Sample data is hardcoded**: All table rows, stat values, chart contents, customer/order/affiliate records, and notification entries are hardcoded directly in the HTML files. No JSON loading, no API simulation.
- **Dashboard charts are placeholders**: The two chart placeholders on the dashboard render as styled SVG/illustrative graphics that suggest charts visually, not interactive plotting libraries. No real-time data binding.
- **QR code placeholders**: QR code regions on affiliate pages render as styled placeholder images (e.g., a static SVG of a QR pattern), not dynamically generated codes.
- **Tailwind delivery**: TailwindCSS is loaded via CDN, not via a build pipeline. Custom Tailwind config is embedded inline in each page if needed for RTL plugins or color tokens.
- **Custom font choice**: A modern Arabic-friendly web font (e.g., Cairo, Tajawal, or IBM Plex Sans Arabic) is loaded via Google Fonts CDN. Specific font selection is delegated to the implementing designer.
- **Theme persistence storage**: The dark/light mode preference is the only key written to `localStorage` (per Constitution Principle VII). It is read on each page load to set the document theme class before paint.
- **No authentication backend**: The login and register forms have no backend wiring; clicking the primary action navigates to `dashboard.html` for demo purposes.
- **Quick-action targets**: The dashboard's "Create order" quick action links to `orders.html` (since there is no `order-create.html` in the spec); "Add product" links to `product-create.html`; "Review affiliates" links to `affiliate-requests.html`; "Create landing page" links to `landing-page-create.html`.
- **File layout**: All HTML pages live at the project root; shared assets live under `assets/` (e.g., `assets/js/main.js`, `assets/css/`, `assets/img/`). This keeps the prototype simple to open and to host on any static server.
- **Image placeholders**: Product images, avatars, dashboard previews, and landing-page hero images use either inline SVG placeholders or a free placeholder service consistent with the premium look. No external production-asset CDN is required.
- **Currency display**: Every monetary value in sample data is rendered with its explicit currency token suffix (e.g., `1,250 SAR`). Numerals use Western Arabic digits (0–9) for table readability; Arabic-Indic digits (٠–٩) are not required. There is no live currency-conversion logic — values across rows are independently authored and not arithmetically related.
