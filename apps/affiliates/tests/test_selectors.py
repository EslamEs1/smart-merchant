from django.test import TestCase

from apps.accounts.models import User
from apps.affiliates.models import AffiliateProfile
from apps.affiliates.selectors import (
    active_affiliates,
    list_affiliates,
    merchant_affiliates,
    pending_affiliates,
)


def make_merchant(username):
    return User.objects.create_user(
        username=username, email=f"{username}@x.com", password="pass", role="MERCHANT"
    )


def make_affiliate(merchant, status=AffiliateProfile.Status.ACTIVE, referral_code="CODE", **kwargs):
    return AffiliateProfile.objects.create(
        merchant=merchant,
        full_name=kwargs.pop("full_name", "Test"),
        status=status,
        referral_code=referral_code,
        **kwargs,
    )


class MerchantAffiliatesIsolationTests(TestCase):
    def setUp(self):
        self.ma = make_merchant("ma")
        self.mb = make_merchant("mb")
        self.a1 = make_affiliate(self.ma, referral_code="MA01")
        self.b1 = make_affiliate(self.mb, referral_code="MB01")

    def test_only_own_affiliates_returned(self):
        qs = merchant_affiliates(self.ma)
        self.assertIn(self.a1, qs)
        self.assertNotIn(self.b1, qs)

    def test_other_merchant_affiliates_excluded(self):
        qs = merchant_affiliates(self.mb)
        self.assertIn(self.b1, qs)
        self.assertNotIn(self.a1, qs)


class PendingActiveSelectorTests(TestCase):
    def setUp(self):
        self.m = make_merchant("m_pa")

    def test_pending_affiliates_returns_only_pending(self):
        p = make_affiliate(self.m, status=AffiliateProfile.Status.PENDING, referral_code="P01")
        a = make_affiliate(self.m, status=AffiliateProfile.Status.ACTIVE, referral_code="A01")
        qs = pending_affiliates(merchant_affiliates(self.m))
        self.assertIn(p, qs)
        self.assertNotIn(a, qs)

    def test_active_affiliates_returns_only_active(self):
        p = make_affiliate(self.m, status=AffiliateProfile.Status.PENDING, referral_code="P02")
        a = make_affiliate(self.m, status=AffiliateProfile.Status.ACTIVE, referral_code="A02")
        qs = active_affiliates(merchant_affiliates(self.m))
        self.assertIn(a, qs)
        self.assertNotIn(p, qs)

    def test_suspended_excluded_from_both(self):
        s = make_affiliate(self.m, status=AffiliateProfile.Status.SUSPENDED, referral_code="S01")
        self.assertNotIn(s, pending_affiliates(merchant_affiliates(self.m)))
        self.assertNotIn(s, active_affiliates(merchant_affiliates(self.m)))


class ListAffiliatesFilterTests(TestCase):
    def setUp(self):
        self.m = make_merchant("m_filter")
        self.a1 = make_affiliate(
            self.m,
            full_name="أحمد الشمري",
            status=AffiliateProfile.Status.ACTIVE,
            level=AffiliateProfile.Level.GOLD,
            referral_code="AHMAD20",
        )
        self.a2 = make_affiliate(
            self.m,
            full_name="سارة المنصور",
            status=AffiliateProfile.Status.PENDING,
            level=AffiliateProfile.Level.SILVER,
            referral_code="SARA10",
        )
        self.a3 = make_affiliate(
            self.m,
            full_name="Nora Ahmed",
            status=AffiliateProfile.Status.ACTIVE,
            level=AffiliateProfile.Level.PLATINUM,
            referral_code="NORA30",
        )

    def test_q_filters_by_full_name(self):
        qs = list_affiliates(self.m, {"q": "أحمد"})
        self.assertIn(self.a1, qs)
        self.assertNotIn(self.a2, qs)
        self.assertNotIn(self.a3, qs)

    def test_q_filters_by_referral_code(self):
        qs = list_affiliates(self.m, {"q": "NORA30"})
        self.assertIn(self.a3, qs)
        self.assertNotIn(self.a1, qs)

    def test_q_case_insensitive(self):
        qs = list_affiliates(self.m, {"q": "nora"})
        self.assertIn(self.a3, qs)

    def test_status_filter(self):
        qs = list_affiliates(self.m, {"status": "Pending"})
        self.assertIn(self.a2, qs)
        self.assertNotIn(self.a1, qs)

    def test_level_filter(self):
        qs = list_affiliates(self.m, {"level": "Gold"})
        self.assertIn(self.a1, qs)
        self.assertNotIn(self.a2, qs)
        self.assertNotIn(self.a3, qs)

    def test_q_and_status_combined(self):
        qs = list_affiliates(self.m, {"q": "سارة", "status": "Pending"})
        self.assertIn(self.a2, qs)
        self.assertNotIn(self.a1, qs)

    def test_blank_params_return_all(self):
        qs = list_affiliates(self.m, {"q": "", "status": "", "level": ""})
        self.assertEqual(qs.count(), 3)

    def test_no_match_returns_empty(self):
        qs = list_affiliates(self.m, {"q": "zzz_nomatch"})
        self.assertFalse(qs.exists())

    def test_isolation_from_other_merchant(self):
        other = make_merchant("other")
        make_affiliate(other, referral_code="OTH01", full_name="أحمد آخر")
        qs = list_affiliates(self.m, {"q": "أحمد"})
        self.assertEqual(qs.count(), 1)
        self.assertIn(self.a1, qs)
