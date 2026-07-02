"""Tests du scoring IPIP Big Five (fonctions pures, sans base de données)."""
from django.test import SimpleTestCase

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
    def test_each_dimension_has_10_items(self):
        for dim in DIMENSIONS:
            items = [i for i in ITEMS if i["dim"] == dim]
            self.assertEqual(len(items), 10, dim)

    def test_item_ids_unique(self):
        ids = [i["id"] for i in ITEMS]
        self.assertEqual(len(ids), len(set(ids)))

    def test_keys_valid(self):
        for item in ITEMS:
            self.assertIn(item["key"], (1, -1), item["id"])
