# Changelog

Toutes les évolutions notables de FitRadarHR sont documentées ici.
Format inspiré de [Keep a Changelog](https://keepachangelog.com/fr/1.1.0/) —
le projet n'étant pas encore versionné, les entrées sont datées.

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
