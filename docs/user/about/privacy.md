# Confidentialité et RGPD

FitRadarHR a été conçu avec la conformité RGPD comme contrainte de conception, pas comme une couche ajoutée après coup.

## Données collectées

| Donnée | Qui | Durée | Base légale |
|---|---|---|---|
| Email, prénom, nom (utilisateurs) | Utilisateurs du compte | Durée du compte | Contrat |
| Email, prénom, nom (personnes évaluées) | Candidats / collaborateurs | Durée de l'organisation | Intérêt légitime + consentement |
| Réponses au questionnaire (brutes) | Personnes évaluées | Supprimées après calcul | Consentement |
| Scores Big Five | Personnes évaluées | Durée de l'organisation | Consentement |
| Rapports de fit | Personnes évaluées | Durée de l'organisation | Intérêt légitime |

## Consentement explicite

Avant de répondre au questionnaire, chaque personne lit et accepte explicitement une notice d'information. Ce consentement est :
- Enregistré avec horodatage et version du texte affiché
- Immuable (non modifiable a posteriori)
- Révocable (la personne peut demander l'effacement de ses données)

## Droit à l'effacement

À la demande d'une personne évaluée, ses données personnelles (prénom, nom, email) sont **anonymisées** (`[supprimé]`). Les rapports de fit associés sont conservés sans lien nominatif pour la traçabilité organisationnelle.

## Journal d'audit

Toutes les actions sensibles (consultation d'un rapport, export PDF, envoi de lien, effacement) sont enregistrées dans un journal immuable — conformément aux exigences de l'EU AI Act pour les systèmes à haut risque.

## Hébergement

FitRadarHR est auto-hébergé. Vous contrôlez l'emplacement de vos données. Aucune donnée n'est transmise à des tiers.

!!! info "Auto-hébergement"
    En déployant FitRadarHR sur votre propre VPS, vous êtes responsable du traitement des données personnelles (rôle de responsable de traitement). Pensez à mettre à jour votre registre des traitements.
