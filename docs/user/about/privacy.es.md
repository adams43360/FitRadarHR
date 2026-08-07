# Privacidad y RGPD

FitRadarHR se diseñó con el cumplimiento del RGPD como restricción de diseño, no como una capa añadida a posteriori.

## Datos recopilados

| Dato | Quién | Duración | Base legal |
|---|---|---|---|
| Email, nombre, apellidos (usuarios de la cuenta) | Usuarios de la cuenta | Duración de la cuenta | Contrato |
| Email, nombre, apellidos (personas evaluadas) | Candidatos / colaboradores | Duración de la organización | Interés legítimo + consentimiento |
| Respuestas al cuestionario (en bruto) | Personas evaluadas | Eliminadas tras el cálculo | Consentimiento |
| Puntuaciones Big Five | Personas evaluadas | Duración de la organización | Consentimiento |
| Informes de fit | Personas evaluadas | Duración de la organización | Interés legítimo |

## Consentimiento explícito

Antes de responder al cuestionario, cada persona lee y acepta explícitamente un aviso de información. Este consentimiento es:
- Registrado con marca temporal y versión del texto mostrado
- Inmutable (no modificable a posteriori)
- Revocable (la persona puede solicitar el borrado de sus datos)

## Derecho al borrado

A petición de una persona evaluada, sus datos personales (nombre, apellidos, email) se **anonimizan** (`[eliminado]`). Los informes de fit asociados se conservan sin vínculo nominativo, con fines de trazabilidad organizativa.

## Registro de auditoría

Todas las acciones sensibles (consulta de un informe, exportación PDF, envío de enlace, borrado) se registran en un registro inmutable — conforme a los requisitos del EU AI Act para los sistemas de alto riesgo (véase [el EU AI Act y la contratación](eu-ai-act.md) para el calendario y el detalle de las obligaciones).

## Medición de audiencia

FitRadarHR utiliza [Matomo](https://matomo.org), autoalojado en la misma infraestructura, para conocer el volumen de uso y las funcionalidades más utilizadas. Esta medición está configurada bajo **exención de consentimiento de la CNIL**: sin cookies, IP anonimizada, ningún dato personal recopilado, ningún dato transmitido a un tercero. Por tanto, no se muestra ningún banner de consentimiento para este uso — a distinguir del consentimiento explícito requerido para el cuestionario Big Five (véase más arriba), que permanece inalterado.

## Alojamiento

FitRadarHR es autoalojado. Usted controla dónde residen sus datos. Ningún dato se transmite a terceros.

!!! info "Autoalojamiento"
    Al desplegar FitRadarHR en su propio VPS, usted es responsable del tratamiento de los datos personales (rol de responsable del tratamiento). Recuerde actualizar su registro de actividades de tratamiento.
