from django.urls import path
from . import views

app_name = "positions"

urlpatterns = [
    path("", views.position_list, name="list"),
    path("new/", views.position_create, name="create"),
    path("<uuid:pk>/", views.position_detail, name="detail"),
    path("<uuid:pk>/edit/", views.position_edit, name="edit"),
    path("<uuid:pk>/archive/", views.position_archive, name="archive"),
    path("<uuid:pk>/profile/", views.position_profile_edit, name="profile_edit"),
    path("<uuid:pk>/compare/", views.position_compare, name="compare"),
]
