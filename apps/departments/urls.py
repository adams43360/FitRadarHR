from django.urls import path
from . import views

app_name = "departments"

urlpatterns = [
    path("", views.department_list, name="list"),
    path("new/", views.department_create, name="create"),
    path("<uuid:pk>/", views.department_detail, name="detail"),
    path("<uuid:pk>/edit/", views.department_edit, name="edit"),
    path("<uuid:pk>/archive/", views.department_archive, name="archive"),
]
