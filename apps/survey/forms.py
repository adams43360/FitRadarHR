from django import forms
from django.utils.translation import gettext_lazy as _
from .models import QuestionnaireLink

CSS = "w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"


class SendLinkForm(forms.Form):
    person_email = forms.EmailField(
        label=_("Email de la personne"),
        widget=forms.EmailInput(attrs={
            "class": CSS,
            "placeholder": "prenom.nom@exemple.com",
        })
    )
    first_name = forms.CharField(
        label=_("Prénom"),
        required=False,
        widget=forms.TextInput(attrs={
            "class": CSS,
            "placeholder": _("Prénom"),
        })
    )
    last_name = forms.CharField(
        label=_("Nom"),
        required=False,
        widget=forms.TextInput(attrs={
            "class": CSS,
            "placeholder": _("Nom de famille"),
        })
    )
    position = forms.ModelChoiceField(
        label=_("Poste concerné"),
        queryset=None,  # défini dans __init__
        required=False,
        empty_label=_("— Aucun poste —"),
        widget=forms.Select(attrs={"class": CSS}),
    )
    questionnaire_version = forms.ChoiceField(
        label=_("Version du questionnaire"),
        choices=QuestionnaireLink.Version.choices,
        initial="50",
        widget=forms.Select(attrs={"class": CSS})
    )
    language = forms.ChoiceField(
        label=_("Langue du questionnaire"),
        choices=QuestionnaireLink.Language.choices,
        initial="fr",
        widget=forms.Select(attrs={"class": CSS})
    )

    def __init__(self, *args, org=None, **kwargs):
        super().__init__(*args, **kwargs)
        if org:
            from apps.positions.models import Position
            self.fields["position"].queryset = (
                Position.objects.filter(org=org, status="active").order_by("title_fr")
            )
        else:
            from apps.positions.models import Position
            self.fields["position"].queryset = Position.objects.none()

    def clean(self):
        cleaned = super().clean()
        email = cleaned.get("person_email")
        first_name = cleaned.get("first_name", "").strip()
        last_name = cleaned.get("last_name", "").strip()

        if email:
            from apps.teams.models import Person
            # On stocke si la personne existe déjà (utilisé dans la vue)
            self._person_exists = Person.objects.filter(
                org=self._org if hasattr(self, "_org") else None,
                email=email,
            ).exists() if hasattr(self, "_org") else False

            # Si elle n'existe pas, prénom et nom sont obligatoires
            if not self._person_exists:
                if not first_name:
                    self.add_error("first_name", _("Le prénom est requis pour créer la personne."))
                if not last_name:
                    self.add_error("last_name", _("Le nom est requis pour créer la personne."))

        return cleaned

    def set_org(self, org):
        """Permet de passer l'org pour la validation cross-field."""
        self._org = org
