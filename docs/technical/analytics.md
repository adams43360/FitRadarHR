# Mesure d'audience — Matomo self-hosted

> Décision : 2026-08-05. Objectif : volume d'usage + fonctionnalités les plus utilisées
> + points de blocage (tunnel questionnaire, création poste/équipe), sans donnée
> personnelle et sans bandeau de consentement. Voir aussi la section « Mesure d'audience »
> de `docs/user/about/privacy.md` et `templates/accounts/privacy_policy.html`.

## Pourquoi Matomo plutôt que Google Analytics

GA4 n'est pas éligible à l'exemption de consentement CNIL (tracking cross-device,
transfert de données hors UE, lien structurel avec l'écosystème publicitaire Google) —
bandeau de consentement obligatoire. Matomo self-hosted, correctement configuré, entre
dans le cadre exempté : finalité strictement limitée à la mesure d'audience du site,
aucun croisement avec d'autres traitements, aucun partage avec un tiers, pas de suivi
cross-site, durée de conservation encadrée.

## Architecture de déploiement

Stack indépendante du dépôt applicatif, sur le même modèle que les autres sites du
serveur (voir `docs/technical/stack.md` — architecture multi-sites) :

```
/srv/matomo → deploy/matomo/docker-compose.yml (Matomo + MariaDB), réseau « web »
```

- `deploy/matomo/docker-compose.yml` : stack à copier sur le serveur dans `/srv/matomo`
- `deploy/matomo/.env.matomo.example` : à copier en `.env` sur le serveur (jamais commité)
- `deploy/proxy/Caddyfile` : bloc `analytics.fitradarhr.fr` déjà ajouté, route vers le
  conteneur `matomo-web`
- Le tracker JS n'est chargé dans `templates/base.html` que si `MATOMO_URL` et
  `MATOMO_SITE_ID` sont renseignés dans le `.env` de l'app **et** que la page n'est pas
  consultée dans l'org de démo (`is_demo_org`) — pas de pollution des stats par le
  trafic de démonstration publique

## Checklist de mise en production (une fois)

### 0. Déployer le code sur le serveur

Le code (Caddyfile mis à jour, `templates/base.html`, `deploy/matomo/`, etc.) part
d'abord en local vers `main`, puis :

```bash
ssh damien@<ip-du-vps>
cd /srv/fitradarhr && make deploy
```

⚠️ **`/srv/proxy/Caddyfile` n'est PAS resynchronisé automatiquement par `make deploy`** —
il a été copié une seule fois par `setup-server.sh` et vit depuis en dehors du dépôt
applicatif (voir `docs/technical/deploy.md`). Le bloc `analytics.fitradarhr.fr` ajouté
dans `deploy/proxy/Caddyfile` doit être reporté à la main dans `/srv/proxy/Caddyfile`
(étape 3 ci-dessous).

### 1. DNS

Dans la zone DNS Scaleway de `fitradarhr.fr`, ajouter :

| Type | Nom | Valeur |
|---|---|---|
| A | `analytics` | IP du VPS (même IP que `fitradarhr.fr`) |

Vérifier la propagation : `dig +short analytics.fitradarhr.fr`.

### 2. Lancer Matomo

```bash
mkdir -p /srv/matomo && cd /srv/matomo
# copier deploy/matomo/docker-compose.yml et deploy/matomo/.env.matomo.example (→ .env)
nano .env   # remplir MATOMO_DB_PASSWORD et MATOMO_DB_ROOT_PASSWORD (générer avec
            # python3 -c "import secrets; print(secrets.token_urlsafe(24))")
docker compose up -d
```

### 3. Router le sous-domaine (Caddy)

Éditer `/srv/proxy/Caddyfile` sur le serveur, y ajouter le bloc (identique à celui déjà
présent dans `deploy/proxy/Caddyfile` du dépôt) :

```
analytics.fitradarhr.fr {
	encode gzip
	reverse_proxy matomo-web:80
}
```

Puis recharger Caddy sans coupure :

```bash
cd /srv/proxy && docker compose exec caddy caddy reload --config /etc/caddy/Caddyfile
```

### 4. Assistant d'installation Matomo

Ouvrir `https://analytics.fitradarhr.fr` et suivre l'assistant :
- Compte admin **local à l'instance** (pas de compte Matomo.org — tout reste
  auto-hébergé, aucune donnée transmise à Matomo l'entreprise)
- Créer le site « FitRadarHR », URL `https://fitradarhr.fr` → note le **Site ID**
  affiché (visible aussi ensuite dans Administration → Sites web → Gérer)

### 5. Configuration exemption CNIL

Appliquer la checklist de la section suivante avant d'activer le tracker côté app —
sans ces réglages, Matomo redevient soumis à consentement.

### 6. Activer le tracker côté app

```bash
cd /srv/fitradarhr && nano .env
# MATOMO_URL=https://analytics.fitradarhr.fr
# MATOMO_SITE_ID=<le Site ID noté à l'étape 4>
make prod-build   # ou : docker compose --env-file .env -f docker/docker-compose.prod.yml --profile demo up -d
```

### 7. Vérifier

- Visiter `https://fitradarhr.fr` (hors org de démo, sinon le tracker reste
  volontairement désactivé), ouvrir Matomo → Visiteurs → Temps réel : la visite doit
  apparaître en quelques secondes
- DevTools → Application → Cookies sur `fitradarhr.fr` : aucun cookie Matomo (`_pk_*`)
  ne doit être présent — confirme le mode cookieless
- Naviguer via un lien HTMX (ex. changer de page dans un tableau) : vérifier dans
  Matomo → Comportement → Pages que la navigation est bien comptée comme une pageview
  distincte (sinon revérifier le hook `htmx:pushedIntoHistory` dans `base.html`)

### 8. Créer les funnels

Voir section « Repérer les points de blocage » plus bas — se fait entièrement dans
l'UI Matomo, aucun redéploiement nécessaire.

## Configuration exemption CNIL (obligatoire, à faire dans l'admin Matomo)

Checklist basée sur le guide officiel CNIL pour Matomo Analytics. Sans ces réglages,
Matomo redevient soumis à consentement.

1. **Administration → Confidentialité des données des visiteurs**
   - Anonymiser les adresses IP des visiteurs : activé, masquer au moins les 2 derniers
     octets (2 recommandé, 3 pour aller au-delà du minimum)
   - Désactiver la réutilisation des cookies existants / le fingerprinting de secours
   - Durée de conservation des rapports détaillés : 25 mois maximum
2. **Administration → Sites web → gérer** : désactiver le suivi cross-domain et le
   partage de données entre sites si plusieurs sites sont créés dans l'instance
3. **Tracker JS** (déjà fait côté code, `templates/base.html`) : `disableCookies()`
   appelé avant `trackPageView` — aucun cookie déposé chez le visiteur
4. **Ne jamais activer** : le suivi publicitaire, l'export de données vers un tiers, le
   « User ID » avec identifiant personnel (email, nom) — resterait dans le champ du
   RGPD classique et sortirait de l'exemption
5. Informer les utilisateurs : mention déjà ajoutée dans la politique de confidentialité
   de l'app (section « Mesure d'audience »)

Référence : [Guide de configuration Matomo Analytics — CNIL (PDF)](https://www.cnil.fr/sites/cnil/files/atoms/files/matomo_analytics_-_exemption_-_guide_de_configuration.pdf)

## Suivre les fonctionnalités les plus utilisées

Le tracking de pages vues (natif + hook HTMX pour les navigations partielles, voir
`base.html`) suffit pour :
- Volume de visites / utilisateurs actifs (Visiteurs → Aperçu)
- Pages et fonctionnalités les plus consultées (Comportement → Pages)
- Répartition par organisation n'est **pas** possible sans donnée personnelle — Matomo
  reste agrégé au niveau du site, pas par tenant. Si un jour un besoin business le
  justifie (ex. usage par plan payant), il faudra un événement custom explicitement
  anonymisé (jamais d'org_id ou d'email en clair dans un événement Matomo).

## Repérer les points de blocage (funnels)

Matomo propose une fonctionnalité **Funnels** (Administration → Objectifs → Funnels,
premium activable gratuitement en self-hosted) basée sur des étapes définies par URL —
pas de code à ajouter. Funnels à créer en priorité :

1. **Questionnaire Big Five** : lien reçu → page de consentement RGPD → bloc 1 → bloc 2
   → ... → page de résultat. Permet de voir à quel bloc les répondants abandonnent.
2. **Création de poste** : liste des postes → formulaire → profil Big Five du poste →
   poste publié.
3. **Création d'équipe** : liste des équipes → formulaire → ajout de membres → équipe
   créée.

Ces funnels se configurent entièrement dans l'interface Matomo (Objectifs → Funnels →
Créer un funnel, en listant les URLs des étapes) — aucune modification de code
nécessaire, grâce au hook HTMX déjà en place qui garantit qu'un changement de « page »
HTMX déclenche bien un `trackPageView` avec la bonne URL.

## Ce qu'on ne fait pas (et pourquoi)

- **Pas de heatmaps / session recording** : hors périmètre du besoin exprimé (volume +
  fonctionnalités + blocages), et plus sensible en termes de vie privée (peut capturer
  du texte saisi) — à réévaluer séparément si le besoin apparaît, avec revue RGPD dédiée.
- **Pas de tracking par organisation/tenant** : irait à l'encontre du principe de
  minimisation et sortirait du cadre de l'exemption CNIL.
- **Pas de tracking dans l'org de démo** : évite de polluer les statistiques produit
  avec du trafic non représentatif.
