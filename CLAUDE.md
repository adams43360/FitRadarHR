# CLAUDE.md — Contexte projet pour Claude Code

> Ce fichier est lu automatiquement par Claude Code à chaque session dans ce dépôt.
> Il donne le contexte produit et les règles à respecter sans avoir à les répéter.

## Le projet

**FitRadarHR** — un outil bilingue (FR/EN), gratuit et open source (MIT), qui aide les RH et
managers à évaluer la compatibilité d'une personne (candidat ou collaborateur en mobilité
interne) avec un poste et/ou une équipe, en s'appuyant sur le modèle de personnalité
**Big Five / OCEAN** (questionnaire IPIP, domaine public).

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
| E7 | Internationalisation | ✅ FR/EN — 300+ strings traduites |
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

## Conventions de travail

- **Stack** : Django 5 + HTMX + Alpine.js + Tailwind CSS + PostgreSQL 16 + Docker Compose
- **Auth V1** : django-allauth (email/password) — Keycloak/OIDC reporté en V2
- **Commits** : Conventional Commits — `feat:`, `fix:`, `docs:`, `refactor:`, `test:`
- **User stories** : format `En tant que [rôle], je veux [besoin], afin de [valeur]`
  avec critères d'acceptation explicites, rédigées en français
- **Code et variables** : en anglais
- **i18n** : toute string UI via `gettext_lazy(_(...))`, jamais de texte en dur
- **Multi-tenant** : chaque modèle lié à une org filtre systématiquement par `org_id`
  via un Django model manager (`OrgQuerySet`) — aucune vue ne peut afficher des données cross-tenant
- **Doc utilisateur** : mise à jour dans `docs/user/` à chaque évolution de feature —
  le workflow GitHub Actions publie automatiquement sur GitHub Pages à chaque push sur `main`
