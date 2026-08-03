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

    Chaque catégorie/item porte une `key` stable (anglais, non traduite) en
    plus du `label` traduit — sert de data-testid dans les templates, pour que
    les sélecteurs des tests E2E ne dépendent pas de la langue active (le
    slug d'un libellé traduit change avec la langue, pas cette clé).
    """
    is_rh = getattr(user, "is_rh", False)

    def item(key, label, url_name):
        return {"key": key, "label": label, "url": reverse(url_name)}

    categories = [
        {
            "key": "organization",
            "label": _("Organisation"),
            "items": (
                ([item("departments", _("Départements"), "departments:list")] if is_rh else [])
                + [item("teams", _("Équipes"), "teams:list")]
                + ([item("members", _("Membres"), "accounts:members")] if is_rh else [])
            ),
        },
        {
            "key": "recruitment",
            "label": _("Recrutement"),
            "items": (
                ([item("positions", _("Postes"), "positions:list")] if is_rh else [])
                + [
                    item("questionnaires", _("Questionnaires"), "survey:dashboard"),
                    item("reports", _("Rapports"), "reports:list"),
                ]
            ),
        },
    ]

    if is_rh:
        categories.append({
            "key": "governance",
            "label": _("Pilotage"),
            "items": [
                item("analytics", _("Analytics"), "reports:analytics"),
                item("audit", _("Audit"), "reports:audit_log"),
            ],
        })
        categories.append({
            "key": "settings",
            "label": _("Paramètres"),
            "items": [
                item("sso", _("SSO"), "accounts:sso_config"),
                item("api-keys", _("API"), "accounts:api_keys_settings"),
                item("billing", _("Abonnement"), "accounts:billing_settings"),
            ],
        })

    return [c for c in categories if c["items"]]
