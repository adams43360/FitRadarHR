from django import template
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

register = template.Library()


@register.simple_tag
def navbar_categories(user):
    """Structure du menu de navigation principal, regroupée par catégories.

    Centralise en un seul endroit la liste des liens (et leur restriction RH),
    utilisée à la fois pour le rendu desktop (sous-menus déroulants) et le
    panneau mobile empilé — évite toute divergence entre les deux rendus
    (US-E1-08 : refonte du menu, chevauchait le logo à mesure des ajouts).

    Une catégorie sans aucun item visible pour l'utilisateur courant (ex.
    Pilotage/Paramètres pour un Manager non-RH) est omise entièrement.
    """
    is_rh = getattr(user, "is_rh", False)

    def item(label, url_name):
        return {"label": label, "url": reverse(url_name)}

    categories = [
        {
            "label": _("Organisation"),
            "items": (
                ([item(_("Départements"), "departments:list")] if is_rh else [])
                + [item(_("Équipes"), "teams:list")]
                + ([item(_("Membres"), "accounts:members")] if is_rh else [])
            ),
        },
        {
            "label": _("Recrutement"),
            "items": (
                ([item(_("Postes"), "positions:list")] if is_rh else [])
                + [
                    item(_("Questionnaires"), "survey:dashboard"),
                    item(_("Rapports"), "reports:list"),
                ]
            ),
        },
    ]

    if is_rh:
        categories.append({
            "label": _("Pilotage"),
            "items": [
                item(_("Analytics"), "reports:analytics"),
                item(_("Audit"), "reports:audit_log"),
            ],
        })
        categories.append({
            "label": _("Paramètres"),
            "items": [
                item(_("SSO"), "accounts:sso_config"),
                item(_("API"), "accounts:api_keys_settings"),
                item(_("Abonnement"), "accounts:billing_settings"),
            ],
        })

    return [c for c in categories if c["items"]]
