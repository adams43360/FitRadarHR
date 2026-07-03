from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = "accounts"

urlpatterns = [
    path("", views.landing, name="home"),
    path("signup/", views.signup_choice, name="signup_choice"),
    path("signup/organisation/", views.signup_b2b, name="signup_b2b"),
    path("signup/personnel/", views.signup_b2c, name="signup_b2c"),
    path("login/", auth_views.LoginView.as_view(template_name="accounts/login.html"), name="login"),
    path("demo/", views.demo_login, name="demo_login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("privacy/", views.privacy_policy, name="privacy_policy"),
    path("feedback/", views.submit_feedback, name="feedback"),
]
