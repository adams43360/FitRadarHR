# Making-of — un produit construit par un PM avec l'IA

> Ce document explique **comment** FitRadarHR a été construit : par un Product Manager
> non-développeur, avec une IA (Claude) comme binôme d'exécution. Il ne raconte pas une
> prouesse technique — il documente une **méthode de travail** reproductible.

## Le point de départ

L'hypothèse testée : *un PM peut-il livrer seul un produit complet — pas un prototype —
en appliquant à l'IA les mêmes pratiques qu'à une équipe de développement ?*

Le sujet choisi n'est pas anodin : un outil RH manipulant des données de personnalité,
c'est un terrain miné (RGPD, EU AI Act, éthique du scoring). Précisément le genre de
produit où le **cadrage** compte plus que le code.

## La méthode, dans l'ordre

### 1. Le cadrage d'abord, le code jamais avant

Avant la première ligne de code : vision, personas, périmètre V1/V2, règles non
négociables, epics E1–E8, user stories au format
`En tant que… je veux… afin de…` avec critères d'acceptation, schéma de données,
choix de stack argumentés. Tout est dans `docs/product/` et `docs/technical/` —
exactement ce qu'on exigerait d'un PM en entreprise.

L'IA a servi de sparring partner sur ce cadrage (challenger le périmètre, dérisquer
les sujets réglementaires), mais **chaque décision est humaine et tracée**.

### 2. CLAUDE.md — le contrat produit lu par la machine

Le fichier `CLAUDE.md` à la racine du dépôt est lu automatiquement par l'IA à chaque
session. Il y trouve le contexte produit, les conventions… et surtout les
**règles non négociables** :

1. Jamais d'analyse de CV pour déduire un profil psychologique
2. Jamais de score de décision automatique — *human in the loop* partout
3. Jamais de typologie non validée scientifiquement (MBTI…)
4. RGPD + EU AI Act by design
5. Bilingue FR/EN dès la conception

C'est le transfert d'une pratique PM classique : plutôt que de répéter les contraintes
à chaque ticket, on les **encode dans l'environnement de travail**. L'IA ne peut pas
"oublier" une règle produit : elle la relit à chaque session. Quand une demande
d'évolution frôle une règle (ex. « ajoute un badge recommandé/non recommandé »),
l'IA la refuse en citant le cadrage — le garde-fou fonctionne dans les deux sens.

### 3. Une boucle de delivery disciplinée

Chaque fonctionnalité suit le même cycle :

```
user story (critères d'acceptation)
   → implémentation par l'IA
   → tests (dont un test d'isolation multi-tenant obligatoire par vue)
   → traductions FR/EN
   → documentation utilisateur
   → commit conventionnel (feat:, fix:, docs:…)
```

Rien d'original — c'est une définition of done. La nouveauté est qu'elle est
**appliquée par l'IA et vérifiée par le PM**, pas l'inverse. La CI GitHub Actions
rejoue les 89 tests à chaque push : le PM non-développeur a une preuve objective
que rien n'est cassé, sans lire le code.

### 4. Les décisions produit restent des décisions

Quelques arbitrages assumés, avec leur raisonnement :

- **Pas de recommandation automatique.** Le rapport dit « voici le profil, voici les
  écarts, voici des questions à explorer en entretien » — jamais « recrutez / ne
  recrutez pas ». C'est à la fois une conviction éthique et une lecture de l'EU AI
  Act (catégorie haut risque : supervision humaine documentée).
- **Le journal d'audit fait double emploi, volontairement.** Exigé pour la conformité,
  il sert aussi de source aux métriques d'engagement — zéro tracking tiers ajouté.
- **La démo publique a des garde-fous produit, pas seulement techniques** : aucun
  email réel ne peut partir, l'effacement RGPD y est désactivé, les personnes
  fictives ont des emails non routables (`.example`). Penser aux abus fait partie
  du travail de conception.
- **North Star = rapports consultés par semaine** — pas les questionnaires envoyés
  (activité) ni les profils créés (stock). On mesure le moment où un humain lit
  une restitution pour éclairer une décision. Voir `docs/product/metrics.md`.

### 5. Ce que l'IA a réellement apporté (et pas)

**Apporté** : la vitesse d'exécution (8 epics livrés en quelques jours), la constance
sur les conventions (i18n, multi-tenant, tests), la disponibilité pour les tâches
ingrates (traductions, données de démo réalistes, documentation).

**Pas apporté** : la vision, les règles éthiques, la priorisation (la roadmap V2 est
scorée RICE par le PM), les arbitrages de périmètre, le sens du "pourquoi". Une IA
sans cadrage aurait produit un outil de scoring RH — exactement ce que ce produit
refuse d'être.

## La leçon

Le métier de PM ne disparaît pas avec l'IA : il se **concentre**. Moins de temps à
attendre le delivery, plus de temps sur le cadrage, les règles, la mesure et
l'éthique. L'IA exécute d'autant mieux que le travail produit en amont est rigoureux —
c'est peut-être la meilleure nouvelle possible pour ce métier.
