# Public API (read-only)

FitRadarHR exposes a read-only JSON API, designed to connect a third-party tool (ATS, HRIS…) without manual intervention: positions, teams, people and fit results for your organization.

!!! warning "Never raw Big Five profiles"
    By product choice (minimizing data transmitted to third parties), the API **never exposes** a person's raw Big Five scores (Openness, Conscientiousness, Extraversion, Agreeableness, Neuroticism). Only derived results (questionnaire status, fit scores) are available.

## Generate an API key

An HR user accesses the management screen from the **API** link in the navigation bar (`/settings/api/`).

1. Enter a name to identify the integration (e.g. "Greenhouse ATS integration")
2. Click **Generate**
3. Copy the displayed key **immediately** — it will never be shown again (only its prefix remains visible in the list, to recognize it)

A key can be **revoked** at any time from the same screen; revocation is immediate and permanent.

## Authentication

Every request must carry the following header:

```
Authorization: Api-Key <your_key>
```

```bash
curl -H "Authorization: Api-Key frk_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" \
  https://your-domain.example/api/v1/positions/
```

A missing, invalid or revoked key returns a `401` error:

```json
{"error": "invalid_api_key", "detail": "Invalid or revoked API key."}
```

A key is always scoped to **a single organization** — it is impossible to access another organization's data, whatever the request.

## Available endpoints

All endpoints are **read-only (GET only)**.

| Endpoint | Description |
|---|---|
| `GET /api/v1/positions/` | List of positions (optional filter `?status=active\|archived`) |
| `GET /api/v1/positions/{id}/` | Position detail |
| `GET /api/v1/teams/` | List of teams |
| `GET /api/v1/teams/{id}/` | Team detail (includes number of active members) |
| `GET /api/v1/people/` | List of people (optional filter `?person_type=candidate\|collaborator`) |
| `GET /api/v1/people/{id}/` | Person detail — questionnaire status and "profile completed" indicator (never the scores) |
| `GET /api/v1/fit-results/positions/` | Position fit results (optional filters `?position_id=` and `?person_id=`) |
| `GET /api/v1/fit-results/teams/` | Team fit results, including complementarity (optional filters `?team_id=` and `?person_id=`) |

## Pagination

Lists are paginated: `?page=2&page_size=50` (maximum page size: 100). Response format:

```json
{
  "count": 128,
  "page": 1,
  "num_pages": 3,
  "page_size": 50,
  "results": [ ... ]
}
```
