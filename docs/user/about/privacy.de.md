# Datenschutz und DSGVO

FitRadarHR wurde mit DSGVO-Konformität als Designvorgabe konzipiert, nicht als nachträglich hinzugefügte Schicht.

## Erhobene Daten

| Daten | Wer | Dauer | Rechtsgrundlage |
|---|---|---|---|
| E-Mail, Vorname, Nachname (Kontonutzer) | Kontonutzer | Dauer des Kontos | Vertrag |
| E-Mail, Vorname, Nachname (bewertete Personen) | Kandidaten / Mitarbeitende | Dauer der Organisation | Berechtigtes Interesse + Einwilligung |
| Fragebogenantworten (Rohdaten) | Bewertete Personen | Nach Berechnung gelöscht | Einwilligung |
| Big-Five-Werte | Bewertete Personen | Dauer der Organisation | Einwilligung |
| Fit-Berichte | Bewertete Personen | Dauer der Organisation | Berechtigtes Interesse |

## Ausdrückliche Einwilligung

Vor Beantwortung des Fragebogens liest und akzeptiert jede Person ausdrücklich einen Informationshinweis. Diese Einwilligung wird:
- mit Zeitstempel und Version des angezeigten Textes erfasst,
- unveränderlich gespeichert (nachträglich nicht änderbar),
- kann widerrufen werden (die Person kann die Löschung ihrer Daten verlangen).

## Recht auf Löschung

Auf Antrag einer bewerteten Person werden ihre personenbezogenen Daten (Vorname, Nachname, E-Mail) **anonymisiert** (`[gelöscht]`). Zugehörige Fit-Berichte werden ohne namentlichen Bezug aufbewahrt, zur organisatorischen Nachvollziehbarkeit.

## Audit-Protokoll

Alle sensiblen Aktionen (Einsicht in einen Bericht, PDF-Export, Linkversand, Löschung) werden in einem unveränderlichen Protokoll erfasst — im Einklang mit den Anforderungen des EU AI Act für Hochrisikosysteme (siehe [EU AI Act und Recruiting](eu-ai-act.md) für den Zeitplan und die Details der Pflichten).

## Reichweitenmessung

FitRadarHR verwendet [Matomo](https://matomo.org), selbst gehostet auf derselben Infrastruktur, um Nutzungsvolumen und meistgenutzte Funktionen zu erfassen. Diese Messung ist unter der **CNIL-Einwilligungsausnahme** konfiguriert: kein Cookie, anonymisierte IP, keine personenbezogenen Daten erhoben, keine Datenübermittlung an Dritte. Für diese Nutzung wird daher kein Einwilligungsbanner angezeigt — zu unterscheiden von der ausdrücklichen Einwilligung, die für den Big-Five-Fragebogen erforderlich ist (siehe oben) und unverändert bleibt.

## Hosting

FitRadarHR wird selbst gehostet. Sie behalten die Kontrolle über den Speicherort Ihrer Daten. Es werden keine Daten an Dritte übermittelt.

!!! info "Self-Hosting"
    Wenn Sie FitRadarHR auf Ihrem eigenen VPS bereitstellen, sind Sie für die Verarbeitung personenbezogener Daten verantwortlich (Rolle des Verantwortlichen). Denken Sie daran, Ihr Verzeichnis von Verarbeitungstätigkeiten zu aktualisieren.
