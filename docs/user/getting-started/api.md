# API publique (lecture seule)

FitRadarHR expose une API JSON en lecture seule, pensée pour connecter un outil tiers (ATS, SIRH…) sans intervention manuelle : postes, équipes, personnes et résultats de fit de votre organisation.

!!! warning "Jamais les profils Big Five bruts"
    Par choix produit (minimisation des données transmises à des tiers), l'API **n'expose jamais** les scores Big Five bruts (Ouverture, Conscienciosité, Extraversion, Agréabilité, Neuroticisme) d'une personne. Seuls des résultats dérivés (statut du questionnaire, scores de fit) sont disponibles.

## Générer une clé API

Un RH accède à l'écran de gestion depuis le lien **API** de la barre de navigation (`/settings/api/`).

1. Saisissez un nom pour identifier l'intégration (ex. « Intégration ATS Greenhouse »)
2. Cliquez sur **Générer**
3. Copiez la clé affichée **immédiatement** — elle ne sera plus jamais visible ensuite (seul son préfixe reste affiché dans la liste, pour la reconnaître)

Une clé peut être **révoquée** à tout moment depuis le même écran ; la révocation est immédiate et définitive.

## Authentification

Chaque requête doit porter l'en-tête suivant :

```
Authorization: Api-Key <votre_clé>
```

```bash
curl -H "Authorization: Api-Key frk_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" \
  https://votre-domaine.example/api/v1/positions/
```

Une clé absente, invalide ou révoquée renvoie une erreur `401` :

```json
{"error": "invalid_api_key", "detail": "Invalid or revoked API key."}
```

Une clé est toujours scopée à **une seule organisation** — impossible d'accéder aux données d'une autre organisation, quelle que soit la requête.

## Endpoints disponibles

Tous les endpoints sont en **lecture seule (GET uniquement)**.

| Endpoint | Description |
|---|---|
| `GET /api/v1/positions/` | Liste des postes (filtre optionnel `?status=active\|archived`) |
| `GET /api/v1/positions/{id}/` | Détail d'un poste |
| `GET /api/v1/teams/` | Liste des équipes |
| `GET /api/v1/teams/{id}/` | Détail d'une équipe (inclut le nombre de membres actifs) |
| `GET /api/v1/people/` | Liste des personnes (filtre optionnel `?person_type=candidate\|collaborator`) |
| `GET /api/v1/people/{id}/` | Détail d'une personne — statut du questionnaire et indicateur "profil renseigné" (jamais les scores) |
| `GET /api/v1/fit-results/positions/` | Résultats de fit Poste (filtres optionnels `?position_id=` et `?person_id=`) |
| `GET /api/v1/fit-results/teams/` | Résultats de fit Équipe, y compris la complémentarité (filtres optionnels `?team_id=` et `?person_id=`) |

## Pagination

Les listes sont paginées : `?page=2&page_size=50` (taille de page maximale : 100). Format de réponse :

```json
{
  "count": 128,
  "page": 1,
  "num_pages": 3,
  "page_size": 50,
  "results": [ ... ]
}
```
