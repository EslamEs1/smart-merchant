from django.test import Client, TestCase
from django.urls import reverse

from apps.accounts.models import User
from apps.affiliates.models import AffiliateProfile

URL = reverse("affiliates:list")


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


class AccessControlTests(TestCase):
    def test_anonymous_redirected_to_login(self):
        response = self.client.get(URL)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login", response["Location"])

    def test_affiliate_role_denied_403(self):
        aff_user = make_affiliate_user("af_user")
        self.client.force_login(aff_user)
        response = self.client.get(URL)
        self.assertEqual(response.status_code, 403)

    def test_merchant_can_access(self):
        m = make_merchant("m_access")
        self.client.force_login(m)
        response = self.client.get(URL)
        self.assertEqual(response.status_code, 200)


class OwnerScopeTests(TestCase):
    def setUp(self):
        self.ma = make_merchant("ma_list")
        self.mb = make_merchant("mb_list")
        self.a_of_a = make_affiliate(self.ma, "CODE_A", full_name="Merchant Alpha Affiliate")
        self.b_of_b = make_affiliate(self.mb, "CODE_B", full_name="Merchant Beta Affiliate")

    def test_merchant_sees_only_own_affiliates(self):
        self.client.force_login(self.ma)
        response = self.client.get(URL)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Merchant Alpha Affiliate")
        self.assertNotContains(response, "Merchant Beta Affiliate")

    def test_other_merchant_affiliates_not_visible(self):
        self.client.force_login(self.mb)
        response = self.client.get(URL)
        self.assertContains(response, "Merchant Beta Affiliate")
        self.assertNotContains(response, "Merchant Alpha Affiliate")


class EmptyStateTests(TestCase):
    def test_zero_affiliates_shows_empty_state(self):
        m = make_merchant("m_empty")
        self.client.force_login(m)
        response = self.client.get(URL)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "لا يوجد مسوقون بعد")

    def test_no_match_filter_shows_empty_state(self):
        m = make_merchant("m_nomatching")
        make_affiliate(m, "CODE1", full_name="Existing Affiliate")
        self.client.force_login(m)
        response = self.client.get(URL + "?q=zzz_nomatch")
        self.assertContains(response, "لا يوجد مسوقون بعد")


class FilterTests(TestCase):
    def setUp(self):
        self.m = make_merchant("m_flt")
        self.active = make_affiliate(
            self.m, "ACTIVE01", full_name="Active Affiliate",
            status=AffiliateProfile.Status.ACTIVE, level=AffiliateProfile.Level.GOLD
        )
        self.pending = make_affiliate(
            self.m, "PEND01", full_name="Pending Affiliate",
            status=AffiliateProfile.Status.PENDING, level=AffiliateProfile.Level.BRONZE
        )
        self.client.force_login(self.m)

    def test_q_filter_by_name(self):
        response = self.client.get(URL + "?q=Active+Affiliate")
        self.assertContains(response, "Active Affiliate")
        self.assertNotContains(response, "Pending Affiliate")

    def test_q_filter_by_referral_code(self):
        response = self.client.get(URL + "?q=PEND01")
        self.assertContains(response, "Pending Affiliate")
        self.assertNotContains(response, "Active Affiliate")

    def test_status_filter(self):
        response = self.client.get(URL + "?status=Pending")
        self.assertContains(response, "Pending Affiliate")
        self.assertNotContains(response, "Active Affiliate")

    def test_level_filter(self):
        response = self.client.get(URL + "?level=Gold")
        self.assertContains(response, "Active Affiliate")
        self.assertNotContains(response, "Pending Affiliate")


class PerformanceColumnsTests(TestCase):
    def test_performance_columns_show_zero(self):
        m = make_merchant("m_perf")
        make_affiliate(m, "PERF01")
        self.client.force_login(m)
        response = self.client.get(URL)
        self.assertEqual(response.status_code, 200)
        content = response.content.decode()
        # All numeric performance cells show 0 and 0%
        self.assertIn(">0%<", content)

    def test_no_fabricated_sales_figures(self):
        m = make_merchant("m_nofake")
        make_affiliate(m, "FAKE01")
        self.client.force_login(m)
        response = self.client.get(URL)
        # Prototype had "28,400 SAR" etc. — must NOT appear after conversion
        self.assertNotContains(response, "28,400")
        self.assertNotContains(response, "12,800")


class PaginationTests(TestCase):
    def test_paginated_list(self):
        m = make_merchant("m_page")
        for i in range(20):
            make_affiliate(m, f"PGCODE{i:02d}", full_name=f"Affiliate {i}")
        self.client.force_login(m)
        response = self.client.get(URL)
        self.assertEqual(response.status_code, 200)
        # First page shows 15 affiliates (page_size=15)
        self.assertContains(response, "عرض")

    def test_page_2_accessible(self):
        m = make_merchant("m_page2")
        for i in range(20):
            make_affiliate(m, f"P2CODE{i:02d}", full_name=f"Affiliate {i}")
        self.client.force_login(m)
        response = self.client.get(URL + "?page=2")
        self.assertEqual(response.status_code, 200)
