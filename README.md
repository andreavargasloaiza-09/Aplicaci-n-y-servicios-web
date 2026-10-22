# Clase 7: Autenticación y Autorización con JWT

## Objetivo

Construir una aplicación web básica con FastAPI que permita autenticar usuarios mediante tokens JWT y controlar el acceso a las operaciones de la API utilizando roles y scopes.

Al finalizar la actividad, el estudiante podrá:

- Crear una API con FastAPI.
- Registrar e iniciar sesión con usuarios.
- Generar y validar tokens JWT.
- Diferenciar autenticación de autorización.
- Proteger endpoints según los permisos del usuario.

## Marco teórico

La autenticación verifica quién es el usuario. La autorización determina qué acciones puede realizar después de iniciar sesión.

JWT —JSON Web Token— es un token firmado que contiene información sobre el usuario y sus permisos. El cliente envía el token en el encabezado de las solicitudes:

```text
Authorization: Bearer <token>
```

En este proyecto se utilizan dos roles:

- `reader`: puede consultar información mediante el scope `read`.
- `editor`: puede consultar y modificar información mediante los scopes `read` y `write`.

## ¿Qué tiene el proyecto?

```text
.
├── backend/
│   ├── auth.py          # Hash de contraseñas, JWT y scopes
│   ├── database.py      # Conexión con SQLite
│   ├── main.py          # Rutas de la API
│   ├── models.py        # Modelos Usuario e Item
│   └── schemas.py       # Esquemas de validación
├── requirements.txt     # Dependencias de Python
└── .env.example         # Variables de configuración
```

La base de datos utilizada es SQLite. Se crea automáticamente como `app.db` al iniciar la aplicación.

## Clonar y ejecutar en la máquina local

Requisitos:

- Python 3.10 o superior.
- Git.

Clonar el repositorio y entrar a la carpeta:

```bash
git clone URL_DEL_REPOSITORIO
cd NOMBRE_DEL_REPOSITORIO
```

Crear y activar el entorno virtual:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

En Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Instalar las dependencias y configurar las variables:

```bash
pip install -r requirements.txt
cp .env.example .env
```

En Windows, copiar `.env.example` manualmente como `.env` si el comando `cp` no está disponible.

Iniciar la API:

```bash
uvicorn backend.main:app --reload
```

La API y su documentación estarán disponibles en:

- API: <http://127.0.0.1:8000>
- Documentación: <http://127.0.0.1:8000/docs>

Desde `/docs` se puede registrar un usuario, iniciar sesión y probar los endpoints protegidos. Para el login se debe usar el formulario OAuth2 disponible en la documentación.

## Subir el proyecto a un repositorio propio

Crear una nueva rama llamada `clase-7`:

```bash
git checkout -b clase-7
```

Agregar los archivos y crear el commit:

```bash
git add .
git commit -m "Implementa clase 7: autenticacion y autorizacion con JWT"
```

En GitHub, crear un repositorio propio vacío. Luego asociarlo como remoto y subir la rama:

```bash
git remote add origin URL_DE_TU_REPOSITORIO
git push -u origin clase-7
```

Verificar en GitHub que la rama `clase-7` y todos los archivos estén disponibles.

No se debe subir el archivo `.env`, porque puede contener secretos. El archivo `.env.example` sí debe permanecer en el repositorio.

Prueba de autenticacion
