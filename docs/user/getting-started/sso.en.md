# SSO login (Keycloak / OIDC)

FitRadarHR lets each organization connect its own identity provider (Keycloak or any OIDC-compatible IdP), so its users can log in with their usual company credentials rather than a dedicated password.

!!! note "SSO is additive, it doesn't replace"
    Enabling SSO never prevents the existing email/password login. It's an additional option — useful to avoid being locked out if your identity provider is unavailable.

## Configuring your organization's SSO

An HR user accesses the configuration screen from the **SSO** link in the navigation bar.

| Field | Description |
|---|---|
| **Display name** | Shown on the login button (e.g. "Acme Corp SSO") |
| **Login identifier** | Unique identifier used in the SSO login URL — to share with your users |
| **OIDC issuer URL** | Discovery endpoint of your identity provider (Keycloak, Okta, Azure AD…) |
| **Client ID / Client secret** | Credentials of the application registered with your IdP |
| **Enabled** | Turns off SSO without losing the configuration |

The **client secret** is never shown again after entry — leave the field empty when editing to keep it unchanged.

## Logging in via SSO

On the login page, a user clicks **"Log in via your organization (SSO)"**, enters their organization's login identifier, then is redirected to the configured IdP.

On the first successful login, an account is automatically created (Manager role by default, editable later by an HR user) — no manual sign-up is needed. If an account already exists with the same email address in the organization, the SSO login attaches to it directly.

!!! warning "Organization isolation"
    Each organization configures its own IdP — no configuration is shared between organizations. An email already used in another organization cannot log in via a different organization's SSO.
