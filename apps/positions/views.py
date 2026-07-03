import json

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from apps.billing.quotas import check_quota
from core.managers import get_org_object_or_404
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
        if quota_error := check_quota(org, "position"):
            messages.error(request, quota_error)
            return redirect("accounts:billing_settings")
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

    position = get_org_object_or_404(Position, request.user.org, pk=pk)
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
        .for_org(request.user.org)
        .filter(position=position)
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
    position = get_org_object_or_404(Position, org, pk=pk)
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
    position = get_org_object_or_404(Position, request.user.org, pk=pk)
    if request.method == "POST":
        position.status = Position.Status.ARCHIVED
        position.save()
        messages.success(request, _("Poste archivé."))
        return redirect("positions:list")
    return render(request, "positions/archive_confirm.html", {"position": position})


@login_required
def position_profile_edit(request, pk):
    position = get_org_object_or_404(Position, request.user.org, pk=pk)
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


# ── Comparaison de candidats (item #3 de la roadmap V2) ──────────────────────

COMPARE_COLORS = ["99,102,241", "244,63,94", "234,179,8", "14,165,233", "168,85,247"]
COMPARE_MAX_CANDIDATES = 5


@login_required
def position_compare(request, pk):
    from apps.fit.engine import DIMENSIONS, DIMENSION_LABELS as FIT_DIMENSION_LABELS
    from apps.fit.models import PositionFitResult
    from apps.reports.insights import DIMENSION_TOOLTIPS
    from apps.reports.services import audit, get_lang

    position = get_org_object_or_404(Position, request.user.org, pk=pk)
    if not position.has_profile:
        messages.error(request, _("Définissez d'abord le profil Big Five cible du poste."))
        return redirect("positions:detail", pk=position.pk)

    person_ids = request.GET.getlist("persons")
    fits = list(
        PositionFitResult.objects
        .for_org(request.user.org)
        .filter(position=position, person_id__in=person_ids)
        .select_related("person", "person_profile")
        .order_by("-overall_fit")
    )

    if len(fits) < 2:
        messages.error(request, _("Sélectionnez au moins 2 personnes à comparer."))
        return redirect("positions:detail", pk=position.pk)
    if len(fits) > COMPARE_MAX_CANDIDATES:
        fits = fits[:COMPARE_MAX_CANDIDATES]
        messages.info(request, _("Comparaison limitée aux %(n)d premières personnes sélectionnées.") % {"n": COMPARE_MAX_CANDIDATES})

    lang = get_lang(request)
    profile = position.profile
    pos_min = [getattr(profile, f"{d}_min") for d in DIMENSIONS]
    pos_max = [getattr(profile, f"{d}_max") for d in DIMENSIONS]
    pos_mid = [round((mn + mx) / 2, 1) for mn, mx in zip(pos_min, pos_max)]

    candidates = []
    for i, fit in enumerate(fits):
        person_profile = fit.person_profile
        scores = (
            [float(getattr(person_profile, d)) for d in DIMENSIONS]
            if person_profile else [50.0] * len(DIMENSIONS)
        )
        candidates.append({
            "person": fit.person,
            "fit": fit,
            "scores": scores,
            "dim_fits": [float(getattr(fit, f"{d}_fit")) for d in DIMENSIONS],
            "color": COMPARE_COLORS[i % len(COMPARE_COLORS)],
            "has_profile": person_profile is not None,
        })

    dim_rows = []
    for idx, d in enumerate(DIMENSIONS):
        dim_rows.append({
            "label": FIT_DIMENSION_LABELS[d][lang],
            "tooltip": DIMENSION_TOOLTIPS[d][lang],
            "min": pos_min[idx],
            "max": pos_max[idx],
            "cells": [
                {
                    "score": c["scores"][idx],
                    "fit": c["dim_fits"][idx],
                    "in_range": pos_min[idx] <= c["scores"][idx] <= pos_max[idx],
                }
                for c in candidates
            ],
        })

    audit(
        request, "position_fit.compared", "Position", position.id,
        person_ids=[str(c["person"].pk) for c in candidates],
    )

    return render(request, "positions/compare.html", {
        "position": position,
        "candidates": candidates,
        "dim_rows": dim_rows,
        "chart_labels_json": json.dumps([FIT_DIMENSION_LABELS[d][lang] for d in DIMENSIONS]),
        "pos_mid_json": json.dumps(pos_mid),
        "candidate_scores_json": json.dumps([c["scores"] for c in candidates]),
        "candidate_names_json": json.dumps([c["person"].full_name for c in candidates]),
        "candidate_colors_json": json.dumps([c["color"] for c in candidates]),
    })


