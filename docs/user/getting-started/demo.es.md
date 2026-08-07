# Probar la demo

FitRadarHR ofrece un **entorno de demostración público**: basta un clic para explorar
la herramienta con datos realistas, sin crear una cuenta.

## Acceder a la demo

En la página de inicio de sesión o en la página de inicio, haga clic en **✨ Probar la demo**.
Se conectará inmediatamente a la cuenta de demostración, con el rol de Responsable de RR. HH.

!!! info "No se requiere registro"
    La cuenta demo no tiene contraseña: el botón es la única forma de acceder a ella.

## Qué contiene la demo

El entorno simula **Nexatech**, una editorial de software ficticia de un centenar de personas:

- 6 departamentos (Ingeniería, Producto y Diseño, Comercial, Customer Success, Finanzas, RR. HH.)
- 10 equipos con sus miembros y sus perfiles OCEAN completados
- 9 puestos abiertos con perfiles Big Five objetivo y clasificaciones de fit
- Candidatos en proceso de evaluación (cuestionarios completados, pendientes o en curso)
- Informes de fit de puesto y de equipo consultables y exportables a PDF

Los perfiles de los equipos son deliberadamente contrastados (un equipo comercial extravertido,
un equipo de finanzas muy responsable…) para que las señales de complementariedad sean claras.

## Las reglas del entorno de demostración

!!! warning "Datos ficticios, reiniciados cada 24 h"
    Todos los datos son **ficticios y deterministas**: se eliminan y se recrean
    de forma idéntica cada día. No introduzca ningún dato real en la demo.

Además, algunas funciones se adaptan:

- **No se envía ningún email** desde la demo. Al enviar un cuestionario,
  el enlace de realización se muestra en pantalla — puede abrirlo usted mismo para probar
  el recorrido del candidato de principio a fin (consentimiento RGPD incluido).
- **El borrado RGPD está desactivado** (ya que los datos son ficticios y compartidos entre
  todos los visitantes).

## ¿Quiere ir más allá?

Cree su propia cuenta gratuita ([ver Crear una cuenta](signup.md)) o
[contáctenos](mailto:contact@fitradarhr.com) para un entorno de prueba dedicado a su equipo.

---

## Para administradores (autoalojamiento)

El modo demo se configura mediante el entorno:

```bash
# .env
DEMO_MODE=True
```

```bash
# Crear o reiniciar la organización demo
python manage.py seed_demo

# En desarrollo (Docker)
make seed-demo
```

En producción, el servicio `demo-reset` de `docker-compose.yml` reproduce el seed cada 24 h:

```bash
docker compose -f docker/docker-compose.prod.yml --profile demo up -d
```
