# FitRadarHR

> 🚧 Projet en cours de développement — porté en public pour démontrer une démarche produit et technique de bout en bout.

**FitRadarHR** est un outil **gratuit et open source** (MIT), bilingue FR/EN, qui aide les équipes RH et les managers à évaluer la compatibilité d'une personne — candidat à l'embauche ou collaborateur en mobilité interne — avec un poste et/ou une équipe, sur la base du modèle de personnalité scientifiquement validé **Big Five / OCEAN** (questionnaire IPIP, domaine public).

## Principes fondateurs

- **Base scientifique uniquement** — Big Five (OCEAN) + questionnaire IPIP. Jamais de MBTI, jamais de déduction de personnalité à partir de CV ou lettre de motivation.
- **Human in the loop** — le produit informe, il ne décide jamais. Pas de score de recommandation binaire.
- **Conformité by design** — RGPD et EU AI Act (catégorie "haut risque") anticipés dès la conception : consentement explicite, journal d'audit immuable, droit à l'effacement.
- **Bilingue FR/EN dès la conception** — i18n native Django, aucune string en dur.
- **Gratuit et auto-hébergeable** — pas de SaaS fermé, déployable sur votre propre VPS.

## Documentation

- 📖 **[Documentation utilisateur](https://adams43360.github.io/FitRadarHR)** — guide complet sur GitHub Pages
- [`docs/product/00-cadrage.md`](docs/product/00-cadrage.md) — cadrage produit complet
- [`docs/product/user-stories.md`](docs/product/user-stories.md) — user stories E1–E8
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

## Statut d'avancement

- [x] Cadrage produit validé
- [x] User stories E1–E8 rédigées
- [x] Stack technique définie
- [x] Schéma de données complet
- [x] Scaffold Django (modèles, migrations, auth B2B/B2C, dashboard)
- [x] Docker Compose dev opérationnel
- [x] Documentation utilisateur publiée (GitHub Pages)
- [x] Vues Postes — liste, création, détail, modification, archivage, profil Big Five (E2)
- [x] Vues Équipes — liste, création, détail, modification, membres + liste Personnes (E3)
- [x] Questionnaire Big Five — envoi lien, consentement RGPD, passation par blocs, scoring OCEAN, profil sauvegardé (E4)
- [ ] Moteur de calcul Fit (E5)
- [ ] Rapports & radar chart (E6)

## Epics

| # | Epic | Statut |
|---|---|---|
| E1 | Authentification & organisations | ✅ Modèles + inscription B2B/B2C |
| E2 | Gestion des postes | ✅ Liste, création, modification, archivage, profil OCEAN |
| E3 | Gestion des équipes | ✅ Liste, création, modification, membres, liste Personnes |
| E4 | Questionnaire Big Five | ✅ Envoi lien, passation, scoring, profil BigFive |
| E5 | Moteur de calcul de Fit | 🔲 À développer |
| E6 | Rapports & restitution | 🔲 À développer |
| E7 | Internationalisation | 🔄 En continu |
| E8 | Conformité & gouvernance | 🔄 En continu |

## Licence

[MIT](LICENSE) — libre d'utilisation, de modification et de redistribution.
