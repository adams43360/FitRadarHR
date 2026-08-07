# API pública (solo lectura)

FitRadarHR expone una API JSON de solo lectura, pensada para conectar una herramienta externa (ATS, SIRH…) sin intervención manual: puestos, equipos, personas y resultados de fit de su organización.

!!! warning "Nunca los perfiles Big Five en bruto"
    Por decisión de producto (minimización de los datos transmitidos a terceros), la API **nunca expone** las puntuaciones Big Five en bruto (Apertura, Responsabilidad, Extraversión, Amabilidad, Neuroticismo) de una persona. Solo están disponibles resultados derivados (estado del cuestionario, puntuaciones de fit).

## Generar una clave API

Un usuario de RR. HH. accede a la pantalla de gestión desde el enlace **API** de la barra de navegación (`/settings/api/`).

1. Introduzca un nombre para identificar la integración (ej. «Integración ATS Greenhouse»)
2. Haga clic en **Generar**
3. Copie la clave mostrada **inmediatamente** — nunca volverá a ser visible después (solo su prefijo permanece visible en la lista, para reconocerla)

Una clave puede **revocarse** en cualquier momento desde la misma pantalla; la revocación es inmediata y definitiva.

## Autenticación

Cada solicitud debe incluir la siguiente cabecera:

```
Authorization: Api-Key <su_clave>
```

```bash
curl -H "Authorization: Api-Key frk_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" \
  https://su-dominio.example/api/v1/positions/
```

Una clave ausente, inválida o revocada devuelve un error `401`:

```json
{"error": "invalid_api_key", "detail": "Invalid or revoked API key."}
```

Una clave siempre está limitada a **una sola organización** — es imposible acceder a los datos de otra organización, sea cual sea la solicitud.

## Endpoints disponibles

Todos los endpoints son de **solo lectura (GET únicamente)**.

| Endpoint | Descripción |
|---|---|
| `GET /api/v1/positions/` | Lista de puestos (filtro opcional `?status=active\|archived`) |
| `GET /api/v1/positions/{id}/` | Detalle de un puesto |
| `GET /api/v1/teams/` | Lista de equipos |
| `GET /api/v1/teams/{id}/` | Detalle de un equipo (incluye el número de miembros activos) |
| `GET /api/v1/people/` | Lista de personas (filtro opcional `?person_type=candidate\|collaborator`) |
| `GET /api/v1/people/{id}/` | Detalle de una persona — estado del cuestionario e indicador «perfil completado» (nunca las puntuaciones) |
| `GET /api/v1/fit-results/positions/` | Resultados de fit de Puesto (filtros opcionales `?position_id=` y `?person_id=`) |
| `GET /api/v1/fit-results/teams/` | Resultados de fit de Equipo, incluida la complementariedad (filtros opcionales `?team_id=` y `?person_id=`) |

## Paginación

Las listas están paginadas: `?page=2&page_size=50` (tamaño máximo de página: 100). Formato de respuesta:

```json
{
  "count": 128,
  "page": 1,
  "num_pages": 3,
  "page_size": 50,
  "results": [ ... ]
}
```
