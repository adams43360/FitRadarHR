"""Tests d'isolation multi-tenant, droits et audit — rapports."""
import uuid
from datetime import timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from apps.accounts.models import User
from apps.fit.models import BigFiveProfile
from apps.survey.models import QuestionnaireLink
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


class ProfileEvolutionTests(TestCase):
    """Suivi longitudinal — item #5 de la roadmap V2."""

    def setUp(self):
        from apps.fit.models import BigFiveProfileHistory

        self.BigFiveProfileHistory = BigFiveProfileHistory
        self.org, self.user = create_org_and_user(email="rh@org.test")
        self.person = Person.objects.create(
            org=self.org, email="alice@org.test", first_name="Alice", last_name="A"
        )
        self.profile = create_profile(self.person)

    def test_no_history_by_default(self):
        self.client.force_login(self.user)
        resp = self.client.get(
            reverse("reports:person_profile", kwargs={"person_pk": self.person.pk})
        )
        self.assertEqual(resp.status_code, 200)
        self.assertFalse(resp.context["show_history"])
        self.assertNotContains(resp, "evolutionChart")

    def test_history_shown_after_archival(self):
        self.BigFiveProfileHistory.objects.create(
            person=self.person,
            openness=20, conscientiousness=20, extraversion=20,
            agreeableness=20, neuroticism=20,
            questionnaire_version="50", computed_at=self.profile.computed_at,
        )
        self.client.force_login(self.user)
        resp = self.client.get(
            reverse("reports:person_profile", kwargs={"person_pk": self.person.pk})
        )
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.context["show_history"])
        self.assertEqual(len(resp.context["history_table"]), 2)
        self.assertFalse(resp.context["history_table"][0]["is_current"])
        self.assertTrue(resp.context["history_table"][1]["is_current"])
        self.assertContains(resp, "evolutionChart")

    def test_history_strings_translated_to_english(self):
        """Le catalogue EN doit couvrir les nouvelles chaînes de l'évolution de
        profil (voir locale/en/LC_MESSAGES/django.po) — pas de régression bilingue."""
        from django.utils import translation
        with translation.override("en"):
            self.assertEqual(
                translation.gettext("Repasser le questionnaire"), "Retake questionnaire"
            )
            self.assertEqual(
                translation.gettext("Évolution du profil"), "Profile evolution"
            )
            self.assertEqual(translation.gettext("actuel"), "current")

    def test_pdf_renders_with_history(self):
        """L'export PDF ne doit pas planter quand un historique existe (item #5)."""
        self.BigFiveProfileHistory.objects.create(
            person=self.person,
            openness=30, conscientiousness=30, extraversion=30,
            agreeableness=30, neuroticism=30,
            questionnaire_version="50", computed_at=self.profile.computed_at,
        )
        self.client.force_login(self.user)
        resp = self.client.get(
            reverse("reports:person_profile_pdf", kwargs={"person_pk": self.person.pk})
        )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp["Content-Type"], "application/pdf")

    def test_history_isolated_by_tenant(self):
        """L'historique d'une personne d'une autre org ne doit jamais fuiter."""
        org2, user2 = create_org_and_user(name="Org 2", email="rh@org2.test")
        person2 = Person.objects.create(
            org=org2, email="bob@org2.test", first_name="Bob", last_name="B"
        )
        create_profile(person2)
        self.BigFiveProfileHistory.objects.create(
            person=person2,
            openness=10, conscientiousness=10, extraversion=10,
            agreeableness=10, neuroticism=10,
            questionnaire_version="50", computed_at=self.profile.computed_at,
        )
        # L'historique de person2 ne doit pas apparaître sur le rapport de self.person
        self.client.force_login(self.user)
        resp = self.client.get(
            reverse("reports:person_profile", kwargs={"person_pk": self.person.pk})
        )
        self.assertFalse(resp.context["show_history"])


class RetentionCohortTests(TestCase):
    """Cohortes de rétention mensuelles — item #6 de la roadmap V2."""

    def setUp(self):
        from apps.reports.analytics import _add_months

        self.add_months = _add_months
        self.org, self.rh = create_org_and_user(email="rh@cohort.test")
        self.now = timezone.now()
        self.current_month = self.now.replace(
            day=1, hour=0, minute=0, second=0, microsecond=0
        )
        self.cohort_a = self.add_months(self.current_month, -1)  # 1 mois avant "aujourd'hui"
        self.cohort_b = self.add_months(self.current_month, -3)  # 3 mois avant

        self.p1 = Person.objects.create(org=self.org, email="p1@cohort.test", first_name="P", last_name="1")
        self.p2 = Person.objects.create(org=self.org, email="p2@cohort.test", first_name="P", last_name="2")
        self.p3 = Person.objects.create(org=self.org, email="p3@cohort.test", first_name="P", last_name="3")

        self._complete_link(self.p1, self.cohort_a)
        self._complete_link(self.p2, self.cohort_a)
        self._complete_link(self.p3, self.cohort_b)

        # p1 consulté le mois de la cohorte ET le mois suivant (rétention pleine)
        self._view(self.p1, self.cohort_a)
        self._view(self.p1, self.add_months(self.cohort_a, 1))
        # p2 consulté seulement le mois de la cohorte (pas de rétention le mois suivant)
        self._view(self.p2, self.cohort_a)
        # p3 jamais consulté (rétention nulle sur toute la cohorte)

    def _complete_link(self, person, month_dt):
        QuestionnaireLink.objects.create(
            org=self.org, person=person, token=f"tok-{uuid.uuid4()}",
            sent_by=self.rh, expires_at=self.now + timedelta(days=7),
            status=QuestionnaireLink.Status.COMPLETED,
            completed_at=month_dt.replace(day=15),
        )

    def _view(self, person, month_dt):
        log = AuditLog.objects.create(
            org=self.org, user=self.rh, action="profile.viewed", entity_type="BigFiveProfile",
            entity_id=uuid.uuid4(), metadata={"person_id": str(person.id)},
        )
        AuditLog.objects.filter(pk=log.pk).update(created_at=month_dt.replace(day=20))

    def _cohort_row(self, ctx, label_month):
        label = label_month.strftime("%m/%Y")
        return next(r for r in ctx["retention_cohorts"] if r["label"] == label)

    def test_cohort_sizes(self):
        from apps.reports.analytics import build_analytics_context

        ctx = build_analytics_context(self.org)
        row_a = self._cohort_row(ctx, self.cohort_a)
        row_b = self._cohort_row(ctx, self.cohort_b)
        self.assertEqual(row_a["size"], 2)
        self.assertEqual(row_b["size"], 1)

    def test_retention_rates(self):
        from apps.reports.analytics import build_analytics_context

        ctx = build_analytics_context(self.org)
        row_a = self._cohort_row(ctx, self.cohort_a)
        # Offset 0 : p1 + p2 ont consulté → 100%
        self.assertEqual(row_a["cells"][0]["rate"], 100.0)
        # Offset 1 : seul p1 a consulté → 50%
        self.assertEqual(row_a["cells"][1]["rate"], 50.0)

        row_b = self._cohort_row(ctx, self.cohort_b)
        # p3 n'a jamais consulté son rapport
        self.assertEqual(row_b["cells"][0]["rate"], 0.0)

    def test_future_offsets_are_none(self):
        """Un mois pas encore atteint ne doit jamais afficher un taux (ni 0 %)."""
        from apps.reports.analytics import build_analytics_context

        ctx = build_analytics_context(self.org)
        row_a = self._cohort_row(ctx, self.cohort_a)
        # La cohorte A n'a que 2 mois d'existence (offset 0 et 1) : au-delà, None.
        self.assertIsNone(row_a["cells"][2])

    def test_retake_does_not_create_phantom_cohort(self):
        """Une re-passation ne doit pas faire apparaître une nouvelle cohorte
        pour une personne déjà activée avant la fenêtre d'affichage."""
        from apps.reports.analytics import build_analytics_context, RETENTION_MONTHS_WINDOW

        # p1 a en réalité été activé bien avant la fenêtre affichée...
        old_month = self.add_months(self.current_month, -(RETENTION_MONTHS_WINDOW + 3))
        self._complete_link(self.p1, old_month)
        # ... la re-passation plus récente (self.cohort_a) ne doit donc pas
        # recréer p1 dans la cohorte de self.cohort_a.
        ctx = build_analytics_context(self.org)
        row_a = self._cohort_row(ctx, self.cohort_a)
        self.assertEqual(row_a["size"], 1)  # seul p2 reste dans cette cohorte

    def test_tenant_isolation(self):
        other_org, other_rh = create_org_and_user(name="Autre org", email="rh@autre-cohort.test")
        from apps.reports.analytics import build_analytics_context

        ctx = build_analytics_context(other_org)
        self.assertEqual(ctx["retention_cohorts"], [])

    def test_analytics_page_renders_cohorts(self):
        self.client.force_login(self.rh)
        resp = self.client.get(reverse("reports:analytics"))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Cohortes de rétention")

    def test_cohort_strings_translated_to_english(self):
        """Le catalogue EN doit couvrir les nouvelles chaînes des cohortes de
        rétention (voir locale/en/LC_MESSAGES/django.po) — pas de régression bilingue."""
        from django.utils import translation
        with translation.override("en"):
            self.assertEqual(translation.gettext("Cohortes de rétention"), "Retention cohorts")
            self.assertEqual(translation.gettext("Cohorte"), "Cohort")
            self.assertEqual(
                translation.ngettext("%(n)s personne", "%(n)s personnes", 1) % {"n": 1},
                "1 person",
            )
            self.assertEqual(
                translation.ngettext("%(n)s personne", "%(n)s personnes", 3) % {"n": 3},
                "3 people",
            )


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


class AnalyticsTests(TestCase):
    """Page analytics : droits, calculs, isolation multi-tenant."""

    def setUp(self):
        from datetime import timedelta
        from django.utils import timezone
        from apps.survey.models import ConsentRecord, QuestionnaireLink

        self.org, self.rh = create_org_and_user(name="Org A", email="rh@orga.test")
        self.manager = User.objects.create_user(
            email="manager@orga.test", password="x",
            first_name="Man", last_name="Ager", org=self.org, role=User.Role.MANAGER,
        )
        self.org2, self.rh2 = create_org_and_user(name="Org B", email="rh@orgb.test")

        now = timezone.now()

        # Org A : 1 lien complété (avec consentement + profil), 1 lien en attente
        self.p1 = Person.objects.create(
            org=self.org, email="p1@orga.test", first_name="P", last_name="Un"
        )
        self.p2 = Person.objects.create(
            org=self.org, email="p2@orga.test", first_name="P", last_name="Deux"
        )
        completed = QuestionnaireLink.objects.create(
            org=self.org, person=self.p1, token="tok-completed",
            sent_by=self.rh, expires_at=now + timedelta(days=7),
            status=QuestionnaireLink.Status.COMPLETED,
            completed_at=now,
        )
        QuestionnaireLink.objects.filter(pk=completed.pk).update(
            sent_at=now - timedelta(days=2)
        )
        ConsentRecord.objects.create(link=completed, language="fr")
        create_profile(self.p1)
        QuestionnaireLink.objects.create(
            org=self.org, person=self.p2, token="tok-pending",
            sent_by=self.rh, expires_at=now + timedelta(days=7),
        )

        # Org B : du bruit qui ne doit pas fuiter dans les métriques d'Org A
        pb = Person.objects.create(
            org=self.org2, email="pb@orgb.test", first_name="P", last_name="B"
        )
        QuestionnaireLink.objects.create(
            org=self.org2, person=pb, token="tok-org2",
            sent_by=self.rh2, expires_at=now + timedelta(days=7),
        )
        create_profile(pb)

    def test_rh_can_access(self):
        self.client.force_login(self.rh)
        resp = self.client.get(reverse("reports:analytics"))
        self.assertEqual(resp.status_code, 200)

    def test_manager_forbidden(self):
        self.client.force_login(self.manager)
        resp = self.client.get(reverse("reports:analytics"))
        self.assertEqual(resp.status_code, 403)

    def test_anonymous_redirected(self):
        resp = self.client.get(reverse("reports:analytics"))
        self.assertEqual(resp.status_code, 302)

    def test_funnel_metrics(self):
        from apps.reports.analytics import build_analytics_context

        ctx = build_analytics_context(self.org)
        self.assertEqual(ctx["funnel"]["sent"], 2)
        self.assertEqual(ctx["funnel"]["started"], 1)
        self.assertEqual(ctx["funnel"]["completed"], 1)
        self.assertEqual(ctx["funnel"]["completion_rate"], 50.0)
        self.assertEqual(ctx["funnel"]["abandon_count"], 0)
        self.assertEqual(ctx["avg_delay_days"], 2.0)
        self.assertEqual(ctx["status_breakdown"]["pending"], 1)
        self.assertEqual(ctx["status_breakdown"]["completed"], 1)

    def test_coverage_and_split(self):
        from apps.reports.analytics import build_analytics_context

        ctx = build_analytics_context(self.org)
        self.assertEqual(ctx["profiles_count"], 1)
        self.assertEqual(ctx["coverage_rate"], 50.0)
        self.assertEqual(ctx["person_split"]["candidates"], 2)

    def test_tenant_isolation(self):
        """Les métriques d'Org A ne comptent jamais les données d'Org B."""
        from apps.reports.analytics import build_analytics_context

        ctx_a = build_analytics_context(self.org)
        ctx_b = build_analytics_context(self.org2)
        self.assertEqual(ctx_a["funnel"]["sent"], 2)
        self.assertEqual(ctx_b["funnel"]["sent"], 1)
        self.assertEqual(ctx_b["profiles_count"], 1)

    def test_empty_org_renders(self):
        """Une org sans aucune donnée doit afficher la page sans erreur."""
        org_empty, rh_empty = create_org_and_user(name="Vide", email="rh@vide.test")
        self.client.force_login(rh_empty)
        resp = self.client.get(reverse("reports:analytics"))
        self.assertEqual(resp.status_code, 200)
