"""Tests d'isolation multi-tenant et de droits — équipes et personnes."""
from django.test import TestCase
from django.urls import reverse

from apps.accounts.models import User
from core.testing import create_org_and_user

from .models import Person, Team, TeamMembership


class TenantIsolationTests(TestCase):
    """Aucune vue ne doit exposer des données d'une autre organisation."""

    def setUp(self):
        self.org1, self.user1 = create_org_and_user(name="Org 1", email="rh@org1.test")
        self.org2, self.user2 = create_org_and_user(name="Org 2", email="rh@org2.test")

        self.team1 = Team.objects.create(org=self.org1, name="Équipe Org1")
        self.person1 = Person.objects.create(
            org=self.org1, email="alice@org1.test", first_name="Alice", last_name="A"
        )

    def test_team_detail_cross_org_404(self):
        self.client.force_login(self.user2)
        resp = self.client.get(reverse("teams:detail", kwargs={"pk": self.team1.pk}))
        self.assertEqual(resp.status_code, 404)

    def test_team_edit_cross_org_404(self):
        self.client.force_login(self.user2)
        resp = self.client.get(reverse("teams:edit", kwargs={"pk": self.team1.pk}))
        self.assertEqual(resp.status_code, 404)

    def test_member_search_cross_org_404(self):
        self.client.force_login(self.user2)
        resp = self.client.get(
            reverse("teams:member_search", kwargs={"pk": self.team1.pk}), {"q": "al"}
        )
        self.assertEqual(resp.status_code, 404)

    def test_person_list_only_own_org(self):
        self.client.force_login(self.user2)
        resp = self.client.get(reverse("teams:persons"))
        self.assertEqual(resp.status_code, 200)
        self.assertNotIn(self.person1, resp.context["persons"])

    def test_person_edit_cross_org_404(self):
        self.client.force_login(self.user2)
        resp = self.client.get(reverse("teams:person_edit", kwargs={"pk": self.person1.pk}))
        self.assertEqual(resp.status_code, 404)

    def test_person_anonymize_cross_org_404(self):
        self.client.force_login(self.user2)
        resp = self.client.post(
            reverse("teams:person_anonymize", kwargs={"pk": self.person1.pk})
        )
        self.assertEqual(resp.status_code, 404)

    def test_org_manager_for_org(self):
        self.assertIn(self.team1, Team.objects.for_org(self.org1))
        self.assertNotIn(self.team1, Team.objects.for_org(self.org2))
        self.assertIn(self.person1, Person.objects.for_org(self.org1))
        self.assertNotIn(self.person1, Person.objects.for_org(self.org2))


class AnonymizeTests(TestCase):
    """Droit à l'effacement RGPD (E8)."""

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
        self.person = Person.objects.create(
            org=self.org, email="alice@org.test", first_name="Alice", last_name="Durand"
        )

    def test_manager_cannot_anonymize(self):
        self.client.force_login(self.manager)
        self.client.post(reverse("teams:person_anonymize", kwargs={"pk": self.person.pk}))
        self.person.refresh_from_db()
        self.assertEqual(self.person.first_name, "Alice")

    def test_rh_can_anonymize(self):
        from apps.reports.models import AuditLog

        self.client.force_login(self.rh)
        self.client.post(reverse("teams:person_anonymize", kwargs={"pk": self.person.pk}))
        self.person.refresh_from_db()
        self.assertEqual(self.person.first_name, "[supprimé]")
        self.assertNotIn("alice", self.person.email)
        self.assertTrue(
            AuditLog.objects.filter(org=self.org, action="person.anonymized").exists()
        )


class MembershipTests(TestCase):
    def setUp(self):
        self.org, self.user = create_org_and_user(email="rh@org.test")
        self.team = Team.objects.create(org=self.org, name="Équipe")
        self.person = Person.objects.create(
            org=self.org, email="alice@org.test", first_name="Alice", last_name="A"
        )

    def test_add_member_by_email(self):
        self.client.force_login(self.user)
        self.client.post(
            reverse("teams:add_member", kwargs={"pk": self.team.pk}),
            {"email": "alice@org.test"},
        )
        self.assertTrue(
            TeamMembership.objects.filter(
                team=self.team, person=self.person, left_at__isnull=True
            ).exists()
        )

    def test_add_member_duplicate_not_created_twice(self):
        TeamMembership.objects.create(team=self.team, person=self.person, added_by=self.user)
        self.client.force_login(self.user)
        self.client.post(
            reverse("teams:add_member", kwargs={"pk": self.team.pk}),
            {"email": "alice@org.test"},
        )
        self.assertEqual(
            TeamMembership.objects.filter(team=self.team, person=self.person).count(), 1
        )

    def test_remove_member_sets_left_at(self):
        membership = TeamMembership.objects.create(
            team=self.team, person=self.person, added_by=self.user
        )
        self.client.force_login(self.user)
        self.client.post(
            reverse(
                "teams:remove_member",
                kwargs={"pk": self.team.pk, "membership_pk": membership.pk},
            )
        )
        membership.refresh_from_db()
        self.assertIsNotNone(membership.left_at)
