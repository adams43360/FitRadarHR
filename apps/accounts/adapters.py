"""
Adapter allauth — provisioning JIT scopé à l'organisation pour le SSO OIDC
(item #7 roadmap V2). Voir docs/product/user-stories.md#US-E1-05.
"""
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from allauth.core.exceptions import ImmediateHttpResponse
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

from .models import OrgSSOConfig, User


class OrgScopedSocialAccountAdapter(DefaultSocialAccountAdapter):
    """Chaque `SocialApp` OIDC (provider_id=login_slug) appartient à une seule
    organisation. À la première connexion SSO :

    - si un `User` existe déjà avec cet email **dans cette organisation**, la
      connexion s'y rattache (pas de doublon) ;
    - si un `User` existe avec cet email dans une **autre** organisation, la
      connexion est refusée — l'email est unique globalement dans le modèle,
      il n'y a jamais de fusion cross-tenant ;
    - sinon, un nouveau `User` est créé (rôle Manager par défaut, modifiable
      ensuite par un RH), avec un mot de passe inutilisable : le SSO reste la
      seule voie de connexion pour ce compte tant qu'un RH ne lui envoie pas
      une invitation classique.
    """

    def pre_social_login(self, request, sociallogin):
        if sociallogin.is_existing:
            return  # déjà rattaché à un compte lors d'une connexion précédente

        login_slug = sociallogin.account.provider
        config = (
            OrgSSOConfig.objects.filter(login_slug=login_slug, enabled=True)
            .select_related("org")
            .first()
        )
        if config is None:
            self._abort(request, _("Connexion SSO non disponible pour cette organisation."))

        email = (sociallogin.user.email or "").lower()
        if not email:
            self._abort(
                request,
                _("Votre fournisseur d'identité n'a pas transmis d'adresse email."),
            )

        existing = User.objects.filter(email=email).first()
        if existing is not None:
            if existing.org_id != config.org_id:
                self._abort(
                    request,
                    _("Un compte existe déjà avec cet email dans une autre organisation."),
                )
            sociallogin.connect(request, existing)
            return

        user = User(
            email=email,
            first_name=sociallogin.user.first_name or "",
            last_name=sociallogin.user.last_name or "",
            org=config.org,
            role=User.Role.MANAGER,
        )
        user.set_unusable_password()
        sociallogin.connect(request, user)

    def _abort(self, request, message):
        """Interrompt la connexion SSO avec un message clair, sans exposer de
        détail technique — redirige vers le point d'entrée SSO plutôt que
        d'afficher une page d'erreur générique."""
        messages.error(request, message)
        raise ImmediateHttpResponse(HttpResponseRedirect(reverse("accounts:sso_login_entry")))
