# Rapport Fit Poste

Le Fit Poste compare le profil Big Five d'une personne au **profil cible défini pour un poste**.

## Générer un rapport

**Prérequis :**
- La personne a complété son questionnaire Big Five
- Le poste a un profil cible défini (fourchettes min/max par dimension)

**Étapes :**
1. Depuis la fiche de la personne ou du poste, cliquez sur **Générer un rapport de fit**
2. Sélectionnez le poste à comparer (si vous partez de la personne)
3. Le rapport est généré instantanément

<!-- screenshot: docs/user/assets/report-job-fit.png -->
!!! note "Capture d'écran à venir"

## Lire le rapport

### Le radar chart

Le graphique superpose deux formes :
- **Bleu** — profil de la personne (scores 0–100 par dimension)
- **Vert** — profil cible du poste (midpoint de la fourchette)

Quand le profil bleu est **dans** la fourchette sur une dimension → bonne proximité.
Quand il est **en dehors** → écart à interpréter en contexte.

### Les scores de proximité

Pour chaque dimension, un score de proximité est calculé :
- **100% / ✓** — le score de la personne est dans la fourchette cible
- **< 100%** — le score est hors fourchette, le pourcentage indique la distance relative

### Les infobulles OCEAN

Passez la souris sur le libellé d'une dimension (Ouverture, Conscienciosité…) pour afficher une courte explication de ce que signifie un score élevé ou faible sur cette dimension. Utile pour interpréter les résultats sans expertise psychométrique.

!!! info "Interpréter les écarts"
    Un écart n'est pas rédhibitoire. Un score d'extraversion légèrement inférieur à la cible peut être compensé par d'autres qualités. Le rapport informe — la décision appartient au RH ou Manager.

### Points à approfondir en entretien

Si une ou plusieurs dimensions sont **hors fourchette cible**, une section dédiée apparaît en bas du rapport. Pour chaque dimension concernée, FitRadarHR propose une piste de question à explorer en entretien — formulée de façon neutre et contextualisée.

!!! warning "Ce ne sont pas des verdicts"
    Les "points à approfondir" sont des suggestions de questions, pas des conclusions. Un score hors fourchette n'exclut pas un candidat. C'est un point de départ pour une conversation humaine.
