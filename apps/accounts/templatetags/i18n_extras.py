from django import template
from django.conf import settings

register = template.Library()


@register.filter
def strip_lang_prefix(path):
    """Retire le préfixe de langue (/en/, /es/, /de/...) d'un chemin.

    Utilisé par le sélecteur de langue de la navbar : avec `i18n_patterns` et
    `prefix_default_language=False`, le préfixe d'URL est prioritaire sur le
    cookie de langue lors de la résolution de `LocaleMiddleware`. Si on
    redirige vers un chemin qui contient encore l'ancien préfixe après avoir
    changé la langue, le changement est silencieusement ignoré. On reconstruit
    donc un chemin « neutre » avant de le passer en `next` à la vue
    `set_language`. Générique sur toutes les langues non-défaut de
    `settings.LANGUAGES` (pas seulement `en`).
    """
    for code, _label in settings.LANGUAGES:
        if code == settings.LANGUAGE_CODE:
            continue
        prefix = f"/{code}/"
        if path.startswith(prefix):
            return path[len(prefix) - 1:]
        if path == f"/{code}":
            return "/"
    return path
