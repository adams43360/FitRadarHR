"""Webhook Stripe — monté hors `i18n_patterns` dans `core/urls.py`, comme
l'API publique : un événement machine n'a pas de préférence de langue."""
from django.urls import path

from . import views

urlpatterns = [
    path("webhook/", views.stripe_webhook, name="stripe_webhook"),
]
