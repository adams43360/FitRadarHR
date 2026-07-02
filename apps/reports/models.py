import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.accounts.models import Organization, User
from core.managers import OrgManager


class AuditLog(models.Model):
    """Journal immuable — EU AI Act + RGPD. Aucun UPDATE/DELETE autorisé."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    org = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="audit_logs")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="audit_logs")
    action = models.CharField(max_length=100)  # ex: "report.viewed", "pdf.exported"
    entity_type = models.CharField(max_length=50)  # ex: "PositionFitResult", "Person"
    entity_id = models.UUIDField()
    metadata = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = OrgManager()

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
