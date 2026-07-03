from django.urls import path
from . import views

app_name = "reports"

urlpatterns = [
    path("", views.report_list, name="list"),
    path("person/<uuid:person_pk>/", views.person_profile, name="person_profile"),
    path("person/<uuid:person_pk>/position/<uuid:position_pk>/", views.position_fit_report, name="position_fit"),
    path("person/<uuid:person_pk>/team/<uuid:team_pk>/", views.team_fit_report, name="team_fit"),
    # Fit inversé — postes recommandés pour une personne (item #1 roadmap V3)
    path("person/<uuid:person_pk>/positions/", views.person_position_ranking, name="person_positions"),
    # Export PDF
    path("person/<uuid:person_pk>/pdf/", views.person_profile_pdf, name="person_profile_pdf"),
    path("person/<uuid:person_pk>/position/<uuid:position_pk>/pdf/", views.position_fit_pdf, name="position_fit_pdf"),
    path("person/<uuid:person_pk>/team/<uuid:team_pk>/pdf/", views.team_fit_pdf, name="team_fit_pdf"),
    path("person/<uuid:person_pk>/positions/pdf/", views.person_position_ranking_pdf, name="person_positions_pdf"),
    # Audit log (E8)
    path("audit/", views.audit_log, name="audit_log"),
    # Analytics produit (RH only)
    path("analytics/", views.analytics, name="analytics"),
]
