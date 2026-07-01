from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Position, PositionProfile


class PositionForm(forms.ModelForm):
    class Meta:
        model = Position
        fields = ["title_fr", "title_en", "description_fr", "description_en", "department"]
        widgets = {
            "title_fr": forms.TextInput(attrs={
                "class": "w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500",
                "placeholder": _("Ex. : Chargé(e) de recrutement"),
            }),
            "title_en": forms.TextInput(attrs={
                "class": "w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500",
                "placeholder": "e.g. Recruitment Officer",
            }),
            "description_fr": forms.Textarea(attrs={
                "class": "w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500",
                "rows": 3,
                "placeholder": _("Contexte, missions principales..."),
            }),
            "description_en": forms.Textarea(attrs={
                "class": "w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500",
                "rows": 3,
                "placeholder": "Context, main responsibilities...",
            }),
            "department": forms.TextInput(attrs={
                "class": "w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500",
                "placeholder": _("Ex. : Ressources humaines"),
            }),
        }


DIMENSION_LABELS = {
    "openness": {
        "label": _("Ouverture à l'expérience (O)"),
        "help": _("Curiosité intellectuelle, créativité, goût pour la nouveauté et l'innovation."),
    },
    "conscientiousness": {
        "label": _("Conscience / Rigueur (C)"),
        "help": _("Organisation, fiabilité, sens des responsabilités et autodiscipline."),
    },
    "extraversion": {
        "label": _("Extraversion (E)"),
        "help": _("Sociabilité, assertivité, énergie dans les interactions sociales."),
    },
    "agreeableness": {
        "label": _("Agréabilité (A)"),
        "help": _("Coopération, empathie, confiance et souci du collectif."),
    },
    "neuroticism": {
        "label": _("Stabilité émotionnelle (N)"),
        "help": _("Calme, gestion du stress et résistance aux émotions négatives. Un score faible indique une grande stabilité."),
    },
}


class PositionProfileForm(forms.ModelForm):
    class Meta:
        model = PositionProfile
        fields = [
            "openness_min", "openness_max",
            "conscientiousness_min", "conscientiousness_max",
            "extraversion_min", "extraversion_max",
            "agreeableness_min", "agreeableness_max",
            "neuroticism_min", "neuroticism_max",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        slider_attrs = {
            "type": "range",
            "min": "0",
            "max": "100",
            "step": "5",
            "class": "w-full accent-indigo-600",
        }
        for field_name in self.fields:
            self.fields[field_name].widget = forms.NumberInput(attrs={
                **slider_attrs,
                "x-on:input": f"$refs.{field_name}_val.textContent = $event.target.value",
            })

    def clean(self):
        cleaned = super().clean()
        dimensions = ["openness", "conscientiousness", "extraversion", "agreeableness", "neuroticism"]
        for dim in dimensions:
            min_val = cleaned.get(f"{dim}_min")
            max_val = cleaned.get(f"{dim}_max")
            if min_val is not None and max_val is not None and min_val > max_val:
                self.add_error(f"{dim}_max", _("Le maximum doit être supérieur ou égal au minimum."))
        return cleaned
