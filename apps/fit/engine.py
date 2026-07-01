"""
Moteur de calcul Fit — version v1.0

Deux types de fit :
  - Fit Poste  : proximité entre le profil OCEAN d'une personne et la plage cible [min, max] d'un poste
  - Fit Équipe : proximité entre le profil OCEAN d'une personne et le profil agrégé d'une équipe,
                 avec signal de complémentarité

Scoring :
  - Chaque dimension produit un score 0–100
  - Le score global est la moyenne arithmétique des 5 dimensions
  - Les scores sont tracés avec algorithm_version pour audit EU AI Act
"""

ALGORITHM_VERSION = "v1.0"
DIMENSIONS = ["openness", "conscientiousness", "extraversion", "agreeableness", "neuroticism"]

# Seuils pour les signaux de complémentarité (fit équipe)
COMPLEMENTARITY_DIFF_THRESHOLD = 20   # écart > 20 pts → "different" ou "complementary"
HOMOGENEITY_STD_THRESHOLD = 15        # std_dev < 15 → équipe homogène sur cette dimension


# ──────────────────────────────────────────────────────────────────────────────
# Fit Poste
# ──────────────────────────────────────────────────────────────────────────────

def compute_position_fit(profile, position_profile):
    """
    Calcule le fit entre un BigFiveProfile et un PositionProfile.

    Algorithme :
      - Si score ∈ [min, max] → fit = 100
      - Si score < min → fit = max(0, 100 - (min - score))
      - Si score > max → fit = max(0, 100 - (score - max))
      Pénalité linéaire de 1 point par point d'écart hors plage.

    Returns: dict {dim: fit_score, "overall": mean_fit}
    """
    dim_fits = {}
    for dim in DIMENSIONS:
        score = float(getattr(profile, dim))
        dim_min = getattr(position_profile, f"{dim}_min")
        dim_max = getattr(position_profile, f"{dim}_max")

        if dim_min <= score <= dim_max:
            fit = 100.0
        elif score < dim_min:
            fit = max(0.0, 100.0 - (dim_min - score))
        else:
            fit = max(0.0, 100.0 - (score - dim_max))

        dim_fits[dim] = round(fit, 2)

    dim_fits["overall"] = round(sum(v for k, v in dim_fits.items()) / len(DIMENSIONS), 2)
    return dim_fits


# ──────────────────────────────────────────────────────────────────────────────
# Fit Équipe
# ──────────────────────────────────────────────────────────────────────────────

def compute_team_profile(member_profiles):
    """
    Calcule le profil agrégé d'une équipe (moyenne + écart-type par dimension).

    Args:
        member_profiles: list de BigFiveProfile

    Returns:
        {"averages": {dim: float}, "std_devs": {dim: float}, "n": int}
        ou None si la liste est vide
    """
    if not member_profiles:
        return None

    n = len(member_profiles)
    averages = {}
    std_devs = {}

    for dim in DIMENSIONS:
        scores = [float(getattr(p, dim)) for p in member_profiles]
        avg = sum(scores) / n
        variance = sum((s - avg) ** 2 for s in scores) / n
        averages[dim] = round(avg, 2)
        std_devs[dim] = round(variance ** 0.5, 2)

    return {"averages": averages, "std_devs": std_devs, "n": n}


def compute_team_fit(profile, team_profile_data):
    """
    Calcule le fit entre un BigFiveProfile et le profil agrégé d'une équipe.

    Algorithme :
      - fit_dim = max(0, 100 - |score - avg| × 0.5)
        (pénalité moitié moins sévère que le fit poste — la similarité n'est pas une obligation)
      - Signal complémentarité :
          * "complementary" : écart > seuil ET équipe homogène (std_dev < seuil)
                              → la personne apporte de la diversité là où l'équipe est uniforme
          * "different"     : écart > seuil mais équipe déjà hétérogène
          * "similar"       : écart ≤ seuil

    Returns: dict {dim: fit_score, "overall": mean_fit, "complementarity": {dim: signal}}
    """
    averages = team_profile_data["averages"]
    std_devs = team_profile_data["std_devs"]

    dim_fits = {}
    complementarity = {}

    for dim in DIMENSIONS:
        score = float(getattr(profile, dim))
        avg = averages[dim]
        std_dev = std_devs[dim]
        diff = abs(score - avg)

        fit = max(0.0, 100.0 - diff * 0.5)
        dim_fits[dim] = round(fit, 2)

        if diff > COMPLEMENTARITY_DIFF_THRESHOLD and std_dev < HOMOGENEITY_STD_THRESHOLD:
            complementarity[dim] = "complementary"
        elif diff > COMPLEMENTARITY_DIFF_THRESHOLD:
            complementarity[dim] = "different"
        else:
            complementarity[dim] = "similar"

    dim_fits["overall"] = round(sum(v for k, v in dim_fits.items() if k != "complementarity") / len(DIMENSIONS), 2)
    dim_fits["complementarity"] = complementarity
    return dim_fits


# ──────────────────────────────────────────────────────────────────────────────
# Orchestrateur — déclenché après chaque profil sauvegardé
# ──────────────────────────────────────────────────────────────────────────────

def compute_all_fits_for_person(person):
    """
    Calcule (ou recalcule) tous les résultats de fit pour une personne.
    Appelé automatiquement après la complétion d'un questionnaire.

    - Fit Poste : tous les postes actifs de l'org ayant un profil cible
    - Fit Équipe : toutes les équipes de l'org ayant au moins 1 autre membre avec un profil
    """
    try:
        profile = person.big_five_profile
    except Exception:
        return  # pas encore de profil

    org = person.org

    _compute_position_fits(person, profile, org)
    _compute_team_fits(person, profile, org)


def _compute_position_fits(person, profile, org):
    from apps.positions.models import Position
    from .models import PositionFitResult

    active_positions = (
        Position.objects
        .filter(org=org, status=Position.Status.ACTIVE)
        .select_related("profile")
    )

    for position in active_positions:
        if not position.has_profile:
            continue

        result = compute_position_fit(profile, position.profile)

        PositionFitResult.objects.update_or_create(
            person=person,
            position=position,
            defaults={
                "person_profile": profile,
                "openness_fit": result["openness"],
                "conscientiousness_fit": result["conscientiousness"],
                "extraversion_fit": result["extraversion"],
                "agreeableness_fit": result["agreeableness"],
                "neuroticism_fit": result["neuroticism"],
                "overall_fit": result["overall"],
                "algorithm_version": ALGORITHM_VERSION,
            },
        )


def _compute_team_fits(person, profile, org):
    from apps.teams.models import Team, TeamMembership
    from .models import TeamFitResult

    teams = Team.objects.filter(org=org)

    for team in teams:
        # Membres actifs de l'équipe ayant un profil, hors la personne elle-même
        member_profiles = []
        memberships = (
            TeamMembership.objects
            .filter(team=team, left_at__isnull=True)
            .exclude(person=person)
            .select_related("person__big_five_profile")
        )
        for m in memberships:
            if hasattr(m.person, "big_five_profile"):
                member_profiles.append(m.person.big_five_profile)

        if not member_profiles:
            continue  # besoin d'au moins 1 autre membre avec profil

        team_data = compute_team_profile(member_profiles)
        result = compute_team_fit(profile, team_data)

        TeamFitResult.objects.update_or_create(
            person=person,
            team=team,
            defaults={
                "person_profile": profile,
                "openness_fit": result["openness"],
                "conscientiousness_fit": result["conscientiousness"],
                "extraversion_fit": result["extraversion"],
                "agreeableness_fit": result["agreeableness"],
                "neuroticism_fit": result["neuroticism"],
                "overall_fit": result["overall"],
                "complementarity": result["complementarity"],
                "team_size_at_computation": len(member_profiles),
                "algorithm_version": ALGORITHM_VERSION,
            },
        )
