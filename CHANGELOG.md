# Changelog

Toutes les évolutions notables de FitRadarHR sont documentées ici.
Format inspiré de [Keep a Changelog](https://keepachangelog.com/fr/1.1.0/) —
le projet n'étant pas encore versionné, les entrées sont datées.

## 2026-07-06 (15)

### Ajouté
- **Kit de déploiement production** (VPS Scaleway Dedibox, Ubuntu 24.04,
  domaine `fitradarhr.fr`) — architecture **multi-sites** : un reverse proxy
  Caddy central (`/srv/proxy`, HTTPS Let's Encrypt automatique) route par
  domaine vers chaque projet via un réseau docker `web` partagé.
  - `docker/docker-compose.prod.yml` (remplace `docker/docker-compose.yml`) :
    aucun port publié, nginx interne (`fitradarhr-web`) pour statiques/média,
    volume `static_data` partagé, migrations + collectstatic au démarrage.
  - `deploy/setup-server.sh` : installation complète du serveur en une commande
    (utilisateur sudo, durcissement SSH, UFW, fail2ban, unattended-upgrades,
    Docker, réseau `web`, proxy Caddy). Idempotent.
  - `deploy/backup.sh` + `deploy/install-crons.sh` : backup PostgreSQL
    quotidien (rotation 14 j) et cron `send_reminders` à 8h (relances J+3 —
    jusqu'ici jamais planifiées nulle part).
  - `core/settings.py` : `SECURE_PROXY_SSL_HEADER` + `CSRF_TRUSTED_ORIGINS`
    dérivées d'`ALLOWED_HOSTS` (fonctionnement derrière proxy TLS).
  - `.env.prod.example`, cibles make (`deploy`, `prod-logs`, `backup`…),
    runbook complet `docs/technical/deploy.md`, `stack.md` mis à jour
    (Scaleway, Caddy, SMTP Brevo).

## 2026-07-06 (14)

### Modifié
- **Passage au freemium — suppression de l'essai 14 jours** : le plan gratuit
  (25 personnes max) s'applique désormais **sans limite de durée** dès la
  création de l'organisation — plus de compte à rebours "Essai gratuit —
  X jour(s) restant(s)". Sous le seuil, FitRadarHR est utilisable gratuitement
  aussi longtemps qu'on le souhaite ; au-delà, un abonnement unique à
  **39 €/mois** lève la limite.
  - Modèle `Subscription` : statuts `free`/`active`/`past_due`/`canceled`
    (le statut `trialing` et le champ `trial_ends_at` sont supprimés —
    migration `billing.0002`, les essais en cours basculent sur le plan
    gratuit). Un statut Stripe `trialing` reçu par webhook est traité comme
    un abonnement actif.
  - Écran `/settings/billing/` : nouveau copy (compteur "X personne(s) sur
    25", prix affiché — le prix facturé reste configuré côté Stripe via
    `STRIPE_PRICE_ID`, à garder cohérent).
  - Mise à jour : tests, doc utilisateur (`billing.md`), `schema.md`,
    US-E1-07, roadmap, traductions EN/ES/DE.

## 2026-07-06 (13)

### Modifié
- **Simplification du modèle payant** : le plan gratuit passe d'une triple
  limite (3 postes actifs, 10 personnes, 5 questionnaires/mois) à un **seuil
  unique et cumulé de 25 personnes** dans l'organisation
  (`apps/billing/quotas.py`).
  - Création de postes désormais libre — c'est le début du parcours, pas
    l'endroit où mettre de la friction. Limite mensuelle de questionnaires
    supprimée — le nombre de personnes capture implicitement ce volume,
    chaque personne recevant en général un lien.
  - L'envoi d'un questionnaire à une personne existante reste libre ; seule la
    création à la volée d'une nouvelle personne lors de l'envoi est soumise au
    seuil (sinon la limite serait contournable par ce chemin).
  - Mise à jour : écran `/settings/billing/`, tests, doc utilisateur
    (`billing.md`), `stack.md`, `schema.md`, US-E1-07, traductions EN/ES/DE.

## 2026-07-04 (12)

### Modifié
- **Refonte du menu de navigation principal** (US-E1-08) : les liens (jusqu'à
  11 pour un RH) sont désormais regroupés en 4 catégories avec sous-menus
  déroulants — Organisation (Départements, Équipes, Membres), Recrutement
  (Postes, Questionnaires, Rapports), Pilotage (Analytics, Audit), Paramètres
  (SSO, API, Abonnement). Corrige le chevauchement avec le logo constaté sur
  écran standard à mesure des ajouts de fonctionnalités.
  - Nouveau template tag `navbar_categories` (`apps/accounts/templatetags/navbar_tags.py`)
    : source unique des catégories/liens (et de leur restriction RH), partagée
    entre le rendu desktop (menus déroulants Alpine.js) et le panneau mobile
    (accordéon empilé) — évite toute divergence entre les deux.
  - Comportement mobile : bouton menu burger sous le seuil `lg`, panneau
    empilé par catégorie.
  - Dropdowns utilisables au clavier (fermeture Échap, clic extérieur), sans
    changement des routes existantes.
  - i18n : nouveaux libellés "Recrutement", "Pilotage", "Paramètres", "Menu"
    traduits EN/ES/DE ("Organisation" déjà présent au catalogue).

## 2026-07-03 (11)

### Ajouté
- **Essai gratuit et abonnement** (item #2 roadmap V3, RICE 3.84, US-E1-07) :
  nouvelle app `apps.billing`, essai gratuit de 14 jours démarré automatiquement
  à la création de toute organisation (B2B et B2C), puis un unique plan payant
  via Stripe.
  - Modèle `Subscription` (1:1 `Organization`) : `status` (`trialing`/`active`/
    `past_due`/`canceled`), `trial_ends_at`, identifiants Stripe. Source de
    vérité côté FitRadarHR, mise à jour uniquement par un webhook Stripe signé
    (`/billing/webhook/`, hors `i18n_patterns`) — jamais interrogée en direct.
  - Stripe Checkout (souscription) + Stripe Customer Portal (gestion,
    résiliation) — aucun flux de paiement ré-implémenté ; le prix est un objet
    Stripe (`STRIPE_PRICE_ID`), jamais en dur dans le code. Écran
    `/settings/billing/` (RH only) affichant le statut et les actions,
    avec repli "configuration Stripe requise" si les clés ne sont pas
    renseignées, plutôt que de planter.
  - **Quotas du plan gratuit** (`apps/billing/quotas.py`), appliqués uniquement
    une fois l'essai terminé sans abonnement actif : 3 postes actifs, 10
    personnes, 5 questionnaires envoyés par mois — jamais de blocage total,
    seule la création de nouvelles ressources est limitée. Branché sur la
    création de poste, création/import CSV de personnes, envoi de
    questionnaire. L'import CSV plafonne les créations au quota restant et
    signale le reste comme non importé plutôt que d'échouer entièrement.
  - L'organisation de démonstration publique est systématiquement exemptée
    (essai et quotas).
  - 30 nouveaux tests (essai automatique, accès complet en essai/payant,
    quotas par ressource, vues bloquantes, webhook Stripe mocké, accès RH only,
    isolation multi-tenant). 261 tests au total.
  - Documentation : `docs/user/getting-started/billing.md`, US-E1-07 dans
    `docs/product/user-stories.md`, entrées `docs/technical/stack.md` et
    `docs/technical/schema.md`.
  - `docs/user/about/roadmap.md` : item #2 V3 marqué livré.

## 2026-07-03 (10)

### Ajouté
- **Fit inversé — postes recommandés pour une personne** (item #1 roadmap V3,
  RICE 6.0, US-E6-07) : première brique de la V3, à partir d'un profil, un
  classement des postes actifs qui lui correspondent le mieux — l'inverse du
  classement des personnes sur un poste (E5).
  - Aucun nouveau calcul de fit : réutilise les `PositionFitResult` déjà
    produits par `compute_all_fits_for_person` (E5) — nouvelle vue seulement
    (`apps/reports/services.py::build_person_position_ranking_context`).
  - Nouvelle page `/reports/person/<id>/positions/` (filtre optionnel par
    département), export PDF cohérent avec les autres rapports, traçabilité
    (journal d'audit `position_ranking.viewed`/`exported_pdf`).
  - Points d'entrée depuis la section "Fit Postes" du profil individuel et
    depuis la liste des rapports.
  - 6 nouveaux tests (tri par fit décroissant, filtre département, export
    PDF, isolation multi-tenant, audit, état vide). 231 tests au total.
  - `docs/user/about/roadmap.md` : item #1 V3 marqué livré.

## 2026-07-03 (9)

### Ajouté
- **API publique en lecture seule** (item #9 roadmap V2, RICE 0.3, US-E1-06) :
  nouvelle app `apps.api`, montée hors `i18n_patterns` sous `/api/v1/`.
  - Modèle `ApiKey` : une organisation génère une clé (préfixe `frk_`), affichée
    en clair **une seule fois** ; seule son empreinte SHA-256 (`key_hash`) est
    stockée. Révocation par horodatage (`revoked_at`), jamais de suppression
    physique — cohérent avec l'`AuditLog` immuable du reste du produit.
  - Authentification par en-tête `Authorization: Api-Key <clé>` (décorateurs
    `apps/api/auth.py::api_key_required`/`api_get_endpoint`), scoping strict
    via `request.api_org` — mêmes garanties multi-tenant que le reste de
    l'application (`.for_org()`).
  - 8 endpoints JSON strictement GET : postes, équipes, personnes (+ statut
    questionnaire), résultats de fit Poste/Équipe. **Les scores Big Five bruts
    ne sont jamais exposés** — seul un indicateur booléen "profil renseigné" et
    les résultats de fit dérivés le sont, par choix produit RGPD (minimisation
    des données transmises à des tiers), confirmé explicitement en amont du
    développement.
  - Pagination maison (`Paginator`, `page`/`page_size`, max 100/page) — pas de
    dépendance ajoutée à Django REST Framework, cohérent avec le style du
    projet.
  - Écran de gestion `/settings/api/` (RH only) : génération, liste (préfixe,
    dates, statut), révocation.
  - 32 nouveaux tests : authentification (succès/échec/clé révoquée),
    isolation cross-tenant, pagination, contenu des 8 endpoints (avec garde-fou
    explicite contre toute fuite de score Big Five brut), accès RH only de
    l'écran de gestion.
  - Documentation : `docs/user/getting-started/api.md` (authentification,
    référence des endpoints, pagination, exemples `curl`), US-E1-06 dans
    `docs/product/user-stories.md`, entrées `docs/technical/stack.md` et
    `docs/technical/schema.md`.

## 2026-07-03 (8)

### Ajouté
- **Traductions ES/DE — parité complète, questionnaire inclus** (item #8
  roadmap V2, RICE 0.8, US-E7-03) : FitRadarHR est maintenant disponible en
  français, anglais, espagnol et allemand — interface **et** questionnaire
  Big Five IPIP-100, pas seulement la chrome UI.
  - Questionnaire IPIP-100 (`apps/survey/ipip_data.py`) : traduction allemande
    sourcée sur la traduction officielle IPIP 100 items (Streib & Wiedmaier,
    2001, Universität Bielefeld) — couverture 100/100. Traduction espagnole
    sourcée sur la traduction officielle IPIP 50 items (de Oliveira, Cherubini
    & Oliver, 2013, ACM TOCHI) pour les 50 premiers items ; les 50 items
    d'extension (51–100) et les 4 items sans équivalent Goldberg (C5, C10, O4,
    O5, déjà des adaptations FR/EN maison) sont traduits en interne — limite
    documentée avec disclaimer utilisateur (`docs/user/about/big-five.md`) et
    méthodologie complète (`docs/product/translations-ipip.md`).
  - Échelles de réponse `SCALE_DE`/`SCALE_ES` (Likert 1-5), dict `SCALES`
    indexé par code langue.
  - Contenus de rapport traduits : libellés de dimension
    (`apps/fit/engine.py::DIMENSION_LABELS`), infobulles OCEAN et « points à
    approfondir » Fit Poste/Fit Équipe (`apps/reports/insights.py`), templates
    PDF (`templates/reports/pdf/*.html`, convertis du branchement `{% if lang
    == "fr" %}` en `{% trans %}`).
  - `QuestionnaireLink.Language`, `Organization.Language`, `User.Language`
    étendus à ES/DE ; `settings.LANGUAGES` ; sélecteur de langue de la navbar
    et filtre `strip_lang_prefix` généralisés à N langues (au lieu d'un
    traitement spécifique à `/en/`).
  - Catalogue UI complet traduit : `locale/es/LC_MESSAGES/django.po`(.mo) et
    `locale/de/LC_MESSAGES/django.po`(.mo), 478 chaînes chacun (formes
    plurielles incluses).
  - Templates de passation (`consent.html`, `questions.html`, `done.html`,
    emails d'invitation/relance/confirmation) migrés du branchement bilingue
    FR/EN codé en dur vers `{% trans %}`/`{% blocktrans %}`, langue activée via
    `translation.override(link.language)`.
- 24 nouveaux tests (couverture traductions IPIP — garde-fou anti-oubli DE/ES
  identiques au FR/EN —, scoring indépendant de la langue, rendu des pages de
  passation en DE/ES, contenus de rapport DE/ES, couverture du catalogue UI,
  extension des `Language.choices`) — 193 tests au total.

## 2026-07-03 (7)

### Modifié
- **Changement de licence : MIT → Fair Source (FSL-1.1-MIT)**. Le code reste public,
  consultable, modifiable et auto-hébergeable pour un usage interne, éducatif ou de
  recherche ; seul un usage commercial concurrent (revendre ou héberger un service
  qui se substitue à FitRadarHR) reste réservé sans autorisation. Chaque version
  repasse automatiquement en MIT deux ans après sa publication.
  Raison : possibilité envisagée d'une offre payante future (essai gratuit puis
  abonnement) — voir `CLAUDE.md`. Fichiers mis à jour : `LICENSE` (nouveau),
  `README.md`, `docs/user/index.md`, `docs/user/about/license.md`, landing page,
  pied de page, politique de confidentialité (toute mention "licence MIT" retirée
  des pages publiques). 4 nouveaux tests (contenu des pages, i18n) — 169 tests
  au total.

## 2026-07-03 (6)

### Ajouté
- **Connexion SSO Keycloak/OIDC** (item #7 roadmap V2, RICE 0.8, US-E1-05) :
  chaque organisation peut connecter son propre fournisseur d'identité OIDC
  (Keycloak ou équivalent) — écran de configuration RH (`/settings/sso/`),
  point d'entrée public de connexion (`/login/sso/`), provisioning JIT d'un
  compte à la première connexion. Le SSO s'ajoute à l'email/mot de passe
  existant, il ne le remplace jamais. Isolation stricte multi-tenant : un
  IdP par org, aucun partage de configuration, refus explicite en cas de
  collision d'email entre deux organisations.
  Intégration technique : `allauth.socialaccount` + provider générique
  `openid_connect`, un `SocialApp` synchronisé par organisation
  (`apps/accounts/sso.py`) — le flux OAuth2/OIDC (échange de jetons,
  validation JWT) s'appuie sur allauth plutôt que d'être ré-écrit.
- 22 nouveaux tests (synchro modèle ↔ SocialApp, isolation multi-tenant,
  provisioning JIT scopé par org, refus cross-org, i18n) — 165 tests au total.
- Documentation utilisateur `docs/user/getting-started/sso.md` et mise à
  jour de `docs/product/user-stories.md` (US-E1-05), `docs/technical/schema.md`
  et `docs/technical/stack.md`.

**⚠️ À valider avec un IdP réel avant mise en production** : le provisioning
JIT et l'isolation multi-tenant sont testés unitairement, mais l'échange
OAuth2/OIDC complet (redirection, callback, validation du jeton) nécessite un
Keycloak (ou équivalent) réel pour une validation de bout en bout — non
disponible dans l'environnement de test automatisé.

## 2026-07-03 (5)

### Ajouté
- **Cohortes de rétention** (item #6 roadmap V2, RICE 2.1) : nouvelle section
  sur `/reports/analytics/` — pour chaque cohorte (mois de première passation
  complétée), taux de consultation du rapport de profil mois par mois (M0,
  M1, M2…), en heatmap. Granularité mensuelle plutôt qu'hebdomadaire (org-scoped,
  volumes trop faibles pour du hebdo) — rationale dans `docs/product/metrics.md`.
  Une re-passation (item #5) ne recrée jamais de cohorte fantôme.
- 7 nouveaux tests (tailles/taux de cohorte, offsets futurs, isolation
  multi-tenant, non-régression re-passation, i18n) — 143 tests au total.

## 2026-07-03 (4)

### Ajouté
- **Re-passation & suivi longitudinal** (item #5 roadmap V2, RICE 4.5) : chaque
  nouvelle passation du questionnaire archive automatiquement le profil Big
  Five précédent (`BigFiveProfileHistory`, additif — le profil courant reste
  inchangé pour tous les calculs de fit). Le rapport de profil affiche une
  section « Évolution du profil » (courbe + tableau, HTML et PDF) dès qu'un
  historique existe, avec un bouton « Repasser le questionnaire ».
- 8 nouveaux tests (archivage à la re-passation, isolation multi-tenant de
  l'historique, rendu PDF, couverture i18n) — 136 tests au total.

## 2026-07-03 (3)

### Ajouté
- **Import CSV des personnes** (item #4 roadmap V2, RICE 4.0) : `teams/persons/import/` —
  upload d'un fichier CSV (`first_name,last_name,email,person_type`), modèle téléchargeable,
  validation ligne par ligne (email invalide, doublons fichier/org ignorés proprement).
- **Invitation de managers** (item #2 roadmap V2, RICE 5.6) : page `/members/` (RH only) —
  invite un utilisateur avec le rôle Manager dans l'org ; le compte est créé sans mot de
  passe utilisable et l'invité reçoit un email (réutilise le flux "mot de passe oublié"
  d'allauth) pour définir le sien.
- **Comparaison de candidats sur un poste** (item #3 roadmap V2, RICE 4.8) : depuis le
  classement de fit d'un poste, sélection de 2 à 5 personnes → radar superposé + tableau
  comparatif par dimension (`positions/<id>/compare/`).
- 128 tests au total (+23 depuis la version précédente).

### Corrigé
- **Traductions anglaises manquantes** : les 3 fonctionnalités ci-dessus ajoutaient 33
  nouvelles chaînes sans équivalent dans `locale/en/LC_MESSAGES/django.po` — un
  utilisateur en anglais voyait du français sur ces écrans. Comblé, avec un test par
  fonctionnalité vérifiant la couverture du catalogue EN.

## 2026-07-03 (2)

### Ajouté
- **Relances automatiques de questionnaire** (item #1 de la roadmap V2, RICE 12.8) :
  commande `manage.py send_reminders` — relance par email les questionnaires
  envoyés depuis 3 jours et non complétés, une seule fois par lien
  (`reminder_sent_at`). Garde-fou démo identique aux autres emails. Cibles
  `make remind` / `make remind-dry-run`, à planifier via cron côté hébergement.
- Identité visuelle FitRadarHR (logo icône radar + wordmark), intégrée au
  favicon, à la navbar, au README et à la doc utilisateur (`branding/`).

### Corrigé
- Déploiement GitHub Pages : le workflow `docs.yml` poussait vers la branche
  `gh-pages` alors que la Source Pages du dépôt est en mode "GitHub Actions" —
  plus aucun nouveau contenu n'était donc publié depuis le tout premier
  déploiement. Migré vers `actions/deploy-pages` (natif).

## 2026-07-03

### Ajouté
- **Environnement de démonstration public** : org fictive « Nexatech » (~100 personnes,
  10 équipes aux profils OCEAN contrastés) générée par `manage.py seed_demo` —
  idempotente et déterministe. Bouton « Essayer la démo » (connexion un clic, sans
  mot de passe, activé par `DEMO_MODE=True`), bannière dédiée, reset quotidien via
  le service Docker `demo-reset` (`--profile demo`).
- **Garde-fous démo** : aucun email réel envoyé (lien de passation affiché à l'écran),
  effacement RGPD désactivé, emails fictifs sur domaines réservés `.example`.
- **Page Analytics** (`/reports/analytics/`, rôle RH) : funnel questionnaire
  (envoyé → commencé → complété), taux de complétion, délai moyen de passation,
  couverture des profils, profils par mois, engagement 30 j (issu du journal
  d'audit — zéro tracking tiers), fit moyen par poste.
- **Doc métriques produit** (`docs/product/metrics.md`) : North Star, funnel AARRR,
  définitions des KPIs, anti-métriques.
- Roadmap publique V2 priorisée RICE, changelog, widget de feedback in-app,
  landing page publique.

## 2026-07-02

### Ajouté
- Questionnaire IPIP-100 (version longue) en plus du 50 items.
- Infobulles OCEAN au survol des dimensions (rapports et profil cible).
- « Points à approfondir » sur les rapports Fit Poste et Fit Équipe — questions
  d'entretien suggérées, jamais de conclusion automatique.
- Suite de tests : scoring IPIP, moteur de fit, isolation multi-tenant, droits, RGPD.
- CI GitHub Actions : tests + system check à chaque push/PR.

### Modifié
- Managers multi-tenant généralisés (`OrgQuerySet` — convention `for_org()`).
- Rapports HTML et PDF dédoublonnés via des context builders partagés.
- Labels de complémentarité et emails passés par gettext (règle i18n du cadrage).

### Supprimé
- Modèle `FitReport` (code mort) et app `api` vide.

## 2026-07-01

### Ajouté
- Gestion des postes : liste, création, modification, archivage, profil Big Five
  cible, classement des personnes par fit (E2).
- Départements : CRUD complet, rattachement des postes et équipes (E2.5).
- Gestion des équipes : liste, création, membres, liste des personnes (E3).
- Questionnaire Big Five : envoi de lien tokenisé, création de personne à la volée,
  consentement RGPD explicite, passation par blocs avec reprise, scoring OCEAN (E4).
- Moteur de calcul Fit : fit poste (plage cible), fit équipe (agrégat +
  complémentarité), recalcul automatique des coéquipiers (E5).
- Rapports : profil OCEAN, Fit Poste, Fit Équipe, radar charts, export PDF
  WeasyPrint (E6).
- Internationalisation FR/EN complète — 260+ strings (E7).
- Conformité : journal d'audit immuable, droit à l'effacement (anonymisation),
  politique de confidentialité (E8).
- Dashboard enrichi : stats org, questionnaires en attente, profils récents,
  activité d'audit.
- Documentation utilisateur MkDocs Material publiée sur GitHub Pages.

## 2026-06-30

### Ajouté
- Cadrage produit complet (vision, périmètre, règles non négociables, epics E1–E8).
- User stories E1–E8, stack technique, schéma de données.
- Scaffold Django : modèles, migrations, inscription B2B/B2C, Docker Compose.
