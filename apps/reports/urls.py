from django.urls import path
from . import views

app_name = "reports"

urlpatterns = [
    path("", views.report_list, name="list"),
    path("person/<uuid:person_pk>/", views.person_profile, name="person_profile"),
    path("person/<uuid:person_pk>/position/<uuid:position_pk>/", views.position_fit_report, name="position_fit"),
    path("person/<uuid:person_pk>/team/<uuid:team_pk>/", views.team_fit_report, name="team_fit"),
    # Export PDF
    path("person/<uuid:person_pk>/pdf/", views.person_profile_pdf, name="person_profile_pdf"),
    path("person/<uuid:person_pk>/position/<uuid:position_pk>/pdf/", views.position_fit_pdf, name="position_fit_pdf"),
    path("person/<uuid:person_pk>/team/<uuid:team_pk>/pdf/", views.team_fit_pdf, name="team_fit_pdf"),
    # Audit log (E8)
    path("audit/", views.audit_log, name="audit_log"),
]
