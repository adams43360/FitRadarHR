from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def report_list(request):
    reports = request.user.org.fit_reports.select_related("profile__person")
    return render(request, "reports/list.html", {"reports": reports})

@login_required
def report_detail(request, pk):
    return render(request, "reports/detail.html")
