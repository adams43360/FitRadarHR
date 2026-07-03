from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, redirect
from django.utils.translation import gettext_lazy as _

from django.utils.http import url_has_allowed_host_and_scheme

from .forms import SignupB2BForm, SignupB2CForm
from .models import Feedback, Organization, User


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
