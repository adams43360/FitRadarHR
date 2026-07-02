from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from .models import Position, PositionProfile
from .forms import PositionForm, PositionProfileForm, DIMENSION_LABELS


@login_required
def position_list(request):
    status_filter = request.GET.get("status", "active")
    positions = (
        request.user.org.positions
        .filter(status=status_filter)
        .select_related("profile")
        .order_by("-created_at")
    )
    return render(request, "positions/list.html", {
        "positions": positions,
        "status_filter": status_filter,
    })


@login_required
def position_create(request):
    org = request.user.org
    if request.method == "POST":
        form = PositionForm(request.POST, org=org)
        if form.is_valid():
            position = form.save(commit=False)
            position.org = org
            position.created_by = request.user
            position.save()
            messages.success(request, _("Poste créé avec succès."))
            return redirect("positions:profile_edit", pk=position.pk)
    else:
        form = PositionForm(org=org)
    return render(request, "positions/create.html", {"form": form})


@login_required
def position_detail(request, pk):
    from apps.fit.models import PositionFitResult
    from apps.teams.models import Person

    position = get_object_or_404(Position, pk=pk, org=request.user.org)
    profile_dimensions = []
    if position.has_profile:
        p = position.profile
        for key, meta in DIMENSION_LABELS.items():
            min_val = getattr(p, f"{key}_min")
            max_val = getattr(p, f"{key}_max")
            profile_dimensions.append({
                "label": meta["label"],
                "help": meta["help"],
                "min": min_val,
                "max": max_val,
                "width": max_val - min_val,
            })

    # Classement des personnes par Fit — filtre optionnel par type
    person_type_filter = request.GET.get("type", "")
    fit_qs = (
        PositionFitResult.objects
        .filter(position=position, person__org=request.user.org)
        .select_related("person")
        .order_by("-overall_fit")
    )
    if person_type_filter in (Person.PersonType.CANDIDATE, Person.PersonType.COLLABORATOR):
        fit_qs = fit_qs.filter(person__person_type=person_type_filter)

    return render(request, "positions/detail.html", {
        "position": position,
        "profile_dimensions": profile_dimensions,
        "fit_ranking": fit_qs,
        "person_type_filter": person_type_filter,
        "CANDIDATE": Person.PersonType.CANDIDATE,
        "COLLABORATOR": Person.PersonType.COLLABORATOR,
    })


@login_required
def position_edit(request, pk):
    org = request.user.org
    position = get_object_or_404(Position, pk=pk, org=org)
    if request.method == "POST":
        form = PositionForm(request.POST, instance=position, org=org)
        if form.is_valid():
            form.save()
            messages.success(request, _("Poste mis à jour."))
            return redirect("positions:detail", pk=position.pk)
    else:
        form = PositionForm(instance=position, org=org)
    return render(request, "positions/edit.html", {"form": form, "position": position})


@login_required
def position_archive(request, pk):
    position = get_object_or_404(Position, pk=pk, org=request.user.org)
    if request.method == "POST":
        position.status = Position.Status.ARCHIVED
        position.save()
        messages.success(request, _("Poste archivé."))
        return redirect("positions:list")
    return render(request, "positions/archive_confirm.html", {"position": position})


@login_required
def position_profile_edit(request, pk):
    position = get_object_or_404(Position, pk=pk, org=request.user.org)
    profile = getattr(position, "profile", None)
    if request.method == "POST":
        form = PositionProfileForm(request.POST, instance=profile)
        if form.is_valid():
            profile_obj = form.save(commit=False)
            profile_obj.position = position
            profile_obj.save()
            messages.success(request, _("Profil Big Five enregistré."))
            return redirect("positions:detail", pk=position.pk)
    else:
        form = PositionProfileForm(instance=profile)

    from apps.reports.insights import DIMENSION_TOOLTIPS
    lang = getattr(request, "LANGUAGE_CODE", "fr")[:2]

    # Prépare les dimensions avec leurs champs de formulaire associés
    dimensions = []
    for key, meta in DIMENSION_LABELS.items():
        dimensions.append({
            "key": key,
            "label": meta["label"],
            "help": meta["help"],
            "tooltip": DIMENSION_TOOLTIPS.get(key, {}).get(lang, ""),
            "field_min": form[f"{key}_min"],
            "field_max": form[f"{key}_max"],
            "val_min": form[f"{key}_min"].value() or 0,
            "val_max": form[f"{key}_max"].value() or 100,
        })

    return render(request, "positions/profile_edit.html", {
        "form": form,
        "position": position,
        "dimensions": dimensions,
    })


