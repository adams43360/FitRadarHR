# Métriques produit — FitRadarHR

> Ce document définit les métriques qui pilotent le produit. La page **Analytics**
> de l'application (`/reports/analytics/`, rôle RH) implémente les métriques
> org-scoped ; les métriques produit globales (multi-orgs) relèvent de
> l'instrumentation de la plateforme (V2).
>
> Implémentation : `apps/reports/analytics.py`.

## 1. North Star Metric

**Nombre de rapports de fit consultés par semaine** (`report.viewed` dans l'audit log).

C'est le moment où le produit délivre sa valeur : un humain lit une restitution
pour éclairer une décision. Ce n'est ni le nombre de questionnaires envoyés
(activité, pas valeur), ni le nombre de profils créés (stock, pas usage) :
un profil jamais consulté n'a créé aucune valeur.

Cette North Star est cohérente avec le principe *human in the loop* du cadrage :
on mesure la consultation par un humain, jamais un taux de "bonnes décisions"
qui supposerait que l'outil décide.

## 2. Funnel d'usage (AARRR adapté B2B)

| Étape | Métrique | Événement mesuré |
|---|---|---|
| **Acquisition** | Orgs créées / visiteurs de la démo | inscription, `demo_login` |
| **Activation** | Org ayant envoyé ≥ 1 questionnaire ET consulté ≥ 1 rapport | premier `report.viewed` |
| **Rétention** | Orgs actives par semaine (≥ 1 rapport consulté) | `report.viewed` hebdo |
| **Referral** | (V2) invitations de managers par les RH | création d'utilisateur invité |
| **Revenue** | N/A — produit gratuit open source | — |

Le maillon critique est **l'activation** : une org qui envoie des questionnaires
mais ne consulte pas les rapports n'a pas compris la proposition de valeur.

## 3. Métriques de la page Analytics (org-scoped)

### Funnel questionnaire

```
envoyé ──→ commencé ──→ complété
        (consentement)   (profil OCEAN)
```

| Métrique | Définition | Levier si dégradée |
|---|---|---|
| **Taux de démarrage** | liens avec consentement RGPD / liens envoyés | reformuler l'email d'invitation, réduire le délai d'envoi |
| **Taux de complétion** | liens complétés / liens envoyés | questionnaire 50 items par défaut, relances |
| **Abandons** | commencés mais jamais terminés | UX de passation (blocs, reprise de session) |
| **Délai moyen de passation** | moyenne(complété_le − envoyé_le) | relances automatiques (V2) |

Chaque **lien envoyé** compte pour une entrée (pas de déduplication par personne) :
un renvoi de lien est un nouvel essai de conversion.

### Adoption & couverture

| Métrique | Définition |
|---|---|
| **Couverture des profils** | personnes avec profil OCEAN / personnes créées |
| **Profils par mois** | profils complétés, 6 derniers mois (tendance d'adoption) |
| **Répartition** | candidats vs collaborateurs (usage recrutement vs mobilité interne) |

### Engagement restitution (fenêtre 30 j)

| Métrique | Définition |
|---|---|
| **Rapports consultés** | événements `report.viewed` (source : audit log E8) |
| **Exports PDF** | événements `pdf.exported` |

L'audit log EU AI Act sert ici une double fonction : traçabilité réglementaire
**et** source des métriques d'engagement — aucune instrumentation supplémentaire,
aucune donnée nouvelle collectée (privacy by design).

### Cohortes de rétention

Sur la page Analytics, chaque **cohorte** regroupe les personnes activées le
même mois (mois de leur première passation *complétée*). Pour chaque mois
suivant (M0, M1, M2…), on affiche la part de la cohorte dont le rapport de
profil a été consulté au moins une fois (`profile.viewed`) — même source
d'audit log que l'engagement 30 j, aucune donnée supplémentaire collectée.

Une re-passation ultérieure (voir [suivi longitudinal](../user/survey/track.md))
ne recrée jamais une cohorte : l'activation reste datée de la toute première
passation complétée de la personne.

Granularité **mensuelle** (et non hebdomadaire comme envisagé initialement en V2,
cf. section 5) : à l'échelle d'une seule org (quelques dizaines de personnes par
mois), une cohorte hebdomadaire serait trop clairsemée pour être lisible ; le
mensuel reste cohérent avec le graphique "Profils par mois" déjà présent sur
la page.

### Vivier par poste

**Fit moyen par poste actif** : moyenne des `overall_fit` des personnes évaluées.
C'est un indicateur de **santé du vivier**, pas un classement de personnes.
Les moyennes sont structurellement hautes (pénalité douce du moteur v1.0) :
c'est l'écart **entre postes** et la tendance qui s'interprètent, pas la valeur absolue.

## 4. Anti-métriques — ce qu'on refuse de mesurer

Conformément aux règles non négociables du cadrage :

- **Aucun taux de "recommandation"** : le produit ne recommande pas, il informe.
- **Aucune métrique de performance individuelle** dérivée des profils OCEAN.
- **Aucun benchmark inter-personnes** affiché comme un score de valeur
  (le classement fit d'un poste est un outil d'exploration, pas une note).
- **Aucun tracking tiers** (analytics web externes) sur les pages de passation :
  les répondants ne sont pas des utilisateurs à tracker mais des personnes
  protégées par le RGPD.

## 5. Instrumentation V2 (backlog)

- Événements d'activation org-level agrégés multi-tenant (dashboard super-admin)
- Temps médian de passation par bloc de questions (détection des blocs qui font décrocher)
- Taux de conversion démo → inscription
- ~~Cohortes de rétention hebdomadaires par org~~ — livré en version **mensuelle**
  et org-scoped (voir section 3 ci-dessus)
