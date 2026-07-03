"""
Tests du mode démonstration (E1 + garde-fous).

- seed_demo : création, idempotence, garde-fou DEMO_MODE
- demo_login : connexion un clic, désactivation hors DEMO_MODE
- Garde-fous org démo : emails bloqués, effacement RGPD désactivé
- Isolation multi-tenant : les données démo ne fuient pas vers une autre org
"""
from django.conf import settings
from django.core import mail
from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase, override_settings
from django.urls import reverse

from apps.accounts.models import Organization, User
from apps.fit.models import BigFiveProfile, PositionFitResult, TeamFitResult
from apps.positions.models import Position
from apps.survey.models import QuestionnaireLink
from apps.teams.models import Person, Team


@override_settings(DEMO_MODE=True)
class SeedDemoCommandTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("seed_demo", verbosity=0)
        cls.org = Organization.objects.get(is_demo=True)

    def test_demo_org_created_with_content(self):
        self.assertEqual(self.org.name, settings.DEMO_ORG_NAME)
        self.assertTrue(self.org.is_demo)
        self.assertEqual(self.org.departments.count(), 6)
        self.assertEqual(Team.objects.for_org(self.org).count(), 10)
        self.assertEqual(Position.objects.for_org(self.org).count(), 9)
        self.assertEqual(Person.objects.for_org(self.org).count(), 48)
        self.assertEqual(BigFiveProfile.objects.for_org(self.org).count(), 45)

    def test_positions_all_have_target_profile(self):
        for position in Position.objects.for_org(self.org):
            self.assertTrue(position.has_profile, position.title_fr)

    def test_fit_results_computed(self):
        self.assertGreater(PositionFitResult.objects.for_org(self.org).count(), 0)
        self.assertGreater(TeamFitResult.objects.for_org(self.org).count(), 0)

    def test_pending_questionnaires_exist(self):
        pending = QuestionnaireLink.objects.for_org(self.org).exclude(
            status=QuestionnaireLink.Status.COMPLETED
        )
        self.assertGreater(pending.count(), 0)

    def test_demo_user_has_unusable_password(self):
        user = User.objects.get(email=settings.DEMO_USER_EMAIL)
        self.assertFalse(user.has_usable_password())
        self.assertTrue(user.is_rh)

    def test_seed_is_idempotent(self):
        counts_before = Person.objects.for_org(self.org).count()
        call_command("seed_demo", verbosity=0)
        orgs = Organization.objects.filter(is_demo=True)
        self.assertEqual(orgs.count(), 1)
        self.assertEqual(Person.objects.for_org(orgs.first()).count(), counts_before)

    def test_demo_emails_use_reserved_domains(self):
        """Les emails fictifs ne doivent jamais être routables (RFC 2606)."""
        for person in Person.objects.for_org(self.org):
            self.assertTrue(
                person.email.endswith(".example"),
                f"{person.email} n'utilise pas un domaine réservé",
            )


class SeedDemoGuardTests(TestCase):
    @override_settings(DEMO_MODE=False)
    def test_refuses_to_run_without_demo_mode(self):
        with self.assertRaises(CommandError):
            call_command("seed_demo", verbosity=0)

    @override_settings(DEMO_MODE=False)
    def test_force_flag_bypasses_guard(self):
        call_command("seed_demo", "--force", verbosity=0)
        self.assertTrue(Organization.objects.filter(is_demo=True).exists())


@override_settings(DEMO_MODE=True)
class DemoLoginTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("seed_demo", verbosity=0)

    def test_post_logs_into_demo_account(self):
        response = self.client.post(reverse("accounts:demo_login"))
        self.assertRedirects(response, reverse("accounts:dashboard"))
        user = User.objects.get(email=settings.DEMO_USER_EMAIL)
        self.assertEqual(self.client.session["_auth_user_id"], str(user.pk))

    def test_get_redirects_to_login(self):
        response = self.client.get(reverse("accounts:demo_login"))
        self.assertRedirects(response, reverse("accounts:login"))

    @override_settings(DEMO_MODE=False)
    def test_404_when_demo_mode_disabled(self):
        response = self.client.post(reverse("accounts:demo_login"))
        self.assertEqual(response.status_code, 404)

    def test_demo_button_visible_on_login_page(self):
        response = self.client.get(reverse("accounts:login"))
        self.assertContains(response, reverse("accounts:demo_login"))

    @override_settings(DEMO_MODE=False)
    def test_demo_button_hidden_when_disabled(self):
        response = self.client.get(reverse("accounts:login"))
        self.assertNotContains(response, reverse("accounts:demo_login"))


@override_settings(DEMO_MODE=True)
class DemoOrgGuardrailTests(TestCase):
    """Garde-fous : pas d'email réel, pas d'effacement RGPD depuis l'org démo."""

    @classmethod
    def setUpTestData(cls):
        call_command("seed_demo", verbosity=0)
        cls.org = Organization.objects.get(is_demo=True)
        cls.demo_user = User.objects.get(email=settings.DEMO_USER_EMAIL)

        # Org témoin (non-démo) pour vérifier le comportement normal
        cls.other_org = Organization.objects.create(name="Autre Org")
        cls.other_user = User.objects.create_user(
            email="rh@autre-org.test", password="x",
            first_name="Test", last_name="RH", org=cls.other_org,
        )

    def test_no_email_sent_from_demo_org(self):
        self.client.force_login(self.demo_user)
        response = self.client.post(reverse("survey:send"), {
            "person_email": "candidat.test@mail.example",
            "first_name": "Candidat",
            "last_name": "Test",
            "questionnaire_version": "50",
            "language": "fr",
        })
        self.assertRedirects(response, reverse("survey:dashboard"))
        self.assertEqual(len(mail.outbox), 0)
        # Le lien existe bien malgré l'absence d'email
        self.assertTrue(QuestionnaireLink.objects.for_org(self.org).filter(
            person__email="candidat.test@mail.example"
        ).exists())

    def test_email_still_sent_from_regular_org(self):
        self.client.force_login(self.other_user)
        response = self.client.post(reverse("survey:send"), {
            "person_email": "vrai.candidat@example.org",
            "first_name": "Vrai",
            "last_name": "Candidat",
            "questionnaire_version": "50",
            "language": "fr",
        })
        self.assertRedirects(response, reverse("survey:dashboard"))
        self.assertEqual(len(mail.outbox), 1)

    def test_rgpd_anonymize_blocked_in_demo_org(self):
        self.client.force_login(self.demo_user)
        person = Person.objects.for_org(self.org).first()
        response = self.client.post(reverse("teams:person_anonymize", kwargs={"pk": person.pk}))
        self.assertRedirects(response, reverse("teams:persons"))
        person.refresh_from_db()
        self.assertNotEqual(person.first_name, "[supprimé]")

    def test_demo_data_isolated_from_other_org(self):
        self.assertEqual(Person.objects.for_org(self.other_org).count(), 0)
        self.assertEqual(Team.objects.for_org(self.other_org).count(), 0)
        self.assertEqual(BigFiveProfile.objects.for_org(self.other_org).count(), 0)
