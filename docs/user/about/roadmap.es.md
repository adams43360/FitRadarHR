# Hoja de ruta pública

La V1 de FitRadarHR está completa (epics E1–E8 entregados) y la **V2 está
totalmente entregada** (9/9 elementos). Esta página también presenta las
posibles pistas para una **V3**, priorizadas con el método **RICE** — con total
transparencia, como el resto del proyecto.

## Cómo leer la puntuación RICE

**RICE = (Reach × Impact × Confidence) / Effort**

- **Reach (alcance)** — cuántos usuarios se ven afectados por trimestre (escala 1–10)
- **Impact (impacto)** — efecto sobre la North Star (informes consultados / semana): 0,5 = bajo, 1 = medio, 2 = alto, 3 = masivo
- **Confidence (confianza)** — confianza en las estimaciones: 50 % / 80 % / 100 %
- **Effort (esfuerzo)** — carga en semanas-persona

## Priorización V2

| # | Funcionalidad | Reach | Impact | Conf. | Effort | Puntuación RICE | Estado |
|---|---|---|---|---|---|---|---|
| 1 | Recordatorios automáticos de cuestionario | 8 | 2 | 80 % | 1 | **12.8** | ✅ Entregado |
| 2 | Invitación de managers a la organización | 7 | 2 | 80 % | 2 | **5.6** | ✅ Entregado |
| 3 | Comparación de candidatos para un puesto | 6 | 2 | 80 % | 2 | **4.8** | ✅ Entregado |
| 4 | Importación CSV de personas | 6 | 1 | 100 % | 1.5 | **4.0** | ✅ Entregado |
| 5 | Repetición y seguimiento longitudinal | 5 | 2 | 50 % | 2 | **2.5** | ✅ Entregado |
| 6 | Cohortes de retención en Analytics | 4 | 1 | 80 % | 1.5 | **2.1** | ✅ Entregado |
| 7 | SSO Keycloak / OIDC | 3 | 1 | 80 % | 3 | **0.8** | ✅ Entregado |
| 8 | Traducciones ES / DE | 2 | 1 | 80 % | 2 | **0.8** | ✅ Entregado |
| 9 | API pública (solo lectura) | 2 | 1 | 50 % | 3 | **0.3** | ✅ Entregado |

## Los argumentos, elemento por elemento

**1. Recordatorios automáticos** — el funnel de Analytics muestra que la mayor
parte de la pérdida se produce entre el envío del enlace y el inicio. Un
recordatorio a los 3 días ataca directamente la tasa de finalización, con un
esfuerzo mínimo. Mejor relación valor/esfuerzo de la lista.

**2. Invitación de managers** — hoy una organización vive con una sola cuenta
de RR. HH. la mayor parte del tiempo. Cada manager invitado es un consumidor
adicional de informes: es la palanca de «referral» del funnel AARRR.

**3. Comparación de candidatos** — el ranking de fit ya existe en la ficha del
puesto; la vista lado a lado (radares superpuestos, complementariedades) es la
continuación natural que pide el caso de uso de contratación. Fuerte impacto
en la consulta de informes.

**4. Importación CSV** — fricción de onboarding: introducir 50 colaboradores a
mano desanima. Impacto indirecto en la North Star pero confianza máxima
(necesidad evidente).

**5. Repetición** — los perfiles Big Five evolucionan lentamente, pero
evolucionan; útil para la movilidad interna. Confianza del 50 %: la necesidad
real aún debe validarse en discovery.

**6. Cohortes de retención** — profundiza la página Analytics para
organizaciones maduras. Reservado a organizaciones ya activadas, por tanto
alcance más bajo.

**7. SSO / OIDC** — necesario para organizaciones más grandes; alcance más
bajo en el público objetivo actual (pymes/scale-ups) pero un IdP por
organización, aditivo a la contraseña (nunca un reemplazo), hace que el coste
de mantenimiento sea aceptable. Entregado, aún no validado con un IdP real en
producción.

**8. Traducciones ES/DE** — paridad completa, incluido el cuestionario IPIP, no
solo la interfaz. El cuestionario alemán está íntegramente basado en la
traducción oficial de IPIP (100/100 ítems); el español lo está para la versión
corta (50 ítems), pero la versión larga introduce una zona traducida
internamente, a falta de una fuente oficial publicada — véase
`docs/user/about/big-five.md`.

**9. API pública (solo lectura)** — valor real pero no diferenciador hoy.
Entregada con un alcance deliberadamente restringido: puestos/equipos,
personas + estado del cuestionario, resultados de fit — nunca los perfiles Big
Five en bruto (minimización RGPD). Autenticación por clave API por
organización.

## Priorización V3

Los elementos #1 y #2 están entregados; los elementos 3 a 8 siguen siendo
candidatos no decididos.

| # | Funcionalidad | Reach | Impact | Conf. | Effort | Puntuación RICE | Estado |
|---|---|---|---|---|---|---|---|
| 1 | Fit inverso — mejores puestos para una persona | 5 | 2 | 90 % | 1.5 | **6.0** | ✅ Entregado |
| 2 | Monetización (plan gratuito → suscripción) | 8 | 3 | 80 % | 5 | **3.84** | ✅ Entregado |
| 3 | Mapa de carencias de un equipo | 5 | 2 | 60 % | 2 | **3.0** | ✅ Entregado |
| 4 | Portal candidato/colaborador (acceso a su perfil) | 6 | 2 | 70 % | 3 | **2.8** | Candidato |
| 5 | Dosier de cumplimiento AI Act exportable | 3 | 2 | 70 % | 2 | **2.1** | Candidato |
| 6 | Webhooks (complemento de la API pública) | 3 | 1 | 70 % | 2 | **1.05** | Candidato |
| 7 | MCP Claude — consultar su actividad fuera del sitio | 2 | 1 | 60 % | 2 | **0.6** | Candidato |
| 8 | Benchmarks anonimizados entre organizaciones | 4 | 1 | 40 % | 4 | **0.4** | Candidato |
| 9 | Conectores nativos (Workday, BambooHR, Personio…) | 3 | 2 | 30 % | 5 | **0.36** | Candidato |

### Los argumentos, elemento por elemento

**1. Fit inverso** — hoy se parte de un puesto para clasificar personas; lo
contrario (partir de una persona y ver los puestos abiertos que mejor le
encajan) sirve a la movilidad interna, sin recopilar ningún dato adicional: es
una nueva vista sobre el motor de fit existente. Mejor relación valor/esfuerzo
de la lista. Entregado: ningún cálculo nuevo, reutiliza los resultados de fit
ya producidos por el motor (E5).

**2. Monetización** — es la razón misma del paso a la licencia Fair Source
(FSL-1.1-MIT): Damien contemplaba explícitamente una prueba gratuita seguida
de una suscripción. Alcance elevado (afecta potencialmente a todas las
organizaciones a largo plazo) e impacto fuerte (es el modelo de negocio), pero
esfuerzo importante: integración con Stripe, cuotas por plan, pantallas de
facturación, gestión de excesos. Entregado: un único plan de pago
(39 €/mes, Stripe Checkout + Customer Portal) y un plan gratuito permanente
(umbral único de 25 personas — puestos y cuestionarios libres). El modelo
inicial de prueba de 14 días se abandonó en favor del freemium: más simple de
entender, sin presión artificial para convertir.

**3. Mapa de carencias de un equipo** — amplía la complementariedad ya
calculada: a partir del perfil agregado de un equipo, hacer visibles las
dimensiones OCEAN infrarrepresentadas. Se mantiene dentro del alcance del
producto — presentado como pistas a explorar para un plan de contratación,
nunca como una recomendación tajante (coherente con la regla «nunca una
puntuación de decisión automática»). Entregado: accesible directamente desde
la ficha del equipo, sin seleccionar a una persona — véase
`docs/user/reports/team-gaps.md`.

**4. Portal candidato/colaborador** — hoy solo RR. HH./managers consultan los
informes. Dar a la propia persona acceso a su perfil e informe refuerza el
principio «human in the loop» y el derecho de acceso RGPD ya implementado
(E8). Confianza media: requiere un nuevo modelo de acceso para registros
`Person` que no necesariamente tienen una cuenta `User`.

**5. Dosier de cumplimiento AI Act exportable** — una exportación (PDF/JSON)
del «dosier de trazabilidad» — quién consultó qué, supervisión humana
documentada — para las organizaciones que deben justificar su cumplimiento
bajo la clasificación de «alto riesgo». Prolonga directamente E8, se dirige
sobre todo a organizaciones más reguladas (alcance más bajo).

**6. Webhooks** — complemento natural de la API pública (elemento #9 de V2):
notificar a un sistema externo cuando se completa un cuestionario o se
recalcula un fit, en lugar de hacer polling. Útil solo para organizaciones que
ya usan la API, por tanto alcance restringido.

**7. MCP Claude** — exponer un servidor MCP como complemento de la API pública
(elemento #9 de V2), para consultar la actividad de FitRadarHR directamente
desde Claude (estado de cuestionarios, resultados de fit, recordatorios a
enviar) sin abrir el sitio. Técnicamente un wrapper ligero alrededor de la API
v1 existente: misma autenticación por clave API con alcance de organización,
mismas reglas de minimización (nunca las puntuaciones Big Five en bruto, solo
resultados derivados). El punto de atención no es el acceso a los datos sino
el uso que hace de ellos el modelo: herramientas deliberadamente estrechas y
estructuradas (listar cuestionarios pendientes, obtener el resumen de fit de
un puesto o equipo) en lugar de una única herramienta abierta tipo «haz
cualquier pregunta sobre esta organización», para no dejar que el agente
derive hacia una recomendación tajante — contrario a la regla «nunca una
puntuación de decisión automática». Alcance modesto (público early-adopter/
organizaciones ya cómodas con herramientas de IA), esfuerzo limitado por la
reutilización de la API existente.

**8. Benchmarks anonimizados** — comparar la distribución OCEAN de una
organización con una media agregada entre organizaciones, de forma opt-in y
anonimizada. Valor analítico real pero confianza baja: plantea cuestiones de
gobernanza de datos (agregación cross-tenant, consentimiento) que aún deben
definirse antes de cualquier desarrollo.

**9. Conectores nativos** — más allá de la API genérica, integraciones
preconstruidas con SIRH/ATS específicos reducirían la fricción de adopción.
Confianza más baja del lote: demanda aún no validada por un caso de uso real
de cliente, esfuerzo elevado (un conector = un proyecto en sí mismo). A
reservar si una organización expresa una necesidad concreta.

## Lo que nunca se hará

Véanse las [antimétricas](https://github.com/adams43360/FitRadarHR/blob/main/docs/product/metrics.md)
y las reglas innegociables del proyecto: sin análisis de CV, sin puntuación de
decisión automática, sin tipología no validada científicamente (MBTI…).

---

*Esta hoja de ruta es orientativa y se reevalúa según los comentarios de los
usuarios — el [widget de feedback](../index.md) integrado en la aplicación
alimenta directamente esta priorización.*
