"""API publique JSON — montée hors `i18n_patterns` dans `core/urls.py`
(un consommateur machine n'a pas de préférence de langue de navigateur)."""
from django.urls import path

from . import views

urlpatterns = [
    path("positions/", views.positions_list, name="positions_list"),
    path("positions/<uuid:pk>/", views.positions_detail, name="positions_detail"),
    path("teams/", views.teams_list, name="teams_list"),
    path("teams/<uuid:pk>/", views.teams_detail, name="teams_detail"),
    path("people/", views.people_list, name="people_list"),
    path("people/<uuid:pk>/", views.people_detail, name="people_detail"),
    path("fit-results/positions/", views.position_fit_results_list, name="position_fit_results_list"),
    path("fit-results/teams/", views.team_fit_results_list, name="team_fit_results_list"),
]
