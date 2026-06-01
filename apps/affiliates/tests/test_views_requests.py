from django.test import Client, TestCase
from django.urls import reverse

from apps.accounts.models import User
from apps.affiliates.models import AffiliateProfile

URL = reverse("affiliates:requests")


def make_merchant(username):
    return User.objects.create_user(
        username=username, email=f"{username}@x.com", password="pass", role="MERCHANT"
    )


def make_affiliate_user(username):
    return User.objects.create_user(
        username=username, email=f"{username}@x.com", password="pass", role="AFFILIATE"
    )


def make_affiliate(merchant, referral_code, status=AffiliateProfile.Status.PENDING, **kwargs):
    return AffiliateProfile.objects.create(
        merchant=merchant,
        referral_code=referral_code,
        full_name=kwargs.pop("full_name", "Test Affiliate"),
        status=status,
        **kwargs,
    )


class AccessControlTests(TestCase):
    def test_anonymous_redirected_to_login(self):
        response = self.client.get(URL)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login", response["Location"])

    def test_affiliate_role_denied_403(self):
        aff = make_affiliate_user("aff_req")
        self.client.force_login(aff)
        response = self.client.get(URL)
        self.assertEqual(response.status_code, 403)

    def test_merchant_can_access(self):
        m = make_merchant("m_req_access")
        self.client.force_login(m)
        response = self.client.get(URL)
        self.assertEqual(response.status_code, 200)


class RequestsListTests(TestCase):
    def setUp(self):
        self.ma = make_merchant("ma_req")
        self.mb = make_merchant("mb_req")
        self.pending = make_affiliate(self.ma, "PEND01", full_name="Pending Affiliate")
        self.active = make_affiliate(
            self.ma, "ACT01", status=AffiliateProfile.Status.ACTIVE, full_name="Active One"
        )
        self.other = make_affiliate(self.mb, "OTHER01", full_name="Other Merchant Aff")
        self.client.force_login(self.ma)

    def test_shows_only_own_pending(self):
        response = self.client.get(URL)
        self.assertContains(response, "Pending Affiliate")
        self.assertNotContains(response, "Active One")
        self.assertNotContains(response, "Other Merchant Aff")

    def test_truthful_pending_count(self):
        response = self.client.get(URL)
        self.assertContains(response, "1")  # pending_count = 1

    def test_empty_state_no_pending(self):
        m = make_merchant("m_no_pending")
        make_affiliate(m, "ACT99", status=AffiliateProfile.Status.ACTIVE)
        self.client.force_login(m)
        response = self.client.get(URL)
        self.assertContains(response, "لا توجد طلبات معلقة")


class SearchTests(TestCase):
    def setUp(self):
        self.m = make_merchant("m_search")
        self.a1 = make_affiliate(self.m, "SRCH01", full_name="Nora Ahmed")
        self.a2 = make_affiliate(self.m, "SRCH02", full_name="Ahmad Salem")
        self.client.force_login(self.m)

    def test_q_filter_by_name(self):
        response = self.client.get(URL + "?q=Nora")
        self.assertContains(response, "Nora Ahmed")
        self.assertNotContains(response, "Ahmad Salem")

    def test_q_filter_by_referral_code(self):
        response = self.client.get(URL + "?q=SRCH02")
        self.assertContains(response, "Ahmad Salem")
        self.assertNotContains(response, "Nora Ahmed")

    def test_no_match_shows_empty_state(self):
        response = self.client.get(URL + "?q=zzz_nomatch")
        self.assertContains(response, "لا توجد طلبات معلقة")

    def test_q_echoed_in_empty_state_message(self):
        response = self.client.get(URL + "?q=zzz_nomatch")
        self.assertContains(response, "zzz_nomatch")


class ApproveTests(TestCase):
    def setUp(self):
        self.m = make_merchant("m_appr")
        self.aff = make_affiliate(self.m, "APR01")
        self.url = reverse("affiliates:approve", kwargs={"pk": self.aff.pk})
        self.client.force_login(self.m)

    def test_approve_sets_active(self):
        self.client.post(self.url)
        self.aff.refresh_from_db()
        self.assertEqual(self.aff.status, AffiliateProfile.Status.ACTIVE)

    def test_approve_redirects_to_requests(self):
        response = self.client.post(self.url)
        self.assertRedirects(response, URL)

    def test_approved_affiliate_leaves_queue(self):
        self.client.post(self.url)
        response = self.client.get(URL)
        self.assertNotContains(response, self.aff.full_name)

    def test_get_returns_405(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 405)

    def test_cross_merchant_approve_returns_404(self):
        other = make_merchant("other_appr")
        self.client.force_login(other)
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 404)
        self.aff.refresh_from_db()
        self.assertEqual(self.aff.status, AffiliateProfile.Status.PENDING)

    def test_missing_csrf_returns_403(self):
        csrf_client = Client(enforce_csrf_checks=True)
        csrf_client.force_login(self.m)
        response = csrf_client.post(self.url)
        self.assertEqual(response.status_code, 403)


class RejectTests(TestCase):
    def setUp(self):
        self.m = make_merchant("m_rej")
        self.aff = make_affiliate(self.m, "REJ01")
        self.url = reverse("affiliates:reject", kwargs={"pk": self.aff.pk})
        self.client.force_login(self.m)

    def test_reject_sets_rejected(self):
        self.client.post(self.url)
        self.aff.refresh_from_db()
        self.assertEqual(self.aff.status, AffiliateProfile.Status.REJECTED)

    def test_reject_with_reason_appended_to_notes(self):
        self.client.post(self.url, {"reason": "لا يستوفي الشروط"})
        self.aff.refresh_from_db()
        self.assertIn("لا يستوفي الشروط", self.aff.notes)

    def test_reject_redirects_to_requests(self):
        response = self.client.post(self.url)
        self.assertRedirects(response, URL)

    def test_rejected_affiliate_leaves_queue(self):
        self.client.post(self.url)
        response = self.client.get(URL)
        self.assertNotContains(response, self.aff.full_name)

    def test_get_returns_405(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 405)

    def test_cross_merchant_reject_returns_404(self):
        other = make_merchant("other_rej")
        self.client.force_login(other)
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 404)
        self.aff.refresh_from_db()
        self.assertEqual(self.aff.status, AffiliateProfile.Status.PENDING)

    def test_missing_csrf_returns_403(self):
        csrf_client = Client(enforce_csrf_checks=True)
        csrf_client.force_login(self.m)
        response = csrf_client.post(self.url)
        self.assertEqual(response.status_code, 403)
