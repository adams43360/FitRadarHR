# Essayer la démo

FitRadarHR propose un **environnement de démonstration public** : un clic suffit pour explorer
l'outil avec des données réalistes, sans créer de compte.

## Accéder à la démo

Sur la page de connexion ou la page d'accueil, cliquez sur **✨ Essayer la démo**.
Vous êtes immédiatement connecté·e au compte de démonstration, avec le rôle Responsable RH.

!!! info "Aucune inscription requise"
    Le compte démo n'a pas de mot de passe : le bouton est le seul moyen d'y accéder.

## Ce que contient la démo

L'environnement simule **Nexatech**, un éditeur de logiciels fictif d'une centaine de personnes :

- 6 départements (Ingénierie, Produit & Design, Commercial, Customer Success, Finance, RH)
- 10 équipes avec leurs membres et leurs profils OCEAN complétés
- 9 postes ouverts avec profils Big Five cibles et classements de fit
- Des candidats en cours d'évaluation (questionnaires complétés, en attente ou en cours)
- Des rapports de fit poste et équipe consultables et exportables en PDF

Les profils des équipes sont volontairement contrastés (une équipe commerciale extravertie,
une équipe finance très consciencieuse…) pour que les signaux de complémentarité soient parlants.

## Les règles de l'environnement de démonstration

!!! warning "Données fictives, réinitialisées toutes les 24 h"
    Toutes les données sont **fictives et déterministes** : elles sont supprimées et recréées
    à l'identique chaque jour. Ne saisissez aucune donnée réelle dans la démo.

Par ailleurs, certaines fonctions sont adaptées :

- **Aucun email n'est envoyé** depuis la démo. Lorsque vous envoyez un questionnaire,
  le lien de passation s'affiche à l'écran — vous pouvez l'ouvrir vous-même pour tester
  le parcours candidat de bout en bout (consentement RGPD inclus).
- **L'effacement RGPD est désactivé** (les données étant fictives et partagées entre
  tous les visiteurs).

## Vous voulez aller plus loin ?

Créez votre propre compte gratuit ([voir Créer un compte](signup.md)) ou
[contactez-nous](mailto:contact@fitradarhr.com) pour un environnement de test dédié à votre équipe.

---

## Pour les administrateurs (auto-hébergement)

Le mode démo se configure via l'environnement :

```bash
# .env
DEMO_MODE=True
```

```bash
# Créer ou réinitialiser l'org démo
python manage.py seed_demo

# En dev (Docker)
make seed-demo
```

En production, le service `demo-reset` du `docker-compose.yml` rejoue le seed toutes les 24 h :

```bash
docker compose -f docker/docker-compose.yml --profile demo up -d
```
