"""Authentification de l'API publique — clé API par organisation.

En-tête attendu : `Authorization: Api-Key <clé>`. Schéma volontairement
distinct de `Bearer` (OAuth2) pour éviter toute confusion : il n'y a pas de
flux OAuth2 ici, une clé opaque scope l'accès à une seule organisation.
"""
import functools

from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.http import require_GET

from .models import ApiKey


def _unauthorized(error, detail):
    return JsonResponse({"error": error, "detail": detail}, status=401)


def api_key_required(view_func):
    """Authentifie la requête via l'en-tête `Authorization: Api-Key <clé>`.

    En cas de succès, attache `request.api_key` (l'objet `ApiKey`) et
    `request.api_org` (l'organisation scopée) — toute vue de l'API doit
    filtrer ses requêtes sur `request.api_org`, jamais sur l'org entière."""

    @functools.wraps(view_func)
    def wrapper(request, *args, **kwargs):
        auth_header = request.META.get("HTTP_AUTHORIZATION", "")
        scheme, _, raw_key = auth_header.partition(" ")
        raw_key = raw_key.strip()
        if scheme != "Api-Key" or not raw_key:
            return _unauthorized(
                "authentication_required",
                "Missing or malformed 'Authorization: Api-Key <key>' header.",
            )
        api_key = ApiKey.authenticate(raw_key)
        if api_key is None:
            return _unauthorized("invalid_api_key", "Invalid or revoked API key.")

        ApiKey.objects.filter(pk=api_key.pk).update(last_used_at=timezone.now())
        request.api_key = api_key
        request.api_org = api_key.org
        return view_func(request, *args, **kwargs)

    return wrapper


def api_get_endpoint(view_func):
    """Combine `api_key_required` et une restriction GET — tous les endpoints
    de l'API publique sont en lecture seule par construction."""
    return require_GET(api_key_required(view_func))
