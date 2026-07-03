# Connexion SSO (Keycloak / OIDC)

FitRadarHR permet à chaque organisation de connecter son propre fournisseur d'identité (Keycloak ou tout IdP compatible OIDC), pour que ses utilisateurs se connectent avec leurs identifiants d'entreprise habituels plutôt qu'un mot de passe dédié.

!!! note "Le SSO s'ajoute, il ne remplace pas"
    Activer le SSO n'empêche jamais la connexion par email/mot de passe existante. C'est une option supplémentaire — utile pour éviter un blocage si votre fournisseur d'identité est indisponible.

## Configurer le SSO de votre organisation

Un RH accède à l'écran de configuration depuis le lien **SSO** de la barre de navigation.

| Champ | Description |
|---|---|
| **Nom d'affichage** | Affiché sur le bouton de connexion (ex. « Acme Corp SSO ») |
| **Identifiant de connexion** | Identifiant unique utilisé dans l'URL de connexion SSO — à communiquer à vos utilisateurs |
| **URL d'émetteur OIDC** | Endpoint de découverte de votre fournisseur d'identité (Keycloak, Okta, Azure AD…) |
| **Client ID / Client secret** | Identifiants de l'application déclarée auprès de votre IdP |
| **Activé** | Coupe le SSO sans perdre la configuration |

Le **client secret** n'est jamais ré-affiché après saisie — laissez le champ vide lors d'une modification pour le conserver.

## Se connecter via SSO

Sur la page de connexion, un utilisateur clique sur **« Se connecter via votre organisation (SSO) »**, saisit l'identifiant de connexion de son organisation, puis est redirigé vers l'IdP configuré.

À la première connexion réussie, un compte est automatiquement créé (rôle Manager par défaut, modifiable ensuite par un RH) — aucune inscription manuelle n'est nécessaire. Si un compte existe déjà avec la même adresse email dans l'organisation, la connexion SSO s'y rattache directement.

!!! warning "Isolation des organisations"
    Chaque organisation configure son propre IdP — aucune configuration n'est partagée entre organisations. Un email déjà utilisé dans une autre organisation ne peut pas se connecter via le SSO d'une organisation différente.
