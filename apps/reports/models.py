import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.accounts.models import Organization, User
from apps.fit.models import BigFiveProfile


class FitReport(models.Model):
    class ReportType(models.TextChoices):
        JOB = "JOB", _("Fit Poste")
        TEAM = "TEAM", _("Fit Équipe")

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    org = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="fit_reports")
    profile = models.ForeignKey(BigFiveProfile, on_delete=models.CASCADE, related_name="fit_reports")
    report_type = models.CharField(max_length=4, choices=ReportType.choices)
    # Nullable selon le type de rapport
    position = models.ForeignKey("positions.Position", on_delete=models.SET_NULL, null=True, blank=True, related_name="fit_reports")
    team = models.ForeignKey("teams.Team", on_delete=models.SET_NULL, null=True, blank=True, related_name="fit_reports")
    # Scores de fit par dimension (pas de score global unique — human in the loop)
    fit_openness = models.DecimalField(max_digits=5, decimal_places=2)
    fit_conscientiousness = models.DecimalField(max_digits=5, decimal_places=2)
    fit_extraversion = models.DecimalField(max_digits=5, decimal_places=2)
    fit_agreeableness = models.DecimalField(max_digits=5, decimal_places=2)
    fit_neuroticism = models.DecimalField(max_digits=5, decimal_places=2)
    algorithm_version = models.CharField(max_length=20, default="v1.0")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="created_reports")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("rapport de fit")
        verbose_name_plural = _("rapports de fit")
        ordering = ["-created_at"]

    def __str__(self):
        return f"Rapport {self.report_type} — {self.profile.person}"


class AuditLog(models.Model):
    """Journal immuable — EU AI Act + RGPD. Aucun UPDATE/DELETE autorisé."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    org = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="audit_logs")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="audit_logs")
    action = models.CharField(max_length=100)  # ex: "report.viewed", "pdf.exported"
    entity_type = models.CharField(max_length=50)  # ex: "FitReport", "Person"
    entity_id = models.UUIDField()
    metadata = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("journal d'audit")
        verbose_name_plural = _("journaux d'audit")
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if not self._state.adding:
            raise Exception("AuditLog est immuable.")
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        raise Exception("AuditLog ne peut pas être supprimé.")
