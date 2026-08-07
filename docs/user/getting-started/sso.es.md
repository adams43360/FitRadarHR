# Inicio de sesión SSO (Keycloak / OIDC)

FitRadarHR permite a cada organización conectar su propio proveedor de identidad (Keycloak o cualquier IdP compatible con OIDC), para que sus usuarios inicien sesión con sus credenciales corporativas habituales en lugar de una contraseña específica.

!!! note "El SSO se añade, no sustituye"
    Activar el SSO nunca impide el inicio de sesión existente por email/contraseña. Es una opción adicional — útil para evitar un bloqueo si su proveedor de identidad no está disponible.

## Configurar el SSO de su organización

Un usuario de RR. HH. accede a la pantalla de configuración desde el enlace **SSO** de la barra de navegación.

| Campo | Descripción |
|---|---|
| **Nombre para mostrar** | Se muestra en el botón de inicio de sesión (ej. «Acme Corp SSO») |
| **Identificador de conexión** | Identificador único utilizado en la URL de inicio de sesión SSO — a comunicar a sus usuarios |
| **URL del emisor OIDC** | Endpoint de descubrimiento de su proveedor de identidad (Keycloak, Okta, Azure AD…) |
| **Client ID / Client secret** | Credenciales de la aplicación registrada ante su IdP |
| **Activado** | Desactiva el SSO sin perder la configuración |

El **client secret** nunca se vuelve a mostrar tras su introducción — deje el campo vacío al modificar la configuración para conservarlo.

## Iniciar sesión mediante SSO

En la página de inicio de sesión, un usuario hace clic en «**Iniciar sesión a través de su organización (SSO)**», introduce el identificador de conexión de su organización, y a continuación se le redirige al IdP configurado.

En el primer inicio de sesión correcto, se crea automáticamente una cuenta (rol Manager por defecto, modificable después por un usuario de RR. HH.) — no es necesario ningún registro manual. Si ya existe una cuenta con la misma dirección de email en la organización, el inicio de sesión SSO se vincula directamente a ella.

!!! warning "Aislamiento de las organizaciones"
    Cada organización configura su propio IdP — ninguna configuración se comparte entre organizaciones. Un email ya utilizado en otra organización no puede iniciar sesión a través del SSO de una organización diferente.
