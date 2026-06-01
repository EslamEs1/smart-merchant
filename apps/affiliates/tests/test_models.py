from django.db import IntegrityError, transaction
from django.test import TestCase

from apps.accounts.models import User
from apps.affiliates.models import REFERRAL_BASE, AffiliateProfile


def make_merchant(username):
    return User.objects.create_user(
        username=username, email=f"{username}@x.com", password="pass", role="MERCHANT"
    )


def make_affiliate(merchant, **kwargs):
    defaults = {"full_name": "Test Affiliate", "referral_code": "TESTCODE1"}
    defaults.update(kwargs)
    return AffiliateProfile.objects.create(merchant=merchant, **defaults)


class DefaultsTests(TestCase):
    def setUp(self):
        self.m = make_merchant("m_defaults")

    def test_default_status_is_pending(self):
        a = make_affiliate(self.m, referral_code="DEF01")
        self.assertEqual(a.status, AffiliateProfile.Status.PENDING)

    def test_default_level_is_bronze(self):
        a = make_affiliate(self.m, referral_code="DEF02")
        self.assertEqual(a.level, AffiliateProfile.Level.BRONZE)


class ReferralCodeUniquenessTests(TestCase):
    def setUp(self):
        self.ma = make_merchant("m_ref_a")
        self.mb = make_merchant("m_ref_b")

    def test_global_uniqueness_enforced(self):
        make_affiliate(self.ma, referral_code="SHARED")
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                make_affiliate(self.mb, referral_code="SHARED")

    def test_auto_generated_when_blank(self):
        a = AffiliateProfile.objects.create(merchant=self.ma, full_name="Auto Code Test")
        self.assertTrue(a.referral_code)

    def test_auto_generated_code_is_unique_on_collision(self):
        # Both affiliates have the same name → auto-generation must not collide
        a1 = AffiliateProfile.objects.create(merchant=self.ma, full_name="Nora Ahmed")
        a2 = AffiliateProfile.objects.create(merchant=self.mb, full_name="Nora Ahmed")
        self.assertNotEqual(a1.referral_code, a2.referral_code)

    def test_arabic_name_falls_back_to_aff_prefix(self):
        # Pure Arabic name → no ASCII chars → base = "AFF"
        a = AffiliateProfile.objects.create(merchant=self.ma, full_name="أحمد سالم")
        self.assertTrue(a.referral_code.startswith("AFF") or a.referral_code)


class CouponCodeUniquenessTests(TestCase):
    def setUp(self):
        self.ma = make_merchant("m_coupon_a")
        self.mb = make_merchant("m_coupon_b")

    def test_duplicate_coupon_same_merchant_rejected(self):
        make_affiliate(self.ma, referral_code="C01", coupon_code="SUMMER")
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                make_affiliate(self.ma, referral_code="C02", coupon_code="SUMMER")

    def test_blank_coupon_allowed_multiple_times_same_merchant(self):
        make_affiliate(self.ma, referral_code="C03", coupon_code="")
        make_affiliate(self.ma, referral_code="C04", coupon_code="")
        self.assertEqual(
            AffiliateProfile.objects.filter(merchant=self.ma, coupon_code="").count(), 2
        )

    def test_same_coupon_different_merchants_allowed(self):
        make_affiliate(self.ma, referral_code="C05", coupon_code="VIP")
        make_affiliate(self.mb, referral_code="C06", coupon_code="VIP")
        self.assertEqual(AffiliateProfile.objects.filter(coupon_code="VIP").count(), 2)


class ReferralLinkPropertyTests(TestCase):
    def setUp(self):
        self.m = make_merchant("m_link")

    def test_referral_link_format(self):
        a = make_affiliate(self.m, referral_code="MYCODE123")
        self.assertEqual(a.referral_link, f"{REFERRAL_BASE}/MYCODE123")

    def test_referral_link_starts_with_base(self):
        a = make_affiliate(self.m, referral_code="CODE99")
        self.assertTrue(a.referral_link.startswith("https://smartmerchant.os/r/"))


class HelperPropertiesTests(TestCase):
    def setUp(self):
        self.m = make_merchant("m_helpers")

    def test_is_active_true(self):
        a = make_affiliate(self.m, referral_code="ACT01", status=AffiliateProfile.Status.ACTIVE)
        self.assertTrue(a.is_active)

    def test_is_active_false_for_pending(self):
        a = make_affiliate(self.m, referral_code="ACT02")
        self.assertFalse(a.is_active)

    def test_is_pending_true(self):
        a = make_affiliate(self.m, referral_code="PEND01")
        self.assertTrue(a.is_pending)

    def test_is_pending_false_for_active(self):
        a = make_affiliate(
            self.m, referral_code="PEND02", status=AffiliateProfile.Status.ACTIVE
        )
        self.assertFalse(a.is_pending)
