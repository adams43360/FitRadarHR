"""Tests d'isolation multi-tenant, droits et audit — rapports."""
from django.test import TestCase
from django.urls import reverse

from apps.accounts.models import User
from apps.fit.models import BigFiveProfile
from apps.teams.models import Person
from core.testing import create_org_and_user, create_profile

from .models import AuditLog


class ReportTenantIsolationTests(TestCase):
    def setUp(self):
        self.org1, self.user1 = create_org_and_user(name="Org 1", email="rh@org1.test")
        self.org2, self.user2 = create_org_and_user(name="Org 2", email="rh@org2.test")
        self.person1 = Person.objects.create(
            org=self.org1, email="alice@org1.test", first_name="Alice", last_name="A"
        )
        self.profile1 = create_profile(self.person1)

    def test_person_profile_cross_org_404(self):
        self.client.force_login(self.user2)
        resp = self.client.get(
            reverse("reports:person_profile", kwargs={"person_pk": self.person1.pk})
        )
        self.assertEqual(resp.status_code, 404)

    def test_person_profile_own_org_ok_and_audited(self):
        self.client.force_login(self.user1)
        resp = self.client.get(
            reverse("reports:person_profile", kwargs={"person_pk": self.person1.pk})
        )
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(
            AuditLog.objects.filter(org=self.org1, action="profile.viewed").exists()
        )

    def test_report_list_only_own_org(self):
        self.client.force_login(self.user2)
        resp = self.client.get(reverse("reports:list"))
        self.assertEqual(resp.status_code, 200)
        self.assertNotIn(self.person1, resp.context["persons"])

    def test_person_org_manager_for_org(self):
        self.assertIn(self.profile1, BigFiveProfile.objects.for_org(self.org1))
        self.assertNotIn(self.profile1, BigFiveProfile.objects.for_org(self.org2))


class AuditLogTests(TestCase):
    def setUp(self):
        self.org, self.rh = create_org_and_user(email="rh@org.test")
        self.manager = User.objects.create_user(
            email="manager@org.test",
            password="test-password",
            first_name="Mano",
            last_name="Ager",
            org=self.org,
            role=User.Role.MANAGER,
        )

    def test_audit_log_view_forbidden_for_manager(self):
        self.client.force_login(self.manager)
        resp = self.client.get(reverse("reports:audit_log"))
        self.assertEqual(resp.status_code, 403)

    def test_audit_log_view_ok_for_rh(self):
        self.client.force_login(self.rh)
        resp = self.client.get(reverse("reports:audit_log"))
        self.assertEqual(resp.status_code, 200)

    def test_audit_log_immutable(self):
        log = AuditLog.objects.create(
            org=self.org,
            user=self.rh,
            action="test.action",
            entity_type="Test",
            entity_id=self.org.id,
        )
        log.action = "modified"
        with self.assertRaises(Exception):
            log.save()
        with self.assertRaises(Exception):
            log.delete()
