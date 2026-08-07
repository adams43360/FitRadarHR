# Demo ausprobieren

FitRadarHR bietet eine **öffentliche Demo-Umgebung**: ein Klick genügt, um das Tool
mit realistischen Daten zu erkunden, ohne ein Konto zu erstellen.

## Zugriff auf die Demo

Klicken Sie auf der Anmeldeseite oder der Startseite auf **✨ Demo ausprobieren**.
Sie werden sofort mit dem Demo-Konto angemeldet, in der Rolle HR-Verantwortliche(r).

!!! info "Keine Registrierung erforderlich"
    Das Demo-Konto hat kein Passwort: Der Button ist der einzige Zugangsweg.

## Was die Demo enthält

Die Umgebung simuliert **Nexatech**, ein fiktives Softwareunternehmen mit rund hundert Beschäftigten:

- 6 Abteilungen (Engineering, Produkt & Design, Vertrieb, Customer Success, Finanzen, HR)
- 10 Teams mit ihren Mitgliedern und vollständig ausgefüllten OCEAN-Profilen
- 9 offene Stellen mit Ziel-Big-Five-Profilen und Fit-Rankings
- Kandidaten in Bewertung (abgeschlossene, ausstehende oder laufende Fragebögen)
- Stellen- und Team-Fit-Berichte, einsehbar und als PDF exportierbar

Die Teamprofile sind bewusst kontrastreich gestaltet (ein extravertiertes Vertriebsteam,
ein sehr gewissenhaftes Finanzteam…), damit die Komplementaritätssignale aussagekräftig sind.

## Die Regeln der Demo-Umgebung

!!! warning "Fiktive Daten, alle 24 Stunden zurückgesetzt"
    Alle Daten sind **fiktiv und deterministisch**: Sie werden täglich identisch
    gelöscht und neu erstellt. Geben Sie keine realen Daten in die Demo ein.

Zudem sind einige Funktionen angepasst:

- **Es wird keine E-Mail aus der Demo versendet.** Beim Versenden eines Fragebogens
  wird der Ausfüll-Link auf dem Bildschirm angezeigt — Sie können ihn selbst öffnen, um den
  Kandidatenablauf vollständig zu testen (einschließlich DSGVO-Einwilligung).
- **Die DSGVO-Löschung ist deaktiviert** (da die Daten fiktiv sind und von allen
  Besucherinnen und Besuchern geteilt werden).

## Möchten Sie weitergehen?

Erstellen Sie Ihr eigenes kostenloses Konto ([siehe Konto erstellen](signup.md)) oder
[kontaktieren Sie uns](mailto:contact@fitradarhr.com) für eine dedizierte Testumgebung für Ihr Team.

---

## Für Administratoren (Self-Hosting)

Der Demo-Modus wird über die Umgebung konfiguriert:

```bash
# .env
DEMO_MODE=True
```

```bash
# Demo-Organisation erstellen oder zurücksetzen
python manage.py seed_demo

# In der Entwicklung (Docker)
make seed-demo
```

In der Produktion spielt der `demo-reset`-Dienst in `docker-compose.yml` den Seed alle 24 Stunden erneut ab:

```bash
docker compose -f docker/docker-compose.prod.yml --profile demo up -d
```
