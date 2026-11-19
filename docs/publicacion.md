# Guía de publicación online

## 1. Subir el proyecto a GitHub
1. Crear un repositorio nuevo en GitHub.
2. En la carpeta del proyecto ejecutar:
   ```
   git init
   git add .
   git commit -m "Primera versión del portfolio"
   git branch -M main
   git remote add origin https://github.com/CMRamiro/NOMBRE_DEL_REPO.git
   git push -u origin main
   ```
3. Verificar que `.env` y `.env.txt` NO se hayan subido (ya están incluidos en `.gitignore`). Usar `.env.example` como plantilla.

## 2. Publicación en PythonAnywhere (opción sencilla)
1. Crear una cuenta en https://www.pythonanywhere.com
2. Subir el proyecto o clonarlo desde GitHub.
3. Crear un entorno virtual e instalar dependencias:
   ```
   pip install -r requirements.txt
   ```
4. Crear el archivo `.env` con los datos reales de la base de datos.
 5. En la sección "Databases" crear una base MySQL y ejecutar `database/schema.sql`.
 6. Crear el usuario administrador con `python crear_admin.py` y luego ejecutar `database/insertar_datos.sql` (el perfil inicial se asocia al administrador creado).
 7. En la sección "Web", configurar el archivo WSGI para que use `wsgi.py` (variable `application`).
 8. Recargar la web y probar. Acceder a `/login` para gestionar el contenido desde `/admin`.

## 3. Publicación en Render con MySQL externo (TiDB Cloud Starter)
1. Crear un cluster **TiDB Cloud Starter** compatible con MySQL y una base `portfolio_db` desde la consola de TiDB.
2. En TiDB: **Connect > Public Endpoint**, crear/obtener el usuario (con prefijo), la contraseña y el puerto `4000`. Ubicar el CA del cluster o usar la CA del sistema.
3. En Render: abrir **Connect > Outbound IP Addresses** del Web Service y agregar esos IPs/rangos al allowlist del endpoint público de TiDB.
4. Cargar el esquema y los datos:
   ```
   mysql -h HOST -P 4000 -u USUARIO -p --ssl-mode=VERIFY_IDENTITY --ssl-ca=RUTA_CA < database/schema_externo.sql
   ```
   Definir `ADMIN_NOMBRE`, `ADMIN_EMAIL` y `ADMIN_PASSWORD` en el entorno (en `.env` local o en las variables de Render). La aplicación crea el administrador automáticamente al iniciar, antes de cargar los datos (el perfil inicial se asocia al administrador). Después podés cambiar nombre, correo y contraseña desde **Panel admin > Datos de acceso**. Para forzar el valor de las variables sobre un administrador ya creado, definir `ADMIN_RESET=true` temporalmente y reiniciar.
   Después:
   ```
   mysql -h HOST -P 4000 -u USUARIO -p --ssl-mode=VERIFY_IDENTITY --ssl-ca=RUTA_CA < database/insertar_datos_externo.sql
   ```
   No usar `database/schema.sql` ni `database/insertar_datos.sql` en proveedores externos: incluyen `CREATE DATABASE`/`USE`.
5. En Render crear **Web Service** desde `https://github.com/CMRamiro/portfolio`, rama `main`, región cercana al cluster TiDB y entorno **Python**.
6. Configurar build y start:
   ```
   python -m pip install --upgrade pip && pip install -r requirements.txt
   gunicorn wsgi:application --bind 0.0.0.0:${PORT:-10000} --workers ${WEB_CONCURRENCY:-2} --timeout 120 --access-logfile - --error-logfile -
   ```
   Gunicorn requiere Linux; en Windows probá localmente con `python app.py` o el test client.
7. Variables de entorno en Render (tomar los nombres de `.env.example`):
   - `SECRET_KEY`: clave larga y aleatoria.
   - `FLASK_PRODUCTION=true`, `FLASK_DEBUG=0`.
   - `DB_HOST`, `DB_PORT=4000`, `DB_USER`, `DB_PASSWORD`, `DB_NAME=portfolio_db`.
   - `DB_SSL_CA=/etc/ssl/certs/ca-certificates.crt` (o la ruta del CA descargado), `DB_SSL_VERIFY_IDENTITY=true`.
   - `ADMIN_NOMBRE`, `ADMIN_EMAIL`, `ADMIN_PASSWORD`: obligatorios para crear el administrador al iniciar.
   - `ADMIN_RESET=true`: opcional y temporal, fuerza sobrescribir el administrador existente con las variables anteriores.
   - `WEB_CONCURRENCY=2` (opcional). Render define `PORT` automáticamente.
   - `.python-version` ya fija Python `3.13.5`; alternativamente configurar `PYTHON_VERSION=3.13.5`.
8. En **Health Check Path** poner `/` y desplegar.
9. Verificar `/`, `/login`, `/static/img/cmrfoto.png`, `/static/docs/cv.pdf` y el panel `/admin`.
10. El plan Free de Render no incluye Shell ni one-off jobs: el administrador se crea automáticamente al iniciar con las variables `ADMIN_*`. `crear_admin.py` queda como opción manual.

## 4. Recomendaciones antes de publicar

- Cambiar la `SECRET_KEY` por una clave larga y privada.
- No subir `.env`, `.env.txt` ni contraseñas al repositorio. Si la clave de `.env.txt` fue real, rotarla: sacarla del índice no limpia el historial de Git.
- Colocar el CV real en `static/docs/cv.pdf`.
- Probar el login y el formulario de contacto en el sitio publicado.
