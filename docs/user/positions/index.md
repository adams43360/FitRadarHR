# Gestion des postes

Un **poste** dans FitRadarHR est une fiche associée à un profil Big Five cible — la "personnalité idéale" définie par le RH pour ce rôle.

## Ce que vous pouvez faire

- [Créer un poste](create.md) avec son titre (FR et EN), son département et son équipe cible
- [Définir le profil cible](profile.md) — fourchette souhaitée pour chacune des 5 dimensions OCEAN
- Consulter le **classement des personnes par Fit** directement sur la fiche poste (filtrable par Candidat / Collaborateur)
- Archiver un poste quand il n'est plus actif
- Générer un [rapport de fit](../reports/job-fit.md) en comparant le profil d'une personne au profil cible du poste

## Lien avec les départements et équipes

Un poste peut être rattaché à un **département** (ex. R&D, Sales) et à une **équipe cible** (ex. Backend Team). Si une équipe est définie, le rapport de profil d'un candidat affiche automatiquement le Fit Équipe correspondant à côté du Fit Poste.

## Concept : le profil cible

Plutôt qu'une valeur unique par dimension, FitRadarHR utilise une **fourchette min/max**. Exemple pour un poste commercial :

| Dimension | Min | Max | Interprétation |
|---|---|---|---|
| Ouverture | 40 | 70 | Créativité modérée, pas nécessairement exploratrice |
| Conscience | 60 | 90 | Rigueur et organisation importantes |
| Extraversion | 65 | 100 | Forte aisance relationnelle souhaitée |
| Agréabilité | 50 | 80 | Coopératif sans être trop conciliant |
| Névrotisme | 0 | 40 | Stabilité émotionnelle importante |

!!! info "Fourchette vs valeur unique"
    La fourchette évite de sur-contraindre le profil. "Agréabilité entre 60 et 80" est plus réaliste qu'une valeur exacte de 70.
