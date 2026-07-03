from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
    # Changement de langue
    path("i18n/", include("django.conf.urls.i18n")),
    # API publique en lecture seule (roadmap V2 #9) — hors i18n_patterns,
    # un consommateur machine n'a pas de préférence de langue de navigateur.
    path("api/v1/", include("apps.api.urls")),
    # Webhook Stripe (roadmap V3 #2) — idem, hors i18n_patterns.
    path("billing/", include("apps.billing.urls")),
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
