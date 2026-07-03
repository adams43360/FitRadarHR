from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Team, Person, TeamMembership


class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ["name", "department", "description", "manager"]
        widgets = {
            "name": forms.TextInput(attrs={
                "class": "w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500",
                "placeholder": _("Ex. : Équipe produit, Sales EMEA…"),
            }),
            "department": forms.Select(attrs={
                "class": "w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500",
            }),
            "description": forms.Textarea(attrs={
                "class": "w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500",
                "rows": 3,
                "placeholder": _("Contexte, missions de l'équipe… (optionnel)"),
            }),
            "manager": forms.Select(attrs={
                "class": "w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500",
            }),
        }

    def __init__(self, *args, org=None, **kwargs):
        super().__init__(*args, **kwargs)
        if org:
            from apps.departments.models import Department
            self.fields["manager"].queryset = org.users.filter(is_active=True)
            self.fields["manager"].label_from_instance = lambda u: u.full_name
            self.fields["department"].queryset = Department.objects.for_org(org).active()
        else:
            from apps.departments.models import Department
            self.fields["department"].queryset = Department.objects.none()
        self.fields["manager"].required = False
        self.fields["manager"].empty_label = _("— Aucun manager assigné —")
        self.fields["department"].required = False
        self.fields["department"].empty_label = _("— Aucun département —")


class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ["first_name", "last_name", "email", "person_type"]
        widgets = {
            "first_name": forms.TextInput(attrs={
                "class": "w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500",
            }),
            "last_name": forms.TextInput(attrs={
                "class": "w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500",
            }),
            "email": forms.EmailInput(attrs={
                "class": "w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500",
            }),
            "person_type": forms.Select(attrs={
                "class": "w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500",
            }),
        }


class PersonImportForm(forms.Form):
    """Import en masse de personnes via un fichier CSV."""
    csv_file = forms.FileField(
        label=_("Fichier CSV"),
        widget=forms.ClearableFileInput(attrs={
            "class": "w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500",
            "accept": ".csv",
        }),
    )

    def clean_csv_file(self):
        f = self.cleaned_data["csv_file"]
        if not f.name.lower().endswith(".csv"):
            raise forms.ValidationError(_("Le fichier doit être au format .csv"))
        if f.size > 2 * 1024 * 1024:  # 2 Mo — largement suffisant, évite les abus
            raise forms.ValidationError(_("Le fichier est trop volumineux (2 Mo max)."))
        return f


class AddMemberForm(forms.Form):
    """Ajouter une personne existante (par email) à une équipe."""
    email = forms.EmailField(
        label=_("Email de la personne"),
        widget=forms.EmailInput(attrs={
            "class": "w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500",
            "placeholder": _("prenom.nom@exemple.com"),
        })
    )
