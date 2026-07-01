# Schéma de données — FitRadarHR

> Décisions de conception alignées sur : multi-tenant `org_id` (row-level), RGPD, EU AI Act, bilingue FR/EN.
> Statut : Draft v1 — 2026-06-30

---

## Diagramme entité-relation

```mermaid
erDiagram

    Organization ||--o{ User : "a"
    Organization ||--o{ Position : "a"
    Organization ||--o{ Team : "a"
    Organization ||--o{ Person : "a"
    Organization ||--o{ AuditLog : "génère"

    User ||--o{ Team : "manage"
    User ||--o{ QuestionnaireLink : "envoie"
    User ||--o{ FitReport : "consulte"

    Position ||--|| PositionProfile : "a un profil cible"
    Position ||--o{ FitReport : "évaluée dans"

    Team ||--o{ TeamMembership : "composée de"
    Person ||--o{ TeamMembership : "appartient à"

    Person ||--o{ QuestionnaireLink : "reçoit"
    Person ||--|| BigFiveProfile : "a un profil"

    QuestionnaireLink ||--|| ConsentRecord : "génère"
    QuestionnaireLink ||--o| QuestionnaireSession : "a une session"
    QuestionnaireLink ||--|| BigFiveProfile : "produit"

    BigFiveProfile ||--o{ FitReport : "utilisé dans"

    Team ||--o{ FitReport : "évaluée dans"
```

---

## Entités

### `Organization`
Représente un tenant — organisation B2B ou espace personnel B2C.

| Champ | Type | Notes |
|---|---|---|
| `id` | UUID | Clé primaire |
| `name` | VARCHAR(255) | Nom de l'org ou "Espace de [prénom]" pour B2C |
| `account_type` | ENUM(`B2B`, `B2C`) | Détermine le parcours d'inscription |
| `questionnaire_version` | ENUM(`50`, `100`) | Version IPIP choisie par l'org (défaut : 50) |
| `language_default` | ENUM(`fr`, `en`) | Langue par défaut de l'org |
| `is_active` | BOOLEAN | Permet de désactiver un compte sans supprimer |
| `created_at` | TIMESTAMP | — |

---

### `User`
Utilisateur ayant un compte FitRadarHR (RH, Manager, ou Solo B2C).

| Champ | Type | Notes |
|---|---|---|
| `id` | UUID | — |
| `org_id` | UUID FK → Organization | Isolation tenant |
| `email` | VARCHAR(255) | Unique global |
| `first_name` | VARCHAR(100) | — |
| `last_name` | VARCHAR(100) | — |
| `role` | ENUM(`RH`, `MANAGER`, `SOLO`) | SOLO = B2C, cumule les droits RH+Manager |
| `language` | ENUM(`fr`, `en`) | Préférence individuelle |
| `is_active` | BOOLEAN | Désactivation sans suppression |
| `invited_by` | UUID FK → User (nullable) | Trace l'invitation |
| `created_at` | TIMESTAMP | — |
| `last_login_at` | TIMESTAMP | — |

> **Note :** le mot de passe est géré par django-allauth, pas stocké en clair. En V2, ce champ est remplacé par un `external_oidc_id` (Keycloak).

---

### `Position`
Poste créé par un RH ou un utilisateur Solo, avec un profil Big Five cible.

| Champ | Type | Notes |
|---|---|---|
| `id` | UUID | — |
| `org_id` | UUID FK → Organization | Isolation tenant |
| `title_fr` | VARCHAR(255) | Titre en français |
| `title_en` | VARCHAR(255) | Titre en anglais |
| `description_fr` | TEXT (nullable) | — |
| `description_en` | TEXT (nullable) | — |
| `department` | VARCHAR(100) (nullable) | — |
| `status` | ENUM(`active`, `archived`) | — |
| `created_by` | UUID FK → User | — |
| `created_at` | TIMESTAMP | — |
| `updated_at` | TIMESTAMP | — |

---

### `PositionProfile`
Profil Big Five cible associé à un poste (définition manuelle par le RH).
Relation 1-1 avec `Position`.

| Champ | Type | Notes |
|---|---|---|
| `id` | UUID | — |
| `position_id` | UUID FK → Position | — |
| `openness_min` | SMALLINT (0–100) | Fourchette cible par dimension |
| `openness_max` | SMALLINT (0–100) | — |
| `conscientiousness_min` | SMALLINT (0–100) | — |
| `conscientiousness_max` | SMALLINT (0–100) | — |
| `extraversion_min` | SMALLINT (0–100) | — |
| `extraversion_max` | SMALLINT (0–100) | — |
| `agreeableness_min` | SMALLINT (0–100) | — |
| `agreeableness_max` | SMALLINT (0–100) | — |
| `neuroticism_min` | SMALLINT (0–100) | — |
| `neuroticism_max` | SMALLINT (0–100) | — |
| `updated_at` | TIMESTAMP | — |

> **Design :** fourchette min/max plutôt qu'une valeur unique — permet d'exprimer "Agréabilité entre 60 et 80" sans sur-contraindre.

---

### `Team`
Équipe gérée par un Manager ou un utilisateur Solo.

| Champ | Type | Notes |
|---|---|---|
| `id` | UUID | — |
| `org_id` | UUID FK → Organization | Isolation tenant |
| `name` | VARCHAR(255) | — |
| `description` | TEXT (nullable) | — |
| `manager_id` | UUID FK → User | Manager responsable |
| `created_at` | TIMESTAMP | — |

---

### `TeamMembership`
Table de liaison Person ↔ Team. Conserve l'historique des appartenances.

| Champ | Type | Notes |
|---|---|---|
| `id` | UUID | — |
| `team_id` | UUID FK → Team | — |
| `person_id` | UUID FK → Person | — |
| `added_by` | UUID FK → User | Traçabilité |
| `joined_at` | TIMESTAMP | — |
| `left_at` | TIMESTAMP (nullable) | NULL = membre actuel |

---

### `Person`
Candidat externe ou collaborateur interne ayant reçu (ou pouvant recevoir) un questionnaire.
N'a pas nécessairement de compte `User`.

| Champ | Type | Notes |
|---|---|---|
| `id` | UUID | — |
| `org_id` | UUID FK → Organization | Isolation tenant |
| `email` | VARCHAR(255) | — |
| `first_name` | VARCHAR(100) | — |
| `last_name` | VARCHAR(100) | — |
| `person_type` | ENUM(`candidate`, `collaborator`) | — |
| `created_by` | UUID FK → User | Qui a créé la fiche |
| `created_at` | TIMESTAMP | — |

> **RGPD :** à la demande d'effacement, les champs `email`, `first_name`, `last_name` sont anonymisés (`[supprimé]`). L'enregistrement est conservé pour la traçabilité des rapports.

---

### `QuestionnaireLink`
Lien tokenisé envoyé à une `Person` pour accéder au questionnaire.

| Champ | Type | Notes |
|---|---|---|
| `id` | UUID | — |
| `org_id` | UUID FK → Organization | Isolation tenant |
| `person_id` | UUID FK → Person | — |
| `token` | VARCHAR(128) | Unique, signé via Django `TimestampSigner` |
| `questionnaire_version` | ENUM(`50`, `100`) | Hérite du paramètre org au moment de la création |
| `language` | ENUM(`fr`, `en`) | Langue choisie à l'envoi (modifiable par la personne) |
| `sent_by` | UUID FK → User | — |
| `sent_at` | TIMESTAMP | — |
| `expires_at` | TIMESTAMP | Défaut : +30 jours |
| `status` | ENUM(`pending`, `in_progress`, `completed`, `expired`) | — |
| `completed_at` | TIMESTAMP (nullable) | — |

---

### `ConsentRecord`
Consentement RGPD explicite recueilli avant la passation du questionnaire.

| Champ | Type | Notes |
|---|---|---|
| `id` | UUID | — |
| `link_id` | UUID FK → QuestionnaireLink | — |
| `consented_at` | TIMESTAMP | — |
| `consent_version` | VARCHAR(20) | Version du texte de consentement affiché (ex. `v1.0`) |
| `ip_address` | INET (nullable) | Preuve technique — à anonymiser après délai légal |
| `language` | ENUM(`fr`, `en`) | Langue dans laquelle le consentement a été lu |

> **RGPD :** enregistrement immuable (pas de UPDATE/DELETE par les utilisateurs).

---

### `QuestionnaireSession`
Sauvegarde de la progression en cours de passation (reprise possible).

| Champ | Type | Notes |
|---|---|---|
| `id` | UUID | — |
| `link_id` | UUID FK → QuestionnaireLink | — |
| `answers` | JSONB | `{"item_id": score, ...}` — réponses partielles |
| `current_item_index` | SMALLINT | Position dans le questionnaire |
| `started_at` | TIMESTAMP | — |
| `last_saved_at` | TIMESTAMP | Mise à jour à chaque sauvegarde auto |

> Supprimée après complétion du questionnaire (les réponses finales sont dans `BigFiveProfile`).

---

### `BigFiveProfile`
Résultat calculé du questionnaire Big Five d'une `Person`.

| Champ | Type | Notes |
|---|---|---|
| `id` | UUID | — |
| `person_id` | UUID FK → Person | — |
| `link_id` | UUID FK → QuestionnaireLink | Source du calcul |
| `openness` | DECIMAL(5,2) | Score 0–100 |
| `conscientiousness` | DECIMAL(5,2) | — |
| `extraversion` | DECIMAL(5,2) | — |
| `agreeableness` | DECIMAL(5,2) | — |
| `neuroticism` | DECIMAL(5,2) | — |
| `questionnaire_version` | ENUM(`50`, `100`) | Version utilisée |
| `algorithm_version` | VARCHAR(20) | Ex. `v1.0` — traçabilité EU AI Act |
| `computed_at` | TIMESTAMP | — |

---

### `FitReport`
Résultat d'un calcul de fit (Poste ou Équipe), généré et consulté par un RH ou Manager.

| Champ | Type | Notes |
|---|---|---|
| `id` | UUID | — |
| `org_id` | UUID FK → Organization | Isolation tenant |
| `profile_id` | UUID FK → BigFiveProfile | Profil évalué |
| `report_type` | ENUM(`JOB`, `TEAM`) | — |
| `position_id` | UUID FK → Position (nullable) | Renseigné si `JOB` |
| `team_id` | UUID FK → Team (nullable) | Renseigné si `TEAM` |
| `fit_openness` | DECIMAL(5,2) | Score de proximité par dimension |
| `fit_conscientiousness` | DECIMAL(5,2) | — |
| `fit_extraversion` | DECIMAL(5,2) | — |
| `fit_agreeableness` | DECIMAL(5,2) | — |
| `fit_neuroticism` | DECIMAL(5,2) | — |
| `algorithm_version` | VARCHAR(20) | Traçabilité EU AI Act |
| `created_by` | UUID FK → User | — |
| `created_at` | TIMESTAMP | — |

> **Principe :** pas de score global unique — les scores par dimension alimentent la restitution visuelle et textuelle, jamais une décision binaire.

---

### `AuditLog`
Journal immuable de toutes les actions sensibles (EU AI Act + RGPD).

| Champ | Type | Notes |
|---|---|---|
| `id` | UUID | — |
| `org_id` | UUID FK → Organization | — |
| `user_id` | UUID FK → User (nullable) | NULL si action système |
| `action` | VARCHAR(100) | Ex. `report.viewed`, `link.sent`, `pdf.exported`, `person.deleted` |
| `entity_type` | VARCHAR(50) | Ex. `FitReport`, `Person`, `QuestionnaireLink` |
| `entity_id` | UUID | — |
| `metadata` | JSONB (nullable) | Contexte additionnel (ex. version algo) |
| `created_at` | TIMESTAMP | — |

> Aucun UPDATE ou DELETE autorisé sur cette table, même pour un ADMIN.

---

## Règles transverses

1. **Isolation tenant** : chaque requête filtre systématiquement par `org_id` via un Django model manager (`OrgQuerySet`). Aucune vue ne peut afficher des données cross-tenant.
2. **Pas de score de décision unique** : `FitReport` stocke 5 scores dimensionnels, jamais un agrégat binaire.
3. **Traçabilité** : toute consultation de rapport, export PDF et envoi de lien est inscrit dans `AuditLog`.
4. **RGPD / droit à l'effacement** : anonymisation des champs PII de `Person` (nom, email) sur demande — les `FitReport` et `AuditLog` associés sont conservés sans lien nominatif.
5. **UUID partout** : pas d'auto-increment entier exposé en URL (évite l'énumération).

---

*Dernière mise à jour : 2026-06-30*
