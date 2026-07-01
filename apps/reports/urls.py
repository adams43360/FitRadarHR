from django.urls import path
from . import views

app_name = "reports"

urlpatterns = [
    path("", views.report_list, name="list"),
    path("person/<uuid:person_pk>/", views.person_profile, name="person_profile"),
    path("person/<uuid:person_pk>/position/<uuid:position_pk>/", views.position_fit_report, name="position_fit"),
    path("person/<uuid:person_pk>/team/<uuid:team_pk>/", views.team_fit_report, name="team_fit"),
]
