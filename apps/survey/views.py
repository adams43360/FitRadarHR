from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def person_list(request):
    persons = request.user.org.persons.all()
    return render(request, "survey/persons.html", {"persons": persons})

@login_required
def send_questionnaire(request):
    return render(request, "survey/send.html")

def questionnaire(request, token):
    return render(request, "survey/questionnaire.html", {"token": token})
