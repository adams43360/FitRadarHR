"""Tests de l'API publique en lecture seule — item #9 roadmap V2 (US-E1-06)."""
import json

from django.test import TestCase, Client

from apps.departments.models import Department
from apps.fit.models import BigFiveProfile, PositionFitResult, TeamFitResult
from apps.positions.models import Position
from apps.teams.models import Person, Team, TeamMembership
from core.testing import create_org_and_user, create_profile

from .models import ApiKey


def _headers(raw_key):
    return {"HTTP_AUTHORIZATION": f"Api-Key {raw_key}"}


class ApiKeyModelTests(TestCase):
    def setUp(self):
        self.org, self.user = create_org_and_user()

    def test_generate_returns_raw_key_once_and_stores_only_hash(self):
        instance, raw_key = ApiKey.generate(org=self.org, name="Test", created_by=self.user)
        self.assertTrue(raw_key.startswith("frk_"))
        self.assertNotEqual(instance.key_hash, raw_key)
        self.assertEqual(instance.key_prefix, raw_key[:12])

    def test_authenticate_valid_key(self):
        instance, raw_key = ApiKey.generate(org=self.org, name="Test")
        found = ApiKey.authenticate(raw_key)
        self.assertEqual(found.pk, instance.pk)

    def test_authenticate_rejects_garbage(self):
        self.assertIsNone(ApiKey.authenticate("not-a-key"))
        self.assertIsNone(ApiKey.authenticate(""))
        self.assertIsNone(ApiKey.authenticate(None))

    def test_authenticate_rejects_revoked_key(self):
        instance, raw_key = ApiKey.generate(org=self.org, name="Test")
        instance.revoke()
        self.assertIsNone(ApiKey.authenticate(raw_key))
        self.assertFalse(instance.is_active)


class ApiAuthTests(TestCase):
    def setUp(self):
        self.org, self.user = create_org_and_user()
        self.instance, self.raw_key = ApiKey.generate(org=self.org, name="Test")
        self.client = Client()

    def test_missing_authorization_header_returns_401(self):
        response = self.client.get("/api/v1/positions/")
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json()["error"], "authentication_required")

    def test_wrong_scheme_returns_401(self):
        response = self.client.get("/api/v1/positions/", HTTP_AUTHORIZATION=f"Bearer {self.raw_key}")
        self.assertEqual(response.status_code, 401)

    def test_invalid_key_returns_401(self):
        response = self.client.get("/api/v1/positions/", HTTP_AUTHORIZATION="Api-Key frk_bogus")
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json()["error"], "invalid_api_key")

    def test_revoked_key_returns_401(self):
        self.instance.revoke()
        response = self.client.get("/api/v1/positions/", **_headers(self.raw_key))
        self.assertEqual(response.status_code, 401)

    def test_valid_key_returns_200_and_updates_last_used(self):
        self.assertIsNone(self.instance.last_used_at)
        response = self.client.get("/api/v1/positions/", **_headers(self.raw_key))
        self.assertEqual(response.status_code, 200)
        self.instance.refresh_from_db()
        self.assertIsNotNone(self.instance.last_used_at)

    def test_post_not_allowed(self):
        response = self.client.post("/api/v1/positions/", **_headers(self.raw_key))
        self.assertEqual(response.status_code, 405)


class ApiEndpointsTests(TestCase):
    def setUp(self):
        self.org, self.user = create_org_and_user()
        _, self.raw_key = ApiKey.generate(org=self.org, name="Test")
        self.dept = Department.objects.create(org=self.org, name_fr="Ingénierie", name_en="Engineering")
        self.position = Position.objects.create(
            org=self.org, title_fr="Développeur", title_en="Developer",
            department=self.dept, created_by=self.user,
        )
        self.team = Team.objects.create(org=self.org, name="Squad Alpha", department=self.dept, manager=self.user)
        self.person = Person.objects.create(
            org=self.org, email="candidate@org.test", first_name="Cami", last_name="Date",
            person_type=Person.PersonType.CANDIDATE, created_by=self.user,
        )
        TeamMembership.objects.create(team=self.team, person=self.person, added_by=self.user)
        self.profile = create_profile(self.person)
        self.position_fit = PositionFitResult.objects.create(
            person=self.person, position=self.position, person_profile=self.profile,
            openness_fit=80, conscientiousness_fit=70, extraversion_fit=60,
            agreeableness_fit=90, neuroticism_fit=50, overall_fit=70,
        )
        self.team_fit = TeamFitResult.objects.create(
            person=self.person, team=self.team, person_profile=self.profile,
            openness_fit=80, conscientiousness_fit=70, extraversion_fit=60,
            agreeableness_fit=90, neuroticism_fit=50, overall_fit=70,
            complementarity={"openness": "similar"},
        )
        self.client = Client()

    def get(self, path):
        return self.client.get(path, **_headers(self.raw_key))

    def test_positions_list(self):
        response = self.get("/api/v1/positions/")
        data = response.json()
        self.assertEqual(data["count"], 1)
        self.assertEqual(data["results"][0]["title_fr"], "Développeur")

    def test_positions_detail(self):
        response = self.get(f"/api/v1/positions/{self.position.id}/")
        self.assertEqual(response.json()["id"], str(self.position.id))

    def test_positions_detail_404_for_unknown(self):
        response = self.get("/api/v1/positions/00000000-0000-0000-0000-000000000000/")
        self.assertEqual(response.status_code, 404)

    def test_teams_list_includes_member_count(self):
        response = self.get("/api/v1/teams/")
        self.assertEqual(response.json()["results"][0]["member_count"], 1)

    def test_teams_detail(self):
        response = self.get(f"/api/v1/teams/{self.team.id}/")
        self.assertEqual(response.json()["name"], "Squad Alpha")

    def test_people_list_status_and_no_raw_scores(self):
        response = self.get("/api/v1/people/")
        person_json = response.json()["results"][0]
        self.assertEqual(person_json["first_name"], "Cami")
        self.assertTrue(person_json["has_big_five_profile"])
        for forbidden in ("openness", "conscientiousness", "extraversion", "agreeableness", "neuroticism"):
            self.assertNotIn(forbidden, person_json)

    def test_people_detail_never_exposes_raw_big_five(self):
        response = self.get(f"/api/v1/people/{self.person.id}/")
        raw_body = response.content.decode()
        # Le profil brut ne doit jamais fuiter, même sous une autre clé JSON.
        self.assertNotIn(str(float(self.profile.openness)), raw_body)

    def test_position_fit_results_list_content(self):
        response = self.get("/api/v1/fit-results/positions/")
        result = response.json()["results"][0]
        self.assertEqual(result["overall_fit"], 70.0)
        self.assertEqual(result["person_id"], str(self.person.id))

    def test_position_fit_results_filter_by_position(self):
        response = self.get(f"/api/v1/fit-results/positions/?position_id={self.position.id}")
        self.assertEqual(response.json()["count"], 1)
        response = self.get("/api/v1/fit-results/positions/?position_id=00000000-0000-0000-0000-000000000000")
        self.assertEqual(response.json()["count"], 0)

    def test_team_fit_results_list_includes_complementarity(self):
        response = self.get("/api/v1/fit-results/teams/")
        result = response.json()["results"][0]
        self.assertEqual(result["complementarity"], {"openness": "similar"})

    def test_no_endpoint_ever_returns_a_raw_big_five_dimension_field(self):
        """Garde-fou global : aucune réponse ne doit contenir les clés brutes
        `openness`/`conscientiousness`/`extraversion`/`agreeableness`/`neuroticism`
        (seules les variantes `_fit` dérivées sont autorisées)."""
        endpoints = [
            "/api/v1/positions/", "/api/v1/teams/", "/api/v1/people/",
            "/api/v1/fit-results/positions/", "/api/v1/fit-results/teams/",
        ]
        forbidden = {"openness", "conscientiousness", "extraversion", "agreeableness", "neuroticism"}
        for endpoint in endpoints:
            response = self.get(endpoint)
            data = json.loads(response.content)
            for result in data["results"]:
                self.assertFalse(forbidden & set(result.keys()), f"{endpoint} exposes raw Big Five keys")


class ApiPaginationTests(TestCase):
    def setUp(self):
        self.org, self.user = create_org_and_user()
        _, self.raw_key = ApiKey.generate(org=self.org, name="Test")
        for i in range(30):
            Position.objects.create(org=self.org, title_fr=f"Poste {i}", created_by=self.user)
        self.client = Client()

    def test_default_page_size(self):
        response = self.client.get("/api/v1/positions/", **_headers(self.raw_key))
        data = response.json()
        self.assertEqual(data["page_size"], 25)
        self.assertEqual(len(data["results"]), 25)
        self.assertEqual(data["num_pages"], 2)

    def test_custom_page_size_clamped_to_max(self):
        response = self.client.get("/api/v1/positions/?page_size=1000", **_headers(self.raw_key))
        self.assertEqual(response.json()["page_size"], 100)

    def test_second_page(self):
        response = self.client.get("/api/v1/positions/?page=2", **_headers(self.raw_key))
        data = response.json()
        self.assertEqual(data["page"], 2)
        self.assertEqual(len(data["results"]), 5)


class ApiCrossOrgIsolationTests(TestCase):
    def setUp(self):
        self.org_a, self.user_a = create_org_and_user(name="Org A", email="a@org.test")
        self.org_b, self.user_b = create_org_and_user(name="Org B", email="b@org.test")
        _, self.key_a = ApiKey.generate(org=self.org_a, name="Key A")

        self.position_a = Position.objects.create(org=self.org_a, title_fr="Poste A", created_by=self.user_a)
        self.position_b = Position.objects.create(org=self.org_b, title_fr="Poste B", created_by=self.user_b)
        self.person_b = Person.objects.create(
            org=self.org_b, email="person-b@org.test", first_name="B", last_name="B", created_by=self.user_b,
        )
        self.client = Client()

    def test_list_only_returns_own_org_data(self):
        response = self.client.get("/api/v1/positions/", **_headers(self.key_a))
        titles = [r["title_fr"] for r in response.json()["results"]]
        self.assertIn("Poste A", titles)
        self.assertNotIn("Poste B", titles)

    def test_detail_of_other_org_object_returns_404(self):
        response = self.client.get(f"/api/v1/positions/{self.position_b.id}/", **_headers(self.key_a))
        self.assertEqual(response.status_code, 404)

    def test_people_of_other_org_not_accessible(self):
        response = self.client.get(f"/api/v1/people/{self.person_b.id}/", **_headers(self.key_a))
        self.assertEqual(response.status_code, 404)


class ApiKeySettingsScreenTests(TestCase):
    def setUp(self):
        self.org, self.rh_user = create_org_and_user(email="rh@org.test", role=None)  # RH par défaut
        from apps.accounts.models import User
        self.manager_user = User.objects.create_user(
            email="manager@org.test", password="test-password",
            first_name="Manager", last_name="User", org=self.org, role=User.Role.MANAGER,
        )

    def test_manager_forbidden(self):
        self.client.login(email="manager@org.test", password="test-password")
        response = self.client.get("/settings/api/")
        self.assertEqual(response.status_code, 403)

    def test_anonymous_redirected_to_login(self):
        response = self.client.get("/settings/api/")
        self.assertEqual(response.status_code, 302)

    def test_rh_can_generate_and_see_raw_key_once(self):
        self.client.login(email="rh@org.test", password="test-password")
        response = self.client.post("/settings/api/", {"action": "generate", "name": "Intégration Test"}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(ApiKey.objects.filter(org=self.org).count(), 1)
        instance = ApiKey.objects.get(org=self.org)
        self.assertContains(response, "frk_")  # la clé en clair est affichée une fois...

        # ...mais un rechargement de la page ne doit plus jamais la montrer
        # (seul le préfixe non secret, `key_prefix`, reste visible dans la liste).
        response2 = self.client.get("/settings/api/")
        full_key_hash = instance.key_hash
        self.assertNotIn(full_key_hash, response2.content.decode())
        # Le corps ne doit contenir aucune chaîne plus longue que le préfixe stocké.
        prefix_occurrences = response2.content.decode().count("frk_")
        self.assertEqual(prefix_occurrences, 1)  # uniquement `key_prefix` dans le tableau

    def test_rh_can_revoke_key(self):
        instance, _raw = ApiKey.generate(org=self.org, name="À révoquer")
        self.client.login(email="rh@org.test", password="test-password")
        response = self.client.post("/settings/api/", {"action": "revoke", "key_id": str(instance.id)}, follow=True)
        self.assertEqual(response.status_code, 200)
        instance.refresh_from_db()
        self.assertFalse(instance.is_active)

    def test_cannot_revoke_key_of_another_org(self):
        other_org, _ = create_org_and_user(name="Other Org", email="other@org.test")
        instance, _raw = ApiKey.generate(org=other_org, name="Autre org")
        self.client.login(email="rh@org.test", password="test-password")
        self.client.post("/settings/api/", {"action": "revoke", "key_id": str(instance.id)})
        instance.refresh_from_db()
        self.assertTrue(instance.is_active)
