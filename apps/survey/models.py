import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.accounts.models import Organization, User
from apps.teams.models import Person
from core.managers import OrgManager


class QuestionnaireLink(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", _("En attente")
        IN_PROGRESS = "in_progress", _("En cours")
        COMPLETED = "completed", _("Complété")
        EXPIRED = "expired", _("Expiré")

    class Language(models.TextChoices):
        FR = "fr", "Français"
        EN = "en", "English"
        ES = "es", "Español"
        DE = "de", "Deutsch"

    class Version(models.TextChoices):
        V50 = "50", _("50 items")
        V100 = "100", _("100 items")

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    org = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="questionnaire_links")
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name="questionnaire_links")
    position = models.ForeignKey(
        "positions.Position",
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name="questionnaire_links",
        verbose_name=_("poste"),
    )
    token = models.CharField(max_length=128, unique=True)
    questionnaire_version = models.CharField(max_length=3, choices=Version.choices, default=Version.V50)
    language = models.CharField(max_length=2, choices=Language.choices, default=Language.FR)
    sent_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="sent_links")
    sent_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    status = models.CharField(max_length=15, choices=Status.choices, default=Status.PENDING)
    completed_at = models.DateTimeField(null=True, blank=True)
    reminder_sent_at = models.DateTimeField(null=True, blank=True)

    objects = OrgManager()

    class Meta:
        verbose_name = _("lien questionnaire")
        verbose_name_plural = _("liens questionnaire")

    def __str__(self):
        return f"Lien {self.person} ({self.status})"


class ConsentRecord(models.Model):
    """Consentement RGPD explicite — immuable."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    link = models.OneToOneField(QuestionnaireLink, on_delete=models.CASCADE, related_name="consent")
    consented_at = models.DateTimeField(auto_now_add=True)
    consent_version = models.CharField(max_length=20, default="v1.0")
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    language = models.CharField(max_length=2, default="fr")

    class Meta:
        verbose_name = _("consentement")

    def save(self, *args, **kwargs):
        if not self._state.adding:
            raise Exception("ConsentRecord est immuable.")
        super().save(*args, **kwargs)


class QuestionnaireSession(models.Model):
    """Sauvegarde de la progression (reprise possible)."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    link = models.OneToOneField(QuestionnaireLink, on_delete=models.CASCADE, related_name="session")
    answers = models.JSONField(default=dict)  # {"item_id": score, ...}
    current_item_index = models.PositiveSmallIntegerField(default=0)
    started_at = models.DateTimeField(auto_now_add=True)
    last_saved_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("session questionnaire")
