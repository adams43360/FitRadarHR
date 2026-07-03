import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.accounts.models import Organization, User
from apps.teams.models import Person, Team
from apps.survey.models import QuestionnaireLink
from core.managers import PersonOrgManager


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

    objects = PersonOrgManager()

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


class BigFiveProfileHistory(models.Model):
    """Instantané d'un profil Big Five remplacé par une re-passation.

    Item #5 de la roadmap V2 — suivi longitudinal. `BigFiveProfile` reste la
    source de vérité pour le profil *courant* (toutes les vues de fit s'appuient
    dessus, inchangé) ; cette table ne sert qu'à l'affichage de l'évolution
    dans le temps sur le rapport de profil.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name="profile_history")
    openness = models.DecimalField(_("ouverture"), max_digits=5, decimal_places=2)
    conscientiousness = models.DecimalField(_("conscienciosité"), max_digits=5, decimal_places=2)
    extraversion = models.DecimalField(_("extraversion"), max_digits=5, decimal_places=2)
    agreeableness = models.DecimalField(_("agréabilité"), max_digits=5, decimal_places=2)
    neuroticism = models.DecimalField(_("neuroticisme"), max_digits=5, decimal_places=2)
    questionnaire_version = models.CharField(max_length=3, choices=BigFiveProfile.Version.choices)
    algorithm_version = models.CharField(max_length=20, default="v1.0")
    computed_at = models.DateTimeField(_("calculé le"))  # date du profil archivé, pas de l'archivage
    archived_at = models.DateTimeField(auto_now_add=True)

    objects = PersonOrgManager()

    class Meta:
        verbose_name = _("historique profil Big Five")
        verbose_name_plural = _("historique profils Big Five")
        ordering = ["computed_at"]

    def __str__(self):
        return f"Historique — {self.person} ({self.computed_at:%d/%m/%Y})"

    def as_dict(self):
        return {
            "O": float(self.openness),
            "C": float(self.conscientiousness),
            "E": float(self.extraversion),
            "A": float(self.agreeableness),
            "N": float(self.neuroticism),
        }

    @classmethod
    def archive(cls, profile):
        """Archive un BigFiveProfile existant avant qu'il ne soit écrasé."""
        return cls.objects.create(
            person=profile.person,
            openness=profile.openness,
            conscientiousness=profile.conscientiousness,
            extraversion=profile.extraversion,
            agreeableness=profile.agreeableness,
            neuroticism=profile.neuroticism,
            questionnaire_version=profile.questionnaire_version,
            algorithm_version=profile.algorithm_version,
            computed_at=profile.computed_at,
        )


class PositionFitResult(models.Model):
    """Résultat du calcul de fit entre une personne et un poste."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name="position_fits")
    position = models.ForeignKey(
        "positions.Position", on_delete=models.CASCADE, related_name="fit_results"
    )
    person_profile = models.ForeignKey(
        BigFiveProfile, on_delete=models.SET_NULL, null=True, related_name="position_fit_results"
    )

    # Scores de fit par dimension (0–100)
    openness_fit = models.DecimalField(_("fit ouverture"), max_digits=5, decimal_places=2)
    conscientiousness_fit = models.DecimalField(_("fit conscienciosité"), max_digits=5, decimal_places=2)
    extraversion_fit = models.DecimalField(_("fit extraversion"), max_digits=5, decimal_places=2)
    agreeableness_fit = models.DecimalField(_("fit agréabilité"), max_digits=5, decimal_places=2)
    neuroticism_fit = models.DecimalField(_("fit neuroticisme"), max_digits=5, decimal_places=2)
    overall_fit = models.DecimalField(_("fit global"), max_digits=5, decimal_places=2)

    algorithm_version = models.CharField(max_length=20, default="v1.0")
    computed_at = models.DateTimeField(auto_now=True)

    objects = PersonOrgManager()

    class Meta:
        verbose_name = _("résultat fit poste")
        verbose_name_plural = _("résultats fit poste")
        unique_together = [("person", "position")]

    def __str__(self):
        return f"Fit {self.person} / {self.position} — {self.overall_fit}%"

    def as_dict(self):
        return {
            "openness": float(self.openness_fit),
            "conscientiousness": float(self.conscientiousness_fit),
            "extraversion": float(self.extraversion_fit),
            "agreeableness": float(self.agreeableness_fit),
            "neuroticism": float(self.neuroticism_fit),
            "overall": float(self.overall_fit),
        }


class TeamFitResult(models.Model):
    """Résultat du calcul de fit entre une personne et une équipe."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name="team_fits")
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="fit_results")
    person_profile = models.ForeignKey(
        BigFiveProfile, on_delete=models.SET_NULL, null=True, related_name="team_fit_results"
    )

    # Scores de fit par dimension (0–100)
    openness_fit = models.DecimalField(_("fit ouverture"), max_digits=5, decimal_places=2)
    conscientiousness_fit = models.DecimalField(_("fit conscienciosité"), max_digits=5, decimal_places=2)
    extraversion_fit = models.DecimalField(_("fit extraversion"), max_digits=5, decimal_places=2)
    agreeableness_fit = models.DecimalField(_("fit agréabilité"), max_digits=5, decimal_places=2)
    neuroticism_fit = models.DecimalField(_("fit neuroticisme"), max_digits=5, decimal_places=2)
    overall_fit = models.DecimalField(_("fit global"), max_digits=5, decimal_places=2)

    # Signal de complémentarité par dimension
    # {"openness": "similar"|"different"|"complementary", ...}
    complementarity = models.JSONField(_("complémentarité"), default=dict)

    team_size_at_computation = models.PositiveSmallIntegerField(default=0)
    algorithm_version = models.CharField(max_length=20, default="v1.0")
    computed_at = models.DateTimeField(auto_now=True)

    objects = PersonOrgManager()

    class Meta:
        verbose_name = _("résultat fit équipe")
        verbose_name_plural = _("résultats fit équipe")
        unique_together = [("person", "team")]

    def __str__(self):
        return f"Fit {self.person} / {self.team} — {self.overall_fit}%"

    def as_dict(self):
        return {
            "openness": float(self.openness_fit),
            "conscientiousness": float(self.conscientiousness_fit),
            "extraversion": float(self.extraversion_fit),
            "agreeableness": float(self.agreeableness_fit),
            "neuroticism": float(self.neuroticism_fit),
            "overall": float(self.overall_fit),
            "complementarity": self.complementarity,
        }
