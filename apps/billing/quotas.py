"""
Quotas du plan gratuit — s'appliquent uniquement une fois l'essai terminé et
en l'absence d'abonnement actif (voir `Subscription.has_full_access`).

Principe produit : jamais de blocage total de l'accès aux données existantes,
seule la création de nouvelles ressources est limitée — l'organisation garde
la consultation de ses postes/équipes/rapports même hors quota.
"""
from django.utils.translation import gettext_lazy as _

from .models import Subscription

FREE_MAX_ACTIVE_POSITIONS = 3
FREE_MAX_PEOPLE = 10
FREE_MAX_QUESTIONNAIRES_PER_MONTH = 5


def has_full_access(org):
    return Subscription.get_or_create_for_org(org).has_full_access


def _month_start():
    from django.utils import timezone
    now = timezone.now()
    return now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)


def check_quota(org, resource):
    """Renvoie `None` si la création est autorisée, ou un message (traduit,
    prêt à afficher) si le quota du plan gratuit est atteint."""
    if has_full_access(org):
        return None

    if resource == "position":
        count = org.positions.filter(status="active").count()
        if count >= FREE_MAX_ACTIVE_POSITIONS:
            return _(
                "Limite du plan gratuit atteinte (%(n)d postes actifs). "
                "Passez à l'abonnement pour en créer davantage."
            ) % {"n": FREE_MAX_ACTIVE_POSITIONS}

    elif resource == "person":
        count = org.persons.count()
        if count >= FREE_MAX_PEOPLE:
            return _(
                "Limite du plan gratuit atteinte (%(n)d personnes). "
                "Passez à l'abonnement pour en ajouter davantage."
            ) % {"n": FREE_MAX_PEOPLE}

    elif resource == "questionnaire":
        from apps.survey.models import QuestionnaireLink
        count = QuestionnaireLink.objects.filter(
            org=org, sent_at__gte=_month_start()
        ).count()
        if count >= FREE_MAX_QUESTIONNAIRES_PER_MONTH:
            return _(
                "Limite du plan gratuit atteinte (%(n)d questionnaires envoyés ce mois-ci). "
                "Passez à l'abonnement pour en envoyer davantage."
            ) % {"n": FREE_MAX_QUESTIONNAIRES_PER_MONTH}

    return None


def remaining_quota(org, resource):
    """Renvoie le nombre de ressources encore créables, ou `None` si illimité
    (essai/abonnement actif/démo). Utilisé pour capper l'import CSV en masse."""
    if has_full_access(org):
        return None
    if resource == "person":
        return max(0, FREE_MAX_PEOPLE - org.persons.count())
    return None
