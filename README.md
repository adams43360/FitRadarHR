<img src="branding/logo-horizontal-color.svg" alt="FitRadarHR" width="360">

[![Tests](https://github.com/adams43360/FitRadarHR/actions/workflows/tests.yml/badge.svg)](https://github.com/adams43360/FitRadarHR/actions/workflows/tests.yml)
[![Docs](https://github.com/adams43360/FitRadarHR/actions/workflows/docs.yml/badge.svg)](https://adams43360.github.io/FitRadarHR)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> Projet porté en public pour démontrer une démarche produit de bout en bout — cadrage, delivery, mesure — menée par un Product Manager avec l'IA. Voir le [making-of](docs/product/making-of.md).

**FitRadarHR** est un outil **gratuit et open source** (MIT), bilingue FR/EN, qui aide les équipes RH et les managers à évaluer la compatibilité d'une personne — candidat à l'embauche ou collaborateur en mobilité interne — avec un poste et/ou une équipe, sur la base du modèle de personnalité scientifiquement validé **Big Five / OCEAN** (questionnaire IPIP, domaine public).

## Fonctionnalités

- **Questionnaire Big Five** (IPIP 50 ou 100 items) — lien tokenisé, consentement RGPD explicite, passation par blocs avec reprise, scoring OCEAN
- **Fit Poste** — profil cible par plages OCEAN, score de proximité par dimension, classement du vivier
- **Fit Équipe** — profil agrégé de l'équipe, signaux de complémentarité (similaire / différent / complémentaire)
- **Rapports** — radar charts, infobulles pédagogiques, « points à approfondir » en entretien, export PDF
- **Analytics** — funnel du questionnaire, taux de complétion, couverture des profils, engagement ([définitions des métriques](docs/product/metrics.md))
- **Multi-tenant** — organisations B2B et comptes personnels, isolation stricte par org
- **Conformité** — journal d'audit immuable, droit à l'effacement, politique de confidentialité
- **Mode démo** — environnement public « Nexatech » réinitialisé toutes les 24 h (`make seed-demo`)

## Principes fondateurs

- **Base scientifique uniquement** — Big Five (OCEAN) + questionnaire IPIP. Jamais de MBTI, jamais de déduction de personnalité à partir de CV ou lettre de motivation.
- **Human in the loop** — le produit informe, il ne décide jamais. Pas de score de recommandation binaire.
- **Conformité by design** — RGPD et EU AI Act (catégorie "haut risque") anticipés dès la conception : consentement explicite, journal d'audit immuable, droit à l'effacement.
- **Bilingue FR/EN dès la conception** — i18n native Django, aucune string en dur.
- **Gratuit et auto-hébergeable** — pas de SaaS fermé, déployable sur votre propre VPS.

## Documentation

- 📖 **[Documentation utilisateur](https://adams43360.github.io/FitRadarHR)** — guide complet sur GitHub Pages
- 🗺️ **[Roadmap publique V2](https://adams43360.github.io/FitRadarHR/about/roadmap/)** — priorisée RICE
- 📓 **[Changelog](CHANGELOG.md)**
- [`docs/product/00-cadrage.md`](docs/product/00-cadrage.md) — cadrage produit complet
- [`docs/product/user-stories.md`](docs/product/user-stories.md) — user stories E1–E8
- [`docs/product/metrics.md`](docs/product/metrics.md) — North Star, funnel AARRR, anti-métriques
- [`docs/product/making-of.md`](docs/product/making-of.md) — comment ce produit a été construit (PM × IA)
- [`docs/technical/stack.md`](docs/technical/stack.md) — décisions techniques
- [`docs/technical/schema.md`](docs/technical/schema.md) — schéma de données (ER + entités)

## Stack technique

| Couche | Choix |
|---|---|
| Backend | Python 3.12 + Django 5.x |
| Base de données | PostgreSQL 16 |
| Frontend | Django Templates + HTMX + Alpine.js + Tailwind CSS |
| Graphiques | Chart.js (radar chart Big Five) |
| Auth | django-allauth (email/password) — Keycloak/OIDC en V2 |
| Export PDF | WeasyPrint |
| Déploiement | Docker Compose (app + db + nginx) |
| Documentation | MkDocs Material → GitHub Pages |
| i18n | Django i18n natif (FR/EN) |

## Lancer en local (développement)

**Prérequis :** Docker Desktop installé.

```bash
git clone https://github.com/adams43360/FitRadarHR.git
cd FitRadarHR
cp .env.example .env
make dev-build    # premier lancement (build + migrations)
# puis : make dev  (lancements suivants)
```

L'application est accessible sur **http://localhost:8000**.

| Commande | Action |
|---|---|
| `make dev` | Démarrer l'environnement de dev |
| `make dev-build` | Build + démarrer (premier lancement) |
| `make stop` | Arrêter les conteneurs |
| `make migrate` | Appliquer les migrations |
| `make createsuperuser` | Créer un compte admin |
| `make shell` | Ouvrir un shell Django |
| `make logs` | Afficher les logs |
| `make test` | Lancer les tests |

## Essayer la démo

Avec `DEMO_MODE=True` dans le `.env`, un bouton **« Essayer la démo »** apparaît sur la
page de connexion : accès un clic (sans mot de passe) à une organisation fictive complète —
« Nexatech », éditeur de logiciels d'une centaine de personnes, avec équipes, profils OCEAN,
postes ouverts et rapports de fit.

```bash
make seed-demo   # crée / réinitialise l'org démo
```

Données fictives, déterministes, réinitialisées toutes les 24 h en production
(service `demo-reset`). Aucun email réel ne part de la démo.

## Statut du projet

**V1 complète** — les 8 epics du cadrage sont livrés et couverts par 89 tests.

| # | Epic | Statut |
|---|---|---|
| E1 | Authentification & organisations | ✅ |
| E2 | Gestion des postes (+ départements) | ✅ |
| E3 | Gestion des équipes | ✅ |
| E4 | Questionnaire Big Five (50 & 100 items) | ✅ |
| E5 | Moteur de calcul de Fit | ✅ |
| E6 | Rapports, radar charts, export PDF, analytics | ✅ |
| E7 | Internationalisation FR/EN | ✅ |
| E8 | Conformité & gouvernance (RGPD, audit) | ✅ |

La suite : voir la [roadmap publique V2](https://adams43360.github.io/FitRadarHR/about/roadmap/) priorisée RICE.

## Licence

[MIT](LICENSE) — libre d'utilisation, de modification et de redistribution.
