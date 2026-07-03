"""Tests d'isolation multi-tenant — postes."""
from django.test import TestCase
from django.urls import reverse

from core.testing import create_org_and_user

from .models import Position, PositionProfile


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


class PositionCompareTests(TestCase):
    """Comparaison de candidats — item #3 de la roadmap V2."""

    def setUp(self):
        from apps.fit.engine import compute_all_fits_for_person
        from apps.fit.models import BigFiveProfile
        from apps.teams.models import Person

        self.org, self.user = create_org_and_user(email="rh@org.test")
        self.position = Position.objects.create(
            org=self.org, title_fr="Développeur", created_by=self.user
        )
        PositionProfile.objects.create(position=self.position)  # plage par défaut 0-100

        self.persons = []
        for i, (o, c, e, a, n) in enumerate([(80, 70, 60, 50, 40), (30, 40, 50, 60, 70), (55, 55, 55, 55, 55)]):
            person = Person.objects.create(
                org=self.org, email=f"person{i}@org.test", first_name=f"P{i}", last_name="Test"
            )
            BigFiveProfile.objects.create(
                person=person, openness=o, conscientiousness=c, extraversion=e,
                agreeableness=a, neuroticism=n, questionnaire_version="50",
            )
            compute_all_fits_for_person(person)
            self.persons.append(person)

    def _compare_url(self, persons):
        url = reverse("positions:compare", kwargs={"pk": self.position.pk})
        query = "&".join(f"persons={p.pk}" for p in persons)
        return f"{url}?{query}"

    def test_compare_two_candidates(self):
        self.client.force_login(self.user)
        resp = self.client.get(self._compare_url(self.persons[:2]))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.context["candidates"]), 2)

    def test_compare_requires_at_least_two(self):
        self.client.force_login(self.user)
        resp = self.client.get(self._compare_url(self.persons[:1]))
        self.assertRedirects(resp, reverse("positions:detail", kwargs={"pk": self.position.pk}))

    def test_compare_without_profile_redirects(self):
        no_profile_position = Position.objects.create(
            org=self.org, title_fr="Sans profil", created_by=self.user
        )
        self.client.force_login(self.user)
        url = reverse("positions:compare", kwargs={"pk": no_profile_position.pk})
        resp = self.client.get(f"{url}?persons={self.persons[0].pk}&persons={self.persons[1].pk}")
        self.assertRedirects(resp, reverse("positions:detail", kwargs={"pk": no_profile_position.pk}))

    def test_compare_cross_org_404(self):
        other_org, other_user = create_org_and_user(name="Autre org", email="rh@autre.test")
        self.client.force_login(other_user)
        resp = self.client.get(self._compare_url(self.persons[:2]))
        self.assertEqual(resp.status_code, 404)

    def test_compare_table_has_all_dimensions(self):
        self.client.force_login(self.user)
        resp = self.client.get(self._compare_url(self.persons))
        self.assertEqual(len(resp.context["dim_rows"]), 5)
        for row in resp.context["dim_rows"]:
            self.assertEqual(len(row["cells"]), 3)

    def test_compare_strings_translated_to_english(self):
        """Le catalogue EN doit couvrir les nouvelles chaînes de la comparaison
        (voir locale/en/LC_MESSAGES/django.po) — pas de régression bilingue."""
        from django.utils import translation
        with translation.override("en"):
            self.assertEqual(translation.gettext("Comparaison de candidats"), "Candidate comparison")
            self.assertEqual(
                translation.gettext("Comparer la sélection (2 à 5)"), "Compare selection (2 to 5)"
            )
