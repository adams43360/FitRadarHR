"""Tests du scoring IPIP Big Five et du formulaire d'envoi."""
from django.test import SimpleTestCase, TestCase
from django.urls import reverse

from .ipip_data import DIMENSIONS, ITEMS
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
