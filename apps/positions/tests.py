"""Tests d'isolation multi-tenant — postes."""
from django.test import TestCase
from django.urls import reverse

from core.testing import create_org_and_user

from .models import Position


class PositionTenantIsolationTests(TestCase):
    def setUp(self):
        self.org1, self.user1 = create_org_and_user(name="Org 1", email="rh@org1.test")
        self.org2, self.user2 = create_org_and_user(name="Org 2", email="rh@org2.test")
        self.position1 = Position.objects.create(
            org=self.org1, title_fr="Dev Org1", created_by=self.user1
        )

    def test_position_list_only_own_org(self):
        self.client.force_login(self.user2)
        resp = self.client.get(reverse("positions:list"))
        self.assertEqual(resp.status_code, 200)
        self.assertNotIn(self.position1, resp.context["positions"])

    def test_position_detail_cross_org_404(self):
        self.client.force_login(self.user2)
        resp = self.client.get(reverse("positions:detail", kwargs={"pk": self.position1.pk}))
        self.assertEqual(resp.status_code, 404)

    def test_position_edit_cross_org_404(self):
        self.client.force_login(self.user2)
        resp = self.client.get(reverse("positions:edit", kwargs={"pk": self.position1.pk}))
        self.assertEqual(resp.status_code, 404)

    def test_position_archive_cross_org_404(self):
        self.client.force_login(self.user2)
        resp = self.client.post(reverse("positions:archive", kwargs={"pk": self.position1.pk}))
        self.assertEqual(resp.status_code, 404)

    def test_profile_edit_cross_org_404(self):
        self.client.force_login(self.user2)
        resp = self.client.get(
            reverse("positions:profile_edit", kwargs={"pk": self.position1.pk})
        )
        self.assertEqual(resp.status_code, 404)

    def test_org_manager_for_org(self):
        self.assertIn(self.position1, Position.objects.for_org(self.org1))
        self.assertNotIn(self.position1, Position.objects.for_org(self.org2))
