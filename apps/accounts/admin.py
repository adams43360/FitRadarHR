from django.contrib import admin

from .models import Feedback, Organization, User


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ("name", "account_type", "is_demo", "is_active", "created_at")
    list_filter = ("account_type", "is_demo", "is_active")
    search_fields = ("name",)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("email", "first_name", "last_name", "org", "role", "is_active")
    list_filter = ("role", "is_active")
    search_fields = ("email", "first_name", "last_name")


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    """Retours utilisateurs — lecture seule, alimente la priorisation roadmap."""

    list_display = ("created_at", "org", "user", "page", "short_message")
    list_filter = ("created_at",)
    search_fields = ("message",)
    readonly_fields = ("org", "user", "message", "page", "created_at")

    def short_message(self, obj):
        return obj.message[:80]

    short_message.short_description = "message"

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
