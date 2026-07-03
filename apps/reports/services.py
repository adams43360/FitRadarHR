"""Construction des contextes de rapport — partagée entre vues HTML et exports PDF.

Chaque rapport existe en deux rendus (page HTML et PDF WeasyPrint) qui
partagent les mêmes données : ces builders sont l'unique source de vérité.
"""
import json

from django.utils.translation import gettext_lazy as _

from apps.fit.engine import DIMENSION_LABELS, DIMENSIONS, compute_team_profile
from apps.teams.models import TeamMembership

from apps.fit.models import BigFiveProfileHistory

from .insights import (
    DIMENSION_TOOLTIPS,
    get_position_exploration_points,
    get_team_exploration_points,
)
from .models import AuditLog

SIGNAL_LABELS = {
    "similar": _("Similaire"),
    "different": _("Différent"),
    "complementary": _("Complémentaire"),
}
SIGNAL_COLORS = {
    "similar": "bg-blue-100 text-blue-800",
    "different": "bg-yellow-100 text-yellow-800",
    "complementary": "bg-green-100 text-green-800",
}


def audit(request, action, entity_type, entity_id, **metadata):
    """Trace une consultation/export dans le journal d'audit (EU AI Act)."""
    AuditLog.objects.create(
        org=request.user.org,
        user=request.user,
        action=action,
        entity_type=entity_type,
        entity_id=entity_id,
        metadata=metadata or None,
    )


def get_lang(request):
    return getattr(request, "LANGUAGE_CODE", "fr")[:2]


def dim_labels(lang):
    return [DIMENSION_LABELS[d][lang] for d in DIMENSIONS]


def person_scores(profile):
    return [float(getattr(profile, d)) for d in DIMENSIONS]


def active_member_profiles(team, exclude_person):
    """Profils Big Five des membres actifs d'une équipe, hors `exclude_person`."""
    return [
        m.person.big_five_profile
        for m in TeamMembership.objects
            .filter(team=team, left_at__isnull=True)
            .exclude(person=exclude_person)
            .select_related("person__big_five_profile")
        if hasattr(m.person, "big_five_profile")
    ]


# ──────────────────────────────────────────────────────────────────────────────
# Contextes de rapport
# ──────────────────────────────────────────────────────────────────────────────

def build_person_profile_evolution(person, profile, lang):
    """Item #5 roadmap V2 — historique des passations pour le suivi longitudinal.

    Renvoie les données pour le graphique d'évolution (une passation courante ne
    donne rien à afficher : `show_history` reste False dans ce cas) et pour le
    tableau détaillé, du plus ancien au plus récent (le profil courant en dernier).
    """
    history_qs = person.profile_history.order_by("computed_at")
    points = list(history_qs) + [profile]

    history_labels = [p.computed_at.strftime("%d/%m/%Y") for p in points]
    history_series = {d: [float(getattr(p, d)) for p in points] for d in DIMENSIONS}
    history_table = [
        {
            "computed_at": p.computed_at,
            "cells": [float(getattr(p, d)) for d in DIMENSIONS],
            "is_current": p is profile,
        }
        for p in points
    ]
    return {
        "show_history": len(points) > 1,
        "history_labels_json": json.dumps(history_labels),
        "history_series_json": json.dumps(history_series),
        "history_table": history_table,
    }


def build_person_profile_context(person, profile, lang):
    scores = person_scores(profile)
    dim_details = [
        {
            "dim_key": d,
            "label": DIMENSION_LABELS[d][lang],
            "score": scores[i],
            "tooltip": DIMENSION_TOOLTIPS[d][lang],
        }
        for i, d in enumerate(DIMENSIONS)
    ]
    context = {
        "person": person,
        "profile": profile,
        "lang": lang,
        "dim_details": dim_details,
        "chart_labels_json": json.dumps(dim_labels(lang)),
        "chart_scores_json": json.dumps(scores),
    }
    context.update(build_person_profile_evolution(person, profile, lang))
    return context


def build_position_fit_context(person, position, fit, lang):
    profile = person.big_five_profile
    scores = person_scores(profile)
    pos_min = [getattr(position.profile, f"{d}_min") for d in DIMENSIONS]
    pos_max = [getattr(position.profile, f"{d}_max") for d in DIMENSIONS]
    pos_mid = [round((mn + mx) / 2, 1) for mn, mx in zip(pos_min, pos_max)]

    dim_details = [
        {
            "dim_key": d,
            "label": DIMENSION_LABELS[d][lang],
            "tooltip": DIMENSION_TOOLTIPS[d][lang],
            "score": scores[i],
            "min": pos_min[i],
            "max": pos_max[i],
            "fit": float(getattr(fit, f"{d}_fit")),
            "in_range": pos_min[i] <= scores[i] <= pos_max[i],
        }
        for i, d in enumerate(DIMENSIONS)
    ]
    return {
        "person": person,
        "position": position,
        "fit": fit,
        "lang": lang,
        "dim_details": dim_details,
        "exploration_points": get_position_exploration_points(dim_details, lang),
        "chart_labels_json": json.dumps(dim_labels(lang)),
        "person_scores_json": json.dumps(scores),
        "pos_min_json": json.dumps(pos_min),
        "pos_max_json": json.dumps(pos_max),
        "pos_mid_json": json.dumps(pos_mid),
    }


def build_person_position_ranking_context(person, lang, department_id=None):
    """Item #1 roadmap V3 — fit inversé : classement des postes actifs les
    mieux adaptés à une personne (au lieu de choisir un poste puis classer les
    personnes, on part de la personne). S'appuie entièrement sur les
    `PositionFitResult` déjà calculés par `compute_all_fits_for_person` —
    aucune nouvelle donnée, aucun nouveau calcul, juste une vue différente.
    """
    qs = (
        person.position_fits
        .select_related("position__department", "position__team")
        .order_by("-overall_fit")
    )
    if department_id:
        qs = qs.filter(position__department_id=department_id)

    from apps.departments.models import Department
    departments = Department.objects.for_org(person.org).active()

    return {
        "person": person,
        "lang": lang,
        "position_fits": qs,
        "departments": departments,
        "department_filter": str(department_id) if department_id else "",
    }


def build_team_fit_context(person, team, fit, lang):
    profile = person.big_five_profile
    scores = person_scores(profile)

    # Recalcule le profil agrégé de l'équipe pour l'affichage
    team_data = compute_team_profile(active_member_profiles(team, exclude_person=person))
    team_avgs = [team_data["averages"][d] if team_data else 50.0 for d in DIMENSIONS]
    complementarity = fit.complementarity

    dim_details = [
        {
            "dim_key": d,
            "label": DIMENSION_LABELS[d][lang],
            "tooltip": DIMENSION_TOOLTIPS[d][lang],
            "score": scores[i],
            "team_avg": team_avgs[i],
            "fit": float(getattr(fit, f"{d}_fit")),
            "signal": complementarity.get(d, "similar"),
            "signal_label": SIGNAL_LABELS.get(complementarity.get(d, "similar"), ""),
            "signal_color": SIGNAL_COLORS.get(complementarity.get(d, "similar"), ""),
        }
        for i, d in enumerate(DIMENSIONS)
    ]
    return {
        "person": person,
        "team": team,
        "fit": fit,
        "lang": lang,
        "dim_details": dim_details,
        "exploration_points": get_team_exploration_points(dim_details, lang),
        "chart_labels_json": json.dumps(dim_labels(lang)),
        "person_scores_json": json.dumps(scores),
        "team_avgs_json": json.dumps(team_avgs),
        "team_size": fit.team_size_at_computation,
    }
