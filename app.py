"""
Punto de entrada de la aplicación Flask.
Proyecto: Portfolio personal - Michael Ramiro Cáceres
"""

from flask import Flask
from flask_login import LoginManager
from flask_wtf import CSRFProtect
from config import Config
from models import db, Usuario
from routes import main_bp

# Extensiones
login_manager = LoginManager()
csrf = CSRFProtect()


def create_app():
    """Crea y configura la aplicación Flask."""
    app = Flask(__name__)
    app.config.from_object(Config)

    # Inicializa extensiones
    db.init_app(app)
    csrf.init_app(app)  # Protección CSRF para formularios Flask-WTF
    login_manager.init_app(app)
    login_manager.login_view = "main.login"

    # Carga el usuario para Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        return Usuario.query.get(int(user_id))

    # Registro de rutas (Blueprint principal)
    app.register_blueprint(main_bp)

    return app


# Permite ejecutar la aplicación directamente con: python app.py
if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
