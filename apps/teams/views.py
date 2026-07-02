from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from core.managers import get_org_object_or_404
from .models import Team, Person, TeamMembership
from .forms import TeamForm, PersonForm, AddMemberForm


# ── Équipes ──────────────────────────────────────────────────────────────────

@login_required
def team_list(request):
    from django.db.models import Count, Q
    teams = (
        request.user.org.teams
        .select_related("manager")
        .annotate(active_member_count=Count(
            "memberships",
            filter=Q(memberships__left_at__isnull=True)
        ))
        .order_by("name")
    )
    return render(request, "teams/list.html", {"teams": teams})


@login_required
def team_create(request):
    if request.method == "POST":
        form = TeamForm(request.POST, org=request.user.org)
        if form.is_valid():
            team = form.save(commit=False)
            team.org = request.user.org
            team.save()
            messages.success(request, _("Équipe créée avec succès."))
            return redirect("teams:detail", pk=team.pk)
    else:
        initial = {}
        if request.user.is_manager:
            initial["manager"] = request.user
        form = TeamForm(org=request.user.org, initial=initial)
    return render(request, "teams/create.html", {"form": form})


@login_required
def team_detail(request, pk):
    team = get_org_object_or_404(Team, request.user.org, pk=pk)
    active_memberships = (
        team.memberships
        .filter(left_at__isnull=True)
        .select_related("person", "added_by")
        .order_by("joined_at")
    )
    add_form = AddMemberForm()
    return render(request, "teams/detail.html", {
        "team": team,
        "active_memberships": active_memberships,
        "add_form": add_form,
    })


@login_required
def team_edit(request, pk):
    team = get_org_object_or_404(Team, request.user.org, pk=pk)
    if request.method == "POST":
        form = TeamForm(request.POST, instance=team, org=request.user.org)
        if form.is_valid():
            form.save()
            messages.success(request, _("Équipe mise à jour."))
            return redirect("teams:detail", pk=team.pk)
    else:
        form = TeamForm(instance=team, org=request.user.org)
    return render(request, "teams/edit.html", {"form": form, "team": team})


# ── Membres ───────────────────────────────────────────────────────────────────

@login_required
def team_add_member(request, pk):
    team = get_org_object_or_404(Team, request.user.org, pk=pk)
    if request.method == "POST":
        form = AddMemberForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            try:
                person = request.user.org.persons.get(email=email)
            except Person.DoesNotExist:
                messages.error(request, _(
                    "Aucune personne avec cet email dans votre organisation. "
                    "Ajoutez-la d'abord depuis la liste des personnes."
                ))
                return redirect("teams:detail", pk=team.pk)

            if team.memberships.filter(person=person, left_at__isnull=True).exists():
                messages.warning(request, _("Cette personne est déjà membre de l'équipe."))
                return redirect("teams:detail", pk=team.pk)

            TeamMembership.objects.create(
                team=team,
                person=person,
                added_by=request.user,
            )
            messages.success(request, _(f"{person.full_name} ajouté(e) à l'équipe."))
    return redirect("teams:detail", pk=team.pk)


@login_required
def team_remove_member(request, pk, membership_pk):
    team = get_org_object_or_404(Team, request.user.org, pk=pk)
    membership = get_object_or_404(TeamMembership, pk=membership_pk, team=team, left_at__isnull=True)
    if request.method == "POST":
        membership.left_at = timezone.now()
        membership.save()
        messages.success(request, _(f"{membership.person.full_name} retiré(e) de l'équipe."))
    return redirect("teams:detail", pk=team.pk)


# ── Personnes ─────────────────────────────────────────────────────────────────

@login_required
def person_list(request):
    persons = request.user.org.persons.order_by("last_name", "first_name")
    return render(request, "teams/person_list.html", {"persons": persons})


@login_required
def person_create(request):
    if request.method == "POST":
        form = PersonForm(request.POST)
        if form.is_valid():
            person = form.save(commit=False)
            person.org = request.user.org
            person.created_by = request.user
            try:
                person.save()
                messages.success(request, _("Personne ajoutée avec succès."))
                return redirect("teams:persons")
            except Exception:
                messages.error(request, _("Cette adresse email est déjà enregistrée dans votre organisation."))
    else:
        form = PersonForm()
    return render(request, "teams/person_create.html", {"form": form})


# ── RGPD — Droit à l'effacement ───────────────────────────────────────────────

@login_required
def person_anonymize(request, pk):
    """Anonymise les PII d'une personne (droit à l'effacement RGPD)."""
    from apps.reports.models import AuditLog
    person = get_org_object_or_404(Person, request.user.org, pk=pk)

    if not request.user.is_rh:
        messages.error(request, _("Vous n'avez pas les droits pour effectuer cette action."))
        return redirect("teams:persons")

    if request.method == "POST":
        person_name = person.full_name
        person.anonymize()
        AuditLog.objects.create(
            org=request.user.org,
            user=request.user,
            action="person.anonymized",
            entity_type="Person",
            entity_id=person.pk,
            metadata={"name": person_name},
        )
        messages.success(request, _("Les données personnelles ont été anonymisées."))
        return redirect("teams:persons")

    return render(request, "teams/person_anonymize_confirm.html", {"person": person})


# ── Autocomplétion membres ────────────────────────────────────────────────────

@login_required
def member_search(request, pk):
    """Retourne en JSON les personnes de l'org matching la query, hors membres actifs."""
    import json
    from django.http import JsonResponse
    from django.db.models import Q

    team = get_org_object_or_404(Team, request.user.org, pk=pk)
    q = request.GET.get("q", "").strip()

    if len(q) < 2:
        return JsonResponse([], safe=False)

    # Exclure les membres actifs
    active_member_ids = team.memberships.filter(
        left_at__isnull=True
    ).values_list("person_id", flat=True)

    persons = (
        request.user.org.persons
        .exclude(pk__in=active_member_ids)
        .filter(
            Q(first_name__icontains=q) |
            Q(last_name__icontains=q) |
            Q(email__icontains=q)
        )
        .order_by("last_name", "first_name")[:8]
    )

    results = [
        {"name": p.full_name, "email": p.email}
        for p in persons
    ]
    return JsonResponse(results, safe=False)


# ── Modification d'une personne ───────────────────────────────────────────────

@login_required
def person_edit(request, pk):
    person = get_org_object_or_404(Person, request.user.org, pk=pk)
    if request.method == "POST":
        form = PersonForm(request.POST, instance=person)
        if form.is_valid():
            # Vérifier unicité email en excluant la personne courante
            email = form.cleaned_data["email"]
            if (
                request.user.org.persons
                .filter(email=email)
                .exclude(pk=person.pk)
                .exists()
            ):
                form.add_error("email", _("Cette adresse email est déjà utilisée dans votre organisation."))
            else:
                form.save()
                messages.success(request, _("Données mises à jour."))
                return redirect("teams:persons")
    else:
        form = PersonForm(instance=person)
    return render(request, "teams/person_edit.html", {"form": form, "person": person})
