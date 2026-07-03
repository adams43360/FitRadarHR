"""
Analytics produit — calculs des KPIs affichés sur la page /reports/analytics/.

Toutes les métriques sont bornées au tenant (org) et documentées dans
`docs/product/metrics.md` (définitions, funnel AARRR, North Star).

Funnel questionnaire (par lien envoyé, non dédupliqué par personne) :
    envoyé → commencé (consentement RGPD donné) → complété (profil OCEAN calculé)
"""
from datetime import timedelta

from django.db.models import Avg, Count, DurationField, ExpressionWrapper, F, Min
from django.db.models.functions import TruncMonth
from django.utils import timezone

from apps.fit.models import BigFiveProfile, PositionFitResult
from apps.positions.models import Position
from apps.survey.models import QuestionnaireLink
from apps.teams.models import Person, Team

from .models import AuditLog

ENGAGEMENT_WINDOW_DAYS = 30
MONTHS_WINDOW = 6
RETENTION_MONTHS_WINDOW = 6  # cohortes sur la même fenêtre que "profils par mois"


def _month_key(dt):
    return (dt.year, dt.month)


def _add_months(date, n):
    month = date.month - 1 + n
    year = date.year + month // 12
    month = month % 12 + 1
    return date.replace(year=year, month=month, day=1)


def _retention_cohorts(org, now):
    """Cohortes de rétention mensuelles — item #6 roadmap V2.

    Cohorte = mois de la première passation *complétée* par personne
    (l'activation, indépendamment d'une éventuelle re-passation ultérieure —
    voir [[BigFiveProfileHistory]] item #5). Rétention à l'offset M+k = part de
    la cohorte dont le rapport de profil a été consulté (`profile.viewed`,
    audit log) au moins une fois durant ce mois-là.

    Version mensuelle plutôt qu'hebdomadaire (cf. docs/product/metrics.md,
    backlog V2) : plus lisible à l'échelle d'une org (quelques dizaines de
    personnes/mois) et cohérente avec le graphique "Profils par mois" déjà
    affiché sur cette page.
    """
    months_start = (now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
                    - timedelta(days=31 * (RETENTION_MONTHS_WINDOW - 1))).replace(day=1)
    current_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    # Activation = première passation complétée par personne (toutes dates
    # confondues), restreinte aux cohortes tombant dans la fenêtre d'affichage —
    # une re-passation ne doit jamais recréer une cohorte "fantôme".
    first_completions = (
        QuestionnaireLink.objects.for_org(org)
        .filter(status=QuestionnaireLink.Status.COMPLETED, completed_at__isnull=False)
        .values("person_id")
        .annotate(first_completed=Min("completed_at"))
        .filter(first_completed__gte=months_start)
    )
    cohorts = {}
    for row in first_completions:
        key = _month_key(row["first_completed"])
        cohorts.setdefault(key, set()).add(row["person_id"])

    if not cohorts:
        return []

    # Consultations de rapport de profil, groupées par personne et par mois.
    viewed_by_person_month = {}
    logs = (
        AuditLog.objects.for_org(org)
        .filter(action="profile.viewed", entity_type="BigFiveProfile", created_at__gte=months_start)
        .values_list("metadata", "created_at")
    )
    for metadata, created_at in logs:
        person_id = (metadata or {}).get("person_id")
        if not person_id:
            continue
        viewed_by_person_month.setdefault(person_id, set()).add(_month_key(created_at))

    rows = []
    cursor = months_start
    while cursor <= current_month:
        key = _month_key(cursor)
        person_ids = cohorts.get(key)
        if person_ids:
            cohort_size = len(person_ids)
            max_offset = (current_month.year - cursor.year) * 12 + (current_month.month - cursor.month)
            cells = []
            for offset in range(RETENTION_MONTHS_WINDOW):
                if offset > max_offset:
                    cells.append(None)  # mois pas encore atteint
                    continue
                target_key = _month_key(_add_months(cursor, offset))
                retained = sum(
                    1 for pid in person_ids
                    if target_key in viewed_by_person_month.get(pid, set())
                )
                cells.append({
                    "offset": offset,
                    "rate": round(100 * retained / cohort_size, 1),
                    "retained": retained,
                })
            rows.append({"label": cursor.strftime("%m/%Y"), "size": cohort_size, "cells": cells})
        cursor = _add_months(cursor, 1)
    return rows


def build_analytics_context(org):
    """Construit toutes les métriques de la page analytics pour une org."""
    now = timezone.now()
    links = QuestionnaireLink.objects.for_org(org)

    # ── Funnel questionnaires ────────────────────────────────────────────────
    sent_count = links.count()
    started_count = links.filter(consent__isnull=False).count()
    completed_count = links.filter(status=QuestionnaireLink.Status.COMPLETED).count()

    completion_rate = round(100 * completed_count / sent_count, 1) if sent_count else None
    start_rate = round(100 * started_count / sent_count, 1) if sent_count else None
    abandon_count = started_count - completed_count  # consenti mais jamais terminé

    # ── Délai moyen envoi → complétion ───────────────────────────────────────
    avg_delay = (
        links.filter(status=QuestionnaireLink.Status.COMPLETED, completed_at__isnull=False)
        .annotate(delay=ExpressionWrapper(
            F("completed_at") - F("sent_at"), output_field=DurationField()
        ))
        .aggregate(avg=Avg("delay"))["avg"]
    )
    avg_delay_days = round(avg_delay.total_seconds() / 86400, 1) if avg_delay else None

    # ── Répartition des statuts (donut) ─────────────────────────────────────
    status_counts = dict(
        links.values_list("status").annotate(n=Count("id")).order_by()
    )
    status_breakdown = {
        "pending": status_counts.get(QuestionnaireLink.Status.PENDING, 0),
        "in_progress": status_counts.get(QuestionnaireLink.Status.IN_PROGRESS, 0),
        "completed": status_counts.get(QuestionnaireLink.Status.COMPLETED, 0),
        "expired": status_counts.get(QuestionnaireLink.Status.EXPIRED, 0),
    }

    # ── Profils OCEAN créés par mois (6 derniers mois) ───────────────────────
    months_start = (now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
                    - timedelta(days=31 * (MONTHS_WINDOW - 1))).replace(day=1)
    monthly_raw = dict(
        BigFiveProfile.objects.for_org(org)
        .filter(computed_at__gte=months_start)
        .annotate(month=TruncMonth("computed_at"))
        .values_list("month")
        .annotate(n=Count("id"))
        .order_by()
    )
    profiles_by_month = []
    cursor = months_start
    while cursor <= now:
        key = next((m for m in monthly_raw if m.year == cursor.year and m.month == cursor.month), None)
        profiles_by_month.append({
            "label": cursor.strftime("%m/%Y"),
            "count": monthly_raw.get(key, 0) if key else 0,
        })
        # mois suivant
        cursor = (cursor + timedelta(days=32)).replace(day=1)

    # ── Engagement restitution (fenêtre 30 j, audit log) ─────────────────────
    window_start = now - timedelta(days=ENGAGEMENT_WINDOW_DAYS)
    audit_window = AuditLog.objects.for_org(org).filter(created_at__gte=window_start)
    reports_viewed = audit_window.filter(action="report.viewed").count()
    pdf_exported = audit_window.filter(action="pdf.exported").count()

    # ── Fit moyen par poste actif (classement) ───────────────────────────────
    fit_by_position = (
        PositionFitResult.objects.for_org(org)
        .filter(position__status=Position.Status.ACTIVE)
        .values("position_id", "position__title_fr", "position__title_en")
        .annotate(avg_fit=Avg("overall_fit"), n=Count("id"))
        .order_by("-avg_fit")
    )

    # ── Volumétrie générale ──────────────────────────────────────────────────
    persons = Person.objects.for_org(org)
    person_split = {
        "candidates": persons.filter(person_type=Person.PersonType.CANDIDATE).count(),
        "collaborators": persons.filter(person_type=Person.PersonType.COLLABORATOR).count(),
    }
    profiles_count = BigFiveProfile.objects.for_org(org).count()
    coverage_rate = (
        round(100 * profiles_count / persons.count(), 1) if persons.count() else None
    )

    return {
        "funnel": {
            "sent": sent_count,
            "started": started_count,
            "completed": completed_count,
            "start_rate": start_rate,
            "completion_rate": completion_rate,
            "abandon_count": abandon_count,
        },
        "avg_delay_days": avg_delay_days,
        "status_breakdown": status_breakdown,
        "profiles_by_month": profiles_by_month,
        "engagement": {
            "window_days": ENGAGEMENT_WINDOW_DAYS,
            "reports_viewed": reports_viewed,
            "pdf_exported": pdf_exported,
        },
        "fit_by_position": list(fit_by_position),
        "person_split": person_split,
        "profiles_count": profiles_count,
        "coverage_rate": coverage_rate,
        "teams_count": Team.objects.for_org(org).count(),
        "retention_cohorts": _retention_cohorts(org, now),
        "retention_offsets": list(range(RETENTION_MONTHS_WINDOW)),
    }
