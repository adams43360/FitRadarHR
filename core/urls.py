from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns

from core import seo

urlpatterns = [
    # Changement de langue
    path("i18n/", include("django.conf.urls.i18n")),
    # API publique en lecture seule (roadmap V2 #9) — hors i18n_patterns,
    # un consommateur machine n'a pas de préférence de langue de navigateur.
    path("api/v1/", include("apps.api.urls")),
    # Webhook Stripe (roadmap V3 #2) — idem, hors i18n_patterns.
    path("billing/", include("apps.billing.urls")),
    # SEO — point d'entrée unique pour les robots, liste les variantes de
    # langue des pages publiques plutôt que d'être eux-mêmes traduits.
    path("robots.txt", seo.robots_txt, name="robots_txt"),
    path("sitemap.xml", seo.sitemap_xml, name="sitemap_xml"),
]

urlpatterns += i18n_patterns(
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path("", include("apps.accounts.urls")),
    path("departments/", include("apps.departments.urls")),
    path("positions/", include("apps.positions.urls")),
    path("teams/", include("apps.teams.urls")),
    path("survey/", include("apps.survey.urls")),
    path("reports/", include("apps.reports.urls")),
    prefix_default_language=False,
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
