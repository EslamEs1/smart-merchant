from django.test import Client, TestCase
from django.urls import reverse

from apps.accounts.models import User
from apps.affiliates.models import AffiliateProfile


def make_merchant(username):
    return User.objects.create_user(
        username=username, email=f"{username}@x.com", password="pass", role="MERCHANT"
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


class SuspendTests(TestCase):
    def setUp(self):
        self.m = make_merchant("m_susp")
        self.aff = make_affiliate(self.m, "SUSP01", status=AffiliateProfile.Status.ACTIVE)
        self.url = reverse("affiliates:suspend", kwargs={"pk": self.aff.pk})
        self.client.force_login(self.m)

    def test_suspend_sets_suspended(self):
        self.client.post(self.url)
        self.aff.refresh_from_db()
        self.assertEqual(self.aff.status, AffiliateProfile.Status.SUSPENDED)

    def test_suspend_sets_suspended_at(self):
        self.client.post(self.url)
        self.aff.refresh_from_db()
        self.assertIsNotNone(self.aff.suspended_at)

    def test_suspend_with_reason_appended_to_notes(self):
        self.client.post(self.url, {"reason": "policy violation"})
        self.aff.refresh_from_db()
        self.assertIn("policy violation", self.aff.notes)

    def test_suspend_redirects_to_detail(self):
        response = self.client.post(self.url)
        self.assertRedirects(
            response,
            reverse("affiliates:detail", kwargs={"pk": self.aff.pk}),
            fetch_redirect_response=False,
        )

    def test_cross_merchant_returns_404(self):
        other = make_merchant("other_susp")
        self.client.force_login(other)
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 404)
        self.aff.refresh_from_db()
        self.assertEqual(self.aff.status, AffiliateProfile.Status.ACTIVE)

    def test_get_returns_405(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 405)

    def test_missing_csrf_returns_403(self):
        csrf_client = Client(enforce_csrf_checks=True)
        csrf_client.force_login(self.m)
        response = csrf_client.post(self.url)
        self.assertEqual(response.status_code, 403)


class ReactivateTests(TestCase):
    def setUp(self):
        self.m = make_merchant("m_react")
        self.aff = make_affiliate(self.m, "REACT01", status=AffiliateProfile.Status.SUSPENDED)
        self.url = reverse("affiliates:reactivate", kwargs={"pk": self.aff.pk})
        self.client.force_login(self.m)

    def test_reactivate_sets_active(self):
        self.client.post(self.url)
        self.aff.refresh_from_db()
        self.assertEqual(self.aff.status, AffiliateProfile.Status.ACTIVE)

    def test_reactivate_redirects_to_detail(self):
        response = self.client.post(self.url)
        self.assertRedirects(
            response,
            reverse("affiliates:detail", kwargs={"pk": self.aff.pk}),
            fetch_redirect_response=False,
        )

    def test_cross_merchant_returns_404(self):
        other = make_merchant("other_react")
        self.client.force_login(other)
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 404)
        self.aff.refresh_from_db()
        self.assertEqual(self.aff.status, AffiliateProfile.Status.SUSPENDED)

    def test_get_returns_405(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 405)

    def test_missing_csrf_returns_403(self):
        csrf_client = Client(enforce_csrf_checks=True)
        csrf_client.force_login(self.m)
        response = csrf_client.post(self.url)
        self.assertEqual(response.status_code, 403)


class ChangeLevelTests(TestCase):
    def setUp(self):
        self.m = make_merchant("m_lvl")
        self.aff = make_affiliate(self.m, "LVL01", level=AffiliateProfile.Level.BRONZE)
        self.url = reverse("affiliates:change-level", kwargs={"pk": self.aff.pk})
        self.client.force_login(self.m)

    def test_change_level_persists(self):
        self.client.post(self.url, {"level": "Gold"})
        self.aff.refresh_from_db()
        self.assertEqual(self.aff.level, AffiliateProfile.Level.GOLD)

    def test_invalid_level_rejected_nothing_saved(self):
        self.client.post(self.url, {"level": "Diamond"})
        self.aff.refresh_from_db()
        self.assertEqual(self.aff.level, AffiliateProfile.Level.BRONZE)

    def test_change_level_redirects_to_detail(self):
        response = self.client.post(self.url, {"level": "Silver"})
        self.assertRedirects(
            response,
            reverse("affiliates:detail", kwargs={"pk": self.aff.pk}),
            fetch_redirect_response=False,
        )

    def test_cross_merchant_returns_404(self):
        other = make_merchant("other_lvl")
        self.client.force_login(other)
        response = self.client.post(self.url, {"level": "Gold"})
        self.assertEqual(response.status_code, 404)
        self.aff.refresh_from_db()
        self.assertEqual(self.aff.level, AffiliateProfile.Level.BRONZE)

    def test_get_returns_405(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 405)

    def test_missing_csrf_returns_403(self):
        csrf_client = Client(enforce_csrf_checks=True)
        csrf_client.force_login(self.m)
        response = csrf_client.post(self.url, {"level": "Gold"})
        self.assertEqual(response.status_code, 403)


class EditNotesTests(TestCase):
    def setUp(self):
        self.m = make_merchant("m_notes")
        self.aff = make_affiliate(self.m, "NOTES01", notes="initial notes")
        self.url = reverse("affiliates:notes", kwargs={"pk": self.aff.pk})
        self.client.force_login(self.m)

    def test_edit_notes_persists(self):
        self.client.post(self.url, {"notes": "updated notes text"})
        self.aff.refresh_from_db()
        self.assertEqual(self.aff.notes, "updated notes text")

    def test_edit_notes_can_clear(self):
        self.client.post(self.url, {"notes": ""})
        self.aff.refresh_from_db()
        self.assertEqual(self.aff.notes, "")

    def test_edit_notes_redirects_to_detail(self):
        response = self.client.post(self.url, {"notes": "test"})
        self.assertRedirects(
            response,
            reverse("affiliates:detail", kwargs={"pk": self.aff.pk}),
            fetch_redirect_response=False,
        )

    def test_cross_merchant_returns_404(self):
        other = make_merchant("other_notes")
        self.client.force_login(other)
        response = self.client.post(self.url, {"notes": "hacked"})
        self.assertEqual(response.status_code, 404)
        self.aff.refresh_from_db()
        self.assertEqual(self.aff.notes, "initial notes")

    def test_get_returns_405(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 405)

    def test_missing_csrf_returns_403(self):
        csrf_client = Client(enforce_csrf_checks=True)
        csrf_client.force_login(self.m)
        response = csrf_client.post(self.url, {"notes": "test"})
        self.assertEqual(response.status_code, 403)
