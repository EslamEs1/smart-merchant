# Quickstart: Smart Merchant OS — Static Frontend MVP

**Feature**: 001-static-frontend-mvp
**Date**: 2026-05-10
**Audience**: Anyone — designer, reviewer, client, developer — who wants to
open the prototype and verify it works.

This is a **static HTML prototype**. There is no install step, no build, no
server required. If you can open a file in a browser, you can run this
project.

---

## Three ways to run it

### 1. Double-click (zero setup)

1. Open the project folder in your file explorer.
2. Double-click `index.html`.
3. The browser opens the marketing home page.
4. Use the top navigation to reach **Login** → click "تسجيل الدخول" → land on **Dashboard**.

> **Note**: One feature degrades on `file://` URLs — the **Copy Referral
> Link** button on the affiliate detail page may silently fail in some
> browsers because the Clipboard API requires a secure context. If you hit
> this, use method 2 or 3 instead.

### 2. VS Code Live Server (recommended for development)

1. Install the **Live Server** extension by Ritwick Dey.
2. In VS Code, open this project folder.
3. Right-click any `.html` file → **Open with Live Server**.
4. The browser opens at `http://127.0.0.1:5500/<page>.html` with hot reload
   on file save.

### 3. Any static HTTP server (for sharing on LAN)

```bash
# Python 3 (preinstalled on macOS/Linux):
python3 -m http.server 8080

# Then visit:
# http://localhost:8080/index.html
```

Other working alternatives:
- `npx http-server` (one-off; doesn't violate Constitution Principle I —
  it's a server, not a build step for the project itself)
- `php -S localhost:8080` (if you happen to have PHP)
- Any static-file capable IDE built-in preview

---

## Verification checklist

Once the prototype is open, walk this checklist to verify the implementation
satisfies the spec's success criteria. Each item ties back to a Success
Criterion (SC) or Functional Requirement (FR) from `spec.md`.

### A. Public site (Story 6)

- [ ] **SC-002 / FR-001..FR-004**: Open `index.html`. Click each top-nav
      link → no 404, all pages load.
- [ ] **FR-001**: On `index.html`, scroll through and confirm all required
      sections appear in order (hero, dashboard preview, affiliate growth,
      products/orders/customers, commissions/payouts, features grid,
      pricing teaser, testimonials, FAQ, footer).
- [ ] **FR-003**: On `pricing.html`, count exactly **3 plans** (Starter,
      Growth, Pro), each with monthly price, products limit, affiliates
      limit, orders limit, features, CTA button.
- [ ] **FR-004**: On `login.html` and `register.html`, brand-panel-plus-form
      layout renders, both pages cross-link, primary CTA navigates to
      `dashboard.html`.

### B. Dashboard shell (Stories 1–8 baseline)

- [ ] **FR-005, FR-006**: On `dashboard.html` (and any dashboard page),
      sidebar lists exactly: Dashboard, Products / Services, Orders,
      Customers, Affiliates, Payouts, Landing Pages, Analytics, Settings —
      in that order.
- [ ] **SC-002 / FR-045**: Click every sidebar item — each lands on an
      existing page. (Run `grep -rE 'href="[^"]+\.html"' . | …` to
      automate this audit if desired.)
- [ ] **FR-007 / SC-006**: Resize browser to 320 px width. Hamburger button
      appears in header. Tap it → drawer slides in, page dims. Tap the
      overlay or press ESC → drawer closes.

### C. Dashboard overview (Story 2)

- [ ] **FR-008 / SC-004**: On `dashboard.html`, count **6 stat cards** at
      the top with Arabic labels matching FR-008 list. Each card shows a
      placeholder value, trend indicator, and Lucide icon.
- [ ] **FR-008**: Two chart placeholders are visible mid-page, neither is
      an empty box. Recent orders table shows ≥ 6 rows. Top affiliates and
      top products cards each show ≥ 3 entries. Pending affiliate requests
      card has a queue with review actions.
- [ ] **FR-008**: Click each of the 4 quick action buttons. Each lands on
      its target page (`product-create.html`, `orders.html`,
      `affiliate-requests.html`, `landing-page-create.html`).

### D. Affiliate system tour (Story 1 — CORE) — < 90 seconds (SC-011)

1. From dashboard, click **Affiliates** in sidebar.
2. **FR-019, FR-020, FR-021**: On `affiliates.html`, scan rows for level
   badges (Bronze/Silver/Gold/Platinum) and status badges
   (Pending/Active/Suspended/Rejected). Open any row's actions dropdown —
   see **7 actions**: View profile, Approve, Suspend, Change level, View
   orders, Pay commission, Copy referral link.
3. Click **View profile** on any row → land on `affiliate-detail.html`.
4. **FR-022**: Verify presence of: profile summary, level + status badges,
   referral link copy box, QR code placeholder, coupon code, stats grid
   (clicks/orders/sales/pending/paid/conversion), attributed orders table,
   payout history, marketing assets, notes, timeline.
5. **FR-023 / SC-010**: Click the **Copy Referral Link** button → see
   transient "Copied" indicator → paste into a text editor to verify link
   was copied.
6. Navigate to `affiliate-requests.html` (sidebar Affiliates submenu or
   from dashboard's pending requests card).
7. **FR-024**: Click **Approve** on a pending row → confirmation modal
   opens with applicant name and confirm/cancel pair. Press ESC → modal
   closes cleanly (SC-005).
8. Navigate to `affiliate-payouts.html`.
9. **FR-025**: Switch tabs Pending → Paid → Rejected. Each tab swaps
   content without page reload, showing realistic rows.
10. **FR-026**: Confirm the commission rule banner ("يتم اعتماد العمولة
    بعد وصول الطلب إلى Delivered أو تأكيد الدفع.") is visible on every
    affiliate-system page.

### E. Products module (Story 3)

- [ ] **FR-009, FR-013**: On `products.html`, see ≥ 12 rows covering all
      five product types (منتج فعلي، خدمة، كورس، ديجيتال برودكت، اشتراك).
- [ ] **FR-010**: Open any row's actions dropdown. See: View details, Edit,
      Copy public link, Duplicate, Disable, Delete.
- [ ] **FR-011, FR-012**: Visit `product-create.html`,
      `product-edit.html`, `product-detail.html`. Confirm every field /
      section listed in spec is present.
- [ ] Click **Delete** on any row → confirmation modal opens with
      destructive-style confirm. Cancel → modal dismisses cleanly.

### F. Orders module (Story 4)

- [ ] **FR-014, FR-016**: On `orders.html`, see ≥ 14 rows. Status badges
      cover all enum values across the three families (order/payment/shipping).
      Some rows have an affiliate, some show "—".
- [ ] **FR-015**: Action dropdown exposes: View details, Edit order,
      Confirm order, Mark as shipped, Mark as delivered, Cancel order,
      Print invoice.
- [ ] **FR-017**: Visit `order-detail.html` — confirm presence of order
      summary, customer info, product info, affiliate attribution,
      commission info, payment status, shipping status, timeline, notes,
      invoice preview card.

### G. Customers module (Story 5)

- [ ] **FR-027, FR-028**: On `customers.html`, see ≥ 15 rows covering all
      seven sources (Direct, Affiliate, WhatsApp, Facebook, Instagram,
      TikTok, Manual). Source filter exposes all seven.
- [ ] **FR-029, FR-030**: Visit `customer-detail.html` and
      `customer-edit.html`. Confirm all required fields and sections.

### H. Landing pages (Story 7)

- [ ] **FR-031, FR-032, FR-033**: Visit `landing-pages.html`,
      `landing-page-create.html`, `landing-page-preview.html`. Confirm
      list rows, create-form fields, and preview-page sections per spec.

### I. Settings, profile, notifications (Story 8)

- [ ] **FR-034**: `settings.html` exposes the six tabs: Business info,
      Branding, Payment, Affiliate commission, Notifications, Security.
      Switch tabs — content swaps without reload.
- [ ] **FR-035**: `profile.html` shows name, email, phone, password
      placeholder, avatar placeholder.
- [ ] **FR-036**: `notifications.html` inbox spans all 5 categories.

### J. Cross-cutting

- [ ] **FR-037**: Every page has `<html dir="rtl" lang="ar">`. Visual reading
      flows right-to-left.
- [ ] **FR-041 / SC-008**: Toggle dark mode in the header. Reload any
      page — theme persists. Navigate to another dashboard page — theme
      still persists.
- [ ] **FR-039 / FR-040**: At 320 / 414 / 768 / 1280 px viewports, layout
      stays clean — tables either scroll horizontally or collapse to
      mobile-friendly cards. No layout breakage.
- [ ] **FR-046, FR-047, FR-048 / SC-012**: Tab through any dashboard
      page — every interactive element shows a focus ring; tab order
      follows visual reading order; ESC closes modals and the mobile drawer.
- [ ] **FR-049**: Inspect a few `<img>` tags — every one has a `alt`
      attribute (purely decorative ones may be `alt=""`).
- [ ] **FR-050**: Use a browser contrast checker on body text and badges
      in both light and dark themes — body achieves ≥ 4.5:1, large text /
      UI components ≥ 3:1.
- [ ] **FR-038a**: Scan list pages for monetary cells — every value has
      an explicit currency token (e.g., `1,250 SAR`, `350 EGP`,
      `90 AED`). Within a single entity (order, affiliate row), currency
      is consistent across fields.
- [ ] **FR-038b**: Scan list pages for names — predominantly Arabic
      script with ~20% Latin, distributed naturally.
- [ ] **FR-042, FR-043, FR-043a**: Inspect `assets/js/main.js` — single
      file, only the allow-listed behaviors. No other JS files. Lucide
      script and inline pre-paint theme script are the only allowed
      `<script>` blocks per page besides the deferred main.js import.
- [ ] **FR-044**: Trigger any destructive action (Delete product, Cancel
      order, Suspend affiliate, Reject affiliate, Pay commission) →
      confirmation modal opens with destructive-style confirm button,
      cancel button, ESC dismissal, overlay-click dismissal.
- [ ] **SC-009**: Audit the project tree — confirm absence of
      `package.json`, `node_modules/`, `dist/`, `webpack.config.*`,
      `vite.config.*`, `.babelrc`, etc.

---

## Smoke test (60-second sanity check)

If you only have one minute, run this:

1. Double-click `index.html` → marketing home loads, hero CTAs visible.
2. Click `تسجيل الدخول` → `login.html` loads with brand-panel layout.
3. Click the form's primary CTA → `dashboard.html` loads with full
   sidebar shell, 6 stat cards, 2 chart placeholders, recent orders.
4. Click **Affiliates** in sidebar → `affiliates.html` loads with ≥ 10
   rows, 4 level badges visible, commission rule banner visible.
5. Click any affiliate row's "View profile" action → `affiliate-detail.html`
   loads with referral link copy box, QR placeholder, stats grid.
6. Toggle dark mode in header → entire UI switches to dark theme.
7. Reload page → dark theme persists.
8. Resize to mobile width (≤ 480 px) → hamburger appears, sidebar
   collapses. Tap hamburger → drawer slides in.

If all 8 steps work, the prototype's spine is healthy.

---

## Common issues & fixes

| Issue | Cause | Fix |
|---|---|---|
| Theme toggle does nothing | `assets/js/main.js` missing or 404'd | Confirm file exists at exact path; check browser DevTools console |
| Icons render as `<i>` placeholders, not SVG | Lucide CDN failed to load OR `lucide.createIcons()` not called | Check Network tab for the Lucide script; ensure `main.js` calls `createIcons()` after DOMContentLoaded |
| Layout flips left-to-right unexpectedly on a single page | That page's `<html>` element is missing `dir="rtl"` | Add `dir="rtl" lang="ar"` |
| Copy Referral Link silently fails | Page is opened via `file://` and Clipboard API is restricted | Run via Live Server / `python -m http.server` |
| Tailwind utilities don't apply at all | Play CDN script blocked or 404'd | Check Network tab; ensure HTTPS connectivity |
| Dark mode flashes light briefly on load | Pre-paint inline theme script missing from `<head>` | Add the 3-line localStorage check before any other content in `<head>` |
| Action dropdown stays open when clicking elsewhere | Click-outside handler missing in `main.js` | Implement document-click handler that closes any open `[data-actions-dropdown]` |

---

**Status**: Quickstart is complete. Anyone with a modern browser can open
the prototype, verify it against the success criteria, and identify any
defects without running a single command beyond opening a file.
