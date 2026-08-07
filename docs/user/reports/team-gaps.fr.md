# Cartographie des manques d'équipe

Contrairement aux rapports de Fit, la cartographie des manques ne compare **aucune personne** à l'équipe. Elle regarde l'équipe seule, pour repérer les dimensions OCEAN où les profils actifs sont peu diversifiés.

## Générer la cartographie

**Prérequis :** au moins 2 membres actifs de l'équipe ont complété leur questionnaire Big Five (un écart-type suppose au moins 2 points de mesure).

**Étapes :**
1. Depuis la fiche de l'équipe, cliquez sur **Cartographie des manques**
2. La cartographie est calculée instantanément à partir des profils actifs

<!-- screenshot: docs/user/assets/report-team-gaps.png -->
!!! note "Capture d'écran à venir"

## Comment est-ce calculé ?

FitRadarHR calcule le **profil moyen de l'équipe** ainsi que l'**écart-type** par dimension (le même calcul qui alimente le rapport [Fit Équipe](team-fit.md)). Une dimension avec un écart-type bas signifie que les membres actifs se ressemblent sur ce trait — l'équipe est **homogène**.

Aucune nouvelle donnée n'est collectée : la cartographie réutilise les profils déjà passés par les membres de l'équipe.

## Lire le rapport

Les 5 dimensions OCEAN sont toujours affichées, avec un signal :

- **◎ Homogène** — les profils actifs sont proches sur cette dimension
- **◇ Hétérogène** — les profils actifs sont déjà diversifiés sur cette dimension

### Pistes à explorer pour un prochain recrutement

Pour chaque dimension homogène, une section dédiée propose une piste de réflexion pour un recrutement ou un plan de développement d'équipe à venir.

!!! warning "Ce ne sont pas des recommandations"
    Une dimension homogène n'est pas un problème en soi — c'est une observation. FitRadarHR ne calcule jamais de profil "manquant" à recruter ; l'interprétation et la décision restent humaines.

## Export

Comme les autres rapports, la cartographie peut être [exportée en PDF](export.md).
