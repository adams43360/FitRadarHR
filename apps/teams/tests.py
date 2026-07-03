"""Tests d'isolation multi-tenant et de droits — équipes et personnes."""
from django.core.files.uploadedfile import SimpleUploadedFile
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


class PersonImportTests(TestCase):
    """Import CSV en masse — item #4 de la roadmap V2."""

    def setUp(self):
        self.org, self.user = create_org_and_user(email="rh@org.test")

    def _upload(self, content):
        f = SimpleUploadedFile("import.csv", content.encode("utf-8"), content_type="text/csv")
        self.client.force_login(self.user)
        return self.client.post(reverse("teams:person_import"), {"csv_file": f})

    def test_valid_csv_creates_persons(self):
        csv_content = (
            "first_name,last_name,email,person_type\n"
            "Camille,Dupont,camille@org.test,candidate\n"
            "Alex,Martin,alex@org.test,collaborator\n"
        )
        self._upload(csv_content)
        self.assertEqual(Person.objects.for_org(self.org).count(), 2)
        alex = Person.objects.for_org(self.org).get(email="alex@org.test")
        self.assertEqual(alex.person_type, Person.PersonType.COLLABORATOR)

    def test_default_person_type_is_candidate(self):
        csv_content = "first_name,last_name,email\nCamille,Dupont,camille@org.test\n"
        self._upload(csv_content)
        person = Person.objects.for_org(self.org).get(email="camille@org.test")
        self.assertEqual(person.person_type, Person.PersonType.CANDIDATE)

    def test_missing_required_column_rejected(self):
        csv_content = "first_name,email\nCamille,camille@org.test\n"
        self._upload(csv_content)
        self.assertEqual(Person.objects.for_org(self.org).count(), 0)

    def test_duplicate_email_in_org_skipped(self):
        Person.objects.create(org=self.org, email="camille@org.test", first_name="X", last_name="Y")
        csv_content = "first_name,last_name,email\nCamille,Dupont,camille@org.test\n"
        self._upload(csv_content)
        # Toujours une seule personne — pas de doublon créé
        self.assertEqual(Person.objects.for_org(self.org).filter(email="camille@org.test").count(), 1)

    def test_duplicate_email_within_file_reported_as_error(self):
        csv_content = (
            "first_name,last_name,email\n"
            "Camille,Dupont,camille@org.test\n"
            "Camille,Bis,camille@org.test\n"
        )
        self._upload(csv_content)
        self.assertEqual(Person.objects.for_org(self.org).filter(email="camille@org.test").count(), 1)

    def test_invalid_email_row_skipped(self):
        csv_content = "first_name,last_name,email\nCamille,Dupont,pas-un-email\n"
        self._upload(csv_content)
        self.assertEqual(Person.objects.for_org(self.org).count(), 0)

    def test_import_isolated_by_org(self):
        other_org, other_user = create_org_and_user(name="Autre org", email="rh@autre.test")
        Person.objects.create(org=other_org, email="camille@org.test", first_name="X", last_name="Y")
        # Le même email existe dans une AUTRE org — ne doit pas bloquer l'import dans org1
        csv_content = "first_name,last_name,email\nCamille,Dupont,camille@org.test\n"
        self._upload(csv_content)
        self.assertEqual(Person.objects.for_org(self.org).filter(email="camille@org.test").count(), 1)

    def test_import_requires_login(self):
        f = SimpleUploadedFile("import.csv", b"first_name,last_name,email\n", content_type="text/csv")
        resp = self.client.post(reverse("teams:person_import"), {"csv_file": f})
        self.assertEqual(resp.status_code, 302)  # redirige vers login

    def test_template_download(self):
        self.client.force_login(self.user)
        resp = self.client.get(reverse("teams:person_import_template"))
        self.assertEqual(resp.status_code, 200)
        self.assertIn("first_name,last_name,email,person_type", resp.content.decode())
