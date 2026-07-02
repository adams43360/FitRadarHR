# Rapport Fit Équipe

Le Fit Équipe compare le profil Big Five d'une personne à la **composition actuelle d'une équipe**.

## Générer un rapport

**Prérequis :**
- La personne a complété son questionnaire Big Five
- L'équipe a au moins un membre avec un profil Big Five complété

**Étapes :**
1. Depuis la fiche de la personne ou de l'équipe, cliquez sur **Générer un rapport de fit**
2. Sélectionnez l'équipe à comparer
3. Le rapport est généré instantanément

<!-- screenshot: docs/user/assets/report-team-fit.png -->
!!! note "Capture d'écran à venir"

## Comment est calculé le Fit Équipe ?

FitRadarHR calcule le **profil moyen de l'équipe** (moyenne des scores par dimension pour tous les membres actifs), puis compare le profil de la personne à ce profil moyen.

!!! info "Complémentarité vs similarité"
    La proximité au profil moyen n'est pas toujours ce qu'on recherche. Une équipe très homogène peut bénéficier d'un profil différent. Le rapport présente les données — l'interprétation en termes de complémentarité reste humaine.

## Lire le rapport

Le radar chart superpose :
- **Bleu** — profil de la personne
- **Ambre** — profil moyen de l'équipe

Les scores de proximité indiquent la distance par dimension entre la personne et la moyenne de l'équipe.

### Les signaux de complémentarité

Pour chaque dimension, le rapport affiche un signal :
- 🌟 **Complémentaire** — la personne apporte de la diversité là où l'équipe est homogène
- ↔ **Différent** — écart notable mais équipe déjà hétérogène
- ≈ **Similaire** — aligné avec le profil de l'équipe

### Les infobulles OCEAN

Passez la souris sur le libellé d'une dimension pour afficher une courte explication de ce que signifie un score élevé ou faible. Utile pour interpréter les résultats sans expertise psychométrique.

### Points à approfondir

Si certaines dimensions affichent un signal **Différent** ou **Complémentaire**, une section dédiée apparaît en bas du rapport. Pour chaque dimension concernée, FitRadarHR propose une piste à aborder lors de l'intégration ou en entretien.

- Les points **Complémentaires** (🌟 fond vert) décrivent comment l'écart peut être un atout
- Les points **Différents** (↔ fond ambre) suggèrent des questions à anticiper sur la dynamique d'équipe

!!! warning "Ce ne sont pas des verdicts"
    Ces observations sont des pistes d'exploration, pas des prédictions. Une différence sur une dimension n'est pas un problème — c'est parfois exactement ce dont l'équipe a besoin.
