"""
Abonnement — item #2 de la roadmap V3 (US-E1-07), modèle freemium depuis 2026-07-06.

Un seul plan payant (39 €/mois, prix configuré côté Stripe via `STRIPE_PRICE_ID`).
Sans abonnement actif, le plan gratuit s'applique sans limite de durée : des
quotas d'usage (voir `apps/billing/quotas.py`) limitent la création de
nouvelles ressources — jamais un blocage total de l'accès, l'organisation
reste consultable.

Historique : le modèle initial (2026-07-03) prévoyait un essai gratuit de
14 jours puis quotas. Remplacé par un plan gratuit permanent (≤ 25 personnes)
— plus simple à comprendre et sans pression artificielle à la conversion.

L'intégration Stripe (Checkout + Customer Portal + webhook) est le mécanisme
de paiement, mais ce modèle reste la source de vérité côté FitRadarHR — les
événements Stripe ne font que mettre à jour `status`/`current_period_end`.
"""
import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.accounts.models import Organization
from core.managers import OrgManager


class Subscription(models.Model):
    class Status(models.TextChoices):
        FREE = "free", _("Plan gratuit")
        ACTIVE = "active", _("Actif")
        PAST_DUE = "past_due", _("Paiement en retard")
        CANCELED = "canceled", _("Résilié")

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    org = models.OneToOneField(
        Organization, on_delete=models.CASCADE,
        related_name="subscription", verbose_name=_("organisation"),
    )
    status = models.CharField(
        _("statut"), max_length=10, choices=Status.choices, default=Status.FREE,
    )
    stripe_customer_id = models.CharField(_("ID client Stripe"), max_length=255, blank=True)
    stripe_subscription_id = models.CharField(_("ID abonnement Stripe"), max_length=255, blank=True)
    current_period_end = models.DateTimeField(_("fin de période en cours"), null=True, blank=True)
    created_at = models.DateTimeField(_("créé le"), auto_now_add=True)
    updated_at = models.DateTimeField(_("mis à jour le"), auto_now=True)

    objects = OrgManager()

    class Meta:
        verbose_name = _("abonnement")
        verbose_name_plural = _("abonnements")

    def __str__(self):
        return f"{self.org} — {self.get_status_display()}"

    @property
    def is_paid_active(self):
        return self.status == self.Status.ACTIVE

    @property
    def has_full_access(self):
        """Abonnement payant actif OU org de démo — sinon les quotas du plan
        gratuit s'appliquent (voir `quotas.py`)."""
        return bool(self.org.is_demo) or self.is_paid_active

    @classmethod
    def get_or_create_for_org(cls, org):
        """Accès résilient : toute organisation (y compris créée avant
        l'introduction de la facturation) obtient un abonnement "plan gratuit"
        au premier accès plutôt que de lever une exception."""
        obj, _created = cls.objects.get_or_create(org=org)
        return obj

    @classmethod
    def start_free_plan(cls, org):
        """Crée explicitement l'abonnement "plan gratuit" à la création d'une
        organisation (appelé depuis les vues d'inscription B2B/B2C)."""
        return cls.get_or_create_for_org(org)
