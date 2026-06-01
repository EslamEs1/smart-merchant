from django.db.models import Q
from django.shortcuts import get_object_or_404

from .models import AffiliateProfile


def merchant_affiliates(user):
    """All affiliates owned by the given merchant (all statuses)."""
    return AffiliateProfile.objects.filter(merchant=user).select_related("user")


def get_owned_affiliate_or_404(user, pk):
    """Return the merchant's affiliate by pk, or 404 — never leaks cross-merchant existence."""
    return get_object_or_404(AffiliateProfile, merchant=user, pk=pk)


def pending_affiliates(qs):
    """Filter to Pending-only (drives the requests queue and pending count)."""
    return qs.filter(status=AffiliateProfile.Status.PENDING)


def active_affiliates(qs):
    """Filter to Active-only (reused by the future commission/portal phase)."""
    return qs.filter(status=AffiliateProfile.Status.ACTIVE)


def list_affiliates(merchant, params):
    """Owner-scoped affiliate queryset with optional q/status/level filtering."""
    qs = merchant_affiliates(merchant)

    q = (params.get("q") or "").strip()
    if q:
        qs = qs.filter(
            Q(full_name__icontains=q) | Q(referral_code__icontains=q)
        )

    status = (params.get("status") or "").strip()
    if status:
        qs = qs.filter(status=status)

    level = (params.get("level") or "").strip()
    if level:
        qs = qs.filter(level=level)

    return qs
