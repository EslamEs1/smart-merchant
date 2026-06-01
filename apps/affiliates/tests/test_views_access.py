"""
US5 consolidated isolation + role + CSRF access matrix (T040).

Tests that the enforcement built incrementally across Foundational + US1–US4
holds end-to-end:
  - Cross-merchant → 404 on detail + all six mutations
  - Affiliate-role → 403 on every page (list, requests, detail, mutations)
  - Anonymous → login redirect on every page and mutation
  - Every mutation: GET → 405
  - Every mutation: missing CSRF → 403
"""

from django.test import Client, TestCase
from django.urls import reverse

from apps.accounts.models import User
from apps.affiliates.models import AffiliateProfile

MUTATION_NAMES = ["approve", "reject", "suspend", "reactivate", "change-level", "notes"]


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


def mutation_url(name, pk):
    return reverse(f"affiliates:{name}", kwargs={"pk": pk})


class CrossMerchantIsolationTests(TestCase):
    """Merchant B cannot GET detail or POST any mutation on merchant A's affiliate."""

    def setUp(self):
        self.owner = make_merchant("iso_owner")
        self.other = make_merchant("iso_other")
        self.aff = make_affiliate(
            self.owner, "ISOC01", status=AffiliateProfile.Status.ACTIVE
        )
        self.client.force_login(self.other)

    # --- read ---

    def test_detail_cross_merchant_404(self):
        url = reverse("affiliates:detail", kwargs={"pk": self.aff.pk})
        self.assertEqual(self.client.get(url).status_code, 404)

    # --- mutations (all six) ---

    def test_approve_cross_merchant_404(self):
        self.assertEqual(
            self.client.post(mutation_url("approve", self.aff.pk)).status_code, 404
        )

    def test_reject_cross_merchant_404(self):
        self.assertEqual(
            self.client.post(mutation_url("reject", self.aff.pk)).status_code, 404
        )

    def test_suspend_cross_merchant_404(self):
        self.assertEqual(
            self.client.post(mutation_url("suspend", self.aff.pk)).status_code, 404
        )

    def test_reactivate_cross_merchant_404(self):
        self.assertEqual(
            self.client.post(mutation_url("reactivate", self.aff.pk)).status_code, 404
        )

    def test_change_level_cross_merchant_404(self):
        self.assertEqual(
            self.client.post(
                mutation_url("change-level", self.aff.pk), {"level": "Gold"}
            ).status_code,
            404,
        )

    def test_notes_cross_merchant_404(self):
        self.assertEqual(
            self.client.post(
                mutation_url("notes", self.aff.pk), {"notes": "injected"}
            ).status_code,
            404,
        )

    def test_cross_merchant_mutations_leave_state_unchanged(self):
        original_status = self.aff.status
        original_level = self.aff.level
        original_notes = self.aff.notes
        for name in MUTATION_NAMES:
            self.client.post(
                mutation_url(name, self.aff.pk), {"level": "Gold", "notes": "injected"}
            )
        self.aff.refresh_from_db()
        self.assertEqual(self.aff.status, original_status)
        self.assertEqual(self.aff.level, original_level)
        self.assertEqual(self.aff.notes, original_notes)


class AffiliateRoleProtectionTests(TestCase):
    """Affiliate-role users → 403 on every merchant page."""

    def setUp(self):
        self.merchant = make_merchant("rp_merchant")
        self.aff_user = make_affiliate_user("rp_aff")
        self.aff = make_affiliate(self.merchant, "RP01")
        self.client.force_login(self.aff_user)

    # --- read pages ---

    def test_list_403_for_affiliate_role(self):
        self.assertEqual(self.client.get(reverse("affiliates:list")).status_code, 403)

    def test_requests_403_for_affiliate_role(self):
        self.assertEqual(
            self.client.get(reverse("affiliates:requests")).status_code, 403
        )

    def test_detail_403_for_affiliate_role(self):
        url = reverse("affiliates:detail", kwargs={"pk": self.aff.pk})
        self.assertEqual(self.client.get(url).status_code, 403)

    # --- mutations ---

    def test_approve_403_for_affiliate_role(self):
        self.assertEqual(
            self.client.post(mutation_url("approve", self.aff.pk)).status_code, 403
        )

    def test_reject_403_for_affiliate_role(self):
        self.assertEqual(
            self.client.post(mutation_url("reject", self.aff.pk)).status_code, 403
        )

    def test_suspend_403_for_affiliate_role(self):
        self.assertEqual(
            self.client.post(mutation_url("suspend", self.aff.pk)).status_code, 403
        )

    def test_reactivate_403_for_affiliate_role(self):
        self.assertEqual(
            self.client.post(mutation_url("reactivate", self.aff.pk)).status_code, 403
        )

    def test_change_level_403_for_affiliate_role(self):
        self.assertEqual(
            self.client.post(
                mutation_url("change-level", self.aff.pk), {"level": "Gold"}
            ).status_code,
            403,
        )

    def test_notes_403_for_affiliate_role(self):
        self.assertEqual(
            self.client.post(
                mutation_url("notes", self.aff.pk), {"notes": "test"}
            ).status_code,
            403,
        )


class AnonymousRedirectTests(TestCase):
    """Unauthenticated requests → login redirect on every page and mutation."""

    def setUp(self):
        merchant = make_merchant("anon_merchant")
        self.aff = make_affiliate(merchant, "ANON01")

    def _assert_login_redirect(self, response):
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login", response["Location"])

    # --- read pages ---

    def test_list_redirects_anonymous(self):
        self._assert_login_redirect(self.client.get(reverse("affiliates:list")))

    def test_requests_redirects_anonymous(self):
        self._assert_login_redirect(self.client.get(reverse("affiliates:requests")))

    def test_detail_redirects_anonymous(self):
        url = reverse("affiliates:detail", kwargs={"pk": self.aff.pk})
        self._assert_login_redirect(self.client.get(url))

    # --- mutations (using POST as intended) ---

    def test_approve_redirects_anonymous(self):
        self._assert_login_redirect(
            self.client.post(mutation_url("approve", self.aff.pk))
        )

    def test_reject_redirects_anonymous(self):
        self._assert_login_redirect(
            self.client.post(mutation_url("reject", self.aff.pk))
        )

    def test_suspend_redirects_anonymous(self):
        self._assert_login_redirect(
            self.client.post(mutation_url("suspend", self.aff.pk))
        )

    def test_reactivate_redirects_anonymous(self):
        self._assert_login_redirect(
            self.client.post(mutation_url("reactivate", self.aff.pk))
        )

    def test_change_level_redirects_anonymous(self):
        self._assert_login_redirect(
            self.client.post(
                mutation_url("change-level", self.aff.pk), {"level": "Gold"}
            )
        )

    def test_notes_redirects_anonymous(self):
        self._assert_login_redirect(
            self.client.post(mutation_url("notes", self.aff.pk), {"notes": "test"})
        )


class MutationHTTPMethodTests(TestCase):
    """GET on every mutation URL → 405 Method Not Allowed."""

    def setUp(self):
        self.merchant = make_merchant("method_merchant")
        self.aff = make_affiliate(self.merchant, "METHOD01")
        self.client.force_login(self.merchant)

    def test_approve_get_405(self):
        self.assertEqual(
            self.client.get(mutation_url("approve", self.aff.pk)).status_code, 405
        )

    def test_reject_get_405(self):
        self.assertEqual(
            self.client.get(mutation_url("reject", self.aff.pk)).status_code, 405
        )

    def test_suspend_get_405(self):
        self.assertEqual(
            self.client.get(mutation_url("suspend", self.aff.pk)).status_code, 405
        )

    def test_reactivate_get_405(self):
        self.assertEqual(
            self.client.get(mutation_url("reactivate", self.aff.pk)).status_code, 405
        )

    def test_change_level_get_405(self):
        self.assertEqual(
            self.client.get(mutation_url("change-level", self.aff.pk)).status_code, 405
        )

    def test_notes_get_405(self):
        self.assertEqual(
            self.client.get(mutation_url("notes", self.aff.pk)).status_code, 405
        )


class CSRFProtectionTests(TestCase):
    """Missing CSRF token on every mutation → 403 Forbidden."""

    def setUp(self):
        self.merchant = make_merchant("csrf_merchant")
        self.aff = make_affiliate(self.merchant, "CSRF01")
        self.csrf_client = Client(enforce_csrf_checks=True)
        self.csrf_client.force_login(self.merchant)

    def test_approve_csrf_required(self):
        self.assertEqual(
            self.csrf_client.post(mutation_url("approve", self.aff.pk)).status_code, 403
        )

    def test_reject_csrf_required(self):
        self.assertEqual(
            self.csrf_client.post(mutation_url("reject", self.aff.pk)).status_code, 403
        )

    def test_suspend_csrf_required(self):
        self.assertEqual(
            self.csrf_client.post(mutation_url("suspend", self.aff.pk)).status_code, 403
        )

    def test_reactivate_csrf_required(self):
        self.assertEqual(
            self.csrf_client.post(
                mutation_url("reactivate", self.aff.pk)
            ).status_code,
            403,
        )

    def test_change_level_csrf_required(self):
        self.assertEqual(
            self.csrf_client.post(
                mutation_url("change-level", self.aff.pk), {"level": "Gold"}
            ).status_code,
            403,
        )

    def test_notes_csrf_required(self):
        self.assertEqual(
            self.csrf_client.post(
                mutation_url("notes", self.aff.pk), {"notes": "test"}
            ).status_code,
            403,
        )
