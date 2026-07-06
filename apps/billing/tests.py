"""Tests facturation — plan gratuit permanent (≤ 25 personnes) et abonnement (US-E1-07)."""
from datetime import timedelta
from unittest.mock import MagicMock, patch

from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone

from apps.accounts.models import Organization, User
from apps.positions.models import Position
from apps.teams.models import Person
from core.testing import create_org_and_user

from . import quotas, stripe_client
from .models import Subscription


class SubscriptionModelTests(TestCase):
    def setUp(self):
        self.org, self.user = create_org_and_user()

    def test_start_free_plan_creates_free_subscription(self):
        sub = Subscription.start_free_plan(self.org)
        self.assertEqual(sub.status, Subscription.Status.FREE)

    def test_get_or_create_is_idempotent(self):
        sub1 = Subscription.get_or_create_for_org(self.org)
        sub2 = Subscription.get_or_create_for_org(self.org)
        self.assertEqual(sub1.pk, sub2.pk)

    def test_free_plan_has_no_full_access(self):
        # Pas d'essai : les quotas du plan gratuit s'appliquent dès la création
        sub = Subscription.start_free_plan(self.org)
        self.assertFalse(sub.has_full_access)

    def test_has_full_access_true_when_paid_active(self):
        sub = Subscription.start_free_plan(self.org)
        sub.status = Subscription.Status.ACTIVE
        sub.save()
        self.assertTrue(sub.has_full_access)

    def test_demo_org_always_has_full_access(self):
        self.org.is_demo = True
        self.org.save()
        sub = Subscription.start_free_plan(self.org)
        sub.status = Subscription.Status.CANCELED
        sub.save()
        self.assertTrue(sub.has_full_access)

    def test_signup_b2b_creates_free_subscription(self):
        response = self.client.post(reverse("accounts:signup_b2b"), {
            "org_name": "Acme", "first_name": "A", "last_name": "B",
            "email": "acme@example.com", "password1": "correct horse battery",
            "password2": "correct horse battery",
        })
        self.assertEqual(response.status_code, 302)
        org = Organization.objects.get(name="Acme")
        self.assertTrue(Subscription.objects.filter(org=org, status=Subscription.Status.FREE).exists())


class QuotaTests(TestCase):
    def setUp(self):
        self.org, self.user = create_org_and_user()
        # Plan gratuit par défaut → quotas actifs
        Subscription.start_free_plan(self.org)

    def _fill_person_quota(self):
        for i in range(quotas.FREE_MAX_PEOPLE):
            Person.objects.create(org=self.org, email=f"p{i}@org.test", first_name="P", last_name=str(i))

    def test_person_quota_blocks_at_limit(self):
        self._fill_person_quota()
        self.assertIsNotNone(quotas.check_quota(self.org, "person"))

    def test_person_quota_allows_under_limit(self):
        Person.objects.create(org=self.org, email="p@org.test", first_name="P", last_name="P")
        self.assertIsNone(quotas.check_quota(self.org, "person"))

    def test_positions_never_quota_limited(self):
        # La création de postes est libre, même sur le plan gratuit
        for i in range(10):
            Position.objects.create(org=self.org, title_fr=f"Poste {i}", created_by=self.user)
        self.assertIsNone(quotas.check_quota(self.org, "position"))

    def test_questionnaires_never_quota_limited(self):
        # L'envoi de questionnaires est libre — le volume est capturé
        # implicitement par le nombre de personnes
        from apps.survey.models import QuestionnaireLink
        person = Person.objects.create(org=self.org, email="c@org.test", first_name="C", last_name="D")
        for i in range(10):
            QuestionnaireLink.objects.create(
                org=self.org, person=person, token=f"tok{i}",
                questionnaire_version="50", sent_by=self.user,
                expires_at=timezone.now() + timedelta(days=7),
            )
        self.assertIsNone(quotas.check_quota(self.org, "questionnaire"))

    def test_no_quota_when_paid_active(self):
        sub = Subscription.objects.get(org=self.org)
        sub.status = Subscription.Status.ACTIVE
        sub.save()
        self._fill_person_quota()
        self.assertIsNone(quotas.check_quota(self.org, "person"))

    def test_demo_org_never_quota_blocked(self):
        self.org.is_demo = True
        self.org.save()
        self._fill_person_quota()
        self.assertIsNone(quotas.check_quota(self.org, "person"))

    def test_remaining_quota_person(self):
        self.assertEqual(quotas.remaining_quota(self.org, "person"), quotas.FREE_MAX_PEOPLE)
        Person.objects.create(org=self.org, email="p@org.test", first_name="P", last_name="P")
        self.assertEqual(quotas.remaining_quota(self.org, "person"), quotas.FREE_MAX_PEOPLE - 1)


class QuotaEnforcedViewTests(TestCase):
    """Les vues de création doivent rediriger vers /settings/billing/ avec un
    message quand le quota est atteint, plutôt que de planter ou d'ignorer la limite."""

    def setUp(self):
        self.org, self.user = create_org_and_user()
        Subscription.start_free_plan(self.org)
        self.client.force_login(self.user)

    def _fill_person_quota(self):
        for i in range(quotas.FREE_MAX_PEOPLE):
            Person.objects.create(org=self.org, email=f"p{i}@org.test", first_name="P", last_name=str(i))

    def test_position_create_never_blocked(self):
        # Plus de limite sur les postes : la création reste possible hors quota
        for i in range(5):
            Position.objects.create(org=self.org, title_fr=f"Poste {i}", created_by=self.user)
        response = self.client.post(reverse("positions:create"), {
            "title_fr": "Poste supplémentaire", "status": "active",
        })
        self.assertEqual(response.status_code, 302)
        self.assertNotEqual(response.url, reverse("accounts:billing_settings"))
        self.assertTrue(Position.objects.filter(title_fr="Poste supplémentaire").exists())

    def test_send_questionnaire_existing_person_never_blocked(self):
        # L'envoi à une personne déjà existante n'est pas soumis au quota
        self._fill_person_quota()
        response = self.client.post(reverse("survey:send"), {
            "person_email": "p0@org.test",
            "questionnaire_version": "50", "language": "fr",
        })
        self.assertRedirects(response, reverse("survey:dashboard"))

    def test_send_questionnaire_new_person_blocked_over_quota(self):
        # Créer une personne à la volée via l'envoi compte dans le quota
        self._fill_person_quota()
        response = self.client.post(reverse("survey:send"), {
            "person_email": "nouveau@org.test",
            "first_name": "Nouveau", "last_name": "Venu",
            "questionnaire_version": "50", "language": "fr",
        })
        self.assertRedirects(response, reverse("accounts:billing_settings"))
        self.assertFalse(Person.objects.filter(email="nouveau@org.test").exists())

    def test_person_create_blocked_over_quota(self):
        self._fill_person_quota()
        response = self.client.post(reverse("teams:person_create"), {
            "first_name": "Trop", "last_name": "Plein", "email": "trop@org.test",
            "person_type": "candidate",
        })
        self.assertRedirects(response, reverse("accounts:billing_settings"))
        self.assertFalse(Person.objects.filter(email="trop@org.test").exists())


class BillingSettingsViewTests(TestCase):
    def setUp(self):
        self.org, self.rh_user = create_org_and_user(email="rh@org.test")
        self.manager_user = User.objects.create_user(
            email="manager@org.test", password="test-password",
            first_name="M", last_name="U", org=self.org, role=User.Role.MANAGER,
        )
        Subscription.start_free_plan(self.org)

    def test_manager_forbidden(self):
        self.client.force_login(self.manager_user)
        response = self.client.get(reverse("accounts:billing_settings"))
        self.assertEqual(response.status_code, 403)

    def test_rh_sees_free_plan_status_and_price(self):
        self.client.force_login(self.rh_user)
        response = self.client.get(reverse("accounts:billing_settings"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Plan gratuit")
        self.assertContains(response, "39")
        self.assertNotContains(response, "Essai")

    def test_no_trial_wording_anywhere(self):
        # Le modèle freemium a remplacé l'essai 14 jours — aucune mention résiduelle
        self.client.force_login(self.rh_user)
        response = self.client.get(reverse("accounts:billing_settings"))
        self.assertNotContains(response, "14 jours")
        self.assertNotContains(response, "restant")

    @override_settings(STRIPE_SECRET_KEY="", STRIPE_PRICE_ID="")
    def test_not_configured_shows_notice_and_blocks_checkout(self):
        self.client.force_login(self.rh_user)
        response = self.client.get(reverse("accounts:billing_settings"))
        self.assertNotContains(response, "S'abonner")

        response = self.client.post(reverse("accounts:billing_checkout"))
        self.assertRedirects(response, reverse("accounts:billing_settings"))

    @override_settings(STRIPE_SECRET_KEY="sk_test_x", STRIPE_PRICE_ID="price_x")
    def test_checkout_redirects_to_stripe(self):
        self.client.force_login(self.rh_user)
        fake_session = MagicMock(url="https://checkout.stripe.com/session/xyz")
        with patch("apps.billing.stripe_client.create_checkout_session", return_value=fake_session) as mocked:
            response = self.client.post(reverse("accounts:billing_checkout"))
        mocked.assert_called_once()
        self.assertRedirects(response, "https://checkout.stripe.com/session/xyz", fetch_redirect_response=False)

    @override_settings(STRIPE_SECRET_KEY="sk_test_x", STRIPE_PRICE_ID="price_x")
    def test_portal_redirects_when_customer_exists(self):
        self.client.force_login(self.rh_user)
        sub = Subscription.objects.get(org=self.org)
        sub.stripe_customer_id = "cus_123"
        sub.save()
        fake_session = MagicMock(url="https://billing.stripe.com/session/abc")
        with patch("apps.billing.stripe_client.create_portal_session", return_value=fake_session) as mocked:
            response = self.client.post(reverse("accounts:billing_portal"))
        mocked.assert_called_once()
        self.assertRedirects(response, "https://billing.stripe.com/session/abc", fetch_redirect_response=False)


class StripeWebhookTests(TestCase):
    def setUp(self):
        self.org, self.user = create_org_and_user()
        self.sub = Subscription.start_free_plan(self.org)

    def _post_event(self, event):
        with patch("stripe.Webhook.construct_event", return_value=event):
            return self.client.post(
                reverse("stripe_webhook"), data=b"{}", content_type="application/json",
                HTTP_STRIPE_SIGNATURE="test-sig",
            )

    @override_settings(STRIPE_WEBHOOK_SECRET="whsec_test")
    def test_missing_secret_returns_503(self):
        with override_settings(STRIPE_WEBHOOK_SECRET=""):
            response = self.client.post(reverse("stripe_webhook"), data=b"{}", content_type="application/json")
        self.assertEqual(response.status_code, 503)

    @override_settings(STRIPE_WEBHOOK_SECRET="whsec_test")
    def test_checkout_completed_activates_subscription(self):
        event = {
            "type": "checkout.session.completed",
            "data": {"object": {
                "metadata": {"org_id": str(self.org.id)},
                "customer": "cus_123",
                "subscription": "sub_123",
            }},
        }
        response = self._post_event(event)
        self.assertEqual(response.status_code, 200)
        self.sub.refresh_from_db()
        self.assertEqual(self.sub.status, Subscription.Status.ACTIVE)
        self.assertEqual(self.sub.stripe_customer_id, "cus_123")
        self.assertEqual(self.sub.stripe_subscription_id, "sub_123")

    @override_settings(STRIPE_WEBHOOK_SECRET="whsec_test")
    def test_subscription_updated_syncs_status_and_period(self):
        self.sub.stripe_subscription_id = "sub_123"
        self.sub.save()
        period_end_ts = int(timezone.now().timestamp()) + 2592000
        event = {
            "type": "customer.subscription.updated",
            "data": {"object": {
                "id": "sub_123", "status": "past_due", "current_period_end": period_end_ts,
            }},
        }
        response = self._post_event(event)
        self.assertEqual(response.status_code, 200)
        self.sub.refresh_from_db()
        self.assertEqual(self.sub.status, Subscription.Status.PAST_DUE)
        self.assertIsNotNone(self.sub.current_period_end)

    @override_settings(STRIPE_WEBHOOK_SECRET="whsec_test")
    def test_stripe_trialing_status_treated_as_active(self):
        # Plus d'essai côté FitRadarHR : un essai configuré côté Stripe
        # équivaut à un abonnement actif
        self.sub.stripe_subscription_id = "sub_123"
        self.sub.save()
        event = {
            "type": "customer.subscription.updated",
            "data": {"object": {"id": "sub_123", "status": "trialing"}},
        }
        response = self._post_event(event)
        self.assertEqual(response.status_code, 200)
        self.sub.refresh_from_db()
        self.assertEqual(self.sub.status, Subscription.Status.ACTIVE)

    @override_settings(STRIPE_WEBHOOK_SECRET="whsec_test")
    def test_subscription_deleted_cancels(self):
        self.sub.stripe_subscription_id = "sub_123"
        self.sub.status = Subscription.Status.ACTIVE
        self.sub.save()
        event = {"type": "customer.subscription.deleted", "data": {"object": {"id": "sub_123"}}}
        response = self._post_event(event)
        self.assertEqual(response.status_code, 200)
        self.sub.refresh_from_db()
        self.assertEqual(self.sub.status, Subscription.Status.CANCELED)

    @override_settings(STRIPE_WEBHOOK_SECRET="whsec_test")
    def test_invalid_signature_returns_400(self):
        import stripe as stripe_module
        with patch("stripe.Webhook.construct_event", side_effect=stripe_module.error.SignatureVerificationError("bad", "sig")):
            response = self.client.post(
                reverse("stripe_webhook"), data=b"{}", content_type="application/json",
                HTTP_STRIPE_SIGNATURE="bad-sig",
            )
        self.assertEqual(response.status_code, 400)

    def test_get_not_allowed(self):
        response = self.client.get(reverse("stripe_webhook"))
        self.assertEqual(response.status_code, 405)


class CsvImportQuotaTests(TestCase):
    def setUp(self):
        self.org, self.user = create_org_and_user()
        Subscription.start_free_plan(self.org)

    def test_import_capped_by_remaining_quota(self):
        from apps.teams.csv_import import import_persons_csv
        import io

        # Déjà à 2 personnes du quota
        for i in range(quotas.FREE_MAX_PEOPLE - 2):
            Person.objects.create(org=self.org, email=f"existing{i}@org.test", first_name="E", last_name=str(i))

        csv_content = "first_name,last_name,email\n" + "".join(
            f"New{i},Person,new{i}@org.test\n" for i in range(5)
        )
        result = import_persons_csv(
            io.BytesIO(csv_content.encode()), self.org, self.user,
            max_new=quotas.remaining_quota(self.org, "person"),
        )
        self.assertEqual(result["created"], 2)
        self.assertEqual(result["skipped_quota"], 3)


class CrossOrgIsolationTests(TestCase):
    def test_subscription_scoped_per_org(self):
        org1, _ = create_org_and_user(name="Org 1", email="a@org1.test")
        org2, _ = create_org_and_user(name="Org 2", email="a@org2.test")
        sub1 = Subscription.start_free_plan(org1)
        sub2 = Subscription.start_free_plan(org2)
        self.assertNotEqual(sub1.pk, sub2.pk)
        self.assertIn(sub1, Subscription.objects.for_org(org1))
        self.assertNotIn(sub2, Subscription.objects.for_org(org1))
