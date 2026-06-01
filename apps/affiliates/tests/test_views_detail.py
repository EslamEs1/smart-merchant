from django.test import TestCase
from django.urls import reverse

from apps.accounts.models import User
from apps.affiliates.models import AffiliateProfile


def make_merchant(username):
    return User.objects.create_user(
        username=username, email=f"{username}@x.com", password="pass", role="MERCHANT"
    )


def make_affiliate_user(username):
    return User.objects.create_user(
        username=username, email=f"{username}@x.com", password="pass", role="AFFILIATE"
    )


def make_affiliate(merchant, referral_code, **kwargs):
    defaults = {
        "full_name": kwargs.pop("full_name", "Test Affiliate"),
        "status": kwargs.pop("status", AffiliateProfile.Status.ACTIVE),
        "level": kwargs.pop("level", AffiliateProfile.Level.BRONZE),
    }
    defaults.update(kwargs)
    return AffiliateProfile.objects.create(
        merchant=merchant, referral_code=referral_code, **defaults
    )


class DetailAccessTests(TestCase):
    def setUp(self):
        self.merchant = make_merchant("det_m")
        self.affiliate = make_affiliate(self.merchant, "DETCODE1", full_name="Detail Test Aff")
        self.url = reverse("affiliates:detail", kwargs={"pk": self.affiliate.pk})

    def test_anonymous_redirected_to_login(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login", response["Location"])

    def test_affiliate_role_denied_403(self):
        aff_user = make_affiliate_user("det_aff")
        self.client.force_login(aff_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_owner_merchant_can_access(self):
        self.client.force_login(self.merchant)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_cross_merchant_detail_returns_404(self):
        other = make_merchant("det_other")
        self.client.force_login(other)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 404)


class DetailDataTests(TestCase):
    def setUp(self):
        self.merchant = make_merchant("det_data")
        self.affiliate = make_affiliate(
            self.merchant,
            "DATACODE1",
            full_name="Data Affiliate",
            email="data@example.com",
            coupon_code="DATA10",
            notes="Important notes here.",
            country="المملكة العربية السعودية",
        )
        self.client.force_login(self.merchant)
        self.url = reverse("affiliates:detail", kwargs={"pk": self.affiliate.pk})

    def test_referral_link_rendered(self):
        response = self.client.get(self.url)
        self.assertContains(response, self.affiliate.referral_link)

    def test_coupon_code_rendered(self):
        response = self.client.get(self.url)
        self.assertContains(response, "DATA10")

    def test_notes_rendered(self):
        response = self.client.get(self.url)
        self.assertContains(response, "Important notes here.")

    def test_full_name_in_heading(self):
        response = self.client.get(self.url)
        self.assertContains(response, "Data Affiliate")

    def test_no_fabricated_order_data(self):
        response = self.client.get(self.url)
        self.assertNotContains(response, "ORD-2024-0091")
        self.assertNotContains(response, "28,400")

    def test_no_fabricated_payout_data(self):
        response = self.client.get(self.url)
        self.assertNotContains(response, "PAY-0034")
        self.assertNotContains(response, "2,500 SAR")

    def test_stat_cards_show_zero(self):
        response = self.client.get(self.url)
        self.assertContains(response, "0%")


class DetailNullUserTests(TestCase):
    def test_affiliate_with_null_user_renders_without_error(self):
        merchant = make_merchant("det_null")
        affiliate = AffiliateProfile.objects.create(
            merchant=merchant,
            full_name="No Account Affiliate",
            referral_code="NOUSER01",
            user=None,
        )
        self.client.force_login(merchant)
        url = reverse("affiliates:detail", kwargs={"pk": affiliate.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No Account Affiliate")
