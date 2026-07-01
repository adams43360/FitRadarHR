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
    if request.method == "POST":
        form = PositionForm(request.POST)
        if form.is_valid():
            position = form.save(commit=False)
            position.org = request.user.org
            position.created_by = request.user
            position.save()
            messages.success(request, _("Poste créé avec succès."))
            return redirect("positions:profile_edit", pk=position.pk)
    else:
        form = PositionForm()
    departments = (
        request.user.org.positions
        .exclude(department="")
        .values_list("department", flat=True)
        .distinct()
        .order_by("department")
    )
    return render(request, "positions/create.html", {"form": form, "departments": departments})


@login_required
def position_detail(request, pk):
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
    return render(request, "positions/detail.html", {
        "position": position,
        "profile_dimensions": profile_dimensions,
    })


@login_required
def position_edit(request, pk):
    position = get_object_or_404(Position, pk=pk, org=request.user.org)
    if request.method == "POST":
        form = PositionForm(request.POST, instance=position)
        if form.is_valid():
            form.save()
            messages.success(request, _("Poste mis à jour."))
            return redirect("positions:detail", pk=position.pk)
    else:
        form = PositionForm(instance=position)
    departments = (
        request.user.org.positions
        .exclude(department="")
        .values_list("department", flat=True)
        .distinct()
        .order_by("department")
    )
    return render(request, "positions/edit.html", {"form": form, "position": position, "departments": departments})


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

    # Prépare les dimensions avec leurs champs de formulaire associés
    dimensions = []
    for key, meta in DIMENSION_LABELS.items():
        dimensions.append({
            "key": key,
            "label": meta["label"],
            "help": meta["help"],
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


@login_required
def department_search(request):
    """Retourne en JSON les départements distincts de l'org matchant la query."""
    from django.http import JsonResponse
    q = request.GET.get("q", "").strip()
    departments = (
        request.user.org.positions
        .exclude(department="")
        .values_list("department", flat=True)
        .distinct()
        .order_by("department")
    )
    if q:
        departments = [d for d in departments if q.lower() in d.lower()]
    else:
        departments = list(departments)
    return JsonResponse(departments[:10], safe=False)
