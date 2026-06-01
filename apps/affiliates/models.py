import re

from django.conf import settings
from django.db import models
from django.db.models import Q, UniqueConstraint
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

REFERRAL_BASE = "https://smartmerchant.os/r"


class AffiliateProfile(models.Model):
    class Status(models.TextChoices):
        PENDING = "Pending", _("قيد المراجعة")
        ACTIVE = "Active", _("نشط")
        SUSPENDED = "Suspended", _("موقوف")
        REJECTED = "Rejected", _("مرفوض")

    class Level(models.TextChoices):
        BRONZE = "Bronze", _("برونزي")
        SILVER = "Silver", _("فضي")
        GOLD = "Gold", _("ذهبي")
        PLATINUM = "Platinum", _("بلاتيني")

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="affiliate_links",
        verbose_name=_("حساب المسوّق"),
    )
    merchant = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="affiliates",
        verbose_name=_("التاجر"),
    )
    full_name = models.CharField(max_length=150, verbose_name=_("الاسم الكامل"))
    phone = models.CharField(max_length=32, blank=True, verbose_name=_("الجوال"))
    email = models.EmailField(blank=True, verbose_name=_("البريد الإلكتروني"))
    city = models.CharField(max_length=80, blank=True, verbose_name=_("المدينة"))
    country = models.CharField(max_length=80, blank=True, verbose_name=_("الدولة"))
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.PENDING,
        verbose_name=_("الحالة"),
    )
    level = models.CharField(
        max_length=10,
        choices=Level.choices,
        default=Level.BRONZE,
        verbose_name=_("المستوى"),
    )
    referral_code = models.CharField(
        max_length=32,
        unique=True,
        verbose_name=_("كود الإحالة"),
    )
    coupon_code = models.CharField(
        max_length=32,
        blank=True,
        verbose_name=_("كود الخصم"),
    )
    bio = models.TextField(blank=True, verbose_name=_("نبذة تعريفية"))
    social_instagram = models.CharField(
        max_length=120, blank=True, verbose_name=_("إنستغرام")
    )
    social_tiktok = models.CharField(
        max_length=120, blank=True, verbose_name=_("تيك توك")
    )
    social_facebook = models.CharField(
        max_length=120, blank=True, verbose_name=_("فيسبوك")
    )
    notes = models.TextField(blank=True, verbose_name=_("ملاحظات"))
    approved_at = models.DateTimeField(
        null=True, blank=True, verbose_name=_("تاريخ القبول")
    )
    rejected_at = models.DateTimeField(
        null=True, blank=True, verbose_name=_("تاريخ الرفض")
    )
    suspended_at = models.DateTimeField(
        null=True, blank=True, verbose_name=_("تاريخ الإيقاف")
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("مسوّق")
        verbose_name_plural = _("المسوّقون")
        ordering = ["-created_at"]
        constraints = [
            UniqueConstraint(
                fields=["merchant", "coupon_code"],
                condition=~Q(coupon_code=""),
                name="uniq_coupon_per_merchant",
            )
        ]

    def __str__(self):
        return self.full_name

    def save(self, *args, **kwargs):
        if not self.referral_code:
            self.referral_code = self._generate_unique_code()
        super().save(*args, **kwargs)

    def _generate_unique_code(self):
        # Keep only ASCII uppercase letters and digits; fall back to "AFF"
        base = re.sub(r"[^A-Z0-9]", "", self.full_name.upper()) or "AFF"
        base = base[:20]
        qs = AffiliateProfile.objects.all()
        if self.pk:
            qs = qs.exclude(pk=self.pk)
        candidate = base
        counter = 1
        while qs.filter(referral_code=candidate).exists():
            suffix = str(counter)
            candidate = base[: 32 - len(suffix)] + suffix
            counter += 1
        return candidate

    def get_absolute_url(self):
        return reverse("affiliates:detail", kwargs={"pk": self.pk})

    @property
    def referral_link(self):
        return f"{REFERRAL_BASE}/{self.referral_code}"

    @property
    def is_active(self):
        return self.status == self.Status.ACTIVE

    @property
    def is_pending(self):
        return self.status == self.Status.PENDING

    @property
    def is_suspended(self):
        return self.status == self.Status.SUSPENDED
