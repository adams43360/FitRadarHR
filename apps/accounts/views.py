from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext_lazy as _
from django import forms
from .models import Organization, User


# ─── Formulaires ──────────────────────────────────────────────────────────────

class SignupB2BForm(forms.Form):
    org_name = forms.CharField(label=_("Nom de l'organisation"), max_length=255)
    first_name = forms.CharField(label=_("Prénom"), max_length=100)
    last_name = forms.CharField(label=_("Nom"), max_length=100)
    email = forms.EmailField(label=_("Email professionnel"))
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


class SignupB2CForm(forms.Form):
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


# ─── Vues ─────────────────────────────────────────────────────────────────────

def signup_choice(request):
    """Page d'accueil — choix B2B ou B2C."""
    if request.user.is_authenticated:
        return redirect("accounts:dashboard")
    return render(request, "accounts/signup_choice.html")


def signup_b2b(request):
    """Inscription organisation (B2B)."""
    if request.user.is_authenticated:
        return redirect("accounts:dashboard")

    form = SignupB2BForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        d = form.cleaned_data
        org = Organization.objects.create(
            name=d["org_name"],
            account_type=Organization.AccountType.B2B,
        )
        user = User.objects.create_user(
            email=d["email"],
            password=d["password1"],
            first_name=d["first_name"],
            last_name=d["last_name"],
            org=org,
            role=User.Role.RH,
        )
        login(request, user, backend="django.contrib.auth.backends.ModelBackend")
        return redirect("accounts:dashboard")

    return render(request, "accounts/signup_b2b.html", {"form": form})


def signup_b2c(request):
    """Inscription individuelle (B2C)."""
    if request.user.is_authenticated:
        return redirect("accounts:dashboard")

    form = SignupB2CForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        d = form.cleaned_data
        org = Organization.objects.create(
            name=f"Espace de {d['first_name']}",
            account_type=Organization.AccountType.B2C,
        )
        user = User.objects.create_user(
            email=d["email"],
            password=d["password1"],
            first_name=d["first_name"],
            last_name=d["last_name"],
            org=org,
            role=User.Role.SOLO,
        )
        login(request, user, backend="django.contrib.auth.backends.ModelBackend")
        return redirect("accounts:dashboard")

    return render(request, "accounts/signup_b2c.html", {"form": form})


@login_required
def dashboard(request):
    user = request.user
    org = user.org
    context = {
        "org": org,
        "positions_count": org.positions.filter(status="active").count(),
        "teams_count": org.teams.count(),
        "persons_count": org.persons.count(),
    }
    return render(request, "accounts/dashboard.html", context)
