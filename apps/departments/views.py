from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.translation import gettext_lazy as _
from .models import Department
from .forms import DepartmentForm


@login_required
def department_list(request):
    departments = (
        Department.objects
        .for_org(request.user.org)
        .prefetch_related("positions", "teams")
    )
    return render(request, "departments/list.html", {"departments": departments})


@login_required
def department_create(request):
    if request.method == "POST":
        form = DepartmentForm(request.POST)
        if form.is_valid():
            dept = form.save(commit=False)
            dept.org = request.user.org
            dept.save()
            return redirect("departments:list")
    else:
        form = DepartmentForm()
    return render(request, "departments/create.html", {"form": form})


@login_required
def department_detail(request, pk):
    dept = get_object_or_404(Department, pk=pk, org=request.user.org)
    positions = dept.positions.filter(status="active").order_by("title_fr")
    teams = dept.teams.all().order_by("name")
    return render(request, "departments/detail.html", {
        "dept": dept,
        "positions": positions,
        "teams": teams,
    })


@login_required
def department_edit(request, pk):
    dept = get_object_or_404(Department, pk=pk, org=request.user.org)
    if request.method == "POST":
        form = DepartmentForm(request.POST, instance=dept)
        if form.is_valid():
            form.save()
            return redirect("departments:detail", pk=dept.pk)
    else:
        form = DepartmentForm(instance=dept)
    return render(request, "departments/edit.html", {"form": form, "dept": dept})


@login_required
def department_archive(request, pk):
    dept = get_object_or_404(Department, pk=pk, org=request.user.org)
    if request.method == "POST":
        dept.is_archived = not dept.is_archived
        dept.save()
    return redirect("departments:list")
