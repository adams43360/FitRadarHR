import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.accounts.models import Organization, User


class Team(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    org = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="teams")
    department = models.ForeignKey(
        "departments.Department",
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name="teams",
        verbose_name=_("département"),
    )
    name = models.CharField(_("nom"), max_length=255)
    description = models.TextField(_("description"), blank=True)
    manager = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="managed_teams")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("équipe")
        verbose_name_plural = _("équipes")

    def __str__(self):
        return self.name


class Person(models.Model):
    """Candidat ou collaborateur — n'a pas nécessairement de compte User."""

    class PersonType(models.TextChoices):
        CANDIDATE = "candidate", _("Candidat")
        COLLABORATOR = "collaborator", _("Collaborateur")

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    org = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="persons")
    email = models.EmailField(_("email"))
    first_name = models.CharField(_("prénom"), max_length=100)
    last_name = models.CharField(_("nom"), max_length=100)
    person_type = models.CharField(max_length=15, choices=PersonType.choices, default=PersonType.CANDIDATE)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="created_persons")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("personne")
        verbose_name_plural = _("personnes")
        unique_together = [("org", "email")]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def anonymize(self):
        """Effacement RGPD — anonymise les PII sans supprimer l'enregistrement."""
        self.first_name = "[supprimé]"
        self.last_name = "[supprimé]"
        self.email = f"deleted-{self.id}@anonymized"
        self.save()


class TeamMembership(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="memberships")
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name="memberships")
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="added_members")
    joined_at = models.DateTimeField(auto_now_add=True)
    left_at = models.DateTimeField(null=True, blank=True)  # NULL = membre actuel

    class Meta:
        verbose_name = _("appartenance équipe")

    def __str__(self):
        return f"{self.person} → {self.team}"
