# 🚀 API REST de Gestión de Usuarios - device_systems

Repositorio correspondiente a la actividad **FastAPI Intermedio: Evolución de device_systems con CRUD Completo, Persistencia de Datos, Manejo de Errores, Swagger/OpenAPI y Dependency Injection**, del programa **Tecnología en Análisis y Desarrollo de Software (ADSO)** del **SENA**.

---

# 📖 Descripción

Este proyecto corresponde a la evolución de la API REST de usuarios desarrollada en la actividad anterior.

La aplicación **device_systems** fue ampliada utilizando **FastAPI**, incorporando persistencia real de datos mediante **SQLite y SQLAlchemy**, además de validaciones con **Pydantic**.

En esta versión se implementó el **CRUD completo** del recurso `users`, permitiendo crear, consultar, actualizar y eliminar usuarios almacenados en una base de datos real.

También se incorporaron mecanismos para el manejo de errores, códigos de estado HTTP, documentación automática mediante **Swagger/OpenAPI**, **ReDoc** y reutilización de lógica mediante **Dependency Injection con `Depends()`**.

Los principales conceptos implementados son:

* FastAPI.
* Uvicorn.
* Pydantic v2.
* SQLAlchemy.
* SQLite.
* Métodos HTTP GET, POST, PUT, PATCH y DELETE.
* Path Parameters.
* Query Parameters.
* Validación de datos.
* Response Models.
* Manejo de errores mediante `HTTPException`.
* Códigos de estado HTTP.
* Dependency Injection con `Depends()`.
* CRUD sobre base de datos.
* Constraints de base de datos.
* Swagger UI.
* ReDoc.
* Documentación OpenAPI.
* Persistencia de datos.

---

# 🎯 Objetivo del proyecto

Transformar la API inicial de gestión de usuarios en una API REST más completa y organizada, implementando operaciones CRUD sobre una base de datos real, validaciones, manejo de errores y reutilización de lógica mediante Dependency Injection.

La API permite:

* Crear usuarios.
* Listar usuarios.
* Consultar usuarios por ID.
* Consultar usuarios por email.
* Filtrar usuarios por rol.
* Filtrar usuarios por estado.
* Ordenar usuarios por fecha de creación.
* Actualizar completamente un usuario.
* Actualizar parcialmente un usuario.
* Eliminar usuarios.
* Validar los datos recibidos.
* Aplicar constraints en la base de datos.
* Controlar errores mediante respuestas HTTP.
* Utilizar códigos de estado apropiados.
* Documentar automáticamente la API.
* Persistir los datos en SQLite.

---

# 🔄 Cambios realizados respecto a la versión anterior

La versión anterior de `device_systems` trabajaba principalmente con datos almacenados en memoria.

En esta nueva versión se incorporaron cambios importantes:

* Persistencia real mediante **SQLite**.
* Integración de **SQLAlchemy** para trabajar con la base de datos.
* Creación del modelo `User`.
* Creación de la tabla `users`.
* Separación entre modelos SQLAlchemy y schemas Pydantic.
* CRUD completo sobre la base de datos.
* Validaciones mediante Pydantic.
* Constraints para proteger la integridad de los datos.
* Manejo de errores mediante `HTTPException`.
* Consulta de usuarios por email.
* Filtros por rol y estado.
* Ordenamiento por fecha de creación.
* Actualización completa mediante PUT.
* Actualización parcial mediante PATCH.
* Eliminación mediante DELETE.
* Persistencia de los usuarios incluso después de reiniciar la API.
* Documentación mediante Swagger UI y ReDoc.
* Manejo de la sesión de base de datos mediante dependencias.

De esta manera, `device_systems` pasó de manejar información temporal a utilizar una base de datos real para almacenar los usuarios.

---

# 📂 Estructura del proyecto

La estructura del proyecto se encuentra organizada por responsabilidades.

```text
device_systems/
│
├── app/
│   │
│   ├── database/
│   │   ├── __init__.py
│   │   └── connection.py
│   │
│   ├── dependencies/
│   │   ├── database_dependency.py
│   │   └── user_dependencies.py
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   └── user_model.py
│   │
│   ├── routes/
│   │   ├── __init__.py
│   │   └── user_routes.py
│   │
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── user_schema.py
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   └── user_service.py
│   │
│   ├── __init__.py
│   └── main.py
│
├── docs/
│   └── capturas/
│
├── tests/
│   └── test_user_api.py
│
├── .gitignore
├── device_systems.db
├── README.md
└── requirements.txt
```

### 📸 Evidencia de la estructura

![Estructura del proyecto](docs/capturas/estructura_proyecto_01.png)

![Estructura de servicios](docs/capturas/estructura_service_02.png)

La organización permite separar la conexión a la base de datos, los modelos, schemas, rutas, servicios y dependencias.

---

# 🗄️ Base de datos

La aplicación utiliza **SQLite** como sistema de base de datos.

El archivo generado es:

```text
device_systems.db
```

Dentro de la base de datos se encuentra la tabla:

```text
users
```

La información creada mediante la API se almacena de forma persistente en esta base de datos.

### 📸 Evidencia de la base de datos generada

![Base de datos device\_systems](docs/capturas/device_systems.db.png)

Esta evidencia muestra la base de datos generada para almacenar los usuarios del sistema.

---

# ⚙️ Configuración de SQLAlchemy

La configuración de SQLAlchemy se encuentra en:

```text
app/database/connection.py
```

Se utiliza SQLite mediante la siguiente URL:

```python
DATABASE_URL = "sqlite:///./device_systems.db"
```

Posteriormente se crea el motor de conexión:

```python
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    future=True,
)
```

También se configura la sesión que será utilizada para realizar las operaciones sobre la base de datos:

```python
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)
```

La aplicación utiliza una base declarativa para definir los modelos de SQLAlchemy.

Las tablas se crean mediante:

```python
Base.metadata.create_all(bind=engine)
```

De esta forma, SQLAlchemy permite trabajar con la base de datos desde Python y realizar las operaciones CRUD sin tener que escribir cada consulta SQL manualmente.

### 📸 Evidencia de conexión SQLite

![Conexión SQLite](docs/capturas/conexion_SQLite.png)

---

# 👤 Modelo User

El modelo `User` representa la tabla `users` dentro de la base de datos.

Se encuentra en:

```text
app/models/user_model.py
```

El modelo contiene los siguientes campos:

```python
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    role = Column(String(20), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
```

## 🔐 Constraints aplicados

El modelo SQLAlchemy aplica diferentes restricciones:

| Campo        | Constraint / configuración          |
| ------------ | ----------------------------------- |
| `id`         | Clave primaria                      |
| `name`       | Obligatorio                         |
| `email`      | Único y obligatorio                 |
| `role`       | Obligatorio                         |
| `is_active`  | Obligatorio y con valor por defecto |
| `created_at` | Fecha de creación automática        |

El constraint `unique=True` aplicado al email evita que dos usuarios tengan el mismo correo electrónico.

---

# 🔀 Diferencia entre modelo SQLAlchemy y schema Pydantic

Aunque ambos representan información relacionada con los usuarios, tienen funciones diferentes.

## 🔵 Modelo SQLAlchemy

El modelo SQLAlchemy representa la información que será almacenada en la base de datos.

Se encarga de:

* Representar la tabla `users`.
* Definir las columnas.
* Definir los tipos de datos.
* Aplicar constraints.
* Relacionarse con SQLite.
* Permitir guardar, consultar, modificar y eliminar registros.

Ejemplo:

```python
class User(Base):
    __tablename__ = "users"
```

---

## 🟡 Schema Pydantic

Los schemas Pydantic representan la estructura de los datos que recibe y devuelve la API.

Se utilizan principalmente para:

* Validar los datos recibidos.
* Comprobar formatos.
* Establecer restricciones.
* Definir la estructura de las peticiones.
* Definir la estructura de las respuestas.

Ejemplo:

```python
class UserCreate(BaseModel):
    name: str = Field(..., min_length=3)
    email: EmailStr
    role: Literal["admin", "support", "user"]
    is_active: bool = True
```

---

## 📌 Diferencia principal

La diferencia se puede resumir de la siguiente manera:

```text
Pydantic
   ↓
Valida los datos que recibe la API
   ↓
SQLAlchemy
   ↓
Persiste los datos en la base de datos
```

Por lo tanto:

* **Pydantic** se enfoca en validación y serialización.
* **SQLAlchemy** se enfoca en el modelo de persistencia y la interacción con la base de datos.

Ambos son complementarios, pero no cumplen la misma función.

---

# 🔵 CRUD sobre la base de datos

Las operaciones CRUD se encuentran principalmente en:

```text
app/services/user_service.py
```

CRUD significa:

```text
Create  → Crear
Read    → Consultar
Update  → Actualizar
Delete  → Eliminar
```

Las principales funciones implementadas son:

```text
get_all_users()
get_user_by_id()
get_user_by_email()
create_user()
email_exists()
update_user()
patch_user()
delete_user()
```

---

## ➕ Create

La creación de usuarios utiliza SQLAlchemy para agregar un nuevo registro:

```python
db.add(new_user)
db.commit()
db.refresh(new_user)
```

Esto permite guardar permanentemente el usuario en SQLite.

---

## 🔎 Read

La API permite consultar:

* Todos los usuarios.
* Un usuario por ID.
* Un usuario por email.
* Usuarios filtrados por rol.
* Usuarios filtrados por estado.
* Usuarios ordenados por fecha de creación.

---

## ✏️ Update

La API implementa dos tipos de actualización:

### PUT

Actualiza completamente un usuario.

```text
PUT /users/{user_id}
```

### PATCH

Actualiza parcialmente un usuario.

```text
PATCH /users/{user_id}
```

PATCH permite modificar solamente los campos enviados, manteniendo intactos los demás.

### 📸 Evidencia de campos intactos

![Campos intactos](docs/capturas/campos_intactos.png)

---

## 🗑️ Delete

El método DELETE elimina un usuario de la base de datos:

```text
DELETE /users/{user_id}
```

La operación utiliza SQLAlchemy para eliminar el registro y posteriormente confirmar el cambio mediante `commit()`.

---

# 🟡 Validaciones y constraints

La API utiliza Pydantic para validar los datos antes de realizar las operaciones sobre la base de datos.

Ejemplo:

```python
class UserCreate(BaseModel):
    name: str = Field(..., min_length=3)
    email: EmailStr
    role: Literal["admin", "support", "user"]
    is_active: bool = True
```

## Validaciones implementadas

* El nombre es obligatorio.
* El nombre debe tener mínimo 3 caracteres.
* El email debe tener un formato válido.
* El rol solamente puede ser `admin`, `support` o `user`.
* `is_active` debe ser booleano.
* Las actualizaciones parciales utilizan un schema específico.
* Los datos deben cumplir las reglas antes de almacenarse.

## Constraints de la base de datos

SQLAlchemy también aplica restricciones para mantener la integridad de los datos.

Entre ellas:

* Clave primaria para `id`.
* `nullable=False` para campos obligatorios.
* `unique=True` para el email.
* Valor por defecto para `is_active`.
* Valor automático para `created_at`.

Esto permite tener validaciones tanto en la entrada de la API como en la estructura de persistencia.

---

# 🔵 Endpoints de la API

La API implementa las siguientes operaciones:

| Método | Endpoint                  | Función                    |
| ------ | ------------------------- | -------------------------- |
| GET    | `/users/`                 | Lista todos los usuarios   |
| GET    | `/users/{user_id}`        | Busca un usuario por ID    |
| GET    | `/users/email/{email}`    | Busca un usuario por email |
| GET    | `/users/?role=admin`      | Filtra por rol             |
| GET    | `/users/?is_active=true`  | Filtra por estado          |
| GET    | `/users/?is_active=false` | Filtra usuarios inactivos  |
| POST   | `/users/`                 | Crea un usuario            |
| PUT    | `/users/{user_id}`        | Actualiza completamente    |
| PATCH  | `/users/{user_id}`        | Actualiza parcialmente     |
| DELETE | `/users/{user_id}`        | Elimina un usuario         |

Además, la API dispone de:

| Método | Endpoint    | Función                          |
| ------ | ----------- | -------------------------------- |
| GET    | `/`         | Verifica el estado de la API     |
| GET    | `/test-db/` | Comprueba la conexión con SQLite |

---

# 🧪 Evidencia de pruebas de endpoints

## ➕ POST /users/

Permite crear un nuevo usuario en la base de datos.

### Código esperado

```text
201 Created
```

### 📸 Evidencia

![Creación de usuario](docs/capturas/creacion_usuario.png)

---

# 🔎 GET /users/

Permite consultar todos los usuarios almacenados.

### Código esperado

```text
200 OK
```

### 📸 Evidencia

![Listar usuarios](docs/capturas/listar_usuarios.png)

---

# 🔍 GET /users/{user_id}

Permite buscar un usuario mediante su ID.

### Código esperado

```text
200 OK
```

Si el usuario no existe:

```text
404 Not Found
```

### 📸 Evidencia

![Buscar usuario por ID](docs/capturas/buscar_usuario_id.png)

---

# 📧 GET /users/email/{email}

Permite buscar un usuario utilizando su dirección de correo electrónico.

Si existe un usuario asociado al correo, la API devuelve su información.

Si no existe ningún usuario con ese correo, la API devuelve:

```text
404 Not Found
```

### 📸 Evidencia

![Buscar por email](docs/capturas/buscar_por_email.png)

### 📸 Evidencia de correo inexistente

![Correo inexistente](docs/capturas/correo_inexistente.png)

Esta prueba corresponde a la búsqueda de un correo que no pertenece a ningún usuario registrado.

---

# 🔎 Filtros por rol

La API permite filtrar los usuarios utilizando el Query Parameter `role`.

Ejemplo:

```text
GET /users/?role=admin
```

Los roles disponibles son:

```text
admin
support
user
```

### 📸 Evidencia

![Filtración por rol](docs/capturas/filtracion_por_rol.png)

---

# 🟢 Filtro por estado activo

Para consultar solamente los usuarios activos:

```text
GET /users/?is_active=true
```

### 📸 Evidencia

![Filtrado por activo](docs/capturas/filtrado_por_activo.png)

---

# ⚪ Filtro por estado inactivo

Para consultar los usuarios inactivos:

```text
GET /users/?is_active=false
```

### 📸 Evidencia

![Filtrado por inactivo](docs/capturas/filtrado_por_activo_false.png)

---

# 📅 Ordenamiento por fecha de creación

La API permite ordenar los usuarios teniendo en cuenta su fecha de creación.

### 📸 Evidencia

![Orden por creación](docs/capturas/orden_creacion.png)

---

# ✏️ PUT /users/{user_id}

Permite actualizar completamente un usuario.

### 📸 Evidencia de actualización completa

![Actualización completa](docs/capturas/actualizacion_completa.png)

---

# 🩹 PATCH /users/{user_id}

Permite actualizar parcialmente un usuario.

### 📸 Evidencia de actualización parcial

![Actualización parcial](docs/capturas/actualizado_parcialmente.png)

### 📸 Evidencia de campos intactos

![Campos intactos](docs/capturas/campos_intactos.png)

---

# 🗑️ DELETE /users/{user_id}

Permite eliminar un usuario existente de la base de datos.

### 📸 Evidencia

![Eliminar usuario](docs/capturas/eliminar_usuario.png)

---

# 🌐 Estado de la API

El endpoint:

```text
GET /
```

permite verificar que la API se encuentra funcionando correctamente.

### 📸 Evidencia

![Estado de la API](docs/capturas/estado_API.png)

---

# 🗄️ Prueba de conexión con la base de datos

El endpoint:

```text
GET /test-db/
```

permite comprobar que la aplicación puede conectarse correctamente con SQLite.

### 📸 Evidencia

![Conexión SQLite](docs/capturas/conexion_SQLite.png)

---

# 🚫 Manejo de errores controlados

La API utiliza `HTTPException` para controlar diferentes situaciones de error.

Los principales errores controlados son:

* Usuario no encontrado.
* Email duplicado.
* Email inexistente.
* Datos inválidos.
* Eliminación de usuario inexistente.
* Actualización de usuario inexistente.

---

# ❌ Usuario no encontrado

Cuando se consulta un usuario mediante un ID que no existe, la API responde:

```text
404 Not Found
```

### 📸 Evidencia

![Usuario no encontrado](docs/capturas/usuario_nofound.png)

---

# 📩 Email duplicado

La API verifica que el email no esté registrado antes de crear o actualizar un usuario.

Si se intenta utilizar un email que ya pertenece a otro usuario, se controla el error y se devuelve:

```text
400 Bad Request
```

### 📸 Evidencia

![Email duplicado](docs/capturas/validacion_correo.png)

La captura muestra el caso en el que se intenta registrar un usuario utilizando un correo que ya se encuentra registrado.

---

# 📧 Email inexistente

Este caso es diferente al email duplicado.

Cuando se realiza una búsqueda mediante:

```text
GET /users/email/{email}
```

y no existe ningún usuario registrado con ese correo, la API responde:

```text
404 Not Found
```

### 📸 Evidencia

![Email inexistente](docs/capturas/correo_inexistente.png)

---

# ⚠️ Datos inválidos

Cuando los datos enviados no cumplen las reglas establecidas por Pydantic, FastAPI genera una respuesta:

```text
422 Unprocessable Entity
```

Algunos ejemplos son:

* Nombre demasiado corto.
* Email inválido.
* Rol no permitido.
* Tipo de dato incorrecto.

### 📸 Evidencia

![Datos inválidos](docs/capturas/datos_invalidos.png)

---

# 📊 Códigos de estado HTTP

La API utiliza códigos de estado para informar el resultado de cada operación.

| Código | Significado          | Ejemplo                                   |
| ------ | -------------------- | ----------------------------------------- |
| 200    | OK                   | Consulta o actualización exitosa          |
| 201    | Created              | Usuario creado                            |
| 204    | No Content           | Usuario eliminado                         |
| 400    | Bad Request          | Email duplicado                           |
| 404    | Not Found            | Usuario inexistente o email no encontrado |
| 422    | Unprocessable Entity | Datos inválidos                           |

El uso de estos códigos permite que el cliente de la API pueda identificar correctamente el resultado de cada petición.

---

# 💉 Dependency Injection con Depends()

La aplicación utiliza **Dependency Injection** mediante `Depends()`.

Las dependencias se encuentran organizadas en:

```text
app/dependencies/
```

Entre ellas se encuentra la dependencia encargada de proporcionar la sesión de la base de datos.

El uso de `Depends()` permite reutilizar lógica y evita crear manualmente una nueva sesión de base de datos en cada endpoint.

Conceptualmente:

```python
def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
```

Esta dependencia puede ser utilizada en las rutas mediante:

```python
Depends(get_db)
```

De esta forma, cada endpoint puede recibir la sesión de base de datos que necesita para realizar sus operaciones.

También permite centralizar el manejo y cierre de las sesiones.

---

# 🧩 Separación de responsabilidades

La aplicación se encuentra organizada en diferentes capas:

```text
                     Cliente
                        │
                        ▼
                   FastAPI
                        │
                        ▼
                     Routes
                        │
                        ▼
                    Services
                        │
                        ▼
                   SQLAlchemy
                        │
                        ▼
                     SQLite
```

Además, las dependencias proporcionan recursos reutilizables a las rutas.

### Routes

Definen los endpoints y reciben las peticiones HTTP.

### Schemas

Validan y estructuran los datos mediante Pydantic.

### Services

Contienen la lógica necesaria para realizar las operaciones CRUD.

### Models

Representan las tablas de la base de datos mediante SQLAlchemy.

### Database

Contiene la configuración del motor y las sesiones de conexión.

### Dependencies

Permiten reutilizar recursos y lógica mediante `Depends()`.

---

# 📚 Swagger UI y OpenAPI

FastAPI genera automáticamente documentación interactiva mediante **Swagger UI**.

Swagger permite:

* Visualizar los endpoints.
* Consultar parámetros.
* Consultar schemas.
* Ejecutar peticiones.
* Revisar respuestas.
* Probar diferentes escenarios.
* Consultar códigos de estado HTTP.

La documentación se encuentra disponible en:

```text
http://127.0.0.1:8000/docs
```

### 📸 Evidencia Swagger/OpenAPI

![Verificar Swagger OpenAPI](docs/capturas/Verificar%20SwaggerOpenAPI.png)


---

# 📘 ReDoc

FastAPI también proporciona documentación mediante ReDoc.

Se encuentra disponible en:

```text
http://127.0.0.1:8000/redoc
```

### 📸 Evidencia

![ReDoc](docs/capturas/redoc.png)

---

# 🧪 Resumen de pruebas realizadas

Durante el desarrollo se realizaron pruebas para verificar las diferentes funcionalidades de la API.

| Funcionalidad          | Evidencia                       |
| ---------------------- | ------------------------------- |
| Crear usuario          | `creacion_usuario.png`          |
| Listar usuarios        | `listar_usuarios.png`           |
| Buscar por ID          | `buscar_usuario_id.png`         |
| Buscar por email       | `buscar_por_email.png`          |
| Email inexistente      | `correo_inexistente.png`        |
| Filtrar por rol        | `filtracion_por_rol.png`        |
| Filtrar activos        | `filtrado_por_activo.png`       |
| Filtrar inactivos      | `filtrado_por_activo_false.png` |
| Ordenar por creación   | `orden_creacion.png`            |
| Actualización completa | `actualizacion_completa.png`    |
| Actualización parcial  | `actualizado_parcialmente.png`  |
| Campos intactos        | `campos_intactos.png`           |
| Eliminar usuario       | `eliminar_usuario.png`          |
| Estado de la API       | `estado_API.png`                |
| Conexión SQLite        | `conexion_SQLite.png`           |
| Usuario inexistente    | `usuario_nofound.png`           |
| Email duplicado        | `validacion_correo.png`         |
| Datos inválidos        | `datos_invalidos.png`           |
| Base de datos generada | `device_systems.db.png`         |

---

# 🧠 ¿Qué aprendí sobre persistencia de datos en APIs REST?

La persistencia permite que la información de una API se mantenga almacenada aunque la aplicación se cierre o se reinicie.

En una API que utiliza únicamente datos en memoria, la información puede perderse cuando el proceso termina. Al utilizar SQLite y SQLAlchemy, los usuarios quedan almacenados en una base de datos real y pueden ser consultados posteriormente.

También que la persistencia no consiste solamente en guardar información. Es necesario controlar la integridad de los datos mediante validaciones y constraints.

Pydantic permite validar los datos antes de procesarlos, mientras que SQLAlchemy permite definir cómo se representan y almacenan en la base de datos.

El uso de sesiones y operaciones como `add()`, `commit()`, `refresh()` y `delete()` permitió comprender mejor la interacción de la API con la base de datos.

---

# 💡 Reflexión final sobre la importancia de la persistencia

Como la API REST permite conservar la información de manera permanente y mantenerla disponible después de reiniciar la aplicación.

Enseña que la utilización de SQLite y SQLAlchemy permitie que los usuarios creados mediante los endpoints no dependieran únicamente de la memoria del programa.

Esto hace que la API sea más útil para un sistema real, ya que los datos pueden almacenarse, consultarse, modificarse y eliminarse de forma organizada.

Además, la separación entre Pydantic y SQLAlchemy permite que la API tenga una estructura más clara: Al Pydantic encargarse de validar los datos que recibe la aplicación y SQLAlchemy encargarse de representar y persistir esos datos en la base de datos.

Su implementación de persistencia permite comprender que la API REST no solamente debe recibir y responder peticiones, sino que debe poder manejar la información de forma confiable y mantener su integridad.

---

# ▶️ Ejecución del proyecto

Para ejecutar el proyecto se debe tener Python instalado.

## 1. Crear el entorno virtual

```bash
python -m venv .venv
```

## 2. Activar el entorno virtual

En Git Bash:

```bash
source .venv/Scripts/activate
```

En PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

## 3. Instalar las dependencias

```bash
pip install -r requirements.txt
```

## 4. Ejecutar la API

```bash
uvicorn app.main:app --reload
```

La API estará disponible en:

```text
http://127.0.0.1:8000
```

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

ReDoc:

```text
http://127.0.0.1:8000/redoc
```

---

# 📦 Tecnologías utilizadas

| Tecnología     | Uso                                    |
| -------------- | -------------------------------------- |
| 🐍 Python      | Lenguaje de programación               |
| ⚡ FastAPI      | Framework para desarrollar la API REST |
| 🚀 Uvicorn     | Servidor ASGI                          |
| 🟡 Pydantic    | Validación y schemas                   |
| 🗄️ SQLAlchemy | ORM y persistencia                     |
| 💾 SQLite      | Base de datos                          |
| 🌐 Swagger UI  | Documentación y pruebas                |
| 📘 ReDoc       | Documentación OpenAPI                  |
| 🔧 Git         | Control de versiones                   |
| 🐙 GitHub      | Repositorio del proyecto               |

---

# 🛠️ Fases 12 y 13: migraciones, documentación y pruebas

## Migraciones con Alembic

La configuración se encuentra en `alembic.ini` y `alembic/env.py`. La migración inicial está en:

```text
alembic/versions/be59ab221b8d_crear_tablas_users_devices_loans.py
```

Comandos ejecutados:

```powershell
alembic init alembic
alembic revision --autogenerate -m "crear tablas users devices loans"
alembic upgrade head
alembic current
```

La migración crea o controla las tablas `users`, `devices` y `loans`, incluyendo claves foráneas, índices y la restricción única del número de serie.

## Documentación Swagger/OpenAPI

La documentación está organizada mediante los tags:

```text
Users
Devices
Loans
```

Cada endpoint incluye `summary`, `description`, `response_description` y respuestas esperadas. Los schemas Pydantic contienen ejemplos para las peticiones y respuestas relacionadas.

```text
Swagger UI: http://127.0.0.1:8000/docs
ReDoc:      http://127.0.0.1:8000/redoc
```

## Pruebas funcionales mínimas

La prueba automatizada se encuentra en:

```text
tests/test_functional_flow.py
```

Ejecutarla con:

```powershell
python -m pytest tests/test_functional_flow.py -q
```

El flujo cubierto es:

1. Crear usuario.
2. Crear dispositivo.
3. Crear préstamo.
4. Intentar prestar un dispositivo no disponible y recibir `409`.
5. Listar préstamos con usuario y dispositivo.
6. Filtrar préstamos por estado.
7. Filtrar préstamos por tipo de dispositivo.
8. Consultar préstamos de un usuario.
9. Devolver el préstamo.
10. Verificar que el dispositivo vuelva a estar disponible.
11. Consultar el historial del dispositivo.
12. Validar un filtro inválido y recibir `422`.

Endpoints de consultas relacionadas:

```text
GET /loans/details
GET /loans/?status=active
GET /loans/?user_email=aprendiz@sena.edu.co
GET /loans/?device_type=laptop
GET /users/{user_id}/loans
GET /devices/{device_id}/loans
```

## Evidencias para el repositorio

La rama de trabajo solicitada es:

```text
device_systems_alembic_relaciones
```

Antes de entregar el repositorio deben incorporarse en `docs/capturas/` las capturas de:

* `alembic init`.
* `alembic revision --autogenerate`.
* `alembic upgrade head`.
* Estructura de las tablas.
* Swagger y ReDoc.
* Creación de usuario, dispositivo y préstamo.
* Consultas con joins y filtros.
* Devolución y disponibilidad restaurada.

## Reflexión

Alembic permite versionar cambios estructurales de forma controlada y reproducible. Las relaciones entre modelos representan la integridad del dominio: un préstamo pertenece a un usuario y a un dispositivo. Finalmente, los joins y filtros permiten entregar respuestas útiles para la operación sin duplicar información ni realizar consultas desconectadas.

---

# ✅ Conclusión

El proyecto `device_systems` evolucionó de una API básica de gestión de usuarios a una API REST con **persistencia real mediante SQLite y SQLAlchemy**, CRUD completo, validaciones con Pydantic, manejo de errores, filtros, consultas por email, actualización completa y parcial, Dependency Injection y documentación mediante Swagger/OpenAPI y ReDoc.

La separación entre modelos, schemas, servicios, rutas, dependencias y conexión a la base de datos permite mantener una estructura más organizada y facilita el mantenimiento del proyecto.

La implementación de persistencia permitió comprender la importancia de almacenar los datos de manera permanente y de proteger su integridad mediante validaciones y constraints.

---

# 👩‍💻 Autora

**Esthefany Valentina Chávez Parra**

**Tecnología en Análisis y Desarrollo de Software (ADSO)**

**SENA**
