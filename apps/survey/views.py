import secrets
from datetime import timedelta

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from apps.fit.models import BigFiveProfile
from apps.teams.models import Person

from .forms import SendLinkForm
from .ipip_data import ITEMS, SCALE_EN, SCALE_FR
from .models import ConsentRecord, QuestionnaireLink, QuestionnaireSession
from .scoring import ALGORITHM_VERSION, compute_scores, validate_answers
from apps.fit.engine import compute_all_fits_for_person

BLOCK_SIZE = 10
LINK_VALIDITY_DAYS = 7


# ──────────────────────────────────────────────────────────────────────────────
# Dashboard (RH / manager)
# ──────────────────────────────────────────────────────────────────────────────

@login_required
def survey_dashboard(request):
    # Tous les liens triés par date décroissante — on déduplique par personne en Python
    # pour ne garder que le plus récent par personne
    all_links = (
        QuestionnaireLink.objects
        .filter(org=request.user.org)
        .select_related("person", "sent_by")
        .order_by("-sent_at")
    )
    seen = set()
    links = []
    for link in all_links:
        if link.person_id not in seen:
            seen.add(link.person_id)
            links.append(link)

    return render(request, "survey/dashboard.html", {"links": links})


# ──────────────────────────────────────────────────────────────────────────────
# Envoi d'un lien
# ──────────────────────────────────────────────────────────────────────────────

@login_required
def send_questionnaire(request):
    initial = {}
    if email := request.GET.get("email"):
        initial["person_email"] = email
    form = SendLinkForm(initial=initial)

    if request.method == "POST":
        form = SendLinkForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["person_email"]
            version = form.cleaned_data["questionnaire_version"]
            language = form.cleaned_data["language"]

            try:
                person = Person.objects.get(org=request.user.org, email=email)
            except Person.DoesNotExist:
                form.add_error(
                    "person_email",
                    _("Aucune personne trouvée avec cet email dans votre organisation. "
                      "Créez-la d'abord dans la liste des Personnes.")
                )
                return render(request, "survey/send.html", {"form": form})

            link = QuestionnaireLink.objects.create(
                org=request.user.org,
                person=person,
                token=secrets.token_urlsafe(48),
                questionnaire_version=version,
                language=language,
                sent_by=request.user,
                expires_at=timezone.now() + timedelta(days=LINK_VALIDITY_DAYS),
            )
            _send_invitation_email(link, request)
            messages.success(request, _("Lien envoyé à %(email)s.") % {"email": email})
            return redirect("survey:dashboard")

    return render(request, "survey/send.html", {"form": form})


@login_required
def resend_link(request, pk):
    link = get_object_or_404(QuestionnaireLink, pk=pk, org=request.user.org)
    if link.status == QuestionnaireLink.Status.COMPLETED:
        messages.error(request, _("Ce questionnaire est déjà complété."))
    else:
        link.expires_at = timezone.now() + timedelta(days=LINK_VALIDITY_DAYS)
        link.status = QuestionnaireLink.Status.PENDING
        link.save()
        _send_invitation_email(link, request)
        messages.success(request, _("Lien renvoyé à %(email)s.") % {"email": link.person.email})
    return redirect("survey:dashboard")


# ──────────────────────────────────────────────────────────────────────────────
# Passation publique (sans compte)
# ──────────────────────────────────────────────────────────────────────────────

def _get_valid_link(token):
    """Renvoie le lien s'il est valide, None sinon."""
    try:
        link = QuestionnaireLink.objects.select_related("person").get(token=token)
    except QuestionnaireLink.DoesNotExist:
        return None
    if link.expires_at < timezone.now():
        link.status = QuestionnaireLink.Status.EXPIRED
        link.save()
        return None
    if link.status == QuestionnaireLink.Status.COMPLETED:
        return None
    return link


def questionnaire_start(request, token):
    """Étape 1 : consentement RGPD."""
    link = _get_valid_link(token)
    if link is None:
        return render(request, "survey/expired.html", {"token": token})

    if hasattr(link, "consent"):
        return redirect("survey:questions", token=token, block=0)

    if request.method == "POST" and request.POST.get("consent") == "yes":
        ip = request.META.get("HTTP_X_FORWARDED_FOR", request.META.get("REMOTE_ADDR", ""))
        ip = ip.split(",")[0].strip() if ip else None
        ConsentRecord.objects.create(
            link=link,
            ip_address=ip,
            language=link.language,
        )
        QuestionnaireSession.objects.get_or_create(link=link)
        link.status = QuestionnaireLink.Status.IN_PROGRESS
        link.save()
        return redirect("survey:questions", token=token, block=0)

    return render(request, "survey/consent.html", {
        "link": link,
        "person": link.person,
    })


def questionnaire_questions(request, token, block):
    """Étape 2 : blocs de questions."""
    link = _get_valid_link(token)
    if link is None:
        return render(request, "survey/expired.html", {"token": token})

    if not hasattr(link, "consent"):
        return redirect("survey:start", token=token)

    session, _ = QuestionnaireSession.objects.get_or_create(link=link)

    n_items = int(link.questionnaire_version)
    items_for_version = ITEMS[:n_items]
    total_blocks = (n_items + BLOCK_SIZE - 1) // BLOCK_SIZE

    if block < 0 or block >= total_blocks:
        return redirect("survey:questions", token=token, block=0)

    block_items = [
        {**item, "current_answer": session.answers.get(item["id"])}
        for item in items_for_version[block * BLOCK_SIZE: (block + 1) * BLOCK_SIZE]
    ]
    scale = SCALE_FR if link.language == "fr" else SCALE_EN

    if request.method == "POST":
        for item in block_items:
            val = request.POST.get(f"item_{item['id']}")
            if val and val.isdigit() and int(val) in (1, 2, 3, 4, 5):
                session.answers[item["id"]] = int(val)
        session.current_item_index = (block + 1) * BLOCK_SIZE
        session.save()

        missing = [i["id"] for i in block_items if i["id"] not in session.answers]
        if missing:
            error_msg = _("Veuillez répondre à toutes les questions avant de continuer.")
            return render(request, "survey/questions.html", {
                "link": link,
                "items": block_items,
                "scale": scale,
                "block": block,
                "total_blocks": total_blocks,
                "answers": session.answers,
                "error": error_msg,
            })

        next_block = block + 1
        if next_block < total_blocks:
            return redirect("survey:questions", token=token, block=next_block)
        else:
            return redirect("survey:submit", token=token)

    return render(request, "survey/questions.html", {
        "link": link,
        "items": block_items,
        "scale": scale,
        "block": block,
        "total_blocks": total_blocks,
        "answers": session.answers,
        "error": None,
    })


def questionnaire_submit(request, token):
    """Étape 3 : calcul des scores et sauvegarde."""
    link = _get_valid_link(token)
    if link is None:
        return render(request, "survey/expired.html", {"token": token})

    if not hasattr(link, "consent"):
        return redirect("survey:start", token=token)

    try:
        session = link.session
    except QuestionnaireSession.DoesNotExist:
        return redirect("survey:start", token=token)

    errors = validate_answers(session.answers, version=link.questionnaire_version)
    if errors:
        return redirect("survey:questions", token=token, block=0)

    scores = compute_scores(session.answers)

    BigFiveProfile.objects.update_or_create(
        person=link.person,
        defaults={
            "link": link,
            "openness": scores["openness"],
            "conscientiousness": scores["conscientiousness"],
            "extraversion": scores["extraversion"],
            "agreeableness": scores["agreeableness"],
            "neuroticism": scores["neuroticism"],
            "questionnaire_version": link.questionnaire_version,
            "algorithm_version": ALGORITHM_VERSION,
        },
    )

    link.status = QuestionnaireLink.Status.COMPLETED
    link.completed_at = timezone.now()
    link.save()

    session.delete()

    # Calcul des scores de fit pour tous les postes et équipes de l'org (E5)
    compute_all_fits_for_person(link.person)

    _send_completion_notification(link)

    return redirect("survey:done", token=token)


def questionnaire_done(request, token):
    """Page de fin."""
    try:
        link = QuestionnaireLink.objects.select_related("person").get(token=token)
    except QuestionnaireLink.DoesNotExist:
        return render(request, "survey/expired.html", {"token": token})

    return render(request, "survey/done.html", {"link": link, "person": link.person})


# ──────────────────────────────────────────────────────────────────────────────
# Helpers email
# ──────────────────────────────────────────────────────────────────────────────

def _send_invitation_email(link, request):
    survey_url = request.build_absolute_uri(reverse("survey:start", kwargs={"token": link.token}))
    subject = (
        "Votre questionnaire de personnalité Big Five"
        if link.language == "fr"
        else "Your Big Five personality questionnaire"
    )
    body = render_to_string("survey/emails/invitation.txt", {
        "link": link,
        "person": link.person,
        "survey_url": survey_url,
        "validity_days": LINK_VALIDITY_DAYS,
    })
    send_mail(
        subject=subject,
        message=body,
        from_email=None,
        recipient_list=[link.person.email],
        fail_silently=False,
    )


def _send_completion_notification(link):
    if not link.sent_by or not link.sent_by.email:
        return
    body = render_to_string("survey/emails/completion.txt", {
        "link": link,
        "person": link.person,
        "sent_by": link.sent_by,
    })
    send_mail(
        subject=f"Questionnaire complété — {link.person.full_name}",
        message=body,
        from_email=None,
        recipient_list=[link.sent_by.email],
        fail_silently=True,
    )
