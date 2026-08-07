# SSO-Anmeldung (Keycloak / OIDC)

FitRadarHR ermöglicht es jeder Organisation, ihren eigenen Identitätsanbieter (Keycloak oder einen beliebigen OIDC-kompatiblen IdP) anzubinden, damit sich Nutzerinnen und Nutzer mit ihren gewohnten Unternehmenszugangsdaten anmelden können, statt mit einem dedizierten Passwort.

!!! note "SSO ergänzt, ersetzt aber nicht"
    Die Aktivierung von SSO verhindert nie die bestehende Anmeldung per E-Mail/Passwort. Es ist eine zusätzliche Option — nützlich, um eine Aussperrung zu vermeiden, falls Ihr Identitätsanbieter nicht verfügbar ist.

## SSO Ihrer Organisation konfigurieren

Eine HR-Person greift über den Link **SSO** in der Navigationsleiste auf den Konfigurationsbildschirm zu.

| Feld | Beschreibung |
|---|---|
| **Anzeigename** | Wird auf dem Anmelde-Button angezeigt (z. B. „Acme Corp SSO“) |
| **Login-Kennung** | Eindeutige Kennung, die in der SSO-Anmelde-URL verwendet wird — an Ihre Nutzer weiterzugeben |
| **OIDC-Issuer-URL** | Discovery-Endpunkt Ihres Identitätsanbieters (Keycloak, Okta, Azure AD…) |
| **Client-ID / Client-Secret** | Zugangsdaten der bei Ihrem IdP registrierten Anwendung |
| **Aktiviert** | Schaltet SSO ab, ohne die Konfiguration zu verlieren |

Das **Client-Secret** wird nach der Eingabe nie wieder angezeigt — lassen Sie das Feld beim Bearbeiten leer, um es unverändert beizubehalten.

## Anmeldung über SSO

Auf der Anmeldeseite klickt eine Nutzerin/ein Nutzer auf „**Über Ihre Organisation anmelden (SSO)**“, gibt die Login-Kennung der Organisation ein und wird anschließend zum konfigurierten IdP weitergeleitet.

Bei der ersten erfolgreichen Anmeldung wird automatisch ein Konto erstellt (standardmäßig Rolle Manager, später von einer HR-Person änderbar) — keine manuelle Registrierung erforderlich. Falls bereits ein Konto mit derselben E-Mail-Adresse in der Organisation existiert, wird die SSO-Anmeldung direkt damit verknüpft.

!!! warning "Isolierung der Organisationen"
    Jede Organisation konfiguriert ihren eigenen IdP — keine Konfiguration wird zwischen Organisationen geteilt. Eine bereits in einer anderen Organisation verwendete E-Mail-Adresse kann sich nicht über das SSO einer anderen Organisation anmelden.
