
# 👨‍🌾 Mi App Ganadera - Plataforma de Gestión de Fincas y Ganado

## 🌟 Descripción del Proyecto

**Mi App Ganadera** es un sistema de gestión web desarrollado con **FastAPI** y **SQLAlchemy** diseñado para digitalizar y centralizar el registro y seguimiento de fincas (propiedades) y el ganado asociado (animales) de forma eficiente. Permite a los usuarios crear, leer, actualizar y eliminar (CRUD) información de las fincas y los animales registrados.

## 🚀 Tecnologías Utilizadas

* **Backend:** Python 3.x
* **Framework Web:** [FastAPI](https://fastapi.tiangolo.com/)
* **ORM:** [SQLAlchemy](https://www.sqlalchemy.org/)
* **Base de Datos:** SQLite (para desarrollo local)
* **Plantillas (Frontend):** Jinja2 (para renderizar vistas HTML)
* **Servidor de Desarrollo:** Uvicorn


### 🚜 Logica de Negocio


La Lógica de Negocio de la Plataforma Ganadera se centra en garantizar la integridad de las relaciones y la unicidad de los datos. Para las Fincas, la regla principal es que el nombre debe ser único y, crucialmente, la eliminación de una finca debe eliminar en cascada todo el Ganado asociado para mantener la coherencia (usando la configuración de cascade en SQLAlchemy). Para el Ganado, la regla fundamental es la unicidad de la identificacion y la obligatoriedad de la asociación a una finca y un tipo de animal válidos (Integridad Referencial). Toda esta lógica se ejecuta en los routers de FastAPI, apoyándose en Pydantic para validar los datos entrantes y en db.commit() con setattr() para la persistencia de las actualizaciones. Finalmente, la lógica de interfaz exige una recarga de página inmediata en el frontend después de cada actualización exitosa (PUT) para sincronizar la vista con los nuevos datos de la base de datos.

### 📑 PARTE TECNICA 

El presente documento detalla la arquitectura, los requisitos y la implementación de la Plataforma de Gestión Ganadera, una solución de software desarrollada con FastAPI y SQLAlchemy para la administración digital de fincas y la información del ganado.

#### 1. REQUISITOS DEL PROYECTO

#### 1.1. REQUISITOS FUNCIONALES (RF)

* **RF01 CRUD Finca:** El sistema debe permitir crear, leer, actualizar y eliminar (CRUD) registros de fincas.

* **RF02 CRUD Ganado:** El sistema debe permitir crear, leer, actualizar y eliminar (CRUD) registros individuales de ganado.

* **RF03 Vistas HTML:** El sistema debe proveer vistas renderizadas con Jinja2 para todas las operaciones principales.

* **RF04 Listado Detallado:** El listado de ganado debe mostrar información relacionada (finca y tipo de animal).

* **RF05 Asociación de Entidades:** Cada animal debe estar asociado obligatoriamente a una única finca y a un único tipo de animal (Integridad Referencial).

#### 1.2. REQUISITOS NO FUNCIONALES (RNF)

* **RNF01 Rendimiento:** El framework debe garantizar respuestas asíncronas de baja latencia (uso de FastAPI).

* **RNF02 Escalabilidad:** La arquitectura debe permitir la migración a bases de datos relacionales robustas (PostgreSQL, MySQL).

* **RNF03 Despliegue:** El proyecto debe ser fácilmente desplegable en servicios PaaS (Render).

* **RNF04 Seguridad:** La aplicación debe mitigar riesgos de inyección SQL (garantizado por el uso del ORM SQLAlchemy).

#### 2. ARQUITECTURA DE CLASES Y MODELOS

Modelos de Base de Datos (models.py):

* **Clase Finca:** Contiene id, nombre, tamaño y ubicacion. Define la relación uno-a-muchos con Ganado.

* **Clase Ganado:** Contiene id, identificacion (única), nombre, edad y claves foráneas para finca_id y tipo_animal_id.

* **Clase TipoAnimal:** Contiene id y nombre (único).

* **Esquemas de Validación (schemas.py):** Se utiliza Pydantic para la serialización y validación de datos en los endpoints API (ej. FincaCreate y GanadoCreate).

#### 3. ENDPOINTS CLAVE Y LÓGICA DE IMPLEMENTACIÓN

* **POST /fincas/:** Crea la instancia del modelo, db.add(), db.commit(), db.refresh().

* **PUT /fincas/{finca_id}:** Actualización: Utiliza setattr() para aplicar los cambios del esquema al objeto SQLAlchemy, seguido de db.commit() y db.refresh().

* **DELETE /fincas/{finca_id}:** db.delete(finca) y db.commit(). La eliminación en cascada de registros de ganado asociados es manejada por el ORM.

* **Lógica de Sincronización (Frontend):** Tras recibir un 200 OK de una operación de edición (PUT), el código JavaScript ejecuta window.location.reload() para forzar la recarga de datos en la plantilla Jinja2.

#### 4. ESTRATEGIA DE DESPLIEGUE

La aplicación se despliega como un Web Service en plataformas PaaS. El comando de inicio es: uvicorn main:app --host 0.0.0.0 --port $PORT.

## 🛠️ Instalación y Configuración Local

### 🧩 1️⃣ Requisitos previos

Antes de iniciar, asegúrate de tener instalado:

- **Python 3.10 o superior**
- **pip** (administrador de paquetes de Python)
- Un editor como **VS Code** o **PyCharm**


# 🚀 Guía de Inicio Rápido

### 🐍 Activación del Entorno Virtual

Sigue estos pasos para configurar y activar el entorno virtual del proyecto:

1.  **Verifica tu versión de Python:**
    Asegúrate de tener instalada una versión compatible de Python ejecutando el siguiente comando:

    ```bash
    python3 --version
    ```

2.  **Crea el Entorno Virtual:**
    Crea un entorno virtual llamado `.venv` en la raíz del proyecto:

    ```bash
    python3 -m venv .venv
    ```

3.  **Activa el Entorno Virtual:**
    Activa el entorno virtual con el siguiente comando:

    ```bash
    source .venv/bin/activate
    ```

**Si sale error al activarlo**
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned

Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

**Para activarlo en Windows**
.\.venv\Scripts\Activate
---

## 🛠 Instalación de Requerimientos

Con el entorno virtual activado, instala todas las dependencias necesarias:

```bash
pip install -r requirements.txt
```
## ▶️ Ejecución del Sistema

Ya con los requerimientos ejecutados y el entorno activado, podrás iniciar el sistema de la siguiente manera:

```bash
uvicorn main:app --reload
```

## 🎉 ¡Disfrutalo!


