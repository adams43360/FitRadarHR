from django.contrib import admin

from .models import ApiKey


@admin.register(ApiKey)
class ApiKeyAdmin(admin.ModelAdmin):
    """Clés API — lecture seule dans l'admin (jamais la clé en clair, jamais
    modifiable ici : la génération/révocation passe par `/settings/api/`)."""

    list_display = ("name", "org", "key_prefix", "created_at", "last_used_at", "is_active")
    list_filter = ("org",)
    search_fields = ("name", "key_prefix", "org__name")
    readonly_fields = ("id", "org", "name", "key_prefix", "key_hash", "created_by", "created_at", "last_used_at", "revoked_at")

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
