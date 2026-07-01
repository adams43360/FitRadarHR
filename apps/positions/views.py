from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def position_list(request):
    positions = request.user.org.positions.filter(status="active").select_related("profile")
    return render(request, "positions/list.html", {"positions": positions})

@login_required
def position_create(request):
    return render(request, "positions/create.html")
