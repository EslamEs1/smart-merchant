from django.test import TestCase
from django.utils import timezone

from apps.accounts.models import User
from apps.affiliates import services
from apps.affiliates.models import AffiliateProfile


def make_merchant(username):
    return User.objects.create_user(
        username=username, email=f"{username}@x.com", password="pass", role="MERCHANT"
    )


def make_affiliate(merchant, status=AffiliateProfile.Status.PENDING, referral_code="CODE1", **kwargs):
    return AffiliateProfile.objects.create(
        merchant=merchant, status=status, referral_code=referral_code, full_name="Test", **kwargs
    )


class ApproveTests(TestCase):
    def setUp(self):
        self.m = make_merchant("m_approve")

    def test_pending_becomes_active(self):
        a = make_affiliate(self.m, referral_code="AP01")
        services.approve(a)
        a.refresh_from_db()
        self.assertEqual(a.status, AffiliateProfile.Status.ACTIVE)

    def test_approved_at_set(self):
        a = make_affiliate(self.m, referral_code="AP02")
        before = timezone.now()
        services.approve(a)
        a.refresh_from_db()
        self.assertIsNotNone(a.approved_at)
        self.assertGreaterEqual(a.approved_at, before)

    def test_non_pending_is_noop_status_unchanged(self):
        a = make_affiliate(
            self.m, status=AffiliateProfile.Status.ACTIVE, referral_code="AP03"
        )
        services.approve(a)
        a.refresh_from_db()
        self.assertEqual(a.status, AffiliateProfile.Status.ACTIVE)

    def test_non_pending_does_not_overwrite_approved_at(self):
        a = make_affiliate(
            self.m, status=AffiliateProfile.Status.ACTIVE, referral_code="AP04"
        )
        old_ts = a.approved_at
        services.approve(a)
        a.refresh_from_db()
        self.assertEqual(a.approved_at, old_ts)


class RejectTests(TestCase):
    def setUp(self):
        self.m = make_merchant("m_reject")

    def test_pending_becomes_rejected(self):
        a = make_affiliate(self.m, referral_code="RJ01")
        services.reject(a)
        a.refresh_from_db()
        self.assertEqual(a.status, AffiliateProfile.Status.REJECTED)

    def test_rejected_at_set(self):
        a = make_affiliate(self.m, referral_code="RJ02")
        before = timezone.now()
        services.reject(a)
        a.refresh_from_db()
        self.assertIsNotNone(a.rejected_at)
        self.assertGreaterEqual(a.rejected_at, before)

    def test_reason_appended_to_notes(self):
        a = make_affiliate(self.m, referral_code="RJ03")
        services.reject(a, reason="لا يستوفي الشروط")
        a.refresh_from_db()
        self.assertIn("لا يستوفي الشروط", a.notes)

    def test_non_pending_is_noop(self):
        a = make_affiliate(
            self.m, status=AffiliateProfile.Status.ACTIVE, referral_code="RJ04"
        )
        services.reject(a)
        a.refresh_from_db()
        self.assertEqual(a.status, AffiliateProfile.Status.ACTIVE)
        self.assertIsNone(a.rejected_at)


class SuspendTests(TestCase):
    def setUp(self):
        self.m = make_merchant("m_suspend")

    def test_active_becomes_suspended(self):
        a = make_affiliate(
            self.m, status=AffiliateProfile.Status.ACTIVE, referral_code="SU01"
        )
        services.suspend(a)
        a.refresh_from_db()
        self.assertEqual(a.status, AffiliateProfile.Status.SUSPENDED)

    def test_suspended_at_set(self):
        a = make_affiliate(
            self.m, status=AffiliateProfile.Status.ACTIVE, referral_code="SU02"
        )
        before = timezone.now()
        services.suspend(a)
        a.refresh_from_db()
        self.assertIsNotNone(a.suspended_at)
        self.assertGreaterEqual(a.suspended_at, before)

    def test_reason_appended_to_notes(self):
        a = make_affiliate(
            self.m, status=AffiliateProfile.Status.ACTIVE, referral_code="SU03"
        )
        services.suspend(a, reason="مخالفة الشروط")
        a.refresh_from_db()
        self.assertIn("مخالفة الشروط", a.notes)

    def test_non_active_is_noop(self):
        a = make_affiliate(self.m, referral_code="SU04")  # Pending
        services.suspend(a)
        a.refresh_from_db()
        self.assertEqual(a.status, AffiliateProfile.Status.PENDING)
        self.assertIsNone(a.suspended_at)

    def test_noop_does_not_overwrite_existing_suspended_at(self):
        a = make_affiliate(self.m, referral_code="SU05")  # Pending
        self.assertIsNone(a.suspended_at)
        services.suspend(a)
        a.refresh_from_db()
        self.assertIsNone(a.suspended_at)


class ReactivateTests(TestCase):
    def setUp(self):
        self.m = make_merchant("m_react")

    def test_suspended_becomes_active(self):
        a = make_affiliate(
            self.m, status=AffiliateProfile.Status.SUSPENDED, referral_code="RE01"
        )
        services.reactivate(a)
        a.refresh_from_db()
        self.assertEqual(a.status, AffiliateProfile.Status.ACTIVE)

    def test_non_suspended_is_noop(self):
        a = make_affiliate(self.m, referral_code="RE02")  # Pending
        services.reactivate(a)
        a.refresh_from_db()
        self.assertEqual(a.status, AffiliateProfile.Status.PENDING)


class ChangeLevelTests(TestCase):
    def setUp(self):
        self.m = make_merchant("m_level")

    def test_valid_level_set(self):
        a = make_affiliate(self.m, referral_code="LV01")
        services.change_level(a, AffiliateProfile.Level.GOLD)
        a.refresh_from_db()
        self.assertEqual(a.level, AffiliateProfile.Level.GOLD)

    def test_invalid_level_raises_value_error(self):
        a = make_affiliate(self.m, referral_code="LV02")
        with self.assertRaises(ValueError):
            services.change_level(a, "Diamond")

    def test_invalid_level_does_not_mutate(self):
        a = make_affiliate(self.m, referral_code="LV03")
        try:
            services.change_level(a, "Diamond")
        except ValueError:
            pass
        a.refresh_from_db()
        self.assertEqual(a.level, AffiliateProfile.Level.BRONZE)

    def test_level_change_independent_of_status(self):
        a = make_affiliate(
            self.m, status=AffiliateProfile.Status.SUSPENDED, referral_code="LV04"
        )
        services.change_level(a, AffiliateProfile.Level.PLATINUM)
        a.refresh_from_db()
        self.assertEqual(a.level, AffiliateProfile.Level.PLATINUM)
        self.assertEqual(a.status, AffiliateProfile.Status.SUSPENDED)


class SetNotesTests(TestCase):
    def setUp(self):
        self.m = make_merchant("m_notes")

    def test_notes_saved(self):
        a = make_affiliate(self.m, referral_code="NT01")
        services.set_notes(a, "ملاحظة جديدة")
        a.refresh_from_db()
        self.assertEqual(a.notes, "ملاحظة جديدة")

    def test_notes_can_be_cleared(self):
        a = make_affiliate(self.m, referral_code="NT02", notes="قديمة")
        services.set_notes(a, "")
        a.refresh_from_db()
        self.assertEqual(a.notes, "")

    def test_works_regardless_of_status(self):
        a = make_affiliate(
            self.m, status=AffiliateProfile.Status.REJECTED, referral_code="NT03"
        )
        services.set_notes(a, "ملاحظة على مرفوض")
        a.refresh_from_db()
        self.assertEqual(a.notes, "ملاحظة على مرفوض")
