from datetime import timedelta

from flask import Flask
from flask_login import LoginManager
from flask_wtf import CSRFProtect
from werkzeug.middleware.proxy_fix import ProxyFix

from config import Config
from models import db, Usuario
from routes import main_bp

login_manager = LoginManager()
csrf = CSRFProtect()


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

    @login_manager.user_loader
    def load_user(user_id):
        return Usuario.query.get(int(user_id))

    app.register_blueprint(main_bp)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=app.config.get("DEBUG", False))
