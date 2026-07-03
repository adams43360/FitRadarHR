from django.urls import path
from . import views

app_name = "teams"

urlpatterns = [
    path("", views.team_list, name="list"),
    path("new/", views.team_create, name="create"),
    path("<uuid:pk>/", views.team_detail, name="detail"),
    path("<uuid:pk>/edit/", views.team_edit, name="edit"),
    path("<uuid:pk>/members/add/", views.team_add_member, name="add_member"),
    path("<uuid:pk>/members/search/", views.member_search, name="member_search"),
    path("<uuid:pk>/members/<uuid:membership_pk>/remove/", views.team_remove_member, name="remove_member"),
    path("persons/", views.person_list, name="persons"),
    path("persons/new/", views.person_create, name="person_create"),
    path("persons/import/", views.person_import, name="person_import"),
    path("persons/import/template/", views.person_import_template, name="person_import_template"),
    path("persons/<uuid:pk>/edit/", views.person_edit, name="person_edit"),
    path("persons/<uuid:pk>/anonymize/", views.person_anonymize, name="person_anonymize"),
]
