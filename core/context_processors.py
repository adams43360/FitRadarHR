"""Context processors globaux."""
import json

from django.conf import settings
from django.templatetags.static import static
from django.urls import translate_url
from django.utils.safestring import mark_safe


def seo(request):
    """Métadonnées SEO communes à toutes les pages — canonical, hreflang,
    image OG par défaut, JSON-LD Organization.

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
    og_image_url = request.build_absolute_uri(static("img/branding/favicon-512.png"))
    site_root_url = request.build_absolute_uri("/")

    # JSON-LD Organization — sitewide, sur toutes les pages (templates/base.html).
    # Construit et sérialisé côté Python (jamais par interpolation de variables
    # dans le template) pour éviter que l'auto-échappement HTML de Django ne
    # corrompe le JSON (ex. guillemets transformés en &quot;).
    organization_ld = {
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": "FitRadarHR",
        "url": site_root_url,
        "logo": og_image_url,
    }

    return {
        "seo_canonical_url": request.build_absolute_uri(request.path),
        "seo_alternate_urls": alternate_urls,
        "seo_x_default_url": alternate_urls.get(settings.LANGUAGE_CODE),
        "seo_og_image": og_image_url,
        # Racine du site (hors préfixe de langue) — utilisée pour le JSON-LD
        # Organization, qui doit toujours pointer vers le domaine, pas la page
        # courante.
        "seo_site_root_url": site_root_url,
        "seo_organization_jsonld": mark_safe(json.dumps(organization_ld)),
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
