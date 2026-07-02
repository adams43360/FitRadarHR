import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.accounts.models import Organization
from core.managers import OrgQuerySet


class DepartmentQuerySet(OrgQuerySet):
    def active(self):
        return self.filter(is_archived=False)


DepartmentManager = models.Manager.from_queryset(DepartmentQuerySet)


class Department(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    org = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="departments",
        verbose_name=_("organisation"),
    )
    name_fr = models.CharField(_("nom (FR)"), max_length=255)
    name_en = models.CharField(_("nom (EN)"), max_length=255, blank=True)
    description = models.TextField(_("description"), blank=True)
    is_archived = models.BooleanField(_("archivé"), default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = DepartmentManager()

    class Meta:
        verbose_name = _("département")
        verbose_name_plural = _("départements")
        ordering = ["name_fr"]
        unique_together = [("org", "name_fr")]

    def __str__(self):
        return self.name_fr

    def get_name(self, lang="fr"):
        return self.name_en if lang == "en" and self.name_en else self.name_fr
