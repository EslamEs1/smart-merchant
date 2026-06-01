from django.utils import timezone

from .models import AffiliateProfile


def approve(affiliate):
    """Pending → Active; sets approved_at. No-op if not Pending (no timestamp overwrite)."""
    if affiliate.status != AffiliateProfile.Status.PENDING:
        return
    affiliate.status = AffiliateProfile.Status.ACTIVE
    affiliate.approved_at = timezone.now()
    affiliate.save(update_fields=["status", "approved_at", "updated_at"])


def reject(affiliate, reason=""):
    """Pending → Rejected; sets rejected_at; appends optional reason to notes. No-op if not Pending."""
    if affiliate.status != AffiliateProfile.Status.PENDING:
        return
    affiliate.status = AffiliateProfile.Status.REJECTED
    affiliate.rejected_at = timezone.now()
    if reason:
        affiliate.notes = (
            (affiliate.notes + "\n" + reason).strip() if affiliate.notes else reason
        )
    affiliate.save(update_fields=["status", "rejected_at", "notes", "updated_at"])


def suspend(affiliate, reason=""):
    """Active → Suspended; sets suspended_at; appends optional reason to notes. No-op if not Active."""
    if affiliate.status != AffiliateProfile.Status.ACTIVE:
        return
    affiliate.status = AffiliateProfile.Status.SUSPENDED
    affiliate.suspended_at = timezone.now()
    if reason:
        affiliate.notes = (
            (affiliate.notes + "\n" + reason).strip() if affiliate.notes else reason
        )
    affiliate.save(update_fields=["status", "suspended_at", "notes", "updated_at"])


def reactivate(affiliate):
    """Suspended → Active. No-op if not Suspended."""
    if affiliate.status != AffiliateProfile.Status.SUSPENDED:
        return
    affiliate.status = AffiliateProfile.Status.ACTIVE
    affiliate.save(update_fields=["status", "updated_at"])


def change_level(affiliate, level):
    """Set affiliate level (any status). Raises ValueError on an invalid value."""
    if level not in AffiliateProfile.Level.values:
        raise ValueError(f"Invalid affiliate level: {level!r}")
    affiliate.level = level
    affiliate.save(update_fields=["level", "updated_at"])


def set_notes(affiliate, text):
    """Replace affiliate notes (any status)."""
    affiliate.notes = text
    affiliate.save(update_fields=["notes", "updated_at"])
