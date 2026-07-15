# Design tokens — POC Figma / Tokens Studio

> **Statut : POC exploratoire** (juillet 2026). N'impacte pas le code de production.
> Objectif : tester une source de vérité unique pour le design, partagée entre le code
> et Figma, et documenter la démarche pour un futur article (labo perso).

## Pourquoi

L'UI de FitRadarHR s'est construite avec Tailwind directement dans les templates : le
design system existe, mais il est **implicite** (répété classe par classe). Ce POC
l'extrait sous forme de **design tokens** — un fichier JSON qui devient la source de
vérité unique, consommable à la fois :

- par **Figma** (via le plugin [Tokens Studio](https://tokens.studio/)) pour produire
  des maquettes fidèles au produit réel ;
- par le **code** (variables CSS générées) pour prototyper des écrans en HTML sans
  dériver du design existant.

Leçon anticipée pour l'article : définir les tokens **au départ** d'un projet évite la
phase de rétro-ingénierie faite ici (audit des 40+ classes Tailwind les plus utilisées
dans les templates).

## Fichiers

```
design/
  tokens/
    tokens.json      # Source de vérité (format Tokens Studio, importable dans Figma)
    build_css.py     # Générateur tokens.json → tokens.css (résout les références)
    tokens.css       # Variables CSS générées — NE PAS ÉDITER À LA MAIN
  mockups/
    dashboard.html   # Maquette Dashboard RH consommant uniquement les tokens
docs/technical/design-tokens.md   # Ce document
```

## Architecture des tokens (3 niveaux)

Le fichier `tokens.json` contient trois *token sets*, du plus brut au plus contextuel :

| Set | Rôle | Exemple |
|---|---|---|
| `core` | **Primitifs** — valeurs brutes, sans signification produit | `color.indigo.600 = #4f46e5` |
| `semantic` | **Sémantiques** — rôle dans l'UI, référence les primitifs | `bg.brand = {color.indigo.600}` |
| `component` | **Composants** — décisions par composant | `button.primary.bg = {bg.brand}` |

La règle : les maquettes et le code ne consomment **que** les niveaux `semantic` et
`component`. Les primitifs ne servent qu'à alimenter les deux autres niveaux (rares
exceptions notées dans la maquette). C'est ce qui rend un rebranding ou un thème sombre
possible en ne touchant que le mapping sémantique.

### Ce que les tokens capturent (extrait de l'audit)

- **Couleur primaire** : indigo-600 (boutons, liens, valeurs de stats), hover indigo-700,
  fonds subtils indigo-50/100.
- **Identité logo** : teal-700 / teal-500 (navbar uniquement).
- **Neutres** : échelle gray (fond de page gray-50, texte gray-900 → gray-400,
  bordures gray-200/300).
- **Statuts** : warning amber (bannière démo, badges "envoyé"), danger red (expiré,
  erreurs), success green.
- **Dataviz** (radar charts Chart.js) : personne = indigo-500, équipe = emerald-500,
  cible/poste = amber-500.
- **Formes** : cartes `radius 16px` (rounded-2xl), boutons/alertes `8px` (rounded-lg),
  badges pleine rondeur.
- **Typo** : stack système, échelle 12→30 px, labels de cartes en uppercase + tracking.

## Workflow

### Code → maquette HTML

```bash
python design/tokens/build_css.py   # régénère tokens.css depuis tokens.json
open design/mockups/dashboard.html  # la maquette consomme uniquement var(--token)
```

Toute modification de `tokens.json` se propage à la maquette après régénération.

### Code → Figma

1. Dans Figma, installer le plugin **Tokens Studio for Figma**.
2. Plugin → Settings → Load from file/URL → charger `design/tokens/tokens.json`
   (le fichier inclut `$themes` et `$metadata`, reconnus par le plugin).
3. Activer le thème « FitRadarHR Light » : les sets `semantic` et `component` sont
   appliqués, `core` reste en source.
4. Appliquer les tokens aux calques (clic droit sur un token → apply). Tokens Studio
   peut aussi pousser les tokens en **variables Figma natives** (Export to Figma).

### Figma → code (sens inverse)

Tokens Studio sait synchroniser vers un dépôt Git (GitHub sync) : un designer peut
modifier un token dans Figma et ouvrir une PR sur `tokens.json`. Non testé dans ce POC.

## Conventions

- **Nommage** : kebab-case, anglais (cohérent avec la convention code du projet).
  Chemin JSON `bg.brand-hover` → variable CSS `--bg-brand-hover`.
- **Types** : types Tokens Studio (`color`, `fontSizes`, `spacing`, `borderRadius`,
  `boxShadow`…). Les types dimensionnels sont convertis en `px` par le générateur.
- **Références** : syntaxe `{path.to.token}`, sans nom de set (les sets sont fusionnés
  dans l'ordre défini par `$metadata.tokenSetOrder`).
- Le format choisi est celui de **Tokens Studio** (clés `value`/`type`), pas le
  standard W3C DTCG (`$value`/`$type`) — choix pragmatique : import Figma direct.
  Une conversion W3C est triviale si besoin (renommage de clés).

## Limites connues du POC

1. **Tailwind n'est pas branché sur les tokens** : l'app de prod utilise toujours le CDN
   Tailwind avec les valeurs par défaut. Les tokens *décrivent* l'existant, ils ne le
   *pilotent* pas encore. Étape suivante naturelle : build Tailwind avec une config
   générée depuis `tokens.json` (ou Style Dictionary → `tailwind.config.js`).
2. **Un seul thème** (light). La structure à 3 niveaux rend un thème sombre possible en
   ajoutant un set `semantic-dark`, mais ce n'est pas fait.
3. **Périmètre partiel** : seuls les tokens observés dans l'audit des templates sont
   capturés. Les écrans PDF (WeasyPrint) ont leur propre CSS, non audité.
4. **Générateur maison** : `build_css.py` (~90 lignes, zéro dépendance) suffit pour le
   POC ; en production, [Style Dictionary](https://styledictionary.com/) serait plus
   robuste (multi-plateformes, transforms).

## Prochaines étapes possibles

- Importer `tokens.json` dans Figma et reconstruire le Dashboard en maquette Figma
  pour valider la boucle complète (fait côté code, pas encore côté Figma).
- Décliner une 2ᵉ maquette (rapport Fit avec radar) pour éprouver les tokens dataviz.
- Brancher le build Tailwind de prod sur les tokens.
- Article de synthèse sur la démarche (projet labo perso, à venir).
