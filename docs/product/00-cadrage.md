# Cadrage Produit — FitRadarHR

> Document vivant. Mis à jour au fil de l'avancement du projet.
> Statut : Draft v1

---

## 1. Contexte et problème

### 1.1 Constat

Les entreprises prennent deux types de décisions structurantes concernant les personnes :

- **Recrutement** : faire entrer une nouvelle personne dans une équipe existante
- **Mobilité interne** : faire évoluer une personne déjà présente vers un nouveau poste ou une nouvelle équipe

Dans les deux cas, la décision repose aujourd'hui très largement sur :
- l'expérience et les compétences techniques (CV, entretiens techniques)
- le "feeling" du recruteur ou du manager lors des entretiens

Ce qui est rarement évalué de façon structurée : **la compatibilité de fonctionnement** entre la personne et l'équipe, ou entre la personne et les exigences comportementales du poste. Or une grande partie des échecs de recrutement ou de mobilité interne ne vient pas d'un manque de compétence technique, mais d'un désalignement de fonctionnement (rythme de travail, gestion du stress, autonomie, rapport à la structure, mode de communication).

### 1.2 Le problème à résoudre

> Comment aider RH et managers à objectiver — sans remplacer leur jugement — la probabilité qu'une personne s'intègre bien dans une équipe donnée ou corresponde aux exigences comportementales d'un poste donné ?

### 1.3 Ce que ce produit n'est pas

Ce point doit être explicite dès le cadrage, car c'est un sujet sensible :

- **Ce n'est pas** un outil de décision automatisée de recrutement (pas de "score final = recrute / ne recrute pas")
- **Ce n'est pas** un outil d'analyse de CV, lettre de motivation ou tout document libre pour en déduire des traits de personnalité (pratique non validée scientifiquement, assimilable à de la graphologie)
- **Ce n'est pas** basé sur des typologies non scientifiques (MBTI, etc.)
- **C'est** un outil d'aide à la décision, basé sur un questionnaire de personnalité validé scientifiquement (Big Five / OCEAN), avec restitution toujours interprétée par un humain

---

## 2. Utilisateurs cibles

| Persona | Besoin principal | Usage |
|---|---|---|
| **RH / Talent Acquisition** (B2B) | Objectiver le fit candidat ↔ poste lors d'un recrutement | Définit les profils de poste, lance les évaluations, consulte les rapports |
| **Manager** (B2B) | Anticiper l'intégration d'une personne (nouvelle recrue ou mobilité interne) dans son équipe | Consulte le fit candidat ↔ équipe, visualise la dynamique d'équipe existante |
| **Utilisateur solo / indépendant** (B2C) | Utiliser FitRadarHR sans appartenir à une organisation formelle (consultant, manager d'une petite équipe) | Crée son propre espace, gère ses équipes et postes en autonomie |
| **Collaborateur / Candidat** *(hors V1, voir périmètre)* | Comprendre son propre profil et la restitution qui en est faite | Répond au questionnaire, consulte (potentiellement) son propre résultat |

### 2.1 Cas d'usage principaux

1. **Recrutement externe** : un RH définit un profil de poste cible, le candidat répond au questionnaire Big Five, le système calcule un score de fit poste, le RH consulte le rapport avant la décision finale.
2. **Mobilité interne** : un manager souhaite faire évoluer un collaborateur vers une autre équipe. Le système compare le profil du collaborateur au profil agrégé de l'équipe cible, et produit une lecture de complémentarité (pas juste de similarité).
3. **Constitution d'équipe** : un manager visualise la composition Big Five de son équipe actuelle, pour comprendre ses forces, ses angles morts, et ce qui manque.

---

## 3. Proposition de valeur

| Pour | Le produit | Plutôt que |
|---|---|---|
| RH | objective une partie de la décision sur des bases scientifiques | le seul ressenti d'entretien |
| Managers | anticipe les frictions d'intégration | découvrir les problèmes après l'embauche |
| Candidats / collaborateurs | bénéficie d'une évaluation transparente, non discriminante par construction | des tests non scientifiques (MBTI...) ou opaques |

---

## 4. Fondement scientifique : le modèle Big Five (OCEAN)

Le produit s'appuie sur le modèle des **Cinq Grands Facteurs de Personnalité**, le modèle dominant et le plus validé scientifiquement en psychologie de la personnalité, libre de droits (contrairement à Belbin ou au MBTI).

| Dimension | Ce qu'elle mesure | Pôle bas | Pôle haut |
|---|---|---|---|
| **O**penness (Ouverture) | Curiosité intellectuelle, goût pour la nouveauté | Conventionnel, pragmatique | Créatif, curieux, abstrait |
| **C**onscientiousness (Conscienciosité) | Organisation, fiabilité, discipline | Spontané, flexible | Rigoureux, organisé, persévérant |
| **E**xtraversion | Orientation vers l'interaction sociale et l'énergie externe | Réservé, autonome | Sociable, énergique, expressif |
| **A**greeableness (Agréabilité) | Coopération, empathie, gestion du consensus | Direct, compétitif | Coopératif, conciliant, empathique |
| **N**euroticism (Stabilité émotionnelle) | Gestion du stress et des émotions négatives | Sensible, réactif | Calme, stable sous pression |

Chaque dimension est mesurée par un questionnaire validé (type IPIP — *International Personality Item Pool*, domaine public, alternative libre de droits aux questionnaires propriétaires comme le NEO-PI-R).

### 4.1 Place de Watzlawick dans le produit

Les travaux de Paul Watzlawick (École de Palo Alto) ne sont **pas un outil de mesure** — ils n'ont jamais eu vocation à qualifier un profil individuel. Ils gardent en revanche une place légitime comme **grille de lecture qualitative** dans la restitution, pour interpréter comment deux profils Big Five sont susceptibles d'interagir en situation de communication (relation symétrique vs complémentaire, gestion des différends). Cette couche reste explicative et pédagogique, jamais un score.

---

## 5. Calcul du "Fit"

Le produit propose **deux modes de calcul**, configurables selon le cas d'usage :

### 5.1 Fit Poste (Person-Job Fit)

Comparaison entre le profil Big Five de la personne et un **profil de poste cible**, défini de deux façons possibles :

- **Mode manuel** : le RH définit lui-même les niveaux attendus sur chaque dimension (ex. "ce poste de support client nécessite une Agréabilité haute et un Neuroticisme bas")
- **Mode calibré** : le profil cible est calculé automatiquement à partir des profils Big Five des personnes qui occupent déjà ce poste avec succès (nécessite un historique de données suffisant — fonctionnalité à activer une fois la base installée)

### 5.2 Fit Équipe (Person-Team Fit)

Comparaison entre le profil de la personne et le **profil agrégé de l'équipe cible**. Ici, l'enjeu n'est pas la similarité mais la **complémentarité** : une équipe entièrement composée de profils similaires peut être un signal d'alerte (angles morts collectifs) autant qu'un gage de cohésion.

### 5.3 Principe de restitution

Dans les deux cas, le résultat n'est **jamais un score brut unique**. La restitution comprend :
- un visuel de positionnement par dimension (radar chart)
- des points de vigilance et de complémentarité en langage clair
- explicitement : "ceci est une aide à la décision, à interpréter avec le contexte humain"

---

## 6. Contraintes réglementaires (à respecter dès la conception)

Ce point est structurant pour l'architecture et doit être traité dès la V1, pas après coup :

- **RGPD** : données de personnalité = données sensibles dans leur traitement. Nécessite consentement explicite, droit d'accès et de suppression, minimisation des données.
- **EU AI Act** : un système d'évaluation de candidats à l'embauche ou de promotion interne est classé **"haut risque"**. Implications dès la conception : traçabilité des décisions, supervision humaine obligatoire (le système ne décide jamais seul), documentation technique, possibilité de contestation.
- **Non-discrimination** : le Big Five n'a pas vocation à corréler avec des caractéristiques protégées (âge, genre, origine...) — à vérifier et documenter dans les choix de calibration des profils de poste.

→ Principe directeur : **"Human in the loop"** à chaque étape de décision. Le produit informe, il ne décide jamais.

---

## 7. Périmètre fonctionnel

### 7.1 Inclus en V1 (MVP)

- Authentification — deux parcours d'inscription self-service : B2B (organisation/tenant isolé) et B2C (compte individuel) — gratuit, sans paiement
- Création et gestion de postes (avec définition manuelle du profil cible)
- Création et gestion d'équipes (rattachement de collaborateurs)
- Questionnaire Big Five (IPIP), bilingue FR/EN, envoyable par lien à un candidat/collaborateur
- Calcul du Fit Poste
- Calcul du Fit Équipe
- Rapport de restitution (visuel + texte explicatif)
- Interface bilingue FR/EN complète

### 7.2 Explicitement hors V1 (backlog futur)

- Mode calibré automatique du profil de poste (nécessite volume de données)
- Espace candidat en self-service (consultation de son propre profil)
- Imports/exports vers des ATS / SIRH tiers
- Module d'administration avancée multi-organisation
- Customisation du questionnaire par l'organisation

### 7.3 Hors périmètre définitif (refusé par principe)

- Analyse de CV / lettre de motivation pour en déduire un profil psychologique
- Tout score de décision automatique ("recommandé / non recommandé")
- Tout typage non scientifiquement validé (MBTI, etc.)

---

## 8. Découpage en Epics (base pour les User Stories)

| # | Epic | Description courte |
|---|---|---|
| E1 | **Authentification & organisations** | Comptes, rôles (RH/Manager), tenants |
| E2 | **Gestion des postes** | CRUD postes, définition du profil cible manuel |
| E3 | **Gestion des équipes** | CRUD équipes, rattachement des membres |
| E4 | **Questionnaire Big Five** | Passation du questionnaire IPIP, bilingue, par lien externe |
| E5 | **Moteur de calcul de Fit** | Algorithmes Fit Poste / Fit Équipe |
| E6 | **Rapports & restitution** | Visualisation radar, synthèse textuelle, export |
| E7 | **Internationalisation** | Infrastructure FR/EN sur l'ensemble du produit |
| E8 | **Conformité & gouvernance** | Consentement, traçabilité, droits RGPD |

Les User Stories seront ajoutées au fil de l'eau dans `docs/product/user-stories.md`, rattachées à ces epics.

---

## 9. Stack technique

*À définir dans une session dédiée, une fois ce cadrage validé.*

---

## 10. Questions ouvertes / à trancher

- [ ] Nom définitif du produit (placeholder actuel : "FitRadarHR")
- [ ] Le questionnaire IPIP exact à utiliser (nombre d'items — versions 50, 100 ou 300 items existent, arbitrage longueur vs précision)
- [ ] Granularité du multi-tenant pour la V1 (une organisation isolée suffit-elle, ou faut-il déjà prévoir des sous-équipes/départements ?)
