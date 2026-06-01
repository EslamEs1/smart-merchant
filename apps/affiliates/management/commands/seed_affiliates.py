import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.affiliates.models import AffiliateProfile

User = get_user_model()

_AFFILIATES = [
    {
        "full_name": "أحمد الشمري",
        "level": AffiliateProfile.Level.GOLD,
        "status": AffiliateProfile.Status.ACTIVE,
        "referral_code": "AHMAD20",
        "coupon_code": "AHMAD20",
        "phone": "0501234567",
        "email": "ahmad.shamri@example.com",
        "city": "الرياض",
        "country": "السعودية",
        "bio": "مسوّق رقمي متخصص في منتجات التقنية والإلكترونيات",
        "social_instagram": "@ahmadmarketer",
    },
    {
        "full_name": "سارة المنصور",
        "level": AffiliateProfile.Level.SILVER,
        "status": AffiliateProfile.Status.ACTIVE,
        "referral_code": "SARA10",
        "coupon_code": "SARA10",
        "phone": "0509876543",
        "email": "sara.mansour@example.com",
        "city": "جدة",
        "country": "السعودية",
        "bio": "مؤثرة على وسائل التواصل الاجتماعي، متخصصة في المنتجات المنزلية",
        "social_tiktok": "@sarainfluencer",
    },
    {
        "full_name": "محمد العتيبي",
        "level": AffiliateProfile.Level.BRONZE,
        "status": AffiliateProfile.Status.PENDING,
        "referral_code": "MOHD01",
        "coupon_code": "",
        "phone": "0551112233",
        "email": "mohd.otaibi@example.com",
        "city": "مكة المكرمة",
        "country": "السعودية",
        "bio": "مهتم بالتجارة الإلكترونية والتسويق الرقمي، أبحث عن فرصة للانضمام",
    },
    {
        "full_name": "Nora Ahmed",
        "level": AffiliateProfile.Level.PLATINUM,
        "status": AffiliateProfile.Status.ACTIVE,
        "referral_code": "NORA30",
        "coupon_code": "NORA30",
        "phone": "0509001122",
        "email": "nora.ahmed@example.com",
        "city": "Dubai",
        "country": "UAE",
        "bio": "Digital marketing expert with 5+ years experience in physical commerce",
        "social_facebook": "fb.com/noramarketing",
    },
    {
        "full_name": "خالد سالم",
        "level": AffiliateProfile.Level.BRONZE,
        "status": AffiliateProfile.Status.SUSPENDED,
        "referral_code": "KHAL05",
        "coupon_code": "KHAL05",
        "phone": "0501237890",
        "email": "khaled.salem@example.com",
        "city": "الدمام",
        "country": "السعودية",
    },
]


class Command(BaseCommand):
    help = "Seed 5 demo affiliates on the demo merchant (idempotent)."

    def handle(self, *args, **options):
        merchant = self._get_merchant()
        self._seed_affiliates(merchant)
        self.stdout.write(self.style.SUCCESS("seed_affiliates completed successfully."))

    def _get_merchant(self):
        merchant = (
            User.objects.filter(role="MERCHANT", is_staff=False, is_superuser=False).first()
            or User.objects.filter(role="MERCHANT").first()
        )
        if merchant:
            self.stdout.write(f"Using existing merchant: {merchant.email}")
            return merchant

        merchant = User.objects.create_user(
            username="demo_merchant",
            email="demo@merchant.com",
            role="MERCHANT",
        )
        password = os.environ.get("DEMO_MERCHANT_PASSWORD")
        if password:
            merchant.set_password(password)
            merchant.save(update_fields=["password"])
            self.stdout.write(
                self.style.WARNING(
                    f"Created demo merchant: {merchant.email} "
                    "(password set from DEMO_MERCHANT_PASSWORD)."
                )
            )
        else:
            self.stdout.write(
                self.style.WARNING(
                    f"Created demo merchant: {merchant.email} (no usable password — set "
                    "DEMO_MERCHANT_PASSWORD before seeding, or run `manage.py changepassword`)."
                )
            )
        return merchant

    def _seed_affiliates(self, merchant):
        now = timezone.now()
        for data in _AFFILIATES:
            affiliate, created = AffiliateProfile.objects.get_or_create(
                merchant=merchant,
                referral_code=data["referral_code"],
                defaults={
                    "full_name": data["full_name"],
                    "level": data["level"],
                    "status": data["status"],
                    "coupon_code": data.get("coupon_code", ""),
                    "phone": data.get("phone", ""),
                    "email": data.get("email", ""),
                    "city": data.get("city", ""),
                    "country": data.get("country", ""),
                    "bio": data.get("bio", ""),
                    "social_instagram": data.get("social_instagram", ""),
                    "social_tiktok": data.get("social_tiktok", ""),
                    "social_facebook": data.get("social_facebook", ""),
                    "approved_at": (
                        now if data["status"] == AffiliateProfile.Status.ACTIVE else None
                    ),
                    "suspended_at": (
                        now if data["status"] == AffiliateProfile.Status.SUSPENDED else None
                    ),
                },
            )
            if created:
                self.stdout.write(
                    f"  Created: {affiliate.full_name} ({affiliate.level}/{affiliate.status})"
                )
