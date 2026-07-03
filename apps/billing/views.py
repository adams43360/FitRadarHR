"""Webhook Stripe — seul endpoint machine de l'app billing (non authentifié,
signature vérifiée). Les vues RH-facing (`/settings/billing/`) vivent dans
`apps.accounts`, comme l'écran SSO et l'écran de gestion des clés API, pour
garder tous les écrans "Paramètres" au même endroit."""
import logging
from datetime import datetime, timezone as dt_timezone

from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .models import Subscription

logger = logging.getLogger(__name__)

_STRIPE_STATUS_MAP = {
    "active": Subscription.Status.ACTIVE,
    "trialing": Subscription.Status.TRIALING,
    "past_due": Subscription.Status.PAST_DUE,
    "unpaid": Subscription.Status.PAST_DUE,
    "canceled": Subscription.Status.CANCELED,
    "incomplete_expired": Subscription.Status.CANCELED,
}


@csrf_exempt
@require_POST
def stripe_webhook(request):
    import stripe

    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE", "")

    if not settings.STRIPE_WEBHOOK_SECRET:
        return HttpResponse(status=503)

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, settings.STRIPE_WEBHOOK_SECRET)
    except (ValueError, stripe.error.SignatureVerificationError):
        return HttpResponse(status=400)

    event_type = event["type"]
    data = event["data"]["object"]

    if event_type == "checkout.session.completed":
        _handle_checkout_completed(data)
    elif event_type in ("customer.subscription.updated", "customer.subscription.created"):
        _handle_subscription_updated(data)
    elif event_type == "customer.subscription.deleted":
        _handle_subscription_deleted(data)
    else:
        logger.info("Événement Stripe ignoré : %s", event_type)

    return HttpResponse(status=200)


def _handle_checkout_completed(data):
    org_id = (data.get("metadata") or {}).get("org_id")
    if not org_id:
        return
    sub = Subscription.objects.filter(org_id=org_id).first()
    if sub is None:
        return
    sub.stripe_customer_id = data.get("customer") or sub.stripe_customer_id
    sub.stripe_subscription_id = data.get("subscription") or sub.stripe_subscription_id
    sub.status = Subscription.Status.ACTIVE
    sub.save()


def _handle_subscription_updated(data):
    stripe_sub_id = data.get("id")
    sub = Subscription.objects.filter(stripe_subscription_id=stripe_sub_id).first()
    if sub is None:
        return
    sub.status = _STRIPE_STATUS_MAP.get(data.get("status"), sub.status)
    period_end = data.get("current_period_end")
    if period_end:
        sub.current_period_end = datetime.fromtimestamp(period_end, tz=dt_timezone.utc)
    sub.save()


def _handle_subscription_deleted(data):
    stripe_sub_id = data.get("id")
    sub = Subscription.objects.filter(stripe_subscription_id=stripe_sub_id).first()
    if sub is None:
        return
    sub.status = Subscription.Status.CANCELED
    sub.save()
