# El EU AI Act y la contratación

!!! danger "Esto no es asesoramiento jurídico"
    Esta página tiene un propósito informativo. El calendario y el contenido del EU AI Act han cambiado varias veces desde su adopción y pueden seguir cambiando. Para cualquier decisión de cumplimiento que afecte a su organización, consulte a un jurista o a su DPO — FitRadarHR no sustituye ese asesoramiento.

## Por qué la contratación está afectada

El **EU AI Act** (Reglamento (UE) 2024/1689) clasifica los sistemas de IA utilizados para la contratación y la gestión de recursos humanos — selección de candidatos, promoción, asignación de tareas, rescisión de contrato, evaluación del rendimiento — en la categoría de **«alto riesgo»** (Anexo III). Es esta clasificación, y no el hecho de usar tal o cual herramienta concreta, la que activa las obligaciones más pesadas del reglamento.

FitRadarHR se diseñó anticipando esta clasificación desde el principio — véase la regla «nunca una puntuación de decisión automática» en los [principios del producto](../index.md) — más que como una reacción a un plazo normativo.

## En qué punto está el calendario (actualizado a 7 de agosto de 2026)

El calendario ha cambiado recientemente. En un principio, las obligaciones de «alto riesgo» debían aplicarse a partir del **2 de agosto de 2026**. Un paquete de simplificación (el *Digital Omnibus AI*) modificó este calendario:

- Acuerdo político provisional entre el Parlamento Europeo y el Consejo: **7 de mayo de 2026**
- Adopción formal por el Parlamento Europeo: **16 de junio de 2026**
- Aprobación final por el Consejo de la UE: **29 de junio de 2026**, seguida de la publicación en el Diario Oficial de la UE

Resultado: las obligaciones de «alto riesgo» para los sistemas autónomos (incluidas las herramientas de RR. HH./contratación) se **posponen al 2 de diciembre de 2027**. Para los sistemas de IA de alto riesgo integrados en un producto más amplio, el plazo es el **2 de agosto de 2028**.

!!! info "Este aplazamiento no cambia lo que ya está en vigor"
    El aplazamiento afecta específicamente a las obligaciones vinculadas a la clasificación de «alto riesgo» (Anexo III). No suspende ni el RGPD, ni el derecho laboral francés, ni las prohibiciones de prácticas de IA ya en vigor desde febrero de 2025 (por ejemplo, el reconocimiento de emociones en el lugar de trabajo, prohibido desde la entrada en aplicación del reglamento).

## Lo que ya se aplica, con independencia del AI Act

Dos marcos jurídicos ya regulan hoy la contratación asistida por una herramienta, sin esperar a diciembre de 2027:

**RGPD, artículo 22** — toda persona tiene derecho a no ser objeto de una decisión basada únicamente en un tratamiento automatizado que produzca efectos jurídicos o le afecte significativamente, cuando no haya intervención humana. Esta es la razón estructural por la que FitRadarHR nunca muestra una puntuación de decisión («recomendado» / «no recomendado»): véase [privacidad y RGPD](privacy.md).

**Código de Trabajo francés, artículos L.1221-8 y L.1221-9** — un candidato debe ser informado, antes de su implementación, de las técnicas y métodos utilizados para su evaluación y contratación, incluso cuando un tratamiento automatizado contribuya a ello. Los resultados obtenidos deben permanecer confidenciales y el candidato puede solicitar que se le comunique la información que le concierne.

## Lo que exigirá la clasificación de «alto riesgo» a partir de 2027

Una vez que las obligaciones sean aplicables, un sistema de IA de alto riesgo utilizado para la contratación deberá disponer, entre otras cosas, de:

- un sistema de gestión de riesgos documentado a lo largo de todo el ciclo de vida de la herramienta,
- una **supervisión humana** efectiva — la persona que utiliza la herramienta debe poder comprender sus límites y no confiar en ella ciegamente,
- **trazabilidad** (registro) de los usos,
- documentación técnica y una evaluación de conformidad antes de su comercialización,
- información clara para las personas afectadas.

## Cómo se sitúa FitRadarHR en este marco

Estos principios no son nuevos en el producto — coinciden con decisiones de diseño ya tomadas:

| Obligación futura (Anexo III) | Lo que ya hace FitRadarHR |
|---|---|
| Supervisión humana documentada | Ninguna puntuación de decisión automática — el producto informa, nunca decide |
| Trazabilidad de los usos | Registro de auditoría inmutable de consultas, exportaciones y envíos de enlaces |
| Minimización / consentimiento | Consentimiento explícito con marca temporal antes del cuestionario, derecho al borrado |
| Instrumento validado científicamente | Cuestionario Big Five (IPIP), nunca análisis de CV ni tipología no validada — véase [Big Five vs MBTI](big-five-vs-mbti.md) |

Esto no exime a su organización de su propio análisis de cumplimiento: la clasificación de «alto riesgo» se refiere al uso que *usted* hace de la herramienta en su proceso de contratación, no solo a la herramienta en sí.

## Fuentes

- [Digital Omnibus AI — aplazamiento de las obligaciones de alto riesgo a diciembre de 2027 (Gibson Dunn)](https://www.gibsondunn.com/eu-ai-act-omnibus-agreement-postponed-high-risk-deadlines-and-other-key-changes/){ target="_blank" }
- [EU Nears Approval of Agreement to Delay Rules for AI Use in Employment Decisions (Ogletree Deakins)](https://ogletree.com/insights-resources/blog-posts/eu-nears-approval-of-agreement-to-delay-rules-for-ai-use-in-employment-decisions/){ target="_blank" }
- [HR Tools and Artificial Intelligence: Europe Delays High-Risk Obligations to December 2027 (actuIA)](https://www.actuia.com/en/news/hr-tools-and-artificial-intelligence-europe-delays-high-risk-obligations-to-december-2027/){ target="_blank" }
- Reglamento (UE) 2024/1689 (EU AI Act), Anexo III
- Código de Trabajo francés, artículos L.1221-8 y L.1221-9
- Reglamento (UE) 2016/679 (RGPD), artículo 22
