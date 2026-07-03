"""
Abonnement — item #2 de la roadmap V3 (essai gratuit puis abonnement, US-E1-07).

Un seul plan payant, un essai gratuit de `TRIAL_DAYS` jours à la création de
l'organisation. Passé l'essai sans abonnement actif, des quotas d'usage
s'appliquent (voir `apps/billing/quotas.py`) — jamais un blocage total de
l'accès, l'organisation reste consultable, seule la création de nouvelles
ressources est limitée.

L'intégration Stripe (Checkout + Customer Portal + webhook) est le mécanisme
de paiement, mais ce modèle reste la source de vérité côté FitRadarHR — les
événements Stripe ne font que mettre à jour `status`/`current_period_end`.
"""
import uuid
from datetime import timedelta

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from apps.accounts.models import Organization
from core.managers import OrgManager

TRIAL_DAYS = 14


class Subscription(models.Model):
    class Status(models.TextChoices):
        TRIALING = "trialing", _("Essai")
        ACTIVE = "active", _("Actif")
        PAST_DUE = "past_due", _("Paiement en retard")
        CANCELED = "canceled", _("Résilié")

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    org = models.OneToOneField(
        Organization, on_delete=models.CASCADE,
        related_name="subscription", verbose_name=_("organisation"),
    )
    status = models.CharField(
        _("statut"), max_length=10, choices=Status.choices, default=Status.TRIALING,
    )
    trial_ends_at = models.DateTimeField(_("fin d'essai"))
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
    def is_trial_active(self):
        return self.status == self.Status.TRIALING and self.trial_ends_at > timezone.now()

    @property
    def is_paid_active(self):
        return self.status == self.Status.ACTIVE

    @property
    def has_full_access(self):
        """Essai en cours OU abonnement payant actif OU org de démo — sinon
        les quotas du plan gratuit s'appliquent (voir `quotas.py`)."""
        return bool(self.org.is_demo) or self.is_trial_active or self.is_paid_active

    @property
    def trial_days_left(self):
        if not self.is_trial_active:
            return 0
        return max(0, (self.trial_ends_at - timezone.now()).days)

    @classmethod
    def get_or_create_for_org(cls, org):
        """Accès résilient : toute organisation (y compris créée avant
        l'introduction de la facturation) obtient un essai par défaut au
        premier accès plutôt que de lever une exception."""
        obj, _created = cls.objects.get_or_create(
            org=org,
            defaults={"trial_ends_at": timezone.now() + timedelta(days=TRIAL_DAYS)},
        )
        return obj

    @classmethod
    def start_trial(cls, org):
        """Crée explicitement l'essai à la création d'une organisation (appelé
        depuis les vues d'inscription B2B/B2C)."""
        return cls.get_or_create_for_org(org)
