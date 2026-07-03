from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, render
from django.template.loader import render_to_string

from apps.fit.models import BigFiveProfile, PositionFitResult, TeamFitResult
from apps.positions.models import Position
from apps.teams.models import Person, Team
from core.managers import get_org_object_or_404

from .analytics import build_analytics_context
from .models import AuditLog
from .services import (
    audit,
    build_person_profile_context,
    build_position_fit_context,
    build_team_fit_context,
    get_lang,
)


# ──────────────────────────────────────────────────────────────────────────────
# Liste des rapports disponibles
# ──────────────────────────────────────────────────────────────────────────────

@login_required
def report_list(request):
    persons = (
        Person.objects
        .for_org(request.user.org)
        .select_related("big_five_profile")
        .prefetch_related("position_fits__position", "team_fits__team")
        .order_by("last_name", "first_name")
    )
    persons_with_profile = [p for p in persons if hasattr(p, "big_five_profile")]
    return render(request, "reports/list.html", {"persons": persons_with_profile})


# ──────────────────────────────────────────────────────────────────────────────
# Récupération des objets (bornée au tenant)
# ──────────────────────────────────────────────────────────────────────────────

def _get_person_profile(request, person_pk):
    person = get_org_object_or_404(Person, request.user.org, pk=person_pk)
    profile = get_object_or_404(BigFiveProfile, person=person)
    return person, profile


def _get_position_fit(request, person_pk, position_pk):
    person = get_org_object_or_404(Person, request.user.org, pk=person_pk)
    position = get_org_object_or_404(Position, request.user.org, pk=position_pk)
    fit = get_object_or_404(PositionFitResult, person=person, position=position)
    return person, position, fit


def _get_team_fit(request, person_pk, team_pk):
    person = get_org_object_or_404(Person, request.user.org, pk=person_pk)
    team = get_org_object_or_404(Team, request.user.org, pk=team_pk)
    fit = get_object_or_404(TeamFitResult, person=person, team=team)
    return person, team, fit


# ──────────────────────────────────────────────────────────────────────────────
# Profil Big Five individuel
# ──────────────────────────────────────────────────────────────────────────────

@login_required
def person_profile(request, person_pk):
    person, profile = _get_person_profile(request, person_pk)
    audit(request, "profile.viewed", "BigFiveProfile", profile.id, person_id=str(person.id))

    context = build_person_profile_context(person, profile, get_lang(request))

    position_fits = person.position_fits.select_related("position__team").order_by("-overall_fit")
    team_fits = person.team_fits.select_related("team").order_by("-overall_fit")

    # Pour chaque fit poste dont le poste a une équipe cible, on joint le fit équipe correspondant
    team_fits_by_team = {tf.team_id: tf for tf in team_fits}
    context.update({
        "position_fits": position_fits,
        "team_fits": team_fits,
        "position_fits_with_team": [
            {
                "position_fit": pf,
                "team_fit": team_fits_by_team.get(pf.position.team_id) if pf.position.team_id else None,
            }
            for pf in position_fits
        ],
    })
    return render(request, "reports/person_profile.html", context)


# ──────────────────────────────────────────────────────────────────────────────
# Rapport Fit Poste
# ──────────────────────────────────────────────────────────────────────────────

@login_required
def position_fit_report(request, person_pk, position_pk):
    person, position, fit = _get_position_fit(request, person_pk, position_pk)
    audit(
        request, "position_fit.viewed", "PositionFitResult", fit.id,
        person_id=str(person.id), position_id=str(position.id),
    )
    context = build_position_fit_context(person, position, fit, get_lang(request))
    return render(request, "reports/position_fit.html", context)


# ──────────────────────────────────────────────────────────────────────────────
# Rapport Fit Équipe
# ──────────────────────────────────────────────────────────────────────────────

@login_required
def team_fit_report(request, person_pk, team_pk):
    person, team, fit = _get_team_fit(request, person_pk, team_pk)
    audit(
        request, "team_fit.viewed", "TeamFitResult", fit.id,
        person_id=str(person.id), team_id=str(team.id),
    )
    context = build_team_fit_context(person, team, fit, get_lang(request))
    return render(request, "reports/team_fit.html", context)


# ──────────────────────────────────────────────────────────────────────────────
# Export PDF (WeasyPrint)
# ──────────────────────────────────────────────────────────────────────────────

def _render_pdf(template_name, context, filename):
    from weasyprint import HTML

    html_string = render_to_string(template_name, context)
    pdf = HTML(string=html_string).write_pdf()
    response = HttpResponse(pdf, content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="{filename}"'
    return response


def _slug(value):
    return value.lower().replace(" ", "-")


@login_required
def person_profile_pdf(request, person_pk):
    person, profile = _get_person_profile(request, person_pk)
    audit(request, "profile.exported_pdf", "BigFiveProfile", profile.id, person_id=str(person.id))

    context = build_person_profile_context(person, profile, get_lang(request))
    filename = f"profil-ocean_{_slug(person.last_name)}_{_slug(person.first_name)}.pdf"
    return _render_pdf("reports/pdf/person_profile.html", context, filename)


@login_required
def position_fit_pdf(request, person_pk, position_pk):
    person, position, fit = _get_position_fit(request, person_pk, position_pk)
    audit(
        request, "position_fit.exported_pdf", "PositionFitResult", fit.id,
        person_id=str(person.id), position_id=str(position.id),
    )
    context = build_position_fit_context(person, position, fit, get_lang(request))
    filename = f"fit-poste_{_slug(person.last_name)}_{_slug(position.title_fr)}.pdf"
    return _render_pdf("reports/pdf/position_fit.html", context, filename)


@login_required
def team_fit_pdf(request, person_pk, team_pk):
    person, team, fit = _get_team_fit(request, person_pk, team_pk)
    audit(
        request, "team_fit.exported_pdf", "TeamFitResult", fit.id,
        person_id=str(person.id), team_id=str(team.id),
    )
    context = build_team_fit_context(person, team, fit, get_lang(request))
    filename = f"fit-equipe_{_slug(person.last_name)}_{_slug(team.name)}.pdf"
    return _render_pdf("reports/pdf/team_fit.html", context, filename)


# ── Audit log viewer (E8) ──────────────────────────────────────────────────────

@login_required
def audit_log(request):
    """Journal d'audit — RH only."""
    if not request.user.is_rh:
        return HttpResponseForbidden()

    logs_qs = (
        AuditLog.objects.for_org(request.user.org)
        .select_related("user")
        .order_by("-created_at")
    )
    paginator = Paginator(logs_qs, 25)
    logs = paginator.get_page(request.GET.get("page", 1))
    return render(request, "reports/audit_log.html", {"logs": logs})


# ──────────────────────────────────────────────────────────────────────────────
# Analytics produit (KPIs) — RH only
# ──────────────────────────────────────────────────────────────────────────────

@login_required
def analytics(request):
    """Tableau de bord analytics — funnel questionnaires, adoption, engagement.

    Définitions des métriques : docs/product/metrics.md
    """
    if not request.user.is_rh:
        return HttpResponseForbidden()

    context = build_analytics_context(request.user.org)
    return render(request, "reports/analytics.html", context)
