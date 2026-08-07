"""Context processors globaux."""
from django.conf import settings
from django.templatetags.static import static
from django.urls import translate_url


def seo(request):
    """Métadonnées SEO communes à toutes les pages — canonical, hreflang,
    image OG par défaut.

    Le produit a déjà une URL dédiée par langue grâce à `i18n_patterns()`
    (core/urls.py) : `/`, `/en/`, `/es/`, `/de/`. `translate_url()` calcule
    l'équivalent de la page courante dans chaque langue configurée
    (`settings.LANGUAGES`) — c'est ce qui alimente les balises hreflang dans
    `templates/base.html`. Robuste par construction : `translate_url` renvoie
    l'URL inchangée si la page ne peut pas être résolue (ex. routes hors
    i18n_patterns comme /api/ ou /billing/).
    """
    alternate_urls = {
        code: request.build_absolute_uri(translate_url(request.path, code))
        for code, _label in settings.LANGUAGES
    }
    return {
        "seo_canonical_url": request.build_absolute_uri(request.path),
        "seo_alternate_urls": alternate_urls,
        "seo_x_default_url": alternate_urls.get(settings.LANGUAGE_CODE),
        "seo_og_image": request.build_absolute_uri(static("img/branding/favicon-512.png")),
    }


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
