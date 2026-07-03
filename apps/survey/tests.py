"""Tests du scoring IPIP Big Five et du formulaire d'envoi."""
import secrets
from datetime import timedelta

from django.core import mail
from django.core.management import call_command
from django.test import SimpleTestCase, TestCase
from django.urls import reverse
from django.utils import timezone

from apps.fit.models import BigFiveProfile, BigFiveProfileHistory
from apps.teams.models import Person

from .ipip_data import DIMENSIONS, ITEMS
from .models import ConsentRecord, QuestionnaireLink, QuestionnaireSession
from .scoring import compute_scores, validate_answers


def _answers(direct_value, reversed_value):
    """Construit un jeu de réponses complet : `direct_value` pour les items
    en score direct (key=1), `reversed_value` pour les items inversés (key=-1)."""
    return {
        item["id"]: direct_value if item["key"] == 1 else reversed_value
        for item in ITEMS
    }


class ComputeScoresTests(SimpleTestCase):
    def test_maximum_profile(self):
        """5 sur les items directs + 1 sur les inversés → 100 partout."""
        scores = compute_scores(_answers(direct_value=5, reversed_value=1))
        for dim in DIMENSIONS:
            self.assertEqual(scores[dim], 100.0, dim)

    def test_minimum_profile(self):
        """1 sur les items directs + 5 sur les inversés → 0 partout."""
        scores = compute_scores(_answers(direct_value=1, reversed_value=5))
        for dim in DIMENSIONS:
            self.assertEqual(scores[dim], 0.0, dim)

    def test_neutral_profile(self):
        """3 partout → exactement 50 partout (items inversés compris)."""
        scores = compute_scores(_answers(direct_value=3, reversed_value=3))
        for dim in DIMENSIONS:
            self.assertEqual(scores[dim], 50.0, dim)

    def test_reversed_items_are_inverted(self):
        """Un item inversé doit compter 6 - réponse.

        E2 est inversé (key=-1) : répondre 1 ("pas du tout d'accord" à
        "Je ne parle pas beaucoup") doit AUGMENTER l'extraversion.
        """
        low = compute_scores({"E2": 5})
        high = compute_scores({"E2": 1})
        self.assertGreater(high["extraversion"], low["extraversion"])
        self.assertEqual(high["extraversion"], 100.0)
        self.assertEqual(low["extraversion"], 0.0)

    def test_no_answers_gives_neutral_50(self):
        scores = compute_scores({})
        for dim in DIMENSIONS:
            self.assertEqual(scores[dim], 50.0, dim)

    def test_invalid_values_are_ignored(self):
        """Les valeurs hors échelle 1–5 sont ignorées (dimension neutre)."""
        scores = compute_scores({"E1": 0, "E3": 6, "E4": 99})
        self.assertEqual(scores["extraversion"], 50.0)

    def test_partial_answers_normalized_on_answered_items(self):
        """E1 (direct) = 5 seul → (5-1)/4 × 100 = 100 sur les items répondus."""
        scores = compute_scores({"E1": 5})
        self.assertEqual(scores["extraversion"], 100.0)

    def test_scores_bounded_0_100(self):
        scores = compute_scores(_answers(5, 5))
        for dim in DIMENSIONS:
            self.assertGreaterEqual(scores[dim], 0.0)
            self.assertLessEqual(scores[dim], 100.0)


class ValidateAnswersTests(SimpleTestCase):
    def test_complete_valid_answers(self):
        self.assertEqual(validate_answers(_answers(3, 3), version="50"), [])

    def test_missing_answer_reported(self):
        answers = _answers(3, 3)
        del answers["O1"]
        self.assertEqual(validate_answers(answers, version="50"), ["O1"])

    def test_out_of_scale_answer_reported(self):
        answers = _answers(3, 3)
        answers["C3"] = 7
        self.assertEqual(validate_answers(answers, version="50"), ["C3"])


class IpipDataIntegrityTests(SimpleTestCase):
    def test_100_items_total_20_per_dimension(self):
        self.assertEqual(len(ITEMS), 100)
        for dim in DIMENSIONS:
            items = [i for i in ITEMS if i["dim"] == dim]
            self.assertEqual(len(items), 20, dim)

    def test_short_version_is_first_50_with_10_per_dimension(self):
        """ITEMS[:50] = version courte historique — ordre à ne jamais changer."""
        short = ITEMS[:50]
        self.assertEqual(len(short), 50)
        for dim in DIMENSIONS:
            items = [i for i in short if i["dim"] == dim]
            self.assertEqual(len(items), 10, dim)
        # Aucun item de l'extension (suffixes 11-20) dans la version courte
        for item in short:
            self.assertLessEqual(int(item["id"][1:]), 10, item["id"])

    def test_item_ids_unique(self):
        ids = [i["id"] for i in ITEMS]
        self.assertEqual(len(ids), len(set(ids)))

    def test_keys_valid(self):
        for item in ITEMS:
            self.assertIn(item["key"], (1, -1), item["id"])


class Version100Tests(SimpleTestCase):
    def test_validate_requires_all_100_items(self):
        answers = _answers(3, 3)  # complet (100 items)
        self.assertEqual(validate_answers(answers, version="100"), [])
        del answers["E20"]
        self.assertEqual(validate_answers(answers, version="100"), ["E20"])

    def test_validate_version_50_ignores_extension_items(self):
        """Un questionnaire 50 items ne doit exiger que les 50 premiers."""
        answers = {item["id"]: 3 for item in ITEMS[:50]}
        self.assertEqual(validate_answers(answers, version="50"), [])

    def test_scores_extreme_profiles_on_100_items(self):
        scores = compute_scores(_answers(direct_value=5, reversed_value=1))
        for dim in DIMENSIONS:
            self.assertEqual(scores[dim], 100.0, dim)
        scores = compute_scores(_answers(direct_value=3, reversed_value=3))
        for dim in DIMENSIONS:
            self.assertEqual(scores[dim], 50.0, dim)


class SendFormRenderingTests(TestCase):
    """La version et la langue doivent être des listes de choix, pas du texte libre."""

    def setUp(self):
        from core.testing import create_org_and_user

        self.org, self.user = create_org_and_user(email="rh@org.test")

    def test_version_and_language_rendered_as_selects(self):
        self.client.force_login(self.user)
        resp = self.client.get(reverse("survey:send"))
        self.assertEqual(resp.status_code, 200)
        content = resp.content.decode()
        self.assertIn('<select name="questionnaire_version"', content)
        self.assertIn('<select name="language"', content)
        # Les deux versions et les deux langues sont proposées
        self.assertIn('value="50"', content)
        self.assertIn('value="100"', content)
        self.assertIn('value="fr"', content)
        self.assertIn('value="en"', content)

    def test_invalid_version_rejected(self):
        """Une valeur hors liste (ex. 75) doit être refusée par le formulaire."""
        self.client.force_login(self.user)
        resp = self.client.post(reverse("survey:send"), {
            "person_email": "alice@org.test",
            "first_name": "Alice",
            "last_name": "A",
            "questionnaire_version": "75",
            "language": "fr",
        })
        self.assertEqual(resp.status_code, 200)  # re-render avec erreur
        self.assertTrue(resp.context["form"].errors.get("questionnaire_version"))


class RetakeArchivalTests(TestCase):
    """Re-passation & suivi longitudinal — item #5 de la roadmap V2.

    Une nouvelle passation ne doit jamais écraser silencieusement le profil
    précédent : il doit être archivé dans `BigFiveProfileHistory` avant d'être
    remplacé, pour permettre le suivi de l'évolution dans le temps.
    """

    def setUp(self):
        from core.testing import create_org_and_user

        self.org, self.user = create_org_and_user(email="rh@org.test")
        self.person = Person.objects.create(
            org=self.org, email="candidate@org.test",
            first_name="Cam", last_name="Didate", created_by=self.user,
        )

    def _submit_via_link(self, direct_value, reversed_value):
        link = QuestionnaireLink.objects.create(
            org=self.org, person=self.person,
            token=secrets.token_urlsafe(32),
            sent_by=self.user,
            status=QuestionnaireLink.Status.IN_PROGRESS,
            expires_at=timezone.now() + timedelta(days=7),
        )
        ConsentRecord.objects.create(link=link, ip_address="127.0.0.1", language="fr")
        answers = _answers(direct_value, reversed_value)
        QuestionnaireSession.objects.create(link=link, answers=answers)
        resp = self.client.get(reverse("survey:submit", kwargs={"token": link.token}))
        self.assertRedirects(resp, reverse("survey:done", kwargs={"token": link.token}))
        return link

    def test_first_submission_creates_no_history(self):
        self._submit_via_link(direct_value=5, reversed_value=1)
        profile = BigFiveProfile.objects.get(person=self.person)
        self.assertEqual(profile.openness, 100)
        self.assertEqual(BigFiveProfileHistory.objects.filter(person=self.person).count(), 0)

    def test_second_submission_archives_previous_profile(self):
        self._submit_via_link(direct_value=5, reversed_value=1)  # profil initial : 100 partout
        self._submit_via_link(direct_value=1, reversed_value=5)  # re-passation : 0 partout

        history = BigFiveProfileHistory.objects.filter(person=self.person)
        self.assertEqual(history.count(), 1)
        self.assertEqual(history.first().openness, 100)  # ancien profil archivé tel quel

        current = BigFiveProfile.objects.get(person=self.person)
        self.assertEqual(current.openness, 0)  # profil courant mis à jour

    def test_third_submission_archives_second_profile_too(self):
        self._submit_via_link(direct_value=5, reversed_value=1)
        self._submit_via_link(direct_value=1, reversed_value=5)
        self._submit_via_link(direct_value=3, reversed_value=3)

        history = BigFiveProfileHistory.objects.filter(person=self.person).order_by("archived_at")
        self.assertEqual(history.count(), 2)
        self.assertEqual([h.openness for h in history], [100, 0])

        current = BigFiveProfile.objects.get(person=self.person)
        self.assertEqual(current.openness, 50)


class SendRemindersCommandTests(TestCase):
    """Item #1 de la roadmap V2 : relance à J+3 des questionnaires non complétés."""

    def setUp(self):
        from apps.teams.models import Person
        from core.testing import create_org_and_user

        self.org, self.user = create_org_and_user(email="rh@org.test")
        self.person = Person.objects.create(
            org=self.org, email="candidate@org.test",
            first_name="Cam", last_name="Didate", created_by=self.user,
        )

    def _make_link(self, days_ago, status=QuestionnaireLink.Status.PENDING, reminder_sent=False):
        now = timezone.now()
        link = QuestionnaireLink.objects.create(
            org=self.org, person=self.person,
            token=secrets.token_urlsafe(32),
            sent_by=self.user,
            status=status,
            expires_at=now + timedelta(days=7 - days_ago),
            reminder_sent_at=now if reminder_sent else None,
        )
        # sent_at a `auto_now_add=True` — .update() contourne le save() pour
        # simuler un envoi passé sans que Django ne le réécrive à "maintenant".
        QuestionnaireLink.objects.filter(pk=link.pk).update(sent_at=now - timedelta(days=days_ago))
        link.refresh_from_db()
        return link

    def test_reminder_sent_for_pending_link_older_than_3_days(self):
        link = self._make_link(days_ago=4)
        call_command("send_reminders")
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ["candidate@org.test"])
        link.refresh_from_db()
        self.assertIsNotNone(link.reminder_sent_at)

    def test_no_reminder_for_recent_link(self):
        self._make_link(days_ago=1)
        call_command("send_reminders")
        self.assertEqual(len(mail.outbox), 0)

    def test_no_reminder_sent_twice(self):
        self._make_link(days_ago=5, reminder_sent=True)
        call_command("send_reminders")
        self.assertEqual(len(mail.outbox), 0)

    def test_no_reminder_for_completed_link(self):
        self._make_link(days_ago=4, status=QuestionnaireLink.Status.COMPLETED)
        call_command("send_reminders")
        self.assertEqual(len(mail.outbox), 0)

    def test_no_reminder_for_expired_link(self):
        # sent_at 10 jours dans le passé avec une validité de 7 jours → expiré
        now = timezone.now()
        link = QuestionnaireLink.objects.create(
            org=self.org, person=self.person,
            token=secrets.token_urlsafe(32),
            sent_by=self.user,
            status=QuestionnaireLink.Status.PENDING,
            expires_at=now - timedelta(days=3),
        )
        QuestionnaireLink.objects.filter(pk=link.pk).update(sent_at=now - timedelta(days=10))
        call_command("send_reminders")
        self.assertEqual(len(mail.outbox), 0)

    def test_no_reminder_for_demo_org(self):
        self.org.is_demo = True
        self.org.save()
        self._make_link(days_ago=4)
        call_command("send_reminders")
        self.assertEqual(len(mail.outbox), 0)

    def test_dry_run_does_not_send_email(self):
        self._make_link(days_ago=4)
        call_command("send_reminders", "--dry-run")
        self.assertEqual(len(mail.outbox), 0)

    def test_in_progress_link_also_reminded(self):
        self._make_link(days_ago=4, status=QuestionnaireLink.Status.IN_PROGRESS)
        call_command("send_reminders")
        self.assertEqual(len(mail.outbox), 1)
