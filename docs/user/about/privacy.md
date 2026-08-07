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

Toutes les actions sensibles (consultation d'un rapport, export PDF, envoi de lien, effacement) sont enregistrées dans un journal immuable — conformément aux exigences de l'EU AI Act pour les systèmes à haut risque (voir [EU AI Act et recrutement](eu-ai-act.md) pour le calendrier et le détail des obligations).

## Mesure d'audience

FitRadarHR utilise [Matomo](https://matomo.org), auto-hébergé sur la même infrastructure, pour connaître le volume d'usage et les fonctionnalités les plus utilisées. Cette mesure est configurée en **exemption de consentement CNIL** : pas de cookie, IP anonymisée, aucune donnée personnelle collectée, aucune donnée transmise à un tiers. Aucun bandeau de consentement n'est donc affiché pour cet usage — à distinguer du consentement explicite requis pour le questionnaire Big Five (voir ci-dessus), qui reste inchangé.

## Hébergement

FitRadarHR est auto-hébergé. Vous contrôlez l'emplacement de vos données. Aucune donnée n'est transmise à des tiers.

!!! info "Auto-hébergement"
    En déployant FitRadarHR sur votre propre VPS, vous êtes responsable du traitement des données personnelles (rôle de responsable de traitement). Pensez à mettre à jour votre registre des traitements.
