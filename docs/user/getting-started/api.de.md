# Öffentliche API (nur Lesezugriff)

FitRadarHR bietet eine JSON-API mit reinem Lesezugriff, konzipiert für die Anbindung eines Drittanbieter-Tools (ATS, HRIS…) ohne manuellen Eingriff: Stellen, Teams, Personen und Fit-Ergebnisse Ihrer Organisation.

!!! warning "Niemals rohe Big-Five-Profile"
    Aus Produktentscheidung (Minimierung der an Dritte übermittelten Daten) gibt die API **niemals** die rohen Big-Five-Werte (Offenheit, Gewissenhaftigkeit, Extraversion, Verträglichkeit, Neurotizismus) einer Person preis. Verfügbar sind ausschließlich abgeleitete Ergebnisse (Fragebogenstatus, Fit-Werte).

## Einen API-Schlüssel erzeugen

Eine HR-Person greift über den Link **API** in der Navigationsleiste (`/settings/api/`) auf den Verwaltungsbildschirm zu.

1. Geben Sie einen Namen zur Identifikation der Integration ein (z. B. „Greenhouse-ATS-Integration“)
2. Klicken Sie auf **Generieren**
3. Kopieren Sie den angezeigten Schlüssel **sofort** — er wird danach nie wieder angezeigt (nur sein Präfix bleibt zur Wiedererkennung in der Liste sichtbar)

Ein Schlüssel kann jederzeit über denselben Bildschirm **widerrufen** werden; der Widerruf ist sofort und endgültig.

## Authentifizierung

Jede Anfrage muss folgenden Header enthalten:

```
Authorization: Api-Key <Ihr_Schlüssel>
```

```bash
curl -H "Authorization: Api-Key frk_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" \
  https://ihre-domain.example/api/v1/positions/
```

Ein fehlender, ungültiger oder widerrufener Schlüssel liefert einen `401`-Fehler:

```json
{"error": "invalid_api_key", "detail": "Invalid or revoked API key."}
```

Ein Schlüssel ist immer auf **eine einzige Organisation** beschränkt — ein Zugriff auf die Daten einer anderen Organisation ist unabhängig von der Anfrage unmöglich.

## Verfügbare Endpunkte

Alle Endpunkte sind **nur lesend (nur GET)**.

| Endpunkt | Beschreibung |
|---|---|
| `GET /api/v1/positions/` | Liste der Stellen (optionaler Filter `?status=active\|archived`) |
| `GET /api/v1/positions/{id}/` | Detail einer Stelle |
| `GET /api/v1/teams/` | Liste der Teams |
| `GET /api/v1/teams/{id}/` | Detail eines Teams (inkl. Anzahl aktiver Mitglieder) |
| `GET /api/v1/people/` | Liste der Personen (optionaler Filter `?person_type=candidate\|collaborator`) |
| `GET /api/v1/people/{id}/` | Detail einer Person — Fragebogenstatus und Indikator „Profil ausgefüllt“ (nie die Werte) |
| `GET /api/v1/fit-results/positions/` | Fit-Ergebnisse für Stellen (optionale Filter `?position_id=` und `?person_id=`) |
| `GET /api/v1/fit-results/teams/` | Fit-Ergebnisse für Teams, einschließlich Komplementarität (optionale Filter `?team_id=` und `?person_id=`) |

## Paginierung

Listen sind paginiert: `?page=2&page_size=50` (maximale Seitengröße: 100). Antwortformat:

```json
{
  "count": 128,
  "page": 1,
  "num_pages": 3,
  "page_size": 50,
  "results": [ ... ]
}
```
