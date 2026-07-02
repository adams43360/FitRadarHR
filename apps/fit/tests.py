"""Tests du moteur de calcul de Fit (E5).

Partie 1 : fonctions pures du moteur (sans base de données).
Partie 2 : orchestrateur compute_all_fits_for_person (avec base).
"""
from types import SimpleNamespace

from django.test import SimpleTestCase, TestCase

from core.testing import create_org_and_user, create_profile

from .engine import (
    DIMENSIONS,
    compute_all_fits_for_person,
    compute_position_fit,
    compute_team_fit,
    compute_team_profile,
)
from .models import PositionFitResult, TeamFitResult


def fake_profile(**scores):
    """Profil factice — le moteur n'utilise que getattr(profile, dim)."""
    values = {dim: 50.0 for dim in DIMENSIONS}
    values.update(scores)
    return SimpleNamespace(**values)


def fake_position_profile(min_=0, max_=100, **overrides):
    """Profil de poste factice : plage [min_, max_] pour toutes les dimensions,
    surchargeable par dimension via openness_min=..., openness_max=...."""
    values = {}
    for dim in DIMENSIONS:
        values[f"{dim}_min"] = min_
        values[f"{dim}_max"] = max_
    values.update(overrides)
    return SimpleNamespace(**values)


class ComputePositionFitTests(SimpleTestCase):
    def test_score_in_range_gives_100(self):
        result = compute_position_fit(fake_profile(), fake_position_profile(30, 70))
        for dim in DIMENSIONS:
            self.assertEqual(result[dim], 100.0, dim)
        self.assertEqual(result["overall"], 100.0)

    def test_score_below_min_linear_penalty(self):
        """1 point de pénalité par point sous le min : 20 vs min 50 → 70."""
        profile = fake_profile(openness=20.0)
        result = compute_position_fit(profile, fake_position_profile(50, 70))
        self.assertEqual(result["openness"], 70.0)

    def test_score_above_max_linear_penalty(self):
        """90 vs max 60 → 100 - 30 = 70."""
        profile = fake_profile(openness=90.0)
        result = compute_position_fit(profile, fake_position_profile(0, 60))
        self.assertEqual(result["openness"], 70.0)

    def test_fit_clamped_at_zero(self):
        """Écart > 100 points → 0, jamais négatif."""
        profile = fake_profile(openness=0.0)
        pos = fake_position_profile(0, 100, openness_min=100, openness_max=100)
        result = compute_position_fit(profile, pos)
        self.assertEqual(result["openness"], 0.0)

    def test_boundaries_inclusive(self):
        profile = fake_profile(openness=30.0, extraversion=70.0)
        result = compute_position_fit(profile, fake_position_profile(30, 70))
        self.assertEqual(result["openness"], 100.0)
        self.assertEqual(result["extraversion"], 100.0)

    def test_overall_is_mean_of_dimensions(self):
        profile = fake_profile(openness=20.0)  # 70, les 4 autres 100
        result = compute_position_fit(profile, fake_position_profile(50, 70))
        self.assertEqual(result["overall"], round((70 + 100 * 4) / 5, 2))


class ComputeTeamProfileTests(SimpleTestCase):
    def test_empty_team_returns_none(self):
        self.assertIsNone(compute_team_profile([]))

    def test_averages_and_std_devs(self):
        profiles = [fake_profile(openness=40.0), fake_profile(openness=60.0)]
        data = compute_team_profile(profiles)
        self.assertEqual(data["n"], 2)
        self.assertEqual(data["averages"]["openness"], 50.0)
        self.assertEqual(data["std_devs"]["openness"], 10.0)  # écart-type population
        self.assertEqual(data["std_devs"]["extraversion"], 0.0)

    def test_single_member(self):
        data = compute_team_profile([fake_profile(openness=72.0)])
        self.assertEqual(data["averages"]["openness"], 72.0)
        self.assertEqual(data["std_devs"]["openness"], 0.0)


class ComputeTeamFitTests(SimpleTestCase):
    def _team_data(self, avg=50.0, std=0.0):
        return {
            "averages": {dim: avg for dim in DIMENSIONS},
            "std_devs": {dim: std for dim in DIMENSIONS},
            "n": 3,
        }

    def test_identical_profile_gives_100_similar(self):
        result = compute_team_fit(fake_profile(), self._team_data(avg=50.0))
        for dim in DIMENSIONS:
            self.assertEqual(result[dim], 100.0)
            self.assertEqual(result["complementarity"][dim], "similar")
        self.assertEqual(result["overall"], 100.0)

    def test_penalty_is_half_of_distance(self):
        """Écart de 40 points → fit = 100 - 40×0.5 = 80."""
        result = compute_team_fit(fake_profile(openness=90.0), self._team_data(avg=50.0))
        self.assertEqual(result["openness"], 80.0)

    def test_complementary_when_team_homogeneous(self):
        """Écart > 20 + équipe homogène (std < 15) → complémentaire."""
        result = compute_team_fit(
            fake_profile(openness=90.0), self._team_data(avg=50.0, std=5.0)
        )
        self.assertEqual(result["complementarity"]["openness"], "complementary")

    def test_different_when_team_heterogeneous(self):
        """Écart > 20 mais équipe déjà hétérogène (std ≥ 15) → différent."""
        result = compute_team_fit(
            fake_profile(openness=90.0), self._team_data(avg=50.0, std=20.0)
        )
        self.assertEqual(result["complementarity"]["openness"], "different")

    def test_threshold_boundary_is_similar(self):
        """Écart exactement égal au seuil (20) → similaire."""
        result = compute_team_fit(
            fake_profile(openness=70.0), self._team_data(avg=50.0, std=5.0)
        )
        self.assertEqual(result["complementarity"]["openness"], "similar")


class ComputeAllFitsForPersonTests(TestCase):
    """Tests d'intégration de l'orchestrateur (avec base)."""

    def setUp(self):
        from apps.positions.models import Position, PositionProfile
        from apps.teams.models import Person, Team, TeamMembership

        self.org, self.user = create_org_and_user(email="rh@org1.test")
        self.alice = Person.objects.create(
            org=self.org, email="alice@org1.test", first_name="Alice", last_name="A"
        )
        self.alice_profile = create_profile(self.alice, o=60)

        # Poste actif avec profil cible
        self.position = Position.objects.create(
            org=self.org, title_fr="Dev", created_by=self.user
        )
        PositionProfile.objects.create(position=self.position)  # plages 0-100

        # Poste sans profil cible → doit être ignoré
        self.position_no_profile = Position.objects.create(
            org=self.org, title_fr="Sans profil", created_by=self.user
        )

        # Équipe avec un autre membre profilé (Bob) + Alice
        self.team = Team.objects.create(org=self.org, name="Équipe 1")
        self.bob = Person.objects.create(
            org=self.org, email="bob@org1.test", first_name="Bob", last_name="B"
        )
        create_profile(self.bob, o=40)
        TeamMembership.objects.create(team=self.team, person=self.bob, added_by=self.user)
        TeamMembership.objects.create(team=self.team, person=self.alice, added_by=self.user)

        # Équipe vide → pas de fit possible
        self.empty_team = Team.objects.create(org=self.org, name="Équipe vide")

    def test_position_fits_created_for_positions_with_profile(self):
        compute_all_fits_for_person(self.alice)
        fit = PositionFitResult.objects.get(person=self.alice, position=self.position)
        self.assertEqual(float(fit.overall_fit), 100.0)  # plages 0-100
        self.assertFalse(
            PositionFitResult.objects.filter(
                person=self.alice, position=self.position_no_profile
            ).exists()
        )

    def test_team_fit_created_and_empty_team_skipped(self):
        compute_all_fits_for_person(self.alice)
        fit = TeamFitResult.objects.get(person=self.alice, team=self.team)
        # Bob openness=40, Alice openness=60 → écart 20 → fit 90 ; autres dims 100
        self.assertEqual(float(fit.openness_fit), 90.0)
        self.assertEqual(fit.team_size_at_computation, 1)
        self.assertFalse(
            TeamFitResult.objects.filter(person=self.alice, team=self.empty_team).exists()
        )

    def test_teammates_recomputed(self):
        """Le fit des coéquipiers doit être recalculé quand un profil arrive."""
        compute_all_fits_for_person(self.alice)
        self.assertTrue(
            TeamFitResult.objects.filter(person=self.bob, team=self.team).exists()
        )

    def test_person_without_profile_is_noop(self):
        from apps.teams.models import Person

        carol = Person.objects.create(
            org=self.org, email="carol@org1.test", first_name="Carol", last_name="C"
        )
        compute_all_fits_for_person(carol)  # ne doit pas lever
        self.assertFalse(PositionFitResult.objects.filter(person=carol).exists())

    def test_no_cross_org_fit(self):
        """Les fits ne doivent jamais traverser les organisations."""
        from apps.positions.models import Position, PositionProfile

        org2, user2 = create_org_and_user(name="Org 2", email="rh@org2.test")
        pos2 = Position.objects.create(org=org2, title_fr="Poste org2", created_by=user2)
        PositionProfile.objects.create(position=pos2)

        compute_all_fits_for_person(self.alice)
        self.assertFalse(
            PositionFitResult.objects.filter(person=self.alice, position=pos2).exists()
        )
