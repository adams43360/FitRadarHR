import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.accounts.models import Organization, User
from apps.teams.models import Person
from apps.survey.models import QuestionnaireLink


class BigFiveProfile(models.Model):
    class Version(models.TextChoices):
        V50 = "50", "50 items"
        V100 = "100", "100 items"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    person = models.OneToOneField(Person, on_delete=models.CASCADE, related_name="big_five_profile")
    link = models.OneToOneField(QuestionnaireLink, on_delete=models.SET_NULL, null=True, related_name="big_five_profile")
    openness = models.DecimalField(_("ouverture"), max_digits=5, decimal_places=2)
    conscientiousness = models.DecimalField(_("conscienciosité"), max_digits=5, decimal_places=2)
    extraversion = models.DecimalField(_("extraversion"), max_digits=5, decimal_places=2)
    agreeableness = models.DecimalField(_("agréabilité"), max_digits=5, decimal_places=2)
    neuroticism = models.DecimalField(_("neuroticisme"), max_digits=5, decimal_places=2)
    questionnaire_version = models.CharField(max_length=3, choices=Version.choices)
    algorithm_version = models.CharField(max_length=20, default="v1.0")
    computed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("profil Big Five")

    def __str__(self):
        return f"Profil Big Five — {self.person}"

    def as_dict(self):
        return {
            "O": float(self.openness),
            "C": float(self.conscientiousness),
            "E": float(self.extraversion),
            "A": float(self.agreeableness),
            "N": float(self.neuroticism),
        }
