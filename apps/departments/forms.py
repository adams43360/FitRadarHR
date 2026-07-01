from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Department


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ["name_fr", "name_en", "description"]
        widgets = {
            "name_fr": forms.TextInput(attrs={
                "class": "w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500",
                "placeholder": _("Ex. : Recherche & Développement"),
            }),
            "name_en": forms.TextInput(attrs={
                "class": "w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500",
                "placeholder": _("Ex. : Research & Development"),
            }),
            "description": forms.Textarea(attrs={
                "class": "w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500",
                "rows": 3,
                "placeholder": _("Description optionnelle du département"),
            }),
        }
