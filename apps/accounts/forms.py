from django import forms
from django.utils.translation import gettext_lazy as _

from .models import OrgSSOConfig, User


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


class InviteManagerForm(forms.Form):
    """Invitation d'un manager dans l'organisation (RH only)."""
    first_name = forms.CharField(label=_("Prénom"), max_length=100)
    last_name = forms.CharField(label=_("Nom"), max_length=100)
    email = forms.EmailField(label=_("Email professionnel"))

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(_("Cet email est déjà utilisé par un compte existant."))
        return email


class OrgSSOConfigForm(forms.ModelForm):
    """Configuration SSO OIDC de l'organisation — RH only (item #7 roadmap V2).

    Le `client_secret` est write-only : le champ est toujours vide à
    l'affichage, une valeur laissée vide à la sauvegarde conserve le secret
    déjà enregistré (pas de ré-affichage, pas de perte accidentelle).
    """

    client_secret = forms.CharField(
        label=_("Client secret"), required=False,
        widget=forms.PasswordInput(render_value=False),
        help_text=_("Laisser vide pour conserver le secret déjà enregistré."),
    )

    class Meta:
        model = OrgSSOConfig
        fields = ["display_name", "login_slug", "issuer_url", "client_id", "client_secret", "enabled"]
        labels = {
            "display_name": _("Nom d'affichage"),
            "login_slug": _("Identifiant de connexion"),
            "issuer_url": _("URL d'émetteur OIDC"),
            "client_id": _("Client ID"),
            "enabled": _("Activé"),
        }

    def __init__(self, *args, **kwargs):
        self._org = kwargs.pop("org")
        super().__init__(*args, **kwargs)

    def clean_login_slug(self):
        slug = self.cleaned_data["login_slug"].strip().lower()
        qs = OrgSSOConfig.objects.exclude(org=self._org)
        if qs.filter(login_slug=slug).exists():
            raise forms.ValidationError(
                _("Cet identifiant de connexion est déjà utilisé par une autre organisation.")
            )
        return slug

    def clean_client_secret(self):
        secret = self.cleaned_data.get("client_secret")
        if not secret:
            if self.instance and self.instance.pk:
                return self.instance.client_secret  # conserve le secret existant
            raise forms.ValidationError(_("Le client secret est obligatoire à la création."))
        return secret


class ApiKeyGenerateForm(forms.Form):
    """Génération d'une clé API publique — RH only (item #9 roadmap V2, US-E1-06)."""

    name = forms.CharField(
        label=_("Nom de la clé"),
        max_length=100,
        help_text=_("Pour vous y retrouver, ex. « Intégration ATS Greenhouse »."),
    )
