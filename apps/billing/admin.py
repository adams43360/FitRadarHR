from django.contrib import admin

from .models import Subscription


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    """Le statut reste modifiable (support client), mais les identifiants
    Stripe sont en lecture seule — gérés uniquement par le webhook, jamais
    à la main."""

    list_display = ("org", "status", "current_period_end", "updated_at")
    list_filter = ("status",)
    search_fields = ("org__name",)
    readonly_fields = ("stripe_customer_id", "stripe_subscription_id", "created_at", "updated_at")
