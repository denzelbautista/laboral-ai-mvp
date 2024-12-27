# Documentación de la fase B2B - Laboral.AI

## Descripción del Proyecto

**Laboral.AI** es una plataforma B2B que conecta empresas con empleados utilizando inteligencia artificial. Este repositorio contiene el MVP (Producto Mínimo Viable), diseñado para gestionar empleos y usuarios asociados a empresas. Las funcionalidades principales incluyen:

- Registro y login de empresas.
- Creación, listado, modificación y eliminación de empleos.

### Autores
- **Diego Randolp Quispe Apaza** - Computer Science - UTEC
- **Denzel Ysai Bautista Rodriguez** - Computer Science - UTEC

### Tecnologías Utilizadas

El proyecto emplea las siguientes tecnologías y herramientas:

- **Backend:** Python con Flask, gestionando la lógica de negocio y las APIs REST.
- **Base de Datos:** PostgreSQL alojado en AWS RDS para una solución escalable.
- **Frontend:** HTML, CSS y JavaScript para la interfaz de usuario.
- **Despliegue:** Vercel para un despliegue rápido, sencillo y eficaz.
- **Autenticación:** Flask-Login para la gestión de usuarios y sesiones.
- **ORM:** SQLAlchemy para interactuar con la base de datos de forma eficiente.

El objetivo principal del MVP es simplificar el flujo de trabajo de empresas que publican empleos, permitiéndoles gestionar sus vacantes y obtener talento adecuado.

---

## Guía de Ejecución

Sigue los pasos a continuación para ejecutar el backend localmente:

### 1. Clonar el Repositorio

```bash
$ git clone https://github.com/denzelbautista/laboral-ai-mvp
$ cd laboral-ai-mvp
```

### 2. Crear el Entorno Virtual

```bash
$ python3 -m venv .venv
```

### 3. Activar el Entorno Virtual

**Linux/MacOS:**
```bash
$ source .venv/bin/activate
```

**Windows:**
```bash
$ .venv\Scripts\activate
```

### 4. Instalar las Dependencias

```bash
$ pip install -r requirements.txt
```

### 5. Ejecutar el Proyecto

```bash
$ python app.py
```

Esto iniciará el servidor Flask en `http://127.0.0.1:5000`.

---

## Esquema de la Base de Datos

### Tabla: `empresas`

| Campo               | Tipo         | Descripción                                    |
|---------------------|--------------|------------------------------------------------|
| `id`                | String(36)   | Identificador único de la empresa.            |
| `correo`            | String       | Correo electrónico de la empresa.             |
| `contraseña`        | String       | Contraseña encriptada.                        |
| `telefono`          | String       | Número de teléfono de contacto.               |
| `ruc`               | String       | Número de RUC único de la empresa.            |
| `nombre_empresa`    | String       | Nombre comercial de la empresa.               |
| `razon_social`      | String       | Razón social registrada.                      |
| `created_at`        | String       | Fecha de creación del registro.               |
| `updated_at`        | String       | Fecha de última actualización del registro.   |

### Tabla: `empleos`

| Campo                   | Tipo         | Descripción                                    |
|-------------------------|--------------|------------------------------------------------|
| `id`                    | String(36)   | Identificador único del empleo.               |
| `nombre`                | String       | Título o nombre del empleo.                   |
| `fecha_creacion`        | String       | Fecha de creación del empleo.                 |
| `fecha_final_postulacion` | String       | Fecha límite para postularse al empleo.       |
| `ubicación`             | String       | Ubicación del empleo.                         |
| `salario`               | String       | Salario ofrecido (puede ser texto).           |
| `vacantes`              | Integer      | Número de vacantes disponibles.               |
| `descripcion`           | Text         | Descripción detallada del empleo.             |
| `funciones`             | Text         | Funciones o responsabilidades del puesto.     |
| `beneficios`            | Text         | Beneficios ofrecidos por el empleo.           |
| `requisitos`            | Text         | Requisitos necesarios para postular.          |
| `tipo_contrato`         | String       | Tipo de contrato (Ej. Indefinido, Temporal).  |
| `modalidad_asistencia`  | String       | Modalidad de trabajo (Ej. Remoto, Presencial).|
| `empresa_id`            | String(36)   | Identificador de la empresa que ofrece el empleo.|

---

## Rutas Principales del Backend

### **1. Crear un Empleo**

- **Endpoint:** `/publicar-empleo`
- **Método:** `POST`
- **Autenticación:** Requerida
- **Payload:**
    ```json
    {
        "nombre": "Desarrollador Backend",
        "fecha_final_postulacion": "2025-01-15",
        "ubicacion": "Lima, Perú",
        "salario": "A convenir",
        "vacantes": 3,
        "descripcion": "Responsable del desarrollo y mantenimiento de APIs.",
        "funciones": "Diseñar, desarrollar y probar servicios backend.",
        "beneficios": "Seguro médico, línea de carrera.",
        "requisitos": "3 años de experiencia, conocimientos en Flask.",
        "tipo_contrato": "Indefinido",
        "modalidad_asistencia": "Remoto"
    }
    ```
- **Respuesta Exitosa:**
    ```json
    {
        "success": true,
        "message": "Empleo creado exitosamente",
        "empleo_id": "123e4567-e89b-12d3-a456-426614174000"
    }
    ```

---

### **2. Modificar un Empleo**

- **Endpoint:** `/empleo/editar`
- **Método:** `PATCH`
- **Autenticación:** Requerida
- **Payload:**
    ```json
    {
        "detalle_key": "123e4567-e89b-12d3-a456-426614174000",
        "empleo_datos": {
            "nombre": "Desarrollador Fullstack",
            "salario": "S/ 5000",
            "vacantes": 2
        }
    }
    ```
- **Respuesta Exitosa:**
    ```json
    {
        "success": true,
        "message": "Empleo actualizado exitosamente",
        "empleo_id": "123e4567-e89b-12d3-a456-426614174000"
    }
    ```

---

### **3. Listar un Empleo por ID**

- **Endpoint:** `/empleos/<id>`
- **Método:** `GET`
- **Respuesta Exitosa:**
    ```json
    {
        "success": true,
        "empleo": {
            "id": "123e4567-e89b-12d3-a456-426614174000",
            "nombre": "Desarrollador Backend",
            "descripcion": "Responsable del desarrollo y mantenimiento de APIs.",
            "salario": "A convenir",
            "vacantes": 3,
            "fecha_creacion": "2024-12-01",
            "fecha_final_postulacion": "2025-01-15",
            "ubicacion": "Lima, Perú",
            "funciones": "Diseñar, desarrollar y probar servicios backend.",
            "beneficios": "Seguro médico, línea de carrera.",
            "requisitos": "3 años de experiencia, conocimientos en Flask.",
            "tipo_contrato": "Indefinido",
            "modalidad_asistencia": "Remoto"
        }
    }
    ```

---

### **4. Listar Todos los Empleos**

- **Endpoint:** `/empleos_listar`
- **Método:** `GET`
- **Descripción:** 
  Obtiene una lista de todos los empleos registrados en la base de datos y los muestra en la plantilla `shop.html`. Esta ruta no requiere autenticación y está diseñada para ser utilizada por cualquier usuario que visite la plataforma.

- **Respuesta Exitosa (Render HTML):** 
  La plantilla `shop.html` mostrará los empleos en formato de lista con la siguiente estructura de datos para cada empleo:
    ```json
    {
        "nombre_empleo": "Desarrollador Backend",
        "descripcion": "Responsable del desarrollo y mantenimiento de APIs.",
        "modalidad_asistencia": "Remoto",
        "tipo_contrato": "Indefinido",
        "funciones": "Diseñar, desarrollar y probar servicios backend.",
        "requisitos": "3 años de experiencia, conocimientos en Flask.",
        "beneficios": "Seguro médico, línea de carrera.",
        "ubicacion": "Lima, Perú",
        "fecha_creacion": "2024-12-01",
        "vacantes": 3,
        "fecha_final": "2025-01-15",
        "salario": "A convenir"
    }
    ```

---

### **5. Registro de Producto**

- **Endpoint:** `/registroproducto`
- **Método:** `GET`
- **Autenticación:** Requerida
- **Descripción:** 
  Permite que una empresa logueada acceda a la plantilla `registroproducto.html`, donde podrá registrar un nuevo empleo.

- **Posibles Errores:**
  - Si el usuario no está autenticado o la empresa no existe, se redirige a la página de login.

---

### **6. Dashboard de la Empresa**

- **Endpoint:** `/dashboard`
- **Método:** `GET`
- **Autenticación:** Requerida
- **Descripción:** 
  Muestra un resumen personalizado de todos los empleos que la empresa ha publicado. Los empleos son filtrados por el `empresa_id` del usuario autenticado.

- **Respuesta Exitosa (Render HTML):**
  La plantilla `dashboard.html` incluirá:
  - Lista de empleos de la empresa con los siguientes campos:
    ```json
    {
        "nombre_empleo": "Desarrollador Fullstack",
        "descripcion": "Desarrollar soluciones frontend y backend.",
        "ubicacion": "Remoto",
        "vacantes": 2,
        "fecha_final": "2025-01-20",
        "salario": "S/ 5000",
        "tipo_contrato": "Indefinido",
        "modalidad_asistencia": "Remoto"
    }
    ```

- **Posibles Errores:**
  - Si el usuario no está autenticado o no tiene empleos publicados, se redirige a la página de login.

---

### **7. Detalles de un Empleo**

- **Endpoint:** `/detallesempleo`
- **Método:** `GET`
- **Descripción:**
  Permite visualizar los detalles completos de un empleo específico. La información se pasa como un parámetro de consulta (`id`) y se renderiza en la plantilla `detallesempleo.html`.

- **Parámetros de Consulta:**
    - `id` (String): Identificador único del empleo.

- **Respuesta Exitosa (Render HTML):**
  La plantilla mostrará todos los campos del empleo, incluyendo nombre, descripción, funciones, beneficios, requisitos, y todos los demás campos pertenecientes a un empleo.

---

## Flujo del Frontend

### Página Principal
La página principal de **Laboral.AI** tiene los siguientes elementos clave:
1. **Descripción de la Startup:**  
   Breve explicación sobre cómo **Laboral.AI** conecta empresas y empleados utilizando inteligencia artificial.
2. **Empresas Asociadas:**  
   Un carrusel o listado de logos de empresas que respaldan la plataforma.
3. **Call to Action (CTA):**  
   Botones destacados para que las empresas puedan registrarse y publicar empleos, o para que los postulantes accedan al listado de empleos.

### Página de Listado de Empleos (`shop.html`)
- Muestra una lista de empleos disponibles con información como nombre, ubicación, modalidad de asistencia, y fecha límite de postulación.
- Cada empleo tiene un botón o enlace que lleva a la página de detalles (`/detallesempleo?id=<id>`).

### Página de Registro de Producto (`registroproducto.html`)
- Permite que una empresa registre un empleo o producto en la plataforma.
- Incluye un formulario con los campos requeridos para el registro, como nombre, descripción, salario, requisitos, y beneficios.

### Página del Dashboard (`dashboard.html`)
- Proporciona un resumen de todos los empleos publicados por la empresa logueada.
- Incluye:
  - Botones para editar o eliminar empleos.
  - Boton de ir a empleo y de copiar enlace del empleo.

### Página de Detalles de Empleo (`detallesempleo.html`)
- Muestra la información completa de un empleo seleccionado, incluyendo el nombre de la empresa y los detalles del puesto.
- Incluye un botón para que el postulante envíe su solicitud llenando sus datos en un formulario de Google.

---

## Mejoras Futuras

1. **Filtrado y Búsqueda Avanzada:**
   - Implementar filtros por ubicación, modalidad de asistencia, salario, y tipo de contrato en el listado de empleos.

2. **Panel Administrativo:**
   - Añadir un panel para los administradores de la plataforma, donde puedan gestionar empresas y empleos.

3. **Notificaciones por Correo:**
   - Enviar notificaciones a las empresas cuando reciban nuevas postulaciones.

4. **Estadísticas para Empresas:**
   - Mostrar métricas detalladas en el dashboard, como el número de visitas y postulaciones por empleo.

5. **Mobile-Friendly Design:**
   - Optimizar las páginas para dispositivos móviles.

---

## Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo `LICENSE` para más detalles.
