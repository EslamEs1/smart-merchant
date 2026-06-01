from django.shortcuts import get_object_or_404

from .models import Product


def merchant_products(user):
    """All products owned by the given merchant (all statuses)."""
    return Product.objects.filter(merchant=user)


def get_owned_product_or_404(user, slug):
    """Return the merchant's product by slug, or 404 — never leaking cross-merchant existence."""
    return get_object_or_404(Product, merchant=user, slug=slug)


def public_products(qs):
    """Filter a queryset down to Active-only products (excludes Draft and Disabled)."""
    return qs.filter(status=Product.Status.ACTIVE)
