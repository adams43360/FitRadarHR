# Méthodologie de traduction du questionnaire IPIP-100

> Note interne (PM). Le disclaimer destiné aux utilisateurs finaux est dans
> `docs/user/about/big-five.md` (publié sur le site de doc). Ce document explique
> *comment* chaque traduction a été produite, pour que toute évolution future
> (correction, ajout d'une langue) parte d'une base tracée plutôt que de mémoire.

## Pourquoi ce document

Règle non négociable #1 du cadrage produit : *« Seul le questionnaire Big Five validé
(IPIP) qualifie un profil. »* Cette exigence de rigueur sur l'instrument s'étend
logiquement à ses traductions — une traduction approximative ou non sourcée
dégraderait la validité de l'instrument aussi sûrement qu'un questionnaire maison.
D'où le choix de sourcer chaque langue sur les traductions officielles publiées par
IPIP quand elles existent, et de documenter précisément ce qui ne l'est pas.

## Sources officielles utilisées

- **Allemand** — [German 100-Item Big-Five Factor Markers](https://ipip.ori.org/German100-ItemBig-FiveFactorMarkers.htm),
  traduit et validé par rétro-traduction en 2001 par Heinz Streib & Manuela Wiedmaier
  (Forschungsstelle Biographische Religionsforschung, Universität Bielefeld).
  Couvre les 100 items → **couverture complète**.
- **Espagnol** — [Spanish Big-Five Factor Markers](https://ipip.ori.org/SpanishBig-FiveFactorMarkers.htm),
  fourni par Rodrigo de Oliveira ; référence de publication : de Oliveira, R.,
  Cherubini, M., Oliver, N. (2013). *Influence of personality on satisfaction with
  mobile phone services*. ACM Transactions on Computer-Human Interaction, 20(2),
  Article 10. Couvre uniquement les **50 items du marqueur original Goldberg** →
  **couverture partielle** (50/100).

## Méthode de correspondance

Le fichier `apps/survey/ipip_data.py` contient nos 100 items FR/EN historiques
(certains étant des adaptations professionnelles, pas des traductions littérales du
marqueur Goldberg d'origine — voir plus bas). Pour chaque item :

1. Recherche du texte anglais officiel IPIP correspondant par correspondance exacte
   de sens dans les tables DE (100 items) et ES (50 items).
2. Si trouvé dans les deux sources → traduction DE et ES officielles utilisées telles
   quelles (avec une correction mineure d'une coquille évidente sur l'item DE #14,
   "Ich bin mache mir Sorgen…" → "Ich mache mir Sorgen…").
3. Si trouvé seulement en allemand (item d'extension 51-100, absent du marqueur
   Goldberg original à 50 items) → DE officiel, **ES traduit par nos soins** dans un
   registre cohérent avec les items ES officiels du même bloc.
4. Si l'item FR/EN lui-même est une adaptation maison ne correspondant à aucun item
   officiel du marqueur Goldberg (voir liste ci-dessous) → DE et ES traduits par nos
   soins, sans base officielle.

## Items sans correspondance officielle dans le marqueur Goldberg

Quatre items de notre questionnaire FR/EN sont des paraphrases qui ne correspondent à
aucun des 100 marqueurs originaux (ce sont des adaptations déjà en place avant ce
travail de traduction, conservées pour ne pas casser la compatibilité des profils déjà
calculés — voir la règle d'immutabilité de l'ordre des 50 premiers items) :

| Id | FR | Raison |
|---|---|---|
| C5 | "Je néglige souvent les détails." | Paraphrase inversée de C3, pas un item Goldberg |
| C10 | "Je mène mes projets à leur terme." | Proche de C14 ("fais des plans et m'y tiens") mais formulation distincte |
| O4 | "Les idées abstraites m'intéressent." | Reformulation positive de l'item officiel inversé "Not interested in abstract ideas" |
| O5 | "Je n'aime pas les sujets qui demandent trop de réflexion." | Paraphrase sans équivalent Goldberg direct |

Pour ces quatre items, DE et ES sont des traductions maison (DE/ES pour C5 et O4
s'appuient sur l'inversion de l'item officiel correspondant quand il existe, pour
rester cohérentes lexicalement avec le reste du questionnaire).

## Couverture finale par langue (100 items)

| Langue | Items officiels | Items maison | Détail |
|---|---|---|---|
| EN | 100 | 0 | Source originale Goldberg (1992) |
| DE | 96 | 4 | Les 4 items sans équivalent Goldberg (C5, C10, O4, O5) |
| ES | ~46 | ~54 | 50 items du marqueur original (moins les 4 non-officiels ci-dessus,
  qui n'ont donc pas de source ES même si leur *position* est dans les 50 premiers) +
  tous les items d'extension 51-100 |

## Portée de la garantie

Cette méthodologie garantit que **la version 50 items est intégralement sourcée sur
des traductions officielles publiées** en anglais, allemand et espagnol (aux 4 items
non-officiels près, qui existaient déjà en FR/EN avant ce travail). La version 100
items introduit pour l'espagnol une zone non validée officiellement (l'extension
51-100), documentée dans le disclaimer utilisateur (`docs/user/about/big-five.md`).

## Échelle de réponse (Likert 1-5)

Les libellés `SCALE_DE`/`SCALE_ES` (`apps/survey/ipip_data.py`) suivent le même choix
de formulation "accord/désaccord" déjà retenu pour FR/EN (plutôt que l'échelle
"exact/inexact" parfois utilisée par IPIP en anglais) — traduction directe des
libellés EN existants, pas une source officielle distincte à documenter.
