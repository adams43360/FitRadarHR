"""Context processors globaux."""
from django.conf import settings


def demo_mode(request):
    """Expose l'état du mode démo aux templates.

    - DEMO_MODE : le bouton "Essayer la démo" est proposé sur les pages publiques
    - is_demo_org : l'utilisateur connecté navigue dans l'org de démonstration
      (affichage de la bannière, désactivation des fonctions sensibles)
    """
    is_demo_org = bool(
        request.user.is_authenticated
        and getattr(request.user.org, "is_demo", False)
    )
    return {
        "DEMO_MODE": settings.DEMO_MODE,
        "is_demo_org": is_demo_org,
    }


def matomo(request):
    """Expose la config Matomo aux templates.

    Le tracker n'est rendu dans base.html que si MATOMO_URL est configuré ET
    que la navigation ne se fait pas dans l'org de démonstration (is_demo_org,
    cf. demo_mode() ci-dessus) — on ne veut pas polluer les stats avec le
    trafic de la démo publique.
    """
    return {
        "MATOMO_URL": settings.MATOMO_URL,
        "MATOMO_SITE_ID": settings.MATOMO_SITE_ID,
    }
