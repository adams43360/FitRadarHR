from django.urls import path
from . import views
app_name = "positions"
urlpatterns = [
    path("", views.position_list, name="list"),
    path("new/", views.position_create, name="create"),
]
