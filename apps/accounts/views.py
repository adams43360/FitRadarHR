from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseForbidden
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from django.utils.http import url_has_allowed_host_and_scheme

from apps.api.models import ApiKey
from apps.billing.models import Subscription

from .forms import ApiKeyGenerateForm, InviteManagerForm, OrgSSOConfigForm, SignupB2BForm, SignupB2CForm
from .models import Feedback, Organization, OrgSSOConfig, User


# ─── Vues ─────────────────────────────────────────────────────────────────────

def landing(request):
    """Page d'accueil publique — présentation du produit."""
    if request.user.is_authenticated:
        return redirect("accounts:dashboard")
    return render(request, "accounts/landing.html")


def signup_choice(request):
    """Choix du type de compte — B2B ou B2C."""
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
        Subscription.start_trial(org)
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
        Subscription.start_trial(org)
        login(request, user, backend="django.contrib.auth.backends.ModelBackend")
        return redirect("accounts:dashboard")

    return render(request, "accounts/signup_b2c.html", {"form": form})


def demo_login(request):
    """Connexion un clic sur le compte de démonstration (bouton "Essayer la démo").

    Uniquement disponible si DEMO_MODE est activé et que l'org démo existe
    (créée par `manage.py seed_demo`). Le compte démo n'a pas de mot de passe
    utilisable : ce bouton est le seul moyen de s'y connecter.
    """
    if not settings.DEMO_MODE:
        raise Http404
    if request.method != "POST":
        return redirect("accounts:login")

    user = User.objects.filter(
        org__is_demo=True,
        email=settings.DEMO_USER_EMAIL,
        is_active=True,
    ).first()
    if user is None:
        messages.error(request, _("La démonstration n'est pas disponible pour le moment."))
        return redirect("accounts:login")

    login(request, user, backend="django.contrib.auth.backends.ModelBackend")
    return redirect("accounts:dashboard")


@login_required
def dashboard(request):
    from apps.survey.models import QuestionnaireLink
    from apps.fit.models import BigFiveProfile, PositionFitResult
    from apps.reports.models import AuditLog
    from django.db.models import Avg

    user = request.user
    org = user.org

    # Stats principales
    positions_count = org.positions.filter(status="active").count()
    teams_count = org.teams.count()
    persons_count = org.persons.count()
    profiles_count = BigFiveProfile.objects.for_org(org).count()

    # Questionnaires en attente — on déduplique par personne (même logique que survey:dashboard)
    # pour ne garder que le lien le plus récent par personne, puis on filtre les non-complétés
    all_links = (
        QuestionnaireLink.objects.for_org(org)
        .select_related("person")
        .order_by("-sent_at")
    )
    seen = set()
    deduped_links = []
    for lnk in all_links:
        if lnk.person_id not in seen:
            seen.add(lnk.person_id)
            deduped_links.append(lnk)

    pending_links = [
        lnk for lnk in deduped_links
        if lnk.status != QuestionnaireLink.Status.COMPLETED
    ]
    pending_count = len(pending_links)
    pending_links = pending_links[:5]

    # Derniers profils complétés
    recent_profiles = (
        BigFiveProfile.objects.for_org(org)
        .select_related("person")
        .order_by("-computed_at")[:5]
    )

    # Score de fit moyen (tous postes)
    avg_position_fit = (
        PositionFitResult.objects.for_org(org)
        .aggregate(avg=Avg("overall_fit"))["avg"]
    )
    if avg_position_fit is not None:
        avg_position_fit = round(float(avg_position_fit), 1)

    # Activité récente (audit log)
    recent_activity = (
        AuditLog.objects.for_org(org)
        .select_related("user")
        .order_by("-created_at")[:8]
    )

    context = {
        "org": org,
        "positions_count": positions_count,
        "teams_count": teams_count,
        "persons_count": persons_count,
        "profiles_count": profiles_count,
        "pending_links": pending_links,
        "pending_count": pending_count,
        "recent_profiles": recent_profiles,
        "avg_position_fit": avg_position_fit,
        "recent_activity": recent_activity,
    }
    return render(request, "accounts/dashboard.html", context)


@login_required
def privacy_policy(request):
    return render(request, "accounts/privacy_policy.html")


# ──────────────────────────────────────────────────────────────────────────────
# Membres de l'organisation — invitation de managers (item #2 de la roadmap V2)
# ──────────────────────────────────────────────────────────────────────────────

def _send_manager_invitation(user, request):
    """Envoie un email de définition de mot de passe via le flux allauth existant
    (aucun nouveau système de token — on réutilise le "mot de passe oublié")."""
    from allauth.account.forms import ResetPasswordForm

    form = ResetPasswordForm({"email": user.email})
    if form.is_valid():
        form.save(request)


@login_required
def org_members(request):
    """Liste des membres de l'organisation + invitation d'un manager — RH only.

    Le compte invité est créé sans mot de passe utilisable ; l'invité reçoit un
    email (flux "mot de passe oublié" d'allauth) pour définir le sien et se connecter.
    """
    if not request.user.is_rh:
        return HttpResponseForbidden()

    if request.method == "POST":
        form = InviteManagerForm(request.POST)
        if form.is_valid():
            d = form.cleaned_data
            user = User.objects.create_user(
                email=d["email"],
                password=None,  # → set_unusable_password()
                first_name=d["first_name"],
                last_name=d["last_name"],
                org=request.user.org,
                role=User.Role.MANAGER,
                invited_by=request.user,
            )
            _send_manager_invitation(user, request)
            messages.success(
                request,
                _("Invitation envoyée à %(email)s.") % {"email": user.email}
            )
            return redirect("accounts:members")
    else:
        form = InviteManagerForm()

    members = request.user.org.users.select_related("invited_by").order_by("-created_at")
    return render(request, "accounts/members.html", {"members": members, "form": form})


# ──────────────────────────────────────────────────────────────────────────────
# Configuration SSO OIDC — item #7 de la roadmap V2 (US-E1-05)
# ──────────────────────────────────────────────────────────────────────────────

@login_required
def sso_config(request):
    """Configuration du fournisseur d'identité (Keycloak/OIDC) de l'org — RH only.

    Le SSO s'ajoute à la connexion email/mot de passe, il ne la remplace
    jamais. Chaque org configure son propre IdP (isolation multi-tenant).
    """
    if not request.user.is_rh:
        return HttpResponseForbidden()

    org = request.user.org
    instance = OrgSSOConfig.objects.filter(org=org).first()

    if request.method == "POST":
        form = OrgSSOConfigForm(request.POST, instance=instance, org=org)
        if form.is_valid():
            config = form.save(commit=False)
            config.org = org
            config.save()
            messages.success(request, _("Configuration SSO enregistrée."))
            return redirect("accounts:sso_config")
    else:
        form = OrgSSOConfigForm(instance=instance, org=org)

    return render(request, "accounts/sso_config.html", {"form": form, "config": instance})


def sso_login_entry(request):
    """Point d'entrée SSO public — demande l'identifiant de connexion de
    l'organisation, puis redirige vers son fournisseur OIDC."""
    if request.method == "POST":
        slug = request.POST.get("login_slug", "").strip().lower()
        config = OrgSSOConfig.objects.filter(login_slug=slug, enabled=True).first()
        if config is not None:
            return redirect("openid_connect_login", provider_id=config.login_slug)
        messages.error(
            request, _("Aucune organisation active ne correspond à cet identifiant.")
        )

    return render(request, "accounts/sso_login_entry.html")


# ──────────────────────────────────────────────────────────────────────────────
# Clés API — item #9 de la roadmap V2 (API publique en lecture seule, US-E1-06)
# ──────────────────────────────────────────────────────────────────────────────

@login_required
def api_keys_settings(request):
    """Gestion des clés API de l'org — RH only.

    La valeur en clair d'une clé n'est affichée qu'une seule fois, juste après
    sa génération (`request.session["_new_api_key"]`, consommée immédiatement
    au rendu pour ne jamais persister en clair nulle part)."""
    if not request.user.is_rh:
        return HttpResponseForbidden()

    org = request.user.org

    if request.method == "POST":
        action = request.POST.get("action")
        if action == "generate":
            form = ApiKeyGenerateForm(request.POST)
            if form.is_valid():
                instance, raw_key = ApiKey.generate(
                    org=org, name=form.cleaned_data["name"], created_by=request.user,
                )
                request.session["_new_api_key"] = raw_key
                request.session["_new_api_key_id"] = str(instance.id)
                messages.success(request, _("Clé API générée."))
                return redirect("accounts:api_keys_settings")
        elif action == "revoke":
            key = ApiKey.objects.for_org(org).filter(pk=request.POST.get("key_id")).first()
            if key is not None and key.is_active:
                key.revoke()
                messages.success(request, _("Clé API révoquée."))
            return redirect("accounts:api_keys_settings")
    else:
        form = ApiKeyGenerateForm()

    new_key_id = request.session.pop("_new_api_key_id", None)
    new_raw_key = request.session.pop("_new_api_key", None) if new_key_id else None

    keys = ApiKey.objects.for_org(org)

    return render(request, "accounts/api_keys.html", {
        "form": form,
        "keys": keys,
        "new_raw_key": new_raw_key,
    })


# ──────────────────────────────────────────────────────────────────────────────
# Facturation — essai gratuit et abonnement (item #2 roadmap V3, US-E1-07)
# ──────────────────────────────────────────────────────────────────────────────

@login_required
def billing_settings(request):
    """Statut de l'essai/abonnement de l'org — RH only.

    N'expose le bouton "S'abonner" que si Stripe est configuré
    (`STRIPE_SECRET_KEY`/`STRIPE_PRICE_ID`) — sinon affiche un message
    "configuration requise" plutôt que de planter."""
    if not request.user.is_rh:
        return HttpResponseForbidden()

    from apps.billing import stripe_client
    from apps.billing.models import Subscription

    org = request.user.org
    subscription = Subscription.get_or_create_for_org(org)

    return render(request, "accounts/billing.html", {
        "subscription": subscription,
        "stripe_configured": stripe_client.is_configured(),
    })


@login_required
def billing_checkout(request):
    if not request.user.is_rh:
        return HttpResponseForbidden()
    if request.method != "POST":
        return redirect("accounts:billing_settings")

    from apps.billing import stripe_client
    if not stripe_client.is_configured():
        messages.error(request, _("La facturation Stripe n'est pas configurée."))
        return redirect("accounts:billing_settings")

    session = stripe_client.create_checkout_session(
        request.user.org,
        success_url=request.build_absolute_uri(reverse("accounts:billing_settings")),
        cancel_url=request.build_absolute_uri(reverse("accounts:billing_settings")),
    )
    return redirect(session.url)


@login_required
def billing_portal(request):
    if not request.user.is_rh:
        return HttpResponseForbidden()
    if request.method != "POST":
        return redirect("accounts:billing_settings")

    from apps.billing import stripe_client
    if not stripe_client.is_configured():
        messages.error(request, _("La facturation Stripe n'est pas configurée."))
        return redirect("accounts:billing_settings")

    session = stripe_client.create_portal_session(
        request.user.org,
        return_url=request.build_absolute_uri(reverse("accounts:billing_settings")),
    )
    if session is None:
        messages.error(request, _("Aucun abonnement à gérer pour le moment."))
        return redirect("accounts:billing_settings")
    return redirect(session.url)


@login_required
def submit_feedback(request):
    """Widget de feedback in-app — un message libre, rattaché à l'org et à la page."""
    next_url = request.POST.get("next", "")
    if not url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
        next_url = "/dashboard/"

    if request.method != "POST":
        return redirect(next_url)

    message = request.POST.get("message", "").strip()
    if not message:
        messages.error(request, _("Votre message est vide."))
        return redirect(next_url)

    Feedback.objects.create(
        org=request.user.org,
        user=request.user,
        message=message[:2000],
        page=next_url[:255],
    )
    messages.success(request, _("Merci pour votre retour ! Il alimente directement la roadmap."))
    return redirect(next_url)
