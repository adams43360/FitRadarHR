# Gestión de departamentos

Un **departamento** representa una entidad organizativa (ej. I+D, Ventas, Finanzas) a la que puede vincular puestos y equipos.

## Qué puede hacer

- Crear un departamento con un nombre en FR y un nombre en EN (opcional)
- Vincular puestos y equipos a un departamento
- Consultar la ficha del departamento — lista de puestos y equipos asociados
- Archivar un departamento cuando ya no esté activo

## Acceso

El enlace **Departamentos** está disponible en la barra de navegación para los usuarios de RR. HH.

## Vinculación de puestos / equipos

Al crear o modificar un puesto, puede seleccionar un departamento en la lista desplegable. Lo mismo para los equipos.

Un puesto también puede vincularse directamente a un **equipo objetivo** (subconjunto de un departamento). En ese caso, el informe de perfil de un candidato muestra automáticamente el Fit de Equipo correspondiente junto al Fit de Puesto.

!!! tip "Crear un departamento al vuelo"
    Desde el formulario de creación de un puesto o un equipo, un enlace **+ Crear nuevo departamento** permite crear el departamento sin salir del formulario en curso.

## Jerarquía organizativa

```
Departamento  (ej. Investigación y Desarrollo)
  ├── Equipo(s)  (ej. Backend Team, Data Team)
  └── Puesto(s)   (ej. Desarrollador Backend → vinculado a Backend Team)
```

Esta estructura permite comparar el fit de un candidato con el perfil objetivo del puesto **y** con los miembros actuales del equipo, en una sola lectura.
