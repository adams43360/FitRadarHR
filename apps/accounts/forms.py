from django import forms
from django.utils.translation import gettext_lazy as _

from .models import User


class BaseSignupForm(forms.Form):
    """Champs et validations communs aux inscriptions B2B et B2C."""

    first_name = forms.CharField(label=_("Prénom"), max_length=100)
    last_name = forms.CharField(label=_("Nom"), max_length=100)
    email = forms.EmailField(label=_("Email"))
    password1 = forms.CharField(label=_("Mot de passe"), widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Confirmer le mot de passe"), widget=forms.PasswordInput)

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("password1") != cleaned.get("password2"):
            raise forms.ValidationError(_("Les mots de passe ne correspondent pas."))
        return cleaned

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(_("Cet email est déjà utilisé."))
        return email


class SignupB2BForm(BaseSignupForm):
    org_name = forms.CharField(label=_("Nom de l'organisation"), max_length=255)
    email = forms.EmailField(label=_("Email professionnel"))

    field_order = ["org_name", "first_name", "last_name", "email", "password1", "password2"]


class SignupB2CForm(BaseSignupForm):
    pass
