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
3. Verificar que `.env` NO se haya subido (ya está incluido en `.gitignore`).

## 2. Publicación en PythonAnywhere (opción sencilla)
1. Crear una cuenta en https://www.pythonanywhere.com
2. Subir el proyecto o clonarlo desde GitHub.
3. Crear un entorno virtual e instalar dependencias:
   ```
   pip install -r requirements.txt
   ```
4. Crear el archivo `.env` con los datos reales de la base de datos.
5. En la sección "Databases" crear una base MySQL y ejecutar `database/schema.sql` y `database/insertar_datos.sql`.
6. Crear el usuario administrador con `python crear_admin.py`.
7. En la sección "Web", configurar el archivo WSGI para que use `wsgi.py` (variable `application`).
8. Recargar la web y probar.

## 3. Publicación en Render (opción alternativa)
1. Subir el proyecto a GitHub.
2. Crear un "Web Service" en Render conectado al repositorio.
3. Configurar las variables de entorno (`SECRET_KEY`, `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD`, `DB_NAME`).
4. Comando de inicio sugerido (requiere agregar gunicorn en el servidor):
   ```
   gunicorn wsgi:application
   ```
5. Usar una base MySQL externa y ejecutar los scripts SQL.

## 4. Recomendaciones antes de publicar
- Cambiar la `SECRET_KEY` por una clave larga y privada.
- No subir `.env` ni contraseñas al repositorio.
- Colocar el CV real en `static/docs/cv.pdf`.
- Probar el login y el formulario de contacto en el sitio publicado.
