"""
SSO OIDC — synchronisation `OrgSSOConfig` ↔ `SocialApp` (django-allauth).

Un `OrgSSOConfig` par organisation ; on s'appuie sur le provider générique
`openid_connect` d'allauth (flux OAuth2/OIDC déjà implémenté et audité) plutôt
que de ré-écrire l'échange de jetons. Chaque config a son propre `SocialApp`,
identifié par `provider_id=login_slug` — voir docs/technical/stack.md.

Convention du projet (voir AuditLog, ConsentRecord) : la synchronisation est
explicite, déclenchée depuis `save()` / `delete()` du modèle, jamais via des
signaux Django implicites.
"""
from django.utils.text import slugify

PROVIDER = "openid_connect"


def unique_login_slug(name, model, instance_pk=None):
    """Génère un slug unique à partir d'un nom, en évitant les collisions
    avec les `login_slug` déjà utilisés par d'autres organisations."""
    base = slugify(name) or "org"
    slug = base
    n = 1
    qs = model.objects.exclude(pk=instance_pk) if instance_pk else model.objects.all()
    while qs.filter(login_slug=slug).exists():
        n += 1
        slug = f"{base}-{n}"
    return slug


def sync_social_app(config):
    """Crée ou met à jour le `SocialApp` allauth correspondant à cette config."""
    from allauth.socialaccount.models import SocialApp
    from django.contrib.sites.models import Site

    app, _created = SocialApp.objects.get_or_create(
        provider=PROVIDER, provider_id=config.login_slug,
        defaults={"name": config.display_name},
    )
    app.name = config.display_name
    app.client_id = config.client_id
    app.secret = config.client_secret
    app.settings = {"server_url": config.issuer_url}
    app.save()

    # Le SocialApp n'est rattaché au site courant que si le SSO est activé —
    # défense en profondeur : même si l'URL de connexion est devinée, allauth
    # ne trouvera aucun SocialApp actif pour ce provider_id.
    site = Site.objects.get_current()
    if config.enabled:
        app.sites.add(site)
    else:
        app.sites.remove(site)


def delete_social_app(login_slug):
    from allauth.socialaccount.models import SocialApp

    SocialApp.objects.filter(provider=PROVIDER, provider_id=login_slug).delete()
