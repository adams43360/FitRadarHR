import json

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render

from apps.fit.engine import DIMENSION_LABELS, DIMENSIONS, compute_team_profile
from apps.fit.models import BigFiveProfile, PositionFitResult, TeamFitResult
from apps.positions.models import Position
from apps.teams.models import Person, Team, TeamMembership

from .models import AuditLog


def _lang(request):
    return getattr(request, "LANGUAGE_CODE", "fr")[:2]


def _dim_labels(lang):
    return [DIMENSION_LABELS[d][lang] for d in DIMENSIONS]


# ──────────────────────────────────────────────────────────────────────────────
# Liste des rapports disponibles
# ──────────────────────────────────────────────────────────────────────────────

@login_required
def report_list(request):
    persons = (
        Person.objects
        .filter(org=request.user.org)
        .select_related("big_five_profile")
        .prefetch_related("position_fits__position", "team_fits__team")
        .order_by("last_name", "first_name")
    )
    persons_with_profile = [p for p in persons if hasattr(p, "big_five_profile")]
    return render(request, "reports/list.html", {"persons": persons_with_profile})


# ──────────────────────────────────────────────────────────────────────────────
# Profil Big Five individuel
# ──────────────────────────────────────────────────────────────────────────────

@login_required
def person_profile(request, person_pk):
    person = get_object_or_404(Person, pk=person_pk, org=request.user.org)
    profile = get_object_or_404(BigFiveProfile, person=person)
    lang = _lang(request)

    AuditLog.objects.create(
        org=request.user.org,
        user=request.user,
        action="profile.viewed",
        entity_type="BigFiveProfile",
        entity_id=profile.id,
        metadata={"person_id": str(person.id)},
    )

    chart_labels = _dim_labels(lang)
    chart_scores = [float(getattr(profile, d)) for d in DIMENSIONS]

    position_fits = person.position_fits.select_related("position").order_by("-overall_fit")
    team_fits = person.team_fits.select_related("team").order_by("-overall_fit")

    return render(request, "reports/person_profile.html", {
        "person": person,
        "profile": profile,
        "chart_labels_json": json.dumps(chart_labels),
        "chart_scores_json": json.dumps(chart_scores),
        "position_fits": position_fits,
        "team_fits": team_fits,
    })


# ──────────────────────────────────────────────────────────────────────────────
# Rapport Fit Poste
# ──────────────────────────────────────────────────────────────────────────────

@login_required
def position_fit_report(request, person_pk, position_pk):
    person = get_object_or_404(Person, pk=person_pk, org=request.user.org)
    position = get_object_or_404(Position, pk=position_pk, org=request.user.org)
    fit = get_object_or_404(PositionFitResult, person=person, position=position)
    profile = person.big_five_profile
    lang = _lang(request)

    AuditLog.objects.create(
        org=request.user.org,
        user=request.user,
        action="position_fit.viewed",
        entity_type="PositionFitResult",
        entity_id=fit.id,
        metadata={"person_id": str(person.id), "position_id": str(position.id)},
    )

    chart_labels = _dim_labels(lang)
    person_scores = [float(getattr(profile, d)) for d in DIMENSIONS]
    pos_min = [getattr(position.profile, f"{d}_min") for d in DIMENSIONS]
    pos_max = [getattr(position.profile, f"{d}_max") for d in DIMENSIONS]
    pos_mid = [round((mn + mx) / 2, 1) for mn, mx in zip(pos_min, pos_max)]

    dim_details = [
        {
            "label": DIMENSION_LABELS[d][lang],
            "score": person_scores[i],
            "min": pos_min[i],
            "max": pos_max[i],
            "fit": float(getattr(fit, f"{d}_fit")),
            "in_range": pos_min[i] <= person_scores[i] <= pos_max[i],
        }
        for i, d in enumerate(DIMENSIONS)
    ]

    return render(request, "reports/position_fit.html", {
        "person": person,
        "position": position,
        "fit": fit,
        "chart_labels_json": json.dumps(chart_labels),
        "person_scores_json": json.dumps(person_scores),
        "pos_min_json": json.dumps(pos_min),
        "pos_max_json": json.dumps(pos_max),
        "pos_mid_json": json.dumps(pos_mid),
        "dim_details": dim_details,
    })


# ──────────────────────────────────────────────────────────────────────────────
# Rapport Fit Équipe
# ──────────────────────────────────────────────────────────────────────────────

@login_required
def team_fit_report(request, person_pk, team_pk):
    person = get_object_or_404(Person, pk=person_pk, org=request.user.org)
    team = get_object_or_404(Team, pk=team_pk, org=request.user.org)
    fit = get_object_or_404(TeamFitResult, person=person, team=team)
    profile = person.big_five_profile
    lang = _lang(request)

    AuditLog.objects.create(
        org=request.user.org,
        user=request.user,
        action="team_fit.viewed",
        entity_type="TeamFitResult",
        entity_id=fit.id,
        metadata={"person_id": str(person.id), "team_id": str(team.id)},
    )

    # Recalcule le profil agrégé de l'équipe pour l'affichage
    member_profiles = [
        m.person.big_five_profile
        for m in TeamMembership.objects
            .filter(team=team, left_at__isnull=True)
            .exclude(person=person)
            .select_related("person__big_five_profile")
        if hasattr(m.person, "big_five_profile")
    ]
    team_data = compute_team_profile(member_profiles)

    chart_labels = _dim_labels(lang)
    person_scores = [float(getattr(profile, d)) for d in DIMENSIONS]
    team_avgs = [team_data["averages"][d] if team_data else 50.0 for d in DIMENSIONS]
    complementarity = fit.complementarity

    SIGNAL_LABELS = {
        "fr": {"similar": "Similaire", "different": "Différent", "complementary": "Complémentaire"},
        "en": {"similar": "Similar", "different": "Different", "complementary": "Complementary"},
    }
    SIGNAL_COLORS = {
        "similar": "bg-blue-100 text-blue-800",
        "different": "bg-yellow-100 text-yellow-800",
        "complementary": "bg-green-100 text-green-800",
    }

    dim_details = [
        {
            "label": DIMENSION_LABELS[d][lang],
            "score": person_scores[i],
            "team_avg": team_avgs[i],
            "fit": float(getattr(fit, f"{d}_fit")),
            "signal": complementarity.get(d, "similar"),
            "signal_label": SIGNAL_LABELS[lang].get(complementarity.get(d, "similar"), ""),
            "signal_color": SIGNAL_COLORS.get(complementarity.get(d, "similar"), ""),
        }
        for i, d in enumerate(DIMENSIONS)
    ]

    return render(request, "reports/team_fit.html", {
        "person": person,
        "team": team,
        "fit": fit,
        "chart_labels_json": json.dumps(chart_labels),
        "person_scores_json": json.dumps(person_scores),
        "team_avgs_json": json.dumps(team_avgs),
        "dim_details": dim_details,
        "team_size": fit.team_size_at_computation,
    })


# ──────────────────────────────────────────────────────────────────────────────
# Export PDF (WeasyPrint)
# ──────────────────────────────────────────────────────────────────────────────

def _render_pdf(template_name, context, filename):
    from django.http import HttpResponse
    from django.template.loader import render_to_string
    from weasyprint import HTML
    html_string = render_to_string(template_name, context)
    pdf = HTML(string=html_string).write_pdf()
    response = HttpResponse(pdf, content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="{filename}"'
    return response


@login_required
def person_profile_pdf(request, person_pk):
    person = get_object_or_404(Person, pk=person_pk, org=request.user.org)
    profile = get_object_or_404(BigFiveProfile, person=person)
    lang = _lang(request)

    AuditLog.objects.create(
        org=request.user.org, user=request.user,
        action="profile.exported_pdf", entity_type="BigFiveProfile",
        entity_id=profile.id, metadata={"person_id": str(person.id)},
    )

    chart_labels = _dim_labels(lang)
    scores = [float(getattr(profile, d)) for d in DIMENSIONS]
    dim_details = [
        {"label": DIMENSION_LABELS[d][lang], "score": scores[i]}
        for i, d in enumerate(DIMENSIONS)
    ]

    filename = f"profil-ocean_{person.last_name.lower()}_{person.first_name.lower()}.pdf"
    return _render_pdf("reports/pdf/person_profile.html", {
        "person": person, "profile": profile,
        "dim_details": dim_details, "lang": lang,
    }, filename)


@login_required
def position_fit_pdf(request, person_pk, position_pk):
    person = get_object_or_404(Person, pk=person_pk, org=request.user.org)
    position = get_object_or_404(Position, pk=position_pk, org=request.user.org)
    fit = get_object_or_404(PositionFitResult, person=person, position=position)
    profile = person.big_five_profile
    lang = _lang(request)

    AuditLog.objects.create(
        org=request.user.org, user=request.user,
        action="position_fit.exported_pdf", entity_type="PositionFitResult",
        entity_id=fit.id,
        metadata={"person_id": str(person.id), "position_id": str(position.id)},
    )

    person_scores = [float(getattr(profile, d)) for d in DIMENSIONS]
    pos_min = [getattr(position.profile, f"{d}_min") for d in DIMENSIONS]
    pos_max = [getattr(position.profile, f"{d}_max") for d in DIMENSIONS]
    dim_details = [
        {
            "label": DIMENSION_LABELS[d][lang],
            "score": person_scores[i],
            "min": pos_min[i], "max": pos_max[i],
            "fit": float(getattr(fit, f"{d}_fit")),
            "in_range": pos_min[i] <= person_scores[i] <= pos_max[i],
        }
        for i, d in enumerate(DIMENSIONS)
    ]

    filename = f"fit-poste_{person.last_name.lower()}_{position.title_fr.lower().replace(' ', '-')}.pdf"
    return _render_pdf("reports/pdf/position_fit.html", {
        "person": person, "position": position, "fit": fit,
        "dim_details": dim_details, "lang": lang,
    }, filename)


@login_required
def team_fit_pdf(request, person_pk, team_pk):
    person = get_object_or_404(Person, pk=person_pk, org=request.user.org)
    team = get_object_or_404(Team, pk=team_pk, org=request.user.org)
    fit = get_object_or_404(TeamFitResult, person=person, team=team)
    profile = person.big_five_profile
    lang = _lang(request)

    AuditLog.objects.create(
        org=request.user.org, user=request.user,
        action="team_fit.exported_pdf", entity_type="TeamFitResult",
        entity_id=fit.id,
        metadata={"person_id": str(person.id), "team_id": str(team.id)},
    )

    member_profiles = [
        m.person.big_five_profile
        for m in TeamMembership.objects
            .filter(team=team, left_at__isnull=True)
            .exclude(person=person)
            .select_related("person__big_five_profile")
        if hasattr(m.person, "big_five_profile")
    ]
    team_data = compute_team_profile(member_profiles)
    person_scores = [float(getattr(profile, d)) for d in DIMENSIONS]
    team_avgs = [team_data["averages"][d] if team_data else 50.0 for d in DIMENSIONS]
    complementarity = fit.complementarity

    SIGNAL_LABELS = {
        "fr": {"similar": "Similaire", "different": "Différent", "complementary": "Complémentaire"},
        "en": {"similar": "Similar", "different": "Different", "complementary": "Complementary"},
    }
    dim_details = [
        {
            "label": DIMENSION_LABELS[d][lang],
            "score": person_scores[i],
            "team_avg": team_avgs[i],
            "fit": float(getattr(fit, f"{d}_fit")),
            "signal": complementarity.get(d, "similar"),
            "signal_label": SIGNAL_LABELS[lang].get(complementarity.get(d, "similar"), ""),
        }
        for i, d in enumerate(DIMENSIONS)
    ]

    filename = f"fit-equipe_{person.last_name.lower()}_{team.name.lower().replace(' ', '-')}.pdf"
    return _render_pdf("reports/pdf/team_fit.html", {
        "person": person, "team": team, "fit": fit,
        "dim_details": dim_details, "lang": lang,
        "team_size": fit.team_size_at_computation,
    }, filename)
