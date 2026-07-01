# CLAUDE.md — Contexte projet pour Claude Code

> Ce fichier est lu automatiquement par Claude Code à chaque session dans ce dépôt.
> Il donne le contexte produit et les règles à respecter sans avoir à les répéter.

## Le projet

**FitRadarHR** *(nom placeholder, à confirmer)* — un outil bilingue (FR/EN), gratuit et libre de droits, qui aide les RH et
managers à évaluer la compatibilité d'une personne (candidat ou collaborateur en mobilité
interne) avec un poste et/ou une équipe, en s'appuyant sur le modèle de personnalité
**Big Five / OCEAN** (questionnaire IPIP, domaine public).

Le cadrage produit complet est dans `docs/product/00-cadrage.md` — à lire avant toute
décision de conception ou de développement structurante.

## Règles non négociables

Ces règles sont issues du cadrage produit et ne doivent jamais être contournées, même si
une demande future semble les justifier ponctuellement :

1. **Jamais d'analyse de CV / lettre de motivation / document libre pour en déduire un
   profil psychologique.** Seul le questionnaire Big Five validé (IPIP) qualifie un profil.
2. **Jamais de score de décision automatique** ("recommandé / non recommandé"). Le produit
   informe, il ne décide jamais — principe de "human in the loop" à chaque restitution.
3. **Jamais de typologie non scientifiquement validée** (MBTI, etc.) comme fondement du
   produit.
4. Toute fonctionnalité touchant aux données de personnalité doit respecter le RGPD
   (consentement explicite, droit d'accès/suppression, minimisation) et anticiper le
   classement "haut risque" de l'EU AI Act (traçabilité, supervision humaine documentée).
5. Le produit est bilingue FR/EN **dès la conception** — pas une couche ajoutée après coup.
   Toute string utilisateur doit passer par le système d'i18n, jamais de texte en dur.

## Structure du dépôt

```
/docs
  /product
    00-cadrage.md        # Cadrage produit complet (vision, périmètre, epics)
    user-stories.md       # User stories, ajoutées au fil de l'eau, rattachées aux epics
  /technical
    (à venir : architecture, stack, schéma de données)
CLAUDE.md                 # Ce fichier
README.md                 # Présentation du projet (pour GitHub)
```

## Epics de référence

User stories à rattacher systématiquement à l'un de ces epics (voir `00-cadrage.md` section 8) :

| # | Epic |
|---|---|
| E1 | Authentification & organisations |
| E2 | Gestion des postes |
| E3 | Gestion des équipes |
| E4 | Questionnaire Big Five |
| E5 | Moteur de calcul de Fit |
| E6 | Rapports & restitution |
| E7 | Internationalisation |
| E8 | Conformité & gouvernance |

## État d'avancement

- [x] Cadrage produit validé
- [ ] Stack technique définie
- [ ] User stories Epic 1 (Authentification)
- [ ] Premier scaffold technique

*(Section à tenir à jour manuellement ou via Claude Code au fil des sessions.)*

## Conventions de travail

- Stack technique : à définir, sera documentée dans `docs/technical/stack.md` une fois tranchée.
- Commits : à définir (convention proposée : Conventional Commits — `feat:`, `fix:`, `docs:`...).
- Les user stories suivent le format `En tant que [rôle], je veux [besoin], afin de [valeur]`
  avec critères d'acceptation explicites, rédigées en français (le code et les noms de
  variables restent en anglais).
