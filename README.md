# Jeas-practice - API REST con FastAPI y PostgreSQL

Proyecto de práctica para la construcción de una API RESTful utilizando FastAPI, PostgreSQL, SQLAlchemy y Pydantic, con soporte para despliegue y desarrollo mediante contenedores Docker y Docker Compose.

---

## Tabla de Contenido

- [Descripcion](#descripcion)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Requisitos Previos](#requisitos-previos)
- [Guia de Ejecucion](#guia-de-ejecucion)
  - [Opcion 1: Ejecucion con Docker y Docker Compose (Recomendada)](#opcion-1-ejecucion-con-docker-y-docker-compose-recomendada)
  - [Opcion 2: Ejecucion Local con Entorno Virtual](#opcion-2-ejecucion-local-con-entorno-virtual)
- [Documentacion Interactiva](#documentacion-interactiva)
- [Endpoints de la API](#endpoints-de-la-api)
  - [Detalle y Ejemplos de Peticion](#detalle-y-ejemplos-de-peticion)
- [Configuracion de la Base de Datos](#configuracion-de-la-base-de-datos)

---

## Descripcion

El proyecto implementa un servicio backend para la gestion basica de usuarios (CRUD: Crear, Leer, Actualizar y Eliminar). Aplica el patron de separacion de responsabilidades dividiendo el codigo en modelos de base de datos, esquemas de validacion de datos y operaciones CRUD desacopladas del enrutador principal.

---

## Tecnologias Utilizadas

- Python 3.11
- FastAPI (framework web asincrono de alto rendimiento)
- SQLAlchemy (ORM para mapeo objeto-relacional)
- Pydantic v2 (validacion y serializacion de esquemas de datos)
- PostgreSQL 15 (sistema de gestion de base de datos relacional)
- Psycopg2 (driver de conexion para PostgreSQL en Python)
- Uvicorn (servidor ASGI)
- Docker y Docker Compose (virtualizacion y orquestacion de contenedores)

---

## Estructura del Proyecto

```text
Jeas-practice/
|-- src/
|   |-- crud.py             # Logica de acceso a datos (queries de SQLAlchemy)
|   |-- database.py         # Configuracion del engine, sesion y Base de SQLAlchemy
|   |-- models.py           # Definicion de tablas de base de datos (modelos ORM)
|   |-- schemas.py          # Modelos de Pydantic para validacion de entrada/salida
|-- Dockerfile              # Definicion de la imagen Docker para la API
|-- docker-compose.yml      # Orquestacion de servicios (API y Base de Datos)
|-- entrypoint.sh           # Script auxiliar de inicializacion
|-- main.py                 # Punto de entrada de la aplicacion y definicion de rutas
|-- requirements.txt        # Dependencias del proyecto
|-- README.md               # Documentacion del proyecto
```

### Descripcion de Modulos

- `main.py`: Inicializa la aplicacion FastAPI, crea las tablas al arrancar la aplicacion, gestiona la inyeccion de dependencias para la sesion de la base de datos (`get_db`) y expone las rutas HTTP.
- `src/database.py`: Define la cadena de conexion hacia PostgreSQL, el motor (`engine`), la fabrica de sesiones (`SessionLocal`) y la clase base declarativa (`Base`).
- `src/models.py`: Declara el modelo `Usuario` correspondiente a la tabla `usuarios` en PostgreSQL.
- `src/schemas.py`: Define las estructuras `UsuarioCreate` y `UsuarioResponse` mediante Pydantic para validar entradas y formatear respuestas.
- `src/crud.py`: Funciones reutilizables que interactuan con la base de datos (obtener por ID, obtener por email, listar paginado, crear, modificar y eliminar).
- `Dockerfile`: Especifica la imagen base `python:3.11-slim`, instala requerimientos y define el comando de inicio con Uvicorn.
- `docker-compose.yml`: Levanta dos servicios intercomunicados: `db` (PostgreSQL 15) y `api` (FastAPI), configurando variables de entorno, mapeo de puertos y volumenes persistentes.

---

## Requisitos Previos

Dependiendo del metodo de ejecucion que elija:

- Para ejecucion con contenedores:
  - Docker (v20.10 o superior)
  - Docker Compose (v2.0 o superior)
- Para ejecucion local en el sistema:
  - Python 3.11 instalado
  - PostgreSQL 15 en ejecucion (local o remoto)

---

## Guia de Ejecucion

### Opcion 1: Ejecucion con Docker y Docker Compose (Recomendada)

Este metodo levanta automaticamente la base de datos PostgreSQL y la aplicacion FastAPI en red interna compartida.

1. Clonar el repositorio o situarse en el directorio raiz del proyecto:

   ```bash
   cd /ruta/hacia/Jeas-practice
   ```

2. Construir la imagen y levantar los contenedores en segundo plano:

   ```bash
   docker compose up -d --build
   ```

3. Verificar que los contenedores esten en ejecucion:

   ```bash
   docker compose ps
   ```

   Deberia observar dos contenedores activos:
   - `postgres_fastapi` en el puerto `5433:5432`
   - `fastapi_backend` en el puerto `8000:8000`

4. Visualizar los logs en tiempo real (opcional):

   ```bash
   docker compose logs -f api
   ```

5. Detener los contenedores:

   ```bash
   docker compose down
   ```

   Si desea detener y eliminar los volumenes asociados (se borraran los datos almacenados):

   ```bash
   docker compose down -v
   ```

---

### Opcion 2: Ejecucion Local con Entorno Virtual

Si prefiere ejecutar la aplicacion directamente en su maquina sin el contenedor de la API:

1. Crear y activar un entorno virtual de Python:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

2. Instalar las dependencias necesarias:

   ```bash
   pip install --no-cache-dir -r requirements.txt
   ```

3. Configurar la conexion a PostgreSQL:
   En `src/database.py`, la URL por defecto apunta al host de Docker (`db`). Para ejecucion local con una base de datos PostgreSQL corriendo en su host (por ejemplo, en `localhost:5432` o `localhost:5433`), ajuste la variable `SQLALCHEMY_DATABASE_URL`:

   ```python
   SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://admin:adminpassword@localhost:5432/fastapi_db"
   ```

4. Iniciar el servidor de desarrollo:

   ```bash
   uvicorn main:app --host 127.0.0.1 --port 8000 --reload
   ```

---

## Documentacion Interactiva

Una vez iniciado el servidor, FastAPI genera documentacion automatica accesible desde el navegador:

- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## Endpoints de la API

| Metodo | Ruta | Descripcion | Codigo de Estado |
| --- | --- | --- | --- |
| GET | `/` | Comprobacion del estado del servicio | 200 OK |
| POST | `/usuarios/` | Registrar un nuevo usuario | 200 OK / 400 Bad Request |
| GET | `/usuarios/` | Listar usuarios con paginacion (`skip`, `limit`) | 200 OK |
| PUT | `/usuarios/{usuario_id}` | Actualizar datos de un usuario existente | 200 OK / 404 Not Found |
| DELETE | `/usuarios/{usuario_id}` | Eliminar un usuario por su ID | 200 OK / 404 Not Found |

---

### Detalle y Ejemplos de Peticion

#### 1. Verificacion del servidor
- **Metodo**: `GET /`
- **Respuesta**:
  ```json
  {
    "mensaje": "¡Base de datos anal...izada y servidor funcionando!"
  }
  ```

#### 2. Crear un usuario
- **Metodo**: `POST /usuarios/`
- **Cuerpo de la peticion**:
  ```json
  {
    "nombre": "Juan Perez",
    "email": "juan.perez@example.com"
  }
  ```
- **Respuesta**:
  ```json
  {
    "id": 1,
    "nombre": "Juan Perez",
    "email": "juan.perez@example.com",
    "activo": true
  }
  ```

#### 3. Listar usuarios
- **Metodo**: `GET /usuarios/?skip=0&limit=10`
- **Respuesta**:
  ```json
  [
    {
      "id": 1,
      "nombre": "Juan Perez",
      "email": "juan.perez@example.com",
      "activo": true
    }
  ]
  ```

#### 4. Actualizar usuario
- **Metodo**: `PUT /usuarios/1`
- **Cuerpo de la peticion**:
  ```json
  {
    "nombre": "Juan Carlos Perez",
    "email": "juan.carlos@example.com"
  }
  ```
- **Respuesta**:
  ```json
  {
    "id": 1,
    "nombre": "Juan Carlos Perez",
    "email": "juan.carlos@example.com",
    "activo": true
  }
  ```

#### 5. Eliminar usuario
- **Metodo**: `DELETE /usuarios/1`
- **Respuesta**:
  ```json
  {
    "id": 1,
    "nombre": "Juan Carlos Perez",
    "email": "juan.carlos@example.com",
    "activo": true
  }
  ```

---

## Configuracion de la Base de Datos

En el archivo `docker-compose.yml`, los valores predeterminados son:

- **Host del contenedor de BD**: `db`
- **Puerto interno contenedor**: `5432`
- **Puerto expuesto al host**: `5433`
- **Usuario**: `admin`
- **Contrasena**: `adminpassword`
- **Nombre de base de datos**: `fastapi_db`
- **Volumen persistente**: `postgres_data` (asegura que la informacion persista al reiniciar contenedores)
