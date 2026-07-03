# Changelog

Toutes les évolutions notables de FitRadarHR sont documentées ici.
Format inspiré de [Keep a Changelog](https://keepachangelog.com/fr/1.1.0/) —
le projet n'étant pas encore versionné, les entrées sont datées.

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
