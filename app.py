import os
from datetime import timedelta

from flask import Flask
from flask_login import LoginManager
from flask_wtf import CSRFProtect
from werkzeug.middleware.proxy_fix import ProxyFix
from werkzeug.security import check_password_hash, generate_password_hash

from config import Config
from models import db, Usuario
from routes import main_bp

login_manager = LoginManager()
csrf = CSRFProtect()


def ensure_admin(app):
    nombre = os.getenv("ADMIN_NOMBRE", "").strip()
    email = os.getenv("ADMIN_EMAIL", "").strip().lower()
    password = os.getenv("ADMIN_PASSWORD", "")
    forzar = os.getenv("ADMIN_RESET", "").strip().lower() in {
        "1",
        "true",
        "yes",
        "on",
    }

    if not nombre or not email or not password:
        if app.config.get("PRODUCTION"):
            app.logger.warning(
                "Faltan ADMIN_NOMBRE, ADMIN_EMAIL o ADMIN_PASSWORD: no se creó el administrador."
            )
        return

    with db.engine.begin() as connection:
        db.Model.metadata.create_all(connection)

    administrador = Usuario.query.filter_by(es_admin=True).first()
    if administrador and not forzar:
        return

    usuario = Usuario.query.filter_by(email=email).first() or administrador
    if usuario is None:
        db.session.add(
            Usuario(
                nombre=nombre,
                email=email,
                password_hash=generate_password_hash(password),
                es_admin=True,
            )
        )
        db.session.commit()
        return

    cambios = False
    if not usuario.es_admin:
        usuario.es_admin = True
        cambios = True
    if usuario.nombre != nombre:
        usuario.nombre = nombre
        cambios = True
    if usuario.email != email:
        usuario.email = email
        cambios = True
    try:
        password_valida = check_password_hash(usuario.password_hash, password)
    except ValueError:
        password_valida = False
    if not password_valida:
        usuario.password_hash = generate_password_hash(password)
        cambios = True
    if cambios:
        db.session.commit()


def create_app():
    """Crea y configura la aplicación Flask."""
    app = Flask(__name__)
    app.config.from_object(Config)
    app.wsgi_app = ProxyFix(
        app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_port=1
    )

    if app.config.get("SQLALCHEMY_DATABASE_URI", "").startswith("sqlite"):
        app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {}

    app.config.setdefault("SESSION_COOKIE_HTTPONLY", True)
    app.config.setdefault("SESSION_COOKIE_SAMESITE", "Lax")
    app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(days=7)

    if app.config.get("PRODUCTION"):
        app.config.update(
            SESSION_COOKIE_SECURE=True,
            REMEMBER_COOKIE_SECURE=True,
            PREFERRED_URL_SCHEME="https",
        )

    db.init_app(app)
    csrf.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "main.login"

    with app.app_context():
        try:
            ensure_admin(app)
        except Exception:
            db.session.rollback()
            app.logger.exception("No se pudo crear/actualizar el usuario administrador.")

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(Usuario, int(user_id))

    app.register_blueprint(main_bp)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=app.config.get("DEBUG", False))
