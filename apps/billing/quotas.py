"""
Quota du plan gratuit — s'applique uniquement une fois l'essai terminé et
en l'absence d'abonnement actif (voir `Subscription.has_full_access`).

Modèle : un seuil unique et cumulé sur le nombre total de personnes de
l'organisation (`org.persons.count()`). La création de postes et l'envoi de
questionnaires restent libres — c'est le début du parcours, pas l'endroit où
mettre de la friction, et le nombre de personnes capture implicitement le
volume de questionnaires puisque chaque personne reçoit en général un lien.

Principe produit : jamais de blocage total de l'accès aux données existantes,
seule la création de nouvelles ressources est limitée — l'organisation garde
la consultation de ses postes/équipes/rapports même hors quota.
"""
from django.utils.translation import gettext_lazy as _

from .models import Subscription

FREE_MAX_PEOPLE = 25


def has_full_access(org):
    return Subscription.get_or_create_for_org(org).has_full_access


def check_quota(org, resource):
    """Renvoie `None` si la création est autorisée, ou un message (traduit,
    prêt à afficher) si le quota du plan gratuit est atteint. Seule la
    ressource "person" est soumise à quota."""
    if has_full_access(org):
        return None

    if resource == "person":
        count = org.persons.count()
        if count >= FREE_MAX_PEOPLE:
            return _(
                "Limite du plan gratuit atteinte (%(n)d personnes). "
                "Passez à l'abonnement pour en ajouter davantage."
            ) % {"n": FREE_MAX_PEOPLE}

    return None


def remaining_quota(org, resource):
    """Renvoie le nombre de ressources encore créables, ou `None` si illimité
    (essai/abonnement actif/démo). Utilisé pour capper l'import CSV en masse."""
    if has_full_access(org):
        return None
    if resource == "person":
        return max(0, FREE_MAX_PEOPLE - org.persons.count())
    return None
