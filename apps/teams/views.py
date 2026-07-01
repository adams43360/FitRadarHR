from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def team_list(request):
    teams = request.user.org.teams.prefetch_related("memberships")
    return render(request, "teams/list.html", {"teams": teams})

@login_required
def team_create(request):
    return render(request, "teams/create.html")
