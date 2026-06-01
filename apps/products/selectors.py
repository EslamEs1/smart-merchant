from django.db.models import Prefetch, Q
from django.shortcuts import get_object_or_404

from .models import Product, ProductImage


def merchant_products(user):
    """All products owned by the given merchant (all statuses)."""
    return Product.objects.filter(merchant=user)


def get_owned_product_or_404(user, slug):
    """Return the merchant's product by slug, or 404 — never leaking cross-merchant existence."""
    return get_object_or_404(Product, merchant=user, slug=slug)


def public_products(qs):
    """Filter a queryset down to Active-only products (excludes Draft and Disabled)."""
    return qs.filter(status=Product.Status.ACTIVE)


def list_products(merchant, params):
    """Owner-scoped product queryset with optional filtering by q/category/status/badge/stock."""
    qs = merchant_products(merchant).select_related("category").prefetch_related(
        Prefetch(
            "images",
            queryset=ProductImage.objects.order_by("sort_order", "id"),
            to_attr="prefetched_images",
        )
    )

    q = (params.get("q") or "").strip()
    if q:
        qs = qs.filter(
            Q(name__icontains=q)
            | Q(slug__icontains=q)
            | Q(public_link_slug__icontains=q)
        )

    category = (params.get("category") or "").strip()
    if category:
        qs = qs.filter(category__slug=category)

    status = (params.get("status") or "").strip()
    if status:
        qs = qs.filter(status=status)

    badge = (params.get("badge") or "").strip()
    if badge:
        qs = qs.filter(badge=badge)

    stock = (params.get("stock") or "").strip()
    if stock == "in":
        qs = qs.filter(stock_quantity__gt=0)
    elif stock == "out":
        qs = qs.filter(stock_quantity=0)

    return qs
