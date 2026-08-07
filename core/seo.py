"""robots.txt et sitemap.xml — fondations SEO, pensées pour les 4 langues.

Le produit expose déjà une URL par langue pour chaque page publique grâce à
`i18n_patterns()` (core/urls.py). Ces deux vues restent volontairement hors
`i18n_patterns` : un robots.txt / sitemap.xml est un point d'entrée unique
pour les robots, pas une page utilisateur à traduire.

Seules 3 pages sont réellement destinées à être indexées : l'accueil,
l'entrée d'inscription et la politique de confidentialité. Tout le reste de
l'application (postes, équipes, rapports, questionnaires, réglages...)
contient des données d'organisation privées et n'a aucune valeur SEO — on
l'exclut explicitement plutôt que de compter sur l'authentification seule.
"""
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.urls import reverse, translate_url
from django.utils import translation

# Pages publiques à indexer (namespace:name des URLs, voir apps/accounts/urls.py)
PUBLIC_VIEW_NAMES = [
    "accounts:home",
    "accounts:signup_choice",
    "accounts:privacy_policy",
]

# Préfixes de chemin privés à exclure du crawl, sans le préfixe de langue
# (celui-ci est ajouté pour chacune des `settings.LANGUAGES` ci-dessous).
PRIVATE_PATH_PREFIXES = [
    "/admin/",
    "/accounts/login/",
    "/accounts/logout/",
    "/accounts/signup/organisation/",
    "/accounts/signup/personnel/",
    "/accounts/demo/",
    "/accounts/dashboard/",
    "/accounts/members/",
    "/accounts/settings/",
    "/accounts/feedback/",
    "/departments/",
    "/positions/",
    "/teams/",
    "/survey/",
    "/reports/",
]


def robots_txt(request):
    lines = ["User-agent: *"]
    for code, _label in settings.LANGUAGES:
        prefix = "" if code == settings.LANGUAGE_CODE else f"/{code}"
        for path in PRIVATE_PATH_PREFIXES:
            lines.append(f"Disallow: {prefix}{path}")
    # Hors i18n_patterns — un seul préfixe possible pour ces routes.
    lines += ["Disallow: /api/", "Disallow: /billing/", "Disallow: /i18n/"]
    lines += [
        "",
        f"Sitemap: {request.build_absolute_uri('/sitemap.xml')}",
        # Sitemap généré par mkdocs lui-même (docs/user/**, servi sous /docs/,
        # voir docker/nginx.prod.conf) — deux fichiers Sitemap: dans un même
        # robots.txt est un usage standard, pas besoin de les fusionner.
        f"Sitemap: {request.build_absolute_uri('/docs/sitemap.xml')}",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")


def sitemap_xml(request):
    entries = []
    with translation.override(settings.LANGUAGE_CODE):
        for view_name in PUBLIC_VIEW_NAMES:
            default_path = reverse(view_name)
            alternates = {
                code: request.build_absolute_uri(translate_url(default_path, code))
                for code, _label in settings.LANGUAGES
            }
            entries.append({
                "loc": alternates[settings.LANGUAGE_CODE],
                "alternates": alternates,
                "x_default": alternates[settings.LANGUAGE_CODE],
            })
        # Une entrée <url> par langue, chacune listant les autres comme alternates.
        urls = []
        for entry in entries:
            for code, loc in entry["alternates"].items():
                urls.append({
                    "loc": loc,
                    "alternates": entry["alternates"],
                    "x_default": entry["x_default"],
                })

    xml = render_to_string("seo/sitemap.xml", {"urls": urls})
    return HttpResponse(xml, content_type="application/xml")
