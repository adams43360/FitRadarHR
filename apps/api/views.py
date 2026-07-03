"""
Endpoints JSON de l'API publique — lecture seule (roadmap V2 #9, US-E1-06).

Toutes les vues sont scopées à `request.api_org` (attaché par
`api_key_required`) : jamais de fuite cross-tenant. Voir `serializers.py` pour
le format des réponses — les scores Big Five bruts ne sont jamais exposés.
"""
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from apps.fit.models import PositionFitResult, TeamFitResult
from apps.positions.models import Position
from apps.teams.models import Person, Team

from .auth import api_get_endpoint
from .serializers import (
    paginate,
    serialize_person,
    serialize_position,
    serialize_position_fit,
    serialize_team,
    serialize_team_fit,
)


@api_get_endpoint
def positions_list(request):
    qs = Position.objects.for_org(request.api_org).order_by("-created_at")
    status = request.GET.get("status")
    if status:
        qs = qs.filter(status=status)
    return JsonResponse(paginate(request, qs, serialize_position))


@api_get_endpoint
def positions_detail(request, pk):
    position = get_object_or_404(Position.objects.for_org(request.api_org), pk=pk)
    return JsonResponse(serialize_position(position))


@api_get_endpoint
def teams_list(request):
    qs = Team.objects.for_org(request.api_org).order_by("name")
    return JsonResponse(paginate(request, qs, serialize_team))


@api_get_endpoint
def teams_detail(request, pk):
    team = get_object_or_404(Team.objects.for_org(request.api_org), pk=pk)
    return JsonResponse(serialize_team(team))


@api_get_endpoint
def people_list(request):
    qs = Person.objects.for_org(request.api_org).order_by("last_name", "first_name")
    person_type = request.GET.get("person_type")
    if person_type:
        qs = qs.filter(person_type=person_type)
    return JsonResponse(paginate(request, qs, serialize_person))


@api_get_endpoint
def people_detail(request, pk):
    person = get_object_or_404(Person.objects.for_org(request.api_org), pk=pk)
    return JsonResponse(serialize_person(person))


@api_get_endpoint
def position_fit_results_list(request):
    qs = (
        PositionFitResult.objects.for_org(request.api_org)
        .order_by("-computed_at")
    )
    if position_id := request.GET.get("position_id"):
        qs = qs.filter(position_id=position_id)
    if person_id := request.GET.get("person_id"):
        qs = qs.filter(person_id=person_id)
    return JsonResponse(paginate(request, qs, serialize_position_fit))


@api_get_endpoint
def team_fit_results_list(request):
    qs = (
        TeamFitResult.objects.for_org(request.api_org)
        .order_by("-computed_at")
    )
    if team_id := request.GET.get("team_id"):
        qs = qs.filter(team_id=team_id)
    if person_id := request.GET.get("person_id"):
        qs = qs.filter(person_id=person_id)
    return JsonResponse(paginate(request, qs, serialize_team_fit))
