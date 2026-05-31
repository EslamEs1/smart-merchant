"""Declarative page registry for the Smart Merchant OS prototype.

Each PageEntry records the URL path fragment, the template to render, and the
access level required.  Access is stored as metadata here; enforcement (login_required
/ role check) is layered on top in Phase 4 (US2) using this metadata.

Authoritative source: specs/003-backend-foundation/contracts/routes.md
33 prototype pages + "/" alias for index.html = 34 URL entries.
"""

from typing import NamedTuple


class Access:
    PUBLIC = "public"
    AUTH = "auth"
    MERCHANT = "merchant"
    AFFILIATE = "affiliate"


class PageEntry(NamedTuple):
    url_path: str  # URL path fragment, no leading slash; "" = site root
    template: str  # template file name inside templates/
    access: str    # one of Access.*


REGISTRY: list[PageEntry] = [
    # ── Public / auth ──────────────────────────────────────────────────────────
    PageEntry("", "index.html", Access.PUBLIC),            # /
    PageEntry("index.html", "index.html", Access.PUBLIC),  # /index.html
    PageEntry("features.html", "features.html", Access.PUBLIC),
    PageEntry("pricing.html", "pricing.html", Access.PUBLIC),
    PageEntry("login.html", "login.html", Access.AUTH),
    PageEntry("register.html", "register.html", Access.AUTH),
    # ── Merchant surface (login required) ─────────────────────────────────────
    PageEntry("dashboard.html", "dashboard.html", Access.MERCHANT),
    PageEntry("products.html", "products.html", Access.MERCHANT),
    PageEntry("product-create.html", "product-create.html", Access.MERCHANT),
    PageEntry("product-detail.html", "product-detail.html", Access.MERCHANT),
    PageEntry("product-edit.html", "product-edit.html", Access.MERCHANT),
    PageEntry("orders.html", "orders.html", Access.MERCHANT),
    PageEntry("order-detail.html", "order-detail.html", Access.MERCHANT),
    PageEntry("order-edit.html", "order-edit.html", Access.MERCHANT),
    PageEntry("customers.html", "customers.html", Access.MERCHANT),
    PageEntry("customer-detail.html", "customer-detail.html", Access.MERCHANT),
    PageEntry("customer-edit.html", "customer-edit.html", Access.MERCHANT),
    PageEntry("affiliates.html", "affiliates.html", Access.MERCHANT),
    PageEntry("affiliate-detail.html", "affiliate-detail.html", Access.MERCHANT),
    PageEntry("affiliate-requests.html", "affiliate-requests.html", Access.MERCHANT),
    PageEntry("affiliate-payouts.html", "affiliate-payouts.html", Access.MERCHANT),
    PageEntry("landing-pages.html", "landing-pages.html", Access.MERCHANT),
    PageEntry("landing-page-create.html", "landing-page-create.html", Access.MERCHANT),
    PageEntry("landing-page-preview.html", "landing-page-preview.html", Access.MERCHANT),
    PageEntry("analytics.html", "analytics.html", Access.MERCHANT),
    PageEntry("settings.html", "settings.html", Access.MERCHANT),
    PageEntry("profile.html", "profile.html", Access.MERCHANT),
    PageEntry("notifications.html", "notifications.html", Access.MERCHANT),
    # ── Affiliate surface (login required) ────────────────────────────────────
    PageEntry("affiliate-dashboard.html", "affiliate-dashboard.html", Access.AFFILIATE),
    PageEntry("affiliate-product-detail.html", "affiliate-product-detail.html", Access.AFFILIATE),
    PageEntry("affiliate-orders.html", "affiliate-orders.html", Access.AFFILIATE),
    PageEntry("affiliate-earnings.html", "affiliate-earnings.html", Access.AFFILIATE),
    PageEntry("affiliate-saved-products.html", "affiliate-saved-products.html", Access.AFFILIATE),
    PageEntry("affiliate-profile.html", "affiliate-profile.html", Access.AFFILIATE),
]
