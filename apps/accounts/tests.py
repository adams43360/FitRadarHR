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


class FeedbackTests(TestCase):
    """Widget de feedback in-app."""

    @classmethod
    def setUpTestData(cls):
        from core.testing import create_org_and_user
        cls.org, cls.user = create_org_and_user(name="Org FB", email="rh@fb.test")

    def test_post_creates_feedback(self):
        from apps.accounts.models import Feedback
        self.client.force_login(self.user)
        response = self.client.post(reverse("accounts:feedback"), {
            "message": "Il manque un import CSV !",
            "next": "/dashboard/",
        })
        self.assertRedirects(response, "/dashboard/")
        fb = Feedback.objects.for_org(self.org).get()
        self.assertEqual(fb.user, self.user)
        self.assertEqual(fb.page, "/dashboard/")

    def test_empty_message_rejected(self):
        from apps.accounts.models import Feedback
        self.client.force_login(self.user)
        self.client.post(reverse("accounts:feedback"), {"message": "   ", "next": "/dashboard/"})
        self.assertEqual(Feedback.objects.for_org(self.org).count(), 0)

    def test_anonymous_redirected_to_login(self):
        response = self.client.post(reverse("accounts:feedback"), {"message": "x"})
        self.assertEqual(response.status_code, 302)
        self.assertIn("login", response["Location"])

    def test_external_next_url_rejected(self):
        """Protection open redirect : un next externe retombe sur le dashboard."""
        self.client.force_login(self.user)
        response = self.client.post(reverse("accounts:feedback"), {
            "message": "test",
            "next": "https://evil.example/phishing",
        })
        self.assertEqual(response["Location"], "/dashboard/")


class LandingPageTests(TestCase):
    """Page d'accueil publique."""

    def test_anonymous_sees_landing(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Big Five")

    @override_settings(DEMO_MODE=True)
    def test_demo_cta_visible_when_enabled(self):
        response = self.client.get("/")
        self.assertContains(response, reverse("accounts:demo_login"))

    @override_settings(DEMO_MODE=False)
    def test_demo_cta_hidden_when_disabled(self):
        response = self.client.get("/")
        self.assertNotContains(response, reverse("accounts:demo_login"))

    def test_authenticated_redirected_to_dashboard(self):
        from core.testing import create_org_and_user
        org, user = create_org_and_user(name="Org L", email="rh@landing.test")
        self.client.force_login(user)
        response = self.client.get("/")
        self.assertRedirects(response, reverse("accounts:dashboard"))


class LicenseWordingTests(TestCase):
    """Changement de licence MIT → Fair Source (FSL-1.1-MIT), 2026-07-03.

    Aucune page publique ne doit plus affirmer "licence MIT" — le produit
    n'est plus "open source" au sens strict depuis ce changement."""

    def test_landing_page_no_longer_claims_mit(self):
        response = self.client.get("/")
        self.assertNotContains(response, "Open source (MIT)")
        self.assertNotContains(response, "licence MIT")
        self.assertContains(response, "FSL-1.1-MIT")

    def test_footer_no_longer_claims_mit(self):
        response = self.client.get("/")
        self.assertContains(response, "FSL-1.1-MIT")

    def test_privacy_policy_reflects_new_license(self):
        from core.testing import create_org_and_user
        _, user = create_org_and_user(name="Org Licence", email="rh@licence.test")
        self.client.force_login(user)
        response = self.client.get(reverse("accounts:privacy_policy"))
        self.assertContains(response, "FSL-1.1-MIT")
        self.assertNotContains(response, "licence MIT")

    def test_license_strings_translated_to_english(self):
        """Le catalogue EN doit couvrir les nouvelles chaînes liées à la
        licence (voir locale/en/LC_MESSAGES/django.po)."""
        from django.utils import translation
        with translation.override("en"):
            self.assertEqual(
                translation.gettext("Code source ouvert (FSL-1.1-MIT)"),
                "Open source code (FSL-1.1-MIT)",
            )
            self.assertEqual(
                translation.gettext("Bilingue & code source ouvert"),
                "Bilingual & open source code",
            )

    def test_license_strings_translated_to_german_and_spanish(self):
        """Item #8 roadmap V2 — parité ES/DE, y compris sur les chaînes de
        licence ajoutées lors du passage à Fair Source (FSL-1.1-MIT)."""
        from django.utils import translation
        with translation.override("de"):
            self.assertEqual(
                translation.gettext("Code source ouvert (FSL-1.1-MIT)"),
                "Quelloffener Code (FSL-1.1-MIT)",
            )
            self.assertEqual(
                translation.gettext("Bilingue & code source ouvert"),
                "Zweisprachig & quelloffener Code",
            )
        with translation.override("es"):
            self.assertEqual(
                translation.gettext("Code source ouvert (FSL-1.1-MIT)"),
                "Código fuente abierto (FSL-1.1-MIT)",
            )
            self.assertEqual(
                translation.gettext("Bilingue & code source ouvert"),
                "Bilingüe y código fuente abierto",
            )


class InviteManagerTests(TestCase):
    """Invitation de managers dans l'org — item #2 de la roadmap V2."""

    def setUp(self):
        from core.testing import create_org_and_user
        self.org, self.rh = create_org_and_user(name="Org Invite", email="rh@invite.test")

    def test_rh_can_invite_manager(self):
        self.client.force_login(self.rh)
        resp = self.client.post(reverse("accounts:members"), {
            "first_name": "Sacha", "last_name": "Manager", "email": "sacha@invite.test",
        })
        self.assertRedirects(resp, reverse("accounts:members"))
        user = User.objects.get(email="sacha@invite.test")
        self.assertEqual(user.role, User.Role.MANAGER)
        self.assertEqual(user.org, self.org)
        self.assertEqual(user.invited_by, self.rh)
        self.assertFalse(user.has_usable_password())

    def test_invitation_sends_password_set_email(self):
        self.client.force_login(self.rh)
        self.client.post(reverse("accounts:members"), {
            "first_name": "Sacha", "last_name": "Manager", "email": "sacha@invite.test",
        })
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ["sacha@invite.test"])

    def test_duplicate_email_rejected(self):
        self.client.force_login(self.rh)
        resp = self.client.post(reverse("accounts:members"), {
            "first_name": "Sacha", "last_name": "Manager", "email": self.rh.email,
        })
        self.assertEqual(resp.status_code, 200)  # re-render avec erreur
        self.assertTrue(resp.context["form"].errors.get("email"))
        self.assertEqual(len(mail.outbox), 0)

    def test_manager_cannot_access_members_page(self):
        from core.testing import create_org_and_user
        _, manager = create_org_and_user(
            name="Org2", email="manager@invite.test", role=User.Role.MANAGER
        )
        self.client.force_login(manager)
        resp = self.client.get(reverse("accounts:members"))
        self.assertEqual(resp.status_code, 403)

    def test_members_list_scoped_to_own_org(self):
        from core.testing import create_org_and_user
        other_org, other_rh = create_org_and_user(name="Autre org", email="rh@autre.test")
        self.client.force_login(self.rh)
        resp = self.client.get(reverse("accounts:members"))
        self.assertNotContains(resp, "rh@autre.test")

    def test_invited_manager_can_login_after_password_reset(self):
        """Vérifie que le compte invité (mot de passe inutilisable) peut bien
        définir un mot de passe puis se connecter — pas de configuration
        allauth qui bloquerait ce compte (ex. vérification email obligatoire)."""
        self.client.force_login(self.rh)
        self.client.post(reverse("accounts:members"), {
            "first_name": "Sacha", "last_name": "Manager", "email": "sacha@invite.test",
        })
        user = User.objects.get(email="sacha@invite.test")
        user.set_password("un-mot-de-passe-solide-123")
        user.save()
        self.client.logout()
        logged_in = self.client.login(username="sacha@invite.test", password="un-mot-de-passe-solide-123")
        self.assertTrue(logged_in)

    def test_invite_strings_translated_to_english(self):
        """Le catalogue EN doit couvrir les nouvelles chaînes de l'invitation manager
        (voir locale/en/LC_MESSAGES/django.po) — pas de régression bilingue."""
        from django.utils import translation
        with translation.override("en"):
            self.assertEqual(translation.gettext("Inviter un manager"), "Invite a manager")
            self.assertEqual(translation.gettext("Membres de l'organisation"), "Organization members")


# ──────────────────────────────────────────────────────────────────────────────
# SSO OIDC — item #7 de la roadmap V2 (US-E1-05)
# ──────────────────────────────────────────────────────────────────────────────

class OrgSSOConfigModelTests(TestCase):
    """Synchronisation OrgSSOConfig ↔ SocialApp (allauth)."""

    def setUp(self):
        from core.testing import create_org_and_user
        self.org, self.rh = create_org_and_user(name="Acme Corp", email="rh@acme.test")

    def _make_config(self, **kwargs):
        from apps.accounts.models import OrgSSOConfig
        defaults = dict(
            org=self.org, display_name="Acme SSO", login_slug="acme",
            issuer_url="https://idp.acme.test/realms/acme",
            client_id="fitradarhr", client_secret="s3cr3t",
        )
        defaults.update(kwargs)
        return OrgSSOConfig.objects.create(**defaults)

    def test_save_creates_matching_social_app(self):
        from allauth.socialaccount.models import SocialApp
        self._make_config(enabled=True)
        app = SocialApp.objects.get(provider="openid_connect", provider_id="acme")
        self.assertEqual(app.name, "Acme SSO")
        self.assertEqual(app.client_id, "fitradarhr")
        self.assertEqual(app.secret, "s3cr3t")
        self.assertEqual(app.settings["server_url"], "https://idp.acme.test/realms/acme")

    def test_disabled_config_not_linked_to_site(self):
        from django.contrib.sites.models import Site
        from allauth.socialaccount.models import SocialApp

        self._make_config(enabled=False)
        app = SocialApp.objects.get(provider="openid_connect", provider_id="acme")
        self.assertNotIn(Site.objects.get_current(), app.sites.all())

    def test_enabling_links_site_disabling_unlinks(self):
        from django.contrib.sites.models import Site
        from allauth.socialaccount.models import SocialApp

        config = self._make_config(enabled=True)
        app = SocialApp.objects.get(provider="openid_connect", provider_id="acme")
        self.assertIn(Site.objects.get_current(), app.sites.all())

        config.enabled = False
        config.save()
        app.refresh_from_db()
        self.assertNotIn(Site.objects.get_current(), app.sites.all())

    def test_delete_removes_social_app(self):
        from allauth.socialaccount.models import SocialApp

        config = self._make_config()
        config.delete()
        self.assertFalse(
            SocialApp.objects.filter(provider="openid_connect", provider_id="acme").exists()
        )

    def test_login_slug_unique_at_db_level(self):
        from core.testing import create_org_and_user
        from apps.accounts.models import OrgSSOConfig
        from django.db import IntegrityError, transaction

        self._make_config(login_slug="acme")
        other_org, _ = create_org_and_user(name="Autre", email="rh@autre-sso.test")
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                OrgSSOConfig.objects.create(
                    org=other_org, display_name="Autre SSO", login_slug="acme",
                    issuer_url="https://idp.autre.test", client_id="x", client_secret="y",
                )


class SSOConfigViewTests(TestCase):
    """Écran de configuration SSO — RH only, isolation multi-tenant."""

    def setUp(self):
        from core.testing import create_org_and_user
        self.org, self.rh = create_org_and_user(name="Acme Corp", email="rh@acme-cfg.test")

    def _post(self, **overrides):
        data = {
            "display_name": "Acme SSO", "login_slug": "acme-cfg",
            "issuer_url": "https://idp.acme.test/realms/acme",
            "client_id": "fitradarhr", "client_secret": "s3cr3t",
        }
        data.update(overrides)
        return self.client.post(reverse("accounts:sso_config"), data)

    def test_rh_can_create_config(self):
        from apps.accounts.models import OrgSSOConfig
        self.client.force_login(self.rh)
        resp = self._post()
        self.assertRedirects(resp, reverse("accounts:sso_config"))
        config = OrgSSOConfig.objects.get(org=self.org)
        self.assertEqual(config.login_slug, "acme-cfg")
        self.assertEqual(config.client_secret, "s3cr3t")

    def test_manager_forbidden(self):
        from core.testing import create_org_and_user
        from apps.accounts.models import User
        _, manager = create_org_and_user(
            name="Org2", email="manager@acme-cfg.test", role=User.Role.MANAGER
        )
        self.client.force_login(manager)
        resp = self.client.get(reverse("accounts:sso_config"))
        self.assertEqual(resp.status_code, 403)

    def test_client_secret_never_rendered(self):
        self.client.force_login(self.rh)
        self._post()
        resp = self.client.get(reverse("accounts:sso_config"))
        self.assertNotContains(resp, "s3cr3t")

    def test_resubmit_without_secret_keeps_existing(self):
        from apps.accounts.models import OrgSSOConfig
        self.client.force_login(self.rh)
        self._post()
        self._post(client_secret="", display_name="Acme SSO (renamed)")
        config = OrgSSOConfig.objects.get(org=self.org)
        self.assertEqual(config.client_secret, "s3cr3t")
        self.assertEqual(config.display_name, "Acme SSO (renamed)")

    def test_login_slug_must_be_unique_across_orgs(self):
        from core.testing import create_org_and_user
        other_org, other_rh = create_org_and_user(name="Autre", email="rh@autre-cfg.test")
        self.client.force_login(other_rh)
        self._post(login_slug="taken-slug")

        self.client.force_login(self.rh)
        resp = self._post(login_slug="taken-slug")
        self.assertEqual(resp.status_code, 200)  # re-render avec erreur
        self.assertTrue(resp.context["form"].errors.get("login_slug"))

    def test_config_isolated_per_org(self):
        from core.testing import create_org_and_user
        other_org, other_rh = create_org_and_user(name="Autre", email="rh@autre-cfg2.test")
        self.client.force_login(self.rh)
        self._post()

        self.client.force_login(other_rh)
        resp = self.client.get(reverse("accounts:sso_config"))
        self.assertIsNone(resp.context["config"])


class SSOLoginEntryTests(TestCase):
    """Point d'entrée public de connexion SSO."""

    def setUp(self):
        from core.testing import create_org_and_user
        from apps.accounts.models import OrgSSOConfig
        self.org, self.rh = create_org_and_user(name="Acme Corp", email="rh@acme-entry.test")
        self.config = OrgSSOConfig.objects.create(
            org=self.org, display_name="Acme SSO", login_slug="acme-entry",
            issuer_url="https://idp.acme.test/realms/acme",
            client_id="fitradarhr", client_secret="s3cr3t", enabled=True,
        )

    def test_enabled_slug_redirects_to_provider(self):
        resp = self.client.post(reverse("accounts:sso_login_entry"), {"login_slug": "acme-entry"})
        self.assertRedirects(
            resp, reverse("openid_connect_login", kwargs={"provider_id": "acme-entry"}),
            fetch_redirect_response=False,
        )

    def test_disabled_config_shows_error(self):
        self.config.enabled = False
        self.config.save()
        resp = self.client.post(reverse("accounts:sso_login_entry"), {"login_slug": "acme-entry"})
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Aucune organisation active")

    def test_unknown_slug_shows_error(self):
        resp = self.client.post(reverse("accounts:sso_login_entry"), {"login_slug": "nope"})
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Aucune organisation active")

    def test_slug_matching_is_case_insensitive(self):
        resp = self.client.post(reverse("accounts:sso_login_entry"), {"login_slug": "ACME-ENTRY"})
        self.assertRedirects(
            resp, reverse("openid_connect_login", kwargs={"provider_id": "acme-entry"}),
            fetch_redirect_response=False,
        )

    def test_sso_link_visible_on_login_page(self):
        resp = self.client.get(reverse("accounts:login"))
        self.assertContains(resp, reverse("accounts:sso_login_entry"))


class OrgScopedSocialAccountAdapterTests(TestCase):
    """Provisioning JIT — logique testée sans échange OAuth2/OIDC réel
    (nécessite un IdP en ligne, hors de portée des tests automatisés).
    Contrat vérifié ici : la partie FitRadarHR de l'adaptateur allauth."""

    def setUp(self):
        from core.testing import create_org_and_user
        from apps.accounts.models import OrgSSOConfig
        from apps.accounts.adapters import OrgScopedSocialAccountAdapter

        self.org, self.rh = create_org_and_user(name="Acme Corp", email="rh@acme-adapter.test")
        self.config = OrgSSOConfig.objects.create(
            org=self.org, display_name="Acme SSO", login_slug="acme-adapter",
            issuer_url="https://idp.acme.test/realms/acme",
            client_id="fitradarhr", client_secret="s3cr3t", enabled=True,
        )
        self.adapter = OrgScopedSocialAccountAdapter()

    def _request(self):
        from django.test import RequestFactory
        from django.contrib.sessions.middleware import SessionMiddleware
        from django.contrib.messages.storage.fallback import FallbackStorage

        request = RequestFactory().get("/")
        SessionMiddleware(lambda r: None).process_request(request)
        request.session.save()
        request._messages = FallbackStorage(request)
        return request

    def _sociallogin(self, email, provider="acme-adapter", uid="sub-1", first_name="New", last_name="Employee"):
        from allauth.socialaccount.models import SocialAccount, SocialLogin
        from apps.accounts.models import User

        account = SocialAccount(provider=provider, uid=uid)
        user_stub = User(email=email, first_name=first_name, last_name=last_name)
        return SocialLogin(user=user_stub, account=account)

    def test_new_user_provisioned_in_correct_org(self):
        from apps.accounts.models import User

        sociallogin = self._sociallogin(email="new@acme-adapter.test")
        self.adapter.pre_social_login(self._request(), sociallogin)

        user = User.objects.get(email="new@acme-adapter.test")
        self.assertEqual(user.org, self.org)
        self.assertEqual(user.role, User.Role.MANAGER)
        self.assertFalse(user.has_usable_password())
        self.assertTrue(sociallogin.is_existing)

    def test_existing_user_same_org_is_reused(self):
        from apps.accounts.models import User

        existing = User.objects.create_user(
            email="existing@acme-adapter.test", password=None,
            first_name="Existing", last_name="Person", org=self.org,
        )
        sociallogin = self._sociallogin(email="existing@acme-adapter.test")
        self.adapter.pre_social_login(self._request(), sociallogin)

        self.assertEqual(sociallogin.user.pk, existing.pk)
        self.assertEqual(User.objects.filter(email="existing@acme-adapter.test").count(), 1)

    def test_existing_user_other_org_is_rejected(self):
        from core.testing import create_org_and_user
        from apps.accounts.models import User
        from allauth.core.exceptions import ImmediateHttpResponse

        other_org, _ = create_org_and_user(name="Autre", email="rh@autre-adapter.test")
        User.objects.create_user(
            email="cross-org@test.test", password=None,
            first_name="Cross", last_name="Org", org=other_org,
        )
        sociallogin = self._sociallogin(email="cross-org@test.test")
        with self.assertRaises(ImmediateHttpResponse):
            self.adapter.pre_social_login(self._request(), sociallogin)

        # Aucun nouveau compte n'a été créé pour l'org du SSO utilisé
        self.assertFalse(User.objects.filter(email="cross-org@test.test", org=self.org).exists())

    def test_disabled_config_rejects_login(self):
        from allauth.core.exceptions import ImmediateHttpResponse

        self.config.enabled = False
        self.config.save()
        sociallogin = self._sociallogin(email="anyone@acme-adapter.test")
        with self.assertRaises(ImmediateHttpResponse):
            self.adapter.pre_social_login(self._request(), sociallogin)

    def test_existing_sociallogin_skips_provisioning(self):
        from apps.accounts.models import User
        from allauth.socialaccount.models import SocialAccount, SocialLogin

        existing = User.objects.create_user(
            email="already-linked@acme-adapter.test", password=None,
            first_name="Already", last_name="Linked", org=self.org,
        )
        account = SocialAccount(provider="acme-adapter", uid="sub-2")
        sociallogin = SocialLogin(user=existing, account=account)
        self.assertTrue(sociallogin.is_existing)

        # Ne doit rien lever ni rien changer — retour anticipé
        self.adapter.pre_social_login(self._request(), sociallogin)
        self.assertEqual(User.objects.filter(email="already-linked@acme-adapter.test").count(), 1)

    def test_sso_strings_translated_to_english(self):
        """Le catalogue EN doit couvrir les nouvelles chaînes SSO (voir
        locale/en/LC_MESSAGES/django.po) — pas de régression bilingue."""
        from django.utils import translation
        with translation.override("en"):
            self.assertEqual(
                translation.gettext("Connexion SSO (SAML/OIDC)"), "SSO login (SAML/OIDC)"
            )
            self.assertEqual(
                translation.gettext("Se connecter via votre organisation (SSO)"),
                "Sign in via your organization (SSO)",
            )
            self.assertEqual(
                translation.gettext("Un compte existe déjà avec cet email dans une autre organisation."),
                "An account already exists with this email in another organization.",
            )
