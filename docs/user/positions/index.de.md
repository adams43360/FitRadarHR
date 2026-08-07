# Stellenverwaltung

Eine **Stelle** in FitRadarHR ist ein Datensatz, der mit einem Ziel-Big-Five-Profil verknüpft ist — der von HR für diese Rolle definierten „idealen Persönlichkeit“.

## Was Sie tun können

- [Eine Stelle erstellen](create.md) mit Titel (FR und EN), Abteilung und Zielteam
- [Das Zielprofil definieren](profile.md) — gewünschter Bereich für jede der 5 OCEAN-Dimensionen
- Das **Ranking der Personen nach Fit** direkt auf der Stellenseite einsehen (filterbar nach Kandidat / Mitarbeitende(r))
- Eine Stelle archivieren, wenn sie nicht mehr aktiv ist
- Einen [Fit-Bericht](../reports/job-fit.md) erstellen, der das Profil einer Person mit dem Zielprofil der Stelle vergleicht

## Verbindung zu Abteilungen und Teams

Eine Stelle kann einer **Abteilung** (z. B. F&E, Vertrieb) und einem **Zielteam** (z. B. Backend Team) zugeordnet werden. Ist ein Team definiert, zeigt der Profilbericht eines Kandidaten automatisch den entsprechenden Team-Fit neben dem Stellen-Fit an.

## Konzept: das Zielprofil

Statt eines einzelnen Werts pro Dimension verwendet FitRadarHR einen **Min/Max-Bereich**. Beispiel für eine Vertriebsstelle:

| Dimension | Min | Max | Interpretation |
|---|---|---|---|
| Offenheit | 40 | 70 | Moderate Kreativität, nicht zwingend explorativ |
| Gewissenhaftigkeit | 60 | 90 | Sorgfalt und Organisation wichtig |
| Extraversion | 65 | 100 | Starke relationale Leichtigkeit gewünscht |
| Verträglichkeit | 50 | 80 | Kooperativ, ohne zu nachgiebig zu sein |
| Neurotizismus | 0 | 40 | Emotionale Stabilität wichtig |

!!! info "Bereich statt Einzelwert"
    Der Bereich vermeidet eine Überregulierung des Profils. „Verträglichkeit zwischen 60 und 80“ ist realistischer als ein exakter Wert von 70.
