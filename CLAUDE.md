# CLAUDE.md — Contexte projet pour Claude Code

> Ce fichier est lu automatiquement par Claude Code à chaque session dans ce dépôt.
> Il donne le contexte produit et les règles à respecter sans avoir à les répéter.

## Le projet

**FitRadarHR** — un outil bilingue (FR/EN), au code source ouvert (licence Fair Source
FSL-1.1-MIT depuis le 2026-07-03 — anciennement MIT), qui aide les RH et managers à évaluer
la compatibilité d'une personne (candidat ou collaborateur en mobilité interne) avec un poste
et/ou une équipe, en s'appuyant sur le modèle de personnalité **Big Five / OCEAN**
(questionnaire IPIP, domaine public).

> **Licence (2026-07-03)** : passage de MIT à FSL-1.1-MIT — le code reste librement
> consultable, modifiable et auto-hébergeable, mais un usage commercial concurrent est
> réservé sans autorisation. Conversion automatique en MIT deux ans après chaque
> publication. Raison : Damien envisage une éventuelle offre payante à terme (plan gratuit ≤ 25 personnes
> puis abonnement 39 €/mois) et voulait garder cette option ouverte sans bloquer la vitrine publique
> du code. Voir `LICENSE` et `docs/user/about/license.md`.

Le cadrage produit complet est dans `docs/product/00-cadrage.md` — à lire avant toute
décision de conception ou de développement structurante.

## Règles non négociables

Ces règles sont issues du cadrage produit et ne doivent jamais être contournées, même si
une demande future semble les justifier ponctuellement :

1. **Jamais d'analyse de CV / lettre de motivation / document libre pour en déduire un
   profil psychologique.** Seul le questionnaire Big Five validé (IPIP) qualifie un profil.
2. **Jamais de score de décision automatique** ("recommandé / non recommandé"). Le produit
   informe, il ne décide jamais — principe de "human in the loop" à chaque restitution.
3. **Jamais de typologie non scientifiquement validée** (MBTI, etc.) comme fondement du
   produit.
4. Toute fonctionnalité touchant aux données de personnalité doit respecter le RGPD
   (consentement explicite, droit d'accès/suppression, minimisation) et anticiper le
   classement "haut risque" de l'EU AI Act (traçabilité, supervision humaine documentée).
5. Le produit est bilingue FR/EN **dès la conception** — pas une couche ajoutée après coup.
   Toute string utilisateur doit passer par le système d'i18n, jamais de texte en dur.

## Structure du dépôt

```
/apps
  /accounts        → utilisateurs, tenants B2B/B2C, rôles (E1)
  /departments     → gestion des départements (E2.5)
  /positions       → gestion des postes (E2)
  /teams           → gestion des équipes (E3)
  /survey          → questionnaire Big Five, liens tokenisés (E4)
  /fit             → moteur de calcul Fit (E5)
  /reports         → restitution, radar chart, export PDF (E6)
/core              → settings Django, URLs racine
/templates         → Django templates + HTMX
/static            → assets frontend
/locale            → fichiers de traduction FR / EN (.po / .mo)
/docker            → Dockerfile, docker-compose.yml, nginx.conf
/docs
  /product
    00-cadrage.md        # Cadrage produit complet (vision, périmètre, epics)
    user-stories.md      # User stories E1–E8
  /technical
    stack.md             # Décisions techniques (stack, déploiement)
    schema.md            # Schéma de données (ER + entités)
  /user                  # Documentation utilisateur (publiée sur GitHub Pages via MkDocs)
CLAUDE.md                # Ce fichier
README.md                # Présentation du projet (pour GitHub)
mkdocs.yml               # Config MkDocs Material (doc utilisateur → GitHub Pages)
requirements.txt         # Dépendances Python (app Django)
requirements-docs.txt    # Dépendances docs (mkdocs + material)
Makefile                 # Commandes courantes (make dev, make migrate, etc.)
```

## Epics de référence

User stories à rattacher systématiquement à l'un de ces epics (voir `00-cadrage.md` section 8) :

| # | Epic | Statut |
|---|---|---|
| E1 | Authentification & organisations | ✅ Modèles + inscription B2B/B2C + dashboard |
| E2 | Gestion des postes | ✅ Liste, création, modification, archivage, profil Big Five, classement Fit |
| E2.5 | Départements | ✅ CRUD complet, FK Poste + Équipe, data migration |
| E3 | Gestion des équipes | ✅ Liste, création, modification, membres, Personnes, rattachement département |
| E4 | Questionnaire Big Five | ✅ Envoi lien, création personne à la volée, rattachement poste, passation, scoring |
| E5 | Moteur de calcul de Fit | ✅ Fit Poste + Fit Équipe + complémentarité + recalcul coéquipiers |
| E6 | Rapports & restitution | ✅ Profil OCEAN, Fit Poste, Fit Équipe, radar charts, export PDF, fit équipe cible, infobulles OCEAN, points à approfondir |
| E7 | Internationalisation | ✅ FR/EN/ES/DE — 478 strings UI + questionnaire IPIP-100 traduit (ES/DE sourcés sur traductions officielles quand elles existent) |
| E8 | Conformité & gouvernance | ✅ Droit à l'effacement, audit log viewer, politique de confidentialité |

## État d'avancement

- [x] Cadrage produit validé
- [x] User stories E1–E8 + UX rédigées
- [x] Stack technique définie (`docs/technical/stack.md`)
- [x] Schéma de données complet (`docs/technical/schema.md`)
- [x] Scaffold Django (modèles, migrations, auth B2B/B2C, dashboard)
- [x] Docker Compose dev opérationnel (`make dev-build`)
- [x] Documentation utilisateur publiée (MkDocs → GitHub Pages)
- [x] Vues Postes — liste, création, détail, modification, archivage, profil Big Five, classement Fit (E2)
- [x] Départements — CRUD complet, FK sur Poste et Équipe, data migration depuis champ texte (E2.5)
- [x] Vues Équipes — liste, création, détail, modification, membres, liste Personnes, rattachement département (E3)
- [x] Questionnaire Big Five — envoi lien, création personne à la volée, rattachement poste, consentement RGPD, passation par blocs, scoring OCEAN, profil sauvegardé (E4)
- [x] Moteur de calcul Fit — Fit Poste (plage OCEAN), Fit Équipe (agrégat + complémentarité), recalcul coéquipiers, déclenchement auto (E5)
- [x] Rapports & radar chart — profil OCEAN, fit poste, fit équipe, complémentarité, fit équipe cible depuis profil (E6)
- [x] Export PDF — WeasyPrint, templates CSS-only, boutons sur les 3 rapports (E6)
- [x] Dashboard enrichi — stats org, questionnaires en attente (dédupliqués), profils récents, activité audit
- [x] Conformité RGPD — droit à l'effacement (anonymize), audit log viewer paginé, politique de confidentialité (E8)
- [x] Améliorations UX — pré-remplissage email questionnaire, autocomplétion ajout membre, modification personne, fix switch langue, déduplication dashboard survey, compteur dashboard corrigé
- [x] Infobulles OCEAN — tooltip au survol des libellés de dimension sur tous les rapports (profil, Fit Poste, Fit Équipe) (E6)
- [x] Points à approfondir — section contextuelle sur les rapports Fit Poste et Fit Équipe, framing "questions à explorer", disponible aussi en PDF (E6)
- [x] Suite de tests — 89 tests : scoring IPIP, moteur de fit, isolation multi-tenant, droits, RGPD, mode démo (`make test-fast`, SQLite via `core/settings_test.py`)
- [x] Refacto — managers `OrgQuerySet` généralisés (`core/managers.py`), context builders rapports partagés HTML/PDF (`apps/reports/services.py`), nettoyages (app api supprimée, forms signup, STORAGES Django 5)
- [x] Analytics produit — page `/reports/analytics/` (RH) : funnel questionnaire (envoyé→commencé→complété), taux de complétion, délai moyen, couverture des profils, profils/mois (Chart.js), engagement 30 j via audit log, fit moyen par poste ; définitions dans `docs/product/metrics.md` (North Star, AARRR, anti-métriques)
- [x] Vitrine produit — landing page publique (`/`, i18n), widget de feedback in-app (modèle `Feedback` org-scoped, admin lecture seule), roadmap publique V2 priorisée RICE (`docs/user/about/roadmap.md`), `CHANGELOG.md`, making-of PM × IA (`docs/product/making-of.md`), README enrichi (badges CI/docs, fonctionnalités, statut V1)
- [x] Mode démo public — org fictive « Nexatech » (~100 pers., 10 équipes aux archétypes OCEAN contrastés) seedée par `manage.py seed_demo` (idempotente, déterministe), bouton "Essayer la démo" (connexion sans mot de passe, `DEMO_MODE=True`), bannière, garde-fous (aucun email réel — lien affiché à l'écran, effacement RGPD désactivé, domaines `.example`), reset 24 h via service `demo-reset` (`--profile demo`), doc utilisateur `getting-started/demo.md`
- [x] SSO Keycloak/OIDC — un IdP par organisation, additif au mot de passe, provisioning JIT scopé par org, écran `/settings/sso/`, point d'entrée `/login/sso/` (roadmap V2 #7, US-E1-05)
- [x] Licence Fair Source (FSL-1.1-MIT) — remplace MIT, code toujours public/modifiable/auto-hébergeable, usage commercial concurrent réservé, conversion en MIT 2 ans après chaque publication
- [x] POC design tokens (labo perso, hors prod) — extraction du design system implicite en tokens Figma/Tokens Studio (`design/tokens/tokens.json`), générateur CSS (`build_css.py`), maquette Dashboard consommant les tokens (`design/mockups/dashboard.html`), démarche documentée dans `docs/technical/design-tokens.md`
- [x] Traduction ES/DE complète (roadmap V2 #8, US-E7-03) — questionnaire IPIP-100 traduit (DE 100/100 sourcé sur la traduction officielle Streib & Wiedmaier 2001 ; ES 50/100 officiels de Oliveira et al. 2013 + 50 items d'extension traduits en interne, limite documentée dans `docs/product/translations-ipip.md` et `docs/user/about/big-five.md`), contenus de rapport (libellés/infobulles/points à approfondir) en DE/ES, catalogue UI complet (478 chaînes) traduit, `Language.choices` étendu partout (questionnaire, org, utilisateur), 193 tests au total

## Conventions de travail

- **Stack** : Django 5 + HTMX + Alpine.js + Tailwind CSS + PostgreSQL 16 + Docker Compose
- **Auth** : django-allauth (email/password) + SSO OIDC optionnel par organisation
  (`allauth.socialaccount`, provider `openid_connect`, un `SocialApp` par org — voir
  `apps/accounts/sso.py`) — additif, jamais un remplacement du mot de passe
- **Commits** : Conventional Commits — `feat:`, `fix:`, `docs:`, `refactor:`, `test:`
- **User stories** : format `En tant que [rôle], je veux [besoin], afin de [valeur]`
  avec critères d'acceptation explicites, rédigées en français
- **Code et variables** : en anglais
- **i18n** : toute string UI via `gettext_lazy(_(...))`, jamais de texte en dur —
  4 langues (FR/EN/ES/DE). Exception assumée : le contenu du questionnaire IPIP
  (`apps/survey/ipip_data.py`) et les contenus de rapport indexés par dimension
  (`apps/fit/engine.py::DIMENSION_LABELS`, `apps/reports/insights.py`) utilisent des
  dicts `{"fr": ..., "en": ..., "de": ..., "es": ...}` plutôt que gettext, car ce sont
  des données scientifiques sourcées (traductions IPIP officielles), pas de la chrome UI
- **Multi-tenant** : chaque modèle lié à une org filtre systématiquement par `org_id`
  via un Django model manager (`OrgQuerySet` dans `core/managers.py` — `for_org()` /
  `get_org_object_or_404()`) — aucune vue ne peut afficher des données cross-tenant
- **Tests** : `make test-fast` (SQLite, sans Docker) ou `make test` (Docker/PostgreSQL) —
  toute nouvelle vue liée à une org doit avoir un test d'isolation cross-tenant
- **Doc utilisateur** : mise à jour dans `docs/user/` à chaque évolution de feature —
  le workflow GitHub Actions publie automatiquement sur GitHub Pages à chaque push sur `main`
