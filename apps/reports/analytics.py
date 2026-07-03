"""
Analytics produit — calculs des KPIs affichés sur la page /reports/analytics/.

Toutes les métriques sont bornées au tenant (org) et documentées dans
`docs/product/metrics.md` (définitions, funnel AARRR, North Star).

Funnel questionnaire (par lien envoyé, non dédupliqué par personne) :
    envoyé → commencé (consentement RGPD donné) → complété (profil OCEAN calculé)
"""
from datetime import timedelta

from django.db.models import Avg, Count, DurationField, ExpressionWrapper, F
from django.db.models.functions import TruncMonth
from django.utils import timezone

from apps.fit.models import BigFiveProfile, PositionFitResult
from apps.positions.models import Position
from apps.survey.models import QuestionnaireLink
from apps.teams.models import Person, Team

from .models import AuditLog

ENGAGEMENT_WINDOW_DAYS = 30
MONTHS_WINDOW = 6


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
    }
