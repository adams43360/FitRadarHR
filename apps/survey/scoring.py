"""
Algorithme de scoring Big Five — version v1.0
Source items : IPIP Big Five Markers, 50 ou 100 items (Goldberg, 1992) — domaine public

Entrée : dict {item_id: raw_score}  (raw_score ∈ {1, 2, 3, 4, 5})
Sortie : dict {dimension: score_0_100}
"""

from .ipip_data import ITEMS, DIMENSIONS

ALGORITHM_VERSION = "v1.0"


def compute_scores(answers: dict) -> dict:
    """
    Calcule les 5 scores OCEAN normalisés sur 0–100.

    Args:
        answers: {"E1": 4, "E2": 2, ...}

    Returns:
        {"openness": 72.5, "conscientiousness": 60.0, ...}
    """
    raw_sums = {dim: 0 for dim in DIMENSIONS}
    counts = {dim: 0 for dim in DIMENSIONS}

    for item in ITEMS:
        item_id = item["id"]
        raw = answers.get(item_id)
        if raw is None:
            continue

        raw = int(raw)
        if raw not in (1, 2, 3, 4, 5):
            continue

        adjusted = raw if item["key"] == 1 else (6 - raw)
        raw_sums[item["dim"]] += adjusted
        counts[item["dim"]] += 1

    scores = {}
    for dim in DIMENSIONS:
        n = counts[dim]
        if n == 0:
            scores[dim] = 50.0  # valeur neutre si aucune réponse
        else:
            # Normalise sur la plage théorique [n×1, n×5]
            score = (raw_sums[dim] - n) / (n * 4) * 100
            scores[dim] = round(max(0.0, min(100.0, score)), 2)

    return scores


def validate_answers(answers: dict, version: str = "50") -> list:
    """
    Vérifie que toutes les réponses requises sont présentes et valides.
    Retourne la liste des item_id manquants ou invalides.
    """
    from .ipip_data import ITEMS
    n_items = int(version)
    required_ids = {item["id"] for item in ITEMS[:n_items]}
    errors = []
    for item_id in required_ids:
        val = answers.get(item_id)
        if val is None or int(val) not in (1, 2, 3, 4, 5):
            errors.append(item_id)
    return errors
