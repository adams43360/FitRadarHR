# Öffentliche Roadmap

Die V1 von FitRadarHR ist vollständig (Epics E1–E8 ausgeliefert), und **V2 ist
vollständig ausgeliefert** (9/9 Punkte). Diese Seite stellt außerdem
Kandidatenideen für eine **V3** vor, priorisiert nach der **RICE**-Methode —
mit voller Transparenz, wie im übrigen Projekt.

## So liest man den RICE-Score

**RICE = (Reach × Impact × Confidence) / Effort**

- **Reach (Reichweite)** — wie viele Nutzer pro Quartal betroffen sind (Skala 1–10)
- **Impact (Wirkung)** — Effekt auf die North Star (aufgerufene Berichte / Woche): 0,5 = gering, 1 = mittel, 2 = hoch, 3 = massiv
- **Confidence (Konfidenz)** — Vertrauen in die Schätzungen: 50 % / 80 % / 100 %
- **Effort (Aufwand)** — Arbeitsaufwand in Personenwochen

## Priorisierung V2

| # | Feature | Reach | Impact | Konf. | Effort | RICE-Score | Status |
|---|---|---|---|---|---|---|---|
| 1 | Automatische Fragebogen-Erinnerungen | 8 | 2 | 80 % | 1 | **12.8** | ✅ Ausgeliefert |
| 2 | Einladen von Managern in die Organisation | 7 | 2 | 80 % | 2 | **5.6** | ✅ Ausgeliefert |
| 3 | Kandidatenvergleich für eine Stelle | 6 | 2 | 80 % | 2 | **4.8** | ✅ Ausgeliefert |
| 4 | CSV-Import von Personen | 6 | 1 | 100 % | 1.5 | **4.0** | ✅ Ausgeliefert |
| 5 | Erneute Durchführung & Longitudinal-Tracking | 5 | 2 | 50 % | 2 | **2.5** | ✅ Ausgeliefert |
| 6 | Retention-Kohorten in Analytics | 4 | 1 | 80 % | 1.5 | **2.1** | ✅ Ausgeliefert |
| 7 | SSO Keycloak / OIDC | 3 | 1 | 80 % | 3 | **0.8** | ✅ Ausgeliefert |
| 8 | ES-/DE-Übersetzungen | 2 | 1 | 80 % | 2 | **0.8** | ✅ Ausgeliefert |
| 9 | Öffentliche API (nur Lesezugriff) | 2 | 1 | 50 % | 3 | **0.3** | ✅ Ausgeliefert |

## Die Argumente, Punkt für Punkt

**1. Automatische Erinnerungen** — der Analytics-Funnel zeigt, dass der Großteil
der Abbrüche zwischen dem Senden des Links und dem Start liegt. Eine Erinnerung
an Tag 3 wirkt direkt auf die Abschlussrate, bei minimalem Aufwand. Bestes
Wert-Aufwand-Verhältnis der Liste.

**2. Einladen von Managern** — heute lebt eine Organisation meist mit nur einem
HR-Konto. Jeder eingeladene Manager ist ein zusätzlicher Berichtskonsument: das
ist der „Referral“-Hebel des AARRR-Funnels.

**3. Kandidatenvergleich** — das Fit-Ranking existiert bereits auf der
Stellenseite; die Nebeneinander-Ansicht (überlagerte Radardiagramme,
Komplementaritäten) ist der natürliche nächste Schritt, den der
Recruiting-Anwendungsfall verlangt. Hohe Wirkung auf die Berichtsnutzung.

**4. CSV-Import** — Onboarding-Reibung: 50 Mitarbeitende manuell zu erfassen,
schreckt ab. Indirekte Wirkung auf die North Star, aber maximale Konfidenz
(offensichtlicher Bedarf).

**5. Erneute Durchführung** — Big-Five-Profile entwickeln sich langsam, aber sie
entwickeln sich; nützlich für interne Mobilität. 50 % Konfidenz: der tatsächliche
Bedarf muss noch in der Discovery-Phase validiert werden.

**6. Retention-Kohorten** — vertieft die Analytics-Seite für reife
Organisationen. Nur für bereits aktivierte Organisationen relevant, daher
geringere Reichweite.

**7. SSO / OIDC** — notwendig für größere Organisationen; geringere Reichweite
in der aktuellen Zielgruppe (KMU/Scale-ups), aber ein IdP pro Organisation,
additiv zum Passwort (nie ein Ersatz), hält den Wartungsaufwand vertretbar.
Ausgeliefert, noch nicht mit einem echten IdP in Produktion validiert.

**8. ES-/DE-Übersetzungen** — vollständige Parität, einschließlich des
IPIP-Fragebogens, nicht nur der Oberfläche. Der deutsche Fragebogen basiert
vollständig auf der offiziellen IPIP-Übersetzung (100/100 Items); Spanisch für
die kurze Version (50 Items), aber die lange Version führt einen intern
übersetzten Bereich ein, da keine veröffentlichte offizielle Quelle vorliegt —
siehe `docs/user/about/big-five.md`.

**9. Öffentliche API (nur Lesezugriff)** — echter Wert, aber heute nicht
differenzierend. Ausgeliefert mit bewusst eingeschränktem Umfang: Stellen/Teams,
Personen + Fragebogenstatus, Fit-Ergebnisse — niemals rohe Big-Five-Profile
(DSGVO-Minimierung). API-Schlüssel-Authentifizierung pro Organisation.

## Priorisierung V3

Die Punkte #1 und #2 sind ausgeliefert; die Punkte 3 bis 8 bleiben unentschiedene
Kandidaten.

| # | Feature | Reach | Impact | Konf. | Effort | RICE-Score | Status |
|---|---|---|---|---|---|---|---|
| 1 | Umgekehrter Fit — beste Stellen für eine Person | 5 | 2 | 90 % | 1.5 | **6.0** | ✅ Ausgeliefert |
| 2 | Monetarisierung (kostenloser Plan → Abo) | 8 | 3 | 80 % | 5 | **3.84** | ✅ Ausgeliefert |
| 3 | Lückenanalyse eines Teams | 5 | 2 | 60 % | 2 | **3.0** | ✅ Ausgeliefert |
| 4 | Kandidaten-/Mitarbeiterportal (Zugriff auf eigenes Profil) | 6 | 2 | 70 % | 3 | **2.8** | Kandidat |
| 5 | Exportierbares AI-Act-Compliance-Dossier | 3 | 2 | 70 % | 2 | **2.1** | Kandidat |
| 6 | Webhooks (Ergänzung zur öffentlichen API) | 3 | 1 | 70 % | 2 | **1.05** | Kandidat |
| 7 | Claude MCP — Aktivität außerhalb der Website einsehen | 2 | 1 | 60 % | 2 | **0.6** | Kandidat |
| 8 | Anonymisierte organisationsübergreifende Benchmarks | 4 | 1 | 40 % | 4 | **0.4** | Kandidat |
| 9 | Native Konnektoren (Workday, BambooHR, Personio…) | 3 | 2 | 30 % | 5 | **0.36** | Kandidat |

### Die Argumente, Punkt für Punkt

**1. Umgekehrter Fit** — heute geht man von einer Stelle aus, um Personen zu
ranken; der umgekehrte Weg (von einer Person ausgehen und sehen, welche offenen
Stellen am besten passen) dient der internen Mobilität, ohne zusätzliche Daten
zu erheben: eine neue Sicht auf die bestehende Fit-Engine. Bestes
Wert-Aufwand-Verhältnis der Liste. Ausgeliefert: keine neue Berechnung, nutzt
die bereits von der Engine (E5) erzeugten Fit-Ergebnisse.

**2. Monetarisierung** — das ist der eigentliche Grund für den Wechsel zur
Fair-Source-Lizenz (FSL-1.1-MIT): Damien erwog explizit eine kostenlose
Testphase, gefolgt von einem Abo. Hohe Reichweite (betrifft potenziell
irgendwann alle Organisationen) und starke Wirkung (es ist das Geschäftsmodell),
aber erheblicher Aufwand: Stripe-Integration, Kontingente pro Plan,
Abrechnungsbildschirme, Überschreitungsmanagement. Ausgeliefert: ein einziger
kostenpflichtiger Plan (39 €/Monat, Stripe Checkout + Customer Portal) und ein
dauerhaft kostenloser Plan (einheitliche Schwelle von 25 Personen —
Stellen und Fragebögen unbegrenzt). Das ursprüngliche 14-Tage-Testmodell wurde
zugunsten von Freemium aufgegeben: einfacher zu verstehen, ohne künstlichen
Konversionsdruck.

**3. Lückenanalyse eines Teams** — erweitert die bereits berechnete
Komplementarität: Aus dem aggregierten Teamprofil werden unterrepräsentierte
OCEAN-Dimensionen sichtbar gemacht. Bleibt im Produktrahmen — präsentiert als
Denkanstöße für einen Rekrutierungsplan, nie als klare Empfehlung (im Einklang
mit der Regel „niemals eine automatisierte Entscheidungsbewertung“).
Ausgeliefert: direkt von der Teamseite aus zugänglich, ohne eine Person
auszuwählen — siehe `docs/user/reports/team-gaps.md`.

**4. Kandidaten-/Mitarbeiterportal** — heute sehen nur HR/Manager die Berichte.
Der Person selbst Zugriff auf ihr Profil und ihren Bericht zu geben, stärkt das
„Human-in-the-loop“-Prinzip und das bereits implementierte DSGVO-Auskunftsrecht
(E8). Mittlere Konfidenz: erfordert ein neues Zugriffsmodell für
`Person`-Datensätze, die nicht zwingend über ein `User`-Konto verfügen.

**5. Exportierbares AI-Act-Compliance-Dossier** — ein Export (PDF/JSON) der
„Nachvollziehbarkeitsakte“ — wer hat was eingesehen, dokumentierte menschliche
Aufsicht — für Organisationen, die ihre Konformität im Rahmen der
„Hochrisiko“-Einstufung nachweisen müssen. Erweitert direkt E8, richtet sich
vor allem an stärker regulierte Organisationen (geringere Reichweite).

**6. Webhooks** — natürliche Ergänzung zur öffentlichen API (V2-Punkt #9): ein
Drittsystem benachrichtigen, wenn ein Fragebogen abgeschlossen oder ein Fit neu
berechnet wird, statt Polling zu betreiben. Nur für Organisationen nützlich, die
die API bereits nutzen, daher eingeschränkte Reichweite.

**7. Claude MCP** — einen MCP-Server als Ergänzung zur öffentlichen API
(V2-Punkt #9) bereitstellen, um die FitRadarHR-Aktivität direkt von Claude aus
einzusehen (Fragebogenstatus, Fit-Ergebnisse, zu versendende Erinnerungen),
ohne die Website zu öffnen. Technisch ein dünner Wrapper um die bestehende
v1-API: gleiche organisationsbezogene API-Schlüssel-Authentifizierung, gleiche
Minimierungsregeln (niemals rohe Big-Five-Werte, nur abgeleitete Ergebnisse).
Der kritische Punkt ist nicht der Datenzugriff, sondern dessen Nutzung durch das
Modell: bewusst enge, strukturierte Tools (ausstehende Fragebögen auflisten,
Fit-Zusammenfassung einer Stelle oder eines Teams abrufen) statt eines einzigen
offenen Tools nach dem Muster „stelle jede beliebige Frage zu dieser
Organisation“, damit der Agent nicht in Richtung einer klaren Empfehlung
abdriftet — im Widerspruch zur Regel „niemals eine automatisierte
Entscheidungsbewertung“. Bescheidene Reichweite (Early-Adopter-Publikum/
Organisationen, die bereits mit KI-Tools vertraut sind), begrenzter Aufwand
durch Wiederverwendung der bestehenden API.

**8. Anonymisierte Benchmarks** — Vergleich der OCEAN-Verteilung einer
Organisation mit einem aggregierten organisationsübergreifenden Durchschnitt,
opt-in und anonymisiert. Echter analytischer Wert, aber geringe Konfidenz: wirft
Fragen der Daten-Governance auf (organisationsübergreifende Aggregation,
Einwilligung), die vor jeder Entwicklung noch geklärt werden müssen.

**9. Native Konnektoren** — über die generische API hinaus würden
vorgefertigte Integrationen mit spezifischen HRIS/ATS-Systemen die
Adoptionsreibung verringern. Geringste Konfidenz der Liste: Nachfrage noch
nicht durch einen realen Kundenanwendungsfall validiert, hoher Aufwand (ein
Konnektor = ein eigenständiges Projekt). Nur umsetzen, wenn eine Organisation
einen konkreten Bedarf äußert.

## Was niemals umgesetzt wird

Siehe die [Anti-Metriken](https://github.com/adams43360/FitRadarHR/blob/main/docs/product/metrics.md)
und die nicht verhandelbaren Regeln des Projekts: keine Lebenslaufanalyse, keine
automatisierte Entscheidungsbewertung, keine wissenschaftlich nicht validierte
Typologie (MBTI…).

---

*Diese Roadmap ist indikativ und wird anhand des Nutzerfeedbacks laufend neu
bewertet — das in die App integrierte [Feedback-Widget](../index.md) fließt
direkt in diese Priorisierung ein.*
