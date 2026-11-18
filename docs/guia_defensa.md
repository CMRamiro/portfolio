# Guía breve para la defensa oral

## 1. ¿Qué hace el proyecto?
Portfolio web personal desarrollado con Flask. El visitante puede ver la información pública (perfil, tecnologías, proyectos, formación y contacto). El administrador inicia sesión y modifica el contenido desde un panel privado.

## 2. Recorrido rápido del código
- `app.py`: crea la aplicación y conecta extensiones (SQLAlchemy, CSRF, Login).
- `config.py`: lee las credenciales desde `.env`.
- `models.py`: define las tablas como clases (POO).
- `forms.py`: formularios con validación y CSRF.
- `routes.py`: rutas públicas, login y panel de administración.
- `templates/`: HTML con Jinja2.
- `static/`: estilos, JavaScript, favicon e imágenes.
- `database/`: script SQL y datos iniciales.

## 3. Los cuatro pilares de POO
- **Abstracción**: cada clase de `models.py` representa una entidad real del sistema (Usuario, Perfil, Proyecto, etc.) y solo modela lo necesario.
- **Encapsulamiento**: los datos y comportamientos están dentro de cada clase; por ejemplo, `mostrar_info()` trabaja con los atributos del propio objeto.
- **Herencia**: todas las clases heredan de `db.Model`; `Usuario` además hereda de `UserMixin`.
- **Polimorfismo**: `mostrar_info()` existe en varias clases y cada una devuelve un texto distinto según el tipo de objeto.

## 4. Seguridad
- Contraseñas guardadas con hash (`generate_password_hash`) y verificadas con `check_password_hash`.
- Formularios protegidos con Flask-WTF y CSRF.
- Credenciales fuera del código, en `.env` (no se sube a GitHub).
- El panel admin requiere estar logueado (`@login_required`).

## 5. Requisitos académicos
- Jinja2: `templates/`.
- Iframe: mapa en la sección Formación.
- Iconos: FontAwesome.
- Tipografía: Google Fonts (Poppins).
- Responsive: media queries en `static/css/style.css`.
- Animaciones/transiciones: comentadas en `static/css/style.css`.
- Favicon: `static/img/favicon.svg`.
- CV descargable: `static/docs/cv.pdf` (a incorporar).

## 6. Base de datos
- 6 tablas: usuarios, perfil, formacion_academica, tecnologias, proyectos, mensajes_contacto.
- Relaciones 1 a N entre `perfil` y formación/tecnologías/proyectos mediante `perfil_id`.
- Script: `database/schema.sql`. Datos iniciales: `database/insertar_datos.sql`.

## 7. Preguntas posibles
- ¿Por qué Flask? Porque es liviano, fácil de entender y permite organizar el proyecto por etapas.
- ¿Dónde se usan las variables de entorno? En `config.py`, a través de `python-dotenv`.
- ¿Cómo se protege el formulario de contacto? Con Flask-WTF y token CSRF.
- ¿Qué pasa si la base de datos está vacía? La página muestra contenido por defecto en algunas secciones.
