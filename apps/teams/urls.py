from django.urls import path
from . import views

app_name = "teams"

urlpatterns = [
    path("", views.team_list, name="list"),
    path("new/", views.team_create, name="create"),
    path("<uuid:pk>/", views.team_detail, name="detail"),
    path("<uuid:pk>/edit/", views.team_edit, name="edit"),
    path("<uuid:pk>/members/add/", views.team_add_member, name="add_member"),
    path("<uuid:pk>/members/<uuid:membership_pk>/remove/", views.team_remove_member, name="remove_member"),
    path("persons/", views.person_list, name="persons"),
    path("persons/new/", views.person_create, name="person_create"),
    path("persons/<uuid:pk>/anonymize/", views.person_anonymize, name="person_anonymize"),
]
