import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.accounts.models import Organization, User


class Position(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "active", _("Actif")
        ARCHIVED = "archived", _("Archivé")

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    org = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="positions", verbose_name=_("organisation"))
    title_fr = models.CharField(_("titre (FR)"), max_length=255)
    title_en = models.CharField(_("titre (EN)"), max_length=255, blank=True)
    description_fr = models.TextField(_("description (FR)"), blank=True)
    description_en = models.TextField(_("description (EN)"), blank=True)
    department = models.ForeignKey(
        "departments.Department",
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name="positions",
        verbose_name=_("département"),
    )
    team = models.ForeignKey(
        "teams.Team",
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name="positions",
        verbose_name=_("équipe cible"),
    )
    status = models.CharField(_("statut"), max_length=10, choices=Status.choices, default=Status.ACTIVE)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="created_positions")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("poste")
        verbose_name_plural = _("postes")
        ordering = ["-created_at"]

    def __str__(self):
        return self.title_fr

    def get_title(self, lang="fr"):
        return self.title_en if lang == "en" and self.title_en else self.title_fr

    @property
    def has_profile(self):
        return hasattr(self, "profile")


class PositionProfile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    position = models.OneToOneField(Position, on_delete=models.CASCADE, related_name="profile")
    openness_min = models.PositiveSmallIntegerField(default=0)
    openness_max = models.PositiveSmallIntegerField(default=100)
    conscientiousness_min = models.PositiveSmallIntegerField(default=0)
    conscientiousness_max = models.PositiveSmallIntegerField(default=100)
    extraversion_min = models.PositiveSmallIntegerField(default=0)
    extraversion_max = models.PositiveSmallIntegerField(default=100)
    agreeableness_min = models.PositiveSmallIntegerField(default=0)
    agreeableness_max = models.PositiveSmallIntegerField(default=100)
    neuroticism_min = models.PositiveSmallIntegerField(default=0)
    neuroticism_max = models.PositiveSmallIntegerField(default=100)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("profil de poste")

    def __str__(self):
        return f"Profil — {self.position}"
