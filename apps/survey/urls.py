from django.urls import path
from . import views
app_name = "survey"
urlpatterns = [
    path("persons/", views.person_list, name="persons"),
    path("send/", views.send_questionnaire, name="send"),
    path("q/<str:token>/", views.questionnaire, name="questionnaire"),
]
