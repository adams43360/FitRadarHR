from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from .models import Team, Person, TeamMembership
from .forms import TeamForm, PersonForm, AddMemberForm


# ── Équipes ──────────────────────────────────────────────────────────────────

@login_required
def team_list(request):
    teams = (
        request.user.org.teams
        .select_related("manager")
        .prefetch_related("memberships")
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
    team = get_object_or_404(Team, pk=pk, org=request.user.org)
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
    team = get_object_or_404(Team, pk=pk, org=request.user.org)
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
    team = get_object_or_404(Team, pk=pk, org=request.user.org)
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
    team = get_object_or_404(Team, pk=pk, org=request.user.org)
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
