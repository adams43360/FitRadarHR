# Privacy and GDPR

FitRadarHR was designed with GDPR compliance as a design constraint, not a layer added after the fact.

## Data collected

| Data | Who | Duration | Legal basis |
|---|---|---|---|
| Email, first name, last name (account users) | Account users | Duration of the account | Contract |
| Email, first name, last name (evaluated people) | Candidates / employees | Duration of the organization | Legitimate interest + consent |
| Questionnaire answers (raw) | Evaluated people | Deleted after calculation | Consent |
| Big Five scores | Evaluated people | Duration of the organization | Consent |
| Fit reports | Evaluated people | Duration of the organization | Legitimate interest |

## Explicit consent

Before answering the questionnaire, each person reads and explicitly accepts an information notice. This consent is:
- Recorded with a timestamp and the version of the text displayed
- Immutable (cannot be modified afterward)
- Revocable (the person can request erasure of their data)

## Right to erasure

At the request of an evaluated person, their personal data (first name, last name, email) is **anonymized** (`[deleted]`). Associated fit reports are kept without a nominative link, for organizational traceability.

## Audit log

All sensitive actions (viewing a report, PDF export, sending a link, erasure) are recorded in an immutable log — in line with EU AI Act requirements for high-risk systems (see [EU AI Act and recruitment](eu-ai-act.md) for the timeline and the detail of obligations).

## Audience measurement

FitRadarHR uses [Matomo](https://matomo.org), self-hosted on the same infrastructure, to know usage volume and the most used features. This measurement is configured under **CNIL consent exemption**: no cookie, anonymized IP, no personal data collected, no data transmitted to a third party. No consent banner is therefore displayed for this use — to be distinguished from the explicit consent required for the Big Five questionnaire (see above), which remains unchanged.

## Hosting

FitRadarHR is self-hosted. You control where your data resides. No data is transmitted to third parties.

!!! info "Self-hosting"
    By deploying FitRadarHR on your own VPS, you are responsible for the processing of personal data (data controller role). Remember to update your records of processing activities.
