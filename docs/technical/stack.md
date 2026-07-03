# Stack Technique — FitRadarHR

> Document de référence des décisions techniques. À mettre à jour si un choix est révisé.
> Statut : validé en session — 2026-06-30

---

## Principes directeurs

- **Solo dev, VPS self-hosted** → pas de sur-ingénierie, stack lisible et maintenable seul
- **Pas d'usine à gaz** → chaque brique a un rôle précis, rien de spéculatif
- **Progressive** → les décisions V1 anticipent les évolutions sans les forcer

---

## Stack V1

### Backend

| Brique | Choix | Notes |
|---|---|---|
| Langage | **Python 3.12+** | — |
| Framework | **Django 5.x** | Batteries incluses, i18n native, ORM, admin |
| Serveur WSGI | **Gunicorn** | Derrière Nginx en prod |
| ORM | **Django ORM** | Migrations avec `makemigrations` / `migrate` |
| Base de données | **PostgreSQL 16** | Multi-tenant, RGPD, robustesse |

### Frontend

| Brique | Choix | Notes |
|---|---|---|
| Templates | **Django Templates** | Server-rendered, pas de SPA |
| Interactivité | **HTMX** | Dynamisme sans framework JS lourd |
| Micro-interactions | **Alpine.js** | Dropdowns, modals, états locaux (~15 kb) |
| CSS / Design | **Tailwind CSS** | Opinioné, rapide, utility-first |
| Radar charts | **Chart.js** (vanilla) | Intégré via `<script>`, pas de bundler requis |

### Fonctionnalités transverses

| Brique | Choix | Notes |
|---|---|---|
| Authentification V1 | **django-allauth** | Email + mot de passe, invitations par lien |
| i18n | **Django i18n natif** | FR/EN/ES/DE, fichiers `.po` / `.mo` — questionnaire IPIP sourcé sur traductions officielles quand elles existent (voir `docs/product/translations-ipip.md`) |
| Emails | **Django Email** + SMTP | Sendgrid ou SMTP self-hosted (ex. Postfix/Mailcow) |
| Export PDF | **WeasyPrint** | HTML → PDF côté serveur, léger sur VPS |
| Liens tokenisés | **Django signing** (`TimestampSigner`) | Liens questionnaire sécurisés, expiration configurable |
| Tâches async | **pas de Celery en V1** | Si besoin : intégrer plus tard (notifications différées) |

### Déploiement

| Brique | Choix | Notes |
|---|---|---|
| Conteneurisation | **Docker Compose** | 3 services : `app`, `db`, `nginx` |
| Reverse proxy | **Nginx** | SSL via Let's Encrypt (Certbot) |
| Hébergement | **VPS** (Hetzner / OVH) | Ubuntu 22.04 LTS recommandé |

#### Structure Docker Compose (V1)

```
services:
  app:    Django + Gunicorn
  db:     PostgreSQL 16
  nginx:  Reverse proxy + SSL
```

Commandes courantes :
```bash
docker compose up -d          # démarrer
docker compose pull && docker compose up -d  # mettre à jour
docker compose exec app python manage.py migrate  # migrations
```

---

## Structure du dépôt (cible)

```
/fitradarhr
  /core              → settings Django, URLs racine, config OIDC (future)
  /apps
    /accounts        → utilisateurs, tenants B2B/B2C, rôles
    /positions       → gestion des postes (E2)
    /teams           → gestion des équipes (E3)
    /survey          → questionnaire Big Five, liens tokenisés (E4)
    /fit             → moteur de calcul Fit Poste / Fit Équipe (E5)
    /reports         → restitution, radar chart, export PDF (E6)
  /templates         → Django templates + HTMX
  /static            → Tailwind CSS (build), Chart.js, Alpine.js
  /locale            → fichiers de traduction FR / EN (.po / .mo)
  /docker
    docker-compose.yml
    nginx.conf
    Dockerfile
  docs/
    product/         → cadrage, user stories
    technical/       → ce fichier, schéma de données (à venir)
```

---

## Décisions reportées à une version future

| Brique | Version future | Motivation |
|---|---|---|
| **Celery + Redis** | Si besoin | Pour les notifications différées ou les calculs lourds. Pas justifié en V1. |
| **Kubernetes** | Si forte charge | K8S = overhead non justifié pour un VPS solo. Évolution naturelle : Docker Compose → Kamal → K8S. |
| **Mode calibré du profil de poste** | V2+ | Nécessite un volume de données historiques. |
| **PWA (Progressive Web App)** | V1.5 | Quelques lignes de config, l'app devient installable sur l'écran d'accueil iOS/Android sans passer par les stores. |
| **Apps natives iOS / Android** | V2+ | V1 = web responsive (Tailwind). Vues spécifiques mobile/tablette et apps natives envisagées en V2 si le produit trouve ses utilisateurs. Une app `/api` (Django REST Framework) sera préparée en V1 pour ne pas avoir à réécrire. |

---

## Décisions techniques tranchées

| Question | Décision |
|---|---|
| **Items IPIP** | 50 ou 100 items au choix — paramètre configurable par organisation (50 items ≈ 10 min, candidats externes ; 100 items = plus précis, mobilité interne). Les deux algorithmes de scoring sont implémentés. |
| **SMTP V1** | Gmail SMTP avec App Password Google. Limite : 500 emails/jour (gratuit) ou 2 000 (Workspace). Migration vers Resend/Sendgrid possible en changeant uniquement la config. |
| **Multi-tenant** | **Option A — `tenant_id` (row-level).** Toutes les orgs partagent les mêmes tables, chaque ligne porte un `org_id`. Filtrage automatique via Django model managers. Simple, solide, standard pour une V1 SaaS. |
| **SSO Keycloak / OIDC (V2)** | **Un IdP par organisation**, via `allauth.socialaccount` + provider générique `openid_connect`. Chaque `OrgSSOConfig` synchronise un `SocialApp` dédié (`provider_id=login_slug`) — pas de configuration statique dans `settings.py`, tout est piloté par la base pour rester cohérent avec le multi-tenant existant. Le SSO s'ajoute à l'email/mot de passe, il ne le remplace jamais (pas de verrouillage si l'IdP tombe). |
| **API publique en lecture seule (V2)** | App dédiée `apps.api`, montée hors `i18n_patterns` sous `/api/v1/` (un client machine n'a pas de préférence de langue navigateur). Authentification par **clé API par organisation** (`Authorization: Api-Key <clé>`, schéma volontairement distinct de `Bearer`/OAuth2 — pas de flux OAuth2, juste une clé opaque scopée à un tenant), hashée en SHA-256 (`ApiKey.key_hash`), jamais stockée en clair. Pas de dépendance à Django REST Framework : vues fonction + `JsonResponse` + pagination maison via `django.core.paginator.Paginator`, cohérent avec le reste du projet qui reste volontairement peu dépendant. Endpoints strictement GET : postes/équipes (métadonnées), personnes + statut questionnaire, résultats de fit — **jamais** les scores Big Five bruts (choix produit RGPD de minimisation des données transmises à des tiers). |
| **Facturation Stripe (V3)** | **Un seul plan payant**, essai gratuit de 14 jours à la création de l'org (`apps.billing.Subscription`, 1:1 avec `Organization`). Le prix est configuré côté Stripe Dashboard (`STRIPE_PRICE_ID` référence un Price Stripe), jamais en dur dans le code. Stripe Checkout pour la souscription, Stripe Customer Portal pour la gestion (résiliation, moyen de paiement) — FitRadarHR ne ré-implémente aucun flux de paiement lui-même. Le statut (`trialing`/`active`/`past_due`/`canceled`) est synchronisé exclusivement via un **webhook signé** (`/billing/webhook/`, hors `i18n_patterns`), jamais interrogé en direct auprès de Stripe à chaque page vue. Passé l'essai sans abonnement actif, des **quotas d'usage** s'appliquent (postes actifs, personnes, questionnaires/mois — `apps/billing/quotas.py`) : jamais de blocage total, uniquement la création de nouvelles ressources. L'org de démonstration (`is_demo`) est toujours exemptée. |

---

*Dernière mise à jour : 2026-07-03*
