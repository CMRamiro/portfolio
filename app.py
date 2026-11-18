

from flask import Flask
from flask_login import LoginManager
from flask_wtf import CSRFProtect
from config import Config
from models import db, Usuario
from routes import main_bp

login_manager = LoginManager()
csrf = CSRFProtect()


def create_app():
    """Crea y configura la aplicación Flask."""
    app = Flask(__name__)
    app.config.from_object(Config)

    
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
    app.run(debug=True)
