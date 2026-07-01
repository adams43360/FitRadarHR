from django import forms
from django.utils.translation import gettext_lazy as _
from .models import QuestionnaireLink


class SendLinkForm(forms.Form):
    person_email = forms.EmailField(
        label=_("Email de la personne"),
        widget=forms.EmailInput(attrs={
            "class": "w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500",
            "placeholder": "prenom.nom@exemple.com",
        })
    )
    questionnaire_version = forms.ChoiceField(
        label=_("Version du questionnaire"),
        choices=QuestionnaireLink.Version.choices,
        initial="50",
        widget=forms.Select(attrs={
            "class": "w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500",
        })
    )
    language = forms.ChoiceField(
        label=_("Langue du questionnaire"),
        choices=QuestionnaireLink.Language.choices,
        initial="fr",
        widget=forms.Select(attrs={
            "class": "w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500",
        })
    )
