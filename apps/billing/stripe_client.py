"""
Intégration Stripe — Checkout (souscription) + Customer Portal (gestion).

Le prix est configuré côté Stripe (Dashboard → Produits), jamais en dur ici :
`settings.STRIPE_PRICE_ID` référence le Price Stripe correspondant. Si Stripe
n'est pas configuré (clé/price manquants), ces fonctions ne sont pas censées
être appelées — voir la vue `billing_settings` qui affiche un message
"configuration Stripe requise" dans ce cas plutôt que de planter.
"""
from django.conf import settings

from .models import Subscription


def is_configured():
    return bool(settings.STRIPE_SECRET_KEY and settings.STRIPE_PRICE_ID)


def _client():
    import stripe
    stripe.api_key = settings.STRIPE_SECRET_KEY
    return stripe


def _get_or_create_customer(org):
    stripe = _client()
    sub = Subscription.get_or_create_for_org(org)
    if sub.stripe_customer_id:
        return sub.stripe_customer_id

    customer = stripe.Customer.create(
        name=org.name,
        metadata={"org_id": str(org.id)},
    )
    sub.stripe_customer_id = customer["id"]
    sub.save(update_fields=["stripe_customer_id"])
    return customer["id"]


def create_checkout_session(org, success_url, cancel_url):
    stripe = _client()
    customer_id = _get_or_create_customer(org)
    return stripe.checkout.Session.create(
        customer=customer_id,
        mode="subscription",
        line_items=[{"price": settings.STRIPE_PRICE_ID, "quantity": 1}],
        success_url=success_url,
        cancel_url=cancel_url,
        metadata={"org_id": str(org.id)},
    )


def create_portal_session(org, return_url):
    stripe = _client()
    sub = Subscription.get_or_create_for_org(org)
    if not sub.stripe_customer_id:
        return None
    return stripe.billing_portal.Session.create(
        customer=sub.stripe_customer_id,
        return_url=return_url,
    )
