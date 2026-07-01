from django.urls import path
from . import views

app_name = "survey"

urlpatterns = [
    # Dashboard & gestion (RH / manager)
    path("", views.survey_dashboard, name="dashboard"),
    path("send/", views.send_questionnaire, name="send"),
    path("<uuid:pk>/resend/", views.resend_link, name="resend"),

    # Passation publique (sans compte)
    path("q/<str:token>/", views.questionnaire_start, name="start"),
    path("q/<str:token>/<int:block>/", views.questionnaire_questions, name="questions"),
    path("q/<str:token>/submit/", views.questionnaire_submit, name="submit"),
    path("q/<str:token>/done/", views.questionnaire_done, name="done"),
]
